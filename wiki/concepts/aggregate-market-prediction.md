---
title: 用新聞預測大盤與總經（Aggregate Market Prediction）
type: concept
summary: 不預測個股，而是用整體新聞的好壞比例預測整個股市與景氣
tags: [return-prediction, macro]
aliases: [大盤預測, 市場風險溢酬, 總經, macro, 好消息比例]
sources: [2025-chen-chatgpt-deepseek]
updated: 2026-11-23
---

預測個股是問「這家公司明天會不會漲」；預測**大盤**是問「整個股市接下來幾個月好不好」，也就是預測**市場風險溢酬**（持有股票比持有無風險資產多賺多少）（[[2025-chen-chatgpt-deepseek]] §1）。

## 為什麼重要

大盤的可預測性告訴我們市場風險溢酬怎麼隨時間變化，是所有投資的基準（[[2025-chen-chatgpt-deepseek]] §1）。

## 怎麼運作

1. 讓 LLM 判斷每則頭版標題對美股是好是壞（[[2025-chen-chatgpt-deepseek]] §3）。
2. 每月算好消息比例 $NR^G$ 與壞消息比例 $NR^B$（[[2025-chen-chatgpt-deepseek]] §3）。
3. 預測迴歸：

$$R_{t+h} = \alpha + \beta\, NR^K_t + \varepsilon_{t+h},\quad K = B \text{ 或 } G$$

（[[2025-chen-chatgpt-deepseek]] §4）

## 發展脈絡

- **2025**｜ChatGPT 的好消息比例能預測未來 1–6 個月的大盤，12 個月的 $R^2$ 是 8.52%（[[2025-chen-chatgpt-deepseek]] §Table 2）〔期間：1996-01–2022-12｜市場：美股 S&P 500｜成本：不適用（迴歸）〕預印本。

## 常見誤解

- ❌「每個 LLM 都可以」→ ✅ DeepSeek 的訊號只反映當月，預測不了未來（[[2025-chen-chatgpt-deepseek]] §4）。

## 相關頁面

- [[news-return-predictability]]、[[market-efficiency]]
