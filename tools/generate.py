from config import call_llm, to_openai_messages
from prompts.templates import get_messages


def generate_code(requirement: str) -> str:
    """
    根据需求生成代码
    
    Args:
        requirement: 需求描述
    
    Returns:
        生成的代码
    """
    if not requirement or not requirement.strip():
        return "错误：没有提供需求描述"
    
    langchain_messages = get_messages("generate", requirement=requirement)
    openai_messages = to_openai_messages(langchain_messages)
    result = call_llm(openai_messages, task="generate")
    
    return result


if __name__ == "__main__":
    test_requirement = "计算两个数的最大公约数（辗转相除法）"
    
    print("=" * 50)
    print("测试代码生成工具")
    print("=" * 50)
    print(f"需求: {test_requirement}")
    print("-" * 50)
    
    result = generate_code(test_requirement)
    print(f"生成的代码:\n{result}")