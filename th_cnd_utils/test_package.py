#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
th_cnd_utils 包测试脚本
验证包的基本功能是否正常工作
"""

def test_package_import():
    """测试包导入"""
    print("=== 测试包导入 ===")
    try:
        import th_cnd_utils
        print(f"[PASS] 包导入成功，版本: {th_cnd_utils.__version__}")
        return True
    except Exception as e:
        print(f"[FAIL] 包导入失败: {e}")
        return False


def test_module_imports():
    """测试模块导入"""
    print("\n=== 测试模块导入 ===")
    modules_to_test = [
        ("mysql_util", "from th_cnd_utils import mysql_util"),
        ("redis_util", "from th_cnd_utils import redis_util"),
        ("rabbitmq_util", "from th_cnd_utils import rabbitmq_util"),
        ("sqlite_util", "from th_cnd_utils import sqlite_util"),
        ("ots_util", "from th_cnd_utils import ots_util"),
        ("oss_util", "from th_cnd_utils import oss_util"),
        ("ServiceClient", "from th_cnd_utils import ServiceClient"),
        ("web_app_client", "from th_cnd_utils import web_app_client"),
        ("flask_util", "from th_cnd_utils import flask_util"),
    ]
    
    success_count = 0
    for name, import_stmt in modules_to_test:
        try:
            exec(import_stmt)
            print(f"[PASS] {name} 导入成功")
            success_count += 1
        except Exception as e:
            print(f"[FAIL] {name} 导入失败: {e}")
    
    print(f"\n模块导入测试结果: {success_count}/{len(modules_to_test)} 成功")
    return success_count == len(modules_to_test)


def test_service_client():
    """测试ServiceClient基本功能"""
    print("\n=== 测试ServiceClient ===")
    try:
        from th_cnd_utils import ServiceClient
        client = ServiceClient(appid="test", appkey="test")
        print("[PASS] ServiceClient 实例化成功")
        print(f"[PASS] ServiceClient 类型: {type(client)}")
        return True
    except Exception as e:
        print(f"[FAIL] ServiceClient 测试失败: {e}")
        return False


def test_web_app_client():
    """测试WebAppClient基本功能"""
    print("\n=== 测试WebAppClient ===")
    try:
        from th_cnd_utils import web_app_client
        print("[PASS] web_app_client 实例获取成功")
        print(f"[PASS] 默认URL: {web_app_client.get_base_url()}")
        return True
    except Exception as e:
        print(f"[FAIL] WebAppClient 测试失败: {e}")
        return False


def main():
    """主函数"""
    print("th_cnd_utils 包测试")
    print("=" * 50)
    
    # 运行所有测试
    tests = [
        test_package_import,
        test_module_imports,
        test_service_client,
        test_web_app_client,
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"测试完成: {passed}/{len(tests)} 通过")
    
    if passed == len(tests):
        print("所有测试通过！th_cnd_utils 包工作正常。")
    else:
        print("部分测试失败，请检查上述错误信息。")


if __name__ == "__main__":
    main()