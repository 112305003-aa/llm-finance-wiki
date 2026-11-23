---
title: 金融情緒分析（Financial Sentiment Analysis）
type: concept
summary: 讓電腦判斷一段金融文字是好消息、壞消息還是中性
tags: [sentiment, models]
aliases: [情緒分析, sentiment analysis, 新聞情緒]
sources: [2019-araci-finbert, 2023-lopez-lira-chatgpt-forecast, 2024-kirtac-sentiment-trading]
updated: 2026-11-23
---

金融情緒分析就是讓電腦讀一句新聞、公告或推文，判斷它對某家公司是**好消息、壞消息還是中性**。和一般的情緒分析不同，它的目的通常是猜「市場會怎麼反應」（[[2019-araci-finbert]] §2.1）。

## 為什麼重要

每天的金融文字太多，人讀不完，所以需要自動化；而新的資訊處理技術，可能在短期內給早期使用者優勢（[[2019-araci-finbert]] §1）。

## 怎麼運作

三代方法：

| 世代 | 做法 | 弱點 |
|---|---|---|
| 1. 詞典法 | 用 Loughran-McDonald 等金融詞典數正負面詞（[[2019-araci-finbert]] §2.1） | 只數字詞，看不懂句子語意（[[2019-araci-finbert]] §1） |
| 2. 預訓練語言模型 | BERT／FinBERT：先讀大量文字，再用少量標註句子微調（[[2019-araci-finbert]] §3） | 需要標註資料；只輸出情緒 |
| 3. 大型語言模型（LLM） | 不另外訓練，直接問 GPT-4「這則標題對股價是好是壞」（[[2023-lopez-lira-chatgpt-forecast]] §5） | 要確認模型沒有「看過答案」，見 [[look-ahead-bias]] |

## 發展脈絡

- **2019**｜FinBERT：在 Financial PhraseBank 達到 accuracy 0.86，是 LLM 之前的代表（[[2019-araci-finbert]] §Table 2）。

- **2023**｜GPT-4 直接讀標題，比 FinBERT 等小模型更能對應到股價漂移（[[2023-lopez-lira-chatgpt-forecast]] §7.1）。預印本。

- **2024**｜在 965,375 篇新聞上，詞典法預測 3 日報酬方向的 accuracy 只有 0.501（幾乎等於丟銅板），OPT 是 0.744（[[2024-kirtac-sentiment-trading]] §Table 3）〔期間：2010–2023｜市場：美股｜成本：不適用（分類準確率）〕

## 常見誤解

- ❌「情緒分類準確 = 能預測股價」→ ✅ FinBERT 只評估句子情緒有沒有標對，沒有測試能不能賺錢（[[2019-araci-finbert]] §5）。

## 相關頁面

- [[domain-specific-pretraining]]、[[news-return-predictability]]、[[model-scale]]
