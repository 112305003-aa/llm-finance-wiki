# AGENTS.md — LLM × 金融 Wiki 的工作手冊

> 任何 AI agent（Claude Code、Codex、Gemini CLI……）開始工作前，**先完整讀完這份文件**。
> 這份文件是「先討論、後生成」的結果：先用 11 個問題訪談使用者，使用者確認需求摘要後才寫成（見 §11）。
> 規則有衝突時，以這份文件為準；要修改這份文件，先跟使用者討論。

---

## 1. 專案目的

這是一個**由 LLM 維護、人負責挑資料與做決定**的知識庫，主題是 **LLM 在金融與量化交易上的應用**，做法參考 Andrej Karpathy 的 LLM Wiki。

這個知識庫有三種產出，**內容都只能來自 wiki**：

1. **教學 HTML 簡報**（§6）：用 graph 流程產生，第一份的題目是「ChatGPT 看新聞能預測股價嗎？」。
2. **策略點子清單**（`wiki/ideas/`）：從文獻整理出可以回測的交易點子，每個點子都要附出處與限制。
3. **期末專案（財經早報 Wiki）的知識庫**：讓早報裡的「新聞情緒」判斷有文獻依據。

**讀者（兩者兼顧）**：
- 每頁開頭先寫一段白話版，沒有金融或 AI 背景的人也看得懂。
- 內文可以寫專業細節，例如回歸設定、交易成本、Sharpe ratio。
- 術語**第一次出現時**要附一句解釋。

**語言（中英混合）**：敘述用繁體中文；術語、模型名稱、指標保留英文，例如「Sharpe ratio（夏普值，每承擔一單位風險換到多少超額報酬）」。

分工：

| 誰 | 做什麼 |
|---|---|
| 使用者 | 挑選與下載資料；**決定矛盾怎麼寫**；確認簡報大綱 |
| AI | 閱讀來源、寫來源頁與概念頁、加交叉連結、標出矛盾、維護索引與日誌、跑 graph 產生簡報 |

---

## 2. 架構與資料夾

```
llm-finance-wiki/
├── AGENTS.md          ← 本文件（schema）
├── CLAUDE.md          ← 只有一行 @AGENTS.md
├── README.md          ← 給人看的說明
├── index.html         ← wiki 網站入口（GitHub Pages）
├── assets/            ← 網站 CSS / JS；vendor/ 放 marked、DOMPurify、KaTeX（不要修改）
├── pages.json         ← 自動產生（不要手改）
├── raw/               ← 第 1 層：原始來源（只讀）
│   ├── <slug>.md      ← 來源卡：書目、可信度、原文連結（上傳 GitHub）
│   └── <slug>.pdf     ← 全文，只留本機（.gitignore 排除，避免侵權）
├── wiki/              ← 第 2 層：LLM 撰寫的知識頁
│   ├── index.md       ← 自動產生的目錄
│   ├── log.md         ← 工作日誌（只能往後加）
│   ├── overview.md    ← 總覽與目前的主論點
│   ├── sources/       ← 每份來源一頁
│   ├── concepts/      ← 每個概念一頁
│   ├── comparisons/   ← 比較頁，含矛盾的處理結果
│   └── ideas/         ← 策略點子清單
├── decks/             ← 產出：教學簡報（graph 的工作區，§6）
│   ├── _theme/        ← 共用樣式與翻頁程式
│   ├── index.html     ← 簡報列表
│   └── <slug>/        ← 一份簡報一個資料夾，每個節點的狀態都存成檔案
├── templates/         ← 範本
└── tools/
    ├── wiki.py        ← build／lint
    ├── deck.py        ← graph 的每個節點與關卡
    └── review_prompt.md ← AI 審查用的提示詞（新對話使用）
```

