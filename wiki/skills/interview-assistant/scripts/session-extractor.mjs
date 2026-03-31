#!/usr/bin/env node
/**
 * session-extractor.mjs
 * 三层过滤，将 100M+ Claude Code CLI session 压缩到 50KB 以内
 * 输出文件：extracted_decisions.md
 * 运行环境：Node.js 18+，零依赖
 *
 * 用法：
 *   node session-extractor.mjs
 *   node session-extractor.mjs --days 14 --max-files 10
 *   SESSION_DIR=~/.claude/projects/my-project node session-extractor.mjs
 */

import fs from 'fs';
import readline from 'readline';
import path from 'path';
import os from 'os';

// ── 配置（可通过环境变量或命令行参数覆盖）────────────────────────────────────
const SESSION_DIR = process.env.SESSION_DIR
  ?? path.join(os.homedir(), '.claude', 'projects');
const OUTPUT_FILE = process.env.OUTPUT_FILE ?? 'extracted_decisions.md';

// 解析命令行参数 --days / --max-files
const args = process.argv.slice(2);
const getArg = (flag, defaultVal) => {
  const idx = args.indexOf(flag);
  return idx !== -1 && args[idx + 1] ? parseInt(args[idx + 1], 10) : defaultVal;
};

const DAYS_LIMIT = getArg('--days', 30);       // 只处理最近 N 天的文件
const MAX_FILES = getArg('--max-files', 20);  // 最多处理 N 个文件（按大小取最大）
const MAX_OUTPUT_KB = 50;                       // 目标输出大小上限（超出时给出警告）

// ── 工具函数 ─────────────────────────────────────────────────────────────────

/** 解析单个 .jsonl 文件，返回标准化消息列表 */
async function loadJsonl(filepath) {
  const messages = [];
  const fileStream = fs.createReadStream(filepath);
  const rl = readline.createInterface({ input: fileStream, crlfDelay: Infinity });
  const filename = path.basename(filepath);
  let lineno = 0;

  for await (const line of rl) {
    lineno++;
    const trimmed = line.trim();
    if (!trimmed) continue;

    let obj;
    try {
      obj = JSON.parse(trimmed);
    } catch {
      process.stderr.write(`  ⚠️  ${filename}:${lineno} JSON 解析失败，跳过\n`);
      continue;
    }

    const role = obj.role ?? '';
    let content = obj.content ?? '';
    const timestamp = obj.timestamp ?? '';

    // content 可能是数组（多块内容），拍平提取 text 类型块
    if (Array.isArray(content)) {
      content = content
        .filter(block => block && typeof block === 'object' && block.type === 'text')
        .map(block => String(block.text ?? ''))
        .join('\n');
    } else if (typeof content !== 'string') {
      content = String(content);
    }

    if (role && content) {
      messages.push({ role, content, timestamp, source_file: filename });
    }
  }
  return messages;
}

// ── 第一层：文件级过滤 ────────────────────────────────────────────────────────
/** 返回最近 DAYS_LIMIT 天内、体积最大的 MAX_FILES 个 .jsonl 文件路径 */
function layer1FileFilter(sessionDir) {
  const cutoffMs = Date.now() - DAYS_LIMIT * 24 * 60 * 60 * 1000;
  const candidates = [];

  function walk(dir) {
    let entries;
    try {
      entries = fs.readdirSync(dir, { withFileTypes: true });
    } catch (err) {
      process.stderr.write(`  ⚠️  跳过无法访问的目录：${dir}（${err.message}）\n`);
      return;
    }
    for (const entry of entries) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        walk(full);
      } else if (entry.isFile() && entry.name.endsWith('.jsonl')) {
        const stat = fs.statSync(full);
        if (stat.mtimeMs >= cutoffMs) {
          candidates.push({ size: stat.size, filepath: full });
        }
      }
    }
  }

  walk(sessionDir);

  // 按大小降序，取前 MAX_FILES 个
  candidates.sort((a, b) => b.size - a.size);
  const selected = candidates.slice(0, MAX_FILES).map(c => c.filepath);
  console.log(
    `📂 文件级过滤：找到 ${candidates.length} 个近期文件（最近 ${DAYS_LIMIT} 天），` +
    `选取最大的 ${selected.length} 个`,
  );
  return selected;
}

// ── 第二层：消息级过滤 ────────────────────────────────────────────────────────
/** 判断消息是否主要由代码块构成 */
function isMostlyCode(text, threshold = 0.7) {
  const codeBlockChars = [...text.matchAll(/```[\s\S]*?```/g)]
    .reduce((sum, m) => sum + m[0].length, 0);
  return text.length > 0 && codeBlockChars / text.length > threshold;
}

/** 丢弃纯代码块（>70%）和过短消息（<50 字） */
function layer2MessageFilter(messages) {
  const filtered = messages.filter(msg =>
    !isMostlyCode(msg.content) && msg.content.trim().length >= 50,
  );
  console.log(`📝 消息级过滤：${messages.length} → ${filtered.length} 条消息`);
  return filtered;
}

