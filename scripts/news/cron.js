/**
 * 漫剧教程站 · 新闻系统 cron 入口
 * 一次性按 schedule 执行:fetch → stats → cleanup
 *
 * 用法:
 *   node cron.js daily     # 每日全流程
 *   node cron.js fetch     # 只抓取
 *   node cron.js stats     # 只统计
 *   node cron.js cleanup   # 只清理
 *
 * crontab 配合(腾讯云):
 *   30 6 * * *  cd /path && node scripts/news/cron.js daily  >> logs/cron.log 2>&1
 *   30 3 * * *  cd /path && node scripts/news/cron.js cleanup >> logs/cron-cleanup.log 2>&1
 *   0  8 * * 0  cd /path && node scripts/news/cron.js stats    >> logs/cron-stats.log 2>&1
 */
import { spawn } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { info, success } from './lib/logger.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const task = process.argv[2] || 'daily';

function runStep(script, args = []) {
  return new Promise((resolve, reject) => {
    info(`▶ ${script} ${args.join(' ')}`);
    const child = spawn(process.execPath, [path.join(__dirname, script), ...args], {
      stdio: 'inherit',
      cwd: __dirname
    });
    child.on('close', code => {
      if (code === 0) resolve();
      else reject(new Error(`${script} exit ${code}`));
    });
    child.on('error', reject);
  });
}

async function main() {
  const start = Date.now();
  info(`====== cron 任务开始: ${task} ======`);

  try {
    if (task === 'daily') {
      await runStep('fetch.js');
      await runStep('cleanup.js');
      await runStep('stats.js');
    } else if (task === 'fetch') {
      await runStep('fetch.js');
    } else if (task === 'stats') {
      await runStep('stats.js');
    } else if (task === 'cleanup') {
      await runStep('cleanup.js');
    } else if (task === 'with-llm') {
      await runStep('fetch.js', ['--with-llm']);
    } else {
      throw new Error(`未知任务: ${task} (可用: daily / fetch / stats / cleanup / with-llm)`);
    }
    success(`====== cron 任务完成: ${task} (${((Date.now() - start) / 1000).toFixed(1)}s) ======`);
  } catch (e) {
    info(`❌ cron 任务失败: ${task} - ${e.message}`);
    process.exit(1);
  }
}

main();