| 層 | 誰寫 | 規則 |
|---|---|---|
| `raw/` | 使用者提供，AI 建來源卡 | **建立後不可修改或刪除** |
| `wiki/` | AI | 每個事實都要能追溯到來源＋章節 |
| `decks/` | AI 透過 `tools/deck.py` | 只能根據 wiki；每個節點只讀寫自己的檔案（§6.2） |
| `AGENTS.md`、`templates/`、`tools/` | 人和 AI 討論後修改 | 修改前先問使用者 |

---

## 3. 命名規則

- 檔名一律用**小寫英文加連字號**。slug 在整個 `wiki/` 中不可重複。
- 來源：`年份-第一作者姓氏-關鍵字`，例如 `2023-lopez-lira-chatgpt-forecast`。`raw/` 和 `wiki/sources/` 用同一個 slug。
- 概念：英文全名，例如 `look-ahead-bias`，不用縮寫當檔名（縮寫放 `aliases`）。
- 比較：`甲-vs-乙`。
- 簡報：`decks/YYYY-MM-DD-英文關鍵字/`，例如 `decks/2026-11-23-chatgpt-news-stock/`。

---

## 4. 頁面格式

### 4.1 Frontmatter

```yaml
---
title: 前瞻偏誤（Look-ahead Bias）
type: concept            # source | concept | comparison | ideas | overview | meta
summary: 40 字以內的一句話
tags: [backtesting, bias]
aliases: [前視偏誤]
sources: [2023-glasserman-look-ahead-bias]
updated: 2026-11-23
---
```

`type: source` 另外加：

```yaml
authors: Paul Glasserman, Caden Lin
year: 2023
venue: arXiv preprint
url: https://arxiv.org/abs/2309.17322
raw: raw/2023-glasserman-look-ahead-bias.md
tier: B                  # A | B | C，見 §4.6
kind: paper              # paper | report | oss | news
```

列表一律用 `[a, b]` 單行寫法。

### 4.2 連結與引用：**到來源＋章節**

- 站內連結：`[[slug]]` 或 `[[slug|顯示文字]]`。
- **引用格式**：`（[[來源slug]] §4.2）`。章節寫論文的節號、表號或頁碼，例如 `§3`、`§Table 2`、`§p.12`。多個來源用「、」分隔：`（[[a]] §2、[[b]] §5.1）`。
- 在來源頁內引用自己時，可以只寫 `（§4.2）`。
- 概念頁、比較頁、點子頁中，**每個事實性敘述都要有引用**。

### 4.3 頁面結構

**來源頁**：`## 一句話重點` → `## 背景：它想解決什麼問題` → `## 資料與方法` → `## 主要發現` → `## 限制與爭議` → `## 和本 wiki 其他頁的關係`（至少連到 2 個概念頁）

**概念頁**：開頭一段白話定義 → `## 為什麼重要` → `## 怎麼運作` → `## 發展脈絡` → `## 常見誤解` → `## 相關頁面`

**比較頁**：開頭說明比較什麼 → `## 比較表` → `## 分歧在哪裡` → `## 使用者的決定`（矛盾的處理方式，見 §5.2）→ `## 還沒解決的問題`

**點子頁（ideas）**：每個點子一個 `## 點子 N｜名稱`，固定寫這五項：
1. **訊號**
2. **依據**（含引用）
3. **文獻報告的績效**（附條件）
4. **風險與限制**
5. **台股／台指期可行性**：只寫 ❓待查或來源有寫的內容，不自己推論績效。

### 4.4 標籤清單

`sentiment`、`return-prediction`、`backtesting`、`bias`、`models`、`trading-strategy`、`market-efficiency`、`macro`、`data`、`evaluation`、`meta`

### 4.5 特殊標記

- 未處理的矛盾：`> ⚠️ **矛盾**（未處理）：A 說……，B 說……（[[A]] §x、[[B]] §y）`
- 處理後：`> ⚠️ **矛盾**（已處理，見 [[比較頁]]）：……`
- 待查：`> ❓ **待查**：……`
- 過時：`> 🕰️ **已被更新**：……`。舊敘述要保留，讓讀者看得到知識怎麼演變。
- 媒體觀點：`> 📰 **媒體觀點**：……（[[C級來源]] §x）`。C 級來源只能用這個格式出現，見 §4.6。

