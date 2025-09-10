# AI-DO Utils (Python 版本)

这是一个 Python 工具类库，包含操作各种数据库和云服务的工具类。

## 功能特性

- MySQL 数据库操作工具
- Redis 缓存操作工具
- RabbitMQ 消息队列操作工具
- SQLite 数据库操作工具
- 阿里云表格存储(OTS)操作工具
- 阿里云对象存储(OSS)操作工具

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置

复制 `.env.example` 文件为 `.env` 并填写相应的配置信息：

```bash
cp .env.example .env
```

## 使用方法

```python
# 引入工具类
from utils import mysql_util, redis_util, rabbitmq_util, sqlite_util, ots_util, oss_util

# 使用 MySQL 工具
mysql_util.connect()
users = mysql_util.execute_query('SELECT * FROM users')

# 使用 Redis 工具
redis_util.connect()
redis_util.set('key', 'value', 3600)  # 保存1小时
value = redis_util.get('key')

# 使用 RabbitMQ 工具
rabbitmq_util.connect()
rabbitmq_util.send_message('task_queue', 'Hello World')

# 使用 SQLite 工具
sqlite_util.connect()
sqlite_util.execute_update('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)')
user = sqlite_util.execute_query('SELECT * FROM users WHERE id = ?', (1,))

# 使用阿里云表格存储工具
ots_util.connect()
primary_key = [('uid', 1)]
attribute_columns = [('name', '张三'), ('age', 25)]
ots_util.put_row('user', primary_key, attribute_columns)

# 使用阿里云 OSS 工具
oss_util.connect()
oss_util.put_object('example.txt', b'Hello World')
```

## 工具类说明

### MySQL 工具 (utils/db/mysql.py)

提供 MySQL 数据库连接和查询功能。

### Redis 工具 (utils/db/redis.py)

提供 Redis 连接和基本操作功能。

### RabbitMQ 工具 (utils/db/rabbitmq.py)

提供 RabbitMQ 连接和消息发送/接收功能。

### SQLite 工具 (utils/db/sqlite.py)

提供 SQLite 数据库操作功能。

### 阿里云表格存储工具 (utils/cloud/ots.py)

提供阿里云表格存储(OTS)的基本操作功能。

### 阿里云 OSS 工具 (utils/cloud/oss.py)

提供阿里云对象存储(OSS)的基本操作功能。

## 配置说明

所有配置项都从 `.env` 文件中读取，详细配置项请参考 `.env.example` 文件。