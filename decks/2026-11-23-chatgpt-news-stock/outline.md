---
title: ChatGPT 看新聞能預測股價嗎？｜大綱
type: outline
brief: decks/2026-11-23-chatgpt-news-stock/brief.md
status: confirmed
---

# 大綱（N3）

教學主線：**問題 → 怎麼做 → 看到什麼 → 能不能賺 → 證據可不可信 → 延伸 → 結論**。全程給不熟這個主題的人看，所以每頁開頭都有一句白話。

## Slide 1｜ChatGPT 看新聞能預測股價嗎？
- layout: cover
- q: Q2
- claims: []
- 重點：題目與副標「讀了 6 篇論文之後的答案：可以，但沒有你想的那麼好賺」

## Slide 2｜讓電腦讀新聞：從數字詞到 FinBERT
- layout: bullets
- q: Q1
- claims: [fb-1, fb-2, fb-3, fb-4]
- 重點：電腦判斷新聞好壞不是新鮮事；但「判斷準」不等於「能預測股價」

## Slide 3｜實驗怎麼做：只問 GPT-4 一個問題
- layout: bullets
- q: Q2
- claims: [lt-1, lt-2, lt-3]
- 重點：prompt、分數、為什麼樣本從 2021-10 開始

## Slide 4｜結果一：當下反應抓很準，之後的漂移弱很多
- layout: bullets
- q: Q2
- claims: [lt-4, lt-5, lt-11]
- 重點：分清楚「初始反應（來不及交易）」和「漂移（可交易）」

## Slide 5｜結果二：真的能賺嗎？看成本
- layout: table
- q: Q3
- claims: [lt-6, lt-7, lt-8, lt-12]
- 重點：Sharpe 2.97 是不扣成本；20 bps 就不賺；只有低成本參與者能用

## Slide 6｜兩篇論文打架：BERT、FinBERT 到底行不行？
- layout: table
- q: Q3
- claims: [lt-9, kg-3, kg-4, kg-5]
- 重點：同一個問題得到相反答案，差在方法與測試方式（教學例子：看數字先看條件）

## Slide 7｜會不會是 ChatGPT 早就「看過答案」？
- layout: bullets
- q: Q4
- claims: [lt-3, gl-1, gl-2, gl-3, gl-4, gl-5]
- 重點：前瞻偏誤 vs 分心效應；遮掉公司名稱的實驗

## Slide 8｜延伸：能不能預測整個大盤？
- layout: bullets
- q: Q5
- claims: [cd-1, cd-2, cd-3, cd-4, cd-6]
- 重點：大盤層次是好消息有預測力；這是樣本內結果，要加警語
- 修改紀錄：原本同時放「預測大盤」與「LLM 追高偏誤」（Q6），AI 審查第 1 輪指出一頁講兩件事，且樣本內警語的依據 cd-6 沒分配到本頁 → 回 N3：刪掉 Q6（延伸題），加入 cd-6

## Slide 9｜結論：可以，但……
- layout: bullets
- q: Q2, Q3, Q4
- claims: [lt-5, lt-8, lt-10, kg-5, gl-5, cd-6]
- 重點：四個 takeaway，以及「機會正在變小」

## Slide 10｜參考資料
- layout: refs
- q: Q1
- claims: []
- 重點：6 篇來源（附可信度）與 wiki 頁
