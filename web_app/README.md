# 数据处理流水线生成器

这是一个Web应用程序，用于生成基于工具库的数据处理流水线代码。

## 功能特点

- 左右布局界面：左侧显示任务要求和工具库说明，右侧显示生成的代码
- 支持动态输入任务描述
- 一键生成数据处理流水线代码
- 支持复制和下载生成的代码

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置API密钥

1. 编辑 `.env` 文件，填写您的阿里云API密钥：
   ```
   OPENAI_API_KEY=your-actual-api-key-here
   ```

2. 如果您使用的是阿里云百炼平台，请确保：
   - API密钥具有访问Qwen3模型的权限
   - 确认base_url正确设置为：`https://dashscope.aliyuncs.com/compatible-mode/v1`

## 运行应用

```bash
python app.py
```

应用将在 `http://127.0.0.1:5000` 上运行。

## 使用说明

1. 打开浏览器访问 `http://127.0.0.1:5000`
2. 在左侧文本区域输入您的任务描述
3. 查看工具库说明
4. 点击"生成代码"按钮生成数据处理流水线代码
5. 使用"复制代码"或"下载代码"按钮保存生成的代码

## 目录结构

```
web_app/
├── app.py                 # Flask应用入口
├── requirements.txt       # Python依赖
├── .env                  # 环境变量配置文件
├── README.md             # 项目说明文档
├── templates/            # HTML模板
│   └── index.html        # 主页面
└── static/               # 静态文件
    ├── css/              # 样式文件
    │   └── style.css     # 主样式
    └── js/               # JavaScript文件
        └── main.js       # 主脚本
```

## 注意事项

1. 确保在项目根目录中有 `UTILS_CALL_GUIDE.md` 文件，应用会从中读取工具库说明
2. 生成的代码需要根据实际环境进行调整
3. 在生产环境中，请修改 `app.run()` 的配置
4. 请妥善保管您的API密钥，不要将其提交到版本控制系统中