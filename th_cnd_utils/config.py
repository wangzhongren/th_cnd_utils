import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置字典
config = {
    # MySQL 配置
    'mysql': {
        'host': os.getenv('MYSQL_HOST', 'localhost'),
        'port': int(os.getenv('MYSQL_PORT', 3306)),
        'user': os.getenv('MYSQL_USER', 'root'),
        'password': os.getenv('MYSQL_PASSWORD', ''),
        'database': os.getenv('MYSQL_DATABASE', 'test')
    },
    
    # Redis 配置
    'redis': {
        'host': os.getenv('REDIS_HOST', 'localhost'),
        'port': int(os.getenv('REDIS_PORT', 6379)),
        'password': os.getenv('REDIS_PASSWORD', ''),
        'db': int(os.getenv('REDIS_DB', 0))
    },
    
    # RabbitMQ 配置
    'rabbitmq': {
        'host': os.getenv('RABBITMQ_HOST', 'localhost'),
        'port': int(os.getenv('RABBITMQ_PORT', 5672)),
        'user': os.getenv('RABBITMQ_USER', 'guest'),
        'password': os.getenv('RABBITMQ_PASSWORD', 'guest'),
        'vhost': os.getenv('RABBITMQ_VHOST', '/')
    },
    
    # SQLite 配置
    'sqlite': {
        'path': os.getenv('SQLITE_PATH', './database.sqlite')
    },
    
    # 阿里云配置
    'aliyun': {
        'access_key_id': os.getenv('ALIYUN_ACCESS_KEY_ID', ''),
        'access_key_secret': os.getenv('ALIYUN_ACCESS_KEY_SECRET', ''),
        'region': os.getenv('ALIYUN_REGION', 'cn-hangzhou')
    },
    
    # 阿里云表格存储配置
    'ots': {
        'endpoint': os.getenv('OTS_ENDPOINT', ''),
        'instance_name': os.getenv('OTS_INSTANCE_NAME', '')
    },
    
    # 阿里云 OSS 配置
    'oss': {
        'endpoint': os.getenv('OSS_ENDPOINT', ''),
        'bucket_name': os.getenv('OSS_BUCKET_NAME', '')
    }
}