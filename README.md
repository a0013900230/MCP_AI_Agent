# 退貨與保固分析系統 (Returns & Warranty Insights)

這是一個基於 MCP (Model Context Protocol) 風格的 Python 應用程式，包含兩個協作的 agent 來處理退貨資料分析和報告生成。

## 專案架構

- **MCP Coordinator**: 協調兩個 agent 的工作流程
- **Retrieval Agent**: 處理 CSV 資料讀取、索引和資料庫操作
- **Report Agent**: 生成 Excel 報告

## 🚀 快速安裝

### 方法 1: 使用安裝腳本 (推薦)

#### Windows 使用者
```bash
# 雙擊執行 setup.bat
# 或以管理員身份執行
setup.bat
```

#### macOS/Linux 使用者
```bash
# 執行安裝腳本
python setup.py
```

### 方法 2: 手動安裝

1. **檢查 Python 版本**
   ```bash
   python --version
   # 需要 Python 3.8 或更高版本
   ```

2. **升級 pip**
   ```bash
   python -m pip install --upgrade pip
   ```

3. **安裝依賴套件**
   ```bash
   pip install -r requirements.txt
   ```

4. **建立必要目錄**
   ```bash
   mkdir reports uploads templates
   ```

## 🏃‍♂️ 執行系統

### 啟動應用程式
```bash
# 直接執行主程式
python main.py
```

### 訪問系統
開啟瀏覽器訪問：http://localhost:8000

## 🔧 故障排除

### 常見問題

#### 1. 虛擬環境建立失敗
**錯誤**: `CREATE_VENV.PIP_FAILED_INSTALL_REQUIREMENTS`

**解決方案**:
```bash
# 升級 pip
python -m pip install --upgrade pip

# 清除 pip 快取
pip cache purge

# 重新安裝依賴
pip install -r requirements.txt --no-cache-dir
```

#### 2. 套件安裝失敗
**錯誤**: `ERROR: Could not find a version that satisfies the requirement`

**解決方案**:
```bash
# 使用國內鏡像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 或使用阿里雲鏡像
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```

#### 3. 權限問題
**錯誤**: `Permission denied`

**解決方案**:
```bash
# Windows: 以管理員身份執行命令提示字元
# macOS/Linux: 使用 sudo
sudo pip install -r requirements.txt
```

#### 4. 網路連接問題
**錯誤**: `Connection timeout`

**解決方案**:
- 檢查網路連接
- 檢查防火牆設定
- 使用 VPN 或代理伺服器

### 系統要求

- **Python**: 3.8 或更高版本
- **記憶體**: 最少 2GB RAM
- **硬碟空間**: 最少 100MB 可用空間
- **作業系統**: Windows 10+, macOS 10.14+, Ubuntu 18.04+

## 📖 使用規則

### 當與 Agent 互動時，請遵循以下規則：

1. **明確性**: 使用清楚、具體的語言描述你的需求
2. **一次一個任務**: 每次只要求一個 agent 執行一個任務
3. **資料格式**: 確保 CSV 檔案格式正確（包含必要的欄位）
4. **查詢語言**: 使用自然語言描述你的查詢需求

### 範例提示詞：

- "請分析最近的退貨趨勢"
- "新增一筆退貨記錄：訂單ID 12345，產品名稱 iPhone，商店名稱 台北店，日期 2024-01-15"
- "生成本月的退貨分析報告"

## ✨ 功能特色

- CSV 資料自動索引和處理
- SQLite 資料庫儲存退貨記錄
- 自然語言查詢介面
- 自動生成 Excel 報告
- 即時資料更新和查詢

## 🏗️ 技術架構

- **後端**: FastAPI + Python
- **資料庫**: SQLite
- **資料處理**: Pandas
- **報告生成**: OpenPyXL
- **前端**: HTML + JavaScript

## 📁 專案結構

```
緯創面試/
├── main.py                 # FastAPI 主應用程式
├── mcp_coordinator.py      # MCP 協調器
├── retrieval_agent.py      # 檢索代理（讀寫）
├── report_agent.py         # 報告代理
├── database.py             # 資料庫管理
├── requirements.txt        # 依賴套件
├── setup.py                # Python 安裝腳本
├── setup.bat               # Windows 安裝腳本
├── sample_returns.csv      # 範例 CSV 資料
├── templates/
│   └── index.html         # 前端介面
├── README.md               # 專案說明
└── .gitignore             # Git 忽略檔案
```

## 🆘 需要幫助？

如果遇到問題，請：

1. 檢查 Python 版本是否符合要求
2. 執行 `python setup.py` 重新安裝環境
3. 查看錯誤訊息和故障排除指南
4. 確保網路連接正常

## 📝 注意事項

- 確保 CSV 檔案包含必要的欄位（order_id, product, store_name, date）
- 資料庫檔案會自動在專案目錄中建立
- 報告檔案會儲存在 reports/ 目錄中
- 首次執行可能需要較長時間來安裝依賴套件
