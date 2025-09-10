import os
from openai import OpenAI
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class CodeGenerator:
    def __init__(self):
        if not os.getenv('OPENAI_API_KEY'):
            raise ValueError("请在.env文件中设置OPENAI_API_KEY")
        # 初始化OpenAI客户端
        self.client = OpenAI(
            api_key=os.getenv('OPENAI_API_KEY'),
            base_url=os.getenv('OPENAI_BASE_URL', 'https://dashscope.aliyuncs.com/compatible-mode/v1')
        )
        
        # 检查API密钥
        
    
    def generate(self, task_description):
        """
        使用Qwen3大模型生成代码
        :param task_description: 任务描述
        :return: 生成的代码
        """
        try:
            # 获取工具库说明
            tool_guide = self._get_tool_guide()
            
            # 构建提示词
            prompt = f"""请使用我提供的工具库编写一个数据处理流水线：

【工具库说明】
{tool_guide}

【任务要求】
{task_description}

请确保包含适当的错误处理和资源清理。

请只返回可执行的Python代码，不需要任何解释或额外文本。
"""

            # 调用Qwen3大模型
            response = self.client.chat.completions.create(
                model="qwen3-14b",  # 指定使用Qwen3模型
                messages=[
                    {"role": "system", "content": "你是一个Python编程专家，专门帮助用户生成基于特定工具库的数据处理代码。"},
                    {"role": "user", "content": prompt}
                ],
                extra_body={"enable_thinking": False},
                stream=False,
                temperature=0.1,
                max_tokens=2048
            )
            
            # 提取生成的代码
            generated_code = response.choices[0].message.content
            return generated_code
            
        except Exception as e:
            raise Exception(f"代码生成失败: {str(e)}")
    
    def _get_tool_guide(self):
        """获取工具库说明"""
        try:
            guide_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'UTILS_CALL_GUIDE.md')
            if os.path.exists(guide_path):
                with open(guide_path, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                return "工具库说明文件未找到"
        except Exception as e:
            return f"加载工具库说明失败: {str(e)}"