---
title: 樣本內 vs 樣本外：在 LLM 訓練期間內回測可不可以？
type: comparison
summary: 本 wiki 以知識截止日之後的樣本外結果為標準，樣本內結果保留但加警語
tags: [backtesting, bias, evaluation]
aliases: [樣本內, 樣本外, in-sample, out-of-sample, 知識截止日]
sources: [2023-lopez-lira-chatgpt-forecast, 2025-chen-chatgpt-deepseek, 2023-glasserman-look-ahead-bias]
updated: 2026-11-23
---

LLM 是用某個日期以前的資料訓練的（知識截止日）。拿截止日**以前**的新聞回測叫樣本內，**以後**的叫樣本外。三篇來源對樣本內回測的態度不同。

## 比較表

| 來源 | 樣本 | 立場 |
|---|---|---|
| Lopez-Lira & Tang | 只用截止日後：2021-10–2024-05（[[2023-lopez-lira-chatgpt-forecast]] §4） | 必須用樣本外，才能避免前瞻偏誤（[[2023-lopez-lira-chatgpt-forecast]] §4） |
| Chen 等人 | 1996–2022，大多在訓練期間內（[[2025-chen-chatgpt-deepseek]] §3） | 問題不大：語言意義穩定、截止日後表現沒變差（[[2025-chen-chatgpt-deepseek]] §1） |
| Glasserman & Lin | 樣本內 2015–2021、樣本外 2021–2022（[[2023-glasserman-look-ahead-bias]] §2.1） | 實際量測：樣本內有偏誤，但主要是分心效應，不是偷看答案（[[2023-glasserman-look-ahead-bias]] §4） |

## 分歧在哪裡

- Chen 等人的理由是間接證據，例如截止日前後的表現比較（[[2025-chen-chatgpt-deepseek]] §1）。
- Glasserman & Lin 直接量測偏誤，結果顯示偏誤存在，只是方向和直覺相反（[[2023-glasserman-look-ahead-bias]] §3.2）。

## 使用者的決定

> 2026-11-23，使用者選擇「**以樣本外為標準，樣本內加警語**」：wiki 與簡報引用 LLM 回測結果時，以知識截止日之後的樣本外結果為主要證據；樣本內結果保留，但要註明「樣本內，可能有前瞻偏誤或分心效應」，並附上 Glasserman & Lin 的實測（AGENTS.md §5.2）。

## 還沒解決的問題

- ❓ 對 GPT-4 等更大的模型，樣本內偏誤是否和 GPT-3.5 一樣，以分心效應為主？
