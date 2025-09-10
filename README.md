# AI-DO Utils (th_cnd_utils) - 将AI装进框架的笼子

[![PyPI](https://img.shields.io/pypi/v/th_cnd_utils)](https://pypi.org/project/th_cnd_utils/)
[![Python Version](https://img.shields.io/pypi/pyversions/th_cnd_utils)](https://pypi.org/project/th_cnd_utils/)
[![License](https://img.shields.io/pypi/l/th_cnd_utils)](https://github.com/your-org/th_cnd_utils/blob/main/LICENSE)

## 项目理念：将AI装进框架的笼子

在AI技术飞速发展的今天，我们面临着一个核心挑战：**如何让AI在可控、可预测的框架内发挥作用，而不是让AI完全主导我们的系统架构**。

AI-DO Utils (th_cnd_utils) 正是基于这一理念而诞生的工具库。我们相信，**最好的AI应用不是让AI决定一切，而是让AI在我们设计好的框架内，成为提升效率的强大助手**。

这正是"将AI装进框架的笼子"的核心理念——**让AI在笼中翱翔，而不是在笼外失控**。

### 我们的理念核心

1. **框架先行**：我们先构建稳定、可靠的软件框架和基础设施
2. **AI辅助**：在框架内，AI负责生成代码、处理数据、优化流程
3. **人工掌控**：开发者始终掌握最终决策权，AI只是强大的辅助工具
4. **标准化输出**：AI生成的内容必须符合预定义的接口和规范

## 项目组成

### 📦 th_cnd_utils (Python工具库)
位于 `th_cnd_utils/` 目录，是一个完整的Python包，包含各种数据存储和云服务工具。

### 🌐 web_app (Web服务端)
位于 `web_app/` 目录，提供Web界面和API接口，用于调用大模型生成代码。

### 🖥️ tkinter_app (桌面应用)
位于 `tkinter_app/` 目录，提供本地桌面界面，可以直接运行生成的代码。

## 功能架构

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   开发者/用户   │    │    Web服务端     │    │   大模型API     │
│                 │◄──►│                  │◄──►│                 │
│  (掌控决策权)   │    │  (框架化接口)    │    │ (AI代码生成)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         ▲                         ▲
         │                         │
         ▼                         ▼
┌─────────────────┐    ┌──────────────────┐
│   桌面应用端    │    │   Python工具库   │
│                 │    │                  │
│ (本地代码执行)  │    │ (标准化工具集)   │
└─────────────────┘    └──────────────────┘
```

## 📦 th_cnd_utils 工具库

### 核心工具集

- **数据库工具**：MySQL、Redis、SQLite、RabbitMQ
- **云服务集成**：阿里云OSS、阿里云OTS
- **AI代码生成客户端**：通过Web服务接口调用大模型生成代码
- **专用客户端**：李龙平台加密接口客户端
- **Web框架工具**：Flask工具类，简化API开发

### 🚀 快速开始

```python
# 安装
pip install th_cnd_utils

# 基本使用
from th_cnd_utils import mysql_util, redis_util

# 数据库操作
mysql_util.connect()
users = mysql_util.execute_query('SELECT * FROM users WHERE age > %s', (18,))

# 缓存操作
redis_util.connect()
redis_util.set('username', '张三', 3600)
```

### 🧠 AI辅助开发

```python
# 通过WebApp接口调用AI生成代码
from th_cnd_utils import web_app_client

task_description = """
1. 从OSS的raw_data/目录下读取最新的CSV文件
2. 将文件内容解析后批量插入到MySQL的raw_records表中
"""

# AI生成代码，但开发者掌控最终使用
generated_code = web_app_client.generate_code(task_description)
```

## 🌐 web_app 服务端

Web应用提供图形化界面和API接口，用于调用大模型生成代码。

### 功能特性

1. **图形化任务描述**：直观的任务要求输入界面
2. **工具库说明展示**：实时查看可用工具和使用方法
3. **代码生成接口**：通过API调用大模型生成Python代码
4. **代码预览和管理**：查看、保存、下载生成的代码

### 启动服务

```bash
cd web_app
pip install -r requirements.txt
python app.py
```

访问 `http://127.0.0.1:5000` 使用Web界面。

### API接口

```bash
# 生成代码接口
POST /api/generate-code
{
  "task_description": "任务描述内容"
}
```

## 🖥️ tkinter_app 桌面应用

桌面应用提供本地界面，可以直接运行生成的代码。

### 功能特性

1. **本地化界面**：无需网络即可使用
2. **代码生成**：调用web_app服务生成代码
3. **代码执行**：直接在本地运行生成的Python代码
4. **文件管理**：保存、加载、复制代码

### 启动应用

```bash
python run_tkinter_app.py
```

## 🤖 AI集成模式

### 1. 代码生成服务架构
```
用户任务描述 → Web服务 → 大模型API → 生成代码 → 用户审核 → 本地执行
```

### 2. 标准化接口
所有AI生成的代码都遵循统一的接口规范，确保可预测性和可控性。

### 3. 框架化设计

#### 统一配置管理
```python
# 所有配置通过环境变量统一管理
from th_cnd_utils import config
mysql_host = config['mysql']['host']
```

#### 单例模式工具
```python
# 所有工具类采用单例模式，确保资源合理使用
from th_cnd_utils import mysql_util
mysql_util.connect()
```

#### 标准化异常处理
```python
# 统一的错误处理机制
try:
    result = mysql_util.execute_query("SELECT * FROM users")
except Exception as e:
    # 标准化错误处理
    handle_error(e)
```

## 使用场景

### 🎯 典型应用

1. **数据处理流水线**
   - AI生成数据ETL脚本
   - 框架确保数据一致性和安全性

2. **微服务开发**
   - AI生成API接口代码
   - 框架提供统一的服务治理

3. **报表系统**
   - AI生成数据分析脚本
   - 框架确保报表格式统一

## 核心价值

### 🔒 **可控性**
- AI在预定义的框架内工作
- 开发者掌握最终决策权
- 所有操作可审计、可回溯

### ⚡ **高效性**
- AI处理重复性编码工作
- 开发者专注于架构设计和业务逻辑
- 标准化组件快速组装

### 🛡️ **安全性**
- 统一的配置管理
- 标准化的安全实践
- 预防AI生成危险代码

### 🔄 **可维护性**
- 标准化接口设计
- 统一的错误处理
- 清晰的代码结构

## 项目结构

```
ai_do/
├── th_cnd_utils/         # Python工具库
│   ├── db/              # 数据库工具
│   ├── cloud/           # 云服务工具
│   ├── examples/        # 使用示例
│   ├── __init__.py      # 包初始化
│   ├── service_client.py # 专用客户端
│   ├── web_app_client.py # Web客户端
│   └── flask_util.py    # Web框架工具
├── web_app/             # Web服务端
│   ├── templates/       # HTML模板
│   ├── static/          # 静态资源
│   ├── app.py           # Flask应用
│   └── requirements.txt # 依赖文件
├── tkinter_app/         # 桌面应用
│   ├── modules/         # 功能模块
│   └── app.py           # 主应用
├── run_tkinter_app.py   # 桌面应用启动脚本
└── requirements.txt     # 项目依赖
```

## 安装和使用

### 安装Python工具库
```bash
pip install th_cnd_utils
```

### 启动Web服务
```bash
cd web_app
pip install -r requirements.txt
python app.py
```

### 启动桌面应用
```bash
python run_tkinter_app.py
```

### 环境配置
```bash
# 复制配置文件模板
cp .env.example .env
# 编辑 .env 文件，填写相应配置
```

## 开发指南

### 1. 工具库开发
```python
# 添加新的工具类到th_cnd_utils/
# 确保遵循单例模式和统一接口规范
```

### 2. Web服务扩展
```python
# 添加新的API接口到web_app/app.py
# 更新模板文件以支持新功能
```

### 3. 桌面应用增强
```python
# 在tkinter_app/modules/中添加新功能模块
```

## 贡献和社区

我们欢迎任何形式的贡献：

1. **功能增强**：添加新的工具类
2. **Bug修复**：改进现有功能
3. **文档完善**：补充使用示例
4. **理念讨论**：分享AI框架化应用的经验

## 许可证

本项目采用 MIT 许可证开源。

## 结语

AI-DO Utils 代表了我们对AI应用的一种思考：**不要让AI成为不可控的力量，而要让AI成为我们手中得力的工具**。通过框架化的设计，我们既享受AI带来的效率提升，又保持对系统的完全掌控。

这正是"将AI装进框架的笼子"的核心理念——**让AI在笼中翱翔，而不是在笼外失控**。
