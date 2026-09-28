/**
 * 漫剧教程站 · 抓取日志
 * 每日一个文件,自动保留 14 天(由 cleanup.js 处理)
 */
import fs from 'node:fs';
import path from 'node:path';

const LOG_DIR = path.join(process.cwd(), 'logs');

if (!fs.existsSync(LOG_DIR)) {
  fs.mkdirSync(LOG_DIR, { recursive: true });
}

function getDate() {
  return new Date().toISOString().split('T')[0];
}

function getTime() {
  return new Date().toISOString().replace('T', ' ').slice(0, 19);
}

function logFile() {
  return path.join(LOG_DIR, `fetch-${getDate()}.log`);
}

function format(level, msg, meta) {
  const m = meta ? ` ${JSON.stringify(meta)}` : '';
  return `[${getTime()}] [${level}] ${msg}${m}`;
}

export function info(msg, meta) {
  const line = format('INFO', msg, meta);
  console.log(line);
  fs.appendFileSync(logFile(), line + '\n', 'utf-8');
}

export function warn(msg, meta) {
  const line = format('WARN', msg, meta);
  console.warn(line);
  fs.appendFileSync(logFile(), line + '\n', 'utf-8');
}

export function error(msg, meta) {
  const line = format('ERROR', msg, meta);
  console.error(line);
  fs.appendFileSync(logFile(), line + '\n', 'utf-8');
}

export function success(msg, meta) {
  const line = format('OK', msg, meta);
  console.log(line);
  fs.appendFileSync(logFile(), line + '\n', 'utf-8');
}

export function getLogs(days = 14) {
  if (!fs.existsSync(LOG_DIR)) return [];
  const cutoff = Date.now() - days * 86400000;
  return fs.readdirSync(LOG_DIR)
    .filter(f => f.endsWith('.log'))
    .map(f => {
      const full = path.join(LOG_DIR, f);
      const stat = fs.statSync(full);
      return {
        file: f,
        size: stat.size,
        mtime: stat.mtimeMs,
        expired: stat.mtimeMs < cutoff
      };
    });
}
