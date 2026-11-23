---
title: 工作日誌
type: meta
summary: 依時間記錄每次 ingest、lint、簡報產出（只能往後加）
tags: [meta]
updated: 2026-11-23
---

## [2026-11-23] setup | 以「先討論、後生成」建立 wiki
- 訪談 11 題 → 需求摘要經使用者確認 → 產生 AGENTS.md（§11 有訪談紀錄）、CLAUDE.md（@AGENTS.md）
- 建立資料夾、templates/、tools/wiki.py（含使用者指定的 4 項 lint）、tools/deck.py（簡報 graph）
- 沿用上一個專案 llm-research-wiki 的網站與簡報主題，新增可信度標籤顯示

## [2026-11-23] ingest | FinBERT: Financial Sentiment Analysis with Pre-trained Language Models
- 新增：raw/2019-araci-finbert.md、wiki/sources/2019-araci-finbert.md、wiki/concepts/financial-sentiment-analysis.md、wiki/concepts/domain-specific-pretraining.md
- 修改：wiki/overview.md
- 備註：碩士論文，B 級；讀全文 11 頁
- lint 第一次跑出 6 個 ERROR（表格數字沒附 §、發展脈絡沒用標準引用格式、連到還沒建的頁），修正後 0 ERROR

## [2026-11-23] ingest | Can ChatGPT Forecast Stock Price Movements?（v6）
- 新增：raw/2023-lopez-lira-chatgpt-forecast.md、wiki/sources/2023-lopez-lira-chatgpt-forecast.md、concepts/news-return-predictability、long-short-sentiment-strategy、transaction-costs、look-ahead-bias、market-efficiency
- 修改：concepts/financial-sentiment-analysis（加第 3 代 LLM）、overview
- 備註：讀 v6（142 頁）正文 §1–§9；與 FinBERT 沒有矛盾（FinBERT 只做分類，本篇測報酬）
- lint 擋下 2 個 ERROR（定義句裡的 0.01% 被當成數據、關聯段落的 20 bps 沒附 §），已修正