// ── 第三层：语义级过滤 ────────────────────────────────────────────────────────
const DECISION_KEYWORDS =
  /为什么|为何|原因|方案|决定|决策|选择|不用|改成|换成|放弃|权衡|取舍|考虑过|试过|坑|问题|瓶颈|优化|重构|架构|设计|模式|策略|实现|方式|why|because|reason|decided|instead|tradeoff|approach|pattern/i;

/**
 * 保留含决策关键词的消息。
 * human turn 优先：人类提问时的措辞（约束条件、判断方向）比 assistant 输出更有面试价值。
 */
function layer3SemanticFilter(messages) {
  const humanMsgs = messages.filter(m => m.role === 'human' && DECISION_KEYWORDS.test(m.content));
  const assistMsgs = messages.filter(m => m.role === 'assistant' && DECISION_KEYWORDS.test(m.content));

  // assistant 数量上限：human 的一半，最少 10 条
  const assistLimit = Math.max(10, Math.floor(humanMsgs.length / 2));
  let result = [...humanMsgs, ...assistMsgs.slice(0, assistLimit)];

  console.log(
    `🔍 语义级过滤：human ${humanMsgs.length} 条 + ` +
    `assistant ${Math.min(assistMsgs.length, assistLimit)} 条`,
  );

  // 降级：语义过滤后为空，保留最长的 20 条 human turn
  if (result.length === 0) {
    console.log('⚠️  语义过滤结果为空，降级为保留最长的 20 条 human turn');
    result = messages
      .filter(m => m.role === 'human')
      .sort((a, b) => b.content.length - a.content.length)
      .slice(0, 20);
  }
  return result;
}

// ── 输出 ──────────────────────────────────────────────────────────────────────
function writeOutput(messages, outputPath) {
  const now = new Date().toISOString().slice(0, 19).replace('T', ' ');
  const lines = [
    '# Session 决策提炼\n\n',
    `> 提取时间：${now}  \n`,
    `> 消息数量：${messages.length} 条  \n`,
    `> 来源目录：${SESSION_DIR}\n\n`,
    '---\n\n',
  ];

  for (let i = 0; i < messages.length; i++) {
    const msg = messages[i];
    const roleLabel = msg.role === 'human' ? '👤 用户' : '🤖 Claude';
    const ts = msg.timestamp
      ? String(msg.timestamp).slice(0, 19).replace('T', ' ')
      : '时间未知';
    lines.push(`### [${i + 1}] ${roleLabel}  \`${ts}\`  \`${msg.source_file}\`\n\n`);
    lines.push(msg.content.trim() + '\n\n');
    lines.push('---\n\n');
  }

  fs.writeFileSync(outputPath, lines.join(''), 'utf-8');
  const sizeKb = fs.statSync(outputPath).size / 1024;
  console.log(`\n✅ 输出：${outputPath}  (${sizeKb.toFixed(1)} KB)`);
  if (sizeKb > MAX_OUTPUT_KB) {
    console.log(
      `⚠️  输出超过 ${MAX_OUTPUT_KB}KB，建议缩减 --max-files 或 --days 参数\n` +
      `   示例：node session-extractor.mjs --days 14 --max-files 10`,
    );
  }
}

// ── 入口 ──────────────────────────────────────────────────────────────────────
async function main() {
  console.log('🚀 Interview Assistant — SessionExtractor\n');

  if (!fs.existsSync(SESSION_DIR)) {
    process.stderr.write(`❌ Session 目录不存在：${SESSION_DIR}\n`);
    process.stderr.write('   请确认已安装 Claude Code CLI 并使用过 claude 命令\n');
    process.exit(1);
  }

  // 第一层：文件级过滤
  const selectedFiles = layer1FileFilter(SESSION_DIR);
  if (selectedFiles.length === 0) {
    process.stderr.write(
      `❌ 未找到最近 ${DAYS_LIMIT} 天内的 session 文件\n` +
      `   尝试增加时间范围：node session-extractor.mjs --days 60\n`,
    );
    process.exit(1);
  }

  // 加载所有选中文件
  let allMessages = [];
  for (const filepath of selectedFiles) {
    const stat = fs.statSync(filepath);
    const sizeMb = (stat.size / 1024 / 1024).toFixed(1);
    process.stdout.write(`  📖 加载 ${path.basename(filepath)} (${sizeMb} MB)...\n`);
    allMessages = allMessages.concat(await loadJsonl(filepath));
  }
  console.log(`\n📊 共加载 ${allMessages.length} 条原始消息\n`);

  // 第二层：消息级过滤
  let messages = layer2MessageFilter(allMessages);

  // 第三层：语义级过滤
  messages = layer3SemanticFilter(messages);

  // 写入输出
  writeOutput(messages, OUTPUT_FILE);

  console.log('\n📋 下一步：');
  console.log('  1. bash code_analyzer.sh /path/to/your/project');
  console.log('  2. 将 extracted_decisions.md + code_summary.md 内容粘贴到');
  console.log('     prompts/01-project-knowledge-builder.md 模板中，发送给 Claude');
}

main().catch(err => {
  process.stderr.write(`❌ 运行失败：${err.message}\n${err.stack}\n`);
  process.exit(1);
});
