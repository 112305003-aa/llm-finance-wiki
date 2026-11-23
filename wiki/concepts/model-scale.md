---
title: 模型規模與預測力（Model Scale）
type: concept
summary: 語言模型越大，讀新聞預測股價的能力是否越強
tags: [models, return-prediction]
aliases: [模型大小, 參數量, emergent, 湧現能力]
sources: [2023-lopez-lira-chatgpt-forecast, 2024-kirtac-sentiment-trading]
updated: 2026-11-23
---

語言模型的大小通常用**參數量**衡量（例如 BERT 約數億、GPT-4 據估計上兆）。兩篇主要來源都發現：模型越大，從新聞讀出「對股價的意義」的能力越強。

## 為什麼重要

如果只有夠大的模型才做得到，代表這是一種需要「推理」的能力，而不只是數正負面字詞（[[2023-lopez-lira-chatgpt-forecast]] §7.1）。

## 怎麼運作

- 零樣本（直接問）的比較：GPT-4 漂移策略 Sharpe 2.97，高於 GPT-3.5 的 1.66、DistilBART-MNLI 的 1.26；GPT-1、GPT-2、BERT 為負（[[2023-lopez-lira-chatgpt-forecast]] §7.1）〔期間：2021-10–2024-05｜市場：美股｜成本：未扣〕
- 微調後的比較：OPT accuracy 0.744 高於 BERT 0.725、FinBERT 0.722（[[2024-kirtac-sentiment-trading]] §Table 3）〔期間：2010–2023｜市場：美股｜成本：不適用（分類準確率）〕

## 發展脈絡

- **2023**｜「門檻效應」：模型要夠大才有用（[[2023-lopez-lira-chatgpt-forecast]] §7.1）。預印本。
- **2024**｜參數較多的 OPT 勝過 BERT 與 FinBERT（[[2024-kirtac-sentiment-trading]] §3.2）。

## 常見誤解

- ❌「金融專用的小模型一定比較好」→ ✅ FinBERT 沒贏過通用的 BERT（[[2024-kirtac-sentiment-trading]] §Table 3）。

## 相關頁面

- [[financial-sentiment-analysis]]、[[domain-specific-pretraining]]
