// LLM × 金融 Wiki 前端：讀 pages.json 建目錄，讀 wiki/*.md 顯示內容。
// 網址格式：index.html#/<slug>（見 AGENTS.md §6）
(function () {
  "use strict";

  const TYPE_LABEL = { overview: "總覽", concept: "概念", comparison: "比較與綜合", ideas: "策略點子", source: "來源", meta: "其他" };
  const NAV_ORDER = ["overview", "concept", "comparison", "ideas", "source", "meta"];
  const TIER_LABEL = { A: "A｜同儕審查", B: "B｜預印本／業界／開源", C: "C｜新聞評論" };
  const SPECIAL = { agents: { slug: "agents", path: "AGENTS.md", title: "規則手冊（AGENTS.md）", type: "meta",
    summary: "AI 維護本 wiki 時必須遵守的結構、格式與流程", tags: ["meta"], links: [], sources: [] } };

  const nav = document.getElementById("nav");
  const content = document.getElementById("content");
  const search = document.getElementById("search");
  const sidebar = document.getElementById("sidebar");
  let pages = [];
  let bySlug = {};

  const escapeHtml = (s) => String(s ?? "").replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);

  // ---------- 目錄 ----------
  function renderNav(filter) {
    const q = (filter || "").trim().toLowerCase();
    const match = (p) => !q || [p.title, p.summary, p.slug, ...(p.tags || []), ...(p.aliases || [])]
      .join(" ").toLowerCase().includes(q);
    let html = "";
    for (const type of NAV_ORDER) {
      const group = pages.filter((p) => p.type === type && match(p))
        .sort((a, b) => type === "source" ? String(a.year).localeCompare(String(b.year)) || a.slug.localeCompare(b.slug)
                                          : a.title.localeCompare(b.title, "zh-Hant"));
      if (!group.length) continue;
      html += `<div class="nav-group"><h3>${TYPE_LABEL[type]}（${group.length}）</h3>`;
      for (const p of group) {
        const label = type === "source" ? `${p.year}｜[${p.tier}] ${p.title}` : p.title;
        html += `<a href="#/${p.slug}" data-slug="${p.slug}" title="${escapeHtml(p.summary)}">${escapeHtml(label)}</a>`;
      }
      html += "</div>";
    }
    nav.innerHTML = html || `<p class="nav-empty">找不到「${escapeHtml(filter)}」</p>`;
    markActive();
  }

  function markActive() {
    const slug = currentSlug();
    nav.querySelectorAll("a").forEach((a) => a.classList.toggle("active", a.dataset.slug === slug));
  }

  // ---------- Markdown 處理 ----------
  function stripFrontmatter(text) {
    if (!text.startsWith("---\n")) return text;
    const end = text.indexOf("\n---", 4);
    return end === -1 ? text : text.slice(end + 4).replace(/^\n+/, "");
  }

  function convertWikilinks(md) {
    // 不轉換 ``` 程式碼區塊內的文字
    return md.split(/(```[\s\S]*?```)/g).map((chunk, i) => i % 2 ? chunk :
      chunk.replace(/\[\[([^\]|#]+)(?:\|([^\]]*))?\]\]/g, (_, slug, label) => {
        slug = slug.trim();
        const page = bySlug[slug];
        // 來源頁沒有指定顯示文字時，用「作者 年份」短格式（例如 Kaplan 2020），內文引用比較好讀
        const shortCite = page && page.type === "source"
          ? `${slug.split("-")[1].replace(/^./, (c) => c.toUpperCase())} ${page.year}` : null;
        const text = (label || shortCite || (page ? page.title : slug)).trim();
        return page ? `<a class="wikilink" href="#/${slug}">${escapeHtml(text)}</a>`
                    : `<span class="broken-link" title="找不到頁面：${escapeHtml(slug)}">${escapeHtml(text)}</span>`;
      })).join("");
  }

  // LaTeX：先把 $$...$$ 與 $...$ 換成佔位符，避免 marked 把 _ 和 * 當成粗斜體；
  // Markdown 轉完、過濾後再用 KaTeX 渲染（AGENTS.md §4.6）
  function protectMath(md, store) {
    return md.split(/(```[\s\S]*?```|`[^`\n]*`)/g).map((chunk, i) => i % 2 ? chunk : chunk
      .replace(/\$\$([\s\S]+?)\$\$/g, (_, tex) => `@@MATH${store.push({ tex, display: true }) - 1}@@`)
      .replace(/(^|[^\\$])\$([^\s$](?:[^$\n]*?[^\s$])?)\$/g,
        (_, pre, tex) => `${pre}@@MATH${store.push({ tex, display: false }) - 1}@@`)
    ).join("");
  }

  function restoreMath(html, store) {
    return html.replace(/@@MATH(\d+)@@/g, (_, n) => {
      const { tex, display } = store[Number(n)];
      if (!window.katex) return escapeHtml(display ? `$$${tex}$$` : `$${tex}$`);
      return katex.renderToString(tex, { displayMode: display, throwOnError: false });
    });
  }

  function renderMarkdown(md) {
    const math = [];
    const safe = DOMPurify.sanitize(marked.parse(protectMath(convertWikilinks(md), math)), { ADD_ATTR: ["target"] });
    const html = restoreMath(safe, math);
    const box = document.createElement("div");
    box.className = "markdown";
    box.innerHTML = html;
    box.querySelectorAll("blockquote").forEach((q) => {
      if (/⚠️|🕰️/.test(q.textContent)) q.classList.add("warn");
      if (/📰/.test(q.textContent)) q.classList.add("media");
    });
    box.querySelectorAll("a[href^='http']").forEach((a) => { a.target = "_blank"; a.rel = "noopener"; });
    return box;
  }

  // ---------- 頁面 ----------
  function header(p) {
    const tags = (p.tags || []).map((t) => `<span class="tag">#${escapeHtml(t)}</span>`).join("");
    let html = `<span class="page-type">${TYPE_LABEL[p.type] || p.type}</span>
      <h1>${escapeHtml(p.title)}</h1>
      ${p.summary ? `<p class="summary">${escapeHtml(p.summary)}</p>` : ""}
      <div class="meta-row">${tags}${p.updated ? `<span>最後更新 ${escapeHtml(p.updated)}</span>` : ""}</div>`;
    if (p.type === "source") {
      html += `<dl class="source-box">
        <dt>作者</dt><dd>${escapeHtml(p.authors)}</dd>
        <dt>年份</dt><dd>${escapeHtml(p.year)}</dd>
        <dt>發表</dt><dd>${escapeHtml(p.venue)}</dd>
        <dt>可信度</dt><dd><span class="tier tier-${escapeHtml(p.tier)}">${escapeHtml(TIER_LABEL[p.tier] || p.tier)}</span></dd>
        <dt>原文</dt><dd><a href="${escapeHtml(p.url)}" target="_blank" rel="noopener">${escapeHtml(p.url)}</a></dd>
        <dt>來源卡</dt><dd><a href="${escapeHtml(p.raw)}" target="_blank" rel="noopener">${escapeHtml(p.raw)}</a></dd>
      </dl>`;
    }
    if (p.slug === "overview") {
      const count = (t) => pages.filter((x) => x.type === t).length;
      html += `<div class="stats">
        <div class="stat"><b>${count("source")}</b><span>來源</span></div>
        <div class="stat"><b>${count("concept")}</b><span>概念頁</span></div>
        <div class="stat"><b>${count("comparison")}</b><span>比較頁</span></div>
        <div class="stat"><b>${pages.reduce((n, x) => n + (x.links || []).length, 0)}</b><span>交叉連結</span></div>
      </div>`;
    }
    return html;
  }

  function footer(p) {
    if (p.slug === "index" || p.slug === "agents") return "";
    const linkList = (slugs) => slugs.length
      ? `<ul>${slugs.map((s) => `<li><a href="#/${s}">${escapeHtml(bySlug[s] ? bySlug[s].title : s)}</a></li>`).join("")}</ul>`
      : `<p class="none">（無）</p>`;
    const backlinks = pages.filter((x) => x.slug !== p.slug && (x.links || []).includes(p.slug))
      .map((x) => x.slug).sort();
    let html = `<div class="page-foot">`;
    if (p.type !== "source" && (p.sources || []).length) {
      html += `<div class="foot-card"><h4>📚 本頁依據的來源（${p.sources.length}）</h4>${linkList(p.sources)}</div>`;
    }
    html += `<div class="foot-card"><h4>🔗 反向連結：哪些頁面提到這頁（${backlinks.length}）</h4>${linkList(backlinks)}</div></div>`;
    return html;
  }

  function currentSlug() {
    const m = location.hash.match(/^#\/([a-z0-9-]+)/);
    return m ? m[1] : "overview";
  }

  async function showPage() {
    const slug = currentSlug();
    const p = bySlug[slug] || SPECIAL[slug];
    markActive();
    sidebar.classList.remove("open");
    if (!p) {
      content.innerHTML = `<div class="error-box">找不到頁面「${escapeHtml(slug)}」。<a href="#/index">回到目錄</a></div>`;
      return;
    }
    document.title = `${p.title}｜LLM × 金融 Wiki`;
    try {
      const res = await fetch(p.path, { cache: "no-cache" });
      if (!res.ok) throw new Error(res.status);
      const md = stripFrontmatter(await res.text());
      const page = document.createElement("article");
      page.className = "page";
      page.innerHTML = header(p);
      page.appendChild(renderMarkdown(md));
      page.insertAdjacentHTML("beforeend", footer(p));
      content.replaceChildren(page);
      window.scrollTo(0, 0);
    } catch (err) {
      content.innerHTML = `<div class="error-box">無法讀取 ${escapeHtml(p.path)}。如果是直接打開 index.html，請改用 <code>python3 -m http.server</code> 預覽。</div>`;
    }
  }

  // ---------- 啟動 ----------
  async function init() {
    try {
      const res = await fetch("pages.json", { cache: "no-cache" });
      pages = (await res.json()).pages;
    } catch (err) {
      content.innerHTML = `<div class="error-box">讀不到 pages.json。請先執行 <code>python3 tools/wiki.py build</code>，並用 <code>python3 -m http.server</code> 預覽。</div>`;
      return;
    }
    bySlug = Object.fromEntries(pages.map((p) => [p.slug, p]));
    renderNav();
    search.addEventListener("input", () => renderNav(search.value));
    document.getElementById("menuToggle").addEventListener("click", () => sidebar.classList.toggle("open"));
    window.addEventListener("hashchange", showPage);
    showPage();
  }

  init();
})();
