# AI-DO Utils 工具库调用指南

## 概述

本指南介绍了如何使用 AI-DO Utils 工具库操作各种数据存储和消息队列系统。所有工具类均采用单例模式设计，提供统一的接口进行数据操作。

## 工具类导入

所有工具类均可通过以下方式导入：

```python
# 导入所有工具类
from utils import mysql_util, redis_util, rabbitmq_util, sqlite_util, ots_util, oss_util, ServiceClient, flask_util, web_app_client

# 或者单独导入某个工具类
from utils.db.mysql import mysql_util
from utils.db.redis import redis_util
from utils.db.rabbitmq import rabbitmq_util
from utils.db.sqlite import sqlite_util
from utils.cloud.ots import ots_util
from utils.cloud.oss import oss_util
from utils.service_client import ServiceClient
from utils.flask_util import FlaskUtil, flask_util
from utils.web_app_client import WebAppClient, web_app_client
```

## HTTP请求使用指南

### 普通HTTP请求
对于普通的HTTP请求（如调用第三方API、微服务接口等），建议直接使用 `requests` 库：

```python
import requests
import json

# GET请求示例
response = requests.get('https://api.example.com/users')
if response.status_code == 200:
    users = response.json()
    print(users)

# POST请求示例
data = {'name': '张三', 'email': 'zhangsan@example.com'}
response = requests.post('https://api.example.com/users', json=data)
if response.status_code == 201:
    result = response.json()
    print(f"用户创建成功: {result}")

# 带认证的请求示例
headers = {'Authorization': 'Bearer your-token'}
response = requests.get('https://api.example.com/protected', headers=headers)
```

### 李龙加密接口请求
对于需要特定加密签名的李龙平台接口或BI平台接口，必须使用 `ServiceClient` 工具类：

```python
from utils import ServiceClient

# 初始化服务客户端（用于李龙平台或BI平台）
client = ServiceClient(
    appid="your_app_id",
    appkey="your_app_key",
    url_prefix="https://api.li-long.com"
)

# 准备请求数据
request_data = {
    "user_id": 12345,
    "action": "get_user_info",
    "params": {
        "include_profile": True,
        "include_preferences": False
    }
}

# 调用李龙平台接口（自动处理加密签名）
response = client.exec("/user/service", request_data)

# 处理响应
if response.get("code") == 0:
    print("请求成功:", response.get("content"))
else:
    print("请求失败:", response.get("content"))
```

## WebAppClient 工具类使用指南

WebAppClient工具类用于调用web_app接口生成和下载代码。

### 配置

WebAppClient 支持从环境变量读取配置。在 `.env` 文件中添加以下配置：

```env
# WebApp 配置
WEB_APP_BASE_URL=http://127.0.0.1:5000
```

### 初始化
```python
from utils import web_app_client

# 使用环境变量配置的URL
client = web_app_client

# 或者创建新的实例并指定URL
from utils import WebAppClient
client = WebAppClient("http://your-web-app-url:5000")
```

### 核心方法
- `generate_code(task_description)` - 调用web_app接口生成代码
- `download_code(task_description, save_path)` - 生成代码并保存到文件
- `set_base_url(base_url)` - 设置基础URL
- `get_base_url()` - 获取当前基础URL
- `close()` - 关闭会话

### 使用示例

#### 1. 生成代码
```python
from utils import web_app_client

# 定义任务描述
task_description = """1. 从OSS的raw_data/目录下读取最新的CSV文件
2. 将文件内容解析后批量插入到MySQL的raw_records表中
3. 对处理完成的文件，在OSS中移动到processed_data/目录
4. 记录处理日志到SQLite的process_logs表

请确保包含适当的错误处理和资源清理。"""

# 生成代码
generated_code = web_app_client.generate_code(task_description)

if generated_code:
    print("生成的代码:")
    print(generated_code)
else:
    print("代码生成失败")
```

#### 2. 生成并保存代码
```python
from utils import web_app_client

# 定义任务描述
task_description = """1. 从OSS的raw_data/目录下读取最新的CSV文件
2. 将文件内容解析后批量插入到MySQL的raw_records表中"""

# 生成并保存代码
success = web_app_client.download_code(
    task_description, 
    "data_pipeline.py"
)

if success:
    print("代码已保存到 data_pipeline.py")
else:
    print("代码生成或保存失败")
```

