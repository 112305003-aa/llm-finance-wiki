#!/usr/bin/env python3
"""LLM × 金融 Wiki 的維護工具（只用 Python 標準庫）。

用法：
    python3 tools/wiki.py build   產生 wiki/index.md 與 pages.json
    python3 tools/wiki.py lint    健康檢查；有 ERROR 時回傳非 0
"""
from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
RAW = ROOT / "raw"
AGENTS = ROOT / "AGENTS.md"
PAGES_JSON = ROOT / "pages.json"
INDEX_MD = WIKI / "index.md"

VALID_TYPES = {"source", "concept", "comparison", "ideas", "overview", "meta"}
REQUIRED = ["title", "type", "summary", "tags", "updated"]
SOURCE_REQUIRED = ["authors", "year", "venue", "url", "raw", "tier", "kind"]
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_RE = re.compile(r"\[\[([^\]|#]+)(?:\|[^\]]*)?\]\]")
CITE_RE = re.compile(r"（\[\[[^\]]+\]\][^（）]*）")
GENERATED = {"index"}   # 自動產生的頁面
HUBS = {"overview", "index", "log"}  # 不檢查孤兒的頁面

TYPE_ORDER = [("overview", "總覽"), ("concept", "概念"), ("comparison", "比較與綜合"),
              ("ideas", "策略點子"), ("source", "來源"), ("meta", "其他")]


# ---------- 解析 ----------
def parse_value(raw: str):
    raw = raw.strip()
    if raw.startswith("[") and raw.endswith("]"):
        return [item.strip().strip("'\"") for item in raw[1:-1].split(",") if item.strip()]
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in "'\"":
        return raw[1:-1]
    return raw


def parse_page(path: Path):
    """回傳 (frontmatter dict, body)。沒有 frontmatter 時 dict 為 None。"""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---", 4)
    if end == -1:
        return None, text
    meta = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, sep, value = line.partition(":")
        if sep:
            meta[key.strip()] = parse_value(value.split(" #")[0] if not value.strip().startswith(("'", '"')) else value)
    body = text[end + 4:].lstrip("\n")
    return meta, body


def allowed_tags() -> set[str]:
    """從 AGENTS.md §4.4 讀取標籤清單（規則只寫一個地方）。"""
    text = AGENTS.read_text(encoding="utf-8")
    section = text.split("### 4.4", 1)[1].split("###", 1)[0]
    return set(re.findall(r"`([a-z0-9-]+)`", section))


def collect():
    pages = []
    for path in sorted(WIKI.rglob("*.md")):
        meta, body = parse_page(path)
        pages.append({"path": path, "slug": path.stem, "meta": meta, "body": body})
    return pages


# ---------- build ----------
def build_index_md(pages) -> str:
    today = date.today().isoformat()
    lines = ["---", "title: 目錄", "type: meta",
             "summary: 自動產生的全站目錄（請勿手動編輯）", "tags: [meta]",
             f"updated: {today}", "---", "",
             "> 本頁由 `python3 tools/wiki.py build` 自動產生，請勿手動編輯。", ""]
    usable = [p for p in pages if p["meta"] and p["slug"] not in GENERATED]
    lines.append(f"共 {len(usable)} 頁。")
    for type_key, label in TYPE_ORDER:
        group = sorted((p for p in usable if p["meta"].get("type") == type_key),
                       key=lambda p: (str(p["meta"].get("year", "")), p["slug"]))
        if not group:
            continue
        lines += ["", f"## {label}（{len(group)}）", ""]
        for p in group:
            m = p["meta"]
            extra = f"｜{m.get('year')}｜{m.get('tier')} 級" if type_key == "source" else ""
            lines.append(f"- [[{p['slug']}|{m.get('title', p['slug'])}]]{extra} — {m.get('summary', '')}")
    return "\n".join(lines) + "\n"


def build():
    pages = collect()
    INDEX_MD.write_text(build_index_md(pages), encoding="utf-8")
    pages = collect()  # 重新讀取，包含剛產生的 index.md
    records = []
    for p in pages:
        if not p["meta"]:
            continue
        m = p["meta"]
        records.append({
            "slug": p["slug"],
            "path": p["path"].relative_to(ROOT).as_posix(),
            "title": m.get("title", p["slug"]),
            "type": m.get("type", "meta"),
            "summary": m.get("summary", ""),
            "tags": m.get("tags", []) if isinstance(m.get("tags"), list) else [],
            "aliases": m.get("aliases", []) if isinstance(m.get("aliases"), list) else [],
            "sources": m.get("sources", []) if isinstance(m.get("sources"), list) else [],
            "updated": m.get("updated", ""),
            "links": sorted(set(LINK_RE.findall(p["body"]))),
            **{k: m[k] for k in SOURCE_REQUIRED if k in m},
        })
    PAGES_JSON.write_text(json.dumps({"generated": date.today().isoformat(), "pages": records},
                                     ensure_ascii=False, indent=1), encoding="utf-8")
    counts = {t: sum(r["type"] == t for r in records) for t, _ in TYPE_ORDER}
    print(f"build 完成：{len(records)} 頁 {counts} → wiki/index.md、pages.json")


