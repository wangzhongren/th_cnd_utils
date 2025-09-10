import pymysql
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class MySQLUtil:
    _instance = None
    _connection = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MySQLUtil, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.host = os.getenv('MYSQL_HOST', 'localhost')
            self.port = int(os.getenv('MYSQL_PORT', 3306))
            self.user = os.getenv('MYSQL_USER', 'root')
            self.password = os.getenv('MYSQL_PASSWORD', '')
            self.database = os.getenv('MYSQL_DATABASE', 'test')
    
    def connect(self):
        """建立数据库连接"""
        try:
            if not self._connection or not self._connection.open:
                self._connection = pymysql.connect(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor
                )
                print("MySQL 连接成功")
            return self._connection
        except Exception as e:
            print(f"MySQL 连接失败: {e}")
            raise e
    
    def execute_query(self, sql, params=None):
        """执行查询语句"""
        try:
            connection = self.connect()
            with connection.cursor() as cursor:
                cursor.execute(sql, params)
                result = cursor.fetchall()
                return result
        except Exception as e:
            print(f"查询执行失败: {e}")
            raise e
    
    def execute_update(self, sql, params=None):
        """执行更新语句（INSERT, UPDATE, DELETE）"""
        try:
            connection = self.connect()
            with connection.cursor() as cursor:
                result = cursor.execute(sql, params)
                connection.commit()
                return result
        except Exception as e:
            print(f"更新执行失败: {e}")
            connection.rollback()
            raise e
    
    def close(self):
        """关闭数据库连接"""
        if self._connection and self._connection.open:
            self._connection.close()
            print("MySQL 连接已关闭")

# 创建单例实例
mysql_util = MySQLUtil()