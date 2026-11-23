---
title: 市場效率與資訊擴散（Market Efficiency）
type: concept
summary: 市場多快把新資訊反映進價格；LLM 普及可能讓它變快
tags: [market-efficiency, return-prediction]
aliases: [效率市場, 反應不足, underreaction, 資訊擴散, 套利限制]
sources: [2023-lopez-lira-chatgpt-forecast, 2019-araci-finbert, 2025-chen-chatgpt-deepseek]
updated: 2026-11-23
---

**效率市場**的意思是：新的公開資訊一出來，價格就馬上反映，沒人能穩定靠公開資訊賺超額報酬（[[2019-araci-finbert]] §1）。如果市場**反應不足（underreaction）**，價格要好幾天才調整到位，就會出現可預測的漂移。

## 為什麼重要

用 LLM 讀新聞能賺錢的前提，是市場沒有馬上消化新聞；而如果大家都用 LLM，這個機會本身就可能消失。

## 怎麼運作

- 反應不足在小型股、壞消息上比較明顯，這和「套利限制」（放空難、成本高）一致（[[2023-lopez-lira-chatgpt-forecast]] §1、§8.2）。
- 越多人用同一個 LLM 訊號交易，價格越快被推到位，訊號就越沒用（[[2023-lopez-lira-chatgpt-forecast]] §3）。

## 發展脈絡

- **2023**｜GPT-4 策略的年化 Sharpe 逐年下降：2021Q4 6.54 → 2024 年 1–5 月 1.22（[[2023-lopez-lira-chatgpt-forecast]] §8.2）〔期間：2021Q4–2024-05｜市場：美股｜成本：未扣〕作者認為與 LLM 普及一致，但也可能是市場環境改變（§8.2）。

- **2025**｜在大盤層次，好消息被慢慢消化、壞消息馬上反映（[[2025-chen-chatgpt-deepseek]] §4）。

> ⚠️ **矛盾**（未處理）：個股層次是壞消息後漂移更明顯（[[2023-lopez-lira-chatgpt-forecast]] §6.1）；大盤層次卻是好消息才有預測力（[[2025-chen-chatgpt-deepseek]] §4）。

## 常見誤解

- ❌「論文證明了 LLM 讓市場變有效率」→ ✅ 作者稱為提示性證據，時間吻合不代表因果（[[2023-lopez-lira-chatgpt-forecast]] §8.2）。

## 相關頁面

- [[news-return-predictability]]
