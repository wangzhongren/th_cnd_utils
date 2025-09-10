document.addEventListener('DOMContentLoaded', function() {
    const generateBtn = document.getElementById('generate-btn');
    const codeOutput = document.getElementById('code-output');
    const copyBtn = document.getElementById('copy-btn');
    const downloadBtn = document.getElementById('download-btn');
    const taskDescription = document.getElementById('task-description');
    const toolGuide = document.getElementById('tool-guide');

    // 页面加载时获取工具库指南
    fetch('/api/tool-guide')
        .then(response => response.json())
        .then(data => {
            toolGuide.textContent = data.content;
        })
        .catch(error => {
            console.error('Error loading tool guide:', error);
            toolGuide.textContent = '加载工具库说明失败';
        });

    // 生成代码功能
    generateBtn.addEventListener('click', async function() {
        try {
            const taskDesc = taskDescription.value;
            
            if (!taskDesc.trim()) {
                alert('请输入任务描述');
                return;
            }
            
            codeOutput.value = '# 正在生成代码，请稍候...';
            
            const response = await fetch('/api/generate-code', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    task_description: taskDesc
                })
            });

            if (response.ok) {
                const data = await response.json();
                codeOutput.value = data.code || '# 生成失败，请重试';
            } else {
                codeOutput.value = '# 生成失败，请重试';
            }
        } catch (error) {
            console.error('Error:', error);
            codeOutput.value = '# 生成失败：' + error.message;
        }
    });

    // 复制代码功能
    copyBtn.addEventListener('click', function() {
        codeOutput.select();
        document.execCommand('copy');
        alert('代码已复制到剪贴板！');
    });

    // 下载代码功能
    downloadBtn.addEventListener('click', function() {
        const code = codeOutput.value;
        const blob = new Blob([code], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'data_pipeline.py';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    });
});