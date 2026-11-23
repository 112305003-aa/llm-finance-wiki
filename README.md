# LLM × 金融 Wiki

一個依照 [Karpathy LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 模式、由 AI 維護的知識庫，主題是 **LLM 在金融與量化交易上的應用**。

- 🌐 Wiki：<https://112305003-aa.github.io/llm-finance-wiki/>
- 🎞️ 教學簡報：<https://112305003-aa.github.io/llm-finance-wiki/decks/>
- 📘 規則：[AGENTS.md](AGENTS.md)。這份規則是先訪談使用者 11 題、使用者確認需求後才產生的，訪談紀錄在 §11。

## 三層結構

| 層 | 位置 | 說明 |
|---|---|---|
| raw | `raw/` | 來源卡。PDF 只留在本機，不上傳 |
| wiki | `wiki/` | 每個數字都附「來源＋章節」，每份來源都標可信度 A／B／C |
| schema | `AGENTS.md` | Ingest／Query／Lint 的流程，以及簡報 graph |

## 簡報是怎麼做出來的

簡報不是用一句 prompt 生成的，而是跑一個 graph 流程（`tools/deck.py`）：

```
檢索 wiki → 覆蓋率關卡 → 證據卡 → 大綱（人確認）→ 逐頁稿 → 忠實度（腳本＋新對話 AI 審查）→ 渲染 → 渲染檢查 → 交件
```

每個節點的狀態都存成檔案，放在 `decks/<slug>/`。每次執行的紀錄寫在 `state.json`，整理後的報告在 `report.md`。

## 常用指令

```bash
python3 tools/wiki.py build && python3 tools/wiki.py lint
python3 tools/deck.py status 2026-11-23-chatgpt-news-stock
python3 -m http.server 8000
```
