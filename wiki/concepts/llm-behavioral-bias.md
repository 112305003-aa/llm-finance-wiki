---
title: LLM 的行為偏誤（Behavioral Biases in LLMs）
type: concept
summary: LLM 從人類文字學到人類的偏誤：過度外推、過度樂觀
tags: [bias, models]
aliases: [行為偏誤, 外推, extrapolation, 過度樂觀, miscalibration, 校準]
sources: [2024-chen-historical-returns, 2023-glasserman-look-ahead-bias]
updated: 2026-11-23
---

LLM 是讀人類寫的文字長大的，所以可能也學到人類的壞習慣。例如**過度外推（extrapolation）**：最近漲得好，就以為會繼續漲。

## 為什麼重要

如果拿 LLM 當「冷靜的分析師」，卻不知道它會犯和人一樣的錯，就可能被它誤導（[[2024-chen-historical-returns]] §3.3）。

## 怎麼運作

- **外推**：GPT-4o 把最近一週的報酬看得最重，可是實際的短期報酬會反轉（[[2024-chen-historical-returns]] §3.1）。
- **過度樂觀**：GPT-4o 的預期月報酬 2.2%，實際只有 1.15%（[[2024-chen-historical-returns]] §3.2）〔期間：1926–2023 隨機抽樣｜市場：美股｜成本：不適用（預測評估）〕
- **過度自信**：讀新聞時，GPT-3.5 對有公司名稱的標題比較敢下判斷，結果判錯的損失最大（[[2023-glasserman-look-ahead-bias]] §3.3.2）。
- **很難用 prompt 關掉**：模型知道這些偏誤的定義，但偏誤藏在訓練資料裡（[[2024-chen-historical-returns]] §3.3）。

## 發展脈絡

- **2023**｜讀新聞時的過度自信與分心效應（[[2023-glasserman-look-ahead-bias]] §3.3.2）。預印本。
- **2024**｜看數字預測時的外推與過度樂觀，Claude 也一樣（[[2024-chen-historical-returns]] §1）。預印本。

## 常見誤解

- ❌「LLM 是機器，所以比人理性」→ ✅ 它的外推方式和人類非常像（[[2024-chen-historical-returns]] §1）。
- ❌「叫它扮演專業投資人就會變理性」→ ✅ 加上這種角色設定幾乎沒有影響（[[2024-chen-historical-returns]] §3.3）。

## 相關頁面

- [[distraction-effect]]、[[model-scale]]
