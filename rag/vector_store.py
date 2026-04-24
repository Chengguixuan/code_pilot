import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict
import os
os.environ['TRANSFORMERS_OFFLINE'] = '1'
os.environ['HF_HUB_OFFLINE'] = '1'

class VectorStore:
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(
            name="codebase",
            embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name="all-MiniLM-L6-v2"
            )
        )
    
    def delete_collection(self):
        """删除整个集合（全量重建时使用）"""
        try:
            self.client.delete_collection("codebase")
            self.collection = self.client.get_or_create_collection(
                name="codebase",
                embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(
                    model_name="all-MiniLM-L6-v2"
                )
            )
            print("已删除并重建集合")
        except Exception as e:
            print(f"删除集合失败: {e}")
    
    def add_documents(self, chunks: List[Dict]):
        ids = []
        documents = []
        metadatas = []
        
        for i, chunk in enumerate(chunks):
            doc_id = f"{chunk['file_path']}_{chunk['function_name']}_{i}"
            doc_id = doc_id.replace('/', '_').replace('\\', '_')
            
            doc_text = f"函数名: {chunk['function_name']}\n代码:\n{chunk['code']}"
            if chunk['docstring']:
                doc_text += f"\n说明: {chunk['docstring']}"
            
            ids.append(doc_id)
            documents.append(doc_text)
            metadatas.append({
                "file_path": chunk['file_path'],
                "function_name": chunk['function_name'] or "",
                "code": chunk['code']
            })
        
        batch_size = 100
        for i in range(0, len(ids), batch_size):
            self.collection.add(
                ids=ids[i:i+batch_size],
                documents=documents[i:i+batch_size],
                metadatas=metadatas[i:i+batch_size]
            )
        
        print(f"已添加 {len(ids)} 个代码块")
    
    def search(self, query: str, k: int = 3) -> List[Dict]:
        results = self.collection.query(
            query_texts=[query],
            n_results=k
        )
        
        documents = []
        if results['documents'] and results['documents'][0]:
            for i, doc in enumerate(results['documents'][0]):
                metadata = results['metadatas'][0][i] if results['metadatas'] else {}
                documents.append({
                    "code": metadata.get("code", ""),
                    "file_path": metadata.get("file_path", ""),
                    "function_name": metadata.get("function_name", ""),
                    "content": doc
                })
        
        return documents

_store = None

def get_store():
    global _store
    if _store is None:
        _store = VectorStore()
    return _store