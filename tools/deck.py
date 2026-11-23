#!/usr/bin/env python3
"""教學簡報的 graph 流程（AGENTS.md §6）。

每個節點／關卡是一個子指令；所有狀態存在 decks/<slug>/ 底下的檔案，
執行紀錄寫進 decks/<slug>/state.json（輪數上限也在這裡計算）。

    python3 tools/deck.py <指令> <slug> [參數]

指令：init, approve, retrieve, coverage, check-cards, check-outline,
      check-drafts, review-pack, record-review, render, check-render, report, status, override
"""
from __future__ import annotations

import html
import json
import re
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from wiki import (COND_RE, LINK_RE, PERF_RE, ROOT, SEC_CITE, data_numbers,  # noqa: E402
                  parse_page, strip_noise)

DECKS = ROOT / "decks"
WIKI = ROOT / "wiki"
TEMPLATES = ROOT / "templates"

NODE_CAP = 2        # 同一張卡／同一頁最多重寫 2 次（§6.3）
GRAPH_CAP = 3       # 從 G4／G5 退回的總輪數上限
MIN_PAGES = 3       # 素材下限
MIN_SCORE = 2       # 檢索分數門檻
MAX_BULLETS = 5

GRAPH_TEXT = """brief（👤）→ N1 檢索 → G1 覆蓋率 ─不足→ ⏹ 停，問要不要 ingest
  → N2 證據卡 → G2 卡片檢查 ─不過→ 回 N2（該卡）
  → N3 大綱 → G3 大綱檢查 → 👤 確認
  → N4 逐頁稿 → G4a 忠實度（腳本）＋ G4b AI 審查（新對話）─不過→ 只退回該頁
  → N5 渲染 → G5 渲染檢查（截圖）─不過→ 回 N4 縮短該頁
  → 交件 report.md"""


# ---------------- 狀態 ----------------
class Deck:
    def __init__(self, slug: str):
        self.slug = slug
        self.dir = DECKS / slug
        self.state_path = self.dir / "state.json"
        if self.state_path.exists():
            self.state = json.loads(self.state_path.read_text(encoding="utf-8"))
        else:
            self.state = {"slug": slug, "events": [], "approved": {}, "fail_counts": {}, "graph_rounds": 0}

    def p(self, *parts) -> Path:
        return self.dir.joinpath(*parts)

    def save(self):
        self.state_path.write_text(json.dumps(self.state, ensure_ascii=False, indent=1), encoding="utf-8")

    def log(self, node: str, result: str, detail: str = "", items=None):
        ev = {"time": datetime.now().isoformat(timespec="seconds"), "node": node, "result": result,
              "detail": detail}
        if items:
            ev["items"] = items
        self.state["events"].append(ev)
        self.save()
        print(f"[{node}] {result}  {detail}")
        for it in items or []:
            print("   -", it)

    def last(self, node: str):
        for ev in reversed(self.state["events"]):
            if ev["node"] == node:
                return ev
        return None

    def require(self, node: str, why: str):
        ev = self.last(node)
        if not ev or ev["result"] != "PASS":
            sys.exit(f"⛔ {why}：{node} 尚未 PASS（目前：{ev['result'] if ev else '沒跑過'}）")

    def require_approved(self, what: str):
        if what not in self.state["approved"]:
            sys.exit(f"⛔ {what} 還沒經使用者確認：請使用者確認後執行 deck.py approve {self.slug} {what}")

    def bump(self, key: str) -> int:
        n = self.state["fail_counts"].get(key, 0) + 1
        self.state["fail_counts"][key] = n
        return n

    def fail_round(self, node: str, keys: list[str]) -> bool:
        """記錄失敗；超過上限回傳 True（要停下來找使用者）。"""
        stop = []
        extra = self.state.get("extra_rounds", 0)   # 👤 使用者以 override 授權的額外輪數
        for key in keys:
            if self.bump(key) > NODE_CAP + extra:
                stop.append(key)
        if node in {"G4a", "G4b", "G5"}:
            self.state["graph_rounds"] += 1
            if self.state["graph_rounds"] > GRAPH_CAP + extra:
                stop.append(f"graph（已退回 {self.state['graph_rounds']} 輪）")
        self.save()
        if stop:
            self.log(node, "STOP", "超過重試上限，交給使用者決定（AGENTS.md §6.3）", stop)
            return True
        return False


