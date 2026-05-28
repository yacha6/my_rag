# my_rag — RAG 知识库问答系统

基于 LangChain + DashScope（通义千问）+ FAISS 的轻量级 RAG 问答系统，支持对本地文档进行智能检索与问答。

## 功能特性

- 上传本地文本文件作为知识库，自动分块、向量化
- 基于语义检索（FAISS）召回相关内容片段
- 搭配大语言模型生成答案，支持流式输出
- 可选 Redis 缓存，相同问题直接返回历史答案
- 基于 Streamlit 的简洁 Web 交互界面

## 技术栈

| 组件 | 技术选型 |
|------|----------|
| UI 框架 | Streamlit |
| 向量存储 | FAISS (CPU) |
| 文本分块 | RecursiveCharacterTextSplitter |
| 嵌入模型 | DashScope text-embedding-v2 |
| 大语言模型 | Qwen3 (通义千问) |
| 缓存（可选） | Redis |
| 编程语言 | Python |

## 快速开始

### 前置条件

- Python 3.10+
- （可选）本地 Redis 服务（用于缓存功能）

### 安装

```bash
git clone https://github.com/yacha6/my_rag.git
cd my_rag
pip install -r requirements.txt
```

### 配置

在项目根目录创建 `.env` 文件：

```env
DASHSCOPE_API_KEY=your_dashscope_api_key
DASHSCOPE_EMBEDDING_MODEL=text-embedding-v2
DASHSCOPE_LLM_MODEL=qwen3-vl-235b-a22b-thinking
DASHSCOPE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
```

> 如需使用 Azure OpenAI，可参考 `.env` 文件中的相关注释字段进行配置。

### 运行

**带缓存版本（需要本地 Redis）：**

```bash
streamlit run rag.py
```

**无缓存版本：**

```bash
streamlit run rag_no_cache.py
```

## 使用说明

1. 运行后浏览器会自动打开 Web 界面
2. 在输入框中输入问题
3. 系统自动从知识库中检索相关内容并生成回答
4. 回答以流式方式实时展示

默认知识库为 `曲面打印机说明书.txt`，你也可以在代码中修改 `file_path` 指向自己的文档。

## 项目结构

```
├── rag.py              # 主程序（含 Redis 缓存）
├── rag_no_cache.py     # 无缓存版本
├── run.py              # 辅助入口
├── requirements.txt    # Python 依赖
├── .env                # 环境变量配置（不上传 GitHub）
└── 曲面打印机说明书.txt  # 示例知识库文档
```

## 注意事项

- **不要将 `.env` 文件提交到 GitHub**，它包含 API 密钥。项目已包含 `.gitignore` 模板供参考
- 启动带缓存版本前请确保本地 Redis 服务已运行
- 首次启动时系统会自动对文档进行分块和向量化，耗时取决于文档大小

## License

MIT
