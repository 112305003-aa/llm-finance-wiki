---
title: 交易成本（Transaction Costs）
type: concept
summary: 手續費、稅、價差與衝擊成本；每天換股的策略特別怕它
tags: [backtesting, trading-strategy]
aliases: [交易成本, bps, 基點, 成本敏感度, 衝擊成本]
sources: [2023-lopez-lira-chatgpt-forecast]
updated: 2026-11-23
---

每買賣一次都要付成本：手續費、稅、買賣價差，以及大單把價格推走的**衝擊成本（price impact）**。論文常用 **bps（基點，萬分之一）** 表示「每次來回」的成本。每天換股的新聞策略交易很頻繁，所以成本假設會大幅改變結論。

## 為什麼重要

不扣成本的績效只能說明「訊號有資訊」，不能說明「實際能賺錢」。

## 怎麼運作

- 敏感度分析：用 5、10、20 bps 等不同成本重算績效。GPT-4 策略在 5 bps 時累積報酬仍超過 300%、10 bps 時仍高於 100%、20 bps 時不賺錢（[[2023-lopez-lira-chatgpt-forecast]] §6.2）〔期間：2021-10–2024-05｜市場：美股｜成本：5／10／20 bps 來回〕
- 降低換手：每日只調整 25% 部位，10 bps 成本下 Sharpe 1.34，高於全部調整的 1.29（[[2023-lopez-lira-chatgpt-forecast]] §6.2）〔期間：2021-10–2024-05｜市場：美股｜成本：扣 10 bps〕
- 用開盤與收盤集合競價成交，沒有買賣價差，所以用固定 bps 代表手續費與衝擊成本（[[2023-lopez-lira-chatgpt-forecast]] §6.2）。

## 發展脈絡

- **2023**｜作者結論：只有交易成本夠低的參與者（例如造市商）能利用（[[2023-lopez-lira-chatgpt-forecast]] §1）。

## 常見誤解

- ❌「Sharpe 很高就能直接用」→ ✅ 先確認是否扣成本、成本假設多少（[[2023-lopez-lira-chatgpt-forecast]] §6.2）。

## 相關頁面

- [[long-short-sentiment-strategy]]