# ---------- lint ----------
def lint() -> int:
    errors, warnings, todos = [], [], []
    pages = collect()
    tags = allowed_tags()
    slugs = {}
    for p in pages:
        rel = p["path"].relative_to(ROOT).as_posix()
        if p["slug"] in slugs:
            errors.append(f"slug 重複：{rel} 與 {slugs[p['slug']]}")
        slugs[p["slug"]] = rel
        if not SLUG_RE.match(p["slug"]):
            errors.append(f"檔名不是 kebab-case：{rel}")
    inbound = {s: set() for s in slugs}

    for p in pages:
        rel, m, slug = p["path"].relative_to(ROOT).as_posix(), p["meta"], p["slug"]
        if m is None:
            errors.append(f"缺少 frontmatter：{rel}")
            continue
        for key in REQUIRED:
            if not m.get(key):
                errors.append(f"{rel}：frontmatter 缺少 {key}")
        ptype = m.get("type")
        if ptype not in VALID_TYPES:
            errors.append(f"{rel}：type「{ptype}」不合法")
        for tag in m.get("tags", []) if isinstance(m.get("tags"), list) else []:
            if tag not in tags:
                errors.append(f"{rel}：未知標籤「{tag}」（請先加入 AGENTS.md §4.4）")
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(m.get("updated", ""))):
            errors.append(f"{rel}：updated 需為 YYYY-MM-DD")
        for src in m.get("sources", []) if isinstance(m.get("sources"), list) else []:
            if src not in slugs:
                errors.append(f"{rel}：sources 中的「{src}」不存在")
        for target in LINK_RE.findall(p["body"]):
            target = target.strip()
            if target not in slugs:
                errors.append(f"{rel}：壞掉的連結 [[{target}]]")
            elif target != slug:
                inbound[target].add(slug)

        if ptype == "source":
            for key in SOURCE_REQUIRED:
                if not m.get(key):
                    errors.append(f"{rel}：來源頁缺少 {key}")
            raw_path = ROOT / str(m.get("raw", ""))
            if m.get("raw") and not raw_path.is_file():
                errors.append(f"{rel}：找不到 raw 檔 {m.get('raw')}")
            if not rel.startswith("wiki/sources/"):
                errors.append(f"{rel}：source 頁應放在 wiki/sources/")
            concept_links = [t for t in LINK_RE.findall(p["body"])
                             if slugs.get(t, "").startswith(("wiki/concepts/", "wiki/comparisons/"))]
            if len(set(concept_links)) < 2:
                warnings.append(f"{rel}：只連到 {len(set(concept_links))} 個概念／比較頁（規定至少 2 個）")
        if ptype == "source":
            if m.get("tier") not in TIERS:
                errors.append(f"{rel}：tier 只能是 A／B／C")
            if m.get("kind") not in KINDS:
                errors.append(f"{rel}：kind 只能是 {'／'.join(sorted(KINDS))}")
        if ptype in {"concept", "comparison", "ideas"}:
            if not CITE_RE.search(p["body"]):
                warnings.append(f"{rel}：內文沒有任何（[[來源]]）引用")
            if not m.get("sources"):
                warnings.append(f"{rel}：frontmatter 沒有 sources")

    for slug, refs in inbound.items():
        if slug not in HUBS and not refs:
            warnings.append(f"孤兒頁（沒有其他頁連進來）：{slugs[slug]}")
    for raw_file in sorted(RAW.glob("*.md")):
        if raw_file.stem not in slugs:
            warnings.append(f"raw/{raw_file.name} 還沒有對應的來源頁（尚未 ingest）")
    for raw_file in sorted(p for p in RAW.iterdir() if p.is_file() and p.suffix != ".md"):
        if not (RAW / f"{raw_file.stem}.md").exists():
            errors.append(f"raw/{raw_file.name} 缺少同名的 .md 來源卡")
    lint_finance(pages, errors, warnings, todos)

    if PAGES_JSON.exists():
        listed = {r["slug"] for r in json.loads(PAGES_JSON.read_text(encoding="utf-8"))["pages"]}
        if listed != set(slugs):
            errors.append("pages.json 與 wiki/ 不一致：請執行 python3 tools/wiki.py build")
    else:
        errors.append("缺少 pages.json：請執行 python3 tools/wiki.py build")

    for title, items in [("ERROR", errors), ("WARNING", warnings), ("④ 未處理矛盾與待查", todos)]:
        print(f"\n== {title}（{len(items)}）")
        for item in items:
            print("  -", item)
    print(f"\nlint 結果：{len(slugs)} 頁，{len(errors)} 個 ERROR，{len(warnings)} 個 WARNING，{len(todos)} 個待查")
    return 1 if errors else 0


