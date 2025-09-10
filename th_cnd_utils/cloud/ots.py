import os
from dotenv import load_dotenv
from tablestore import *

# 加载环境变量
load_dotenv()

class OTSUtil:
    _instance = None
    _client = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OTSUtil, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.endpoint = os.getenv('OTS_ENDPOINT', '')
            self.instance_name = os.getenv('OTS_INSTANCE_NAME', '')
            self.access_key_id = os.getenv('ALIYUN_ACCESS_KEY_ID', '')
            self.access_key_secret = os.getenv('ALIYUN_ACCESS_KEY_SECRET', '')
            self.region = os.getenv('ALIYUN_REGION', 'cn-hangzhou')
    
    def connect(self, instance_name=None):
        """建立 OTS 客户端连接"""
        try:
            # 如果指定了实例名称，则使用指定的实例名称
            target_instance_name = instance_name if instance_name else self.instance_name
            
            # 如果实例名称或客户端未初始化，或者实例名称发生变化，则重新创建客户端
            if not self._client or target_instance_name != self.instance_name:
                self._client = OTSClient(
                    self.endpoint,
                    self.access_key_id,
                    self.access_key_secret,
                    target_instance_name
                )
                print(f"阿里云表格存储连接成功，实例名称: {target_instance_name}")
            return self._client
        except Exception as e:
            print(f"阿里云表格存储连接失败: {e}")
            raise e
    
    def create_table(self, table_meta, reserved_throughput, instance_name=None):
        """创建表"""
        try:
            client = self.connect(instance_name)
            result = client.create_table(table_meta, reserved_throughput)
            print(f"表格 '{table_meta.table_name}' 创建成功")
            return result
        except Exception as e:
            print(f"创建表失败: {e}")
            raise e
    
    def put_row(self, table_name, primary_key, attribute_columns, instance_name=None):
        """插入一行数据"""
        try:
            client = self.connect(instance_name)
            row = Row(primary_key, attribute_columns)
            result = client.put_row(table_name, RowPutChange(table_name, row))
            print(f"数据插入成功")
            return result
        except Exception as e:
            print(f"插入数据失败: {e}")
            raise e
    
    def get_row(self, table_name, primary_key, columns_to_get=None, instance_name=None):
        """获取一行数据"""
        try:
            client = self.connect(instance_name)
            row = Row(primary_key)
            result = client.get_row(table_name, RowGetChange(table_name, row, columns_to_get))
            return result
        except Exception as e:
            print(f"获取数据失败: {e}")
            raise e
    
    def delete_row(self, table_name, primary_key, instance_name=None):
        """删除一行数据"""
        try:
            client = self.connect(instance_name)
            row = Row(primary_key)
            result = client.delete_row(table_name, RowDeleteChange(table_name, row))
            print(f"数据删除成功")
            return result
        except Exception as e:
            print(f"删除数据失败: {e}")
            raise e
    
    def update_row(self, table_name, primary_key, attribute_columns, instance_name=None):
        """更新一行数据"""
        try:
            client = self.connect(instance_name)
            row = Row(primary_key, attribute_columns)
            result = client.update_row(table_name, RowUpdateChange(table_name, row))
            print(f"数据更新成功")
            return result
        except Exception as e:
            print(f"更新数据失败: {e}")
            raise e
    
    def batch_write_row(self, request, instance_name=None):
        """批量写入数据"""
        try:
            client = self.connect(instance_name)
            result = client.batch_write_row(request)
            print(f"批量写入操作完成")
            return result
        except Exception as e:
            print(f"批量写入失败: {e}")
            raise e
    
    def batch_get_row(self, request, instance_name=None):
        """批量读取数据"""
        try:
            client = self.connect(instance_name)
            result = client.batch_get_row(request)
            print(f"批量读取操作完成")
            return result
        except Exception as e:
            print(f"批量读取失败: {e}")
            raise e
    
    def get_range(self, table_name, direction, inclusive_start_primary_key, 
                  exclusive_end_primary_key, columns_to_get=None, limit=None, 
                  instance_name=None):
        """范围查询"""
        try:
            client = self.connect(instance_name)
            request = GetRangeRequest(table_name, direction, 
                                    inclusive_start_primary_key, exclusive_end_primary_key,
                                    columns_to_get=columns_to_get, limit=limit)
            result = client.get_range(request)
            return result
        except Exception as e:
            print(f"范围查询失败: {e}")
            raise e
    
    def search(self, table_name, search_query, columns_to_get=None, 
               instance_name=None, index_name=None):
        """索引查询（搜索）"""
        try:
            client = self.connect(instance_name)
            request = SearchRequest(table_name, index_name, search_query, columns_to_get=columns_to_get)
            result = client.search(request)
            return result
        except Exception as e:
            print(f"索引查询失败: {e}")
            raise e
    
    def create_search_index(self, table_name, index_name, index_schema, instance_name=None):
        """创建搜索索引"""
        try:
            client = self.connect(instance_name)
            result = client.create_search_index(table_name, index_name, index_schema)
            print(f"搜索索引 '{index_name}' 创建成功")
            return result
        except Exception as e:
            print(f"创建搜索索引失败: {e}")
            raise e
    
    def delete_search_index(self, table_name, index_name, instance_name=None):
        """删除搜索索引"""
        try:
            client = self.connect(instance_name)
            result = client.delete_search_index(table_name, index_name)
            print(f"搜索索引 '{index_name}' 删除成功")
            return result
        except Exception as e:
            print(f"删除搜索索引失败: {e}")
            raise e
    
    def list_search_index(self, table_name, instance_name=None):
        """列出搜索索引"""
        try:
            client = self.connect(instance_name)
            result = client.list_search_index(table_name)
            return result
        except Exception as e:
            print(f"列出搜索索引失败: {e}")
            raise e

# 创建单例实例
ots_util = OTSUtil()