---
title: "ChatGPT and DeepSeek: Can They Predict the Stock Market and Macroeconomy?"
type: source
summary: 用 ChatGPT 判斷華爾街日報頭版標題的好壞，每月「好消息比例」能預測大盤與總經
tags: [return-prediction, macro, sentiment, models]
authors: Jian Chen, Guohao Tang, Guofu Zhou, Wu Zhu
year: 2025
venue: arXiv preprint（初稿 2023-07）
url: https://arxiv.org/abs/2502.10008
raw: raw/2025-chen-chatgpt-deepseek.md
tier: B
kind: paper
updated: 2026-11-23
---

## 一句話重點

不看個股，改看**整個股市**：每個月數一數華爾街日報頭版有多少則被 ChatGPT 判成「好消息」。好消息比例越高，接下來 1–6 個月大盤越好；壞消息只跟當月有關，預測不了未來。DeepSeek、BERT、詞典法都做不到。

## 背景：它想解決什麼問題

- 先前研究多半預測個股，很少有人用 LLM 預測**整體市場**，也就是市場風險溢酬（§1）。
- 作者想知道：華爾街日報有沒有足夠的資訊？如果有，市場是否已經完全反映（§1）？

## 資料與方法

- **資料**：華爾街日報頭版的標題與快訊，1996-01 到 2022-12，共 84,535 則，平均每月 260.91 則（§3、§Table 1）。
- **Prompt**：請 ChatGPT-3.5 判斷這則標題代表美股 GOING UP、GOING DOWN 還是 UNKNOWN（§3）。
- **訊號**：每月好消息比例 ^G$、壞消息比例 ^B$（§3）。
- **預測迴歸**：用 ^G$、^B$ 預測 S&P 500 未來 1–12 個月的平均超額報酬（§4）。
- **比較**：DeepSeek-R1、ChatGPT-4、微調後的 ChatGPT-3.5、BERT、RoBERTa、Loughran-McDonald 詞典（§3、§4）。

## 主要發現

> 本篇主要結果是**樣本內**（1996–2022，多數在 GPT-3.5 訓練期間內），可能有前瞻偏誤或分心效應，見 [[in-sample-vs-out-of-sample-llm-backtest]]。

- 好消息比例預測下個月市場超額報酬：斜率 0.53%，^2$ 1.37%；拉長到 12 個月，^2$ 升到 8.52%（§1、§Table 2）〔期間：1996-01–2022-12｜市場：美股 S&P 500｜成本：不適用（迴歸）〕
- 壞消息比例只和當月報酬有關，斜率 −1.03%，沒有預測力（§4、§Table 2）〔期間：1996-01–2022-12｜市場：美股 S&P 500｜成本：不適用（迴歸）〕
- 樣本外：^2_{OS}$ 1.17%（§1）〔期間：2006-01–2022-12｜市場：美股｜成本：不適用（預測評估）〕
- 經濟價值：均值–變異數投資人（風險趨避係數 3）每月在大盤與無風險資產間配置，年化確定等值報酬（CER）增加 4.92%；扣 50 bps 交易成本後仍有 3.55%（§1）〔期間：2006-01–2022-12｜市場：美股｜成本：扣 50 bps〕
- 用好消息預測做配置，年化 Sharpe 0.51，大盤只有 0.30（§1）〔期間：2006-01–2022-12｜市場：美股｜成本：未說明〕
- **DeepSeek 不行**：它的好壞消息只和當月報酬有關，預測不了未來。作者推測原因是它主要用中英文訓練（§4、§6）。
- DeepSeek 的好消息和投資人情緒指數相關，ChatGPT 的訊號則和總經基本面相關（§5、§Table 9）。
- 詞典法與 BERT 預測不了大盤（§1、§Table 3）。
- 好消息比例也能預測未來的總經，例如工業生產、實質 GDP 成長、VIX、衰退機率（§5、§Table 8）。

## 限制與爭議

- **前瞻偏誤**：樣本內期間 1996–2022 大部分在 GPT-3.5 的訓練期間內。作者提出三點理由，認為問題不大（§1）：
  1. 語言的意義很穩定。
  2. GPT-3.5 相對 BERT 的優勢，在 2018–2021 年間沒有突然變大。
  3. 2021-09 之後表現沒有變差。
- ❓ **待查**：作者 §4 內文說壞消息比例和當期報酬「正相關」，但同一段報告的斜率是 −1.03%（§4、§Table 2）〔期間：1996-01–2022-12｜市場：美股 S&P 500｜成本：不適用（迴歸）〕
- 作者正在把方法用在中文新聞與中國股市（§6 註 11），目前還沒有結果。

> ⚠️ **矛盾**（已處理，見 [[stock-vs-market-news-asymmetry]]）：本篇發現**好消息**才有預測力、壞消息很快被消化（§4）；Lopez-Lira & Tang 卻發現**壞消息**之後漂移更明顯、空方賺得多（[[2023-lopez-lira-chatgpt-forecast]] §6.1）。

> ⚠️ **矛盾**（已處理，見 [[in-sample-vs-out-of-sample-llm-backtest]]）：本篇認為用訓練期間內的樣本問題不大（§1）；Lopez-Lira & Tang 則認為必須用知識截止日之後的樣本，才能避免前瞻偏誤（[[2023-lopez-lira-chatgpt-forecast]] §4）。

## 和本 wiki 其他頁的關係

- [[aggregate-market-prediction]]：本篇的主題。
- [[look-ahead-bias]]：對樣本內使用 LLM 提出不同看法。
- [[model-scale]]：大模型勝過 BERT 與詞典法；DeepSeek 不如 ChatGPT。
- [[market-efficiency]]：好消息反應不足、壞消息馬上反映。
- [[stock-vs-market-news-asymmetry]]、[[in-sample-vs-out-of-sample-llm-backtest]]：與其他來源的矛盾與處理。
