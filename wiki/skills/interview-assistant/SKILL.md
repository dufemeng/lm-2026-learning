---
name: interview-assistant
description: Generates personalized technical interview questions and STAR story cards from a user's Claude Code CLI session history and project codebase. Use this skill whenever a user wants to prepare for a technical interview, especially when they built a project using Claude Code or other AI-assisted tools. Trigger on phrases like "帮我准备面试", "面试准备", "面试题", "help me prepare for my interview", "generate interview questions about my project", "turn my work into interview stories", "I have an interview next week about my project", or any time someone wants to talk about their engineering decisions in an interview context. Don't wait for explicit mention of "Claude Code" — if someone built a project and needs interview prep, use this skill.
---

# Interview Assistant

根据工程师的 Claude Code CLI session 历史和项目代码，生成定制化面试题和 STAR 故事卡。

核心价值：生成**"只有你能答的题"**——题目锚定在你的真实架构决策上，而不是通用八股题库。

---

## 使用前提

- 已安装 Claude Code CLI，且 `~/.claude/projects/` 下有 `.jsonl` session 文件
- Node.js 18+（运行 `session-extractor.mjs`）
- 需要分析的项目代码在本地

---

## 工作流程

### Step 1 — 确认输入

询问用户：

1. **项目目录路径**（必须）：`/path/to/your/project`
2. **目标职级**：资深前端 / 全栈工程师 / Agent 工程师
3. **目标 JD**（可选）：是否有招聘描述文本？

如果用户已在消息里提供了项目路径，直接进入 Step 2。

---

### Step 2 — 自动提取（运行脚本）

运行以下命令（`SKILL_DIR` 为本 skill 所在目录）：

```bash
bash {SKILL_DIR}/scripts/run.sh <project_path>
```

等待脚本完成，确认生成了：
- `extracted_decisions.md`（session 决策摘要，约 30–50KB）
- `code_summary.md`（代码架构摘要，约 5–10KB）

如果 session 数据量很大（>200MB），提示用户：
```bash
bash {SKILL_DIR}/scripts/run.sh <project_path> --days 14 --max-files 10
```

---

### Step 3 — 构建项目知识图谱

读取 `extracted_decisions.md` 和 `code_summary.md` 的内容。

按照 `{SKILL_DIR}/references/01-project-knowledge-builder.md` 的格式要求，
在**同一次分析**中交叉印证两份文档，构建知识图谱。

> 关键原则：必须在同一 context 中同时读取两份文档，不能先读一份再读另一份。
> 目的是发现"session 说要做但代码没做"的张力点——这是最高价值的面试话题。

将知识图谱输出保存到 `project_knowledge_graph.md`。

---

### Step 4 — 生成面试题

按照 `{SKILL_DIR}/references/02-interview-generator.md` 的格式，
基于知识图谱中的 TOP5 高价值决策生成面试题。

每条决策对应：基础确认题（×1）+ 深度追问题（×3）+ 扩展场景题（×1）。

将结果保存到 `interview_questions.md`。

---

### Step 5 — 生成 STAR 故事卡

按照 `{SKILL_DIR}/references/03-story-card-builder.md` 的格式，
将 TOP5 决策整理为可直接口述的 STAR 故事卡（每张 200–300 字，第一人称）。

将结果保存到 `story_cards.md`。

---

### 完成

告知用户生成了以下文件：

| 文件 | 内容 |
|------|------|
| `project_knowledge_graph.md` | 技术栈、决策清单、置信度标注 |
| `interview_questions.md` | 20–30 道定制面试题（含追问和评分要点） |
| `story_cards.md` | 5 张 STAR 故事卡（可直接口述） |

---

## 文件结构

```
interview-assistant/
├── SKILL.md              ← 本文件（skill 定义）
├── README.md             ← 详细设计文档
├── install.sh            ← curl 一键安装脚本
├── scripts/
│   ├── session-extractor.mjs  ← Step 2：三层过滤提取 session 决策对话
│   ├── code_analyzer.sh       ← Step 2：提取代码架构摘要
│   └── run.sh                 ← Step 2：编排入口
├── references/
│   ├── 01-project-knowledge-builder.md  ← Step 3 Prompt 模板
│   ├── 02-interview-generator.md         ← Step 4 Prompt 模板
│   └── 03-story-card-builder.md          ← Step 5 Prompt 模板
└── evals/
    └── evals.json        ← skill-creator 测试用例
```

---

## 边界处理

**session 数据稀少**：若 `extracted_decisions.md` < 5KB，提示用户：
"Session 内容较少，知识图谱将主要依赖代码摘要，决策置信度标注为 🟡 中。
建议补充回答：项目最难的技术问题是什么？你主动做了哪些工程化决策？"

**无 git 仓库**：`code_summary.md` 中 git 历史为空，跳过该节，其余正常处理。

**session 目录不存在**：提示用户确认 Claude Code CLI 已安装并使用过
（`~/.claude/projects/` 目录需存在）。
