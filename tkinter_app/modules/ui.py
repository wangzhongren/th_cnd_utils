import tkinter as tk
from tkinter import ttk, scrolledtext
import os


class CodeGeneratorUI:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.setup_ui()
    
    def setup_ui(self):
        """设置用户界面"""
        # 创建主布局框架
        self.create_layout_frames()
        
        # 创建任务描述区域（左侧面板）
        self.create_task_description_panel()
        
        # 创建代码显示区域（右侧面板）
        self.create_code_display_panel()
        
        # 创建控制按钮区域
        self.create_control_buttons()
        
        # 创建状态栏
        self.create_status_bar()
        
        # 初始化工具库说明
        self.load_tool_guide()
    
    def create_layout_frames(self):
        """创建布局框架"""
        # 创建左右分割窗口
        self.paned_window = ttk.PanedWindow(self.parent, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)
        
        # 左侧面板框架
        self.left_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(self.left_frame, weight=1)
        
        # 右侧面板框架
        self.right_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(self.right_frame, weight=1)
    
    def create_task_description_panel(self):
        """创建任务描述面板"""
        # 任务描述框架
        task_frame = ttk.LabelFrame(self.left_frame, text="任务要求", padding=10)
        task_frame.pack(fill=tk.BOTH, expand=True)
        
        # 任务描述文本框
        self.task_text = scrolledtext.ScrolledText(
            task_frame,
            wrap=tk.WORD,
            font=("Consolas", 10),
            height=15
        )
        self.task_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # 设置默认任务描述
        default_task = """1. 从OSS的raw_data/目录下读取最新的CSV文件
2. 将文件内容解析后批量插入到MySQL的raw_records表中
3. 对处理完成的文件，在OSS中移动到processed_data/目录
4. 记录处理日志到SQLite的process_logs表

请确保包含适当的错误处理和资源清理。"""
        self.task_text.insert(tk.END, default_task)
        
        # 工具库说明框架
        guide_frame = ttk.LabelFrame(self.left_frame, text="工具库说明", padding=10)
        guide_frame.pack(fill=tk.BOTH, expand=True)
        
        # 工具库说明文本框
        self.guide_text = scrolledtext.ScrolledText(
            guide_frame,
            wrap=tk.WORD,
            font=("Consolas", 9),
            state=tk.DISABLED,
            height=10
        )
        self.guide_text.pack(fill=tk.BOTH, expand=True)
    
    def create_code_display_panel(self):
        """创建代码显示面板"""
        # 代码显示框架
        code_frame = ttk.LabelFrame(self.right_frame, text="生成的代码", padding=10)
        code_frame.pack(fill=tk.BOTH, expand=True)
        
        # 代码显示文本框
        self.code_text = scrolledtext.ScrolledText(
            code_frame,
            wrap=tk.NONE,  # 不自动换行，允许水平滚动
            font=("Consolas", 10)
        )
        self.code_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # 设置默认代码
        self.code_text.insert(tk.END, "# 点击'生成代码'按钮来生成数据处理流水线代码")
        
        # 输出显示框架
        output_frame = ttk.LabelFrame(self.right_frame, text="运行输出", padding=10)
        output_frame.pack(fill=tk.BOTH, expand=True)
        
        # 输出显示文本框
        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            wrap=tk.WORD,
            font=("Consolas", 10),
            height=8
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
    
    def create_control_buttons(self):
        """创建控制按钮"""
        # 按钮框架
        button_frame = ttk.Frame(self.parent)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # 创建按钮样式
        button_style = ttk.Style()
        button_style.configure("Action.TButton", padding=6)
        
        # 第一行按钮
        row1_frame = ttk.Frame(button_frame)
        row1_frame.pack(fill=tk.X, pady=(0, 5))
        
        # 生成代码按钮
        self.generate_btn = ttk.Button(
            row1_frame,
            text="生成代码",
            command=self.app.generate_code,
            style="Action.TButton"
        )
        self.generate_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # 运行代码按钮
        self.run_btn = ttk.Button(
            row1_frame,
            text="运行代码",
            command=self.app.run_code,
            style="Action.TButton"
        )
        self.run_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # 第二行按钮
        row2_frame = ttk.Frame(button_frame)
        row2_frame.pack(fill=tk.X)
        
        # 保存代码按钮
        self.save_btn = ttk.Button(
            row2_frame,
            text="保存代码",
            command=self.app.save_code,
            style="Action.TButton"
        )
        self.save_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # 加载代码按钮
        self.load_btn = ttk.Button(
            row2_frame,
            text="加载代码",
            command=self.app.load_code,
            style="Action.TButton"
        )
        self.load_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # 复制代码按钮
        self.copy_btn = ttk.Button(
            row2_frame,
            text="复制代码",
            command=self.app.copy_code,
            style="Action.TButton"
        )
        self.copy_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # 清空按钮
        self.clear_btn = ttk.Button(
            row2_frame,
            text="清空",
            command=self.app.clear_all,
            style="Action.TButton"
        )
        self.clear_btn.pack(side=tk.LEFT, padx=(0, 5))
    
    def create_status_bar(self):
        """创建状态栏"""
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        
        status_bar = ttk.Label(
            self.parent,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            padding=5
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def load_tool_guide(self):
        """加载工具库说明"""
        try:
            # 尝试从项目根目录加载工具库说明
            guide_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'UTILS_CALL_GUIDE.md')
            if os.path.exists(guide_path):
                with open(guide_path, 'r', encoding='utf-8') as f:
                    guide_content = f.read()
                    self.guide_text.config(state=tk.NORMAL)
                    self.guide_text.delete(1.0, tk.END)
                    self.guide_text.insert(tk.END, guide_content)
                    self.guide_text.config(state=tk.DISABLED)
            else:
                self.guide_text.config(state=tk.NORMAL)
                self.guide_text.delete(1.0, tk.END)
                self.guide_text.insert(tk.END, "工具库说明文件未找到，请确保项目根目录有 UTILS_CALL_GUIDE.md 文件")
                self.guide_text.config(state=tk.DISABLED)
        except Exception as e:
            self.guide_text.config(state=tk.NORMAL)
            self.guide_text.delete(1.0, tk.END)
            self.guide_text.insert(tk.END, f"加载工具库说明失败: {str(e)}")
            self.guide_text.config(state=tk.DISABLED)
    
    def get_task_description(self):
        """获取任务描述"""
        return self.task_text.get(1.0, tk.END)
    
    def get_code(self):
        """获取代码"""
        return self.code_text.get(1.0, tk.END)
    
    def update_code_display(self, code):
        """更新代码显示"""
        self.code_text.delete(1.0, tk.END)
        self.code_text.insert(tk.END, code)
    
    def update_output(self, output):
        """更新输出显示"""
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, output)
    
    def update_status(self, message):
        """更新状态栏"""
        self.status_var.set(message)
        self.parent.update_idletasks()
    
    def clear_all(self):
        """清空所有内容"""
        self.task_text.delete(1.0, tk.END)
        self.code_text.delete(1.0, tk.END)
        self.output_text.delete(1.0, tk.END)
        self.code_text.insert(tk.END, "# 点击'生成代码'按钮来生成数据处理流水线代码")