import hashlib
import json
import time
from urllib.parse import urlencode
import requests


class ServiceClient:
    def __init__(self, appid, appkey, url_prefix=None):
        """
        初始化 API 客户端
        :param appid: 应用ID
        :param appkey: 应用密钥
        :param url_prefix: URL前缀(可选)
        """
        self.appid = appid
        self.appkey = appkey
        self.url_prefix = url_prefix or ""  # 默认为空字符串

    def exec(self, url, obj_data, timeout=20000):
        """
        调用远程接口
        :param url: 接口地址
        :param obj_data: 要发送的数据对象(会自动转为JSON)
        :param timeout: 超时时间(毫秒，默认20秒)
        :return: 响应字典
        """
        # 将数据对象转为JSON字符串
        data = json.dumps(obj_data)
        # 生成13位时间戳(毫秒)
        stamp = str(int(time.time() * 1000))  
        
        # 生成签名(MD5(appid + appkey + data + stamp))
        sign_str = f"{self.appid}{self.appkey}{data}{stamp}"
        password = hashlib.md5(sign_str.encode('utf-8')).hexdigest()

        # 基础请求参数
        base_params = {
            'appid': self.appid,
            'stamp': stamp,
            'password': password
        }

        try:
            if len(data) > 1024 * 1024:  # 数据大于1MB时
                # 使用JSON格式发送，参数放在URL中
                full_url = f"{self.url_prefix}{url}?{urlencode(base_params)}"
                
                response = requests.post(
                    full_url,
                    data=data.encode('utf-8'),
                    headers={'Content-Type': 'application/json'},
                    timeout=timeout/1000,  # 转为秒
                    verify=False  # 跳过SSL验证
                )
            else:  # 小数据使用表单格式
                full_url = f"{self.url_prefix}{url}"
                form_data = base_params.copy()
                form_data['data'] = data  # 添加数据到表单
                
                response = requests.post(
                    full_url,
                    data=form_data,
                    timeout=timeout/1000,
                    verify=False
                )

            # 检查HTTP状态码
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            return {
                "code": 101,
                "content": f"请求失败: {str(e)}"
            }
        except Exception as e:
            return {
                "code": 102,
                "content": f"处理错误: {str(e)}"
            }