#### 3. 自定义WebApp URL
```python
from utils import WebAppClient

# 创建客户端实例并指定自定义URL
client = WebAppClient("http://192.168.1.100:5000")

# 生成代码
task_description = "创建一个简单的数据处理脚本"
code = client.generate_code(task_description)

# 使用完毕后关闭会话
client.close()
```

#### 4. 完整示例
```python
from utils import web_app_client
import os

def main():
    # 定义任务描述
    task_description = """1. 从OSS的raw_data/目录下读取最新的CSV文件
2. 将文件内容解析后批量插入到MySQL的raw_records表中
3. 对处理完成的文件，在OSS中移动到processed_data/目录
4. 记录处理日志到SQLite的process_logs表"""

    # 生成代码
    print("正在生成代码...")
    generated_code = web_app_client.generate_code(task_description)
    
    if generated_code:
        print("代码生成成功!")
        
        # 保存代码到文件
        filename = "data_pipeline.py"
        success = web_app_client.download_code(task_description, filename)
        
        if success:
            print(f"代码已保存到 {filename}")
            
            # 显示代码的一部分
            print("\n生成的代码预览:")
            lines = generated_code.split('\n')
            for i, line in enumerate(lines[:10]):  # 显示前10行
                print(f"{i+1:2d}: {line}")
            
            if len(lines) > 10:
                print("... (代码省略)")
        else:
            print("保存代码失败")
    else:
        print("代码生成失败")

if __name__ == "__main__":
    main()
```

## Flask 工具类使用指南

### 初始化
```python
from flask import Flask
from utils import flask_util

app = Flask(__name__)
flask_util.init_app(app)
```

### 核心方法
- `success_response(data=None, message="操作成功", code=200)` - 成功响应
- `error_response(message="操作失败", code=500, data=None)` - 错误响应
- `validate_json(required_fields=None)` - 验证JSON请求数据装饰器
- `require_params(required_params=None)` - 验证查询参数装饰器
- `paginate(default_page=1, default_per_page=10, max_per_page=100)` - 分页装饰器
- `api_route(rule, **options)` - API路由装饰器
- `get_client_ip()` - 获取客户端IP地址
- `get_request_id()` - 获取请求ID

### 使用示例

#### 1. 基本响应
```python
from flask import Flask
from utils import flask_util

app = Flask(__name__)
flask_util.init_app(app)

@app.route('/api/users')
def get_users():
    users = [{'id': 1, 'name': '张三'}, {'id': 2, 'name': '李四'}]
    return flask_util.success_response(users, "获取用户列表成功")

@app.route('/api/error')
def error_example():
    return flask_util.error_response("这是一个错误示例", 400)
```

#### 2. JSON验证装饰器
```python
@app.route('/api/users', methods=['POST'])
@flask_util.validate_json(['name', 'email'])
def create_user():
    data = request.json_data  # 通过装饰器添加的JSON数据
    name = data['name']
    email = data['email']
    
    # 处理创建用户逻辑
    user = {'id': 1, 'name': name, 'email': email}
    return flask_util.success_response(user, "用户创建成功")
```

#### 3. 参数验证装饰器
```python
@app.route('/api/search')
@flask_util.require_params(['keyword'])
def search():
    keyword = request.args.get('keyword')
    # 处理搜索逻辑
    results = [{'id': 1, 'title': f'包含{keyword}的结果'}]
    return flask_util.success_response(results, "搜索完成")
```

#### 4. 分页装饰器
```python
@app.route('/api/users')
@flask_util.paginate(default_page=1, default_per_page=10)
def get_users_paginated():
    pagination = request.pagination  # 通过装饰器添加的分页信息
    page = pagination['page']
    per_page = pagination['per_page']
    offset = pagination['offset']
    
    # 处理分页查询逻辑
    users = []
    for i in range(offset, offset + per_page):
        users.append({'id': i, 'name': f'用户{i}'})
    
    return flask_util.success_response({
        'users': users,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': 100
        }
    }, "获取用户列表成功")
```

#### 5. API路由装饰器
```python
# 使用API路由装饰器自动处理响应
@flask_util.api_route('/api/hello', methods=['GET'])
def hello():
    return "Hello, World!"  # 自动包装为成功响应

@flask_util.api_route('/api/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    # 返回 (data, message, code) 元组
    return {'id': user_id, 'name': f'用户{user_id}'}, "获取用户信息成功", 200
```

