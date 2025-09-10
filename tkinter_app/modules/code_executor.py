import subprocess
import sys
import os
import tempfile


class CodeExecutor:
    def __init__(self):
        pass
    
    def execute(self, code, timeout=300):
        """
        执行Python代码
        :param code: 要执行的代码
        :param timeout: 超时时间（秒）
        :return: 执行结果字典
        """
        try:
            # 创建临时文件
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            # 在子进程中执行代码
            result = subprocess.run(
                [sys.executable, temp_file],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=os.path.dirname(os.path.abspath(__file__))
            )
            
            # 删除临时文件
            os.unlink(temp_file)
            
            return {
                'success': True,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
            
        except subprocess.TimeoutExpired:
            # 删除临时文件
            if 'temp_file' in locals():
                os.unlink(temp_file)
                
            return {
                'success': False,
                'error': f'代码执行超时（超过{timeout}秒）'
            }
            
        except Exception as e:
            # 删除临时文件
            if 'temp_file' in locals():
                os.unlink(temp_file)
                
            return {
                'success': False,
                'error': f'执行代码时出错: {str(e)}'
            }