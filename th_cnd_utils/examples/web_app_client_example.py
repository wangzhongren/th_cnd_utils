#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
WebAppClient 使用示例
演示如何使用 WebAppClient 工具类调用 web_app 接口生成和下载代码
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from th_cnd_utils import web_app_client


def example1_basic_usage():
    """基本使用示例"""
    print("=== 基本使用示例 ===")
    
    # 获取当前配置的URL
    print(f"WebApp URL: {web_app_client.get_base_url()}")
    
    # 定义任务描述
    task_description = """1. 从OSS的raw_data/目录下读取最新的CSV文件
2. 将文件内容解析后批量插入到MySQL的raw_records表中
3. 对处理完成的文件，在OSS中移动到processed_data/目录
4. 记录处理日志到SQLite的process_logs表

请确保包含适当的错误处理和资源清理。"""
    
    # 生成代码
    print("正在生成代码...")
    generated_code = web_app_client.generate_code(task_description)
    
    if generated_code:
        print("代码生成成功!")
        print("生成的代码预览:")
        lines = generated_code.split('\n')
        for i, line in enumerate(lines[:15]):  # 显示前15行
            print(f"{i+1:2d}: {line}")
        
        if len(lines) > 15:
            print("... (代码省略)")
    else:
        print("代码生成失败")


def example2_download_code():
    """下载代码示例"""
    print("\n=== 下载代码示例 ===")
    
    # 定义简单的任务描述
    task_description = "创建一个Python脚本，打印'Hello, World!'"
    
    # 生成并保存代码
    filename = "hello_world.py"
    success = web_app_client.download_code(task_description, filename)
    
    if success:
        print(f"代码已保存到 {filename}")
        
        # 读取并显示保存的代码
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                code = f.read()
                print("保存的代码内容:")
                print(code)
                
            # 清理创建的文件
            os.remove(filename)
        except Exception as e:
            print(f"读取文件时出错: {e}")
    else:
        print("代码生成或保存失败")


def example3_custom_url():
    """自定义URL示例"""
    print("\n=== 自定义URL示例 ===")
    
    # 创建新的客户端实例并指定自定义URL
    from th_cnd_utils import WebAppClient
    client = WebAppClient("http://127.0.0.1:5000")  # 使用默认URL
    
    print(f"当前基础URL: {client.get_base_url()}")
    
    # 生成代码
    task_description = "创建一个简单的Python脚本"
    code = client.generate_code(task_description)
    
    if code:
        print("代码生成成功!")
        print("生成的代码预览:")
        print(code[:200] + "..." if len(code) > 200 else code)
    else:
        print("代码生成失败")
    
    # 关闭会话
    client.close()


def main():
    """主函数"""
    print("WebAppClient 使用示例")
    print("=" * 50)
    
    # 运行示例
    example1_basic_usage()
    example2_download_code()
    example3_custom_url()
    
    print("\n所有示例运行完成!")


if __name__ == "__main__":
    main()