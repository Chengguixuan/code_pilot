from config import call_llm, to_openai_messages
from prompts.templates import get_messages


def decide_intent(user_input: str) -> str:
    """
    判断用户意图
    
    Returns:
        "explain" | "generate" | "review"
    """
    
    langchain_messages = get_messages("agent", input=user_input)
    openai_messages = to_openai_messages(langchain_messages)
    result = call_llm(openai_messages, task="agent")
    
    result = result.strip().lower()
    
    if result in ["explain", "generate", "review"]:
        return result
    
    return "explain"