# ---------------- 解析工具 ----------------
def load_pages() -> dict:
    data = json.loads((ROOT / "pages.json").read_text(encoding="utf-8"))
    out = {}
    for rec in data["pages"]:
        meta, body = parse_page(ROOT / rec["path"])
        rec["body"] = body
        out[rec["slug"]] = rec
    return out


def short_cite(rec: dict) -> str:
    if rec.get("type") != "source":
        return "比較頁「" + rec.get("title", rec["slug"]).split("：")[0] + "」"
    first = str(rec.get("authors", rec["slug"])).split(",")[0].split(" et al")[0].strip()
    surname = first.split()[-1] if first else rec["slug"]
    return f"{surname} {rec.get('year', '')}".strip()


def parse_brief(deck: Deck):
    meta, body = parse_page(deck.p("brief.md"))
    qs = []
    for line in body.splitlines():
        m = re.match(r"-\s*(Q\d+)｜(core|extra)｜(.+?)｜keywords:\s*(.+)$", line.strip())
        if m:
            qs.append({"id": m[1], "core": m[2] == "core", "text": m[3].strip(),
                       "keywords": [k.strip() for k in m[4].split(",") if k.strip()]})
    return meta, qs


CLAIM_RE = re.compile(r"^-\s*\*\*([a-z0-9-]+)\*\*｜(.+)$")


def load_cards(deck: Deck) -> tuple[dict, dict]:
    """回傳 (claims: id → {text, card, tier}, cards: name → meta)。"""
    claims, cards = {}, {}
    for path in sorted(deck.p("cards").glob("*.md")):
        meta, body = parse_page(path)
        cards[path.stem] = {"meta": meta or {}, "body": body, "claims": []}
        for line in body.splitlines():
            m = CLAIM_RE.match(line.strip())
            if m:
                cards[path.stem]["claims"].append(m[1])
                claims.setdefault(m[1], []).append({"text": m[2], "card": path.stem,
                                                     "tier": (meta or {}).get("tier")})
    return claims, cards


def norm_num(n: str) -> str:
    return n.replace("％", "%").replace(" ", "").replace("個基點", "bps").rstrip("%").rstrip("bps").rstrip("bp")


def number_in(n: str, text: str) -> bool:
    core = norm_num(n)
    flat = text.replace(" ", "")
    return core in flat


def parse_outline(deck: Deck):
    text = deck.p("outline.md").read_text(encoding="utf-8")
    blocks = re.split(r"^## Slide (\d+)｜(.+)$", text, flags=re.M)
    slides = []
    for i in range(1, len(blocks), 3):
        num, title, body = int(blocks[i]), blocks[i + 1].strip(), blocks[i + 2]
        get = lambda key: (re.search(rf"^-\s*{key}:\s*(.*)$", body, re.M) or [None, ""])[1].strip()
        claims = [c.strip() for c in get("claims").strip("[]").split(",") if c.strip()]
        slides.append({"n": num, "title": title, "q": [q.strip() for q in get("q").split(",") if q.strip()],
                       "layout": get("layout") or "bullets", "claims": claims})
    return slides


def parse_draft(path: Path):
    meta, body = parse_page(path)
    sections = {}
    for m in re.finditer(r"^## (白話|畫面|講者稿)\s*\n(.*?)(?=^## |\Z)", body, re.M | re.S):
        sections[m[1]] = m[2].strip()
    return meta or {}, sections


# ---------------- 節點與關卡 ----------------
def cmd_init(deck: Deck):
    deck.dir.mkdir(parents=True, exist_ok=True)
    for sub in ["cards", "drafts", "reviews", "shots"]:
        deck.p(sub).mkdir(exist_ok=True)
    if not deck.p("brief.md").exists():
        deck.p("brief.md").write_text((TEMPLATES / "brief.md").read_text(encoding="utf-8"), encoding="utf-8")
    deck.log("init", "DONE", f"建立 decks/{deck.slug}/，請填寫 brief.md 並由使用者確認")


