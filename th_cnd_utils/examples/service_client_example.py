#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ServiceClient 使用示例
演示如何使用 ServiceClient 工具类调用需要特定加密签名的远程接口
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from th_cnd_utils import ServiceClient


def example1_li_long_platform():
    """李龙平台接口调用示例"""
    print("=== 李龙平台接口调用示例 ===")
    
    # 初始化李龙平台客户端
    client = ServiceClient(
        appid="your_li_long_app_id",
        appkey="your_li_long_app_key",
        url_prefix="https://api.li-long.com"
    )
    
    # 准备请求数据（李龙平台特定格式）
    request_data = {
        "service": "user_management",
        "action": "get_user_list",
        "params": {
            "page": 1,
            "limit": 30,
            "filter": {
                "status": "active"
            }
        }
    }
    
    # 调用李龙平台接口
    response = client.exec("/gateway/service", request_data)
    
    # 处理响应
    if response.get("code") == 0:
        print("李龙平台接口调用成功:")
        print(f"返回数据: {response.get('content')}")
    else:
        print(f"李龙平台接口调用失败: {response.get('content')}")


def example2_bi_platform():
    """BI平台接口调用示例"""
    print("\n=== BI平台接口调用示例 ===")
    
    # 初始化BI平台客户端
    client = ServiceClient(
        appid="your_bi_app_id",
        appkey="your_bi_app_key",
        url_prefix="https://bi.example.com/api"
    )
    
    # 准备请求数据（BI平台特定格式）
    request_data = {
        "report_id": "sales_summary_2023",
        "parameters": {
            "start_date": "2023-01-01",
            "end_date": "2023-12-31",
            "group_by": ["region", "product_category"]
        }
    }
    
    # 调用BI平台接口
    response = client.exec("/reports/generate", request_data)
    
    # 处理响应
    if response.get("code") == 0:
        print("BI平台接口调用成功:")
        print(f"报表数据: {response.get('content')}")
    else:
        print(f"BI平台接口调用失败: {response.get('content')}")


def example3_regular_http_vs_service_client():
    """普通HTTP请求 vs ServiceClient 对比示例"""
    print("\n=== 普通HTTP请求 vs ServiceClient 对比 ===")
    
    import requests
    
    # 普通HTTP请求（使用requests库）
    print("1. 普通HTTP请求（使用requests库）:")
    try:
        response = requests.get("https://jsonplaceholder.typicode.com/users/1")
        if response.status_code == 200:
            user_data = response.json()
            print(f"   获取用户信息成功: {user_data['name']}")
        else:
            print(f"   请求失败，状态码: {response.status_code}")
    except Exception as e:
        print(f"   请求出错: {e}")
    
    # 李龙平台接口（使用ServiceClient）
    print("2. 李龙平台接口（使用ServiceClient）:")
    client = ServiceClient(
        appid="ll_app_123",
        appkey="ll_key_456",
        url_prefix="https://api.li-long.com"
    )
    
    ll_request_data = {
        "service": "user",
        "action": "get_info",
        "user_id": 12345
    }
    
    # ServiceClient会自动处理加密签名
    response = client.exec("/gateway", ll_request_data)
    print("   ServiceClient会自动处理加密签名和认证")


def main():
    """主函数"""
    print("ServiceClient 使用示例")
    print("=" * 50)
    print("ServiceClient专用于调用需要特定加密签名的远程接口")
    print("如：李龙平台接口、BI平台接口等")
    print()
    
    # 运行示例
    example1_li_long_platform()
    example2_bi_platform()
    example3_regular_http_vs_service_client()
    
    print("\n所有示例运行完成!")


if __name__ == "__main__":
    main()