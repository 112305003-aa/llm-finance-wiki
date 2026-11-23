---
title: 直接問 vs 用報酬微調：兩篇論文的情緒交易結果為何打架
type: comparison
summary: Lopez-Lira & Tang 與 Kirtac & Germano 對 BERT／FinBERT 能否交易得出相反結論，差在方法與樣本切分
tags: [sentiment, trading-strategy, backtesting, evaluation]
aliases: [Lopez-Lira vs Kirtac, 零樣本 vs 微調, zero-shot vs fine-tuned]
sources: [2023-lopez-lira-chatgpt-forecast, 2024-kirtac-sentiment-trading]
updated: 2026-11-23
---

兩篇論文都用美股新聞做多空策略，卻對「BERT／FinBERT 的分數能不能用來交易」得出相反結論。這頁把兩邊並排，說明差別來自**方法與檢驗方式不同**，而不是誰算錯。

## 比較表

| 面向 | Lopez-Lira & Tang | Kirtac & Germano |
|---|---|---|
| 可信度 | B 級預印本（[[2023-lopez-lira-chatgpt-forecast]] §1） | A 級期刊（[[2024-kirtac-sentiment-trading]] §1） |
| 怎麼得到情緒 | 直接問模型、不另外訓練（[[2023-lopez-lira-chatgpt-forecast]] §5） | 用 3 日超額報酬當標籤**微調** BERT、OPT（[[2024-kirtac-sentiment-trading]] §2.2） |
| 樣本 | 2021-10–2024-05，知識截止日之後（[[2023-lopez-lira-chatgpt-forecast]] §4） | 2010-01–2023-06（[[2024-kirtac-sentiment-trading]] §2.1） |
| 測試方式 | 整段都是樣本外（[[2023-lopez-lira-chatgpt-forecast]] §4） | 隨機抽 20% 當測試集，不依時間（[[2024-kirtac-sentiment-trading]] §2.2） |
| 組合 | 依正負號、等權（[[2023-lopez-lira-chatgpt-forecast]] §6.2） | 前 20%／後 20%、市值加權（[[2024-kirtac-sentiment-trading]] §2.2） |
| FinBERT 多空 Sharpe | −0.33（[[2023-lopez-lira-chatgpt-forecast]] §7.1）〔期間：2021-10–2024-05｜市場：美股｜成本：未扣〕 | 2.07（[[2024-kirtac-sentiment-trading]] §Table 5）〔期間：未說明｜市場：美股｜成本：扣 10 bps〕 |
| 最好的模型 | GPT-4，Sharpe 2.97（[[2023-lopez-lira-chatgpt-forecast]] §Table 1）〔期間：2021-10–2024-05｜市場：美股｜成本：未扣〕 | OPT，Sharpe 3.05（[[2024-kirtac-sentiment-trading]] §Table 5）〔期間：未說明｜市場：美股｜成本：扣 10 bps〕 |
| 交易成本 | 扣 10 bps 後 Sharpe 1.29（[[2023-lopez-lira-chatgpt-forecast]] §6.2）〔期間：2021-10–2024-05｜市場：美股｜成本：扣 10 bps〕 | 已扣 10 bps（[[2024-kirtac-sentiment-trading]] §2.2） |

## 分歧在哪裡

1. **FinBERT 用法不同**：Lopez-Lira 直接拿現成 FinBERT 判斷，它把 75% 的新聞判成中性（[[2023-lopez-lira-chatgpt-forecast]] §7.1）；Kirtac 的 BERT、OPT 是拿「之後股價漲或跌」當答案訓練過的（[[2024-kirtac-sentiment-trading]] §2.2）。前者測的是「讀懂新聞」，後者測的是「學會什麼新聞後面會漲」。
2. **檢驗方式不同**：隨機切分代表訓練集可能含有比測試新聞更晚的資料（[[2024-kirtac-sentiment-trading]] §2.2）；Lopez-Lira 刻意只用模型沒看過的期間（[[2023-lopez-lira-chatgpt-forecast]] §4）。
3. **期間不同**：Lopez-Lira 發現策略逐年變弱（[[2023-lopez-lira-chatgpt-forecast]] §8.2），兩篇的期間又不重疊，數字本來就難以直接比較。

## 使用者的決定

> 2026-11-23，使用者選擇「**並陳＋點出條件差異**」：wiki 與簡報兩邊數字都列，不判輸贏；簡報把這個矛盾當成「為什麼論文數字會打架」的教學例子，提醒讀者看數字前先看條件（AGENTS.md §5.2）。

## 還沒解決的問題

- ❓ Kirtac 的 Sharpe 3.05 是哪一段期間算的？論文沒寫清楚（[[2024-kirtac-sentiment-trading]] §Table 5）〔期間：未說明｜市場：美股｜成本：扣 10 bps〕
- ❓ 如果 Kirtac 改用依時間切分，結果還會一樣好嗎？
