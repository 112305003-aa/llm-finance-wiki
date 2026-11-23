---
title: 分心效應（Distraction Effect）
type: concept
summary: LLM 對公司的既有印象，干擾它判斷這則新聞本身是好是壞
tags: [bias, sentiment, models]
aliases: [分心效應, distraction, 匿名化, anonymization, 過度自信]
sources: [2023-glasserman-look-ahead-bias]
updated: 2026-11-23
---

LLM 讀過很多關於大公司的文章。問它「這則標題對 Google 是好是壞」時，它可能不是在讀這則標題，而是想起「Google 那年表現很好」。這種**既有印象干擾判斷**的現象叫分心效應，和「偷看答案」的[[look-ahead-bias|前瞻偏誤]]不同（[[2023-glasserman-look-ahead-bias]] §1.1）。

## 為什麼重要

- 前瞻偏誤只發生在訓練期間內，分心效應**在樣本外也會發生**，所以實際使用時也要提防（[[2023-glasserman-look-ahead-bias]] §1.1、§4）。
- 它的方向不一定，可能幫倒忙（[[2023-glasserman-look-ahead-bias]] §1.1）。

## 怎麼運作

- **怎麼量測**：把公司名稱和產品名稱換成 “Blahblahblah”，比較原始標題與匿名標題的策略績效（[[2023-glasserman-look-ahead-bias]] §2.4）。
- **結果**：樣本內，匿名標題的多空策略平均日報酬較高，爬取組是 30.97 對 25.08 bps（[[2023-glasserman-look-ahead-bias]] §Table 3）〔期間：2015-01–2021-09｜市場：美股｜成本：未扣〕
- **原因**：模型對原始標題給出明確判斷、對匿名標題卻判中性時，損失最大，是一種過度自信（[[2023-glasserman-look-ahead-bias]] §3.3.2）。
- **大公司更嚴重**：GPT-3.5 推薦交易的公司，市值明顯偏大（[[2023-glasserman-look-ahead-bias]] §3.4）。

## 發展脈絡

- **2023**｜提出分心效應與匿名化檢驗（[[2023-glasserman-look-ahead-bias]] §1.1）。預印本。

## 常見誤解

- ❌「模型知道越多越好」→ ✅ 對 GPT-3.5 來說，對公司的既有知識在判斷新聞情緒時弊大於利（[[2023-glasserman-look-ahead-bias]] §4）。

## 相關頁面

- [[look-ahead-bias]]、[[news-return-predictability]]
