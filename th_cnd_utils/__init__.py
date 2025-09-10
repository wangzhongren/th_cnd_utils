# th_cnd_utils/__init__.py
"""
th_cnd_utils - AI-DO工具库

一个包含各种数据存储和云服务工具的Python库。

功能特性：
- MySQL数据库操作工具
- Redis缓存操作工具
- RabbitMQ消息队列工具
- SQLite数据库操作工具
- 阿里云表格存储(OTS)工具
- 阿里云对象存储(OSS)工具
- 李龙平台加密接口客户端
- Web应用程序客户端
- Flask工具类
"""

from .db.mysql import mysql_util
from .db.redis import redis_util
from .db.rabbitmq import rabbitmq_util
from .db.sqlite import sqlite_util
from .cloud.ots import ots_util
from .cloud.oss import oss_util
from .service_client import ServiceClient
from .flask_util import FlaskUtil, flask_util
from .web_app_client import WebAppClient, web_app_client
from .config import config

__all__ = [
    'mysql_util',
    'redis_util',
    'rabbitmq_util',
    'sqlite_util',
    'ots_util',
    'oss_util',
    'ServiceClient',
    'FlaskUtil',
    'flask_util',
    'WebAppClient',
    'web_app_client',
    'config'
]

__version__ = "1.0.0"
__author__ = "AI-DO开发团队"
__email__ = "aido@example.com"
__license__ = "MIT"
__description__ = "AI-DO工具库 - 包含各种数据存储和云服务工具的Python库"