#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
th_cnd_utils 使用示例
演示如何使用 th_cnd_utils 包的各种功能
"""

def example_basic_usage():
    """基本使用示例"""
    print("=== th_cnd_utils 基本使用示例 ===")
    
    # 导入所需的模块
    from th_cnd_utils import ServiceClient, web_app_client
    
    # 使用ServiceClient调用李龙平台接口
    print("1. 使用ServiceClient调用李龙平台接口:")
    client = ServiceClient(
        appid="your_app_id",
        appkey="your_app_key",
        url_prefix="https://api.example.com"
    )
    print(f"   ServiceClient创建成功，URL前缀: {client.url_prefix}")
    
    # 使用WebAppClient
    print("2. 使用WebAppClient:")
    print(f"   WebApp URL: {web_app_client.get_base_url()}")


def example_database_tools():
    """数据库工具示例"""
    print("\n=== 数据库工具示例 ===")
    
    try:
        from th_cnd_utils import mysql_util, redis_util
        
        print("1. MySQL工具:")
        print(f"   MySQL工具实例: {type(mysql_util)}")
        
        print("2. Redis工具:")
        print(f"   Redis工具实例: {type(redis_util)}")
        
    except Exception as e:
        print(f"   数据库工具导入失败: {e}")


def example_cloud_tools():
    """云服务工具示例"""
    print("\n=== 云服务工具示例 ===")
    
    try:
        from th_cnd_utils import oss_util, ots_util
        
        print("1. OSS工具:")
        print(f"   OSS工具实例: {type(oss_util)}")
        
        print("2. OTS工具:")
        print(f"   OTS工具实例: {type(ots_util)}")
        
    except Exception as e:
        print(f"   云服务工具导入失败: {e}")


def example_message_queue():
    """消息队列工具示例"""
    print("\n=== 消息队列工具示例 ===")
    
    try:
        from th_cnd_utils import rabbitmq_util
        
        print("1. RabbitMQ工具:")
        print(f"   RabbitMQ工具实例: {type(rabbitmq_util)}")
        
    except Exception as e:
        print(f"   消息队列工具导入失败: {e}")


def example_flask_util():
    """Flask工具示例"""
    print("\n=== Flask工具示例 ===")
    
    try:
        from th_cnd_utils import flask_util
        
        print("1. Flask工具:")
        print(f"   Flask工具实例: {type(flask_util)}")
        
    except Exception as e:
        print(f"   Flask工具导入失败: {e}")


def main():
    """主函数"""
    print("th_cnd_utils 使用示例")
    print("=" * 50)
    
    # 运行所有示例
    examples = [
        example_basic_usage,
        example_database_tools,
        example_cloud_tools,
        example_message_queue,
        example_flask_util,
    ]
    
    for example in examples:
        example()
    
    print("\n" + "=" * 50)
    print("所有示例运行完成!")
    print("详细使用说明请参考 UTILS_CALL_GUIDE.md")


if __name__ == "__main__":
    main()