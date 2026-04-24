from config import call_llm, to_openai_messages
from prompts.templates import get_messages


def review_code(code: str) -> str:
    """
    评审给定的代码
    
    Args:
        code: 代码字符串
    
    Returns:
        代码评审意见
    """
    if not code or not code.strip():
        return "错误：没有提供代码"
    
    langchain_messages = get_messages("review", code=code)
    openai_messages = to_openai_messages(langchain_messages)
    result = call_llm(openai_messages, task="review")
    
    return result


# ========== 测试 ==========
if __name__ == "__main__":
    test_code = """
def divide(a, b):
    return a / b

def get_user(id):
    users = {1: "Alice", 2: "Bob"}
    return users[id]
"""
    
    print("=" * 50)
    print("测试代码评审工具")
    print("=" * 50)
    print(f"输入代码:\n{test_code}")
    print("-" * 50)
    
    result = review_code(test_code)
    print(f"评审结果:\n{result}")