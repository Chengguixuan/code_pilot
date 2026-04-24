from .retriever import index_codebase, search_code

def is_indexed() -> bool:
    """检查是否有已索引的代码库"""
    from .vector_store import get_store
    store = get_store()
    try:
        return store.collection.count() > 0
    except Exception:
        return False

__all__ = ["index_codebase", "search_code", "is_indexed"]