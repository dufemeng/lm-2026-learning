# 🕸️ LangGraph.js · 状态图驱动的 Agent 开发完整学习体系

> 目标：掌握 LangGraph.js 核心机制，构建具备多步规划、动态路由、持久记忆能力的复杂 Agent
> 优先级：P0 必须掌握 → P1 项目中会用到 → P2 面试加分 → P3 了解概念

---

## 为什么需要 LangGraph？

```
LangChain LCEL（链式管道）的局限：
  ├── 只支持线性 / 有限分支的固定流程
  ├── 无法表达"循环"（ReAct 的 Thought→Action→Observation 循环）
  ├── 无法在节点之间共享和修改复杂状态
  └── 难以实现多 Agent 协作与监督模式

LangGraph 解决了什么：
  ├── 用「状态图」描述任意复杂的 Agent 逻辑（包含循环）
  ├── 显式的共享状态（State），每个节点都可读写
  ├── 条件边（Conditional Edge）实现动态路由决策
  ├── 内置检查点（Checkpoint）支持持久化 + 人工干预
  └── 天然支持多 Agent 协作（Supervisor / Swarm 模式）
```

---

## 核心概念速览

```
LangGraph 三要素
│
├── State（状态）  — 贯穿整个图的共享数据对象，每步执行后更新
├── Node（节点）   — 一个 JS 函数，读取 State → 执行逻辑 → 返回 State 更新
└── Edge（边）     — 节点之间的连接，可以是固定的，也可以是条件判断的
```

---

## 思维导图

