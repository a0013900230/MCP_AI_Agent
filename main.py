from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
import uvicorn
import os
import json
from datetime import datetime

from mcp_coordinator import MCPCoordinator
from database import DatabaseManager

# 建立 FastAPI 應用程式
app = FastAPI(
    title="退貨與保固分析系統",
    description="基於 MCP 風格的 Python 應用程式，包含兩個協作的 agent",
    version="1.0.0"
)

# 初始化 MCP Coordinator
coordinator = MCPCoordinator()
db_manager = DatabaseManager()

# 建立必要的目錄
os.makedirs("reports", exist_ok=True)
os.makedirs("uploads", exist_ok=True)
os.makedirs("static", exist_ok=True)
os.makedirs("static/css", exist_ok=True)
os.makedirs("static/js", exist_ok=True)
os.makedirs("static/images", exist_ok=True)

# 掛載靜態檔案
app.mount("/static", StaticFiles(directory="static"), name="static")

# 設定模板
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """首頁"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/status")
async def get_status():
    """獲取系統狀態"""
    try:
        print("獲取系統狀態...")
        status = coordinator.get_system_status()
        print(f"系統狀態: {status}")
        return status
    except Exception as e:
        print(f"獲取系統狀態失敗: {e}")
        import traceback
        traceback.print_exc()
        return {
            "status": "error",
            "message": "系統狀態獲取失敗",
            "details": str(e)
        }

@app.get("/api/help")
async def get_help():
    """獲取使用說明"""
    return coordinator.get_help()

@app.post("/api/process")
async def process_request(request: Request):
    """處理自然語言請求"""
    try:
        body = await request.json()
        user_input = body.get("input", "")
        operation_type = body.get("operation_type")
        
        if not user_input:
            raise HTTPException(status_code=400, detail="請提供輸入內容")
        
        result = coordinator.process_request(user_input, operation_type)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/add_return")
async def add_return(
    order_id: str = Form(...),
    product: str = Form(...),
    store_name: str = Form(...),
    return_date: str = Form(...)
):
    """新增退貨記錄"""
    try:
        # 驗證日期格式
        datetime.strptime(return_date, '%Y-%m-%d')
        
        # 插入資料庫
        record_id = db_manager.insert_return(order_id, product, store_name, return_date)
        
        # 獲取當前所有退貨記錄
        all_returns = db_manager.get_all_returns()
        
        return {
            "status": "success",
            "message": f"成功新增退貨記錄，記錄ID: {record_id}",
            "data": {
                "record_id": record_id,
                "all_returns": all_returns.to_dict('records')
            }
        }
        
    except ValueError:
        raise HTTPException(status_code=400, detail="日期格式錯誤，請使用 YYYY-MM-DD 格式")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/returns")
async def get_returns():
    """獲取所有退貨記錄"""
    try:
        returns = db_manager.get_all_returns()
        return {
            "status": "success",
            "data": returns.to_dict('records')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/statistics")
async def get_statistics():
    """獲取統計資料"""
    try:
        print("🔍 開始獲取統計資料...")
        
        # 檢查資料庫管理器是否正常
        if not db_manager:
            print("❌ 資料庫管理器未初始化")
            return {
                "status": "error",
                "message": "資料庫管理器未初始化",
                "details": "系統初始化失敗"
            }
        
        # 獲取統計資料
        print("📊 調用資料庫統計方法...")
        try:
            stats = db_manager.get_statistics()
            print(f"📈 資料庫返回的統計資料: {stats}")
        except Exception as db_error:
            print(f"❌ 資料庫統計方法調用失敗: {db_error}")
            import traceback
            traceback.print_exc()
            return {
                "status": "error",
                "message": "資料庫統計方法調用失敗",
                "details": str(db_error)
            }
        
        # 檢查統計資料是否有效
        if stats is None:
            print("❌ 統計資料為 None")
            return {
                "status": "error",
                "message": "統計資料為空",
                "details": "資料庫返回空值"
            }
        
        if isinstance(stats, dict):
            print("✅ 統計資料是字典格式")
            
            # 檢查必要欄位
            required_fields = ['total_returns', 'store_stats', 'product_stats', 'monthly_stats']
            missing_fields = [field for field in required_fields if field not in stats]
            
            if not missing_fields:
                print("✅ 統計資料包含所有必要欄位")
                print(f"總退貨數: {stats.get('total_returns', 0)}")
                print(f"商店統計: {len(stats.get('store_stats', []))} 項")
                print(f"產品統計: {len(stats.get('product_stats', []))} 項")
                print(f"月份統計: {len(stats.get('monthly_stats', []))} 項")
                
                result = {
                    "status": "success",
                    "data": stats
                }
                print(f"🎉 返回成功結果: {result}")
                return result
            else:
                print(f"❌ 統計資料缺少欄位: {missing_fields}")
                return {
                    "status": "error",
                    "message": "統計資料格式不完整",
                    "details": f"缺少欄位: {missing_fields}"
                }
        else:
            print(f"❌ 統計資料不是字典格式: {type(stats)}")
            return {
                "status": "error",
                "message": "統計資料格式錯誤",
                "details": f"期望字典格式，實際為 {type(stats)}"
            }
            
    except Exception as e:
        print(f"❌ 獲取統計資料時發生錯誤: {e}")
        import traceback
        traceback.print_exc()
        return {
            "status": "error",
            "message": "統計資料獲取失敗",
            "details": str(e)
        }

@app.post("/api/upload_csv")
async def upload_csv(file: UploadFile = File(...)):
    """上傳 CSV 檔案"""
    try:
        # 檢查檔案類型
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="只支援 CSV 檔案")
        
        # 儲存檔案
        file_path = os.path.join("uploads", file.filename)
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # 導入資料
        imported_count = db_manager.import_csv_data(file_path)
        
        return {
            "status": "success",
            "message": f"成功導入 {imported_count} 筆退貨記錄",
            "data": {
                "filename": file.filename,
                "imported_count": imported_count
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate_report")
async def generate_report(report_type: str = Form("comprehensive")):
    """生成報告"""
    try:
        print(f"開始生成報告，類型: {report_type}")
        
        # 獲取退貨資料和統計資料
        returns_data = db_manager.get_all_returns()
        statistics_data = db_manager.get_statistics()
        
        print(f"退貨資料類型: {type(returns_data)}")
        print(f"退貨資料長度: {len(returns_data) if returns_data is not None else 'None'}")
        print(f"統計資料: {statistics_data}")
        
        # 將 DataFrame 轉換為字典列表
        if returns_data is not None and not returns_data.empty:
            returns_list = returns_data.to_dict('records')
            print(f"轉換後的資料長度: {len(returns_list)}")
        else:
            returns_list = []
            print("沒有退貨資料")
        
        if report_type == "simple":
            print("生成簡單報告...")
            result = coordinator.report_agent.generate_simple_report(returns_list)
        else:
            print("生成完整報告...")
            result = coordinator.report_agent.generate_excel_report(returns_list, statistics_data)
        
        print(f"報告生成結果: {result}")
        
        if result['status'] == 'success':
            return {
                "status": "success",
                "message": result['message'],
                "data": result['data']
            }
        else:
            print(f"報告生成失敗: {result['message']}")
            raise HTTPException(status_code=500, detail=result['message'])
            
    except Exception as e:
        print(f"生成報告時發生錯誤: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/download_report/{filename}")
async def download_report(filename: str):
    """下載報告檔案"""
    try:
        file_path = os.path.join("reports", filename)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="報告檔案不存在")
        
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/reports")
async def list_reports():
    """列出所有報告檔案"""
    try:
        reports_dir = "reports"
        if not os.path.exists(reports_dir):
            return {"status": "success", "data": []}
        
        reports = []
        for filename in os.listdir(reports_dir):
            if filename.endswith('.xlsx'):
                file_path = os.path.join(reports_dir, filename)
                file_stat = os.stat(file_path)
                reports.append({
                    "filename": filename,
                    "size": file_stat.st_size,
                    "created_at": datetime.fromtimestamp(file_stat.st_ctime).isoformat()
                })
        
        # 按建立時間排序
        reports.sort(key=lambda x: x['created_at'], reverse=True)
        
        return {
            "status": "success",
            "data": reports
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/workflow")
async def execute_workflow(request: Request):
    """執行工作流程"""
    try:
        body = await request.json()
        workflow_steps = body.get("steps", [])
        
        if not workflow_steps:
            raise HTTPException(status_code=400, detail="請提供工作流程步驟")
        
        result = coordinator.execute_workflow(workflow_steps)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 建立範例 CSV 資料
@app.post("/api/create_sample_data")
async def create_sample_data():
    """建立範例資料"""
    try:
        import pandas as pd
        
        # 建立範例退貨資料
        sample_data = {
            'order_id': ['ORD001', 'ORD002', 'ORD003', 'ORD004', 'ORD005'],
            'product': ['iPhone 15', 'Samsung Galaxy', 'MacBook Pro', 'iPad Air', 'Apple Watch'],
            'store_name': ['台北店', '台中店', '高雄店', '台北店', '台中店'],
            'date': ['2024-01-15', '2024-01-16', '2024-01-17', '2024-01-18', '2024-01-19']
        }
        
        df = pd.DataFrame(sample_data)
        
        # 儲存為 CSV
        csv_path = "sample_returns.csv"
        df.to_csv(csv_path, index=False, encoding='utf-8')
        
        # 導入到資料庫
        imported_count = db_manager.import_csv_data(csv_path)
        
        return {
            "status": "success",
            "message": f"成功建立範例資料，導入 {imported_count} 筆記錄",
            "data": {
                "csv_file": csv_path,
                "imported_count": imported_count
            }
        }
        
    except ImportError as e:
        print(f"Pandas 導入失敗: {e}")
        raise HTTPException(status_code=500, detail="Pandas 套件未安裝或無法導入")
    except Exception as e:
        print(f"建立範例資料失敗: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"建立範例資料失敗: {str(e)}")

def find_available_port(start_port=8000, max_attempts=100):
    """尋找可用的端口"""
    import socket
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    return None

if __name__ == "__main__":
    print("啟動退貨與保固分析系統...")
    
    # 尋找可用端口
    port = find_available_port()
    if port is None:
        print("❌ 無法找到可用端口")
        sys.exit(1)
    
    print(f"✅ 使用端口: {port}")
    print(f"🌐 訪問 http://localhost:{port} 開始使用")
    
    try:
        uvicorn.run(app, host="0.0.0.0", port=port)
    except KeyboardInterrupt:
        print("\n👋 系統已停止")
    except Exception as e:
        print(f"❌ 啟動失敗: {e}")
        print("💡 請檢查端口是否被佔用")
