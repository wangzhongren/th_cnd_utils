# AI-DO Utils 工具库调用报告

## 概述

本报告详细介绍了 AI-DO Utils 工具库的使用方法。该工具库提供了对多种数据存储和消息队列系统的统一访问接口，包括 MySQL、Redis、RabbitMQ、SQLite、阿里云表格存储(OTS) 和阿里云对象存储(OSS)。所有配置均通过环境变量进行管理，以确保安全性和可配置性。

## 目录结构

```
utils/
├── __init__.py              # 包入口文件，导出所有工具类
├── config.py                # 配置加载模块
├── db/                      # 数据库相关工具
│   ├── __init__.py
│   ├── mysql.py             # MySQL 工具类
│   ├── redis.py             # Redis 工具类
│   ├── rabbitmq.py          # RabbitMQ 工具类
│   └── sqlite.py            # SQLite 工具类
└── cloud/                   # 云服务相关工具
    ├── __init__.py
    ├── ots.py               # 阿里云表格存储工具类
    └── oss.py               # 阿里云 OSS 工具类
```

## 配置说明

所有工具类都从环境变量读取配置信息。请在项目根目录下创建 `.env` 文件，并参考 `.env.example` 填写相应配置。

### 配置项说明

```env
# 数据库配置
MYSQL_HOST=localhost           # MySQL 主机地址
MYSQL_PORT=3306               # MySQL 端口
MYSQL_USER=root               # MySQL 用户名
MYSQL_PASSWORD=               # MySQL 密码
MYSQL_DATABASE=test           # MySQL 数据库名

REDIS_HOST=localhost          # Redis 主机地址
REDIS_PORT=6379               # Redis 端口
REDIS_PASSWORD=               # Redis 密码
REDIS_DB=0                    # Redis 数据库编号

RABBITMQ_HOST=localhost       # RabbitMQ 主机地址
RABBITMQ_PORT=5672            # RabbitMQ 端口
RABBITMQ_USER=guest           # RabbitMQ 用户名
RABBITMQ_PASSWORD=guest       # RabbitMQ 密码
RABBITMQ_VHOST=/              # RabbitMQ 虚拟主机

SQLITE_PATH=./database.sqlite # SQLite 数据库文件路径

# 阿里云配置
ALIYUN_ACCESS_KEY_ID=         # 阿里云访问密钥 ID
ALIYUN_ACCESS_KEY_SECRET=     # 阿里云访问密钥 Secret
ALIYUN_REGION=cn-hangzhou     # 阿里云区域

# 阿里云表格存储配置
OTS_ENDPOINT=                 # OTS 服务终端节点
OTS_INSTANCE_NAME=            # OTS 实例名称

# 阿里云 OSS 配置
OSS_ENDPOINT=                 # OSS 服务终端节点
OSS_BUCKET_NAME=              # OSS 存储桶名称
```

## 工具类使用说明

### 1. MySQL 工具类 (`utils.db.mysql`)

#### 导入方式
```python
from utils import mysql_util
# 或者
from utils.db.mysql import mysql_util
```

#### 主要方法
- `connect()` - 建立数据库连接
- `execute_query(sql, params=None)` - 执行查询语句
- `execute_update(sql, params=None)` - 执行更新语句
- `close()` - 关闭数据库连接

#### 使用示例
```python
# 建立连接
mysql_util.connect()

# 执行查询
users = mysql_util.execute_query('SELECT * FROM users WHERE age > %s', (18,))

# 执行更新
affected_rows = mysql_util.execute_update(
    'INSERT INTO users (name, age) VALUES (%s, %s)', 
    ('张三', 25)
)

# 关闭连接
mysql_util.close()
```

### 2. Redis 工具类 (`utils.db.redis`)

#### 导入方式
```python
from utils import redis_util
# 或者
from utils.db.redis import redis_util
```

#### 主要方法
- `connect()` - 建立 Redis 连接
- `get(key)` - 获取键值
- `set(key, value, expire_seconds=None)` - 设置键值
- `delete(key)` - 删除键
- `close()` - 关闭 Redis 连接

#### 使用示例
```python
# 建立连接
redis_util.connect()

# 设置键值
redis_util.set('username', '张三', 3600)  # 保存1小时

# 获取键值
username = redis_util.get('username')

# 删除键
redis_util.delete('username')

# 关闭连接
redis_util.close()
```

### 3. RabbitMQ 工具类 (`utils.db.rabbitmq`)

#### 导入方式
```python
from utils import rabbitmq_util
# 或者
from utils.db.rabbitmq import rabbitmq_util
```