def cmd_approve(deck: Deck, what: str):
    target = {"brief": "brief.md", "outline": "outline.md"}[what]
    path = deck.p(target)
    if what == "outline":
        deck.require("G3", "大綱要先通過 G3 才能確認")
    text = path.read_text(encoding="utf-8")
    if "status:" in text.split("\n---", 1)[0]:
        text = re.sub(r"^status:.*$", "status: confirmed", text, count=1, flags=re.M)
        path.write_text(text, encoding="utf-8")
    deck.state["approved"][what] = datetime.now().isoformat(timespec="seconds")
    deck.log(f"👤 {what}", "APPROVED", "使用者確認")


def cmd_retrieve(deck: Deck):
    deck.require_approved("brief")
    _, qs = parse_brief(deck)
    pages = load_pages()
    out = []
    for q in qs:
        hits = []
        for slug, rec in pages.items():
            if rec["type"] in {"meta", "overview"} or slug in {"index", "log"}:
                continue
            head = " ".join([rec["title"], rec["summary"], *rec.get("aliases", []), *rec.get("tags", [])]).lower()
            body = rec["body"].lower()
            score = sum(3 * head.count(k.lower()) + min(body.count(k.lower()), 5) for k in q["keywords"])
            if score:
                hits.append({"slug": slug, "type": rec["type"], "score": score})
        hits.sort(key=lambda h: -h["score"])
        out.append({**q, "pages": hits})
    deck.p("retrieval.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    lines = [f"# 檢索結果（N1）｜{deck.slug}", "", "| 子問題 | 核心 | 命中的 wiki 頁（分數） |", "|---|---|---|"]
    for q in out:
        pages_txt = "、".join(f"{h['slug']}({h['score']})" for h in q["pages"][:8]) or "（無）"
        lines.append(f"| {q['id']} {q['text']} | {'✓' if q['core'] else ''} | {pages_txt} |")
    deck.p("retrieval.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    deck.log("N1", "DONE", f"{len(out)} 個子問題，結果寫入 retrieval.md")


def cmd_coverage(deck: Deck):
    qs = json.loads(deck.p("retrieval.json").read_text(encoding="utf-8"))
    relevant = sorted({h["slug"] for q in qs for h in q["pages"] if h["score"] >= MIN_SCORE})
    missing = [f"{q['id']} {q['text']}" for q in qs
               if q["core"] and not any(h["score"] >= MIN_SCORE for h in q["pages"])]
    ok = len(relevant) >= MIN_PAGES and not missing
    lines = [f"# 覆蓋率關卡（G1）｜{deck.slug}", "",
             f"- 相關 wiki 頁（分數 ≥ {MIN_SCORE}）：{len(relevant)} 頁（下限 {MIN_PAGES}）",
             f"- 沒有依據的核心子問題：{'、'.join(missing) or '無'}",
             f"- 結果：**{'PASS' if ok else 'STOP'}**", "", "## 相關頁", ""]
    lines += [f"- [[{s}]]" for s in relevant]
    deck.p("coverage.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    if ok:
        deck.log("G1", "PASS", f"{len(relevant)} 個相關頁，核心子問題都有依據")
    else:
        deck.log("G1", "STOP", "素材不足：停下來問使用者要不要先 ingest（不硬寫）", missing or ["相關頁太少"])


def cmd_check_cards(deck: Deck):
    deck.require("G1", "要先通過覆蓋率關卡")
    pages = load_pages()
    claims, cards = load_cards(deck)
    problems = {}

    def bad(card, msg):
        problems.setdefault(card, []).append(msg)

    relevant = re.findall(r"^- \[\[([^\]]+)\]\]", deck.p("coverage.md").read_text(encoding="utf-8"), re.M)
    for slug in relevant:
        if pages.get(slug, {}).get("type") == "source" and slug not in cards:
            bad(slug, "相關來源沒有證據卡（每份來源一張）")
    for cid, entries in claims.items():
        if len(entries) > 1:
            bad(entries[0]["card"], f"claim id {cid} 重複")
    for name, card in cards.items():
        meta = card["meta"]
        src = pages.get(str(meta.get("source")))
        if not src or src["type"] != "source":
            bad(name, f"source「{meta.get('source')}」不是 wiki 來源頁")
            continue
        if str(meta.get("tier")) != str(src.get("tier")):
            bad(name, f"tier {meta.get('tier')} 與來源頁 {src.get('tier')} 不一致")
        if not card["claims"]:
            bad(name, "沒有任何 claim")
        for cid in card["claims"]:
            text = claims[cid][0]["text"]
            if not SEC_CITE.search(text):
                bad(name, f"{cid}：沒有「[[wiki頁]] §章節」引用")
                continue
            cited = [t.split("|")[0].strip() for t in LINK_RE.findall(text)]
            for t in cited:
                if t not in pages:
                    bad(name, f"{cid}：引用的 [[{t}]] 不存在")
            corpus = " ".join(pages[t]["body"] for t in cited if t in pages)
            for n in data_numbers(text):
                if not number_in(n, corpus):
                    bad(name, f"{cid}：數字 {n} 在被引用的 wiki 頁找不到（可能是編造或抄錯）")
            if data_numbers(text) and PERF_RE.search(strip_noise(text)) and not COND_RE.search(text):
                bad(name, f"{cid}：績效數字缺〔期間｜市場｜成本〕")
    total = sum(len(c["claims"]) for c in cards.values())
    if problems:
        items = [f"{card}：{m}" for card, ms in problems.items() for m in ms]
        deck.log("G2", "FAIL", f"{len(problems)} 張卡要回 N2 修改", items)
        deck.fail_round("G2", [f"card:{c}" for c in problems])
    else:
        deck.log("G2", "PASS", f"{len(cards)} 張卡、{total} 條 claim 都有出處，數字都對得上 wiki")


def cmd_check_outline(deck: Deck):
    deck.require("G2", "要先通過卡片檢查")
    meta, qs = parse_brief(deck)
    claims, _ = load_cards(deck)
    slides = parse_outline(deck)
    want = int(meta.get("slides", 10))
    issues = []
    if len(slides) != want:
        issues.append(f"大綱有 {len(slides)} 頁，brief 要 {want} 頁")
    if [s["n"] for s in slides] != list(range(1, len(slides) + 1)):
        issues.append("頁碼不連續")
    for s in slides:
        for c in s["claims"]:
            if c not in claims:
                issues.append(f"Slide {s['n']}：claim {c} 不存在")
        if s["layout"] not in {"cover", "refs"} and not s["claims"]:
            issues.append(f"Slide {s['n']}：內容頁沒有任何 claim 依據")
    covered = {q for s in slides for q in s["q"]}
    for q in qs:
        if q["core"] and q["id"] not in covered:
            issues.append(f"核心子問題 {q['id']} 沒有分配到任何一頁")
    if issues:
        deck.log("G3", "FAIL", "回 N3 修改大綱", issues)
        deck.fail_round("G3", ["outline"])
    else:
        deck.log("G3", "PASS", f"{len(slides)} 頁，每頁都有依據；下一步：👤 使用者確認大綱")


def draft_paths(deck: Deck, n: int):
    return [deck.p("drafts", f"slide-{i:02d}.md") for i in range(1, n + 1)]


def cmd_check_drafts(deck: Deck):
    deck.require_approved("outline")
    meta, _ = parse_brief(deck)
    claims, _ = load_cards(deck)
    outline = {s["n"]: s for s in parse_outline(deck)}
    fails = {}
    for i, path in enumerate(draft_paths(deck, int(meta.get("slides", 10))), 1):
        key = f"slide-{i:02d}"
        if not path.exists():
            fails[key] = ["缺少逐頁稿"]
            continue
        dmeta, sec = parse_draft(path)
        msgs = []
        for need in ["白話", "畫面", "講者稿"]:
            if not sec.get(need):
                msgs.append(f"缺少「{need}」")
        ids = dmeta.get("claims", []) if isinstance(dmeta.get("claims"), list) else []
        layout = dmeta.get("layout", outline.get(i, {}).get("layout", "bullets"))
        unknown = [c for c in ids if c not in claims]
        if unknown:
            msgs.append(f"claims 不存在：{unknown}")
        extra = [c for c in ids if c not in outline.get(i, {}).get("claims", [])]
        if extra and layout not in {"cover", "refs"}:
            msgs.append(f"用了大綱沒分配給這頁的 claim：{extra}（要改大綱請回 N3）")
        evidence = " ".join(e["text"] for c in ids if c in claims for e in claims[c])
        body = "\n".join(sec.values())
        if layout != "refs":
            for n in data_numbers(body):
                if not number_in(n, evidence):
                    msgs.append(f"數字 {n} 不在這頁的 claims 裡（忠實度）")
            if re.search(r"https?://", body):
                msgs.append("出現外部網址（只有參考資料頁可以放）")
        tiers = {e["tier"] for c in ids if c in claims for e in claims[c]}
        if tiers == {"C"}:
            msgs.append("整頁只靠 C 級來源")
        bullets = [l for l in sec.get("畫面", "").splitlines() if re.match(r"^[-*] ", l)]
        if len(bullets) > MAX_BULLETS:
            msgs.append(f"畫面有 {len(bullets)} 點（上限 {MAX_BULLETS}）")
        if msgs:
            fails[key] = msgs
    if fails:
        deck.log("G4a", "FAIL", f"{len(fails)} 頁退回 N4（只改這幾頁）",
                 [f"{k}：{'；'.join(v)}" for k, v in fails.items()])
        deck.fail_round("G4a", list(fails))
    else:
        deck.log("G4a", "PASS", "每頁的數字都能在該頁的 claims 找到，格式正確")


def cmd_review_pack(deck: Deck):
    deck.require("G4a", "腳本忠實度檢查要先通過，才送 AI 審查")
    meta, _ = parse_brief(deck)
    claims, _ = load_cards(deck)
    n = len(list(deck.p("reviews").glob("round-*.md"))) + 1
    prompt = (ROOT / "tools" / "review_prompt.md").read_text(encoding="utf-8")
    parts = [prompt, "", f"# 審查資料（第 {n} 輪）｜讀者：{meta.get('audience')}", ""]
    for i, path in enumerate(draft_paths(deck, int(meta.get("slides", 10))), 1):
        dmeta, sec = parse_draft(path)
        ids = dmeta.get("claims", []) if isinstance(dmeta.get("claims"), list) else []
        parts += [f"## slide-{i:02d}｜{dmeta.get('title', '')}", "", "### 逐頁稿", ""]
        parts += [f"**{k}**\n\n{v}\n" for k, v in sec.items()]
        parts += ["### 這頁可以依據的證據（只有這些）", ""]
        parts += [f"- {c}（{e['tier']} 級）：{e['text']}" for c in ids if c in claims for e in claims[c]]
        parts += ["- （封面或參考資料頁，沒有 claim）"] if not ids else []
        parts.append("")
    out = deck.p("reviews", f"pack-round{n}.md")
    out.write_text("\n".join(parts), encoding="utf-8")
    deck.log("G4b-pack", "DONE", f"已產生 {out.relative_to(ROOT)}；請在**新對話**只給它這個檔案，結果存成 reviews/round-{n}.md")


def cmd_record_review(deck: Deck, n: str):
    meta, _ = parse_brief(deck)
    path = deck.p("reviews", f"round-{n}.md")
    text = path.read_text(encoding="utf-8")
    results = dict(re.findall(r"^\s*(slide-\d\d)\s*:\s*(.+)$", text, re.M))
    want = [f"slide-{i:02d}" for i in range(1, int(meta.get("slides", 10)) + 1)]
    missing = [w for w in want if w not in results]
    if missing:
        sys.exit(f"⛔ 審查結果缺少：{missing}")
    fails = {k: v.split("｜", 1)[-1].strip() for k, v in results.items() if v.strip().upper().startswith("FAIL")}
    if fails:
        deck.log("G4b", "FAIL", f"AI 審查（第 {n} 輪）退回 {len(fails)} 頁", [f"{k}：{v}" for k, v in fails.items()])
        deck.fail_round("G4b", list(fails))
    else:
        deck.log("G4b", "PASS", f"AI 審查（第 {n} 輪）全部通過")


# ---------------- 渲染 ----------------
def protect_math(md: str, store: list) -> str:
    md = re.sub(r"\$\$([\s\S]+?)\$\$", lambda m: f"@@MATH{store.append('$$' + m[1] + '$$') or len(store) - 1}@@", md)
    return re.sub(r"(?<![\\$])\$([^\s$][^$\n]*?)\$", lambda m: f"@@MATH{store.append('$' + m[1] + '$') or len(store) - 1}@@", md)


def md_to_html(md: str) -> str:
    import markdown
    store: list = []
    md = re.sub(r"\[\[([^\]|]+)\|([^\]]+)\]\]", r"\2", md)
    md = re.sub(r"\[\[([^\]]+)\]\]", r"\1", md)
    out = markdown.markdown(protect_math(md, store), extensions=["tables", "sane_lists"])
    return re.sub(r"@@MATH(\d+)@@", lambda m: html.escape(store[int(m[1])], quote=False), out)


def cite_line(ids, claims, pages) -> str:
    """底部「依據」：同一來源的章節合併，例如 Lopez-Lira 2023 §6.1、§6.2。"""
    groups: dict = {}
    for c in ids:
        for e in claims.get(c, []):
            for slug, sec in re.findall(r"\[\[([^\]|]+)(?:\|[^\]]*)?\]\][^（）§]*?§\s*((?:Table|Figure|p\.)\s*[\w.]+|[^\s（）、]+)", e["text"]):
                name = short_cite(pages[slug]) if slug in pages else slug
                secs = groups.setdefault(name, [])
                if f"§{sec}" not in secs:
                    secs.append(f"§{sec}")
    return "；".join(f"{name} {'、'.join(secs)}" for name, secs in groups.items())


def cmd_render(deck: Deck):
    deck.require("G4a", "忠實度檢查要先通過")
    deck.require("G4b", "AI 審查要先通過")
    meta, _ = parse_brief(deck)
    claims, _ = load_cards(deck)
    pages = load_pages()
    sections = []
    for i, path in enumerate(draft_paths(deck, int(meta.get("slides", 10))), 1):
        dmeta, sec = parse_draft(path)
        layout = dmeta.get("layout", "bullets")
        ids = dmeta.get("claims", []) if isinstance(dmeta.get("claims"), list) else []
        title = html.escape(str(dmeta.get("title", "")))
        lead = md_to_html(sec.get("白話", "")).removeprefix("<p>").removesuffix("</p>")
        notes = md_to_html(sec.get("講者稿", ""))
        screen = sec.get("畫面", "")
        cites = cite_line(ids, claims, pages)
        src = f'<div class="src">依據：{html.escape(cites)}</div>' if cites else ""
        if layout == "cover":
            inner = (f'<h1>{title}</h1>\n<p class="subtitle">{lead}</p>\n'
                     f'<div class="meta">{md_to_html(screen)}</div>')
            cls = "slide cover"
        else:
            cols = [md_to_html(c) for c in re.split(r"^<!--\s*col\s*-->$", screen, flags=re.M)]
            body = "".join(f"<div>{c}</div>" for c in cols) if len(cols) > 1 else cols[0]
            klass = "body two-col" if len(cols) > 1 else "body"
            inner = f'<h2>{title}</h2>\n<p class="lead">{lead}</p>\n<div class="{klass}">{body}</div>'
            cls = f"slide layout-{layout}"
        sections.append(f'<section class="{cls}" data-claims="{",".join(ids)}">\n{inner}\n{src}\n'
                        f'<aside class="notes">{notes}</aside>\n</section>')
    title = html.escape(str(meta.get("title", deck.slug)))
    doc = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <!-- 由 tools/deck.py render 從 drafts/ 產生，請勿手改（AGENTS.md §6） -->
  <title>{title}｜LLM × 金融 Wiki</title>
  <link rel="stylesheet" href="../../assets/vendor/katex/katex.min.css">
  <link rel="stylesheet" href="../_theme/deck.css">
</head>
<body>
  <main class="deck" data-slug="{deck.slug}">
{chr(10).join(sections)}
  </main>
  <script src="../../assets/vendor/katex/katex.min.js"></script>
  <script src="../../assets/vendor/katex/contrib/auto-render.min.js"></script>
  <script src="../_theme/deck.js"></script>
</body>
</html>
"""
    deck.p("index.html").write_text(doc, encoding="utf-8")
    write_deck_index()
    deck.log("N5", "DONE", f"渲染 {len(sections)} 頁 → decks/{deck.slug}/index.html")


def write_deck_index():
    rows = []
    for d in sorted(DECKS.iterdir(), reverse=True):
        if d.is_dir() and (d / "index.html").exists() and (d / "brief.md").exists():
            meta, _ = parse_page(d / "brief.md")
            rows.append(f'<li><a href="{d.name}/">{html.escape(str(meta.get("title")))}</a>'
                        f' <span>{d.name[:10]}｜<a href="{d.name}/report.md">檢查紀錄</a></span></li>')
    (DECKS / "index.html").write_text(f"""<!DOCTYPE html>
<html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>教學簡報｜LLM × 金融 Wiki</title><link rel="stylesheet" href="../assets/style.css"></head>
<body><main class="content" style="margin:40px auto;max-width:760px">
<p><a href="../">← 回 wiki</a></p><h1>教學簡報</h1>
<p>每份簡報都由 graph 流程（AGENTS.md §6）從 wiki 產生，附完整檢查紀錄。</p>
<ul>{''.join(rows)}</ul></main></body></html>
""", encoding="utf-8")


def cmd_check_render(deck: Deck):
    from playwright.sync_api import sync_playwright
    meta, _ = parse_brief(deck)
    want = int(meta.get("slides", 10))
    url = deck.p("index.html").resolve().as_uri()
    fails, info = {}, []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1334, "height": 750})
        page.goto(url)
        page.wait_for_timeout(600)
        count = page.evaluate("document.querySelectorAll('.deck .slide').length")
        if count != want:
            fails["deck"] = [f"簡報有 {count} 頁，brief 要 {want} 頁"]
        for i in range(count):
            res = page.evaluate("""(i) => {
              const slides = [...document.querySelectorAll('.deck .slide')];
              slides.forEach((s, k) => s.classList.toggle('active', k === i));
              const s = slides[i], r = s.getBoundingClientRect(), k = r.height / 720;
              let bottom = 0, right = 0;
              s.querySelectorAll('.body *, h1, h2, .lead, .subtitle, .meta *').forEach(el => {
                const b = el.getBoundingClientRect();
                if (b.height === 0) return;
                bottom = Math.max(bottom, (b.bottom - r.top) / k);
                right = Math.max(right, (b.right - r.left) / k);
              });
              const src = s.querySelector('.src');
              const srcBox = src ? src.getBoundingClientRect() : null;
              return { bottom: Math.round(bottom), right: Math.round(right),
                       srcLines: srcBox ? Math.round(srcBox.height / k / 20) : 0,
                       srcRight: srcBox ? Math.round((srcBox.right - r.left) / k) : 0,
                       katexErr: s.querySelectorAll('.katex-error').length,
                       rawMath: /\\$[^$]+\\$/.test(s.querySelector('h1,h2,.body,.lead')?.innerText || '') };
            }""", i)
            key = f"slide-{i + 1:02d}"
            msgs = []
            if res["bottom"] > 720 - 48:
                msgs.append(f"文字超出版面底部（到 {res['bottom']}px，上限 672px）")
            if res["right"] > 1280 - 40:
                msgs.append(f"文字超出右邊界（到 {res['right']}px）")
            if res["srcLines"] > 1 or res["srcRight"] > 1280 - 120:
                msgs.append("底部「依據」那一行換行或撞到頁碼")
            if res["katexErr"] or res["rawMath"]:
                msgs.append("公式渲染失敗")
            page.wait_for_timeout(80)
            page.screenshot(path=str(deck.p("shots", f"{key}.png")))
            info.append(f"{key}：底部 {res['bottom']}px")
            if msgs:
                fails[key] = msgs
        browser.close()
    if fails:
        deck.log("G5", "FAIL", f"{len(fails)} 頁退回 N4 調整", [f"{k}：{'；'.join(v)}" for k, v in fails.items()])
        deck.fail_round("G5", [k for k in fails if k != "deck"])
    else:
        deck.log("G5", "PASS", f"{want} 頁都沒有溢出、公式正常；截圖在 shots/")


# ---------------- 交件 ----------------
def cmd_report(deck: Deck):
    meta, qs = parse_brief(deck)
    ev = deck.state["events"]
    for node in ["G1", "G2", "G3", "G4a", "G4b", "G5"]:
        deck.require(node, "交件前每個關卡都要 PASS")
    lines = [f"# 執行與檢查紀錄｜{meta.get('title')}", "",
             f"- slug：`{deck.slug}`　讀者：{meta.get('audience')}　頁數：{meta.get('slides')}　語言：{meta.get('language')}",
             f"- 簡報：[index.html](index.html)　截圖：[shots/](shots/)　AI 審查：[reviews/](reviews/)",
             f"- 從 G4／G5 退回的總輪數：{deck.state['graph_rounds']}（上限 {GRAPH_CAP}）", "",
             "## Graph", "", "```", GRAPH_TEXT, "```", "", "## 子問題", ""]
    lines += [f"- {q['id']}（{'核心' if q['core'] else '延伸'}）{q['text']}" for q in qs]
    lines += ["", "## 每一步的結果（依時間）", "", "| # | 時間 | 節點 | 結果 | 說明 |", "|---|---|---|---|---|"]
    for k, e in enumerate(ev, 1):
        detail = e["detail"].replace("|", "／")
        if e.get("items"):
            detail += "<br>" + "<br>".join("・" + i.replace("|", "／") for i in e["items"])
        lines.append(f"| {k} | {e['time'][11:16]} | {e['node']} | {e['result']} | {detail} |")
    fails = {}
    for e in ev:
        if e["result"] in {"FAIL", "STOP"}:
            fails[e["node"]] = fails.get(e["node"], 0) + 1
    lines += ["", "## 各關卡被擋下的次數", ""]
    lines += [f"- {n}：{c} 次" for n, c in sorted(fails.items(), key=lambda x: -x[1])] or ["- 無"]
    lines += ["", "## 重寫次數（每張卡／每頁上限 2）", ""]
    lines += [f"- {k}：{v}" for k, v in sorted(deck.state["fail_counts"].items())] or ["- 無"]
    deck.p("report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    deck.log("交件", "DONE", "report.md 已產生")


def cmd_override(deck: Deck, action: str, *args):
    """👤 只有使用者決定後才能執行：extend＝多給一輪；pass <節點>＝人工放行。"""
    if action == "extend":
        reason = " ".join(args) or "使用者決定"
        deck.state["extra_rounds"] = deck.state.get("extra_rounds", 0) + 1
        deck.log("👤 override", "EXTEND", f"使用者授權多一輪（上限變為每頁 {NODE_CAP + deck.state['extra_rounds']} 次、graph {GRAPH_CAP + deck.state['extra_rounds']} 輪）：{reason}")
    elif action == "pass":
        node = args[0]
        deck.log(node, "PASS", f"👤 使用者人工放行：{' '.join(args[1:]) or '使用者決定'}")
    else:
        sys.exit("用法：deck.py override <slug> extend <理由> ｜ deck.py override <slug> pass <節點> <理由>")


def cmd_status(deck: Deck):
    order = ["init", "👤 brief", "N1", "G1", "G2", "G3", "👤 outline", "G4a", "G4b", "N5", "G5", "交件"]
    for node in order:
        e = deck.last(node)
        print(f"{node:10s} {e['result'] if e else '—':9s} {e['detail'] if e else ''}")
    print(f"graph 退回輪數：{deck.state['graph_rounds']}/{GRAPH_CAP}；重寫次數：{deck.state['fail_counts']}")


COMMANDS = {"init": cmd_init, "approve": cmd_approve, "retrieve": cmd_retrieve, "coverage": cmd_coverage,
            "check-cards": cmd_check_cards, "check-outline": cmd_check_outline, "check-drafts": cmd_check_drafts,
            "review-pack": cmd_review_pack, "record-review": cmd_record_review, "render": cmd_render,
            "check-render": cmd_check_render, "report": cmd_report, "status": cmd_status,
            "override": cmd_override}

if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] not in COMMANDS:
        print(__doc__)
        sys.exit(2)
    d = Deck(sys.argv[2])
    if d.state["events"] and d.state["events"][-1]["result"] == "STOP" and sys.argv[1] not in {"status", "approve", "override"}:
        print("⚠️ 上一步是 STOP（需要使用者決定）。使用者處理後再繼續。")
    COMMANDS[sys.argv[1]](d, *sys.argv[3:])
