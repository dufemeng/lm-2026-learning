# AGENTS.md

## 仓库概览

这是一个前端架构及相关技术的学习工作区。当前结构：

```
2026-learning/
├── architecture/        # 架构设计方法论笔记（中文）
├── langchain.js/        # LangChain.js 学习项目（空）
└── nest.js/             # NestJS 学习项目（空）
```

## 构建/Lint/测试命令

尚未配置构建系统。添加新项目时：

- **NestJS 项目**（`nest.js/`）：使用 `npm run build`、`npm run test`、`npm run test:e2e`、`npm run lint`。运行单个测试：`npm run test -- --testNamePattern="test name"` 或 `npm run test -- path/to/spec.ts`
- **LangChain.js 项目**（`langchain.js/`）：使用 `npm run build`、`npm run test`、`npm run lint`。运行单个测试：`npx vitest run path/to/test.spec.ts` 或 `npx jest path/to/test.spec.ts`
- 每个子项目应有独立的 `package.json`，依赖隔离

## 代码风格规范

### 通用规范
- 所有新代码使用 TypeScript；在 `tsconfig.json` 中启用 `strict` 模式
- 新项目优先使用 `pnpm` 作为包管理器
- 2 空格缩进，单引号，尾逗号（ES5）
- 最大行长：100 字符
- 文件末尾必须有换行符

### 导入规范
- 排列顺序：Node 内置模块 → 外部依赖 → 内部模块 → 相对路径导入
- 项目扩大后使用 `paths` 别名进行绝对导入（如 `@/services/`）
- 优先使用具名导出，避免默认导出（React 组件和 NestJS 模块除外）
- 各导入区块之间用空行分隔

### 命名规范
- **文件**：工具/服务用 kebab-case（`user-service.ts`），组件/类用 PascalCase（`UserProfile.tsx`）
- **变量/函数**：camelCase（`getUserById`）
- **常量**：UPPER_SNAKE_CASE（`MAX_RETRY_COUNT`）
- **类型/接口**：PascalCase（`UserResponse`、`CreateUserDto`）
- **NestJS**：遵循 Angular 风格命名：`*.module.ts`、`*.controller.ts`、`*.service.ts`、`*.dto.ts`、`*.entity.ts`

### 类型规范
- 避免使用 `any`；使用 `unknown` 并通过类型守卫收窄
- 对象形状优先使用 `interface`，联合/交叉/计算类型使用 `type`
- 使用 Zod 或 class-validator 对外部数据进行运行时校验
- 类型导出至集中管理的 `types.ts` 或与消费模块同级

### 错误处理
- 使用继承 `Error` 的自定义错误类，附带错误码
- NestJS：使用内置异常（`HttpException`、`NotFoundException` 等）和异常过滤器
- LangChain：用 try/catch 包裹 LLM 调用，实现指数退避重试
- 严禁静默吞掉错误；必须记录日志或重新抛出

### NestJS 专项
- 遵循模块化架构：一个功能 = 一个模块
- 使用依赖注入；避免直接导入服务
- 所有请求/响应用 DTO 定义；使用 `class-validator` 装饰器
- Guard 做认证，Pipe 做校验，Interceptor 做横切关注点
- 保持 Controller 精简；业务逻辑放在 Service 中

### LangChain.js 专项
- 使用 `Runnable` 接口构建可组合的链
- 将 prompt 放在独立文件/模板中，便于迭代
- 使用回调（callbacks）记录和监控 LLM 调用
- 适时缓存昂贵的 LLM 响应

## 测试

- 单元测试：`*.spec.ts` 与源文件同目录
- E2E 测试：`*.e2e-spec.ts` 放在 `test/` 目录
- 遵循 Arrange-Act-Assert 模式
- Mock 外部依赖（数据库、API、LLM）
- 追求业务逻辑的有效覆盖，而非 100% 行覆盖率

## Git 规范

- 使用 Conventional Commits：`feat:`、`fix:`、`docs:`、`refactor:`、`test:`、`chore:`
- 分支命名：`feature/`、`fix/`、`docs/` 前缀 + kebab-case 描述
- 保持提交原子性，提交信息具有描述性

## 添加新项目

启动新的学习项目时：
1. 在对应分类下创建新目录
2. 使用 `pnpm init` 初始化并配置 TypeScript
3. 添加简要 `README.md` 说明学习目标
4. 遵循上述代码风格规范