# ---------- 使用者指定的 4 項 lint（AGENTS.md §5.4） ----------
TIERS = {"A", "B", "C"}
KINDS = {"paper", "report", "oss", "news"}
# 「數字」：帶單位（% bps 倍）、有小數點、或 ≥1000 的數量；年份、節號、slug 裡的數字不算
UNIT_NUM = re.compile(r"\d[\d,]*(?:\.\d+)?\s*(?:%|％|bps|bp|個基點|倍)")
DEC_NUM = re.compile(r"(?<![\w.§])\d+\.\d+(?![\w.])")
BIG_NUM = re.compile(r"(?<![\w.§,])\d{1,3}(?:,\d{3})+(?![\d,])|(?<![\w.§,])\d{4,}(?![\d,.])")
PERF_RE = re.compile(r"Sharpe|夏普|報酬|return|alpha|α|勝率|年化|超額|累積|績效", re.I)
COND_RE = re.compile(r"〔期間：[^｜〕]+｜市場：[^｜〕]+｜成本：[^〕]+〕")
SEC_CITE = re.compile(r"\[\[[^\]|]+(?:\|[^\]]*)?\]\][^（）]*?§\s*[\w.]")
SELF_SEC = re.compile(r"§\s*[\w.]")
CITE_SLUGS = re.compile(r"（([^（）]*\[\[[^（）]*)）")


def strip_noise(line: str) -> str:
    """去掉不算「數字」的部分：引用、節號、條件標籤、行內程式碼、公式。"""
    line = re.sub(r"\[\[[^\]]*\]\]", "", line)
    line = re.sub(r"§\s*[\w.]+", "", line)
    line = re.sub(r"`[^`]*`", "", line)
    line = re.sub(r"\$[^$]*\$", "", line)
    line = re.sub(r"〔[^〕]*〕", "", line)
    return line


def data_numbers(line: str) -> list[str]:
    s = strip_noise(line)
    found = UNIT_NUM.findall(s) + DEC_NUM.findall(s)
    for n in BIG_NUM.findall(s):
        if not re.fullmatch(r"(19|20)\d\d", n):
            found.append(n)
    return found


def body_lines(body: str):
    """逐行回傳正文（跳過程式碼區塊與標題）。"""
    fence = False
    for line in body.splitlines():
        if line.strip().startswith("```"):
            fence = not fence
            continue
        if fence or line.lstrip().startswith("#") or not line.strip():
            continue
        if re.fullmatch(r"\|?[\s:|-]+\|?", line.strip()):   # 表格分隔線
            continue
        yield line


def lint_finance(pages, errors, warnings, todos):
    tier = {p["slug"]: p["meta"].get("tier") for p in pages
            if p["meta"] and p["meta"].get("type") == "source"}
    for p in pages:
        m = p["meta"]
        if not m or m.get("type") in {"meta"} or p["slug"] in GENERATED | {"log"}:
            continue
        rel, is_source = p["path"].relative_to(ROOT).as_posix(), m.get("type") == "source"
        for line in body_lines(p["body"]):
            short = line.strip()[:60]
            nums = data_numbers(line)
            # ① 數字要有出處＋章節
            if nums:
                ok = SEC_CITE.search(line) or (is_source and SELF_SEC.search(line))
                if not ok:
                    errors.append(f"{rel}：①數字 {nums[0]} 沒有附「來源＋§章節」：{short}")
            # ③ 績效數字要附條件
            if nums and PERF_RE.search(strip_noise(line)) and not COND_RE.search(line):
                errors.append(f"{rel}：③績效數字缺〔期間｜市場｜成本〕：{short}")
            # ② C 級不能單獨支撐
            if not line.lstrip().startswith("> 📰"):
                cited = [s.split("|")[0].strip() for c in CITE_SLUGS.findall(line)
                         for s in re.findall(r"\[\[([^\]]+)\]\]", c)]
                cited = [s for s in cited if s in tier]
                if cited and all(tier[s] == "C" for s in cited):
                    errors.append(f"{rel}：②只靠 C 級來源支撐（請改放 > 📰 或加 A／B 來源）：{short}")
            # ④ 未處理的矛盾與待查
            if "⚠️" in line and "未處理" in line:
                todos.append(f"{rel}：⚠️ 未處理矛盾：{short}")
            if "❓" in line:
                todos.append(f"{rel}：❓ {short}")


if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else ""
    if command == "build":
        build()
    elif command == "lint":
        sys.exit(lint())
    else:
        print(__doc__)
        sys.exit(2)
