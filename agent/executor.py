from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from config import API_KEY, BASE_URL, MODEL_NAME
from tools.tool_definitions import tools

# 初始化 LLM
llm = ChatOpenAI(
    model=MODEL_NAME,
    api_key=API_KEY,
    base_url=BASE_URL,
    temperature=0.1,
)

# 对话记忆
checkpointer = MemorySaver()

# 创建 Agent
_agent = None

def get_agent():
    global _agent
    if _agent is None:
        _agent = create_agent(
            model=llm,
            tools=tools,
            checkpointer=checkpointer,
            system_prompt="你是 CodePilot，一个智能代码助手。根据用户问题选择合适的工具：解释代码、生成代码或评审代码。",
        )
    return _agent

# 会话 ID
SESSION_ID = "code_pilot_session"

def run_agent(user_input: str) -> str:
    """运行 Agent，返回最终回答"""
    agent = get_agent()
    
    # 通过 config 指定 thread_id 来维持对话记忆
    config = {"configurable": {"thread_id": SESSION_ID}}
    
    # 输入格式必须是 {"messages": [{"role": "user", "content": "..."}]}
    response = agent.invoke(
        {"messages": [{"role": "user", "content": user_input}]},
        config=config
    )
    
    # 提取最后一条 AI 消息作为答案
    messages = response.get("messages", [])
    for msg in reversed(messages):
        if msg.type == "ai":
            return msg.content
    
    return "无法获取回答"