#### 主要方法
- `connect()` - 建立 RabbitMQ 连接
- `send_message(queue, message)` - 发送消息到队列
- `consume_messages(queue, callback)` - 消费队列中的消息
- `close()` - 关闭 RabbitMQ 连接

#### 使用示例
```python
# 建立连接
rabbitmq_util.connect()

# 发送消息
rabbitmq_util.send_message('task_queue', '处理用户注册')

# 定义消息处理回调函数
def handle_message(message):
    print(f"收到消息: {message}")
    # 处理业务逻辑

# 消费消息
rabbitmq_util.consume_messages('task_queue', handle_message)

# 关闭连接
rabbitmq_util.close()
```

### 4. SQLite 工具类 (`utils.db.sqlite`)

#### 导入方式
```python
from utils import sqlite_util
# 或者
from utils.db.sqlite import sqlite_util
```

#### 主要方法
- `connect()` - 建立 SQLite 连接
- `execute_query(sql, params=None)` - 执行查询语句
- `execute_update(sql, params=None)` - 执行更新语句
- `close()` - 关闭数据库连接

#### 使用示例
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

# 关闭连接
sqlite_util.close()
```

### 5. 阿里云表格存储工具类 (`utils.cloud.ots`)

#### 导入方式
```python
from utils import ots_util
# 或者
from utils.cloud.ots import ots_util
```

#### 主要方法
- `connect()` - 建立 OTS 客户端连接
- `put_row(table_name, primary_key, attribute_columns)` - 插入一行数据
- `get_row(table_name, primary_key, columns_to_get=None)` - 获取一行数据
- `delete_row(table_name, primary_key)` - 删除一行数据
- `create_table(table_meta, reserved_throughput)` - 创建表

#### 使用示例
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
    print(f"用户信息: {result.row}")

# 删除数据
ots_util.delete_row('user', [('uid', 1)])

# 关闭连接（表格存储工具类无显式关闭方法）
```

### 6. 阿里云 OSS 工具类 (`utils.cloud.oss`)

#### 导入方式
```python
from utils import oss_util
# 或者
from utils.cloud.oss import oss_util
```

#### 主要方法
- `connect()` - 建立 OSS 客户端连接
- `put_object(object_name, data)` - 上传对象
- `get_object(object_name)` - 获取对象
- `delete_object(object_name)` - 删除对象
- `list_objects(prefix='', max_keys=100)` - 列出对象

#### 使用示例
```python
# 建立连接
oss_util.connect()

# 上传对象
oss_util.put_object('example.txt', b'Hello World')

# 获取对象
obj = oss_util.get_object('example.txt')
content = obj.read()

# 删除对象
oss_util.delete_object('example.txt')

# 列出对象
objects = oss_util.list_objects(prefix='images/', max_keys=50)
for obj in objects:
    print(obj.key)

# 关闭连接（OSS 工具类无显式关闭方法）
```

## 配置模块使用说明

### 导入方式
```python
from utils import config
# 或者
from utils.config import config
```

### 使用示例
```python
# 获取 MySQL 配置
mysql_host = config['mysql']['host']
mysql_port = config['mysql']['port']

# 获取 Redis 配置
redis_host = config['redis']['host']
redis_db = config['redis']['db']

# 获取阿里云配置
access_key_id = config['aliyun']['access_key_id']
```

## 安装依赖

在使用这些工具类之前，请确保安装了所有必需的依赖项：

```bash
pip install -r requirements.txt
```

## 注意事项

1. 所有工具类均采用单例模式设计，确保在整个应用程序中只有一个实例。
2. 连接方法会自动处理连接的建立和复用，无需手动管理连接池。
3. 建议在应用程序结束时调用 `close()` 方法关闭数据库连接（MySQL、Redis、RabbitMQ、SQLite）。
4. 表格存储和 OSS 工具类会自动管理连接，无需显式关闭。
5. 所有敏感配置信息（如密码、密钥）应通过环境变量管理，不要硬编码在代码中。
6. 在生产环境中，请确保配置了正确的访问权限和安全策略。

## 故障排除

1. 如果连接失败，请检查：
   - 环境变量是否正确配置
   - 对应服务是否正在运行
   - 网络连接是否正常
   - 访问凭证是否正确

2. 如果出现权限错误，请检查：
   - 数据库用户权限
   - Redis 访问密码
   - 阿里云访问密钥权限

3. 如果出现导入错误，请检查：
   - 是否已安装所有依赖项
   - Python 路径是否正确设置
   - 包结构是否完整