```
LangGraph.js 完整学习体系
│
├─── 1. 🧱 核心基础（P0 第一周必须掌握）
│    │
│    ├─── 1.1 图的基本构建块
│    │    │
│    │    ├── [StateGraph]
│    │    │   ├── 整个应用的"画布"，所有节点和边都注册在这里
│    │    │   ├── 创建：new StateGraph(StateAnnotation)
│    │    │   ├── 添加节点：graph.addNode('nodeName', nodeFunction)
│    │    │   ├── 添加边：graph.addEdge('from', 'to')
│    │    │   ├── 添加条件边：graph.addConditionalEdges('from', routerFn, edgeMap)
│    │    │   ├── 设置入口：graph.setEntryPoint('nodeName') 或 graph.addEdge(START, 'nodeName')
│    │    │   ├── 设置出口：graph.addEdge('nodeName', END)
│    │    │   └── 编译：const app = graph.compile()
│    │    │
│    │    ├── [State（状态）]
│    │    │   ├── 本质：一个普通的 TypeScript 对象，贯穿所有节点
│    │    │   ├── 定义方式：Annotation.Root({ key: Annotation<Type> })
│    │    │   ├── 默认 Reducer：后一个值覆盖前一个（替换语义）
│    │    │   ├── 自定义 Reducer：指定合并逻辑（如数组追加）
│    │    │   │   └── messages: Annotation<BaseMessage[]>({ reducer: addMessages })
│    │    │   └── 常见字段设计
│    │    │       ├── messages   — 对话历史（用 addMessages reducer）
│    │    │       ├── taskList   — 待执行任务列表
│    │    │       ├── results    — 工具调用结果
│    │    │       ├── iteration  — 循环计数（防止无限循环）
│    │    │       └── error      — 错误信息（用于条件路由）
│    │    │
│    │    ├── [Node（节点）]
│    │    │   ├── 本质：(state: State) => Partial<State> | Promise<Partial<State>>
│    │    │   ├── 只需返回需要更新的字段，未返回的字段保持不变
│    │    │   ├── 节点类型
│    │    │   │   ├── LLM 节点    — 调用模型，生成文本或 Tool Call
│    │    │   │   ├── Tool 节点   — 执行工具，返回 ToolMessage
│    │    │   │   ├── 路由节点    — 纯逻辑，决定下一步走哪条边
│    │    │   │   └── 人工节点    — 暂停等待人类输入（Human-in-the-Loop）
│    │    │   └── 内置节点
│    │    │       └── ToolNode   — 自动解析 AIMessage 中的 tool_calls 并执行
│    │    │
│    │    └── [Edge（边）]
│    │         ├── 固定边：graph.addEdge('nodeA', 'nodeB')  — 总是从 A 到 B
│    │         ├── 条件边：graph.addConditionalEdges('nodeA', routerFn)
│    │         │   ├── routerFn：(state) => string  — 返回下一个节点名
│    │         │   └── 常用于：工具调用判断、错误处理分支、任务完成检测
│    │         ├── 特殊节点：START（图入口）、END（图出口）
│    │         └── 多出口：一个节点可以连多条条件边到不同节点
│    │
│    ├─── 1.2 执行模型
│    │    │
│    │    ├── 同步执行（invoke）
│    │    │   └── const result = await app.invoke(initialState)
│    │    ├── 流式执行（stream）— 实时获取每个节点的输出
│    │    │   ├── for await (const chunk of app.stream(input)) { ... }
│    │    │   ├── streamMode: "values"   — 每步输出完整 State
│    │    │   └── streamMode: "updates"  — 每步只输出 State 变化量（更常用）
│    │    ├── 批量执行（batch）— 并行处理多个输入
│    │    │   └── await app.batch([input1, input2, input3])
│    │    └── 执行顺序
│    │         ├── START → 入口节点 → 条件路由 → 各业务节点 → END
│    │         └── 超级步（Superstep）：同一轮中并行执行的节点集合
│    │
│    └─── 1.3 第一个 LangGraph Agent（ReAct 最小实现）
│         │
│         ├── 步骤一：定义 State
│         │   └── { messages: BaseMessage[] }（用 addMessages reducer）
│         ├── 步骤二：创建 LLM 节点（绑定工具）
│         │   └── model.bindTools(tools) → 调用 → 返回含 tool_calls 的 AIMessage
│         ├── 步骤三：添加 ToolNode（自动执行工具）
│         │   └── new ToolNode(tools)
│         ├── 步骤四：条件路由判断是否结束
│         │   └── toolsCondition：检测 AIMessage 是否有 tool_calls
│         │       ├── 有 tool_calls → 路由到 ToolNode
│         │       └── 无 tool_calls → 路由到 END
│         └── 步骤五：编译并运行
│
├─── 2. 🔄 记忆与持久化（P0）
│    │
│    ├─── 2.1 短期记忆（会话内）
│    │    ├── 存储在 State.messages 数组中
│    │    ├── addMessages reducer 自动追加消息，不会覆盖历史
│    │    ├── 对话历史会随每次 invoke 传入 LLM
│    │    └── 注意：Context Window 限制，需要定期截断或摘要
│    │
│    ├─── 2.2 检查点（Checkpointer）— 跨会话持久化
│    │    │
│    │    ├── 作用：将每步执行后的 State 快照保存到存储后端
│    │    ├── 带来的能力
│    │    │   ├── 多轮对话（跨请求保持上下文）
│    │    │   ├── 断点续跑（失败后从最近检查点恢复）
│    │    │   ├── 时间旅行（回溯到任意历史状态）
│    │    │   └── 人工干预（暂停 → 人类修改 → 继续执行）
│    │    ├── 内置实现
│    │    │   ├── MemorySaver       — 内存，适合开发调试
│    │    │   ├── SqliteSaver       — SQLite，适合单机部署
│    │    │   └── @langchain/langgraph-checkpoint-postgres — 生产推荐
│    │    ├── 使用方式
│    │    │   ├── const app = graph.compile({ checkpointer: new MemorySaver() })
│    │    │   └── 每次调用需传入 thread_id：{ configurable: { thread_id: 'user-123' } }
│    │    └── thread_id 设计建议
│    │         ├── 一个用户一个对话 = 一个 thread_id
│    │         └── 可以是 userId + sessionId 的组合
│    │
│    ├─── 2.3 长期记忆（跨会话）
│    │    ├── 使用向量数据库存储知识（RAG 模式）
│    │    ├── 使用结构化存储记录用户偏好
│    │    ├── LangGraph Store API（实验性）
│    │    │   └── namespace + key-value 结构
│    │    └── 实际项目：Redis / PostgreSQL 存用户画像 + pgvector 做语义搜索
│    │
│    └─── 2.4 状态管理最佳实践
│         ├── State 中只存必要数据，避免存大对象
│         ├── 区分"当前对话消息"和"长期用户数据"
│         └── 定期用摘要压缩历史消息（summarizeMessages）
│
├─── 3. 🛠️ 工具调用（Tool Use）（P0）
│    │
│    ├─── 3.1 定义工具
│    │    ├── 方式一：tool() 函数（推荐）
│    │    │   ├── import { tool } from '@langchain/core/tools'
│    │    │   ├── tool(fn, { name, description, schema: z.object({...}) })
│    │    │   └── schema 用 Zod 定义，会自动生成 JSON Schema 给 LLM
│    │    └── 方式二：继承 StructuredTool 类
│    │
│    ├─── 3.2 工具执行流程
│    │    ├── 1. LLM 决定调用哪个工具 → 生成 tool_calls（在 AIMessage 中）
│    │    ├── 2. ToolNode 解析 tool_calls → 执行对应工具函数
│    │    ├── 3. 工具返回结果 → 封装成 ToolMessage 追加到 messages
│    │    └── 4. LLM 读取 ToolMessage → 继续推理 or 给出最终答案
│    │
│    ├─── 3.3 工具类型设计（按职责分类）
│    │    ├── 信息检索类
│    │    │   ├── searchWeb           — 网页搜索（Tavily / SerpAPI）
│    │    │   ├── searchKnowledgeBase — 向量库语义搜索（RAG）
│    │    │   └── getWeather / getNews
│    │    ├── 数据操作类
│    │    │   ├── readDatabase / writeDatabase
│    │    │   ├── readFile / writeFile
│    │    │   └── callAPI             — 调用第三方 REST API
│    │    ├── 计算类
│    │    │   └── calculator / codeInterpreter
│    │    └── 项目专用（视频脚本 Agent）
│    │         ├── generateScriptOutline  — 生成脚本大纲
│    │         ├── expandScriptSection    — 扩写某段脚本
│    │         ├── submitVideoTask        — 提交视频生成任务
│    │         └── checkTaskStatus        — 查询任务状态
│    │
│    └─── 3.4 工具错误处理
│         ├── 工具内部 try/catch → 返回错误描述字符串（让 LLM 知道出错了）
│         ├── ToolNode 的 handleToolErrors 选项
│         └── 条件边检测工具错误 → 路由到错误处理节点
│
├─── 4. 🎯 条件路由与控制流（P0）
│    │
│    ├─── 4.1 条件边（Conditional Edges）
│    │    ├── 核心：根据当前 State 动态决定下一步
│    │    ├── 路由函数签名：(state: State) => string | string[]
│    │    ├── 常见路由模式
│    │    │   ├── 工具调用检测：hasToolCalls(state) → 'tools' | END
│    │    │   ├── 任务完成检测：isTaskDone(state) → END | 'planNode'
│    │    │   ├── 错误处理：hasError(state) → 'errorNode' | 'nextNode'
│    │    │   ├── 最大迭代限制：state.iteration >= MAX → END | 'loopNode'
│    │    │   └── 多 Agent 路由：supervisorDecision(state) → 'agentA' | 'agentB'
│    │    └── 内置路由函数
│    │         └── toolsCondition — 检测 AIMessage 最后一条是否有 tool_calls
│    │
│    ├─── 4.2 循环控制
│    │    ├── ReAct 循环：agent → tools → agent（直到无 tool_calls）
│    │    ├── 防死循环：在 State 中记录 iteration，超过阈值强制结束
│    │    └── recursionLimit：compile 时设置最大递归深度（默认 25）
│    │
│    └─── 4.3 并行节点
│         ├── 同一个 Superstep 中，多个节点可以并行执行
│         ├── 实现：从一个节点连多条固定边到不同节点
│         │   └── graph.addEdge('split', 'nodeA'); graph.addEdge('split', 'nodeB')
│         └── 场景：并行调用多个工具 / 多 Agent 并行处理子任务
│
├─── 5. 🧩 多 Agent 协作模式（P1）
│    │
│    ├─── 5.1 为什么需要多 Agent？
│    │    ├── 单 Agent 的局限：Context 太长 → 模型性能下降
│    │    ├── 职责分离：不同领域的 Agent 专注自己的任务
│    │    └── 并行处理：多 Agent 同时工作，提高效率
│    │
│    ├─── 5.2 Supervisor 模式（监督者模式）
│    │    │
│    │    ├── 结构
│    │    │   ├── Supervisor Agent — 接收用户输入，分配任务给 Worker
│    │    │   ├── Worker Agent A   — 专注特定任务（如脚本生成）
│    │    │   └── Worker Agent B   — 专注特定任务（如视频生成）
│    │    ├── 实现方式
│    │    │   ├── Supervisor 是一个 LLM 节点，输出决策（路由到哪个 Worker）
│    │    │   ├── 每个 Worker 是一个子图（Subgraph）
│    │    │   └── Worker 完成后将结果返回给 Supervisor
│    │    └── 适合场景：任务有明确分工，Supervisor 能判断任务类型
│    │
│    ├─── 5.3 网络模式（Agent Network / Swarm）
│    │    ├── Agent 之间可以互相"转交"任务（handoff）
│    │    ├── 没有固定层级，更加灵活
│    │    ├── 实现：每个 Agent 可以调用"转交给 AgentX"工具
│    │    └── 适合场景：任务边界模糊，需要动态协商
│    │
│    ├─── 5.4 子图（Subgraph）
│    │    ├── 一个完整的 StateGraph 可以作为另一个图的节点
│    │    ├── 子图有自己独立的 State，通过输入/输出与父图交互
│    │    ├── 好处：模块化、可复用、可独立测试
│    │    └── 使用：graph.addNode('workerA', workerAGraph.compile())
│    │
│    └─── 5.5 实战：视频脚本 Agent 的多 Agent 架构
│         ├── Supervisor    — 解析用户意图，分配任务
│         ├── ScriptAgent   — 生成视频脚本（调用 LLM + 脚本工具）
│         ├── ReviewAgent   — 审核脚本质量（可选）
│         └── VideoAgent    — 提交视频生成任务，追踪状态
│
├─── 6. ⏸️ Human-in-the-Loop（人工干预）（P1）
│    │
│    ├─── 6.1 什么是 Human-in-the-Loop？
│    │    ├── Agent 执行到关键决策点时暂停，等待人类确认/修改
│    │    └── 典型场景：执行不可逆操作前（发送邮件、生成视频、扣费）
│    │
│    ├─── 6.2 实现机制：interrupt
│    │    ├── 在节点函数中调用 interrupt(value) 暂停执行
│    │    ├── 需要 Checkpointer 才能工作（保存暂停前的 State）
│    │    ├── 暂停后通过 app.invoke(null, config) 恢复并传入人类反馈
│    │    └── 工作流
│    │         ├── 1. Agent 运行 → 遇到 interrupt → 暂停 → 返回暂停信息
│    │         ├── 2. 人类查看信息 → 决定继续/修改/取消
│    │         └── 3. 调用 app.invoke(Command.RESUME(humanInput), config) 继续
│    │
│    ├─── 6.3 breakpoints（断点）— 更简单的暂停方式
│    │    ├── compile 时指定：{ interruptBefore: ['nodeName'] }
│    │    └── 在进入指定节点之前自动暂停（不需要修改节点代码）
│    │
│    └─── 6.4 时间旅行（Time Travel）
│         ├── 查看历史状态：app.getStateHistory(config)
│         ├── 回到过去：app.updateState(config, newState, { asNode: 'nodeName' })
│         └── 场景：调试、纠错、探索不同决策路径
│
├─── 7. 📡 流式输出（Streaming）（P1）
│    │
│    ├─── 7.1 为什么流式很重要？
│    │    ├── LLM 生成速度慢，流式输出大幅改善用户体验
│    │    └── 实时展示 Agent 的"思考过程"（工具调用、中间结果）
│    │
│    ├─── 7.2 stream 模式
│    │    ├── "values"  — 每步输出完整 State（适合简单场景）
│    │    ├── "updates" — 每步只输出 State 变化（更高效，推荐）
│    │    ├── "messages"— 流式输出 LLM 的 token（字级别流式）
│    │    └── "events"  — 最细粒度，输出所有事件（调试用）
│    │
│    ├─── 7.3 与前端集成（SSE / WebSocket）
│    │    ├── NestJS + SSE：
│    │    │   ├── @Sse() 装饰器 + Observable<MessageEvent>
│    │    │   └── for await 读取 app.stream() → 推送给前端
│    │    └── 前端消费：EventSource API 或 fetch with ReadableStream
│    │
│    └─── 7.4 流式最佳实践
│         ├── 区分"思考过程流"和"最终结果流"（分别推送）
│         └── 使用 streamMode: "messages" 实现逐 token 打字机效果
│
├─── 8. 🏗️ 高级模式（P2）
│    │
│    ├─── 8.1 Plan-and-Execute（计划执行模式）
│    │    ├── 流程
│    │    │   ├── 1. Planner Agent  — 将复杂任务分解为步骤列表
│    │    │   ├── 2. Executor Agent — 逐步执行每个步骤
│    │    │   └── 3. Replanner      — 根据执行结果调整计划
│    │    ├── 适合场景：任务复杂、步骤多、需要动态调整
│    │    └── State 设计：{ plan: string[], pastSteps: [string, string][], response: string }
│    │
│    ├─── 8.2 Reflection（自我反思模式）
│    │    ├── 流程：生成输出 → 反思批评 → 修改重写 → 循环直到满意
│    │    ├── 节点：generate → reflect → (continue | end)
│    │    └── 适合场景：内容生成（文章/代码/脚本）的质量提升
│    │
│    ├─── 8.3 Map-Reduce 模式
│    │    ├── Send API：动态创建并行节点（数量不固定）
│    │    │   └── graph.addConditionalEdges('split', (s) => s.items.map(i => new Send('process', {item: i})))
│    │    ├── 适合场景：批量处理（对每个脚本并行生成视频）
│    │    └── 注意：需要自定义 Reducer 合并各节点结果
│    │
│    └─── 8.4 纠错与重试模式
│         ├── 工具调用失败 → 进入 fallback 节点 → 重写工具参数 → 重试
│         ├── 最大重试次数：State 中记录 retryCount
│         └── 指数退避：在工具节点内实现延迟重试逻辑
│
├─── 9. 🔍 调试与可观测性（P1）
│    │
│    ├─── 9.1 LangSmith 集成
│    │    ├── 配置环境变量
│    │    │   ├── LANGCHAIN_TRACING_V2=true
│    │    │   ├── LANGCHAIN_API_KEY=your-key
│    │    │   └── LANGCHAIN_PROJECT=your-project-name
│    │    ├── 功能
│    │    │   ├── Trace 追踪：可视化每次 LLM 调用的输入/输出/耗时/费用
│    │    │   ├── Playground：在线回放和修改 Trace
│    │    │   └── Evaluation：批量评估 Agent 输出质量
│    │    └── 无需修改代码，环境变量即可开启
│    │
│    ├─── 9.2 本地调试技巧
│    │    ├── streamMode: "updates" — 逐步打印每个节点的输出
│    │    ├── app.getState(config)  — 查看当前完整 State
│    │    ├── app.getStateHistory(config) — 查看所有历史快照
│    │    └── 打印 State 变化：在每个节点开头 console.log(state)
│    │
│    └─── 9.3 常见问题排查
│         ├── 无限循环：检查条件边是否正确配置了终止条件
│         ├── State 未更新：检查节点是否返回了正确的字段名
│         ├── 工具未调用：检查 model.bindTools(tools) 是否绑定了工具
│         └── Checkpointer 问题：确保每次调用都传入了相同的 thread_id
│
├─── 10. 🔧 工程化与生产部署（P2）
│    │
│    ├─── 10.1 与 NestJS 集成
│    │    ├── 将编译后的 graph 封装为 NestJS Service
│    │    │   └── @Injectable() AgentService { constructor() { this.graph = buildGraph() } }
│    │    ├── 使用 NestJS 的 ConfigService 管理 API Key
│    │    ├── 通过 SSE Controller 暴露流式接口
│    │    └── 用 BullMQ 队列包装 Agent 调用（避免超时、支持重试）
│    │
│    ├─── 10.2 性能优化
│    │    ├── 模型选择：GPT-4o-mini / Claude Haiku 处理简单子任务（省钱）
│    │    ├── 缓存 LLM 响应：相同输入直接返回缓存（Redis + hash key）
│    │    ├── 流式处理：避免长时间等待，用户体验更好
│    │    └── 并行工具调用：LLM 支持一次返回多个 tool_calls
│    │
│    ├─── 10.3 费用控制
│    │    ├── 追踪 Token 使用：LangSmith 可统计每次调用的 Token 消耗
│    │    ├── 设置 maxTokens 限制输出长度
│    │    ├── 合理选择模型：不同任务用不同规格模型
│    │    └── 请求合并：批量调用 vs 逐个调用
│    │
│    └─── 10.4 安全考量
│         ├── Prompt Injection 防御：对用户输入进行过滤
│         ├── 工具权限控制：最小权限原则（读写分离、操作范围限制）
│         ├── Rate Limiting：限制每用户的 Agent 调用频率
│         └── 敏感数据脱敏：日志中不记录 API Key / 用户隐私
│
└─── 11. 🎯 实战项目：视频脚本生成 Agent（P0 最终目标）
     │
     ├─── 11.1 项目架构设计
     │    │
     │    ├── 用户请求 → NestJS Controller → BullMQ 队列
     │    │              ↓
     │    │         [LangGraph Agent]
     │    │              ├── SupervisorNode  — 解析意图、制定计划
     │    │              ├── ScriptNode      — 调用 LLM 生成脚本
     │    │              ├── ReviewNode      — 质量审核（可选）
     │    │              └── VideoTaskNode   — 提交视频生成任务
     │    │              ↓
     │    │         [State 持久化] → PostgreSQL Checkpointer
     │    │              ↓
     │    │         SSE 流式推送 → 前端实时更新
     │    │
     │    └── State 设计
     │         ├── messages        — 对话历史
     │         ├── userIntent      — 用户原始意图
     │         ├── scripts         — 生成的脚本列表
     │         ├── videoTasks      — 视频任务状态列表
     │         ├── currentStep     — 当前执行步骤
     │         └── error           — 错误信息
     │
     ├─── 11.2 关键代码片段
     │    ├── 定义 State：Annotation.Root + addMessages
     │    ├── LLM 节点：model.bindTools(tools) → invoke → 返回 Partial<State>
     │    ├── 条件路由：toolsCondition + 自定义完成检测
     │    ├── 流式接口：app.stream() + SSE 推送
     │    └── 断点续跑：PostgresCheckpointer + thread_id
     │
     └─── 11.3 学习里程碑
          ├── 里程碑 1：Hello LangGraph — 单节点 LLM 问答图
          ├── 里程碑 2：ReAct Agent    — LLM 节点 + ToolNode + 条件路由
          ├── 里程碑 3：有记忆的 Agent — 接入 MemorySaver，多轮对话
          ├── 里程碑 4：Plan-Execute   — 规划器 + 执行器，处理复杂任务
          ├── 里程碑 5：流式输出       — stream() + NestJS SSE 接口
          └── 里程碑 6：生产级 Agent  — PostgresCheckpointer + Human-in-Loop + LangSmith
```

