# Computer-network-final-project-2025-fall
mini_judge/
├─ backend/
│ ├─ main.py # FastAPI 入口
│ ├─ analyzer.py # 智慧提示（Pre-Compile Analyzer）
│ ├─ runner.py # 本地執行程式 & 輸出比對
│ └─ rules/
│ ├─ init.py # 匯出各 rule
│ ├─ full_width.py # 規則 1：全形符號
│ ├─ brackets.py # 規則 2：括號未成對
│ ├─ quotes.py # 規則 3：引號未封閉
│ └─ confusable.py # 規則 4：相似字元
├─ frontend/
│ └─ index.html # 最簡版前端頁面
