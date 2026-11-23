---
title: 新聞與報酬可預測性（News-based Return Predictability）
type: concept
summary: 新聞出來之後，股價會不會繼續往同一方向走，讓人有機會預測
tags: [return-prediction, sentiment, market-efficiency]
aliases: [可預測性, 隔日報酬, 漂移, post-news drift, 新聞漂移]
sources: [2023-lopez-lira-chatgpt-forecast, 2019-araci-finbert, 2024-kirtac-sentiment-trading]
updated: 2026-11-23
---

一則新聞出來，股價會馬上反應（**初始反應**）。如果市場一次沒消化完，之後幾天股價還會繼續往同一方向走（**漂移 drift**）。「用新聞預測股價」真正能交易的，是這段漂移，而不是初始反應。

## 為什麼重要

- 初始反應發生在新聞發布當下，一般投資人來不及交易；只有之後的漂移能變成交易策略（[[2023-lopez-lira-chatgpt-forecast]] §6）。
- 有沒有漂移，反映市場是否「反應不足」（underreaction），也就是市場效率的問題（[[market-efficiency]]）。

## 怎麼運作

```
新聞發布 ──▶ 初始反應（來不及交易）──▶ 第 1–2 天漂移（可交易）──▶ 之後不顯著
```

- 量測方式：把新聞分成好／壞，看之後的報酬。常見做法是多空組合（[[long-short-sentiment-strategy]]）或迴歸。
- GPT-4 預測初始反應方向的日命中率 93.3%，預測漂移只有 58%（[[2023-lopez-lira-chatgpt-forecast]] §6.1）。
- 隔夜新聞的資訊約兩天被吸收：第 1 天 34 bps、第 2 天 19 bps（[[2023-lopez-lira-chatgpt-forecast]] §8.1）〔期間：2021-10–2024-05｜市場：美股｜成本：未扣〕

## 發展脈絡

- **2019**｜FinBERT 只做情緒分類，沒有測報酬（[[2019-araci-finbert]] §5）。
- **2023**｜GPT-4 的分數能預測 1–2 天漂移，壞消息與小型股更明顯（[[2023-lopez-lira-chatgpt-forecast]] §6.1、§8.2）。預印本。

- **2024**｜用報酬當標籤微調的 OPT，分數能顯著預測隔日報酬，係數 0.254（[[2024-kirtac-sentiment-trading]] §Table 4）〔期間：2010–2023｜市場：美股｜成本：不適用（迴歸）〕

> ⚠️ **矛盾**（已處理，見 [[zero-shot-vs-fine-tuned-sentiment]]）：BERT／FinBERT 的分數能不能預測報酬？Lopez-Lira & Tang 說不能，Sharpe 為負（[[2023-lopez-lira-chatgpt-forecast]] §7.1）；Kirtac & Germano 說能，Sharpe 超過 2（[[2024-kirtac-sentiment-trading]] §Table 5）〔期間：兩篇不同｜市場：美股｜成本：前者未扣、後者扣 10 bps〕

## 常見誤解

- ❌「能預測初始反應 = 能賺錢」→ ✅ 初始反應來不及交易，能交易的只有漂移，而且漂移弱很多（[[2023-lopez-lira-chatgpt-forecast]] §6.1）。

## 相關頁面

- [[long-short-sentiment-strategy]]、[[transaction-costs]]、[[look-ahead-bias]]、[[market-efficiency]]
