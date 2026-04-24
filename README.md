# 🤖 CodePilot - 智能代码辅助工具

基于大模型的代码助手，支持代码解释、代码生成、代码评审 + RAG 代码库问答。

## ✨ 功能特性

| 功能 | 说明 |
|------|------|
| 🔍 代码解释 | 输入代码，输出自然语言解释 |
| ⚡ 代码生成 | 输入需求，输出代码实现 |
| 📝 代码评审 | 输入代码，输出优化建议 |
| 📚 RAG 代码库问答 | 上传代码库，基于代码库内容回答问题 |
| 🧠 Agent 智能调度 | 自动判断用户意图，选择合适的工具 |

## 🛠 技术栈

- Python 3.12
- LangChain + LangGraph - Agent 框架
- DeepSeek API - 大模型
- ChromaDB - 向量数据库
- Sentence-Transformers - 本地 Embedding（离线模式）
- Streamlit - Web 界面
- python-dotenv - 环境变量管理

## 📁 项目结构
code_pilot/
├── config.py # API 配置（读取 .env）
├── prompts/
│ └── templates.py # 提示词模板
├── tools/
│ ├── explain.py # 代码解释工具
│ ├── generate.py # 代码生成工具
│ ├── review.py # 代码评审工具
│ ├── agent.py # 意图判断
│ └── tool_definitions.py
├── agent/
│ └── executor.py # Agent 执行器
├── rag/
│ ├── loader.py # 代码加载
│ ├── splitter.py # AST 函数分割
│ ├── vector_store.py # ChromaDB 存储与检索
│ └── retriever.py # 索引与检索入口
├── main.py # 命令行版入口
├── web/
│ └── app.py # Streamlit Web 界面
├── .env # 环境变量（API Key，不提交）
├── .gitignore
├── requirements.txt
└── README.md

## 🚀 快速开始
### 1. 克隆项目
```
git clone https://github.com/chengguixuan/code_pilot.git
cd code_pilot

2. 安装依赖
pip install -r requirements.txt

3. 配置 API Key
在项目根目录创建 .env 文件：
DEEPSEEK_API_KEY=your_deepseek_api_key_here
获取 API Key：https://platform.deepseek.com/

4. 首次运行（下载 Embedding 模型）
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
等待模型下载完成（约 90MB，仅首次需要）。

5. 运行
命令行版：
python main.py
Web 版：
streamlit run web/app.py
浏览器自动打开 http://localhost:8501

📸 效果展示
代码生成
用户：写一个快排函数

AI：
def quick_sort(arr):
if len(arr) <= 1:
return arr
pivot = arr[0]
left = [x for x in arr[1:] if x <= pivot]
right = [x for x in arr[1:] if x > pivot]
return quick_sort(left) + [pivot] + quick_sort(right)

代码解释
用户：解释一下这段代码 def add(a,b): return a+b

AI：这是一个加法函数，接收两个参数 a 和 b，返回它们的和。

代码评审
用户：这段代码有什么问题 def divide(a,b): return a/b

AI：存在除零风险，当 b=0 时会抛出 ZeroDivisionError，建议增加参数校验。

📌 离线模式
项目默认启用 HuggingFace 离线模式（HF_HUB_OFFLINE=1），Embedding 模型首次下载后完全离线运行，不依赖网络。

🔧 环境变量
变量	说明	必填
DEEPSEEK_API_KEY	DeepSeek API 密钥	是

📄 License
MIT