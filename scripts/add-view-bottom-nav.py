# -*- coding: utf-8 -*-
"""给剧本 SPA 的每个 view 底部加"上一节/下一节"按钮
- 在 footer 前插入一个 bottom-nav
- JS 监听 hash,动态算 prev/next 目标
- 同时应用到根目录 剧本.html 和 site/剧本.html
"""
import os, sys
sys.stdout.reconfigure(encoding='utf-8')

BOTTOM_NAV_HTML = r'''
<nav class="bottom-nav" id="view-bottom-nav" aria-label="B 板块章节导航">
  <a class="prev" href="#view-1-1">
    <span class="label">← 上一节</span>
    <span class="title" id="view-prev-title">B-1 选题库</span>
  </a>
  <a class="next" href="#view-1-1">
    <span class="label">下一节 →</span>
    <span class="title" id="view-next-title">B-1 选题库</span>
  </a>
</nav>

<script>
// view 8 个章节顺序表
const VIEW_ORDER = [
  { id: 'view-1-1', title: 'B-1 选题库' },
  { id: 'view-1-2', title: 'B-2 AI 辅助原创' },
  { id: 'view-1-3', title: 'B-3 爽点模板' },
  { id: 'view-1-4', title: 'B-4 改稿方法' },
  { id: 'view-2-1', title: 'B-5 怎么找授权' },
  { id: 'view-2-2', title: 'B-6 合同怎么看' },
  { id: 'view-2-3', title: 'B-7 改编流程' },
  { id: 'view-2-4', title: 'B-8 相似度检查' },
];

function updateBottomNav() {
  const hash = window.location.hash || '#view-1-1';
  const idx = VIEW_ORDER.findIndex(v => '#' + v.id === hash);
  if (idx === -1) return;
  const nav = document.getElementById('view-bottom-nav');
  if (!nav) return;
  const prev = VIEW_ORDER[idx - 1]; // 第一个 view 时 idx - 1 = -1,undefined
  const next = VIEW_ORDER[idx + 1];
  const prevA = nav.querySelector('.prev');
  const nextA = nav.querySelector('.next');
  const prevTitle = document.getElementById('view-prev-title');
  const nextTitle = document.getElementById('view-next-title');
  if (prev) {
    prevA.href = '#' + prev.id;
    prevA.style.visibility = 'visible';
    prevTitle.textContent = prev.title;
  } else {
    // 第一节:返回"上级"(B 板块目录页,即 tutorial/index.html#B)
    prevA.href = '../tutorial/index.html#B';
    prevA.style.visibility = 'visible';
    prevTitle.textContent = 'B 板块目录';
  }
  if (next) {
    nextA.href = '#' + next.id;
    nextA.style.visibility = 'visible';
    nextTitle.textContent = next.title;
  } else {
    // 最后一节:进入下一个大类 C
    nextA.href = '../tutorial/C-character/C-1.html';
    nextA.style.visibility = 'visible';
    nextTitle.textContent = 'C-1 角色制作简介';
  }
}

window.addEventListener('hashchange', updateBottomNav);
window.addEventListener('DOMContentLoaded', updateBottomNav);
// 初始也调一次
updateBottomNav();
</script>
'''

ANCHOR = '<footer class="dock-run compact">'

files = [
    r'E:\AIGC\课件\12小说\剧本.html',
    r'E:\AIGC\课件\12小说\site\剧本.html',
]

changed = 0
for fp in files:
    if not os.path.exists(fp):
        print(f'❌ {fp} 不存在')
        continue
    with open(fp, 'rb') as fh:
        raw = fh.read()
    has_bom = raw.startswith(b'\xef\xbb\xbf')
    text = raw.decode('utf-8-sig') if has_bom else raw.decode('utf-8')
    if 'id="view-bottom-nav"' in text:
        print(f'⏭ {fp} 已存在底部导航,跳过')
        continue
    if ANCHOR not in text:
        print(f'❌ {fp} 找不到 footer 锚点,跳过')
        continue
    new_text = text.replace(ANCHOR, BOTTOM_NAV_HTML + '\n' + ANCHOR, 1)
    out = (b'\xef\xbb\xbf' + new_text.encode('utf-8')) if has_bom else new_text.encode('utf-8')
    with open(fp, 'wb') as fh:
        fh.write(out)
    changed += 1
    print(f'✅ {fp}')

print(f'\n共处理 {changed} 个文件')