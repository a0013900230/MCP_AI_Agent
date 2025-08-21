# MCP AI Agent 系統架構圖 (ASCII 版本)

## 🏗️ 系統整體架構

```
┌─────────────────────────────────────────────────────────────────┐
│                    MCP AI Agent 系統                            │
│              Returns & Warranty Insights                       │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
                    ┌─────────────────────┐
                    │   MCP Coordinator   │
                    │  (mcp_coordinator)  │
                    │                     │
                    │ • 自然語言解析      │
                    │ • 任務分發          │
                    │ • Agent 協調        │
                    └─────────────────────┘
                                │
                    ┌───────────┼───────────┐
                    │           │           │
                    ▼           ▼           ▼
        ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
        │ Retrieval Agent │ │  Report Agent   │ │  Future Agent   │
        │                 │ │                 │ │                 │
        │ • CSV 處理      │ │ • 資料分析      │ │ • 擴展功能      │
        │ • 資料庫操作    │ │ • Excel 報告    │ │                 │
        │ • 自然語言查詢  │ │ • 統計計算      │ │                 │
        └─────────────────┘ └─────────────────┘ └─────────────────┘
                    │           │
                    ▼           ▼
        ┌─────────────────┐ ┌─────────────────┐
        │   Database      │ │   Reports       │
        │   (SQLite)      │ │   (Excel)       │
        │                 │ │                 │
        │ • returns 表格  │ │ • 完整報告      │
        │ • 資料 CRUD     │ │ • 簡單報告      │
        │ • 統計查詢      │ │ • 趨勢分析      │
        └─────────────────┘ └─────────────────┘
                                │
                                ▼
                    ┌─────────────────────┐
                    │   FastAPI Server    │
                    │     (main.py)       │
                    │                     │
                    │ • RESTful API       │
                    │ • 靜態檔案服務      │
                    │ • 模板渲染          │
                    └─────────────────────┘
                                │
                                ▼
                    ┌─────────────────────┐
                    │   Web Interface     │
                    │   (templates/)      │
                    │                     │
                    │ • 自然語言輸入      │
                    │ • 資料顯示          │
                    │ • 報告下載          │
                    └─────────────────────┘
```

## 🔄 資料流程

```
用戶輸入 → MCP 協調器 → Agent 選擇 → 任務執行 → 結果返回
   │           │           │           │           │
   ▼           ▼           ▼           ▼           ▼
自然語言   解析指令    分發任務    資料處理    顯示結果
   │           │           │           │           │
   ▼           ▼           ▼           ▼           ▼
瀏覽器     Python     選擇合適    SQLite/     HTML/JS
介面      邏輯       的 Agent    Excel      輸出
```

## 🎯 核心組件關係

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   User      │    │   MCP      │    │   Agents    │
│  Input      │───▶│Coordinator │───▶│             │
└─────────────┘    └─────────────┘    └─────────────┘
                           │                   │
                           ▼                   ▼
                    ┌─────────────┐    ┌─────────────┐
                    │   Task      │    │   Data      │
                    │ Routing     │    │ Processing  │
                    └─────────────┘    └─────────────┘
                           │                   │
                           ▼                   ▼
                    ┌─────────────┐    ┌─────────────┐
                    │   Agent     │    │   Storage   │
                    │ Selection   │    │   & Output  │
                    └─────────────┘    └─────────────┘
```

## 📊 技術棧對應

```
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│   Frontend      │  │   Backend       │  │   Database      │
│                 │  │                 │  │                 │
│ • HTML5         │  │ • Python        │  │ • SQLite        │
│ • CSS3          │  │ • FastAPI       │  │ • Pandas        │
│ • JavaScript    │  │ • Jinja2        │  │ • OpenPyXL      │
│ • Bootstrap     │  │ • Uvicorn       │  │                 │
└─────────────────┘  └─────────────────┘  └─────────────────┘
         │                     │                     │
         └─────────────────────┼─────────────────────┘
                               │
                    ┌─────────────────┐
                    │   MCP System    │
                    │                 │
                    │ • Coordinator   │
                    │ • Agents        │
                    │ • Task Flow     │
                    └─────────────────┘
```

## 🚀 部署架構

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   User      │    │   Web      │    │   Python    │
│  Browser    │───▶│  Server    │───▶│  Virtual   │
│             │    │ (Port 8000)│    │ Environment │
└─────────────┘    └─────────────┘    └─────────────┘
                           │                   │
                           ▼                   ▼
                    ┌─────────────┐    ┌─────────────┐
                    │   Static    │    │   Database  │
                    │   Files     │    │   (SQLite)  │
                    │ (CSS/JS)    │    │             │
                    └─────────────┘    └─────────────┘
```

## 📁 檔案結構對應

```
實際檔案結構                    │    架構模組
─────────────────────────────────┼─────────────────────
main.py                         │  FastAPI Server
mcp_coordinator.py              │  MCP Coordinator
retrieval_agent.py              │  Retrieval Agent
report_agent.py                 │  Report Agent
database.py                     │  Database Manager
templates/index.html            │  Web Interface
static/                         │  Static Resources
requirements.txt                │  Dependencies
setup.py                       │  Installation
README.md                      │  Documentation
```

## 🎯 系統特色

- **🎯 MCP 架構**: 協調器 + 多個專業 Agent
- **🔍 智能檢索**: 自然語言處理 + 資料庫操作
- **📊 專業報告**: Excel 格式 + 統計分析
- **🌐 現代化介面**: 響應式設計 + 用戶友好
- **🚀 易於部署**: 一鍵安裝 + 自動化配置
- **📈 可擴展性**: 模組化設計 + 插件支援

這個架構完全展示了你的 Python 專案的專業性和完整性！🎉
