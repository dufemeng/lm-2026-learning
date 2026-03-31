#!/usr/bin/env bash
# code_analyzer.sh
# 4 条命令提取代码摘要，输出 code_summary.md
#
# 用法：
#   bash code_analyzer.sh /path/to/your/project
#   bash code_analyzer.sh .                       # 当前目录
#
# 输出：code_summary.md（约 5–10KB）

set -euo pipefail

PROJECT_DIR="${1:-.}"
OUTPUT="code_summary.md"

# 标准化为绝对路径
PROJECT_DIR="$(cd "$PROJECT_DIR" && pwd)"

echo "🚀 Interview Assistant — CodeArchitectureAnalyzer"
echo "   项目目录：$PROJECT_DIR"
echo ""

# ── 初始化输出文件 ────────────────────────────────────────────────────────────
{
  echo "# 代码架构摘要"
  echo ""
  echo "> 生成时间：$(date '+%Y-%m-%d %H:%M:%S')"
  echo "> 项目目录：$PROJECT_DIR"
  echo ""
} > "$OUTPUT"

# ── ① 目录结构（最多 3 层）─────────────────────────────────────────────────
echo "  📁 提取目录结构..."
{
  echo "## 目录结构"
  echo '```'
  if command -v tree &>/dev/null; then
    tree "$PROJECT_DIR" -L 3 --gitignore 2>/dev/null \
      || tree "$PROJECT_DIR" -L 3 2>/dev/null
  else
    # tree 不存在时用 find 模拟（-not -path 过滤常见忽略目录）
    find "$PROJECT_DIR" \
      -not -path '*/.git/*' \
      -not -path '*/node_modules/*' \
      -not -path '*/__pycache__/*' \
      -not -path '*/.next/*' \
      -not -path '*/dist/*' \
      -not -path '*/.turbo/*' \
      | head -150
  fi
  echo '```'
  echo ""
} >> "$OUTPUT"

# ── ② 依赖栈（package.json / pyproject.toml / requirements.txt / go.mod）────
echo "  📦 提取依赖栈..."
{
  echo "## 依赖栈"
} >> "$OUTPUT"

for manifest in package.json pyproject.toml requirements.txt go.mod Cargo.toml; do
  if [ -f "$PROJECT_DIR/$manifest" ]; then
    {
      echo "### $manifest"
      echo '```'
      head -80 "$PROJECT_DIR/$manifest"
      echo '```'
      echo ""
    } >> "$OUTPUT"
  fi
done

# pnpm-workspace.yaml / lerna.json（Monorepo 特征文件）
for mono_config in pnpm-workspace.yaml lerna.json nx.json turbo.json; do
  if [ -f "$PROJECT_DIR/$mono_config" ]; then
    {
      echo "### $mono_config（Monorepo 配置）"
      echo '```'
      cat "$PROJECT_DIR/$mono_config"
      echo '```'
      echo ""
    } >> "$OUTPUT"
  fi
done

# ── ③ Git 提交历史（最近 50 条）──────────────────────────────────────────────
echo "  📜 提取 Git 历史..."
{
  echo "## 提交历史（最近 50 条）"
  echo '```'
  if git -C "$PROJECT_DIR" rev-parse --is-inside-work-tree &>/dev/null; then
    git -C "$PROJECT_DIR" log --oneline -50 2>/dev/null
  else
    echo "（未初始化 Git 仓库）"
  fi
  echo '```'
  echo ""
} >> "$OUTPUT"

# ── ④ 核心模块入口文件（前 50 行）──────────────────────────────────────────
echo "  🔍 提取核心模块入口..."
{
  echo "## 核心模块入口"
  echo ""
} >> "$OUTPUT"

# 常见入口文件列表
entry_files=(
  "src/index.ts"   "src/main.ts"   "src/app.ts"    "src/server.ts"
  "src/index.js"   "src/main.js"   "index.ts"      "main.ts"
  "src/__init__.py" "main.py"      "app.py"        "server.py"
  "src/index.tsx"  "app/page.tsx"
)

for rel in "${entry_files[@]}"; do
  entry="$PROJECT_DIR/$rel"
  if [ -f "$entry" ]; then
    line_count=$(wc -l < "$entry" 2>/dev/null || echo 0)
    ext="${rel##*.}"
    {
      echo "### $rel（${line_count} 行，取前 50 行）"
      echo "\`\`\`${ext}"
      head -50 "$entry"
      echo "\`\`\`"
      echo ""
    } >> "$OUTPUT"
  fi
done

# src/ 下各子目录的 index.ts / index.js（模块边界）
echo "  🗂️  提取子模块入口..."
if [ -d "$PROJECT_DIR/src" ]; then
  while IFS= read -r f; do
    # 跳过顶层 src/index.ts（已经处理过）
    [ "$f" = "$PROJECT_DIR/src/index.ts" ] && continue
    [ "$f" = "$PROJECT_DIR/src/index.js" ] && continue
    rel="${f#"$PROJECT_DIR/"}"
    ext="${f##*.}"
    {
      echo "### $rel（子模块，取前 30 行）"
      echo "\`\`\`${ext}"
      head -30 "$f"
      echo "\`\`\`"
      echo ""
    } >> "$OUTPUT"
  done < <(
    find "$PROJECT_DIR/src" \
      -name "index.ts" -o -name "index.js" \
      -not -path "*/node_modules/*" \
      2>/dev/null \
      | head -15
  )
fi

# ── 输出统计 ──────────────────────────────────────────────────────────────────
size_kb=$(( $(wc -c < "$OUTPUT") / 1024 ))
echo ""
echo "✅ 代码摘要已输出：$OUTPUT（约 ${size_kb} KB）"
echo ""
echo "📋 下一步："
echo "  将 extracted_decisions.md + $OUTPUT 内容同时粘贴到"
echo "  prompts/01-project-knowledge-builder.md 模板中，发送给 Claude"
