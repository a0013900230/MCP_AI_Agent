# MCP AI Agent 系統架構圖

## 🏗️ 專案架構概覽

```
returns-warranty-insights/
├── 🎯 coordinator/                    # MCP 協調器模組
│   └── mcp_coordinator.py            # 主控制代理 (MCP) - 解析用戶提示並分發任務
│
├── 🔍 retrieval/                      # 資料檢索與管理模組
│   ├── database.py                    # 資料庫管理器 - SQLite 表格創建、插入、查詢
│   ├── csv_processor.py               # CSV 處理器 - 讀取 CSV 資料並存入資料庫
│   └── retrieval_agent.py             # 檢索代理 - 處理自然語言指令和資料庫操作
│
├── 📊 reporting/                      # 報告生成與分析模組
│   ├── report_agent.py                # 報告代理 - 生成 Excel 報告
│   ├── data_analyzer.py               # 資料分析器 - 計算統計摘要和趨勢
│   └── excel_generator.py             # Excel 生成器 - 創建詳細的 Excel 報告
│
├── 🗄️ storage/                        # 資料儲存模組
│   ├── returns.db                     # SQLite 資料庫 - 儲存退貨記錄
│   ├── sample_returns.csv             # 範例 CSV 資料
│   └── reports/                       # 報告輸出目錄
│
├── 🌐 api/                            # API 服務模組
│   ├── main.py                        # FastAPI 主服務器
│   ├── routes/                        # API 路由定義
│   │   ├── /api/insert                # 插入新退貨記錄
│   │   ├── /api/query                 # 查詢退貨資料
│   │   ├── /api/statistics            # 獲取統計資料
│   │   ├── /api/generate_report       # 生成完整報告
│   │   └── /api/generate_simple_report # 生成簡單報告
│   └── middleware/                    # 中間件 (錯誤處理、日誌記錄)
│
├── 🎨 frontend/                       # 前端介面模組
│   ├── templates/                     # HTML 模板
│   │   └── index.html                 # 主頁面 - 用戶輸入提示的介面
│   ├── static/                        # 靜態資源
│   │   ├── css/                       # 樣式表
│   │   ├── js/                        # JavaScript 功能
│   │   └── images/                    # 圖片資源
│   └── components/                    # 前端組件
│       ├── prompt_input.py            # 提示輸入組件 - 接受自然語言提示
│       └── report_display.py          # 報告顯示組件 - 顯示退貨列表和下載 Excel 報告
│
├── 🛠️ utils/                          # 工具模組
│   ├── setup.py                       # 安裝腳本 - 自動化環境設置
│   ├── setup.bat                      # Windows 安裝批次檔
│   ├── requirements.txt               # 依賴管理 - 列出所需的 Python 套件
│   └── logger.py                      # 日誌記錄器 - 記錄系統操作和錯誤
│
├── 📚 docs/                           # 文檔模組
│   ├── README.md                      # 專案說明文檔
│   ├── ARCHITECTURE.md                # 架構說明文檔 (本檔案)
│   └── API_REFERENCE.md               # API 參考文檔
│
└── 🧪 tests/                          # 測試模組
    ├── test_database.py               # 資料庫功能測試
    ├── test_agents.py                 # Agent 功能測試
    └── test_api.py                    # API 端點測試
```

## 🔄 資料流程圖

```
用戶輸入自然語言提示
         ↓
    MCP 協調器解析
         ↓
    ┌─────────────┬─────────────┐
    ↓             ↓             ↓
Retrieval Agent  Report Agent  其他 Agent
    ↓             ↓
資料庫操作      資料分析
    ↓             ↓
SQLite 儲存     Excel 報告
    ↓             ↓
    └─────────────┴─────────────┘
         ↓
    結果返回用戶
```

## 🎯 核心模組詳細說明

### **1. MCP 協調器 (mcp_coordinator.py)**
- **角色**: 主控制代理，負責解析用戶提示並分發任務
- **功能**: 
  - 自然語言理解
  - 任務分類和路由
  - Agent 協調管理
  - 結果整合和返回

