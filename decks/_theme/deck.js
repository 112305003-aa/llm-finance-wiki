// 簡報共用翻頁程式（AGENTS.md §6.4）
// ← → / 空白鍵翻頁、Home/End 跳頭尾、N 講者稿、F 全螢幕；網址 #3 代表第 3 頁
(function () {
  "use strict";
  const slides = Array.from(document.querySelectorAll(".deck .slide"));
  if (!slides.length) return;

  // 進度條、講者稿面板、提示
  const progress = Object.assign(document.createElement("div"), { className: "progress" });
  const notesPanel = Object.assign(document.createElement("div"), { className: "notes-panel" });
  const hint = Object.assign(document.createElement("div"), { className: "hint", textContent: "← → 翻頁　N 講者稿　F 全螢幕" });
  document.body.append(progress, notesPanel, hint);

  // 頁碼
  slides.forEach((s, k) => {
    const no = document.createElement("div");
    no.className = "pageno";
    no.textContent = `${k + 1} / ${slides.length}`;
    s.appendChild(no);
  });

  // 公式（KaTeX auto-render）
  if (window.renderMathInElement) {
    renderMathInElement(document.querySelector(".deck"), {
      delimiters: [{ left: "$$", right: "$$", display: true }, { left: "$", right: "$", display: false }],
      throwOnError: false,
    });
  }

  let current = 0;
  function fit() {
    const scale = Math.min(window.innerWidth / 1280, window.innerHeight / 720) * 0.96;
    document.documentElement.style.setProperty("--scale", scale);
  }

  function show(n) {
    current = Math.max(0, Math.min(slides.length - 1, n));
    slides.forEach((s, k) => s.classList.toggle("active", k === current));
    progress.style.width = `${((current + 1) / slides.length) * 100}%`;
    const notes = slides[current].querySelector("aside.notes");
    notesPanel.innerHTML = `<h4>講者稿｜第 ${current + 1} 頁</h4>` + (notes ? notes.innerHTML : "（這頁沒有講者稿）");
    history.replaceState(null, "", `#${current + 1}`);
  }

  document.addEventListener("keydown", (e) => {
    if (["ArrowRight", "PageDown", " "].includes(e.key)) { e.preventDefault(); show(current + 1); }
    else if (["ArrowLeft", "PageUp"].includes(e.key)) { e.preventDefault(); show(current - 1); }
    else if (e.key === "Home") show(0);
    else if (e.key === "End") show(slides.length - 1);
    else if (e.key.toLowerCase() === "n") notesPanel.classList.toggle("show");
    else if (e.key.toLowerCase() === "f") {
      if (document.fullscreenElement) document.exitFullscreen(); else document.documentElement.requestFullscreen?.();
    }
  });

  // 點擊左右半邊翻頁、手機左右滑動
  document.addEventListener("click", (e) => {
    if (e.target.closest("a, .notes-panel")) return;
    show(current + (e.clientX > window.innerWidth / 2 ? 1 : -1));
  });
  let touchX = null;
  document.addEventListener("touchstart", (e) => { touchX = e.touches[0].clientX; }, { passive: true });
  document.addEventListener("touchend", (e) => {
    if (touchX === null) return;
    const dx = e.changedTouches[0].clientX - touchX;
    if (Math.abs(dx) > 50) show(current + (dx < 0 ? 1 : -1));
    touchX = null;
  });

  window.addEventListener("resize", fit);
  fit();
  show((parseInt(location.hash.slice(1), 10) || 1) - 1);
})();