### 4.6 可信度三級

| 等級 | 包含 | 能做什麼 |
|---|---|---|
| **A** | 同儕審查的期刊或會議論文 | 可以單獨支撐數字與結論 |
| **B** | 預印本（arXiv、SSRN）、業界報告、開源專案文件 | 可以支撐，但結論要寫「預印本指出／尚未經同儕審查」 |
| **C** | 新聞、評論、部落格 | **不能單獨支撐數字或結論**，只能放在 `> 📰` 媒體觀點區塊，或和 A／B 來源一起引用 |

- 等級寫在來源頁的 `tier`。預印本後來正式發表時，改成 A，並在 log 記一筆 `edit`。

### 4.7 數字與績效數字

- **數字都要有出處＋章節**。這裡的數字指百分比、bps、帶小數的數字、1,000 以上的數量（年份除外）。
- **績效數字要附條件**：包括報酬、Sharpe ratio、alpha、勝率、年化報酬等。在同一行寫：

  `〔期間：2010–2023｜市場：美股｜成本：扣 10 bps〕`

  三項都必須寫。來源沒寫的那一項填「未說明」，不能省略。

### 4.8 數學式

使用 KaTeX。行內公式寫 `$...$`；獨立公式寫 `$$...$$`，`$$` 各自一行。金額不要用 `$` 符號，改寫 USD。

---

## 5. 維護 wiki 的流程

### 5.1 Ingest：加入一份來源（一次一篇，每篇 commit，不必等使用者）

1. **保存**：PDF 複製到 `raw/<slug>.pdf`，建立 `raw/<slug>.md` 來源卡（書目、tier、kind、原文連結、加入日期）。來源卡建立後就不再修改。
2. **讀全文**：以全文為準。數字要記下所在的節號或表號。
3. **寫來源頁**：照 `templates/source.md`。
4. **更新概念頁**：通常 2–6 頁。改寫「發展脈絡」、補充內文、在 `sources` 加上新 slug、更新 `updated`。缺少的概念用 `templates/concept.md` 新建。
5. **檢查矛盾**：新來源和 wiki 現有內容衝突時，**立刻停下來問使用者**（§5.2）。
6. **更新** `wiki/overview.md`，有新的可回測點子就更新 `wiki/ideas/`。
7. **寫日誌**、執行 `python3 tools/wiki.py build && python3 tools/wiki.py lint`，lint 不可有 ERROR。
8. **commit**：一篇來源一個 commit，訊息寫 `ingest: <slug>`。
9. 沒有矛盾就**直接做下一篇**，不必等使用者確認。

### 5.2 遇到矛盾：每次都停下來問

1. 先在相關頁加 `⚠️ **矛盾**（未處理）`，引用兩邊的來源與章節。
2. 用 3–5 行向使用者說明：
   - 誰說了什麼
   - 兩邊的條件有什麼不同，例如期間、市場、模型、有沒有扣成本
   - 2–3 種可能的寫法
3. **等使用者決定**。
4. 照使用者的決定建立或更新比較頁，把決定寫進 `## 使用者的決定`，並把標記改成「已處理」。
5. log 記一筆 `edit`。

### 5.3 Query：回答問題

1. 先讀 `wiki/index.md` 找相關頁，用 `[[slug]] §x` 標出依據。
2. wiki 沒寫到的部分，直接說「wiki 目前沒有這部分」，並建議可以 ingest 什麼來源。
3. 有長期價值的回答，先問使用者要不要存成新頁。

### 5.4 Lint：健康檢查

執行 `python3 tools/wiki.py lint`。

**一般檢查**：frontmatter、標籤、壞連結、孤兒頁、raw 與來源頁是否對應、`pages.json` 是否最新。

