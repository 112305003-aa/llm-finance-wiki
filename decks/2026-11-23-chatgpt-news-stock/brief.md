---
title: ChatGPT 看新聞能預測股價嗎？
type: brief
audience: 完全不熟這個主題的人
slides: 10
language: 中英混合
created: 2026-11-23
status: confirmed
---

## 一句話目標

聽完的人能回答：「ChatGPT 讀新聞標題能不能預測股價？證據有多強？有哪些坑？」

## 子問題

每行格式：`- Qn｜core 或 extra｜子問題｜keywords: 關鍵字1, 關鍵字2`（keywords 用來檢索 wiki）

- Q1｜core｜讓電腦讀新聞判斷好壞消息是什麼？LLM 之前怎麼做？｜keywords: 情緒分析, sentiment, FinBERT
- Q2｜core｜ChatGPT 給的情緒分數能預測隔天股價嗎？｜keywords: ChatGPT, 隔日報酬, 可預測性, 標題
- Q3｜core｜扣掉交易成本還有用嗎？哪種模型比較好？｜keywords: 交易成本, Sharpe, 多空, OPT
- Q4｜core｜會不會是模型早就「看過答案」？｜keywords: 前瞻偏誤, look-ahead, 匿名化, 分心效應
- Q5｜extra｜能不能預測整個市場或總經？｜keywords: 總經, 市場報酬, DeepSeek, macro
- Q6｜extra｜LLM 自己有沒有行為偏誤？｜keywords: 外推, extrapolation, 行為偏誤
