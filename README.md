# th_cnd_utils - AI-DO工具库

一个包含各种数据存储和云服务工具的Python库，旨在将AI装进框架的笼子。

## 项目理念

**将AI装进框架的笼子** - 我们相信最好的AI应用不是让AI决定一切，而是让AI在我们设计好的框架内，成为提升效率的强大助手。

## 功能特性

- **数据库工具**：MySQL、Redis、SQLite、RabbitMQ
- **云服务集成**：阿里云OSS、阿里云OTS
- **AI代码生成客户端**：通过Web服务接口调用大模型生成代码
- **专用客户端**：李龙平台加密接口客户端
- **Web框架工具**：Flask工具类，简化API开发

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

### AI代码生成

```python
from th_cnd_utils import web_app_client

# 通过WebApp接口调用AI生成代码
task = "创建一个从OSS读取CSV文件并插入MySQL的脚本"
code = web_app_client.generate_code(task)
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

## 核心模块

### 数据库工具
- `mysql_util`: MySQL数据库操作工具
- `redis_util`: Redis缓存操作工具
- `sqlite_util`: SQLite数据库操作工具
- `rabbitmq_util`: RabbitMQ消息队列工具

### 云服务工具
- `oss_util`: 阿里云对象存储(OSS)工具
- `ots_util`: 阿里云表格存储(OTS)工具

### 专用客户端
- `ServiceClient`: 李龙平台加密接口客户端
- `web_app_client`: Web应用程序客户端

### Web框架工具
- `flask_util`: Flask工具类

### 配置管理
- `config`: 统一配置加载模块

## 文档

详细使用说明请参考项目根目录的 [调用指南](../UTILS_CALL_GUIDE.md)

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

## 项目结构

```
th_cnd_utils/
├── db/                   # 数据库工具
│   ├── mysql.py          # MySQL工具
│   ├── redis.py          # Redis工具
│   ├── rabbitmq.py       # RabbitMQ工具
│   └── sqlite.py         # SQLite工具
├── cloud/                # 云服务工具
│   ├── oss.py            # 阿里云OSS工具
│   └── ots.py            # 阿里云OTS工具
├── examples/             # 使用示例
├── service_client.py     # 李龙平台客户端
├── web_app_client.py     # Web应用客户端
├── flask_util.py         # Flask工具类
├── config.py             # 配置模块
└── __init__.py           # 包初始化文件
```

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

## 相关项目

这个包是 [AI-DO项目](../README.md) 的一部分，该项目还包括：
- [web_app](../web_app/): Web服务端，提供图形界面和API接口
- [tkinter_app](../tkinter_app/): 桌面应用，提供本地界面和代码执行

了解完整架构和使用方式，请查看项目根目录的README.md文件。
