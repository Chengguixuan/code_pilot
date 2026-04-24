from langchain.tools import tool
from .explain import explain_code as explain_code_impl
from .generate import generate_code as generate_code_impl
from .review import review_code as review_code_impl


@tool
def explain_code(code: str) -> str:
    """解释给定的代码片段。当用户想理解代码的功能、逻辑时使用此工具。"""
    return explain_code_impl(code)


@tool
def generate_code(requirement: str) -> str:
    """根据需求生成代码。当用户想要写代码、实现功能时使用此工具。"""
    return generate_code_impl(requirement)


@tool
def review_code(code: str) -> str:
    """评审给定的代码片段。当用户想检查代码质量、找出问题时使用此工具。"""
    return review_code_impl(code)


# 导出工具列表供 Agent 使用
__all__ = ["tools"]

tools = [explain_code, generate_code, review_code]