**使用者指定的 4 項檢查**：

| # | 檢查 | 嚴重度 |
|---|---|---|
| ① | 有數字的那一行，必須有帶 `§` 的引用 | ERROR |
| ② | 一行的引用全部是 C 級（而且不在 `> 📰` 區塊內） | ERROR |
| ③ | 績效數字那一行，必須有 `〔期間：…｜市場：…｜成本：…〕` | ERROR |
| ④ | 列出所有 `⚠️（未處理）` 與 `❓ 待查` | WARNING，清單交給使用者決定 |

### 5.5 日誌格式

只能往 `wiki/log.md` **最後面**加，不改舊紀錄：

```markdown
## [2026-11-23] ingest | Can ChatGPT Forecast Stock Price Movements?
- 新增：wiki/sources/2023-lopez-lira-chatgpt-forecast.md
- 修改：wiki/concepts/llm-news-sentiment.md
- 備註：……
```

類型只有這幾種：`ingest`、`query`、`lint`、`edit`、`setup`、`deck`。

---

## 6. 教學簡報：graph 流程

### 6.1 為什麼用 graph，而不是一句 prompt

一句 prompt 直接生成簡報，常見的問題有三個：
- 憑印象補數字
- 把預印本當成定論
- 文字溢出版面

所以把工作拆成節點：
- 每個節點**只看得到、只改得到**自己那一份檔案。
- 每兩個節點之間有一個**關卡**。
- 關卡沒通過時，**只退回出錯的那一個節點、那一頁**，不全部重做。

### 6.2 節點與關卡

```
brief.md（人寫／確認）
  │
  ▼
N1 檢索 wiki ─────▶ G1 覆蓋率關卡（腳本）──不足──▶ ⏹ 停：問使用者要不要 ingest
  │ 足夠
  ▼
N2 證據卡（每份來源一張）─▶ G2 卡片檢查（腳本）──不過──▶ 回 N2（該卡，≤2 輪）
  │
  ▼
N3 大綱（10 頁）─▶ G3 大綱檢查（腳本）─▶ 👤 使用者確認 ──要改──▶ 回 N3
  │
  ▼
N4 逐頁稿（一頁一檔）─▶ G4a 忠實度（腳本）＋ G4b AI 審查（新對話）
  │                       └─不過──▶ 只退回該頁到 N4（每頁 ≤2 輪）
  ▼
N5 渲染 HTML（腳本）─▶ G5 渲染檢查（Playwright 截圖）──不過──▶ 回 N4 縮短該頁
  │
  ▼
交件：report.md ＋ log
```

| 節點 | 只能讀 | 只能寫 | 檢查方式 | 不通過時 |
|---|---|---|---|---|
| N1 檢索 | `brief.md`、`wiki/` | `retrieval.json`、`retrieval.md` | — | — |
| G1 覆蓋率 | `retrieval.json` | `coverage.md` | 相關頁 ≥ 3，而且每個「核心」子問題至少 1 頁 | **停**：素材不夠就不硬寫，問使用者要不要 ingest |
| N2 證據卡 | retrieval 列出的 wiki 頁 | `cards/<source>.md` | G2（見下方） | 回 N2，只修那張卡 |
| N3 大綱 | `brief.md`、`cards/` | `outline.md` | G3：頁數正確、claim id 都存在、每個子問題都有頁；接著 **👤 使用者確認** | 回 N3 |
| N4 逐頁稿 | `outline.md`（已確認），以及**該頁**用到的 claims | `drafts/slide-NN.md` | G4a（腳本）＋G4b（AI 審查，見 §6.4） | 只退回不通過的頁 |
| N5 渲染 | `drafts/` | `index.html` | G5：頁數、KaTeX 沒有錯誤、文字沒有超出版面，並截圖到 `shots/` | 回 N4，縮短該頁 |
| 交件 | `state.json` | `report.md`、`wiki/log.md` | — | — |

