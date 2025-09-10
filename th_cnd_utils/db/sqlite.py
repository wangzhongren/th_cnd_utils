import sqlite3
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class SQLiteUtil:
    _instance = None
    _connection = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SQLiteUtil, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.db_path = os.getenv('SQLITE_PATH', './database.sqlite')
    
    def connect(self):
        """建立 SQLite 数据库连接"""
        try:
            if not self._connection:
                self._connection = sqlite3.connect(self.db_path)
                self._connection.row_factory = sqlite3.Row  # 使结果可以通过列名访问
                print("SQLite 连接成功")
            return self._connection
        except Exception as e:
            print(f"SQLite 连接失败: {e}")
            raise e
    
    def execute_query(self, sql, params=None):
        """执行查询语句"""
        try:
            connection = self.connect()
            cursor = connection.cursor()
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            result = cursor.fetchall()
            return [dict(row) for row in result]
        except Exception as e:
            print(f"查询执行失败: {e}")
            raise e
        finally:
            if cursor:
                cursor.close()
    
    def execute_update(self, sql, params=None):
        """执行更新语句（INSERT, UPDATE, DELETE）"""
        try:
            connection = self.connect()
            cursor = connection.cursor()
            if params:
                result = cursor.execute(sql, params)
            else:
                result = cursor.execute(sql)
            connection.commit()
            return result.rowcount
        except Exception as e:
            print(f"更新执行失败: {e}")
            connection.rollback()
            raise e
        finally:
            if cursor:
                cursor.close()
    
    def close(self):
        """关闭数据库连接"""
        if self._connection:
            self._connection.close()
            print("SQLite 连接已关闭")

# 创建单例实例
sqlite_util = SQLiteUtil()