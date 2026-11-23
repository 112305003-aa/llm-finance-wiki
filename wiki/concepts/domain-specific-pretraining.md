---
title: 領域再預訓練（Domain-specific Pre-training）
type: concept
summary: 把通用語言模型再用某個領域（如金融）的文字訓練一次
tags: [models, data]
aliases: [further pre-training, 金融領域預訓練]
sources: [2019-araci-finbert]
updated: 2026-11-23
---

通用語言模型是讀維基百科、書本長大的；「領域再預訓練」是讓它**再讀一批金融新聞**，希望它更懂金融用語，之後再拿少量標註資料微調。

## 為什麼重要

金融用語和一般文字差很多，通用模型可能看不懂，所以直覺上應該先讓模型熟悉金融文字（[[2019-araci-finbert]] §1、§3.2.1）。

## 怎麼運作

1. 通用預訓練：BERT 讀 BookCorpus 和英文維基（[[2019-araci-finbert]] §3.1.5）。
2. 領域再預訓練：再讀金融語料 TRC2-financial（[[2019-araci-finbert]] §4.2.1）。
3. 任務微調：用標註好的金融句子訓練分類器（[[2019-araci-finbert]] §3.2.2）。

## 發展脈絡

- **2019**｜FinBERT：再預訓練的幫助很小，accuracy 只從 0.85 到 0.86（[[2019-araci-finbert]] §Table 4）。

## 常見誤解

- ❌「金融專用模型一定比通用模型好」→ ✅ 在 FinBERT 的實驗裡差距很小（[[2019-araci-finbert]] §6.1）。

## 相關頁面

- [[financial-sentiment-analysis]]
