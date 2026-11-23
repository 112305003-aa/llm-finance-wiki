---
title: 多空情緒策略（Long-short Sentiment Strategy）
type: concept
summary: 買進好消息股票、放空壞消息股票，用來檢驗情緒訊號有沒有用
tags: [trading-strategy, sentiment, evaluation]
aliases: [多空, long-short, 多空組合, Sharpe ratio, 夏普值]
sources: [2023-lopez-lira-chatgpt-forecast, 2024-kirtac-sentiment-trading]
updated: 2026-11-23
---

**多空策略**：每天把有新聞的股票分兩組，好消息的買進（多方 long），壞消息的放空（空方 short），兩邊金額相同。這樣大盤漲跌大致抵銷，賺到的錢主要來自「好消息股贏過壞消息股」，所以適合用來檢驗情緒訊號本身有沒有用。

## 為什麼重要

論文常用它的績效（平均報酬、Sharpe ratio）來說明訊號強不強；讀這類數字時，一定要看條件（期間、市場、有沒有扣成本）。

## 怎麼運作

- **建組合**：例如 GPT-4 score 為正買進、為負放空，等權、每日再平衡（[[2023-lopez-lira-chatgpt-forecast]] §6.2）。
- **另一種建法**：取情緒分數最高 20% 做多、最低 20% 放空，市值加權（[[2024-kirtac-sentiment-trading]] §2.2）。
- **進出場時點**：隔夜新聞在開盤進場、收盤出場（[[2023-lopez-lira-chatgpt-forecast]] §6.2）。
- **Sharpe ratio（夏普值）**：平均超額報酬 ÷ 報酬波動，代表每承擔一單位風險換到多少報酬；年化後常拿來比較策略。

$$\text{Sharpe} = \frac{\bar r - r_f}{\sigma_r}$$

## 發展脈絡

- **2023**｜GPT-4 隔夜新聞多空策略年化 Sharpe 2.97（[[2023-lopez-lira-chatgpt-forecast]] §Table 1）〔期間：2021-10–2024-05｜市場：美股｜成本：未扣〕

- **2024**｜OPT 多空策略年化 Sharpe 3.05（[[2024-kirtac-sentiment-trading]] §Table 5）〔期間：未說明｜市場：美股｜成本：扣 10 bps〕

> ⚠️ **矛盾**（未處理）：同樣扣 10 bps，GPT-4 策略的 Sharpe 只剩 1.29（[[2023-lopez-lira-chatgpt-forecast]] §6.2），OPT 策略卻有 3.05（[[2024-kirtac-sentiment-trading]] §Table 5）〔期間：兩篇不同｜市場：美股｜成本：扣 10 bps〕

## 常見誤解

- ❌「多空兩邊一樣重要」→ ✅ GPT-4 策略的獲利主要來自空方：空方 Sharpe 2.01、多方 0.78（[[2023-lopez-lira-chatgpt-forecast]] §6.1）〔期間：2021-10–2024-05｜市場：美股｜成本：未扣〕

## 相關頁面

- [[transaction-costs]]、[[news-return-predictability]]
