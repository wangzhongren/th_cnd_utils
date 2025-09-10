# th_cnd_utils - AI-DO工具库

[![PyPI](https://img.shields.io/pypi/v/th_cnd_utils)](https://pypi.org/project/th_cnd_utils/)
[![Python Version](https://img.shields.io/pypi/pyversions/th_cnd_utils)](https://pypi.org/project/th_cnd_utils/)
[![License](https://img.shields.io/pypi/l/th_cnd_utils)](https://github.com/your-org/th_cnd_utils/blob/main/LICENSE)

一个包含各种数据存储和云服务工具的Python库。

## 功能特性

- **数据库工具**：MySQL、Redis、SQLite
- **消息队列**：RabbitMQ
- **云服务**：阿里云表格存储(OTS)、阿里云对象存储(OSS)
- **专用客户端**：李龙平台加密接口客户端
- **Web工具**：Web应用程序客户端、Flask工具类

## 安装

```bash
pip install th_cnd_utils
```

## 快速开始

### 数据库操作

```python
from th_cnd_utils import mysql_util, redis_util

# MySQL操作
mysql_util.connect()
users = mysql_util.execute_query('SELECT * FROM users WHERE age > %s', (18,))

# Redis操作
redis_util.connect()
redis_util.set('username', '张三', 3600)
username = redis_util.get('username')
```

### 云服务操作

```python
from th_cnd_utils import oss_util, ots_util

# OSS操作
oss_util.connect()
oss_util.put_object('documents/readme.txt', b'Hello World')

# OTS操作
ots_util.connect()
ots_util.put_row('user', [('uid', 1)], [('name', '张三'), ('age', 25)])
```

### 李龙平台接口调用

```python
from th_cnd_utils import ServiceClient

client = ServiceClient(
    appid="your_app_id",
    appkey="your_app_key",
    url_prefix="https://api.example.com"
)

response = client.exec("/user/service", {
    "user_id": 12345,
    "action": "get_user_info"
})
```

## 文档

详细使用说明请参考 [调用指南](UTILS_CALL_GUIDE.md)

## 依赖

- python-dotenv>=1.0.0
- PyMySQL>=1.0.2
- redis>=4.5.4
- pika>=1.3.1
- tablestore>=5.1.0
- oss2>=2.17.0
- requests>=2.31.0
- flask>=2.3.2
- flask-cors>=4.0.0

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 开发

```bash
# 安装开发依赖
pip install -e .[dev]

# 运行测试
pytest

# 代码格式化
black .
```