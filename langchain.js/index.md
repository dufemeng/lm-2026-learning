# 🤖 LangChain.js Agent 开发完整学习体系

> 目标：掌握 Agent 开发全链路，服务于「智能生成视频脚本 + 批量视频生成」实战项目

---

## 思维导图

```
LangChain.js Agent 开发
│
├─── 1. 🧱 核心基础层
│    │
│    ├─── 1.1 认知框架
│    │    ├── LLM vs Chain vs Agent 的本质区别
│    │    │   ├── LLM：单次输入输出，无状态
│    │    │   ├── Chain：固定流程，多步串联
│    │    │   └── Agent：自主规划 + 动态决策 + 工具调用
│    │    ├── Agent 的核心能力三角
│    │    │   ├── 工具调用 (Tool Use)        — 与外部世界交互
│    │    │   ├── 上下文记忆 (Memory)        — 记住对话和状态
│    │    │   └── 自主规划 (Planning)        — 分解任务、决策路径
│    │    └── ReAct 循环模型
│    │         ├── Thought  — 推理：我需要做什么
│    │         ├── Action   — 选择并调用工具
│    │         ├── Observation — 观察工具返回结果
│    │         └── 循环 or Final Answer
│    │
│    ├─── 1.2 生态全景
│    │    ├── LangChain.js 核心包
│    │    │   ├── @langchain/core      — 核心接口与抽象（Runnable / Message / Tool）
│    │    │   ├── @langchain/openai    — OpenAI / Azure 集成
│    │    │   ├── @langchain/community — 社区工具、向量库、文档加载器
│    │    │   └── langchain            — 高层封装（Chain / Agent / Memory）
│    │    ├── LangGraph.js             — 状态机编排，复杂 Agent 首选
│    │    ├── LangSmith                — 调试、追踪、评估平台
│    │    └── 竞品对比
│    │         ├── Vercel AI SDK        — TypeScript 友好，适合 Next.js
│    │         ├── Mastra               — 新兴 JS Agent 框架
│    │         └── AutoGen / CrewAI     — Python 生态，多 Agent 协作
│    │
│    └─── 1.3 Runnable 接口（核心抽象）
│         ├── 统一接口：invoke / stream / batch / pipe
│         ├── LCEL（LangChain Expression Language）
│         │   ├── 管道语法：prompt | model | parser
│         │   ├── RunnableSequence  — 顺序执行
│         │   ├── RunnableParallel  — 并行执行
│         │   ├── RunnablePassthrough — 透传数据
│         │   ├── RunnableLambda    — 任意函数转 Runnable
│         │   └── RunnableBranch    — 条件分支
│         └── 为什么用 LCEL
│              ├── 统一接口，可组合
│              ├── 天然支持流式输出
│              └── 自动支持批量、并行
│
├─── 2. 🧠 模型层（Model Layer）
│    │
│    ├─── 2.1 模型类型
│    │    ├── Chat Model（主流）     — 多轮对话，返回 AIMessage
│    │    ├── LLM（传统）            — 文本补全，返回字符串
│    │    ├── Embedding Model        — 文本向量化，用于 RAG
│    │    └── Multi-Modal Model      — 支持图片/音频输入
│    │
│    ├─── 2.2 主流模型集成
│    │    ├── OpenAI        — GPT-4o / GPT-4o-mini
│    │    ├── Anthropic     — Claude 3.5 Sonnet
│    │    ├── Google        — Gemini 1.5 Pro
│    │    ├── 本地模型      — Ollama（llama3 / qwen 等）
│    │    └── 国内模型      — DeepSeek / Qwen / Moonshot
│    │
│    ├─── 2.3 模型参数调优
│    │    ├── temperature   — 创造性（0=确定，1=随机）
│    │    ├── maxTokens     — 最大输出长度
│    │    ├── topP          — 核采样
│    │    └── stop          — 停止序列
│    │
│    └─── 2.4 消息类型体系
│         ├── SystemMessage    — 系统指令（定义角色、规则）
│         ├── HumanMessage     — 用户输入
│         ├── AIMessage        — 模型输出
│         ├── ToolMessage      — 工具调用结果
│         └── FunctionMessage  — 旧版函数调用结果
│
├─── 3. 📝 Prompt 层（提示词工程）
│    │
│    ├─── 3.1 Prompt 模板类型
│    │    ├── PromptTemplate              — 字符串模板（变量替换）
│    │    ├── ChatPromptTemplate          — 多角色对话模板
│    │    ├── FewShotPromptTemplate       — 少样本示例模板
│    │    └── MessagesPlaceholder         — 动态插入消息列表
│    │
│    ├─── 3.2 Prompt 设计原则
│    │    ├── 角色设定 (Persona)          — 明确 AI 的身份和能力边界
│    │    ├── 任务描述 (Task)             — 清晰描述期望输出
│    │    ├── 输出格式 (Format)           — 指定 JSON / Markdown / 列表等
│    │    ├── 约束条件 (Constraints)      — 字数限制、风格要求
│    │    ├── 上下文注入 (Context)        — 注入背景知识
│    │    └── Few-shot 示例               — 提供 2-3 个输入输出范例
│    │
│    ├─── 3.3 高级 Prompt 技巧
│    │    ├── Chain-of-Thought (CoT)      — 让模型展示推理过程
│    │    ├── Tree-of-Thought (ToT)       — 多路径探索
│    │    ├── ReACT Prompting             — 推理 + 行动交替
│    │    ├── Self-Consistency            — 多次采样取最一致答案
│    │    └── Prompt Chaining             — 拆分复杂任务为多步
│    │
│    └─── 3.4 Prompt 管理与版本控制
│         ├── 存放在独立文件 / 模板文件夹
│         ├── LangSmith Hub               — 在线 Prompt 仓库
│         └── 版本化：A/B 测试不同 Prompt
│
├─── 4. 🛠️ Tool（工具）：赋予 Agent 行动能力
│    │
│    ├─── 4.1 Tool 的本质
│    │    ├── 工具 = 有 name + description + schema 的函数
│    │    ├── LLM 根据 description 决定是否调用
│    │    └── schema 定义参数类型（基于 Zod）
│    │
│    ├─── 4.2 Tool 定义方式
│    │    ├── tool() 函数               — 最简洁方式（推荐）
│    │    ├── StructuredTool 类         — 适合复杂工具，面向对象
│    │    ├── DynamicTool              — 运行时动态创建
│    │    └── @tool 装饰器（实验性）
│    │
│    ├─── 4.3 Tool 参数 Schema 设计
│    │    ├── 用 Zod 定义参数结构
│    │    ├── 每个字段必须有 .describe()（LLM 靠这个理解参数含义）
│    │    ├── 可选参数用 .optional()
│    │    └── 枚举值用 z.enum()
│    │
│    ├─── 4.4 Tool Calling 流程
│    │    ├── 1. 将工具绑定到模型：model.bindTools(tools)
│    │    ├── 2. 模型返回 tool_calls（不是直接回答）
│    │    ├── 3. 解析 tool_calls，执行对应函数
│    │    ├── 4. 将 ToolMessage（工具结果）加入消息历史
│    │    └── 5. 再次调用模型，生成最终回答
│    │
│    ├─── 4.5 常用内置工具
│    │    ├── 搜索类
│    │    │   ├── TavilySearch          — 实时网络搜索（推荐）
│    │    │   ├── BraveSearch           — 隐私优先搜索
│    │    │   └── DuckDuckGoSearch      — 免费搜索
│    │    ├── 代码执行
│    │    │   └── Calculator / Python REPL
│    │    ├── 数据读取
│    │    │   ├── WikipediaTool
│    │    │   └── ArxivTool
│    │    └── 文件操作
│    │         └── ReadFileTool / WriteFileTool
│    │
│    └─── 4.6 自定义 Tool 设计要点
│         ├── description 要精准（影响模型决策）
│         ├── 工具应该原子化（单一职责）
│         ├── 返回值用字符串或 JSON 字符串
│         ├── 工具内部做好错误捕获，返回错误信息而非抛异常
│         └── 工具数量控制（建议 < 10 个，避免选择困难）
│
├─── 5. 💾 Memory（记忆）：上下文管理
│    │
│    ├─── 5.1 为什么需要 Memory
│    │    ├── LLM 本身无状态（每次调用独立）
│    │    ├── Agent 需要记住对话历史
│    │    └── 长任务需要保存中间状态
│    │
│    ├─── 5.2 记忆类型分类
│    │    ├── 短期记忆（In-Context Memory）
│    │    │   ├── 对话历史窗口           — 保留最近 N 轮对话
│    │    │   └── 整个上下文直接输入模型
│    │    ├── 长期记忆（External Memory）
│    │    │   ├── 向量数据库存储历史      — 语义检索相关记忆
│    │    │   └── 关键信息提炼后持久化
│    │    └── 工作记忆（Working Memory）
│    │         └── 当前任务执行状态（LangGraph State）
│    │
│    ├─── 5.3 对话历史管理方案
│    │    ├── 消息列表（最简单）         — 直接传入 messages 数组
│    │    ├── ConversationBufferMemory   — 保存全部历史（旧版 API）
│    │    ├── ConversationWindowMemory   — 滑动窗口（保留最近 K 轮）
│    │    ├── ConversationSummaryMemory  — 定期摘要压缩历史
│    │    ├── ConversationTokenBufferMemory — 按 Token 数量限制
│    │    └── ChatMessageHistory（推荐新版）— 基于存储后端
│    │
│    ├─── 5.4 持久化存储后端
│    │    ├── InMemoryChatMessageHistory — 内存（开发调试用）
│    │    ├── RedisChatMessageHistory    — Redis（生产推荐）
│    │    ├── PostgresChatMessageHistory — 数据库持久化
│    │    └── MongoDBChatMessageHistory  — MongoDB
│    │
│    ├─── 5.5 记忆压缩策略
│    │    ├── 摘要压缩（Summarization）
│    │    │   └── 超过阈值后，让 LLM 对历史进行摘要
│    │    ├── RAG 记忆（Vector Memory）
│    │    │   └── 历史消息向量化存储，按语义检索
│    │    └── 关键信息提取
│    │         └── 只保存「实体」「偏好」「事实」等关键信息
│    │
│    └─── 5.6 LangGraph 中的状态管理（新范式）
│         ├── State = Graph 的共享状态对象
│         ├── messages 字段自动管理对话历史
│         ├── MemorySaver — 内存级持久化
│         └── 自定义 Checkpointer — 数据库持久化
│
├─── 6. 📚 RAG（检索增强生成）
│    │
│    ├─── 6.1 RAG 解决的问题
│    │    ├── LLM 知识截止日期限制
│    │    ├── 私有/专有知识库问答
│    │    ├── 减少幻觉（基于真实文档回答）
│    │    └── 降低成本（避免超长 Context）
│    │
│    ├─── 6.2 RAG 完整流程
│    │    │
│    │    ├── [离线阶段：构建知识库]
│    │    │   ├── 1. 文档加载 (Document Loading)
│    │    │   ├── 2. 文档分割 (Text Splitting)
│    │    │   ├── 3. 向量化 (Embedding)
│    │    │   └── 4. 存入向量数据库 (Vector Store)
│    │    │
│    │    └── [在线阶段：检索回答]
│    │         ├── 5. 用户问题向量化
│    │         ├── 6. 相似度检索 (Retrieval)
│    │         ├── 7. 注入到 Prompt (Augmentation)
│    │         └── 8. LLM 生成答案 (Generation)
│    │
│    ├─── 6.3 文档加载器（Document Loaders）
│    │    ├── 文件格式
│    │    │   ├── PDFLoader / DocxLoader
│    │    │   ├── CSVLoader / JSONLoader
│    │    │   └── MarkdownLoader / TextLoader
│    │    ├── 网络来源
│    │    │   ├── WebBaseLoader              — 爬取网页
│    │    │   ├── YoutubeLoader              — YouTube 字幕
│    │    │   └── GitHubLoader               — GitHub 仓库
│    │    └── 数据库
│    │         └── NotionLoader / ConfluenceLoader
│    │
│    ├─── 6.4 文档分割策略（Text Splitters）
│    │    ├── RecursiveCharacterTextSplitter  — 通用首选
│    │    │   ├── chunkSize                  — 每块大小（字符数）
│    │    │   └── chunkOverlap               — 块间重叠（保证上下文连贯）
│    │    ├── MarkdownHeaderTextSplitter      — 按标题分割
│    │    ├── TokenTextSplitter               — 按 Token 分割
│    │    ├── SemanticChunker                 — 语义分割（更智能）
│    │    └── 分割策略选择
│    │         ├── 通用文档 → RecursiveCharacter
│    │         ├── 结构化文档 → 按标题/段落
│    │         └── 代码 → 按语言语法分割
│    │
│    ├─── 6.5 Embedding 模型
│    │    ├── OpenAI text-embedding-3-small   — 性价比高（推荐）
│    │    ├── OpenAI text-embedding-3-large   — 更高精度
│    │    ├── Cohere Embeddings               — 多语言优化
│    │    └── 本地 Embedding（HuggingFace）  — 私有化部署
│    │
│    ├─── 6.6 向量数据库（Vector Stores）
│    │    ├── 托管服务
│    │    │   ├── Pinecone                   — 最成熟，生产推荐
│    │    │   └── Weaviate                   — 开源可自托管
│    │    ├── 轻量级（适合开发/小型项目）
│    │    │   ├── Chroma                     — 纯本地，开发友好
│    │    │   ├── FAISS                      — Meta 出品，高效
│    │    │   └── LanceDB                    — 无服务器向量库
│    │    └── 关系型 + 向量
│    │         └── pgvector (PostgreSQL 扩展) — 已有 PG 的项目首选
│    │
│    ├─── 6.7 检索策略（Retrievers）
│    │    ├── 基础检索
│    │    │   ├── 相似度检索 (Similarity)     — 余弦/点积距离
│    │    │   └── MMR 检索                    — 最大边际相关性（去重）
│    │    ├── 高级检索
│    │    │   ├── MultiQueryRetriever         — 多角度改写问题后检索
│    │    │   ├── ContextualCompressionRetriever — 检索后压缩内容
│    │    │   ├── SelfQueryRetriever          — 自动解析过滤条件
│    │    │   ├── EnsembleRetriever           — 混合多个检索器（加权）
│    │    │   └── ParentDocumentRetriever     — 小块检索、大块返回
│    │    └── 混合检索（Hybrid Search）
│    │         ├── 关键词检索（BM25）+ 向量检索
│    │         └── RRF（倒数排名融合）重排序
│    │
│    └─── 6.8 RAG 进阶优化
│         ├── 查询优化
│         │   ├── Query Rewriting            — 改写问题，更利于检索
│         │   ├── HyDE（假设文档嵌入）        — 先生成假设答案再检索
│         │   └── Step-Back Prompting        — 泛化问题再检索
│         ├── 检索优化
│         │   ├── Reranking（重排序）         — Cohere Rerank / BGE
│         │   └── 元数据过滤                 — 按时间/来源筛选
│         └── RAG 评估指标
│              ├── Faithfulness（忠实度）     — 答案是否基于文档
│              ├── Answer Relevancy（答案相关性）
│              └── Context Precision/Recall  — 检索准确率/召回率
│
├─── 7. 🤖 Agent 架构（核心章节）
│    │
│    ├─── 7.1 Agent 类型
│    │    ├── ReAct Agent                    — 推理 + 行动循环（最通用）
│    │    ├── Plan-and-Execute Agent         — 先规划全流程，再逐步执行
│    │    ├── OpenAI Functions Agent         — 基于 Function Calling（旧版）
│    │    ├── Tool Calling Agent             — 基于 Tool Calling（新版推荐）
│    │    ├── Self-Ask Agent                 — 自问自答，处理复杂推理
│    │    └── Conversational Agent           — 多轮对话 + 工具 + 记忆
│    │
│    ├─── 7.2 AgentExecutor（经典 Agent 运行器）
│    │    ├── 组成：agent（决策） + tools（执行） + memory（记忆）
│    │    ├── maxIterations              — 最大迭代次数（防死循环）
│    │    ├── earlyStoppingMethod        — 超限时的处理策略
│    │    ├── returnIntermediateSteps    — 返回中间步骤（调试用）
│    │    └── handleParsingErrors       — 解析错误处理
│    │
│    ├─── 7.3 Agent 决策机制
│    │    ├── LLM 如何选择工具
│    │    │   ├── 基于 Tool 的 name + description
│    │    │   ├── 基于当前对话上下文
│    │    │   └── 基于 system prompt 中的指令
│    │    ├── 停止条件
│    │    │   ├── 模型输出 Final Answer
│    │    │   ├── 达到 maxIterations
│    │    │   └── 工具返回特定信号
│    │    └── 强制工具调用
│    │         └── tool_choice: 指定必须调用某工具
│    │
│    ├─── 7.4 Multi-Agent 架构（多智能体）
│    │    ├── 为什么需要 Multi-Agent
│    │    │   ├── 单 Agent Context 有限
│    │    │   ├── 任务可以并行处理
│    │    │   └── 不同 Agent 专注不同能力
│    │    ├── 协作模式
│    │    │   ├── Supervisor 模式            — 一个主 Agent 调度多个子 Agent
│    │    │   ├── 流水线模式                 — Agent A → Agent B → Agent C
│    │    │   └── 辩论模式                   — 多 Agent 互相 Review
│    │    └── 实现方式
│    │         └── LangGraph 多节点图
│    │
│    └─── 7.5 Agent 评估与调试
│         ├── 中间步骤追踪                   — returnIntermediateSteps
│         ├── LangSmith 全链路追踪
│         ├── Token 消耗监控
│         └── 常见问题
│              ├── 工具选择错误              — 优化 description
│              ├── 死循环                    — 设置 maxIterations
│              ├── 幻觉工具调用              — 增加工具调用约束
│              └── 上下文溢出                — 压缩历史 / 使用 RAG
│
├─── 8. 🔀 LangGraph（复杂 Agent 编排）
│    │
│    ├─── 8.1 为什么需要 LangGraph
│    │    ├── AgentExecutor 无法表达复杂流程（分支/循环/并行）
│    │    ├── 无法在执行过程中修改状态
│    │    └── 无法实现人工介入（Human-in-the-loop）
│    │
│    ├─── 8.2 核心概念
│    │    ├── Graph（图）                    — 整个 Agent 的流程定义
│    │    ├── Node（节点）                   — 一个处理步骤（函数）
│    │    ├── Edge（边）                     — 节点间的连接关系
│    │    ├── Conditional Edge               — 条件分支（根据状态决定下一步）
│    │    └── State（状态）                  — 贯穿整个 Graph 的共享数据
│    │
│    ├─── 8.3 State 设计
│    │    ├── 用 Annotation 定义 State 结构
│    │    ├── messages 字段              — 内置对话历史（自动追加）
│    │    ├── 自定义字段                 — 任务状态、中间结果等
│    │    └── Reducer 函数              — 定义字段如何合并更新
│    │
│    ├─── 8.4 Graph 构建模式
│    │    ├── 基础 Agent 图
│    │    │   ├── START → agent_node → tools_node → agent_node（循环）→ END
│    │    │   └── should_continue 函数控制循环 or 结束
│    │    ├── 预构建 createReactAgent
│    │    │   └── 快速创建标准 ReAct Agent
│    │    └── 自定义复杂图
│    │         ├── 多条件分支
│    │         ├── 并行子图
│    │         └── 子图嵌套（SubGraph）
│    │
│    ├─── 8.5 持久化与检查点（Checkpointing）
│    │    ├── MemorySaver                   — 内存持久化（开发调试）
│    │    ├── SqliteSaver                   — SQLite 持久化
│    │    ├── PostgresSaver                 — PostgreSQL 持久化（生产推荐）
│    │    ├── thread_id                     — 标识独立对话会话
│    │    └── 支持中断后恢复（Resume）
│    │
│    ├─── 8.6 Human-in-the-Loop（人工介入）
│    │    ├── 在关键节点暂停等待人工确认
│    │    ├── interrupt_before / interrupt_after
│    │    ├── 人工修改 State 后继续执行
│    │    └── 适用场景：执行前确认、结果审核
│    │
│    └─── 8.7 流式输出
│         ├── stream()                      — 节点级流式
│         ├── streamEvents()                — 细粒度事件流
│         └── 前端接入 SSE / WebSocket 实时展示进度
│
├─── 9. 📤 Structured Output（结构化输出）
│    │
│    ├─── 9.1 为什么需要结构化输出
│    │    ├── 后续代码需要解析 LLM 输出
│    │    ├── 确保输出格式一致（避免随机格式）
│    │    └── 对接数据库 / API 时需要强类型
│    │
│    ├─── 9.2 实现方式
│    │    ├── model.withStructuredOutput(schema)  — 推荐方式
│    │    │   ├── 基于 Zod Schema 或 JSON Schema
│    │    │   └── 自动处理 Function Calling / JSON Mode
│    │    ├── JsonOutputParser               — 解析 JSON 字符串
│    │    ├── StructuredOutputParser         — 自定义格式解析
│    │    └── Prompt 引导 + 手动解析         — 兜底方案
│    │
│    ├─── 9.3 Schema 设计最佳实践
│    │    ├── 每个字段加 .describe()（引导模型正确填充）
│    │    ├── 合理使用 optional()（避免模型强行补全）
│    │    ├── 枚举值限定范围
│    │    └── 避免过度嵌套（增加模型理解难度）
│    │
│    └─── 9.4 与视频脚本项目的结合
│         ├── 脚本结构体：{ title, scenes[], duration, style }
│         ├── 场景结构体：{ sceneIndex, visual, voiceover, duration }
│         └── 批量任务结构体：{ taskId, status, scripts[] }
│
├─── 10. ⚡ Streaming（流式响应）
│    │
│    ├─── 10.1 为什么重要
│    │    ├── 提升用户体验（即时反馈，无需等待）
│    │    └── 视频生成进度实时推送
│    │
│    ├─── 10.2 流式类型
│    │    ├── Token 流                       — 字符逐个输出
│    │    ├── Chain 流                       — 每个节点的输出
│    │    └── Event 流                       — LangGraph 的细粒度事件
│    │
│    ├─── 10.3 服务端推送方案
│    │    ├── SSE（Server-Sent Events）      — 单向推送，HTTP 协议
│    │    └── WebSocket                     — 双向通信，适合交互式场景
│    │
│    └─── 10.4 流式处理注意事项
│         ├── 错误处理（流中断时的恢复）
│         ├── 背压处理（客户端消费慢时）
│         └── 结构化输出 + 流式（streaming with structured output）
│
├─── 11. 🔍 可观测性（Observability）
│    │
│    ├─── 11.1 为什么 Agent 需要可观测性
│    │    ├── Agent 的决策过程不透明（黑盒）
│    │    ├── 调试复杂链路需要追踪每一步
│    │    └── 监控 Token 消耗和成本
│    │
│    ├─── 11.2 LangSmith（官方推荐）
│    │    ├── 全链路追踪（每次 LLM 调用的输入输出）
│    │    ├── Latency 分析
│    │    ├── Token 消耗统计
│    │    ├── Prompt 版本管理
│    │    └── 数据集 + 评估工作流
│    │
│    ├─── 11.3 Callback 系统
│    │    ├── 内置 Callback（ConsoleCallbackHandler、TracebackCallbackHandler）
│    │    ├── 自定义 BaseCallbackHandler
│    │    ├── 可监听事件：
│    │    │   ├── onLLMStart / onLLMEnd / onLLMError
│    │    │   ├── onToolStart / onToolEnd / onToolError
│    │    │   ├── onChainStart / onChainEnd
│    │    │   └── onAgentAction / onAgentFinish
│    │    └── 传入位置：全局 / 单次调用 / 链级别
│    │
│    └─── 11.4 生产监控
│         ├── 集成 OpenTelemetry
│         ├── 成本告警（Token 消耗超出阈值）
│         └── 错误率监控
│
├─── 12. 🛡️ 错误处理与鲁棒性
│    │
│    ├─── 12.1 LLM 调用失败
│    │    ├── Rate Limit（频率限制）          — 指数退避重试
│    │    ├── Timeout（超时）                 — 设置超时 + 重试
│    │    ├── API 不可用                      — 备用模型（Fallback）
│    │    └── RunnableWithFallbacks          — 自动切换备用模型
│    │
│    ├─── 12.2 Tool 调用失败
│    │    ├── 工具内部错误                    — 返回错误信息字符串（不抛异常）
│    │    ├── 参数解析失败                    — 返回解析错误提示
│    │    └── 超时                           — 设置工具超时
│    │
│    ├─── 12.3 输出格式错误
│    │    ├── JSON 解析失败                   — OutputFixingParser（让 LLM 修正）
│    │    ├── 缺少必需字段                    — Zod 校验失败处理
│    │    └── 重试策略                        — withRetry() 方法
│    │
│    └─── 12.4 Agent 异常行为
│         ├── 无限循环检测                    — maxIterations 硬限制
│         ├── 幻觉工具（调用不存在的工具）    — 工具名称严格匹配
│         └── 输出内容安全                   — 接入内容审核工具
│
└─── 13. 🏭 生产级 Agent 架构
     │
     ├─── 13.1 项目结构
     │    ├── src/
     │    │   ├── agents/              — Agent 定义（按功能分文件）
     │    │   ├── tools/               — Tool 定义
     │    │   ├── prompts/             — Prompt 模板（独立文件）
     │    │   ├── memory/              — 记忆配置与存储
     │    │   ├── retrievers/          — RAG 检索器
     │    │   └── graphs/              — LangGraph 图定义
     │    └── tests/                   — Agent 测试
     │
     ├─── 13.2 与后端框架集成
     │    ├── NestJS 集成
     │    │   ├── 将 Agent 封装为 Service
     │    │   ├── 长任务配合 BullMQ 队列
     │    │   └── WebSocket / SSE 流式返回给前端
     │    └── 异步任务模式
     │         ├── 用户发起请求 → 入队 → 返回 taskId
     │         ├── BullMQ Worker 执行 Agent
     │         └── 进度通过 Redis Pub/Sub 推送
     │
     ├─── 13.3 安全注意事项
     │    ├── Prompt Injection（提示注入攻击）
     │    │   ├── 用户输入可能操控 Agent 行为
     │    │   └── 防御：输入过滤 + 沙箱工具 + 权限最小化
     │    ├── Tool 权限控制
     │    │   ├── 工具应只有必要的最小权限
     │    │   └── 危险操作（删除/写文件）需二次确认
     │    ├── 敏感信息泄露
     │    │   ├── 不在 Prompt 中硬编码密钥
     │    │   └── 不将敏感数据发给外部 LLM
     │    └── 成本控制
     │         ├── maxTokens 限制输出
     │         ├── maxIterations 限制循环
     │         └── 接入成本告警
     │
     ├─── 13.4 测试策略
     │    ├── 单元测试：Tool 函数测试（Mock LLM）
     │    ├── 集成测试：Chain / Agent 端到端
     │    ├── 评估测试：
     │    │   ├── 使用 LangSmith 构建测试数据集
     │    │   └── 自动化评估答案质量（LLM-as-Judge）
     │    └── 回归测试：Prompt 修改后运行评估集
     │
     └─── 13.5 视频脚本 Agent 实战映射
          │
          ├── 用户输入意图
          │   └── → 意图解析 Agent（提取主题/风格/时长）
          ├── 脚本生成
          │   └── → 结构化输出（ScriptSchema）
          │       → 多场景并行生成（RunnableParallel）
          ├── 批量任务管理
          │   └── → BullMQ 队列 + LangGraph 状态机
          ├── 视频生成
          │   └── → 外部 API Tool（Runway / Pika）
          │       → 异步轮询状态（Polling Tool）
          └── 结果汇总
               └── → 任务状态聚合 + SSE 推送前端
```

---

## 📖 学习优先级（对应一个月计划）

| 优先级 | 模块 | 学习周期 | 与项目关联 |
|--------|------|---------|-----------|
| **P0** | 1.核心基础 + Runnable | Week 1 | 所有功能基础 |
| **P0** | 4.Tool 工具系统 | Week 1 | 视频生成 / 搜索工具 |
| **P0** | 9.Structured Output | Week 1 | 脚本结构化输出 |
| **P0** | 5.Memory 记忆 | Week 2 | 多轮对话保持上下文 |
| **P0** | 7.Agent 架构 | Week 2 | 核心 Agent 实现 |
| **P1** | 8.LangGraph | Week 2-3 | 复杂任务流编排 |
| **P1** | 6.RAG | Week 3 | 知识库 / 风格参考文档 |
| **P1** | 10.Streaming | Week 3 | 实时进度推送 |
| **P2** | 11.可观测性 | Week 4 | 调试与监控 |
| **P2** | 13.生产架构 | Week 4 | 项目上线 |

> 💡 **学习建议**：每个模块先理解「是什么、解决什么问题、核心 API」，然后立即在脚本生成 Agent 项目中找到对应的应用点实践。避免为学而学——一切以能跑起来系统为目标。