import pandas as pd
import re
from datetime import datetime
from database import DatabaseManager
import os

class RetrievalAgent:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.csv_data = None
    
    def process_natural_language(self, prompt):
        """處理自然語言提示詞，識別意圖並執行相應操作"""
        prompt_lower = prompt.lower()
        
        # 識別新增退貨記錄的意圖
        if any(word in prompt_lower for word in ['新增', '插入', '加入', 'add', 'insert']):
            return self._extract_and_insert_return(prompt)
        
        # 識別查詢退貨記錄的意圖
        elif any(word in prompt_lower for word in ['查詢', '顯示', '列出', '查詢', 'query', 'show', 'list']):
            return self._query_returns(prompt)
        
        # 識別導入 CSV 的意圖
        elif any(word in prompt_lower for word in ['導入', '上傳', 'import', 'upload']):
            return self._handle_csv_import(prompt)
        
        # 識別統計分析的意圖
        elif any(word in prompt_lower for word in ['統計', '分析', '統計', 'statistics', 'analysis']):
            return self._get_statistics()
        
        else:
            return {
                'status': 'error',
                'message': '無法識別您的請求。請使用以下格式之一：\n1. 新增退貨記錄：訂單ID XXX，產品名稱 XXX，商店名稱 XXX，日期 XXX\n2. 查詢退貨記錄\n3. 導入 CSV 檔案\n4. 獲取統計資料'
            }
    
    def _extract_and_insert_return(self, prompt):
        """從自然語言中提取退貨資訊並插入資料庫"""
        try:
            # 使用正則表達式提取資訊
            order_id_match = re.search(r'訂單ID\s*(\w+)', prompt)
            product_match = re.search(r'產品名稱\s*([^，,]+)', prompt)
            store_match = re.search(r'商店名稱\s*([^，,]+)', prompt)
            date_match = re.search(r'日期\s*(\d{4}-\d{2}-\d{2})', prompt)
            
            if not all([order_id_match, product_match, store_match, date_match]):
                return {
                    'status': 'error',
                    'message': '請提供完整的退貨資訊，包括：訂單ID、產品名稱、商店名稱、日期（格式：YYYY-MM-DD）'
                }
            
            order_id = order_id_match.group(1).strip()
            product = product_match.group(1).strip()
            store_name = store_match.group(1).strip()
            return_date = date_match.group(1).strip()
            
            # 驗證日期格式
            try:
                datetime.strptime(return_date, '%Y-%m-%d')
            except ValueError:
                return {
                    'status': 'error',
                    'message': '日期格式錯誤，請使用 YYYY-MM-DD 格式'
                }
            
            # 插入資料庫
            record_id = self.db_manager.insert_return(order_id, product, store_name, return_date)
            
            # 獲取當前所有退貨記錄
            all_returns = self.db_manager.get_all_returns()
            
            return {
                'status': 'success',
                'message': f'成功新增退貨記錄，記錄ID: {record_id}',
                'data': {
                    'new_record': {
                        'order_id': order_id,
                        'product': product,
                        'store_name': store_name,
                        'return_date': return_date
                    },
                    'all_returns': all_returns.to_dict('records')
                }
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'處理新增退貨記錄時發生錯誤: {str(e)}'
            }
    
    def _query_returns(self, prompt):
        """查詢退貨記錄"""
        try:
            prompt_lower = prompt.lower()
            
            # 根據查詢條件獲取資料
            if '全部' in prompt_lower or '所有' in prompt_lower:
                returns = self.db_manager.get_all_returns()
                return {
                    'status': 'success',
                    'message': f'共找到 {len(returns)} 筆退貨記錄',
                    'data': returns.to_dict('records')
                }
            
            # 按日期範圍查詢
            elif '日期' in prompt_lower or '期間' in prompt_lower:
                # 這裡可以進一步解析日期範圍
                returns = self.db_manager.get_all_returns()
                return {
                    'status': 'success',
                    'message': f'共找到 {len(returns)} 筆退貨記錄',
                    'data': returns.to_dict('records')
                }
            
            # 按商店查詢
            elif '商店' in prompt_lower:
                store_match = re.search(r'商店\s*([^，,]+)', prompt)
                if store_match:
                    store_name = store_match.group(1).strip()
                    returns = self.db_manager.get_returns_by_store(store_name)
                    return {
                        'status': 'success',
                        'message': f'商店 "{store_name}" 共有 {len(returns)} 筆退貨記錄',
                        'data': returns.to_dict('records')
                    }
            
            # 按產品查詢
            elif '產品' in prompt_lower:
                product_match = re.search(r'產品\s*([^，,]+)', prompt)
                if product_match:
                    product = product_match.group(1).strip()
                    returns = self.db_manager.get_returns_by_product(product)
                    return {
                        'status': 'success',
                        'message': f'產品 "{product}" 共有 {len(returns)} 筆退貨記錄',
                        'data': returns.to_dict('records')
                    }
            
            # 預設返回所有記錄
            returns = self.db_manager.get_all_returns()
            return {
                'status': 'success',
                'message': f'共找到 {len(returns)} 筆退貨記錄',
                'data': returns.to_dict('records')
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'查詢退貨記錄時發生錯誤: {str(e)}'
            }
    
    def _handle_csv_import(self, prompt):
        """處理 CSV 檔案導入"""
        try:
            # 檢查是否有上傳的 CSV 檔案
            # 這裡假設 CSV 檔案已經在專案目錄中
            csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
            
            if not csv_files:
                return {
                    'status': 'error',
                    'message': '未找到 CSV 檔案。請將 CSV 檔案放在專案目錄中，或使用檔案上傳功能。'
                }
            
            # 使用第一個找到的 CSV 檔案
            csv_file = csv_files[0]
            imported_count = self.db_manager.import_csv_data(csv_file)
            
            return {
                'status': 'success',
                'message': f'成功從 {csv_file} 導入 {imported_count} 筆退貨記錄',
                'data': {
                    'file': csv_file,
                    'imported_count': imported_count
                }
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'導入 CSV 檔案時發生錯誤: {str(e)}'
            }
    
    def _get_statistics(self):
        """獲取統計資料"""
        try:
            stats = self.db_manager.get_statistics()
            return {
                'status': 'success',
                'message': '統計資料獲取成功',
                'data': stats
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'獲取統計資料時發生錯誤: {str(e)}'
            }
    
    def get_current_returns(self):
        """獲取當前所有退貨記錄"""
        try:
            returns = self.db_manager.get_all_returns()
            return {
                'status': 'success',
                'data': returns.to_dict('records')
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'獲取退貨記錄時發生錯誤: {str(e)}'
            }