---

## LangGraph vs LangChain LCEL 对比

| 维度 | LangChain LCEL | LangGraph |
|------|---------------|-----------|
| **适用场景** | 固定流程、线性管道 | 循环、动态路由、复杂 Agent |
| **状态管理** | 无显式共享状态 | 显式 State，所有节点共享 |
| **控制流** | 顺序 / 有限分支 | 任意图结构（包含循环） |
| **持久化** | 不支持 | 内置 Checkpointer |
| **Human-in-Loop** | 不支持 | 原生支持 interrupt |
| **多 Agent** | 手动实现 | Supervisor / Swarm 模式 |
| **学习曲线** | 低 | 中等 |
| **何时用** | 简单 RAG、Prompt Chain | 生产级 Agent、复杂任务 |

---

## 核心 API 速查

```typescript
import { StateGraph, Annotation, START, END } from '@langchain/langgraph';
import { MemorySaver } from '@langchain/langgraph';
import { ToolNode, toolsCondition } from '@langchain/langgraph/prebuilt';
import { addMessages } from '@langchain/langgraph';
import { BaseMessage } from '@langchain/core/messages';
import { tool } from '@langchain/core/tools';
import { z } from 'zod';

// 1. 定义 State
const StateAnnotation = Annotation.Root({
  messages: Annotation<BaseMessage[]>({ reducer: addMessages }),
  taskCount: Annotation<number>(),
});

// 2. 定义工具
const myTool = tool(
  async ({ query }) => { return `搜索结果: ${query}`; },
  { name: 'search', description: '搜索信息', schema: z.object({ query: z.string() }) }
);

// 3. 创建节点
const llmNode = async (state: typeof StateAnnotation.State) => {
  const result = await model.bindTools([myTool]).invoke(state.messages);
  return { messages: [result] };
};

// 4. 构建图
const graph = new StateGraph(StateAnnotation)
  .addNode('agent', llmNode)
  .addNode('tools', new ToolNode([myTool]))
  .addEdge(START, 'agent')
  .addConditionalEdges('agent', toolsCondition)
  .addEdge('tools', 'agent');

// 5. 编译（带记忆）
const app = graph.compile({ checkpointer: new MemorySaver() });

// 6. 调用
const result = await app.invoke(
  { messages: [{ role: 'user', content: '你好' }] },
  { configurable: { thread_id: 'user-001' } }
);

// 7. 流式调用
for await (const chunk of app.stream(input, { streamMode: 'updates' })) {
  console.log(chunk);
}
```

