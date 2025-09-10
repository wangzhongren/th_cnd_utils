# th_cnd_utils 包结构说明

## 包目录结构

```
th_cnd_utils/
├── th_cnd_utils/              # 主包目录
│   ├── __init__.py           # 包初始化文件
│   ├── config.py             # 配置模块
│   ├── service_client.py     # 李龙平台加密接口客户端
│   ├── web_app_client.py     # Web应用程序客户端
│   ├── flask_util.py         # Flask工具类
│   ├── db/                   # 数据库工具
│   │   ├── __init__.py
│   │   ├── mysql.py          # MySQL工具
│   │   ├── redis.py          # Redis工具
│   │   ├── rabbitmq.py       # RabbitMQ工具
│   │   └── sqlite.py         # SQLite工具
│   ├── cloud/                # 云服务工具
│   │   ├── __init__.py
│   │   ├── oss.py            # 阿里云OSS工具
│   │   └── ots.py            # 阿里云OTS工具
│   └── examples/             # 使用示例
│       ├── service_client_example.py
│       └── web_app_client_example.py
├── README.md                 # 包说明文档
├── LICENSE                   # 许可证文件
├── requirements.txt          # 依赖列表
├── setup.py                  # 安装配置
├── pyproject.toml            # 现代化构建配置
├── MANIFEST.in               # 包含文件清单
├── .env.example             # 环境变量示例
├── UTILS_CALL_GUIDE.md      # 工具使用指南
└── UTILS_CALL_REPORT.md     # 工具调用报告
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

## 安装和使用

### 安装
```bash
pip install th_cnd_utils
```

### 基本使用
```python
# 导入工具
from th_cnd_utils import mysql_util, redis_util, ServiceClient

# 使用MySQL工具
mysql_util.connect()
users = mysql_util.execute_query('SELECT * FROM users')

# 使用Redis工具
redis_util.connect()
redis_util.set('key', 'value')

# 使用李龙平台客户端
client = ServiceClient(appid='your_id', appkey='your_key')
response = client.exec('/api/path', {'data': 'value'})
```

## 配置

包支持通过环境变量进行配置，参考 `.env.example` 文件：

```env
# 数据库配置
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_DATABASE=test

# 李龙平台配置
WEB_APP_BASE_URL=http://127.0.0.1:5000
```

## 许可证

本包采用 MIT 许可证发布。