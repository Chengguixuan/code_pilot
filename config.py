from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()


# ========== API配置 ==========
API_KEY = os.environ.get("DEEPSEEK_API_KEY")
BASE_URL = "https://api.deepseek.com"
MODEL_NAME = "deepseek-chat"

if not API_KEY:
    raise ValueError("请设置环境变量 DEEPSEEK_API_KEY")

os.environ["OPENAI_API_KEY"] = API_KEY
os.environ["OPENAI_BASE_URL"] = BASE_URL

# ========== 模型参数默认值 ==========
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 1024

# 不同任务的推荐参数
TASK_CONFIG = {
    "explain": {"temperature": 0.3, "max_tokens": 1024},   # 代码解释：低温度，稳定
    "generate": {"temperature": 0.7, "max_tokens": 2048},  # 代码生成：中等温度，有创造性
    "review": {"temperature": 0.2, "max_tokens": 2048},    # 代码评审：低温度，严谨
    "agent": {"temperature": 0.1, "max_tokens": 512},      # 代理判断：低温度，严格
}

# ========== 初始化客户端 ==========
client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
    timeout=60.0,
    max_retries=1
)

# ========== 通用调用函数 ==========
def call_llm(messages, task="explain"):
    """
    统一调用LLM的函数
    - messages: 对话消息列表
    - task: 任务类型 (explain/generate/review/agent)
    """
    config = TASK_CONFIG.get(task, DEFAULT_TEMPERATURE)
    
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=config["temperature"],
        max_tokens=config["max_tokens"],
        timeout=60
    )
    
    return response.choices[0].message.content


def to_openai_messages(langchain_messages):
    """将 LangChain 消息转换为 OpenAI 格式"""
    result = []
    for msg in langchain_messages:
        role = msg.type
        if role == "human":
            role = "user"
        elif role == "ai":
            role = "assistant"
        result.append({"role": role, "content": msg.content})
    return result

# ========== 简单测试 ==========
if __name__ == "__main__":
    # 测试API是否正常
    test_messages = [{"role": "user", "content": "回复'OK'，只回复这一个词"}]
    result = call_llm(test_messages, task="explain")
    print(f"测试结果: {result}")