#### 6. 获取客户端信息
```python
@app.route('/api/info')
def get_info():
    client_ip = flask_util.get_client_ip()
    request_id = flask_util.get_request_id()
    
    return flask_util.success_response({
        'client_ip': client_ip,
        'request_id': request_id
    }, "获取客户端信息成功")
```

#### 7. 完整示例
```python
from flask import Flask
from utils import flask_util, mysql_util

app = Flask(__name__)
flask_util.init_app(app)

# 初始化数据库连接
mysql_util.connect()

@app.route('/')
def index():
    return flask_util.success_response({"message": "欢迎使用AI-DO Utils工具库"})

@flask_util.api_route('/api/users', methods=['GET'])
@flask_util.paginate(default_page=1, default_per_page=10)
def get_users():
    pagination = request.pagination
    offset = pagination['offset']
    limit = pagination['per_page']
    
    # 从数据库查询用户
    users = mysql_util.execute_query(
        "SELECT * FROM users LIMIT %s OFFSET %s", 
        (limit, offset)
    )
    
    # 获取总数
    total_result = mysql_util.execute_query("SELECT COUNT(*) as total FROM users")
    total = total_result[0]['total'] if total_result else 0
    
    return {
        'users': users,
        'pagination': {
            'page': pagination['page'],
            'per_page': pagination['per_page'],
            'total': total
        }
    }, "获取用户列表成功"

@flask_util.api_route('/api/users', methods=['POST'])
@flask_util.validate_json(['name', 'email'])
def create_user():
    data = request.json_data
    name = data['name']
    email = data['email']
    
    # 插入到数据库
    mysql_util.execute_update(
        "INSERT INTO users (name, email) VALUES (%s, %s)",
        (name, email)
    )
    
    return {"name": name, "email": email}, "用户创建成功", 201

if __name__ == '__main__':
    app.run(debug=True)
```

## ServiceClient 工具类使用指南

ServiceClient工具类专用于调用需要特定加密签名的远程接口（如李龙平台接口、BI平台接口等）。

### 初始化
```python
# 初始化服务客户端
client = ServiceClient(appid="your_appid", appkey="your_appkey", url_prefix="https://api.example.com")
```

### 核心方法
- `exec(url, obj_data, timeout=20000)` - 调用远程接口

### 使用示例
```python
# 初始化客户端
client = ServiceClient(
    appid="your_app_id",
    appkey="your_app_key",
    url_prefix="https://api.example.com"
)

# 准备请求数据
request_data = {
    "user_id": 12345,
    "action": "get_user_info",
    "params": {
        "include_profile": True,
        "include_preferences": False
    }
}

# 调用远程接口
response = client.exec("/user/service", request_data)

# 处理响应
if response.get("code") == 0:
    print("请求成功:", response.get("content"))
else:
    print("请求失败:", response.get("content"))
```

## MySQL 工具类使用指南

### 核心方法
- `connect()` - 建立数据库连接
- `execute_query(sql, params=None)` - 执行查询语句，返回查询结果
- `execute_update(sql, params=None)` - 执行更新语句（INSERT/UPDATE/DELETE），返回影响行数
- `close()` - 关闭数据库连接

### 使用示例
```python
# 建立连接
mysql_util.connect()

# 查询数据
users = mysql_util.execute_query('SELECT * FROM users WHERE age > %s', (18,))

# 插入数据
affected_rows = mysql_util.execute_update(
    'INSERT INTO users (name, age) VALUES (%s, %s)', 
    ('张三', 25)
)

# 更新数据
mysql_util.execute_update(
    'UPDATE users SET age = %s WHERE name = %s', 
    (26, '张三')
)

# 删除数据
mysql_util.execute_update('DELETE FROM users WHERE name = %s', ('张三',))

# 关闭连接
mysql_util.close()
```

## Redis 工具类使用指南

### 核心方法
- `connect()` - 建立 Redis 连接
- `get(key)` - 获取指定键的值
- `set(key, value, expire_seconds=None)` - 设置键值对，可设置过期时间
- `delete(key)` - 删除指定键
- `close()` - 关闭 Redis 连接

### 使用示例
```python
# 建立连接
redis_util.connect()

# 设置键值
redis_util.set('username', '张三')
redis_util.set('session_token', 'abc123', 3600)  # 1小时后过期

# 获取键值
username = redis_util.get('username')

# 删除键
redis_util.delete('session_token')

# 关闭连接
redis_util.close()
```

## RabbitMQ 工具类使用指南

