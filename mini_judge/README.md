# Mini Judge - 線上程式碼檢查與執行平台

Mini Judge 是一個提供智慧程式碼分析和執行功能的平台，可在編譯前檢查常見的語法錯誤。

## 專案結構

```
mini_judge/
├── backend/
│   ├── main.py           # FastAPI 入口
│   ├── analyzer.py       # 智慧提示（Pre-Compile Analyzer）
│   ├── runner.py         # 本地執行程式 & 輸出比對
│   └── rules/
│       ├── __init__.py     # 匯出各 rule
│       ├── full_width.py   # 規則 1：全形符號
│       ├── brackets.py     # 規則 2：括號未成對
│       ├── quotes.py       # 規則 3：引號未封閉
│       └── confusable.py   # 規則 4：相似字元
├── frontend/
│   └── index.html        # 最簡版前端頁面
└── requirements.txt      # Python 依賴套件
```

## 功能特色

### 智慧分析檢查（Pre-Compile Analyzer）

1. **全形符號檢查** - 偵測中文全形符號（如：（、）、；等）
2. **括號配對檢查** - 偵測未配對的括號（()、[]、{}）
3. **引號封閉檢查** - 偵測未封閉的單引號或雙引號
4. **相似字元檢查** - 偵測容易混淆的字元（如：西里爾字母 vs 拉丁字母）

### 程式執行功能

- 支援多種程式語言：Python、C、C++、Java
- 提供測試輸入
- 自動比對預期輸出
- 顯示執行時間

## 安裝與執行

### 安裝依賴

```bash
cd mini_judge
pip install -r requirements.txt
```

### 啟動後端伺服器

```bash
cd backend
python -m uvicorn main:app --reload
```

或直接執行：

```bash
python -m mini_judge.backend.main
```

伺服器將在 `http://localhost:8000` 啟動。

### 開啟前端

使用瀏覽器開啟 `frontend/index.html` 檔案，或使用簡單的 HTTP 伺服器：

```bash
cd frontend
python -m http.server 8080
```

然後在瀏覽器訪問 `http://localhost:8080`。

## API 端點

### 分析端點

- `POST /analyze` - 分析程式碼
- `POST /analyze/formatted` - 分析程式碼（格式化輸出）

### 執行端點

- `POST /run` - 執行程式碼
- `POST /test` - 執行多個測試案例

### 其他端點

- `GET /` - API 資訊
- `GET /rules` - 列出所有可用規則
- `GET /health` - 健康檢查

## 使用範例

### 分析程式碼

```python
import requests

response = requests.post('http://localhost:8000/analyze', json={
    'code': 'print（"Hello"）',  # 包含全形括號
    'rules': ['full_width']
})

print(response.json())
```

### 執行程式碼

```python
import requests

response = requests.post('http://localhost:8000/run', json={
    'code': 'print("Hello, World!")',
    'language': 'python',
    'test_input': '',
    'expected_output': 'Hello, World!\n'
})

print(response.json())
```

## 開發說明

### 新增檢查規則

1. 在 `backend/rules/` 目錄下新增規則檔案
2. 實作檢查函數，返回問題清單
3. 在 `backend/rules/__init__.py` 中匯出新規則
4. 在 `backend/analyzer.py` 的 `CodeAnalyzer` 中註冊規則

### 規則函數格式

```python
def check_xxx(code: str) -> list[dict]:
    """
    檢查程式碼
    
    Returns:
        問題清單，每個問題包含：
        - line: 行號
        - column: 列號
        - char: 問題字元
        - message: 錯誤訊息
        - suggestion: 建議修正（選填）
    """
    issues = []
    # 實作檢查邏輯
    return issues
```

## 技術棧

- **後端**: FastAPI、Python 3.8+
- **前端**: HTML、CSS、JavaScript（純前端，無框架）
- **程式執行**: subprocess（支援 Python、C、C++、Java）

## 授權

MIT License

## 貢獻

歡迎提交 Issue 和 Pull Request！
