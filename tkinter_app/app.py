import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import os
import sys
from dotenv import load_dotenv

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.ui import CodeGeneratorUI
from modules.code_generator import CodeGenerator
from modules.code_executor import CodeExecutor

# 加载环境变量
load_dotenv()


class CodeGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("数据处理流水线代码生成器")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # 创建主框架
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建代码生成器
        self.code_generator = CodeGenerator()
        
        # 创建代码执行器
        self.code_executor = CodeExecutor()
        
        # 创建UI界面
        self.ui = CodeGeneratorUI(self.main_frame, self)
        
        # 绑定关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def generate_code(self):
        """生成代码"""
        # 获取任务描述
        task_description = self.ui.get_task_description()
        if not task_description.strip():
            messagebox.showwarning("警告", "请输入任务描述")
            return
        
        # 在新线程中生成代码以避免阻塞UI
        thread = threading.Thread(target=self._generate_code_thread, args=(task_description,))
        thread.daemon = True
        thread.start()
    
    def _generate_code_thread(self, task_description):
        """在新线程中生成代码"""
        try:
            # 更新UI状态
            self.ui.update_status("正在生成代码，请稍候...")
            
            # 生成代码
            generated_code = self.code_generator.generate(task_description)
            
            # 更新UI
            self.ui.update_code_display(generated_code)
            self.ui.update_status("代码生成完成")
            
        except Exception as e:
            error_msg = f"# 代码生成失败: {str(e)}"
            self.ui.update_code_display(error_msg)
            self.ui.update_status("代码生成失败")
    
    def run_code(self):
        """运行代码"""
        code = self.ui.get_code()
        if not code.strip() or code.startswith("#"):
            messagebox.showwarning("警告", "没有可运行的有效代码")
            return
        
        # 确认运行
        if not messagebox.askyesno("确认运行", "确定要运行这段代码吗？\n\n注意：请确保代码安全可靠后再运行。"):
            return
        
        # 在新线程中运行代码以避免阻塞UI
        thread = threading.Thread(target=self._run_code_thread, args=(code,))
        thread.daemon = True
        thread.start()
    
    def _run_code_thread(self, code):
        """在新线程中运行代码"""
        try:
            # 更新UI状态
            self.ui.update_status("正在运行代码...")
            
            # 运行代码
            result = self.code_executor.execute(code)
            
            # 更新UI输出
            if result['success']:
                output = f"执行结果:\n\n标准输出:\n{result['stdout']}\n\n标准错误:\n{result['stderr']}\n\n返回码: {result['returncode']}"
            else:
                output = f"执行错误:\n{result['error']}"
            
            self.ui.update_output(output)
            self.ui.update_status("代码执行完成")
            
        except Exception as e:
            error_msg = f"执行错误: {str(e)}"
            self.ui.update_output(error_msg)
            self.ui.update_status("代码执行失败")
    
    def save_code(self):
        """保存代码"""
        code = self.ui.get_code()
        if not code.strip():
            messagebox.showwarning("警告", "没有可保存的代码")
            return
        
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".py",
                filetypes=[("Python文件", "*.py"), ("所有文件", "*.*")],
                title="保存代码"
            )
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(code)
                messagebox.showinfo("保存成功", f"代码已保存到:\n{file_path}")
        except Exception as e:
            messagebox.showerror("保存失败", f"保存代码时出错:\n{str(e)}")
    
    def load_code(self):
        """加载代码"""
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("Python文件", "*.py"), ("所有文件", "*.*")],
                title="加载代码"
            )
            if file_path:
                with open(file_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                self.ui.update_code_display(code)
                messagebox.showinfo("加载成功", "代码已加载")
        except Exception as e:
            messagebox.showerror("加载失败", f"加载代码时出错:\n{str(e)}")
    
    def copy_code(self):
        """复制代码到剪贴板"""
        code = self.ui.get_code()
        if not code.strip():
            messagebox.showwarning("警告", "没有可复制的代码")
            return
        
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(code)
            self.root.update()
            messagebox.showinfo("复制成功", "代码已复制到剪贴板")
        except Exception as e:
            messagebox.showerror("复制失败", f"复制代码时出错:\n{str(e)}")
    
    def clear_all(self):
        """清空所有内容"""
        if messagebox.askyesno("确认清空", "确定要清空所有内容吗？"):
            self.ui.clear_all()
            self.ui.update_status("已清空")
    
    def on_closing(self):
        """应用关闭事件"""
        if messagebox.askokcancel("退出", "确定要退出代码生成器吗？"):
            self.root.destroy()


def main():
    root = tk.Tk()
    app = CodeGeneratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()