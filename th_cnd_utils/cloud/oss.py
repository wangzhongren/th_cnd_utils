import os
from dotenv import load_dotenv
import oss2

# 加载环境变量
load_dotenv()

class OSSUtil:
    _instance = None
    _client = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OSSUtil, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.endpoint = os.getenv('OSS_ENDPOINT', '')
            self.bucket_name = os.getenv('OSS_BUCKET_NAME', '')
            self.access_key_id = os.getenv('ALIYUN_ACCESS_KEY_ID', '')
            self.access_key_secret = os.getenv('ALIYUN_ACCESS_KEY_SECRET', '')
            self.region = os.getenv('ALIYUN_REGION', 'cn-hangzhou')
    
    def connect(self):
        """建立 OSS 客户端连接"""
        try:
            if not self._client:
                auth = oss2.Auth(self.access_key_id, self.access_key_secret)
                self._client = oss2.Bucket(auth, self.endpoint, self.bucket_name)
                print("阿里云 OSS 连接成功")
            return self._client
        except Exception as e:
            print(f"阿里云 OSS 连接失败: {e}")
            raise e
    
    def put_object(self, object_name, data):
        """上传对象"""
        try:
            client = self.connect()
            result = client.put_object(object_name, data)
            print(f"对象 '{object_name}' 上传成功")
            return result
        except Exception as e:
            print(f"上传对象失败: {e}")
            raise e
    
    def get_object(self, object_name):
        """获取对象"""
        try:
            client = self.connect()
            result = client.get_object(object_name)
            return result
        except Exception as e:
            print(f"获取对象失败: {e}")
            raise e
    
    def delete_object(self, object_name):
        """删除对象"""
        try:
            client = self.connect()
            result = client.delete_object(object_name)
            print(f"对象 '{object_name}' 删除成功")
            return result
        except Exception as e:
            print(f"删除对象失败: {e}")
            raise e
    
    def list_objects(self, prefix='', max_keys=100):
        """列出对象"""
        try:
            client = self.connect()
            result = client.list_objects(prefix=prefix, max_keys=max_keys)
            return result.object_list
        except Exception as e:
            print(f"列出对象失败: {e}")
            raise e

# 创建单例实例
oss_util = OSSUtil()