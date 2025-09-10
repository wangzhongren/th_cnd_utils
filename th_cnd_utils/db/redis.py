import redis
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class RedisUtil:
    _instance = None
    _client = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RedisUtil, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.host = os.getenv('REDIS_HOST', 'localhost')
            self.port = int(os.getenv('REDIS_PORT', 6379))
            self.password = os.getenv('REDIS_PASSWORD', '')
            self.db = int(os.getenv('REDIS_DB', 0))
    
    def connect(self):
        """建立 Redis 连接"""
        try:
            if not self._client:
                self._client = redis.Redis(
                    host=self.host,
                    port=self.port,
                    password=self.password if self.password else None,
                    db=self.db,
                    decode_responses=True
                )
                # 测试连接
                self._client.ping()
                print("Redis 连接成功")
            return self._client
        except Exception as e:
            print(f"Redis 连接失败: {e}")
            raise e
    
    def get(self, key):
        """获取键值"""
        try:
            client = self.connect()
            return client.get(key)
        except Exception as e:
            print(f"获取键值失败: {e}")
            raise e
    
    def set(self, key, value, expire_seconds=None):
        """设置键值"""
        try:
            client = self.connect()
            if expire_seconds:
                return client.set(key, value, ex=expire_seconds)
            else:
                return client.set(key, value)
        except Exception as e:
            print(f"设置键值失败: {e}")
            raise e
    
    def delete(self, key):
        """删除键"""
        try:
            client = self.connect()
            return client.delete(key)
        except Exception as e:
            print(f"删除键失败: {e}")
            raise e
    
    def close(self):
        """关闭 Redis 连接"""
        if self._client:
            self._client.close()
            print("Redis 连接已关闭")

# 创建单例实例
redis_util = RedisUtil()