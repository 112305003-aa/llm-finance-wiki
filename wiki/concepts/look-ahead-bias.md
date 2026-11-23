---
title: 前瞻偏誤（Look-ahead Bias）
type: concept
summary: 回測時不小心用到「當時還不知道的資訊」，讓績效看起來比實際好
tags: [bias, backtesting, evaluation]
aliases: [前瞻偏誤, look-ahead, 前視偏誤, 記憶, memorization, 知識截止日]
sources: [2023-lopez-lira-chatgpt-forecast]
updated: 2026-11-23
---

**前瞻偏誤**是回測時用到了「當時還不知道的資訊」。對 LLM 來說特別麻煩：模型是用網路文章訓練的，如果訓練資料裡已經有「某則新聞之後股價怎麼走」，它在回測時就可能是在**背答案**，而不是在推理。

## 為什麼重要

如果 LLM 的好成績是背答案，那它在未來（沒看過的新聞）上就做不到。

## 怎麼運作

- **常見對策：只用知識截止日之後的樣本**。`gpt-4-0314` 的訓練資料到 2021-09，所以樣本從 2021-10 開始（[[2023-lopez-lira-chatgpt-forecast]] §4）。
- **時間上的檢查**：GPT-4 在樣本後段表現較好，與「模型有截止日後的知識」不一致（[[2023-lopez-lira-chatgpt-forecast]] §4 註 11）。

## 發展脈絡

- **2023**｜用截止日後的樣本處理（[[2023-lopez-lira-chatgpt-forecast]] §4）。

## 常見誤解

- ❌「用了截止日後的樣本就完全沒問題」→ ❓ 待查：其他來源對此有不同做法。

## 相關頁面

- [[news-return-predictability]]
