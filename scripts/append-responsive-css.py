# -*- coding: utf-8 -*-
"""在 tutorial.css 末尾追加响应式样式
- 桌面(≥1090px):3 栏
- 平板(768-1089px):2 栏(隐藏右侧 TOC)
- 手机(<768px):1 栏 + sidebar 折叠成顶部抽屉
"""
import os, sys
sys.stdout.reconfigure(encoding='utf-8')

fp = r'E:\AIGC\课件\12小说\site\assets\tutorial.css'

APPEND = r'''

/* ============================================================
   响应式布局(玉哥定稿 2026-09-19)
   - 桌面 ≥1090px:3 栏布局(左目录 + 主区 + 右 TOC)
   - 平板 768-1089px:2 栏(隐藏右 TOC,左目录保留)
   - 手机 <768px:1 栏 + sidebar 折叠成顶部按钮 + 抽屉
   ============================================================ */

/* ---------- 平板端(768-1089px) ---------- */
@media (max-width: 1089px) {
  .layout-3col {
    grid-template-columns: var(--side-l-w) minmax(0, 1fr);
  }
  /* 隐藏右侧 TOC */
  .sidebar-right {
    display: none !important;
  }
  /* 主区占满 */
  .tut-main, .content {
    max-width: 100% !important;
    padding-right: 16px;
  }
  /* sidebar 稍窄 */
  :root { --side-l-w: 200px; }
}

/* ---------- 手机端(<768px) ---------- */
@media (max-width: 767px) {
  /* 1 栏布局 */
  .layout-3col {
    display: block !important;
    padding: 0 !important;
  }

  /* sidebar 默认隐藏(变成抽屉) */
  .sidebar-left {
    position: fixed !important;
    top: var(--top-h) !important;
    left: 0 !important;
    width: 280px !important;
    max-width: 85vw !important;
    height: calc(100vh - var(--top-h)) !important;
    background: var(--bg) !important;
    border-right: 1px solid var(--line) !important;
    box-shadow: 4px 0 24px rgba(0,0,0,.12) !important;
    transform: translateX(-100%) !important;
    transition: transform .28s ease !important;
    z-index: 999 !important;
    padding: 16px 14px 60px !important;
    overflow-y: auto !important;
  }
  .sidebar-left.is-open {
    transform: translateX(0) !important;
  }

  /* 主区占满 */
  .tut-main, .content {
    max-width: 100% !important;
    padding: 16px !important;
  }

  /* 顶栏加个"目录"按钮(JS 注入) */
  .topbar {
    position: relative !important;
  }
  .topbar .menu-toggle {
    display: inline-flex !important;
  }

  /* 抽屉打开时遮罩 */
  body.sidebar-open::after {
    content: '';
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,.4);
    z-index: 998;
  }

  /* 隐藏右侧 TOC */
  .sidebar-right { display: none !important; }

  /* 表格横向滚动 */
  table {
    display: block;
    overflow-x: auto;
    white-space: nowrap;
  }

  /* 代码块可滚动 */
  pre {
    overflow-x: auto;
  }

  /* 图片自适应 */
  img { max-width: 100%; height: auto; }
}

/* ---------- 顶栏菜单按钮(默认隐藏,手机端显示) ---------- */
.topbar .menu-toggle {
  display: none;
  background: transparent;
  border: 1px solid var(--line);
  border-radius: 18px;
  width: 36px;
  height: 36px;
  margin-right: 4px;
  cursor: pointer;
  font-size: 16px;
  align-items: center;
  justify-content: center;
}

/* ---------- 横屏手机 ---------- */
@media (max-height: 500px) and (orientation: landscape) {
  .sidebar-left {
    width: 240px !important;
  }
}
'''

with open(fp, 'rb') as fh:
    raw = fh.read()
has_bom = raw.startswith(b'\xef\xbb\xbf')
text = raw.decode('utf-8-sig') if has_bom else raw.decode('utf-8')

if '响应式布局' in text:
    print('⚠️  响应式样式已存在,跳过')
else:
    text += APPEND
    out = (b'\xef\xbb\xbf' + text.encode('utf-8')) if has_bom else text.encode('utf-8')
    with open(fp, 'wb') as fh:
        fh.write(out)
    print('✅ 响应式样式已追加到 tutorial.css')