import ast
from typing import List, Dict

def extract_functions(code: str, file_path: str) -> List[Dict]:
    """
    使用 AST 提取 Python 文件中的所有函数
    
    Returns:
        [{"file_path": "...", "function_name": "...", "code": "...", "docstring": "..."}]
    """
    functions = []
    
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # 获取函数源代码
                try:
                    function_code = ast.unparse(node)
                except AttributeError:
                    # Python 3.8 以下没有 ast.unparse，用原始代码片段
                    function_code = f"def {node.name}(...): ..."
                
                docstring = ast.get_docstring(node) or ""
                
                functions.append({
                    "file_path": file_path,
                    "function_name": node.name,
                    "code": function_code,
                    "docstring": docstring
                })
    except SyntaxError:
        # 语法错误，无法解析，返回整个文件作为一个块
        functions.append({
            "file_path": file_path,
            "function_name": None,
            "code": code,
            "docstring": ""
        })
    
    return functions


def split_codebase(documents: List[Dict]) -> List[Dict]:
    """
    将代码库分割成函数级别的块
    """
    chunks = []
    
    for doc in documents:
        functions = extract_functions(doc["content"], doc["file_path"])
        chunks.extend(functions)
    
    return chunks