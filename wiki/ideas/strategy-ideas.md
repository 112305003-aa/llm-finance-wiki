---
title: 策略點子清單
type: ideas
summary: 從已 ingest 的文獻整理出可回測的新聞情緒點子（不是投資建議）
tags: [trading-strategy, sentiment]
sources: [2023-lopez-lira-chatgpt-forecast, 2023-glasserman-look-ahead-bias, 2025-chen-chatgpt-deepseek, 2024-kirtac-sentiment-trading]
updated: 2026-11-23
---

> 每個點子只寫文獻報告過的內容；績效一律附條件，不自己估算（AGENTS.md §8-11）。這是給研究與回測用的清單，不是投資建議。

## 點子 1｜隔夜新聞 LLM 情緒多空

- **訊號**：收盤後到開盤前的公司新聞標題，問 LLM 好／壞／不確定，轉成 1／0／−1；開盤做多正分、放空負分，收盤出場（[[2023-lopez-lira-chatgpt-forecast]] §5、§6.2）。
- **依據**：GPT-4 分數能預測新聞後 1–2 天的漂移（[[2023-lopez-lira-chatgpt-forecast]] §8.1）。
- **文獻報告的績效**：年化 Sharpe 2.97（[[2023-lopez-lira-chatgpt-forecast]] §Table 1）〔期間：2021-10–2024-05｜市場：美股｜成本：未扣〕；每次來回 20 bps 時不賺錢（[[2023-lopez-lira-chatgpt-forecast]] §6.2）〔期間：2021-10–2024-05｜市場：美股｜成本：5／10／20 bps 來回〕
- **風險與限制**：獲利主要來自放空（[[2023-lopez-lira-chatgpt-forecast]] §6.1）；策略近年變弱（[[2023-lopez-lira-chatgpt-forecast]] §8.2）；需要極低交易成本（[[2023-lopez-lira-chatgpt-forecast]] §1）。預印本。
- **台股／台指期可行性**：❓ 待查。wiki 目前沒有台股或中文新聞的來源；台股放空限制與成本結構也還沒有文獻。

## 點子 2｜先遮掉公司名稱再問 LLM

- **訊號**：同點子 1，但把標題中的公司名稱與產品換成隨機字串再問（[[2023-glasserman-look-ahead-bias]] §2.4）。
- **依據**：遮掉名稱可以降低分心效應；樣本外對大公司有邊際顯著的改善（[[2023-glasserman-look-ahead-bias]] §4）。
- **文獻報告的績效**：TR 組樣本外多空日報酬，原始標題 6.07 bps、匿名標題 12.23 bps，p=0.064（[[2023-glasserman-look-ahead-bias]] §Table 3）〔期間：2021-10–2022-12｜市場：美股 S&P 500｜成本：未扣〕
- **風險與限制**：只測過 GPT-3.5，樣本外差異只有邊際顯著（[[2023-glasserman-look-ahead-bias]] §4）。預印本。
- **台股／台指期可行性**：❓ 待查。

## 點子 3｜頭版好消息比例做大盤擇時

- **訊號**：每月計算財經報紙頭版標題被 LLM 判為好消息的比例，用來預測下個月大盤（[[2025-chen-chatgpt-deepseek]] §3）。
- **依據**：好消息比例能預測未來 1–6 個月的大盤，壞消息沒有預測力（[[2025-chen-chatgpt-deepseek]] §4）。
- **文獻報告的績效**：每月在大盤與無風險資產間配置，扣 50 bps 後年化 CER 增加 3.55%（[[2025-chen-chatgpt-deepseek]] §1）〔期間：2006-01–2022-12｜市場：美股｜成本：扣 50 bps〕
- **風險與限制**：主要是樣本內結果，見 [[in-sample-vs-out-of-sample-llm-backtest]]；DeepSeek 做不到（[[2025-chen-chatgpt-deepseek]] §4）。預印本。
- **台股／台指期可行性**：❓ 待查。作者正把方法用在中文新聞與中國股市，還沒有結果（[[2025-chen-chatgpt-deepseek]] §6）。這和期末專案「財經早報 Wiki」的方向相關。
