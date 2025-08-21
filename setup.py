#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
簡化安裝腳本
自動創建虛擬環境並安裝依賴
"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """執行命令並顯示結果"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} 成功")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} 失敗: {e}")
        if e.stderr:
            print(f"錯誤詳情: {e.stderr}")
        return False

def check_python_version():
    """檢查 Python 版本"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ 需要 Python 3.8 或更高版本")
        print(f"當前版本: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python 版本檢查通過: {version.major}.{version.minor}.{version.micro}")
    return True

def create_venv():
    """創建虛擬環境"""
    if os.path.exists("venv"):
        print("✅ 虛擬環境已存在")
        return True
    
    print("🔄 創建虛擬環境...")
    if run_command("python -m venv venv", "創建虛擬環境"):
        print("✅ 虛擬環境創建成功")
        return True
    return False

def activate_venv():
    """啟動虛擬環境"""
    if platform.system() == "Windows":
        activate_script = "venv\\Scripts\\Activate.ps1"
        if os.path.exists(activate_script):
            print("✅ 虛擬環境啟動腳本準備就緒")
            print("請執行: venv\\Scripts\\Activate.ps1")
            return True
    else:
        activate_script = "venv/bin/activate"
        if os.path.exists(activate_script):
            print("✅ 虛擬環境啟動腳本準備就緒")
            print("請執行: source venv/bin/activate")
            return True
    
    print("❌ 虛擬環境啟動腳本未找到")
    return False

def install_requirements():
    """安裝依賴套件"""
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt 檔案不存在")
        return False
    
    print("🔄 安裝依賴套件...")
    if platform.system() == "Windows":
        pip_cmd = "venv\\Scripts\\pip install -r requirements.txt"
    else:
        pip_cmd = "venv/bin/pip install -r requirements.txt"
    
    return run_command(pip_cmd, "安裝依賴套件")

def create_directories():
    """創建必要的目錄"""
    directories = [
        "reports",
        "uploads", 
        "static",
        "static/css",
        "static/js",
        "static/images"
    ]
    
    print("🔄 創建必要目錄...")
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"✅ 創建目錄: {directory}")
        else:
            print(f"✅ 目錄已存在: {directory}")

def main():
    """主安裝流程"""
    print("🚀 MCP AI Agent 安裝腳本")
    print("=" * 50)
    
    # 檢查 Python 版本
    if not check_python_version():
        return
    
    # 創建虛擬環境
    if not create_venv():
        print("❌ 虛擬環境創建失敗")
        return
    
    # 創建必要目錄
    create_directories()
    
    # 安裝依賴
    if not install_requirements():
        print("❌ 依賴安裝失敗")
        return
    
    # 啟動虛擬環境
    activate_venv()
    
    print("\n" + "=" * 50)
    print("🎉 安裝完成！")
    print("\n📋 下一步操作:")
    print("1. 啟動虛擬環境:")
    if platform.system() == "Windows":
        print("   venv\\Scripts\\Activate.ps1")
    else:
        print("   source venv/bin/activate")
    
    print("2. 運行應用:")
    print("   python main.py")
    print("\n3. 開啟瀏覽器訪問:")
    print("   http://localhost:8000")
    print("=" * 50)

if __name__ == "__main__":
    main()
