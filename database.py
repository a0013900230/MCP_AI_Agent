import sqlite3
import pandas as pd
from datetime import datetime
import os

class DatabaseManager:
    def __init__(self, db_path="returns.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """初始化資料庫和表格"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 建立退貨記錄表格
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS returns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id TEXT NOT NULL,
                product TEXT NOT NULL,
                store_name TEXT NOT NULL,
                return_date DATE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def insert_return(self, order_id, product, store_name, return_date):
        """插入新的退貨記錄"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO returns (order_id, product, store_name, return_date)
            VALUES (?, ?, ?, ?)
        ''', (order_id, product, store_name, return_date))
        
        conn.commit()
        conn.close()
        
        return cursor.lastrowid
    
    def get_all_returns(self):
        """獲取所有退貨記錄"""
        try:
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query("SELECT * FROM returns ORDER BY return_date DESC", conn)
            conn.close()
            
            # 檢查是否有資料
            if df is None or df.empty:
                print("資料庫中沒有退貨記錄")
                return pd.DataFrame()  # 返回空的 DataFrame
            
            print(f"成功獲取 {len(df)} 筆退貨記錄")
            return df
            
        except Exception as e:
            print(f"獲取退貨記錄時發生錯誤: {e}")
            import traceback
            traceback.print_exc()
            # 返回空的 DataFrame 而不是 None
            return pd.DataFrame()
    
    def get_returns_by_date_range(self, start_date, end_date):
        """根據日期範圍獲取退貨記錄"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query('''
            SELECT * FROM returns 
            WHERE return_date BETWEEN ? AND ?
            ORDER BY return_date DESC
        ''', conn, params=[start_date, end_date])
        conn.close()
        return df
    
    def get_returns_by_store(self, store_name):
        """根據商店名稱獲取退貨記錄"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query('''
            SELECT * FROM returns 
            WHERE store_name = ?
            ORDER BY return_date DESC
        ''', conn, params=[store_name])
        conn.close()
        return df
    
    def get_returns_by_product(self, product):
        """根據產品名稱獲取退貨記錄"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query('''
            SELECT * FROM returns 
            WHERE product = ?
            ORDER BY return_date DESC
        ''', conn, params=[product])
        conn.close()
        return df
    
    def import_csv_data(self, csv_file_path):
        """從 CSV 檔案導入資料"""
        try:
            # 檢查檔案是否存在
            if not os.path.exists(csv_file_path):
                raise FileNotFoundError(f"CSV 檔案不存在: {csv_file_path}")
            
            # 讀取 CSV 檔案
            df = pd.read_csv(csv_file_path, encoding='utf-8')
            required_columns = ['order_id', 'product', 'store_name', 'date']
            
            # 檢查必要欄位
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise ValueError(f"CSV 檔案缺少必要欄位: {missing_columns}")
            
            # 清理資料
            df = df.dropna(subset=required_columns)
            
            if len(df) == 0:
                raise ValueError("CSV 檔案中沒有有效資料")
            
            # 重新命名欄位以匹配資料庫結構
            df = df.rename(columns={'date': 'return_date'})
            
            # 插入資料到資料庫
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 逐行插入資料
            inserted_count = 0
            for _, row in df.iterrows():
                try:
                    cursor.execute('''
                        INSERT INTO returns (order_id, product, store_name, return_date)
                        VALUES (?, ?, ?, ?)
                    ''', (row['order_id'], row['product'], row['store_name'], row['return_date']))
                    inserted_count += 1
                except Exception as row_error:
                    print(f"插入行資料失敗: {row_error}, 資料: {row}")
                    continue
            
            conn.commit()
            conn.close()
            
            print(f"成功導入 {inserted_count} 筆記錄")
            return inserted_count
            
        except Exception as e:
            print(f"導入 CSV 資料失敗: {e}")
            import traceback
            traceback.print_exc()
            raise Exception(f"導入 CSV 資料失敗: {str(e)}")
    
    def get_statistics(self):
        """獲取統計資料"""
        try:
            print("🔍 開始獲取統計資料...")
            
            # 檢查資料庫檔案是否存在
            if not os.path.exists(self.db_path):
                print(f"❌ 資料庫檔案不存在: {self.db_path}")
                default_stats = {
                    'total_returns': 0,
                    'store_stats': [],
                    'product_stats': [],
                    'monthly_stats': []
                }
                print(f"返回預設統計資料: {default_stats}")
                return default_stats
            
            conn = sqlite3.connect(self.db_path)
            
            # 檢查表格是否存在
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='returns'")
            if not cursor.fetchone():
                print("❌ returns 表格不存在")
                conn.close()
                default_stats = {
                    'total_returns': 0,
                    'store_stats': [],
                    'product_stats': [],
                    'monthly_stats': []
                }
                print(f"返回預設統計資料: {default_stats}")
                return default_stats
            
            print("✅ returns 表格存在，開始查詢統計資料...")
            
            # 總退貨數量
            try:
                total_result = pd.read_sql_query("SELECT COUNT(*) as total FROM returns", conn)
                total_returns = int(total_result.iloc[0]['total']) if not total_result.empty else 0
                print(f"✅ 總退貨數量: {total_returns}")
            except Exception as e:
                print(f"❌ 獲取總退貨數量失敗: {e}")
                total_returns = 0
            
            # 按商店統計
            try:
                store_stats = pd.read_sql_query('''
                    SELECT store_name, COUNT(*) as count 
                    FROM returns 
                    GROUP BY store_name 
                    ORDER BY count DESC
                ''', conn)
                if not store_stats.empty:
                    # 轉換 numpy.int64 為 Python int
                    store_stats_list = []
                    for _, row in store_stats.iterrows():
                        store_stats_list.append({
                            'store_name': str(row['store_name']),
                            'count': int(row['count'])
                        })
                else:
                    store_stats_list = []
                print(f"✅ 商店統計: {len(store_stats_list)} 項")
            except Exception as e:
                print(f"❌ 獲取商店統計失敗: {e}")
                store_stats_list = []
            
            # 按產品統計
            try:
                product_stats = pd.read_sql_query('''
                    SELECT product, COUNT(*) as count 
                    FROM returns 
                    GROUP BY product 
                    ORDER BY count DESC
                ''', conn)
                if not product_stats.empty:
                    # 轉換 numpy.int64 為 Python int
                    product_stats_list = []
                    for _, row in product_stats.iterrows():
                        product_stats_list.append({
                            'product': str(row['product']),
                            'count': int(row['count'])
                        })
                else:
                    product_stats_list = []
                print(f"✅ 產品統計: {len(product_stats_list)} 項")
            except Exception as e:
                print(f"❌ 獲取產品統計失敗: {e}")
                product_stats_list = []
            
            # 按月份統計
            try:
                monthly_stats = pd.read_sql_query('''
                    SELECT strftime('%Y-%m', return_date) as month, COUNT(*) as count 
                    FROM returns 
                    GROUP BY month 
                    ORDER BY month DESC
                ''', conn)
                if not monthly_stats.empty:
                    # 轉換 numpy.int64 為 Python int
                    monthly_stats_list = []
                    for _, row in monthly_stats.iterrows():
                        monthly_stats_list.append({
                            'month': str(row['month']),
                            'count': int(row['count'])
                        })
                else:
                    monthly_stats_list = []
                print(f"✅ 月份統計: {len(monthly_stats_list)} 項")
            except Exception as e:
                print(f"❌ 獲取月份統計失敗: {e}")
                monthly_stats_list = []
            
            conn.close()
            
            final_stats = {
                'total_returns': total_returns,
                'store_stats': store_stats_list,
                'product_stats': product_stats_list,
                'monthly_stats': monthly_stats_list
            }
            
            print(f"🎉 統計資料獲取成功: {final_stats}")
            return final_stats
            
        except Exception as e:
            print(f"❌ 獲取統計資料時發生錯誤: {e}")
            import traceback
            traceback.print_exc()
            # 返回預設值
            default_stats = {
                'total_returns': 0,
                'store_stats': [],
                'product_stats': [],
                'monthly_stats': []
            }
            print(f"🔄 返回預設統計資料: {default_stats}")
            return default_stats
