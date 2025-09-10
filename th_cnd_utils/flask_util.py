import os
import json
import logging
from functools import wraps
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class FlaskUtil:
    """Flask工具类，提供常用功能和装饰器"""
    
    def __init__(self, app=None):
        """
        初始化Flask工具类
        :param app: Flask应用实例
        """
        self.app = app
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """
        初始化应用
        :param app: Flask应用实例
        """
        self.app = app
        
        # 配置CORS
        CORS_ORIGIN = os.getenv('CORS_ORIGIN', '*')
        if CORS_ORIGIN != '*':
            CORS(app, origins=CORS_ORIGIN.split(','))
        else:
            CORS(app)
        
        # 配置日志
        self._configure_logging()
        
        # 注册错误处理
        self._register_error_handlers()
    
    def _configure_logging(self):
        """配置日志"""
        log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='%(asctime)s %(name)s %(levelname)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    
    def _register_error_handlers(self):
        """注册错误处理"""
        @self.app.errorhandler(404)
        def not_found(error):
            return self.error_response('资源未找到', 404)
        
        @self.app.errorhandler(500)
        def internal_error(error):
            return self.error_response('服务器内部错误', 500)
    
    def success_response(self, data=None, message="操作成功", code=200):
        """
        成功响应
        :param data: 返回数据
        :param message: 消息
        :param code: 状态码
        :return: JSON响应
        """
        response = {
            "code": code,
            "message": message,
            "data": data
        }
        return jsonify(response), code
    
    def error_response(self, message="操作失败", code=500, data=None):
        """
        错误响应
        :param message: 错误消息
        :param code: 状态码
        :param data: 返回数据
        :return: JSON响应
        """
        response = {
            "code": code,
            "message": message,
            "data": data
        }
        return jsonify(response), code
    
    def validate_json(self, required_fields=None):
        """
        验证JSON请求数据的装饰器
        :param required_fields: 必需字段列表
        """
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                # 检查是否为JSON请求
                if not request.is_json:
                    return self.error_response("请求必须为JSON格式", 400)
                
                # 获取JSON数据
                data = request.get_json()
                if data is None:
                    return self.error_response("无效的JSON数据", 400)
                
                # 检查必需字段
                if required_fields:
                    for field in required_fields:
                        if field not in data:
                            return self.error_response(f"缺少必需字段: {field}", 400)
                
                # 将数据添加到请求上下文
                request.json_data = data
                return f(*args, **kwargs)
            return decorated_function
        return decorator
    
    def require_params(self, required_params=None):
        """
        验证查询参数的装饰器
        :param required_params: 必需参数列表
        """
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                if required_params:
                    for param in required_params:
                        if param not in request.args:
                            return self.error_response(f"缺少必需参数: {param}", 400)
                return f(*args, **kwargs)
            return decorated_function
        return decorator
    
    def paginate(self, default_page=1, default_per_page=10, max_per_page=100):
        """
        分页装饰器
        :param default_page: 默认页码
        :param default_per_page: 默认每页数量
        :param max_per_page: 最大每页数量
        """
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                try:
                    page = int(request.args.get('page', default_page))
                    per_page = int(request.args.get('per_page', default_per_page))
                except ValueError:
                    return self.error_response("页码和每页数量必须为数字", 400)
                
                # 限制每页最大数量
                per_page = min(per_page, max_per_page)
                
                # 确保页码和每页数量为正数
                page = max(1, page)
                per_page = max(1, per_page)
                
                # 将分页信息添加到请求上下文
                request.pagination = {
                    'page': page,
                    'per_page': per_page,
                    'offset': (page - 1) * per_page
                }
                return f(*args, **kwargs)
            return decorated_function
        return decorator
    
    def api_route(self, rule, **options):
        """
        API路由装饰器，自动处理JSON响应
        :param rule: 路由规则
        :param options: 路由选项
        """
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                try:
                    result = f(*args, **kwargs)
                    # 如果返回的是元组，认为是 (data, message, code) 格式
                    if isinstance(result, tuple):
                        if len(result) == 3:
                            return self.success_response(result[0], result[1], result[2])
                        elif len(result) == 2:
                            return self.success_response(result[0], result[1])
                        else:
                            return self.success_response(result[0])
                    # 如果返回的是Response对象，直接返回
                    elif isinstance(result, Response):
                        return result
                    # 否则认为是数据
                    else:
                        return self.success_response(result)
                except Exception as e:
                    # 记录错误日志
                    logging.error(f"API调用出错: {str(e)}", exc_info=True)
                    return self.error_response(str(e), 500)
            
            # 注册路由
            if 'methods' not in options:
                options['methods'] = ['GET']
            self.app.add_url_rule(rule, f.__name__, decorated_function, **options)
            return decorated_function
        return decorator
    
    def get_client_ip(self):
        """
        获取客户端IP地址
        :return: 客户端IP地址
        """
        if request.headers.get('X-Forwarded-For'):
            return request.headers.get('X-Forwarded-For').split(',')[0]
        elif request.headers.get('X-Real-IP'):
            return request.headers.get('X-Real-IP')
        else:
            return request.remote_addr
    
    def get_request_id(self):
        """
        获取请求ID（如果有的话）
        :return: 请求ID
        """
        return request.headers.get('X-Request-ID', None)
    
    def cors_headers(self, response):
        """
        添加CORS头部
        :param response: 响应对象
        :return: 响应对象
        """
        response.headers['Access-Control-Allow-Origin'] = os.getenv('CORS_ORIGIN', '*')
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
        return response

# 创建全局实例
flask_util = FlaskUtil()