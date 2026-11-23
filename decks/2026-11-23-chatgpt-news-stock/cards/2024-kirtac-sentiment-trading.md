---
source: 2024-kirtac-sentiment-trading
tier: A
updated: 2026-11-23
---

# 證據卡：Kirtac & Germano（Finance Research Letters 2024）

- **kg-1**｜樣本是 2010-01-01 到 2023-06-30 的美股新聞，篩選後 965,375 篇（[[2024-kirtac-sentiment-trading]] §2.1）
- **kg-2**｜BERT、OPT 用「發布後 3 天超額報酬的正負」當標籤微調；測試集是隨機抽 20%（[[2024-kirtac-sentiment-trading]] §2.2）〔期間：2010–2023｜市場：美股｜成本：不適用（方法說明）〕
- **kg-3**｜預測 3 日報酬方向：OPT（類 GPT-3 的模型，2.7B 參數）accuracy 0.744、詞典法 0.501（[[2024-kirtac-sentiment-trading]] §Table 3）〔期間：2010–2023｜市場：美股｜成本：不適用（分類準確率）〕
- **kg-4**｜扣 10 bps 後多空 Sharpe：OPT 3.05、BERT 2.11、FinBERT 2.07、詞典 1.23（[[2024-kirtac-sentiment-trading]] §Table 5）〔期間：未說明（表 5 只寫「樣本期間」）｜市場：美股｜成本：扣 10 bps〕
- **kg-5**｜兩篇對 BERT／FinBERT 的結論相反，差在「直接問 vs 用報酬微調」與「樣本外 vs 隨機切分」；使用者決定並陳、不判輸贏（[[zero-shot-vs-fine-tuned-sentiment]] §使用者的決定）
