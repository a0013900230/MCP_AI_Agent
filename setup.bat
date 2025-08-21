@echo off
chcp 65001 >nul
echo 🚀 MCP AI Agent 安裝腳本
echo ==================================================

echo 🔍 檢查 Python 版本...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python 未安裝或不在 PATH 中
    echo 請先安裝 Python 3.8 或更高版本
    pause
    exit /b 1
)

echo ✅ Python 檢查通過

echo 🔄 創建虛擬環境...
if exist "venv" (
    echo ✅ 虛擬環境已存在
) else (
    python -m venv venv
    if errorlevel 1 (
        echo ❌ 虛擬環境創建失敗
        pause
        exit /b 1
    )
    echo ✅ 虛擬環境創建成功
)

echo 🔄 創建必要目錄...
if not exist "reports" mkdir reports
if not exist "uploads" mkdir uploads
if not exist "static" mkdir static
if not exist "static\css" mkdir static\css
if not exist "static\js" mkdir static\js
if not exist "static\images" mkdir static\images
echo ✅ 目錄創建完成

echo 🔄 啟動虛擬環境...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ 虛擬環境啟動失敗
    pause
    exit /b 1
)

echo 🔄 安裝依賴套件...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ 依賴安裝失敗
    pause
    exit /b 1
)

echo.
echo ==================================================
echo 🎉 安裝完成！
echo.
echo 📋 下一步操作:
echo 1. 啟動虛擬環境: venv\Scripts\activate.bat
echo 2. 運行應用: python main.py
echo 3. 開啟瀏覽器訪問: http://localhost:8000
echo ==================================================
echo.
echo 按任意鍵啟動虛擬環境並運行應用...
pause >nul

echo 🔄 啟動虛擬環境...
call venv\Scripts\activate.bat

echo 🔄 運行應用...
python main.py

pause
