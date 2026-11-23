---
source: 2023-lopez-lira-chatgpt-forecast
tier: B
updated: 2026-11-23
---

# 證據卡：Lopez-Lira & Tang（v6）

- **lt-1**｜樣本是美股 2021-10 到 2024-05，共 159,137 筆公司–標題–日期觀測（[[2023-lopez-lira-chatgpt-forecast]] §4）
- **lt-2**｜Prompt 請模型扮演金融專家，回答 YES／NO／UNKNOWN，轉成 1／0／−1 的分數（[[2023-lopez-lira-chatgpt-forecast]] §5）
- **lt-3**｜gpt-4-0314 訓練資料只到 2021-09，樣本從 2021-10 開始，確保是樣本外（[[2023-lopez-lira-chatgpt-forecast]] §4）
- **lt-4**｜預測新聞發布當下的初始反應，隔夜新聞日命中率 93.3%，但這來不及交易（[[2023-lopez-lira-chatgpt-forecast]] §6.1）
- **lt-5**｜可交易的漂移較弱：隔夜新聞漂移策略日命中率 58%（[[2023-lopez-lira-chatgpt-forecast]] §6.1）
- **lt-6**｜隔夜新聞漂移策略平均每日 0.34%、年化 Sharpe ratio 2.97（[[2023-lopez-lira-chatgpt-forecast]] §Table 1）〔期間：2021-10–2024-05｜市場：美股｜成本：未扣〕
- **lt-7**｜壞消息更有用：空方每日 26 bps、多方 8 bps（[[2023-lopez-lira-chatgpt-forecast]] §6.1）〔期間：2021-10–2024-05｜市場：美股｜成本：未扣〕
- **lt-8**｜每次來回成本 5 bps 累積報酬仍超過 300%、10 bps 仍高於 100%、20 bps 不賺錢（[[2023-lopez-lira-chatgpt-forecast]] §6.2）〔期間：2021-10–2024-05｜市場：美股｜成本：5／10／20 bps 來回〕
- **lt-9**｜模型越大越好：GPT-3.5 Sharpe 1.66，GPT-1、GPT-2、BERT 為負（[[2023-lopez-lira-chatgpt-forecast]] §7.1）〔期間：2021-10–2024-05｜市場：美股｜成本：未扣〕
- **lt-10**｜年化 Sharpe 從 2021Q4 的 6.54 降到 2024 年 1–5 月的 1.22，作者認為與 LLM 普及一致，但也可能是市場環境改變（[[2023-lopez-lira-chatgpt-forecast]] §8.2）〔期間：2021Q4–2024-05｜市場：美股｜成本：未扣〕
- **lt-11**｜資訊約兩天被吸收：第 1 天 34 bps、第 2 天 19 bps（[[2023-lopez-lira-chatgpt-forecast]] §8.1）〔期間：2021-10–2024-05｜市場：美股｜成本：未扣〕
- **lt-12**｜只有交易成本夠低的參與者（例如造市商）能利用（[[2023-lopez-lira-chatgpt-forecast]] §1）
