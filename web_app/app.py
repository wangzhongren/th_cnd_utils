from flask import Flask, render_template, jsonify, request
import os
from dotenv import load_dotenv
from openai import OpenAI

# 加载环境变量
load_dotenv()

app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')

# 初始化OpenAI客户端
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    base_url=os.getenv('OPENAI_BASE_URL')
)

# 读取工具库指南内容
def get_tool_guide():
    guide_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'UTILS_CALL_GUIDE.md')
    if os.path.exists(guide_path):
        with open(guide_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "工具库指南内容未找到"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/tool-guide')
def tool_guide():
    guide_content = get_tool_guide()
    return jsonify({'content': guide_content})

@app.route('/api/generate-code', methods=['POST'])
def generate_code():
    try:
        # 获取请求数据
        data = request.get_json()
        task_description = data.get('task_description', '')
        
        if not task_description.strip():
            return jsonify({'error': '任务描述不能为空'}), 400
        
        # 构建提示词
        tool_guide = get_tool_guide()
        prompt = f"""请使用我提供的工具库编写一个数据处理流水线：

【工具库说明】
{tool_guide}

【任务要求】
{task_description}

请确保包含适当的错误处理和资源清理。

请只返回可执行的Python代码，不需要任何解释或额外文本。
"""

        # 调用Qwen3大模型
        response = client.chat.completions.create(
            model="qwen3-14b",  # 指定使用Qwen3模型
            messages=[
                {"role": "system", "content": "你是一个Python编程专家，专门帮助用户生成基于特定工具库的数据处理代码。"},
                {"role": "user", "content": prompt}
            ],
            extra_body={"enable_thinking": False},
            stream=False,
            temperature=0.7,
            max_tokens=2048
        )
        
        # 提取生成的代码
        generated_code = response.choices[0].message.content
        
        return jsonify({'code': generated_code})
        
    except Exception as e:
        print(f"Error generating code: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)