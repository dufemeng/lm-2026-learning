#!/usr/bin/env bash
# install.sh — Interview Assistant 一键安装脚本
#
# 安装方式（一行命令）：
#   curl -fsSL https://raw.githubusercontent.com/dufemeng/lm-2026-learning/main/wiki/skills/interview-assistant/install.sh | bash
#
# 安装内容：
#   ~/.interview-assistant/           — 工具脚本
#   ~/.claude/commands/interview-assistant.md  — Claude Code CLI 斜杠命令

set -euo pipefail

REPO_RAW="https://raw.githubusercontent.com/dufemeng/lm-2026-learning/main/wiki/skills/interview-assistant"
INSTALL_DIR="$HOME/.interview-assistant"
CLAUDE_COMMANDS_DIR="$HOME/.claude/commands"

# ── 颜色输出 ──────────────────────────────────────────────────────────────────
green()  { printf "\033[32m%s\033[0m\n" "$*"; }
yellow() { printf "\033[33m%s\033[0m\n" "$*"; }
red()    { printf "\033[31m%s\033[0m\n" "$*"; }

echo ""
echo "============================================================"
echo "  Interview Assistant — 安装程序"
echo "============================================================"
echo ""

# ── 前置检查 ──────────────────────────────────────────────────────────────────
if ! command -v curl &>/dev/null; then
  red "❌ 未找到 curl，请先安装 curl"
  exit 1
fi

if ! command -v node &>/dev/null; then
  yellow "⚠️  未找到 node。运行工具时需要 Node.js 18+。"
  yellow "   安装：https://nodejs.org/ 或 brew install node"
fi

# ── 创建目录 ──────────────────────────────────────────────────────────────────
mkdir -p "$INSTALL_DIR/prompts"
mkdir -p "$CLAUDE_COMMANDS_DIR"

# ── 下载脚本文件 ──────────────────────────────────────────────────────────────
echo "📥 下载脚本文件到 $INSTALL_DIR ..."

files=(
  "session-extractor.mjs"
  "code_analyzer.sh"
  "run.sh"
  "prompts/01-project-knowledge-builder.md"
  "prompts/02-interview-generator.md"
  "prompts/03-story-card-builder.md"
)

for f in "${files[@]}"; do
  printf "  %-50s" "$f"
  curl -fsSL "$REPO_RAW/$f" -o "$INSTALL_DIR/$f"
  green "✓"
done

# 赋予脚本执行权限
chmod +x "$INSTALL_DIR/run.sh" "$INSTALL_DIR/code_analyzer.sh" 2>/dev/null || true

# ── 安装 Claude Code CLI 斜杠命令 ─────────────────────────────────────────────
COMMAND_FILE="$CLAUDE_COMMANDS_DIR/interview-assistant.md"

cat > "$COMMAND_FILE" << 'CLAUDE_CMD'
你是面试助手（Interview Assistant）。根据工程师的 Claude Code 开发 session 和项目代码，生成定制化面试题和 STAR 故事卡。

## 执行步骤

**输入参数**：`$ARGUMENTS`（项目目录路径，如 `/path/to/my-project`）

### Step 1 — 自动提取（运行脚本）

运行以下命令：

```bash
bash ~/.interview-assistant/run.sh $ARGUMENTS
```

等待脚本完成，确认生成了 `extracted_decisions.md` 和 `code_summary.md`。

### Step 2 — 构建项目知识图谱

读取 `extracted_decisions.md` 和 `code_summary.md` 的内容，然后严格按照
`~/.interview-assistant/prompts/01-project-knowledge-builder.md` 中的格式要求，
在**同一次分析**中交叉印证两份文档，输出项目知识图谱。

将结果保存到 `project_knowledge_graph.md`。

### Step 3 — 生成面试题

询问用户：
- 目标职级（资深前端 / 全栈工程师 / Agent 工程师）
- 是否有目标 JD（有则粘贴）

按照 `~/.interview-assistant/prompts/02-interview-generator.md` 的格式，
基于知识图谱中的 TOP5 高价值决策生成面试题。

将结果保存到 `interview_questions.md`。

### Step 4 — 生成 STAR 故事卡

按照 `~/.interview-assistant/prompts/03-story-card-builder.md` 的格式，
将 TOP5 决策整理为可直接口述的 STAR 故事卡（每张 200–300 字）。

将结果保存到 `story_cards.md`。

### 完成

告知用户：
- `interview_questions.md` — 定制面试题（20–30 道）
- `story_cards.md` — STAR 故事卡（5 张，可直接口述）
CLAUDE_CMD

green "✓  Claude Code 斜杠命令已安装：$COMMAND_FILE"

# ── 可选：添加 shell alias ────────────────────────────────────────────────────
SHELL_RC=""
if [ -f "$HOME/.zshrc" ]; then
  SHELL_RC="$HOME/.zshrc"
elif [ -f "$HOME/.bashrc" ]; then
  SHELL_RC="$HOME/.bashrc"
fi

if [ -n "$SHELL_RC" ]; then
  if ! grep -q "interview-assistant" "$SHELL_RC" 2>/dev/null; then
    echo "" >> "$SHELL_RC"
    echo "# Interview Assistant" >> "$SHELL_RC"
    echo "alias interview-assistant='bash $INSTALL_DIR/run.sh'" >> "$SHELL_RC"
    green "✓  Shell alias 已添加到 $SHELL_RC"
  else
    yellow "ℹ️  Shell alias 已存在，跳过"
  fi
fi

# ── 完成 ──────────────────────────────────────────────────────────────────────
echo ""
echo "============================================================"
green "  ✅ 安装完成！"
echo "============================================================"
echo ""
echo "  使用方式一：Claude Code CLI 斜杠命令（推荐）"
echo "    在任意项目目录打开 Claude Code CLI，输入："
echo ""
echo "      /interview-assistant /path/to/your/project"
echo ""
echo "  使用方式二：直接运行脚本"
echo "    bash ~/.interview-assistant/run.sh /path/to/your/project"
echo ""
if [ -n "$SHELL_RC" ]; then
  echo "  使用方式三：Shell alias（需重启终端或 source $SHELL_RC）"
  echo "    interview-assistant /path/to/your/project"
  echo ""
fi
echo "  更新到最新版："
echo "    curl -fsSL $REPO_RAW/install.sh | bash"
echo ""