### **2. 檢索代理 (retrieval_agent.py)**
- **角色**: 處理資料檢索、插入和查詢操作
- **功能**:
  - CSV 資料導入和索引
  - 新退貨記錄插入
  - 資料庫查詢和過濾
  - 自然語言指令處理

### **3. 報告代理 (report_agent.py)**
- **角色**: 生成資料分析和 Excel 報告
- **功能**:
  - 統計資料計算
  - 趨勢分析
  - Excel 報告生成
  - 報告格式化和樣式

### **4. 資料庫管理器 (database.py)**
- **角色**: 管理 SQLite 資料庫操作
- **功能**:
  - 表格創建和管理
  - 資料插入和更新
  - 查詢和過濾
  - 資料驗證和清理

### **5. FastAPI 主服務器 (main.py)**
- **角色**: 提供 Web API 服務
- **功能**:
  - RESTful API 端點
  - 靜態檔案服務
  - 模板渲染
  - 錯誤處理和日誌

## 🔧 技術棧對應

| 功能模組 | 技術實現 | 說明 |
|---------|----------|------|
| **Web 框架** | FastAPI | 現代化、高性能的 Python Web 框架 |
| **資料庫** | SQLite | 輕量級、無需配置的關聯式資料庫 |
| **資料處理** | Pandas | 強大的資料分析和操作庫 |
| **報告生成** | OpenPyXL | 專業的 Excel 檔案操作庫 |
| **模板引擎** | Jinja2 | 靈活的 HTML 模板系統 |
| **前端框架** | Bootstrap + JavaScript | 響應式、現代化的 UI 框架 |
| **API 文檔** | FastAPI 自動生成 | 自動生成 Swagger/OpenAPI 文檔 |

## 📊 資料模型

### **退貨記錄表格結構**
```sql
CREATE TABLE returns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id TEXT NOT NULL,           -- 訂單 ID
    product TEXT NOT NULL,            -- 產品名稱
    store_name TEXT NOT NULL,         -- 商店名稱
    return_date DATE NOT NULL,        -- 退貨日期
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- 創建時間
);
```

### **統計資料結構**
```python
{
    'total_returns': int,             # 總退貨數量
    'store_stats': [                  # 按商店統計
        {'store_name': str, 'count': int}
    ],
    'product_stats': [                # 按產品統計
        {'product': str, 'count': int}
    ],
    'monthly_stats': [                # 按月份統計
        {'month': str, 'count': int}
    ]
}
```

## 🚀 部署架構

### **本地開發環境**
```
用戶電腦 → Python 虛擬環境 → FastAPI 服務器 → SQLite 資料庫
    ↓
瀏覽器 → http://localhost:8000 → 前端介面
```

### **生產環境部署**
```
用戶 → 負載平衡器 → 多個 FastAPI 實例 → 共享資料庫
    ↓
CDN → 靜態資源快取
```

## 🔒 安全與權限

- **資料驗證**: 所有輸入資料都經過驗證
- **SQL 注入防護**: 使用參數化查詢
- **檔案上傳安全**: 限制檔案類型和大小
- **錯誤處理**: 不暴露敏感系統資訊

## 📈 擴展性設計

- **模組化架構**: 每個 Agent 都是獨立模組
- **插件系統**: 可以輕鬆添加新的 Agent
- **配置驅動**: 通過配置檔案調整行為
- **API 優先**: 支援多種前端和客戶端

## 🎯 與原始需求對比

| 原始需求 | 實現狀態 | 說明 |
|---------|----------|------|
| ✅ MCP 風格協調器 | 完全實現 | `mcp_coordinator.py` |
| ✅ Retrieval Agent | 完全實現 | `retrieval_agent.py` + `database.py` |
| ✅ Report Agent | 完全實現 | `report_agent.py` |
| ✅ CSV 索引 | 完全實現 | `import_csv_data()` 方法 |
| ✅ 自然語言處理 | 完全實現 | 支援中文的自然語言指令 |
| ✅ Excel 報告 | 完全實現 | 完整的 Excel 報告生成 |
| ✅ 輕量級資料庫 | 完全實現 | SQLite 資料庫 |

這個架構完全符合你的專案需求，並且在技術實現上更加現代化和專業！🎉
