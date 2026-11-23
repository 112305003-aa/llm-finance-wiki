---
title: Sentiment trading with large language models
type: source
summary: 用報酬當標籤微調 OPT、BERT，比較 FinBERT 與詞典法，OPT 多空策略扣 10 bps 後 Sharpe 3.05
tags: [sentiment, trading-strategy, models]
authors: Kemal Kirtac, Guido Germano
year: 2024
venue: Finance Research Letters 62, 105227
url: https://doi.org/10.1016/j.frl.2024.105227
raw: raw/2024-kirtac-sentiment-trading.md
tier: A
kind: paper
updated: 2026-11-23
---

## 一句話重點

把新聞丟給幾種語言模型打情緒分數，再用分數最高、最低的 20% 股票做多空（§2.2）：**模型越大越好**，OPT（類 GPT-3）最好，傳統金融詞典幾乎沒用。

## 背景：它想解決什麼問題

- 詞典法只算字詞頻率，忽略字序與上下文（§1）。
- 作者想知道 LLM 的文字表示能不能更好地預測個股報酬（§1）。
- 作者原本想用 GPT-4，但當時沒有公開權重，所以改用開源、類似 GPT 的 OPT（§1）。

## 資料與方法

- **資料**：Refinitiv 美股新聞，2010-01-01 到 2023-06-30。原始配對 2,732,845 則新聞，篩選後剩 965,375 篇（§2.1、§Table 1）。
- **去重**：和前面文章的 cosine similarity ≥ 0.8 就刪掉（§2.1）。
- **模型**：OPT（2.7B 參數）、BERT（345M），用報酬當標籤**微調**；FinBERT 與 Loughran-McDonald 詞典不微調（§1、§2.2）。
- **標籤**：發布日起 3 天的超額報酬為正就標 1，否則標 0（§2.2）。
- **切分**：**隨機**抽 20% 當測試集，剩下的再抽 20% 當驗證集，訓練集 193,070 篇（§2.2）。
- **策略**：每天依情緒分數取最高 20% 做多、最低 20% 放空，市值加權、每日再平衡，每筆交易扣 10 bps（§2.2）。

## 主要發現

| 模型 | 3 日超額報酬方向的分類 accuracy | 出處 |
|---|---|---|
| OPT | 0.744 | §Table 3 |
| BERT | 0.725 | §Table 3 |
| FinBERT | 0.722 | §Table 3 |
| Loughran-McDonald 詞典 | 0.501 | §Table 3 |

- 迴歸預測隔日報酬：OPT 分數係數 0.254（t=4.871），詞典分數 0.083（t=1.871）不顯著（§Table 4）〔期間：2010–2023｜市場：美股｜成本：不適用（迴歸）〕
- 多空策略年化 Sharpe：OPT 3.05、BERT 2.11、FinBERT 2.07、詞典 1.23（§Table 5）〔期間：未說明（表 5 只寫「樣本期間」）｜市場：美股｜成本：扣 10 bps〕
- OPT 多空策略：多方 Sharpe 1.81、空方 1.42（§Table 5）〔期間：未說明｜市場：美股｜成本：扣 10 bps〕
- 2021-08 到 2023-07 累積報酬：OPT 多空 355%、BERT 235%、FinBERT 165%、詞典 0.91%（§3.3、§Figure 1）〔期間：2021-08–2023-07｜市場：美股｜成本：扣 10 bps〕
- FinBERT 雖然是金融專用模型，卻沒贏過通用的 BERT；作者推測是 BERT 的預訓練資料更多元，以及專用模型可能過度擬合（§3.2）。

## 限制與爭議

- 測試集是從 2010–2023 **隨機抽樣**，不是依時間切分（§2.2）。❓ **待查**：論文沒有說明訓練集是否包含測試期間之後的新聞。
- 標籤用的 3 日報酬從發布日起算（§2.2），與策略的持有期間有重疊。
- Sharpe 3.05 的計算期間在表 5 沒有寫清楚（§Table 5、§4）〔期間：未說明｜市場：美股｜成本：扣 10 bps〕
- 與 Lopez-Lira & Tang 的結果互相衝突，見下方 ⚠️。

> ⚠️ **矛盾**（未處理）：Lopez-Lira & Tang 發現 FinBERT 與 BERT 的分數預測不了新聞後的漂移，Sharpe 為負（[[2023-lopez-lira-chatgpt-forecast]] §7.1）；本篇卻發現 FinBERT、BERT 多空策略扣 10 bps 後 Sharpe 都超過 2（[[2024-kirtac-sentiment-trading]] §Table 5）〔期間：兩篇不同｜市場：美股｜成本：前者未扣、後者扣 10 bps〕

## 和本 wiki 其他頁的關係

- [[financial-sentiment-analysis]]：詞典法 vs LLM 的直接比較。
- [[long-short-sentiment-strategy]]：前 20%／後 20%、市值加權的做法（§2.2）。
- [[transaction-costs]]：扣 10 bps 的結果（§Table 5）。
- [[domain-specific-pretraining]]：FinBERT 沒贏過 BERT。
- [[model-scale]]：參數越多，預測越準。
