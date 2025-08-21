from retrieval_agent import RetrievalAgent
from report_agent import ReportAgent
from database import DatabaseManager
import json

class MCPCoordinator:
    def __init__(self):
        """初始化 MCP Coordinator 和兩個 agent"""
        self.retrieval_agent = RetrievalAgent()
        self.report_agent = ReportAgent()
        self.db_manager = DatabaseManager()
        
        # 定義可用的操作類型
        self.available_operations = {
            'retrieval': [
                'add_return',      # 新增退貨記錄
                'query_returns',   # 查詢退貨記錄
                'import_csv',      # 導入 CSV 資料
                'get_statistics'   # 獲取統計資料
            ],
            'report': [
                'generate_report', # 生成報告
                'generate_simple_report'  # 生成簡單報告
            ]
        }
    
    def process_request(self, user_input, operation_type=None):
        """處理使用者請求，協調兩個 agent"""
        try:
            # 如果沒有指定操作類型，嘗試自動識別
            if not operation_type:
                operation_type = self._identify_operation_type(user_input)
            
            # 根據操作類型分發給相應的 agent
            if operation_type in self.available_operations['retrieval']:
                return self._handle_retrieval_operation(user_input, operation_type)
            elif operation_type in self.available_operations['report']:
                return self._handle_report_operation(user_input, operation_type)
            else:
                return {
                    'status': 'error',
                    'message': f'不支援的操作類型: {operation_type}',
                    'available_operations': self.available_operations
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'message': f'處理請求時發生錯誤: {str(e)}'
            }
    
    def _identify_operation_type(self, user_input):
        """自動識別操作類型"""
        input_lower = user_input.lower()
        
        # 識別 Retrieval Agent 操作
        if any(word in input_lower for word in ['新增', '插入', '加入', 'add', 'insert']):
            return 'add_return'
        elif any(word in input_lower for word in ['查詢', '顯示', '列出', 'query', 'show', 'list']):
            return 'query_returns'
        elif any(word in input_lower for word in ['導入', '上傳', 'import', 'upload']):
            return 'import_csv'
        elif any(word in input_lower for word in ['統計', '分析', 'statistics', 'analysis']):
            return 'get_statistics'
        
        # 識別 Report Agent 操作
        elif any(word in input_lower for word in ['報告', '報表', 'report', 'excel']):
            return 'generate_report'
        
        # 預設為查詢操作
        return 'query_returns'
    
    def _handle_retrieval_operation(self, user_input, operation_type):
        """處理 Retrieval Agent 相關操作"""
        if operation_type == 'add_return':
            return self.retrieval_agent.process_natural_language(user_input)
        elif operation_type == 'query_returns':
            return self.retrieval_agent.process_natural_language(user_input)
        elif operation_type == 'import_csv':
            return self.retrieval_agent.process_natural_language(user_input)
        elif operation_type == 'get_statistics':
            return self.retrieval_agent.process_natural_language(user_input)
        else:
            return {
                'status': 'error',
                'message': f'不支援的 Retrieval 操作: {operation_type}'
            }
    
    def _handle_report_operation(self, user_input, operation_type):
        """處理 Report Agent 相關操作"""
        try:
            if operation_type == 'generate_report':
                # 獲取退貨資料和統計資料
                returns_result = self.retrieval_agent.get_current_returns()
                statistics_result = self.retrieval_agent._get_statistics()
                
                if returns_result['status'] == 'success' and statistics_result['status'] == 'success':
                    returns_data = returns_result['data']
                    statistics_data = statistics_result['data']
                    
                    # 生成完整報告
                    report_result = self.report_agent.generate_excel_report(
                        returns_data, statistics_data
                    )
                    
                    return {
                        'status': 'success',
                        'message': '報告生成完成',
                        'data': {
                            'report': report_result,
                            'returns_count': len(returns_data),
                            'statistics': statistics_data
                        }
                    }
                else:
                    return {
                        'status': 'error',
                        'message': '無法獲取資料來生成報告',
                        'details': {
                            'returns_status': returns_result.get('status'),
                            'statistics_status': statistics_result.get('status')
                        }
                    }
            
            elif operation_type == 'generate_simple_report':
                # 獲取退貨資料
                returns_result = self.retrieval_agent.get_current_returns()
                
                if returns_result['status'] == 'success':
                    returns_data = returns_result['data']
                    
                    # 生成簡單報告
                    report_result = self.report_agent.generate_simple_report(returns_data)
                    
                    return {
                        'status': 'success',
                        'message': '簡單報告生成完成',
                        'data': {
                            'report': report_result,
                            'returns_count': len(returns_data)
                        }
                    }
                else:
                    return {
                        'status': 'error',
                        'message': '無法獲取退貨資料來生成報告'
                    }
            
            else:
                return {
                    'status': 'error',
                    'message': f'不支援的 Report 操作: {operation_type}'
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'message': f'處理報告操作時發生錯誤: {str(e)}'
            }
    
    def get_system_status(self):
        """獲取系統狀態"""
        try:
            print("檢查系統狀態...")
            
            # 檢查資料庫狀態
            try:
                returns_data = self.db_manager.get_all_returns()
                returns_count = len(returns_data) if returns_data is not None else 0
                db_status = 'connected'
                print(f"資料庫狀態: {db_status}, 退貨記錄數: {returns_count}")
            except Exception as db_error:
                print(f"資料庫檢查失敗: {db_error}")
                returns_count = 0
                db_status = 'error'
            
            # 檢查報告目錄
            import os
            reports_dir = "reports"
            try:
                if os.path.exists(reports_dir):
                    reports_count = len([f for f in os.listdir(reports_dir) if f.endswith('.xlsx')])
                    print(f"報告目錄: {reports_dir}, 報告數量: {reports_count}")
                else:
                    reports_count = 0
                    print(f"報告目錄不存在: {reports_dir}")
            except Exception as dir_error:
                print(f"報告目錄檢查失敗: {dir_error}")
                reports_count = 0
            
            # 檢查 agent 狀態
            agents_status = {
                'retrieval_agent': 'ready',
                'report_agent': 'ready'
            }
            
            status_data = {
                'database': {
                    'status': db_status,
                    'returns_count': returns_count
                },
                'reports': {
                    'directory': reports_dir,
                    'reports_count': reports_count
                },
                'agents': agents_status
            }
            
            print(f"系統狀態檢查完成: {status_data}")
            
            return {
                'status': 'success',
                'data': status_data
            }
            
        except Exception as e:
            print(f"獲取系統狀態時發生錯誤: {e}")
            import traceback
            traceback.print_exc()
            return {
                'status': 'error',
                'message': f'獲取系統狀態時發生錯誤: {str(e)}'
            }
    
    def get_help(self):
        """獲取使用說明"""
        return {
            'status': 'success',
            'data': {
                'description': 'MCP 風格的退貨分析系統',
                'available_operations': self.available_operations,
                'examples': {
                    'add_return': '新增退貨記錄：訂單ID 12345，產品名稱 iPhone，商店名稱 台北店，日期 2024-01-15',
                    'query_returns': '查詢所有退貨記錄',
                    'import_csv': '導入 CSV 檔案',
                    'get_statistics': '獲取統計資料',
                    'generate_report': '生成完整 Excel 報告',
                    'generate_simple_report': '生成簡單報告'
                },
                'usage_tips': [
                    '使用自然語言描述您的需求',
                    '系統會自動識別操作類型',
                    '可以指定具體的操作類型來提高準確性',
                    '報告會自動儲存在 reports/ 目錄中'
                ]
            }
        }
    
    def execute_workflow(self, workflow_steps):
        """執行工作流程（多步驟操作）"""
        try:
            results = []
            
            for step in workflow_steps:
                step_type = step.get('type')
                step_input = step.get('input')
                step_operation = step.get('operation')
                
                if step_type == 'retrieval':
                    result = self._handle_retrieval_operation(step_input, step_operation)
                elif step_type == 'report':
                    result = self._handle_report_operation(step_input, step_operation)
                else:
                    result = {
                        'status': 'error',
                        'message': f'不支援的步驟類型: {step_type}'
                    }
                
                results.append({
                    'step': step,
                    'result': result
                })
                
                # 如果某個步驟失敗，停止工作流程
                if result['status'] == 'error':
                    break
            
            return {
                'status': 'success',
                'message': '工作流程執行完成',
                'data': {
                    'total_steps': len(workflow_steps),
                    'completed_steps': len(results),
                    'results': results
                }
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'執行工作流程時發生錯誤: {str(e)}'
            }
