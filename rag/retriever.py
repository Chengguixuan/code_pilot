from typing import List, Dict
from .loader import load_codebase
from .splitter import split_codebase
from .vector_store import get_store

def index_codebase(codebase_path: str):
    print(f"正在加载代码库: {codebase_path}")
    documents = load_codebase(codebase_path)
    print(f"加载了 {len(documents)} 个文件")
    
    if not documents:
        print("没有找到代码文件")
        return
    
    print("正在分割代码...")
    chunks = split_codebase(documents)
    print(f"分割成 {len(chunks)} 个代码块")
    
    print("正在创建向量索引...")
    store = get_store()
    store.delete_collection()
    store.add_documents(chunks)
    print("索引完成！")

def search_code(query: str, k: int = 3) -> List[Dict]:
    if not query or not query.strip():
        return []
    try:
        store = get_store()
        return store.search(query, k)
    except Exception as e:
        print(f"检索失败: {e}")
        return []