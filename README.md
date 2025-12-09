# Computer-network-final-project-2025-fall

簡易的線上程式碼 Judge 雛形，包含 Flask 後端與最簡版前端。

```text
mini_judge/
├─ backend/
│  ├─ main.py           # Flask 入口（提供靜態檢查與執行 API）
│  ├─ analyzer.py       # 智慧提示（Pre-Compile Analyzer）
│  ├─ runner.py         # 本地執行程式 & 輸出比對
│  └─ rules/
│     ├─ __init__.py     # 匯出各 rule
│     ├─ full_width.py   # 規則 1：全形符號
│     ├─ brackets.py     # 規則 2：括號未成對
│     ├─ quotes.py       # 規則 3：引號未封閉
│     └─ confusable.py   # 規則 4：相似字元
├─ frontend/
│  └─ index.html        # 最簡版前端頁面
```

## 快速啟動

1. 安裝依賴：`pip install flask`
2. 啟動後端：
   ```bash
   python -m mini_judge.backend.main
   ```
3. 將 `frontend/index.html` 以瀏覽器開啟，即可透過 `/api/analyze`、`/api/run` 進行測試。