---

## 推荐学习路径

| 阶段 | 重点内容 | 预计时间 | 对应里程碑 |
|------|---------|---------|----------|
| **第 1 天** | 理解 State / Node / Edge 三要素，跑通官方 QuickStart | 1 天 | 里程碑 1 |
| **第 2-3 天** | 构建 ReAct Agent（ToolNode + 条件路由 + 自定义工具） | 2 天 | 里程碑 2 |
| **第 4 天** | 接入 MemorySaver，实现多轮对话记忆 | 1 天 | 里程碑 3 |
| **第 5-6 天** | Plan-Execute 模式，处理复杂任务分解 | 2 天 | 里程碑 4 |
| **第 7 天** | 流式输出 + 对接 NestJS SSE 接口 | 1 天 | 里程碑 5 |
| **第 8-10 天** | 多 Agent 协作（Supervisor 模式）+ 生产级部署 | 3 天 | 里程碑 6 |

> 💡 **学习建议**：
> 1. 每个里程碑都要写出能跑的代码，不要只看文档
> 2. 遇到 LangGraph.js 文档不清楚的地方，参考 LangGraph Python 版（逻辑相同，语法略有差异）
> 3. 全程开启 LangSmith 追踪，直观看到每一步发生了什么
> 4. 优先用 GPT-4o-mini 开发（省钱），功能验证后再切换更强的模型

---

## 参考资源

- 📖 官方文档：https://langchain-ai.github.io/langgraphjs/
- 🎓 官方教程（Concepts）：https://langchain-ai.github.io/langgraphjs/concepts/
- 💻 How-to 指南：https://langchain-ai.github.io/langgraphjs/how-tos/
- 🐍 LangGraph Python（逻辑参考）：https://langchain-ai.github.io/langgraph/
- 🛠️ LangSmith：https://smith.langchain.com/
