from langchain_core.prompts import ChatPromptTemplate

# ========== 不同任务的内容配置 ==========
TASK_CONTENT = {
    "explain": {
        "system": "你是一个代码解释专家。用简洁的中文分点解释代码的功能、逻辑。",
        "user": "请解释以下代码：\n\n```python\n{code}\n```"
    },
    "generate": {
        "system": "你是一个代码生成专家。只输出代码，不要解释。包含必要的import和注释。",
        "user": "请根据以下需求生成代码：\n\n{requirement}"
    },
    "review": {
        "system": "你是一个代码评审专家。指出代码的问题和改进建议。",
        "user": "请评审以下代码：\n\n```python\n{code}\n```"
    },
    "agent": {
        "system": "",  # agent 不需要 system 提示词
        "user": "判断用户意图，只输出一个词：explain、generate 或 review\n\n用户输入：{input}"
    }
}

# ========== 一个通用模板 ==========
base_template = ChatPromptTemplate.from_messages([
    ("system", "{system_content}"),
    ("user", "{user_content}")
])

# ========== 一个格式化函数 ==========
def get_messages(task: str, **kwargs):
    """根据任务类型和参数，返回格式化后的消息列表"""
    content = TASK_CONTENT[task]
    return base_template.format_messages(
        system_content=content["system"],
        user_content=content["user"].format(**kwargs)
    )