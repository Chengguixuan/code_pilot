from config import call_llm, to_openai_messages
from prompts.templates import get_messages


def explain_code(code: str) -> str:
    """
    解释给定的代码
    
    Args:
        code: 代码字符串
    
    Returns:
        代码解释文本
    """
    if not code or not code.strip():
        return "错误：没有提供代码"
    
    langchain_messages = get_messages("explain", code=code)
    openai_messages = to_openai_messages(langchain_messages)
    result = call_llm(openai_messages, task="explain")
    
    return result


# ========== 测试 ==========
if __name__ == "__main__":
    test_code = """
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n-1)
"""
    
    print("=" * 50)
    print("测试代码解释工具")
    print("=" * 50)
    print(f"输入代码:\n{test_code}")
    print("-" * 50)
    
    result = explain_code(test_code)
    print(f"解释结果:\n{result}")