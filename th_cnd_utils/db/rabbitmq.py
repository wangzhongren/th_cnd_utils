import pika
import os
import json
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class RabbitMQUtil:
    _instance = None
    _connection = None
    _channel = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RabbitMQUtil, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.host = os.getenv('RABBITMQ_HOST', 'localhost')
            self.port = int(os.getenv('RABBITMQ_PORT', 5672))
            self.user = os.getenv('RABBITMQ_USER', 'guest')
            self.password = os.getenv('RABBITMQ_PASSWORD', 'guest')
            self.vhost = os.getenv('RABBITMQ_VHOST', '/')
    
    def connect(self):
        """建立 RabbitMQ 连接"""
        try:
            if not self._connection or self._connection.is_closed:
                credentials = pika.PlainCredentials(self.user, self.password)
                parameters = pika.ConnectionParameters(
                    host=self.host,
                    port=self.port,
                    virtual_host=self.vhost,
                    credentials=credentials
                )
                self._connection = pika.BlockingConnection(parameters)
                self._channel = self._connection.channel()
                print("RabbitMQ 连接成功")
            return self._channel
        except Exception as e:
            print(f"RabbitMQ 连接失败: {e}")
            raise e
    
    def send_message(self, queue, message):
        """发送消息到队列"""
        try:
            channel = self.connect()
            channel.queue_declare(queue=queue, durable=True)
            
            # 如果消息是字典，转换为 JSON 字符串
            if isinstance(message, dict):
                message = json.dumps(message)
            
            channel.basic_publish(
                exchange='',
                routing_key=queue,
                body=message,
                properties=pika.BasicProperties(
                    delivery_mode=2,  # 消息持久化
                )
            )
            print(f"消息已发送到队列 '{queue}'")
        except Exception as e:
            print(f"发送消息失败: {e}")
            raise e
    
    def consume_messages(self, queue, callback, auto_ack=False):
        """消费队列中的消息"""
        try:
            channel = self.connect()
            channel.queue_declare(queue=queue, durable=True)
            
            def wrapper(ch, method, properties, body):
                try:
                    # 将消息信息传递给回调函数，包括channel和method用于手动确认
                    message_info = {
                        'body': body.decode('utf-8'),
                        'channel': ch,
                        'method': method,
                        'properties': properties
                    }
                    callback(message_info)
                    
                    # 如果启用了自动确认，则自动确认消息
                    if auto_ack:
                        ch.basic_ack(delivery_tag=method.delivery_tag)
                except Exception as e:
                    print(f"处理消息失败: {e}")
                    # 如果启用了自动确认，则拒绝消息并重新入队
                    if auto_ack:
                        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
            
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue=queue, on_message_callback=wrapper, auto_ack=auto_ack)
            print(f"开始消费队列 '{queue}' 中的消息")
            channel.start_consuming()
        except Exception as e:
            print(f"消费消息失败: {e}")
            raise e
    
    def manual_ack(self, channel, delivery_tag):
        """手动确认消息"""
        try:
            channel.basic_ack(delivery_tag=delivery_tag)
            print(f"消息 {delivery_tag} 已手动确认")
        except Exception as e:
            print(f"手动确认消息失败: {e}")
            raise e
    
    def manual_nack(self, channel, delivery_tag, requeue=True):
        """手动拒绝消息"""
        try:
            channel.basic_nack(delivery_tag=delivery_tag, requeue=requeue)
            print(f"消息 {delivery_tag} 已手动拒绝")
        except Exception as e:
            print(f"手动拒绝消息失败: {e}")
            raise e
    
    def stop_consuming(self):
        """停止消费消息"""
        try:
            if self._channel:
                self._channel.stop_consuming()
                print("已停止消费消息")
        except Exception as e:
            print(f"停止消费消息失败: {e}")
            raise e
    
    def close(self):
        """关闭 RabbitMQ 连接"""
        if self._connection and not self._connection.is_closed:
            self._connection.close()
            print("RabbitMQ 连接已关闭")

# 创建单例实例
rabbitmq_util = RabbitMQUtil()