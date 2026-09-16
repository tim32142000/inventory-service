# Item Management API

一個以 **FastAPI** 建構的商品（Item）管理 RESTful API，使用 **SQLite** 作為資料儲存，並透過 **pytest** 進行自動化測試。專案採用分層架構（Router / Service / Database），並使用 Pydantic 進行資料驗證。

## 功能特色

- 商品的新增、查詢、修改、刪除（CRUD）
- 使用 Pydantic 模型驗證輸入資料（名稱不可為空、價格與數量不可為負數）
- 業務邏輯層（Service）獨立於資料庫存取層（Database），方便維護與測試
- 完整的 pytest 測試套件，使用獨立的臨時資料庫進行測試，避免污染正式資料

## 專案結構

```
.
├── main.py               # FastAPI 路由（API 進入點）
├── models.py             # Pydantic 請求/回應模型
├── database_models.py    # Item 資料類別（dataclass）
├── database.py           # SQLite 連線與資料存取（CRUD SQL）
├── service.py            # 業務邏輯層（驗證規則、交易處理）
├── requirements.txt      # 相依套件
├── items.db              # SQLite 資料庫檔案（執行後自動產生）
└── tests/
    └── test_api.py       # API 整合測試
```

## 環境需求

- Python 3.10 以上（使用了 `int | None` 型別語法）

## 安裝方式

```bash
# 建立虛擬環境（可選）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安裝相依套件
pip install -r requirements.txt
```

主要相依套件：

| 套件      | 用途                     |
|-----------|--------------------------|
| fastapi   | Web API 框架             |
| uvicorn   | ASGI 伺服器              |
| pytest    | 測試框架                 |
| httpx     | TestClient 底層 HTTP 客戶端 |

## 啟動伺服器

```bash
uvicorn main:app --reload
```

啟動後可至 `http://127.0.0.1:8000/docs` 查看自動產生的 Swagger UI 文件。

## API 端點說明

| 方法   | 路徑            | 說明             | 回傳狀態碼 |
|--------|-----------------|------------------|------------|
| GET    | `/`             | 運行狀態檢查         | 200        |
| GET    | `/items`        | 取得所有商品     | 200        |
| GET    | `/items/{id}`   | 取得單一商品     | 200 / 404  |
| POST   | `/items`        | 新增商品         | 201 / 422  |
| PUT    | `/items/{id}`   | 更新商品         | 200 / 400 / 404 / 422 |
| DELETE | `/items/{id}`   | 刪除商品         | 204 / 404  |

### 商品資料格式

```json
{
  "name": "範例商品",
  "category": "test",
  "price": 100,
  "quantity": 10
}
```

- `name`：字串，長度必須大於 0
- `category`：字串
- `price`：整數，必須 ≥ 0
- `quantity`：整數，必須 ≥ 0，且更新時不可超過 10000（超過會回傳 400 錯誤）


## 執行測試

```bash
pytest
```

測試會針對每個測試案例建立獨立的臨時 SQLite 資料庫，涵蓋以下情境：

- 基本 CRUD 流程
- 邊界值測試（數量為 0 或 10000）
- 無效輸入驗證（負數價格/數量、空白名稱、型別錯誤）
- 查詢或刪除不存在的商品（404）
- 更新數量超過上限（400）

## 架構設計說明

專案採用三層架構：

1. **`main.py`（Router 層）**：負責處理 HTTP 請求與回應，將請求轉換為 `Item` 物件並呼叫對應的 Service 函式，並處理例外轉換為 HTTP 狀態碼。
2. **`service.py`（Service 層）**：包含業務規則（例如數量上限驗證），並負責資料庫交易（commit / rollback）。
3. **`database.py`（Database 層）**：負責實際的 SQL 操作與資料庫連線管理。

分層設計讓業務邏輯與資料庫實作互相獨立，也方便針對不同層級撰寫測試。

---