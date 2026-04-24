from agent import run_agent
from rag import index_codebase, search_code, is_indexed
import os

def load_codebase():
    """加载代码库（用户主动触发）"""
    path = input("请输入代码库路径: ").strip()
    if os.path.exists(path):
        index_codebase(path)
        print("✅ 代码库加载完成！")
    else:
        print("❌ 路径不存在")

def chat_with_rag(user_input: str) -> str:
    """根据是否有代码库，决定是否检索"""
    if is_indexed():
        # 有代码库：先检索相关代码
        results = search_code(user_input, k=3)
        if results:
            context = "\n\n【相关代码】\n"
            for r in results:
                context += f"\n📁 {r['file_path']}\n```python\n{r['code']}\n```\n"
            enhanced_input = f"{context}\n\n【用户问题】\n{user_input}"
            return run_agent(enhanced_input)
    
    # 无代码库或没检索到：直接提问
    return run_agent(user_input)

def main():
    print("=" * 50)
    print("CodePilot - 智能代码辅助工具")
    print("=" * 50)
    
    while True:
        print("\n请选择：")
        print("1. 直接提问")
        print("2. 加载代码库")
        print("0. 退出")
        
        choice = input("\n请输入 (0-2): ").strip()
        
        if choice == "0":
            print("再见！")
            break
        elif choice == "2":
            load_codebase()
        elif choice == "1":
            status = "✅ 已启用" if is_indexed() else "❌ 未启用"
            print(f"\n[RAG 状态: {status}]")
            user_input = input("你: ").strip()
            if user_input.lower() in ["quit", "exit"]:
                break
            result = chat_with_rag(user_input)
            print(f"\n🤖: {result}")
        else:
            print("无效选择")

if __name__ == "__main__":
    main()