import requests
import json
import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class WebAppClient:
    """Web应用程序客户端，用于调用web_app接口生成和下载代码"""
    
    def __init__(self, base_url: str = None):
        """
        初始化WebApp客户端
        :param base_url: web_app服务的基础URL，如果不提供则从环境变量读取
        """
        if base_url:
            self.base_url = base_url.rstrip('/')
        else:
            # 从环境变量读取，如果没有则使用默认值
            self.base_url = os.getenv('WEB_APP_BASE_URL', 'http://127.0.0.1:5000').rstrip('/')
        
        self.session = requests.Session()
    
    def generate_code(self, task_description: str) -> Optional[str]:
        """
        调用web_app接口生成代码
        :param task_description: 任务描述
        :return: 生成的代码，如果失败返回None
        """
        try:
            url = f"{self.base_url}/api/generate-code"
            payload = {
                "task_description": task_description
            }
            
            response = self.session.post(
                url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=300  # 5分钟超时
            )
            
            # 检查响应状态
            response.raise_for_status()
            
            # 解析响应
            result = response.json()
            
            # 检查是否有错误
            if "error" in result:
                print(f"代码生成错误: {result['error']}")
                return None
            
            # 返回生成的代码
            if "code" in result:
                return result["code"]
            else:
                print("响应中没有找到代码")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"请求错误: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
            return None
        except Exception as e:
            print(f"生成代码时发生未知错误: {e}")
            return None
    
    def download_code(self, task_description: str, save_path: str) -> bool:
        """
        生成代码并保存到文件
        :param task_description: 任务描述
        :param save_path: 保存路径
        :return: 是否成功
        """
        try:
            # 生成代码
            code = self.generate_code(task_description)
            if code is None:
                return False
            
            # 保存到文件
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(code)
            
            print(f"代码已保存到: {save_path}")
            return True
            
        except Exception as e:
            print(f"保存代码时发生错误: {e}")
            return False
    
    def set_base_url(self, base_url: str):
        """
        设置基础URL
        :param base_url: 新的基础URL
        """
        self.base_url = base_url.rstrip('/')
    
    def get_base_url(self) -> str:
        """
        获取当前基础URL
        :return: 当前基础URL
        """
        return self.base_url
    
    def close(self):
        """
        关闭会话
        """
        self.session.close()


# 创建全局实例
web_app_client = WebAppClient()