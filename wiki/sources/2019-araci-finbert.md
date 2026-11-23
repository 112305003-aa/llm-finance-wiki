---
title: "FinBERT: Financial Sentiment Analysis with Pre-trained Language Models"
type: source
summary: 把 BERT 再用金融新聞訓練，做成金融句子的正／負／中性分類器
tags: [sentiment, models]
authors: Dogu Tan Araci
year: 2019
venue: arXiv preprint（University of Amsterdam 碩士論文）
url: https://arxiv.org/abs/1908.10063
raw: raw/2019-araci-finbert.md
tier: B
kind: paper
updated: 2026-11-23
---

## 一句話重點

把通用的語言模型 BERT 拿來「再讀一點金融新聞、再看一點標註好的例句」，它判斷一句金融新聞是好消息、壞消息還是中性的能力，就勝過當時所有方法。注意：它判斷的是**句子情緒**，不是預測股價。

## 背景：它想解決什麼問題

- 金融情緒分析有兩個難處：標註資料要金融專業、很貴；通用模型看不懂金融用語，而且金融文字常用含糊的說法（§1）。
- 以前常用的 Loughran-McDonald 金融詞典屬於「數字詞」方法（數正面詞、負面詞），抓不到整句的語意（§1、§2.1）。

## 資料與方法

- **模型**：BERT-base（12 層 encoder）加一層分類層，用 `[CLS]` 的輸出做三分類（§3.1.5、§3.2.2）。
- **再預訓練（further pre-training）**：用 Reuters TRC2 篩出的金融語料 TRC2-financial，共 46,143 篇文件、超過 29M 字（§4.2.1）。
- **標註資料**：Financial PhraseBank，4,845 句金融新聞，由 16 位有金融背景的人依「對該公司股價的影響」標註（§4.2.2）；另用 FiQA 的 1,174 則標題與推文做情緒分數迴歸（§4.2.3）。
- **比較對象**：LSTM（GloVe）、LSTM＋ELMo、ULMFit，以及文獻中的 LPS、HSC、FinSSLX（§4.3、§5）。

## 主要發現

| 模型（Financial PhraseBank 全部資料） | Accuracy | F1 | 出處 |
|---|---|---|---|
| LSTM | 0.71 | 0.64 | §Table 2 |
| ULMFit | 0.83 | 0.79 | §Table 2 |
| **FinBERT** | **0.86** | **0.84** | §Table 2 |

- 只看標註者 100% 同意的句子時，FinBERT 的 accuracy 0.97、F1 0.95（§Table 2）。
- FiQA 情緒分數：FinBERT 的 MSE 0.07、$R^2$ 0.55，優於文獻的 0.40–0.41（§Table 3）。
- 只用 250 筆訓練資料，FinBERT 的 accuracy 就能到約 80%（§5）——預訓練讓模型不需要大量標註。
- **意外的結果**：「再用金融語料預訓練」幫助很小：Vanilla BERT accuracy 0.85、FinBERT-domain 0.86，F1 都是 0.84（§Table 4、§6.1）。

## 限制與爭議

- 作者自己說：比較用的基準模型沒有像 BERT 一樣仔細調參，不能當作「某方法一定比較好」的定論（§4.3）。
- 只評估「句子情緒分類」，沒有拿去預測股價或做交易。後來的研究把它拿去做交易時，結果見之後 ingest 的來源。
- 碩士論文、預印本（B 級）。

## 和本 wiki 其他頁的關係

- [[financial-sentiment-analysis]]：FinBERT 是 LLM 之前的代表方法。
- [[domain-specific-pretraining]]：「再用金融語料訓練」到底有沒有用，這篇給了第一個證據。
