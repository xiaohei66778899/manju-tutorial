/**
 * 把 tools/index.html 里所有 emoji icon 替换成 <img> 产品 logo
 * 策略:遍历每个 .tool-card,提取 <h3> 里的工具名,映射到对应的 logo
 */
import fs from 'node:fs';
import path from 'node:path';

const ROOT = path.resolve(process.cwd(), '..', '..');
const TOOLS_HTML = path.join(ROOT, 'site', 'tools', 'index.html');
const ICON_DIR = '../assets/icons/tools/';

// 工具名 → icon 文件名 映射
const ICON_MAP = {
  'DeepSeek': 'deepseek',
  '豆包': 'doubao',
  'ChatGPT': 'chatgpt',
  'Claude': 'claude',
  '巨日禄': null,
  '小云雀': null,
  'ViMax': 'vimax',
  '即梦': 'jimeng',
  'Midjourney': 'midjourney',
  'Stable Diffusion WebUI': 'stability',
  'ComfyUI': 'comfyui',
  'Flux': 'flux',
  'SDXL + JuggernautXL': 'sdxl',
  'Toonflow': 'toonflow',
  '可灵': 'kling',
  '即梦视频': 'jimeng',
  'Runway Gen-4 Turbo': 'runway',
  'Vidu': 'vidu',
  'Hailuo 海螺': 'hailuo',
  'Hailuo': 'hailuo',
  'Wan 2.x': 'wan',
  'Wan 2.2': 'wan',
  'Sora 2': 'sora',
  'HunyuanVideo': 'hunyuanvideo',
  'LTX-Video': 'ltx',
  'AnimateDiff': 'animatediff',
  'AnimateDiff + SDXL': 'animatediff',
  'Seedance 2.0': 'seedance',
  'seedance-2.0': 'seedance',
  'Suno': 'suno',
  '剪映': 'jianying',
  'ElevenLabs': 'elevenlabs',
  '魔音工坊': null,
  'ChatTTS': 'chattts',
  'Sync.so': 'syncso',
  'Udio': 'udio',
  'Freesound 音效库': 'freesound',
  'Premiere Pro': 'premiere',
  'DaVinci Resolve': 'davinci',
  'Final Cut Pro': 'finalcut',
  'CapCut 国际版': 'capcut',
  'Canva 可画': 'canva',
  'RIFE': 'rife',
  'RIFE 插帧': 'rife',
  '4x-UltraSharp': 'ultrasharp',
  '4x-UltraSharp 高清放大': 'ultrasharp',
  'libtv': null,
  '商汤 Seko': null,
  '有戏 AI': null,
  'Catimind': null,
  'Pixmax': null,
  '60 端': null,
  '60 端漫剧流水线': null,
  '字狐跳跳': null,
  '海螺 AI Agent': 'minimax',
  'MiniMax 海螺 AI': 'minimax',
  'TapNow 长视频': 'tapnow',
  '智谱清影': 'zhipu',
  'aid-studio': 'aid-studio',
  'LumenX Studio': 'lumenx',
  'lumenx': 'lumenx',
  'MoneyPrinterTurbo': 'mpt',
  'huobao-drama': 'huobao',
  'NarratoAI': 'narratoai',
  'Jellyfish': 'jellyfish',
  'ArcReel': 'arcreel',
  'FireRed-OpenStoryline': 'firered',
  'PixVerse': 'pixverse',
  'Pika': 'pika',
  'Luma': 'luma',
  'Stability': 'stability',
  'Qwen': 'qwen',
  '通义 Wan 2.2': 'wan'
};

// 列出已下载的 icons(实际验证)
const ICON_DIR_FULL = path.join(ROOT, 'site', 'assets', 'icons', 'tools');
const availableIcons = new Set(fs.readdirSync(ICON_DIR_FULL).map(f => f.replace(/\.png$/, '')));

// 读取 HTML
let html = fs.readFileSync(TOOLS_HTML, 'utf-8');
const originalLen = html.length;

// 找出所有 <div class="tool-card" ...>...</div> 块,逐个替换
let replaced = 0;
let skipped = 0;
const unmapped = [];

function replaceInCard(cardBlock) {
  // 提取工具名(h3 里的第一个文本节点,可能有 badge 等)
  const h3Match = cardBlock.match(/<h3>([\s\S]*?)<\/h3>/);
  if (!h3Match) return null;
  const h3Content = h3Match[1];

  // 提取 h3 里的纯文本工具名(去掉 badge)
  const toolName = h3Content.replace(/<span[^>]*>[\s\S]*?<\/span>/g, '').trim();

  // 查映射
  let iconKey = ICON_MAP[toolName];
  // 备用:模糊匹配
  if (!iconKey) {
    for (const [k, v] of Object.entries(ICON_MAP)) {
      if (k && toolName.includes(k)) { iconKey = v; break; }
    }
  }

  if (!iconKey) {
    unmapped.push(toolName);
    return null;
  }
  if (!availableIcons.has(iconKey)) {
    unmapped.push(toolName + ' (no icon: ' + iconKey + ')');
    return null;
  }

  // 找 <div class="head"><div class="ic ...">[emoji]</div>
  const newIcBlock = `<div class="head"><div class="ic ic-${iconKey}"><img src="${ICON_DIR}${iconKey}.png" alt="${toolName}"></div>`;
  return cardBlock.replace(/<div class="head"><div class="ic[^"]*">[^<]*<\/div>/, newIcBlock);
}

// 遍历每个 tool-card 块
html = html.replace(/<div class="tool-card"[\s\S]*?<\/div>\s*<\/div>/g, (match) => {
  const replaced_ = replaceInCard(match);
  if (replaced_) { replaced++; return replaced_; }
  skipped++;
  return match;
});

fs.writeFileSync(TOOLS_HTML, html, 'utf-8');
console.log(`替换完成:`);
console.log(`  ✓ 已替换: ${replaced} 个卡片`);
console.log(`  ✗ 跳过(无 icon 或未映射): ${skipped}`);
console.log(`未映射的工具:`);
[...new Set(unmapped)].forEach(n => console.log(`  - ${n}`));
console.log(`文件: ${TOOLS_HTML}`);
console.log(`  原大小: ${originalLen} bytes`);
console.log(`  新大小: ${html.length} bytes`);
