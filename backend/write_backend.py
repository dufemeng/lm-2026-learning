content = r"""# 🖥️ 后端知识体系 · NestJS 技术栈学习思维导图

> 面向前端转全栈，以 **NestJS + Prisma + Redis + BullMQ + PostgreSQL** 为核心技术栈
> 按「重要程度 × 使用频率 × 理解难度」由浅入深排列
> 优先级：P0 必须掌握 → P1 项目中会用到 → P2 面试加分 → P3 了解概念

---

## 技术栈全景

```
用户请求
   ↓
[NestJS 应用]
   ├── Controller   — 路由层，接收 HTTP 请求
   ├── Guard        — 认证授权（JWT 校验）
   ├── Pipe         — 参数校验（class-validator + DTO）
   ├── Interceptor  — 横切逻辑（日志、响应格式化、缓存）
   ├── Service      — 业务逻辑
   └── Module       — 依赖注入容器
         ↓
[数据层]
   ├── Prisma ORM   → PostgreSQL（持久化数据）
   ├── Redis        → 缓存 / 分布式锁 / Pub/Sub
   └── BullMQ       → 消息队列（基于 Redis，处理异步长任务）
```

---

## 思维导图

```
NestJS 后端知识体系
│
├─── 🟢 Level 1：NestJS 核心基础（前端易理解，第一周必须掌握）
│    ── 优先级 P0
│    │
│    ├─── 1.1 NestJS 框架架构
│    │    │
│    │    ├── [模块化体系（Module）]
│    │    │   ├── 每个功能域一个 Module（类比前端路由模块）
│    │    │   │   └── AppModule → UserModule → TaskModule → VideoModule
│    │    │   ├── @Module 装饰器的四个字段
│    │    │   │   ├── imports   — 导入其他模块（使用其导出的 Provider）
│    │    │   │   ├── providers — 注册 Service / Repository（依赖注入容器托管）
│    │    │   │   ├── controllers — 注册 Controller
│    │    │   │   └── exports   — 导出 Provider 给其他模块使用
│    │    │   └── 全局模块：@Global() — 一次注册，全局可用（如 ConfigModule）
│    │    │
│    │    ├── [依赖注入（DI）]
│    │    │   ├── 什么是 DI：类不自己 new 依赖，由框架注入
│    │    │   ├── @Injectable() — 标记类可被注入
│    │    │   ├── 构造函数注入（最常用）
│    │    │   │   └── constructor(private readonly userService: UserService) {}
│    │    │   ├── 前端类比：类似 React Context.Provider 自动分发依赖
│    │    │   └── 好处：解耦 / 可测试（Mock 替换）/ 生命周期管理
│    │    │
│    │    ├── [Controller 控制器]
│    │    │   ├── 职责：只负责路由映射和请求/响应处理，不写业务逻辑
│    │    │   ├── 常用装饰器
│    │    │   │   ├── @Controller('tasks')        — 路由前缀
│    │    │   │   ├── @Get() / @Post() / @Put() / @Patch() / @Delete()
│    │    │   │   ├── @Param('id')                — 路径参数
│    │    │   │   ├── @Query()                    — Query String
│    │    │   │   ├── @Body()                     — 请求体
│    │    │   │   └── @Headers() / @Req() / @Res()
│    │    │   └── 响应码：@HttpCode(201)
│    │    │
│    │    ├── [Service 服务层]
│    │    │   ├── 职责：所有业务逻辑放这里，Controller 只调用 Service
│    │    │   ├── @Injectable() 标记
│    │    │   └── 可注入其他 Service / Repository / 第三方客户端
│    │    │
│    │    └── [请求生命周期与中间件体系]
│    │         ├── 执行顺序（从外到内）：
│    │         │   Middleware → Guard → Interceptor(前) → Pipe → Handler → Interceptor(后) → Filter
│    │         ├── Middleware（中间件）
│    │         │   ├── 类似 Express middleware，最先执行
│    │         │   └── 场景：请求日志、IP 白名单
│    │         ├── Guard（守卫）— 认证入口
│    │         │   ├── 返回 true 放行，false 抛 403
│    │         │   ├── @UseGuards(JwtAuthGuard) 应用在 Controller 或方法上
│    │         │   └── 场景：JWT 校验、角色权限校验
│    │         ├── Pipe（管道）— 参数校验入口
│    │         │   ├── 校验或转换请求参数
│    │         │   ├── 内置：ValidationPipe（配合 class-validator 自动校验 DTO）
│    │         │   └── ParseIntPipe / ParseUUIDPipe — 类型转换
│    │         ├── Interceptor（拦截器）
│    │         │   ├── 前后切面，可修改请求和响应
│    │         │   └── 场景：统一响应格式包装、日志记录、响应缓存
│    │         └── ExceptionFilter（异常过滤器）
│    │              ├── 捕获所有未处理异常，返回统一错误格式
│    │              └── 内置：HttpException / NotFoundException / ForbiddenException
│    │
│    ├─── 1.2 HTTP 状态码与 RESTful 规范（NestJS 实践）
│    │    ├── 状态码正确使用
│    │    │   ├── 200 OK         — GET / PUT / PATCH 成功
│    │    │   ├── 201 Created    — POST 创建成功（配合 @HttpCode(201)）
│    │    │   ├── 204 No Content — DELETE 成功（无响应体）
│    │    │   ├── 400 Bad Request — 参数错误（ValidationPipe 自动返回）
│    │    │   ├── 401 Unauthorized — 未携带/无效 Token（JwtAuthGuard 返回）
│    │    │   ├── 403 Forbidden  — 无权限（RolesGuard 返回）
│    │    │   ├── 404 Not Found  — throw new NotFoundException()
│    │    │   └── 409 Conflict   — 资源冲突（如重复创建）
│    │    ├── RESTful URL 设计
│    │    │   ├── @Controller('tasks')            → /tasks
│    │    │   ├── @Get(':id')                     → GET /tasks/:id
│    │    │   ├── @Post()                         → POST /tasks
│    │    │   └── @Get(':id/scripts')             → GET /tasks/:id/scripts
│    │    └── 统一响应结构（用 TransformInterceptor 实现）
│    │         └── { success, data, message, timestamp }
│    │
│    └─── 1.3 配置管理（ConfigModule）
│         ├── @nestjs/config — NestJS 官方配置模块
│         ├── .env 文件 + ConfigService 读取环境变量
│         ├── 配置校验（Joi 或 Zod，启动时快速发现缺失配置）
│         └── 多环境：.env.development / .env.production
│
├─── 🟡 Level 2：数据层（Prisma + PostgreSQL，第一周重点）
│    ── 优先级 P0
│    │
│    ├─── 2.1 Prisma ORM
│    │    ├── [Schema 定义]
│    │    │   ├── schema.prisma — 数据模型单一来源（类比 TypeScript 类型定义）
│    │    │   ├── 模型示例
│    │    │   │   ├── model User { id / email / role / createdAt / tasks Task[] }
│    │    │   │   ├── model Task { id / status / version / userId / scripts Script[] }
│    │    │   │   └── model Script { id / content / taskId }
│    │    │   ├── 字段类型：String / Int / DateTime / Boolean / Json
│    │    │   ├── 关系定义：@relation（一对多 / 多对多）
│    │    │   └── 索引：@@index([field]) / @@unique([field])
│    │    │
│    │    ├── [Migration 数据库迁移]
│    │    │   ├── prisma migrate dev      — 开发环境：生成并执行迁移
│    │    │   ├── prisma migrate deploy   — 生产环境：仅执行已有迁移
│    │    │   ├── prisma db push          — 原型阶段快速同步（不生成迁移文件）
│    │    │   └── 迁移 = 数据库 DDL 变更的 Git 版本控制
│    │    │
│    │    ├── [Prisma Client CRUD]
│    │    │   ├── prisma.user.findUnique({ where: { id } })
│    │    │   ├── prisma.user.findMany({ where: {}, orderBy: {}, take: 20, skip: 0 })
│    │    │   ├── prisma.task.create({ data: { ... } })
│    │    │   ├── prisma.task.update({ where: { id }, data: { ... } })
│    │    │   └── prisma.task.delete({ where: { id } })
│    │    │
│    │    ├── [关联查询 — 解决 N+1 问题]
│    │    │   ├── N+1 问题：查 N 个 Task + 每个 Task 再查 Scripts = N+1 次查询
│    │    │   ├── 解决：include 预加载
│    │    │   │   └── prisma.task.findMany({ include: { scripts: true, user: true } })
│    │    │   ├── select 只查需要字段（减少数据传输）
│    │    │   └── 复杂查询用 prisma.$queryRaw 原生 SQL
│    │    │
│    │    ├── [事务（Transaction）] ⭐ 重要
│    │    │   ├── ACID 四特性
│    │    │   │   ├── A — 原子性：批量创建脚本失败时回滚任务创建
│    │    │   │   ├── C — 一致性：不会出现「Task 存在但 Scripts 为空」的中间态
│    │    │   │   ├── I — 隔离性：并发请求互不干扰
│    │    │   │   └── D — 持久性：提交后永久保存
│    │    │   ├── 隔离级别（了解即可，默认 REPEATABLE READ）
│    │    │   │   ├── READ COMMITTED  — 只读已提交（避免脏读）
│    │    │   │   └── SERIALIZABLE    — 完全串行（最安全，最慢）
│    │    │   └── Prisma 事务写法
│    │    │        ├── 顺序事务：prisma.$transaction([op1, op2])
│    │    │        └── 交互式事务：prisma.$transaction(async (tx) => { ... })
│    │    │
│    │    └── [分页设计]
│    │         ├── Offset 分页：skip / take（简单，大数据量慢）
│    │         └── Cursor 分页：cursor / take（推荐，适合无限滚动）
│    │
│    ├─── 2.2 索引 & 软删除
│    │    ├── Prisma Schema 中配置索引
│    │    │   ├── @@index([userId])           — 外键全部加索引
│    │    │   ├── @@unique([email])            — 唯一约束
│    │    │   └── @@index([status, createdAt]) — 联合索引（任务列表查询）
│    │    └── 软删除（Soft Delete）
│    │         ├── 加 deletedAt DateTime? 字段
│    │         ├── 查询时过滤：where: { deletedAt: null }
│    │         └── 好处：可恢复、保留审计记录、不破坏外键
│    │
│    └─── 2.3 DTO 与数据校验（class-validator）
│         ├── DTO：定义接口输入输出结构（类比 TypeScript Interface）
│         ├── class-validator 装饰器
│         │   ├── @IsString() / @IsEmail() / @IsUUID()
│         │   ├── @IsNotEmpty() / @IsOptional()
│         │   ├── @Min() / @Max() / @Length()
│         │   └── @IsEnum(TaskStatus)
│         ├── main.ts 全局启用
│         │   └── app.useGlobalPipes(new ValidationPipe({ whitelist: true, transform: true }))
│         └── whitelist: true — 自动过滤 DTO 未定义的字段（防止额外字段注入）
│
├─── 🟡 Level 3：缓存层（Redis，第二周重点）
│    ── 优先级 P0-P1
│    │
│    ├─── 3.1 Redis 基础与 NestJS 集成
│    │    ├── 集成：ioredis 直接使用（推荐） / @nestjs/cache-manager（简单场景）
│    │    ├── 数据类型与场景
│    │    │   ├── String  — 缓存单个值、计数器（Token 用量）、分布式锁
│    │    │   ├── Hash    — 缓存对象（用户 Session）
│    │    │   ├── List    — 简单队列（BullMQ 底层使用）
│    │    │   ├── Set     — 去重集合（在线用户 ID）
│    │    │   └── ZSet    — 有序集合（优先级队列、排行榜）
│    │    └── TTL 设计原则
│    │         ├── 频繁变动 → 短 TTL（5-60 秒）
│    │         ├── 相对稳定 → 中 TTL（10-30 分钟）
│    │         └── LLM 生成结果 → 长 TTL（24 小时）
│    │
│    ├─── 3.2 缓存策略（Cache-Aside）⭐
│    │    ├── 读：先查 Redis → 命中直接返回 → 未命中查 DB → 写入 Redis
│    │    ├── 写：先写 DB → 再删 Redis（注意：是删，不是更新）
│    │    ├── 三大缓存问题 ⭐ 面试必考
│    │    │   ├── 缓存穿透：查询不存在的 key，每次都打到 DB
│    │    │   │   └── 解决：缓存空值（TTL 设短）/ 布隆过滤器
│    │    │   ├── 缓存击穿：热点 key 过期瞬间，大量请求涌入 DB
│    │    │   │   └── 解决：Redis SETNX 互斥锁，只允许一个请求重建缓存
│    │    │   └── 缓存雪崩：大量 key 同时过期，DB 被打垮
│    │    │        └── 解决：TTL 加随机偏移（TTL + random(0, 60s)）
│    │    └── LLM 结果缓存（Agent 项目核心优化）
│    │         ├── key = sha256(model + prompt)
│    │         └── 相同生成请求命中缓存，直接返回，节省 Token 成本
│    │
│    └─── 3.3 分布式锁（Redis 实现）⭐
│         ├── 场景：NestJS 多实例部署时，进程内锁失效
│         ├── 原理：SET key value NX PX timeout
│         │   ├── NX = Not eXists（原子 CAS，保证只有一个实例获锁）
│         │   └── PX = 毫秒过期（持锁者崩溃后锁自动释放，防止死锁）
│         └── 场景
│              ├── 定时任务防重复执行（多实例只有一个跑）
│              └── 批量任务防并发冲突（同一 Job 不被多 Worker 抢占）
│
├─── 🟠 Level 4：异步任务层（BullMQ，第二周核心）
│    ── 优先级 P0（视频生成项目的核心后端能力）
│    │
│    ├─── 4.1 为什么必须用消息队列
│    │    ├── 解耦：Controller 只入队返回 taskId，不直接调用 LLM
│    │    ├── 异步：视频生成耗时几分钟，不阻塞 HTTP 连接
│    │    └── 削峰：高并发时缓冲请求，Worker 按能力消费
│    │
│    ├─── 4.2 BullMQ 与 NestJS 集成
│    │    ├── 安装：@nestjs/bullmq + bullmq
│    │    ├── 注册队列：BullModule.registerQueue({ name: 'video-gen' })
│    │    ├── 生产者（Service 中）
│    │    │   └── @InjectQueue('video-gen') private queue: Queue
│    │    │       await this.queue.add('generate', payload, { attempts: 3 })
│    │    └── 消费者（Processor）
│    │         ├── @Processor('video-gen')
│    │         └── @Process('generate') async handle(job: Job) { ... }
│    │
│    ├─── 4.3 Job 状态机
│    │    ├── waiting   — 队列中等待
│    │    ├── active    — Worker 正在处理
│    │    ├── completed — 处理成功（自动清理 removeOnComplete: true）
│    │    └── failed    — 达到最大重试后失败（转入 Dead Letter Queue）
│    │
│    ├─── 4.4 重试策略（指数退避）⭐
│    │    ├── attempts: 3
│    │    ├── backoff: { type: 'exponential', delay: 1000 }  — 1s / 2s / 4s
│    │    ├── 死信队列（Failed Queue）— 最终失败后告警人工处理
│    │    └── 区分可重试 vs 不可重试错误
│    │         ├── 可重试：网络超时 / Rate Limit / 5xx
│    │         └── 不可重试：参数错误 / 认证失败 / 业务规则冲突
│    │
│    ├─── 4.5 幂等性设计 ⭐
│    │    ├── 什么是幂等：同一操作执行 N 次，结果与执行一次相同
│    │    ├── 为什么需要：客户端超时重试时，防止重复创建任务/重复扣费
│    │    ├── NestJS 实现
│    │    │   ├── 客户端请求头传 X-Idempotency-Key（UUID）
│    │    │   ├── IdempotencyInterceptor 查 Redis 是否存在该 key
│    │    │   └── 存在直接返回缓存结果；不存在则处理并写入 Redis（TTL 24h）
│    │    └── 数据库唯一约束兜底：@@unique([userId, idempotencyKey])
│    │
│    └─── 4.6 任务进度推送（Redis Pub/Sub + SSE）
│         ├── Worker 完成阶段性操作 → redis.publish('task:progress', { taskId, progress })
│         ├── NestJS SSE Controller 订阅 Redis Channel
│         └── 前端 EventSource API 监听实时进度
│
├─── 🟠 Level 5：认证授权层（第二周）
│    ── 优先级 P1
│    │
│    ├─── 5.1 JWT 认证
│    │    ├── 安装：@nestjs/jwt + @nestjs/passport + passport-jwt
│    │    ├── 双令牌策略
│    │    │   ├── Access Token：短期（15min），网络传输
│    │    │   └── Refresh Token：长期（7d），存数据库，可主动吊销
│    │    ├── JwtAuthGuard 全局注册 + @Public() 标记公开接口
│    │    └── 安全要点
│    │         ├── JWT_SECRET 存 .env，不硬编码
│    │         └── Token 存 httpOnly Cookie（防 XSS 窃取）
│    │
│    ├─── 5.2 RBAC 权限控制
│    │    ├── Prisma User 模型加 role 字段：enum Role { USER ADMIN }
│    │    ├── @Roles('admin') 自定义装饰器（SetMetadata）
│    │    └── RolesGuard 读取元数据 + request.user.role 校验
│    │
│    └─── 5.3 API Key 认证（Server-to-Server）
│         ├── 场景：Agent 调用外部视频 API，机器间认证
│         ├── ApiKeyGuard 读取 X-Api-Key 请求头，查数据库校验
│         └── 密钥 SHA-256 哈希存储（不存明文）
│
├─── 🟠 Level 6：锁与并发控制（第三周）
│    ── 优先级 P1
│    │
│    ├─── 6.1 悲观锁（Pessimistic Lock）
│    │    ├── 思想：操作前先加排他锁，假设冲突一定发生
│    │    ├── Prisma：prisma.$queryRaw`SELECT ... FOR UPDATE`
│    │    ├── 场景：扣减用量配额（高并发防超限）
│    │    └── 缺点：性能低，有死锁风险
│    │
│    ├─── 6.2 乐观锁（Optimistic Lock）⭐
│    │    ├── 思想：提交时检查 version，冲突则重试
│    │    ├── Prisma 实现
│    │    │   ├── Schema 加 version Int @default(0)
│    │    │   └── update where: { id, version } data: { ..., version: { increment: 1 } }
│    │    │       → version 不匹配 → 更新 0 行 → 捕获并重试
│    │    ├── 场景：任务状态流转（防并发写同一状态）
│    │    └── 优点：无锁高并发；缺点：高冲突时重试次数多
│    │
│    └─── 6.3 死锁预防
│         ├── 所有事务按相同顺序访问资源
│         ├── 设置 lock_timeout（超时自动释放）
│         └── 事务内不做网络 I/O，缩短持锁时间
│
├─── 🟠 Level 7：限流与稳健性（第三周）
│    ── 优先级 P1-P2
│    │
│    ├─── 7.1 限流（Rate Limiting）
│    │    ├── 为什么：防 API 滥用，控制 LLM 调用成本
│    │    ├── NestJS：@nestjs/throttler
│    │    │   ├── 全局：ThrottlerModule.forRoot({ ttl: 60000, limit: 10 })
│    │    │   └── 局部：@Throttle({ default: { limit: 3, ttl: 60000 } })
│    │    └── 多实例共享：ThrottlerStorageRedisService（计数存 Redis）
│    │
│    ├─── 7.2 熔断（Circuit Breaker）
│    │    ├── 场景：OpenAI / 视频生成 API 不稳定时快速失败
│    │    ├── 状态机：Closed → Open（快速失败）→ Half-Open（探测）
│    │    ├── NestJS：opossum 库封装外部调用
│    │    └── 熔断期间 Job 转入延迟队列等待恢复
│    │
│    └─── 7.3 服务降级（Fallback）
│         ├── 主服务不可用时返回兜底结果
│         └── 场景：LLM API 熔断时返回缓存的历史结果
│
├─── 🔴 Level 8：日志与可观测性（第三周）
│    ── 优先级 P1
│    │
│    ├─── 8.1 结构化日志（nestjs-pino）
│    │    ├── pino：高性能 JSON 日志，NestJS 首选
│    │    ├── 日志级别
│    │    │   ├── error  — 需立即处理（5xx / 未捕获异常）
│    │    │   ├── warn   — 非致命问题（重试次数过多）
│    │    │   ├── info   — 重要业务事件（任务创建 / 状态变更）
│    │    │   └── debug  — 调试信息（生产环境关闭）
│    │    ├── 必要字段：{ timestamp, level, message, requestId, userId, duration }
│    │    └── 绝不输出：密码 / Token / 完整个人信息
│    │
│    ├─── 8.2 链路追踪（X-Request-ID）
│    │    ├── 每个请求生成唯一 requestId（UUID v4）
│    │    ├── RequestIdMiddleware 注入到 AsyncLocalStorage（无需参数传递）
│    │    ├── 所有日志自动携带 requestId，包括 BullMQ Worker 中
│    │    └── 响应头返回 X-Request-ID，前端报错时可提供给后端排查
│    │
│    └─── 8.3 全局异常过滤器（AllExceptionsFilter）
│         ├── 统一捕获所有异常，返回标准错误结构
│         ├── HttpException → 按状态码返回
│         └── 未知异常 → 返回 500 + 记录 error 级别日志
│
├─── 🔴 Level 9：架构设计模式（第三四周）
│    ── 优先级 P1-P2（面试加分）
│    │
│    ├─── 9.1 Repository 模式
│    │    ├── 为什么：Service 不直接用 PrismaService，通过 Repository 抽象数据层
│    │    ├── TaskRepository 封装所有 Task 相关 DB 操作
│    │    ├── 好处：单元测试可 Mock Repository，不需要真实 DB
│    │    └── @Injectable() 注册为 Provider，注入到 Service
│    │
│    ├─── 9.2 任务状态机设计
│    │    ├── 视频生成任务状态机
│    │    │   ├── PENDING    → QUEUED     （入队成功）
│    │    │   ├── QUEUED     → PROCESSING （Worker 开始处理）
│    │    │   ├── PROCESSING → COMPLETED  （生成成功）
│    │    │   ├── PROCESSING → FAILED     （达到最大重试）
│    │    │   └── FAILED     → QUEUED     （手动重试）
│    │    ├── Prisma：enum TaskStatus { PENDING QUEUED PROCESSING COMPLETED FAILED }
│    │    └── Service 校验合法转换，非法转换抛 BadRequestException
│    │
│    ├─── 9.3 CQRS（@nestjs/cqrs）— 了解即可
│    │    ├── Command（写）：CreateTaskCommand → CreateTaskHandler
│    │    ├── Query（读）：GetTaskQuery → GetTaskHandler
│    │    ├── Event：TaskCompletedEvent → 通知 / 统计 / 清缓存
│    │    └── 适用场景：复杂业务时引入，MVP 阶段不需要
│    │
│    └─── 9.4 事件驱动（@nestjs/event-emitter）
│         ├── 进程内事件总线（不跨服务，不持久化）
│         ├── 任务完成后 emit → 通知模块 / 统计模块各自监听
│         └── 与 BullMQ 区别：EventEmitter 进程内同步，BullMQ 跨进程持久化
│
└─── 🔵 Level 10：部署与运维（第四周）
     ── 优先级 P2
     │
     ├─── 10.1 Docker 容器化
     │    ├── Dockerfile 多阶段构建（builder + runner，减小镜像体积）
     │    ├── docker-compose.yml 本地一键启动
     │    │   ├── nestjs-app  — 应用（端口 3000）
     │    │   ├── postgres    — 数据库（端口 5432）
     │    │   ├── redis       — 缓存 + 队列（端口 6379）
     │    │   └── bull-board  — BullMQ 可视化监控（端口 3001）
     │    └── 环境变量通过 env_file 注入，不 COPY .env 进镜像
     │
     ├─── 10.2 安全加固
     │    ├── helmet — 设置安全 HTTP 响应头
     │    ├── CORS 配置白名单域名（不用 origin: '*'）
     │    ├── ValidationPipe whitelist: true — 过滤额外字段
     │    └── 依赖扫描：pnpm audit / Snyk
     │
     └─── 10.3 CI/CD（GitHub Actions）
          ├── 触发：push main / PR merge
          ├── 步骤：pnpm install → lint → type-check → test → build → deploy
          ├── 部署后执行 prisma migrate deploy
          └── main 分支保护：需 PR + CI 全绿才能合并
```

---

## 📅 NestJS 技术栈学习优先级总览

| 层级 | 模块 | 核心技术 | 重要程度 | 学习时机 |
|------|------|---------|---------|---------|
| 🟢 L1 | NestJS 框架核心 | Module / Controller / Service / DI | ⭐⭐⭐⭐⭐ | Week 1 Day 1-3 |
| 🟢 L1 | HTTP 规范 & 配置管理 | @nestjs/config / ValidationPipe | ⭐⭐⭐⭐⭐ | Week 1 Day 1-2 |
| 🟡 L2 | Prisma ORM | Schema / Migration / Client | ⭐⭐⭐⭐⭐ | Week 1 Day 3-5 |
| 🟡 L2 | DTO 校验 | class-validator / class-transformer | ⭐⭐⭐⭐⭐ | Week 1 Day 3 |
| 🟡 L2 | 事务 | Prisma $transaction + ACID | ⭐⭐⭐⭐⭐ | Week 1 Day 5-7 |
| 🟡 L3 | Redis 缓存 | ioredis / Cache-Aside 策略 | ⭐⭐⭐⭐⭐ | Week 2 Day 1-2 |
| 🟡 L3 | 分布式锁 | Redis SETNX | ⭐⭐⭐⭐ | Week 2 Day 3 |
| 🟠 L4 | BullMQ 消息队列 | @nestjs/bullmq / Processor | ⭐⭐⭐⭐⭐ | Week 2 Day 1-4 |
| 🟠 L4 | 幂等性设计 | X-Idempotency-Key + Redis | ⭐⭐⭐⭐⭐ | Week 2 Day 4-5 |
| 🟠 L5 | JWT 认证 | @nestjs/jwt / JwtAuthGuard | ⭐⭐⭐⭐⭐ | Week 2 Day 5-7 |
| 🟠 L5 | RBAC 授权 | RolesGuard / @Roles() 装饰器 | ⭐⭐⭐⭐ | Week 2 Day 7 |
| 🟠 L6 | 乐观锁 | version 字段 / Prisma CAS | ⭐⭐⭐⭐ | Week 3 Day 1-2 |
| 🟠 L7 | 限流 | @nestjs/throttler + Redis | ⭐⭐⭐⭐ | Week 3 Day 2-3 |
| 🟠 L7 | 熔断重试 | opossum + BullMQ backoff | ⭐⭐⭐ | Week 3 Day 3-4 |
| 🔴 L8 | 日志链路 | nestjs-pino + X-Request-ID | ⭐⭐⭐⭐ | Week 3 Day 4-5 |
| 🔴 L9 | 状态机设计 | Prisma enum + Service 校验 | ⭐⭐⭐⭐ | Week 3 Day 5-7 |
| 🔴 L9 | 事件驱动 | @nestjs/event-emitter | ⭐⭐⭐ | Week 3-4 |
| 🔵 L10 | Docker 容器化 | Dockerfile + docker-compose | ⭐⭐⭐⭐ | Week 4 Day 1-2 |
| 🔵 L10 | CI/CD | GitHub Actions | ⭐⭐⭐ | Week 4 Day 3-4 |

---

## 🎯 视频 Agent 项目完整技术映射（NestJS 视角）

```
业务功能                   NestJS 实现
───────────────────────────────────────────────────────────────────
用户注册/登录          →   AuthModule：POST /auth/register & /auth/login
                            bcrypt 哈希密码，JwtService 签发双令牌
                            Prisma User 模型 + @IsEmail DTO 校验

API 鉴权               →   全局 JwtAuthGuard + @Public() 公开接口跳过
                            RolesGuard 控制管理后台权限

提交生成任务（防重）   →   POST /tasks 携带 X-Idempotency-Key
                            IdempotencyInterceptor 查 Redis 去重
                            Prisma 创建 Task（status: PENDING）
                            BullMQ 入队，返回 { taskId }

执行脚本生成 Agent     →   BullMQ Processor 消费 Job
                            更新 Task status: PROCESSING
                            调用 LangChain.js Agent 生成脚本
                            Prisma $transaction 批量创建 Script（原子性）
                            更新 Task status: COMPLETED
                            redis.publish('task:progress', data)

前端实时进度推送       →   GET /tasks/:id/progress（SSE）
                            NestJS Controller 订阅 Redis Channel 推送

LLM 结果缓存           →   key = sha256(model + prompt)，TTL 24h
                            相同请求命中缓存直接返回，节省 Token 成本

批量并发控制           →   BullMQ concurrency: 3（同时最多 3 个 Worker）
                            乐观锁 version 字段防并发状态覆盖
                            @nestjs/throttler 限制用户提交频率

外部 API 保护          →   opossum 熔断（OpenAI / 视频 API）
                            BullMQ 指数退避重试
                            降级：熔断期间返回缓存历史结果

文件存储               →   StorageService 生成 OSS 预签名 URL
                            前端直传 OSS，后端只存文件元信息

线上问题排查           →   nestjs-pino JSON 日志 + X-Request-ID 全链路
                            Bull Board 可视化查看队列状态和失败 Job
                            Prisma queryEvent 监控慢查询（> 200ms 告警）
```

> 💡 **学习建议**：先把 `Module → Controller → Service → Prisma` 这条基础链路跑通，
> 其他所有模块（Redis / BullMQ / JWT / Guard）都以 Provider 形式注入进来，
> 越到后面越顺手。每学一个概念立刻在项目中找到对应代码落脚点实现一遍。
"""

with open('/Users/loomisli/Desktop/loomisli/2026-learning/backend/backend-mindmap.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done!", "Size:", len(content), "bytes")
