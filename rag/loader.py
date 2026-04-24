import os
from typing import List, Dict

def load_codebase(codebase_path: str, extensions: List[str] = None) -> List[Dict]:
    """
    加载整个代码库的所有文件
    
    Args:
        codebase_path: 代码库根目录
        extensions: 要加载的文件扩展名，默认 [".py"]
    
    Returns:
        [{"file_path": "xxx.py", "content": "代码内容"}]
    """
    if extensions is None:
        extensions = [".py"]
    
    documents = []
    
    for root, dirs, files in os.walk(codebase_path):
        # 跳过隐藏目录和缓存目录
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'venv', 'env']]
        
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    documents.append({
                        "file_path": file_path,
                        "content": content
                    })
                except Exception as e:
                    print(f"读取失败 {file_path}: {e}")
    
    return documents