# Inventory Service

以 FastAPI 和 SQLite 建立的商品管理 API。

這是一個 Python 後端開發的專案，本檔案修改時功能包含 CRUD、資料驗證、錯誤處理、交易、分類篩選、價格排序和自動化測試。

## 功能

- 新增商品
- 查詢商品列表
- 查詢單一商品
- 更新商品
- 刪除商品
- 依分類篩選商品
- 依價格升冪或降冪排序
- 業務規則與輸入驗證
- SQLite 交易與 rollback
- pytest API 與 Service 測試

## 使用技術

- Python 3.14
- FastAPI
- Uvicorn
- SQLite
- pytest
- HTTPX2

目前已使用 Python 3.14 驗證安裝與測試流程。

## 安裝

下載專案後，進入專案目錄：

```powershell
cd inventory-service
```

建立虛擬環境：

```powershell
python -m venv .venv
```

Windows PowerShell 啟用方式：

```powershell
.venv\Scripts\Activate.ps1
```

macOS 或 Linux 啟用方式：

```bash
source .venv/bin/activate
```

安裝依賴：

```powershell
python -m pip install -r requirements.txt
```

確認依賴沒有衝突：

```powershell
python -m pip check
```

## 啟動 API

在專案根目錄執行：

```powershell
python -m uvicorn main:app --reload
```

啟動後可開啟：

- API 根目錄：[http://127.0.0.1:8000](http://127.0.0.1:8000)
- Swagger API 文件：[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc 文件：[http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

第一次啟動時會自動建立 SQLite 資料庫檔案 `items.db`。

## 商品資料格式

新增或更新商品時，請提供：

```json
{
  "name": "apple",
  "category": "food",
  "price": 30,
  "quantity": 10
}
```

欄位規則：

| 欄位         | 型別      | 規則             |
| ---------- | ------- | -------------- |
| `name`     | string  | 不可為空字串         |
| `category` | string  | 商品分類           |
| `price`    | integer | 不可小於 0         |
| `quantity` | integer | 必須介於 0 到 10000 |

## API

| 方法       | 路徑            | 功能          |
| -------- | ------------- | ----------- |
| `GET`    | `/`           | 確認 API 是否運作 |
| `POST`   | `/items`      | 新增商品        |
| `GET`    | `/items`      | 查詢商品列表      |
| `GET`    | `/items/{id}` | 查詢單一商品      |
| `PUT`    | `/items/{id}` | 更新商品        |
| `DELETE` | `/items/{id}` | 刪除商品        |

### 依分類篩選

```http
GET /items?category=food
```

只回傳 `category` 等於 `food` 的商品。

### 依價格排序

價格由低到高：

```http
GET /items?sort_by=price&order=asc
```

價格由高到低：

```http
GET /items?sort_by=price&order=desc
```

`sort_by` 目前只接受 `price`，`order` 只接受 `asc` 或 `desc`。

### 同時篩選和排序

```http
GET /items?category=food&sort_by=price&order=asc
```

## HTTP 狀態碼

| 狀態碼   | 意義          |
| ----- | ----------- |
| `200` | 查詢或更新成功     |
| `201` | 商品建立成功      |
| `204` | 商品刪除成功      |
| `400` | 違反業務規則      |
| `404` | 找不到商品       |
| `422` | 輸入格式或查詢參數錯誤 |

## 執行測試

執行全部測試：

```powershell
python -m pytest -v
```

只執行 API 測試：

```powershell
python -m pytest tests/test_api.py -v
```

只執行 Service 測試：

```powershell
python -m pytest tests/test_service.py -v
```

## 專案結構

```text
inventory-service/
├── main.py               # FastAPI 路由與錯誤處理
├── models.py             # API 輸入與輸出模型
├── database_models.py    # 內部商品資料模型
├── service.py            # 業務規則與交易控制
├── database.py           # SQLite 查詢
├── exceptions.py         # 自訂例外
├── requirements.txt      # Python 依賴
└── tests/
    ├── conftest.py       # 共用測試資料庫設定
    ├── test_api.py       # API 測試
    └── test_service.py   # Service 與交易測試
```