**G2 卡片檢查**：
- 每條 claim 都有 `§`。
- claim 裡的每個數字，**真的出現在**被引用的 wiki 頁。
- 績效數字附有條件。
- 卡片的 tier 和來源頁一致。

**G4a 忠實度檢查（腳本）**：
- 逐頁稿裡的每個數字，都要出現在**該頁** claims 的原文裡。
- 不可以有外部網址；參考資料頁例外。
- 不可以整頁只靠 C 級來源。
- 必要欄位都要有。
- 「畫面」最多 5 點。

### 6.3 上限與停止條件

| 規則 | 數值 | 超過時 |
|---|---|---|
| 每個節點內部迴圈 | 最多 **2 輪**（同一張卡或同一頁最多重寫 2 次） | 停下來交給使用者 |
| 整個 graph 從 G4／G5 退回的總輪數 | 最多 **3 輪** | 停下來交給使用者 |
| 素材下限 | 相關 wiki 頁 < 3 | 在 G1 停止 |
| 人工確認點 | brief、outline | 沒確認就不能往下 |

`tools/deck.py` 會把每次執行的結果寫進 `state.json`，並負責計算輪數。超過上限時，腳本直接拒絕執行，並提示要找使用者。

### 6.4 AI 審查（G4b）怎麼做

1. 執行 `python3 tools/deck.py review-pack <slug>`。它會產生 `reviews/pack-roundN.md`，裡面**只有**逐頁稿、該頁引用的 claims，以及 `tools/review_prompt.md`。
2. **開一個新的對話**或新的 subagent，只把這個 pack 交給它。它看不到這次的對話，也看不到 wiki 其他內容。
3. 審查者對每一頁輸出 `slide-NN: PASS` 或 `slide-NN: FAIL｜原因`，存成 `reviews/round-N.md`。
4. 執行 `python3 tools/deck.py record-review <slug> N`，把結果寫進 state，FAIL 的頁會退回 N4。

這樣做的理由：寫稿的 AI 會「記得自己想表達什麼」，因此看不出稿子缺了什麼。換成不知道前情的審查者，才能用聽眾的角度檢查。

### 6.5 簡報預設值

| 項目 | 預設 | 說明 |
|---|---|---|
| 讀者 | 完全不熟這個主題的人 | 依 §1 的「兩者兼顧」寫法 |
| 頁數 | 10 頁 | 包含封面與參考資料 |
| 語言 | 中英混合 | 依 §1 |

每次都可以在 `brief.md` 覆寫。

**逐頁稿固定欄位**：
- `## 白話`：一句話
- `## 畫面`：最多 5 點；可以放表格或公式
- `## 講者稿`
- frontmatter 的 `claims`：這頁依據的 claim id

### 6.6 指令

```bash
python3 tools/deck.py init <slug>           # 從 templates/brief.md 建 brief
python3 tools/deck.py retrieve <slug>       # N1
python3 tools/deck.py coverage <slug>       # G1
python3 tools/deck.py check-cards <slug>    # G2
python3 tools/deck.py check-outline <slug>  # G3
python3 tools/deck.py approve <slug> outline   # 👤 使用者確認後才執行
python3 tools/deck.py check-drafts <slug>   # G4a
python3 tools/deck.py review-pack <slug>    # G4b 準備
python3 tools/deck.py record-review <slug> N
python3 tools/deck.py render <slug>         # N5
python3 tools/deck.py check-render <slug>   # G5
python3 tools/deck.py report <slug>         # 交件
python3 tools/deck.py status <slug>         # 現在卡在哪個節點
```

---

## 7. 網站規則

- 純靜態網站，沒有 npm、打包工具或後端。所有套件放在 `assets/vendor/`。
- 新增、刪除或改名任何頁面後，都要執行 `python3 tools/wiki.py build`。
- 網址格式：`index.html#/<slug>`。`#/agents` 會顯示本文件。
- 來源頁會顯示可信度標籤。目錄裡的來源標題前面會加 `[A]`、`[B]`、`[C]`。
- 本機預覽：`python3 -m http.server 8000`。

