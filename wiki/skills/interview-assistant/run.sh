#!/usr/bin/env bash
# run.sh — Interview Assistant 一键执行入口
#
# 用法：
#   bash run.sh /path/to/your/project
#   bash run.sh /path/to/your/project --days 14 --max-files 10
#
# 执行流程：
#   Step 1 — SessionExtractor: 提取 Claude Code CLI session → extracted_decisions.md
#   Step 2 — CodeArchitectureAnalyzer: 分析代码结构     → code_summary.md
#   Step 3 — 打印后续 LLM 步骤指引

set -euo pipefail

# ── 参数解析 ──────────────────────────────────────────────────────────────────
PROJECT_DIR="${1:-}"
EXTRA_ARGS="${*:2}"   # 透传给 session-extractor.mjs 的额外参数（--days / --max-files）

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# ── 前置检查 ──────────────────────────────────────────────────────────────────
echo "============================================================"
echo "  Interview Assistant — 面试助手"
echo "============================================================"
echo ""

# 检查 Node.js
if ! command -v node &>/dev/null; then
  echo "❌ 未找到 node。请先安装 Node.js 18+：https://nodejs.org/"
  exit 1
fi

NODE_MAJOR=$(node --version | cut -d. -f1 | tr -d 'v')
if [ "$NODE_MAJOR" -lt 18 ]; then
  echo "❌ Node.js 版本过低（当前 $(node --version)），需要 18+。"
  exit 1
fi

# 检查项目目录参数
if [ -z "$PROJECT_DIR" ]; then
  echo "用法：bash run.sh /path/to/your/project [--days <N>] [--max-files <N>]"
  echo ""
  echo "示例："
  echo "  bash run.sh ~/projects/my-video-agent"
  echo "  bash run.sh ~/projects/my-video-agent --days 14 --max-files 10"
  exit 1
fi

if [ ! -d "$PROJECT_DIR" ]; then
  echo "❌ 项目目录不存在：$PROJECT_DIR"
  exit 1
fi

PROJECT_DIR="$(cd "$PROJECT_DIR" && pwd)"

echo "📋 配置信息："
echo "   项目目录：$PROJECT_DIR"
echo "   脚本目录：$SCRIPT_DIR"
echo "   Node.js：$(node --version)"
echo ""

# ── Step 1：SessionExtractor ──────────────────────────────────────────────────
echo "------------------------------------------------------------"
echo "  Step 1 / 2 — SessionExtractor"
echo "  从 ~/.claude/projects/ 提取决策对话 → extracted_decisions.md"
echo "------------------------------------------------------------"
echo ""

# shellcheck disable=SC2086
node "$SCRIPT_DIR/session-extractor.mjs" $EXTRA_ARGS

if [ ! -f "extracted_decisions.md" ]; then
  echo "❌ extracted_decisions.md 未生成，请检查上方错误信息"
  exit 1
fi

echo ""

# ── Step 2：CodeArchitectureAnalyzer ─────────────────────────────────────────
echo "------------------------------------------------------------"
echo "  Step 2 / 2 — CodeArchitectureAnalyzer"
echo "  分析项目代码结构 → code_summary.md"
echo "------------------------------------------------------------"
echo ""

bash "$SCRIPT_DIR/code_analyzer.sh" "$PROJECT_DIR"

if [ ! -f "code_summary.md" ]; then
  echo "❌ code_summary.md 未生成，请检查上方错误信息"
  exit 1
fi

echo ""

# ── 输出统计 ──────────────────────────────────────────────────────────────────
decisions_size=$(( $(wc -c < extracted_decisions.md) / 1024 ))
code_size=$(( $(wc -c < code_summary.md) / 1024 ))
total_size=$(( decisions_size + code_size ))

echo "============================================================"
echo "  ✅ 自动化步骤完成！"
echo "============================================================"
echo ""
echo "  生成文件："
printf "    %-30s %s KB\n" "extracted_decisions.md" "$decisions_size"
printf "    %-30s %s KB\n" "code_summary.md" "$code_size"
echo "                                     ──────"
printf "    %-30s %s KB (LLM 输入)\n" "合计" "$total_size"
echo ""

if [ "$total_size" -gt 80 ]; then
  echo "  ⚠️  合计超过 80KB，LLM 调用前建议检查 extracted_decisions.md 是否有大量无关内容"
  echo "     可尝试：bash run.sh $PROJECT_DIR --days 14 --max-files 10"
  echo ""
fi

# ── 后续步骤指引 ──────────────────────────────────────────────────────────────
echo "------------------------------------------------------------"
echo "  后续 LLM 步骤（手动执行，需要 claude.ai）"
echo "------------------------------------------------------------"
echo ""
echo "  Step 3 — ProjectKnowledgeBuilder（约 5 分钟）"
echo "    打开：$SCRIPT_DIR/prompts/01-project-knowledge-builder.md"
echo "    将 extracted_decisions.md + code_summary.md 内容填入模板"
echo "    发送给 Claude → 保存输出为：project_knowledge_graph.md"
echo ""
echo "  Step 4 — InterviewGenerator（约 3 分钟）"
echo "    打开：$SCRIPT_DIR/prompts/02-interview-generator.md"
echo "    填入 project_knowledge_graph.md + 目标职级 + JD（可选）"
echo "    发送给 Claude → 保存输出为：interview_questions.md"
echo ""
echo "  Step 5 — StoryCardBuilder（约 3 分钟）"
echo "    打开：$SCRIPT_DIR/prompts/03-story-card-builder.md"
echo "    填入决策清单 + session 片段"
echo "    发送给 Claude → 保存输出为：story_cards.md"
echo ""
echo "  完成后你将得到："
echo "    📝 interview_questions.md — 20–30 道定制面试题"
echo "    🎯 story_cards.md         — 5 张 STAR 故事卡（可直接口述）"
echo ""
echo "============================================================"
