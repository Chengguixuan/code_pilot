import streamlit as st
import sys
import os
import zipfile
import tempfile

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import run_agent
from rag import index_codebase, search_code, is_indexed

st.set_page_config(page_title="CodePilot", page_icon="🤖", layout="wide")

st.title("🤖 CodePilot - 智能代码辅助工具")
st.markdown("基于 DeepSeek 的代码助手，支持代码解释、生成、评审 + RAG 代码库问答")

# 侧边栏：代码库管理
with st.sidebar:
    st.header("📁 代码库管理")
    
    # 显示当前状态
    if is_indexed():
        st.success("✅ RAG 已启用")
    else:
        st.info("❌ RAG 未启用（上传代码库即可启用）")
    
    # 上传代码库
    uploaded_file = st.file_uploader("上传代码库 (ZIP 文件)", type=["zip"])
    
    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name
        
        extract_dir = tempfile.mkdtemp()
        with zipfile.ZipFile(tmp_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        
        with st.spinner("正在索引代码库..."):
            index_codebase(extract_dir)
        
        st.success("✅ 代码库加载完成！RAG 已启用")
        st.rerun()
    
    st.divider()
    st.caption("💡 提示：直接输入问题，Agent 会自动选择工具")
    st.caption("📌 支持：代码解释、代码生成、代码评审")

# 主界面：对话历史
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 用户输入
user_input = st.chat_input("输入你的问题...")

if user_input:
    # 显示用户消息
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # 构建最终输入（如果有 RAG）
    final_input = user_input
    if is_indexed():
        with st.spinner("正在检索代码库..."):
            results = search_code(user_input, k=3)
        if results:
            context = "\n\n【相关代码】\n"
            for r in results:
                context += f"\n📁 `{r['file_path']}`\n```python\n{r['code']}\n```\n"
            final_input = f"{context}\n\n【用户问题】\n{user_input}"
    
    # 调用 Agent
    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            response = run_agent(final_input)
        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