---

## 8. AI 一定要遵守的規則

1. 不修改、不刪除 `raw/` 裡已經存在的檔案。
2. **不編造**：數字、作者、年份、發表處都要來自全文。沒有全文的部分，用 ❓ 標出來。
3. 不大段複製原文。必要的引用不超過一句，並加引號。
4. **遇到矛盾一定停下來問**，不自己選邊。
5. 改完一定 build + lint；lint 有 ERROR，就不算完成。
6. 不手改 `wiki/index.md` 和 `pages.json`。
7. 一次 ingest 一篇，每篇 commit 一次。
8. 簡報只能用 wiki 的內容。網路搜尋只能用來找下一篇值得 ingest 的文獻。
9. graph 的節點只能讀寫 §6.2 表格中規定的檔案。關卡沒通過就不往下走，超過上限就停。
10. 修改 `AGENTS.md`、`templates/`、`tools/`、網站或簡報主題之前，先問使用者。
11. 策略點子只能寫文獻報告過的內容。**不可以自己估算績效**，也不可以把文獻寫成投資建議。

---

## 9. 驗收清單

**Ingest 時**：
- [ ] `raw/<slug>.md` 來源卡已建立，`tier`、`kind` 正確
- [ ] 來源頁和概念頁的數字都有 `§`，績效數字都有〔期間｜市場｜成本〕
- [ ] 新來源頁至少連到 2 個概念頁
- [ ] 有矛盾時已經停下來問使用者，並寫進比較頁
- [ ] log 已記錄，build、lint 沒有 ERROR，已 commit

**簡報時**：
- [ ] `state.json` 裡 G1–G5 都是 PASS，大綱已確認
- [ ] AI 審查是在新對話中做的，`reviews/round-N.md` 已存檔
- [ ] `shots/` 裡每一頁的截圖都看過
- [ ] `report.md` 已產生，log 已記一筆 `deck`

---

## 10. 常用指令範例

| 想做的事 | 對 AI 說 |
|---|---|
| 加入來源 | 「請先讀 AGENTS.md。ingest 這篇」＋PDF |
| 問問題 | 「根據 wiki，LLM 的新聞情緒訊號扣掉交易成本後還有用嗎？」 |
| 做簡報 | 「請先讀 AGENTS.md。用 graph 做一份簡報：<題目>」 |
| 健康檢查 | 「lint，列出未處理的矛盾和待查」 |
| 加策略點子 | 「根據 wiki 更新策略點子清單」 |

---

## 11. 需求訪談紀錄（先討論、後生成）

訪談日期是 2026-11-23。AI 一次問一題，共 11 題，整理成需求摘要給使用者確認之後，才寫出本文件。

| # | 問題 | 使用者的回答 | 寫進哪一節 |
|---|---|---|---|
| 1 | 主題 | LLM 在金融／量化交易 | §1 |
| 2 | 讀者 | 兩者兼顧：開頭白話、內文專業、術語附解釋 | §1 |
| 3 | 資料類型 | 學術論文、業界報告、開源文件、新聞評論 | §4.1 `kind` |
| 4 | 語言 | 中英混合 | §1 |
| 5 | 出處粒度 | 到來源＋章節 | §4.2 |
| 6 | 遇到矛盾 | 每次停下來問我 | §5.2 |
| 7 | 可信度 | 三級標籤，C 級不能單獨支撐 | §4.6 |
| 8 | Ingest 方式 | 一次一篇、不用等我（矛盾還是要停） | §5.1 |
| 9 | 產出 | 教學簡報、策略點子、期末專案知識庫 | §1 |
| 10 | Lint 額外檢查 | 數字要有出處、C 級不能單獨支撐、績效附條件、列出矛盾與待查 | §5.4 |
| 11 | 第一份簡報 | ChatGPT 看新聞能預測股價嗎？ | §6 |