### 核心方法
- `connect()` - 建立 RabbitMQ 连接
- `send_message(queue, message)` - 向指定队列发送消息
- `consume_messages(queue, callback, auto_ack=False)` - 消费指定队列的消息
- `manual_ack(channel, delivery_tag)` - 手动确认消息
- `manual_nack(channel, delivery_tag, requeue=True)` - 手动拒绝消息
- `stop_consuming()` - 停止消费消息
- `close()` - 关闭 RabbitMQ 连接

### 使用示例

#### 1. 发送消息
```python
# 建立连接
rabbitmq_util.connect()

# 发送消息
rabbitmq_util.send_message('user_registration', '{"user_id": 123, "email": "user@example.com"}')
```

#### 2. 自动确认消息消费
```python
# 定义消息处理函数
def process_message_auto_ack(message_info):
    message = message_info['body']
    print(f"自动确认模式 - 收到消息: {message}")
    # 处理业务逻辑
    # 无需手动确认，系统会自动确认

# 消费消息（自动确认）
rabbitmq_util.consume_messages('user_registration', process_message_auto_ack, auto_ack=True)
```

#### 3. 手动确认消息消费
```python
# 定义消息处理函数
def process_message_manual_ack(message_info):
    message = message_info['body']
    channel = message_info['channel']
    method = message_info['method']
    
    try:
        print(f"手动确认模式 - 收到消息: {message}")
        # 处理业务逻辑
        # ... 处理过程 ...
        
        # 手动确认消息
        rabbitmq_util.manual_ack(channel, method.delivery_tag)
        print("消息处理完成并已确认")
    except Exception as e:
        print(f"处理消息失败: {e}")
        # 手动拒绝消息，可以选择是否重新入队
        rabbitmq_util.manual_nack(channel, method.delivery_tag, requeue=True)

# 消费消息（手动确认）
rabbitmq_util.consume_messages('user_registration', process_message_manual_ack, auto_ack=False)
```

#### 4. 停止消费
```python
# 在需要停止消费时调用
rabbitmq_util.stop_consuming()
```

#### 5. 关闭连接
```python
# 关闭连接
rabbitmq_util.close()
```

## SQLite 工具类使用指南

### 核心方法
- `connect()` - 建立 SQLite 连接
- `execute_query(sql, params=None)` - 执行查询语句，返回查询结果
- `execute_update(sql, params=None)` - 执行更新语句，返回影响行数
- `close()` - 关闭数据库连接

### 使用示例
```python
# 建立连接
sqlite_util.connect()

# 创建表
sqlite_util.execute_update('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER
    )
''')

# 插入数据
sqlite_util.execute_update(
    'INSERT INTO users (name, age) VALUES (?, ?)', 
    ('张三', 25)
)

# 查询数据
users = sqlite_util.execute_query('SELECT * FROM users WHERE age > ?', (18,))

# 更新数据
sqlite_util.execute_update(
    'UPDATE users SET age = ? WHERE name = ?', 
    (26, '张三')
)

# 删除数据
sqlite_util.execute_update('DELETE FROM users WHERE name = ?', ('张三',))

# 关闭连接
sqlite_util.close()
```

## 阿里云表格存储(OTS)工具类使用指南

### 核心方法
- `connect(instance_name=None)` - 建立 OTS 客户端连接
- `create_table(table_meta, reserved_throughput, instance_name=None)` - 创建表
- `put_row(table_name, primary_key, attribute_columns, instance_name=None)` - 插入一行数据
- `get_row(table_name, primary_key, columns_to_get=None, instance_name=None)` - 获取一行数据
- `delete_row(table_name, primary_key, instance_name=None)` - 删除一行数据
- `update_row(table_name, primary_key, attribute_columns, instance_name=None)` - 更新一行数据
- `batch_write_row(request, instance_name=None)` - 批量写入数据
- `batch_get_row(request, instance_name=None)` - 批量读取数据
- `get_range(table_name, direction, inclusive_start_primary_key, exclusive_end_primary_key, columns_to_get=None, limit=None, instance_name=None)` - 范围查询
- `search(table_name, search_query, columns_to_get=None, instance_name=None, index_name=None)` - 索引查询
- `create_search_index(table_name, index_name, index_schema, instance_name=None)` - 创建搜索索引
- `delete_search_index(table_name, index_name, instance_name=None)` - 删除搜索索引
- `list_search_index(table_name, instance_name=None)` - 列出搜索索引

### 使用示例

