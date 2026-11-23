---
title: 總覽：LLM 在金融與量化交易
type: overview
summary: 這個 wiki 在回答什麼問題、目前的主論點是什麼
tags: [meta]
updated: 2026-11-23
---

這個 wiki 整理「大型語言模型（LLM）能不能、以及怎麼用在金融市場」的文獻，重點放在**用 LLM 讀新聞、判斷情緒，再拿來預測股價**。每份來源都標了可信度：A 是同儕審查，B 是預印本／業界／開源，C 是新聞評論。每個數字都附上來源和章節。

## 目前的主論點

1. **讓電腦判斷金融新聞的好壞，在 LLM 之前就做得不錯**：FinBERT 用少量標註句子就能分類金融句子情緒（[[2019-araci-finbert]] §5）。但「分類準」不等於「能預測股價」（[[financial-sentiment-analysis]]）。

2. **GPT-4 讀標題，能預測新聞後 1–2 天的漂移**，壞消息、小型股更明顯；但扣掉 20 bps 來回成本就不賺錢，而且隨 LLM 普及逐年變弱（[[2023-lopez-lira-chatgpt-forecast]] §6.2、§8.2）。這是預印本（B 級）的結果。
3. **期刊論文（A 級）報告更樂觀的數字**：用報酬當標籤微調的 OPT，扣 10 bps 後多空 Sharpe 3.05（[[2024-kirtac-sentiment-trading]] §Table 5）〔期間：未說明｜市場：美股｜成本：扣 10 bps〕。但它和 2. 的方法、切分方式不同，兩者並陳，見 [[zero-shot-vs-fine-tuned-sentiment]]。
4. **「模型偷看答案」不是唯一的坑**：遮掉公司名稱後，GPT-3.5 的樣本內績效反而更好，代表它對公司的既有印象（分心效應）會干擾判斷，而且在樣本外也存在（[[2023-glasserman-look-ahead-bias]] §4）。
5. **大盤也可以預測，但方向和個股相反**：華爾街日報頭版的「好消息比例」能預測未來 1–6 個月的大盤，壞消息則當月就被消化（[[2025-chen-chatgpt-deepseek]] §4）；個股則是壞消息反應不足，見 [[stock-vs-market-news-asymmetry]]。這是樣本內的結果。

**本 wiki 的證據標準**：LLM 回測以知識截止日後的樣本外結果為主，見 [[in-sample-vs-out-of-sample-llm-backtest]]。

## 從哪裡開始讀

- 依時間讀來源：見 [[index]]
- 規則：見 AGENTS.md（網站上方「規則手冊」）