#### 1. 基本操作
```python
# 建立连接
ots_util.connect()

# 插入数据
primary_key = [('uid', 1)]
attribute_columns = [('name', '张三'), ('age', 25)]
ots_util.put_row('user', primary_key, attribute_columns)

# 获取数据
result = ots_util.get_row('user', [('uid', 1)])
if result.row:
    print("用户信息:")
    for column in result.row.primary_key_columns:
        print(f"  {column[0]}: {column[1]}")
    for column in result.row.attribute_columns:
        print(f"  {column[0]}: {column[1]}")

# 更新数据
update_columns = [('age', 26)]
ots_util.update_row('user', [('uid', 1)], update_columns)

# 删除数据
ots_util.delete_row('user', [('uid', 1)])
```

#### 2. 指定实例名称操作
```python
# 在特定实例上操作
instance_name = "my-instance"
ots_util.put_row('user', [('uid', 1)], [('name', '张三')], instance_name=instance_name)
```

#### 3. 范围查询
```python
from tablestore import Direction

# 范围查询
start_pk = [('uid', INF_MIN)]
end_pk = [('uid', INF_MAX)]
result = ots_util.get_range('user', Direction.FORWARD, start_pk, end_pk, limit=10)
```

#### 4. 索引查询（搜索）
```python
from tablestore import SearchQuery, TermQuery, ColumnsToGet

# 构建搜索查询
term_query = TermQuery('name', '张三')
search_query = SearchQuery(term_query, limit=10)

# 执行索引查询
result = ots_util.search('user', search_query, index_name='user_index')
```

#### 5. 搜索索引管理
```python
from tablestore import FieldSchema, FieldType, IndexSchema

# 创建搜索索引
field_schema = FieldSchema('name', FieldType.TEXT)
index_schema = IndexSchema([field_schema])
ots_util.create_search_index('user', 'user_index', index_schema)

# 列出搜索索引
indexes = ots_util.list_search_index('user')
print("搜索索引列表:", indexes)

# 删除搜索索引
ots_util.delete_search_index('user', 'user_index')
```

## 阿里云 OSS 工具类使用指南

### 核心方法
- `connect()` - 建立 OSS 客户端连接
- `put_object(object_name, data)` - 上传对象
- `get_object(object_name)` - 获取对象
- `delete_object(object_name)` - 删除对象
- `list_objects(prefix='', max_keys=100)` - 列出对象

### 使用示例
```python
# 建立连接
oss_util.connect()

# 上传文件
oss_util.put_object('documents/user_info.txt', b'用户信息内容')

# 上传二进制数据
with open('image.jpg', 'rb') as f:
    oss_util.put_object('images/profile.jpg', f.read())

# 下载文件
obj = oss_util.get_object('documents/user_info.txt')
content = obj.read()

# 删除文件
oss_util.delete_object('images/profile.jpg')

# 列出文件
objects = oss_util.list_objects(prefix='documents/', max_keys=50)
for obj in objects:
    print(f"文件: {obj.key}")
```

## 最佳实践

1. **HTTP请求选择**：
   - 普通HTTP请求：使用 `requests` 库
   - 李龙平台/Bi平台接口：使用 `ServiceClient` 工具类

2. 所有工具类都是单例模式，不需要重复创建实例
3. 建议在应用程序启动时调用 `connect()` 方法建立连接
4. 对于长时间运行的应用程序，建议在适当的时候调用 `close()` 方法释放连接资源
5. 表格存储和 OSS 工具类会自动管理连接，无需显式关闭
6. 使用参数化查询防止 SQL 注入攻击
7. 在处理消息队列时，确保回调函数能够正确处理异常情况
8. 对于批量操作，考虑使用事务或批量接口以提高性能
9. 在使用 RabbitMQ 手动确认模式时，确保在处理完消息后调用 `manual_ack()` 或 `manual_nack()`
10. 在使用 OTS 时，合理设计主键和索引以提高查询性能
11. 在使用 Flask 工具类时，充分利用装饰器简化代码
12. 使用 WebAppClient 工具类时，确保 web_app 服务正在运行
13. 通过环境变量配置 WebAppClient 的基础 URL，提高配置的灵活性

## 异常处理

所有工具类在遇到错误时都会抛出相应的异常，建议在使用时进行适当的异常处理：

```python
try:
    mysql_util.connect()
    users = mysql_util.execute_query('SELECT * FROM users')
except Exception as e:
    print(f"MySQL操作失败: {e}")
```