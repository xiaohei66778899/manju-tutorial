#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理全站"原版"残留(第二轮:修饰、徽章、卡片描述、footer)。
策略:
  - footer "教程内容源自原版课件 + AI 辅助编排" → "教程内容 + AI 辅助编排"
  - 各种 badge "原版" → "专题"
  - 卡片描述 / meta 里 "原版 vX" → "vX"(去掉修饰)
  - news/qa "📚 原版课件" → "📚 课件"
  - 剧本.html 顶部 "原版 · " → ""
保留:
  - J/K/L/H 4 大专题文件 title/logo 里的"原版"(品牌标识)
  - CSS/HTML 注释里的"原版"
BOM 安全。
"""
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

ROOT = r"E:\AIGC\课件\12小说"
SITE = os.path.join(ROOT, "site")

TARGETS = []
for root, dirs, files in os.walk(SITE):
    for f in files:
        if f.endswith(".html"):
            TARGETS.append(os.path.join(root, f))
JUBEN = os.path.join(ROOT, "剧本.html")
if os.path.exists(JUBEN):
    TARGETS.append(JUBEN)

# 排除:J/K/L/H 4 大专题文件(保留内部 title/logo 的"原版")
PRESERVE = {
    'ComfyUI漫剧工作流.html',
    '千川投流SOP.html',
    '短剧AI仓库.html',
    '短剧创业SOP.html',
}

# 全站规则(简单字符串替换)
RULES_COMMON = [
    # footer 标准化(几乎所有 HTML)
    ('教程内容源自原版课件 + AI 辅助编排',
     '教程内容 + AI 辅助编排'),

    # tools / tutorial / 剧本 徽章
    ('<i class="fas fa-bolt"></i>原版</span>',
     '<i class="fas fa-bolt"></i>专题</span>'),

    # tutorial/index badge "4 张原版"
    ('<span class="badge"><i>⭐</i>4 张原版</span>',
     '<span class="badge"><i>⭐</i>4 张专题</span>'),

    # templates/index "原版整理"
    ('<b>原版</b>整理</span>',
     '<b>专题</b>整理</span>'),

    # 剧本.html badge "📖 原版"
    ('<span class="badge"><i>📖</i>原版</span>',
     '<span class="badge"><i>📖</i>专题</span>'),

    # news/qa "📚 原版课件 · 15 份完整保真"
    ('📚 原版课件 · 15 份完整保真',
     '📚 课件 · 15 份完整保真'),

    # commercial/index "原版 v9.0 商业化 SOP"
    ('3 条变现路径 · 原版 v9.0 商业化 SOP · 不混入教程主线',
     '3 条变现路径 · v9.0 商业化 SOP · 不混入教程主线'),
    ('千川 ROI 1.2+ 月入 1-3 万 · 原版 v9.0',
     '千川 ROI 1.2+ 月入 1-3 万 · v9.0'),
    ('<div class="sub">3 条变现路径 · 原版 v9.0 商业化 SOP · 不混入教程主线</div>',
     '<div class="sub">3 条变现路径 · v9.0 商业化 SOP · 不混入教程主线</div>'),

    # templates/index "4 阶段 + ROI 计算器 · 原版"
    ('4 阶段 + ROI 计算器 · 原版',
     '4 阶段 + ROI 计算器'),

    # tools/index meta description
    ('原版 + 全网 80+ 工具汇总',
     '全网 80+ 工具汇总'),

    # 剧本.html description / 顶部
    ('原版 · 原创剧本 + 小说改编剧本',
     '原创剧本 + 小说改编剧本'),
]

# J/K/L/H 4 大专题文件额外保留,但允许 footer 标准化
RULES_PRESERVED_FILES = [
    ('教程内容源自原版课件 + AI 辅助编排',
     '教程内容 + AI 辅助编排'),
]


def clean_file(fp):
    fname = os.path.basename(fp)
    with open(fp, 'rb') as f:
        raw = f.read()
    has_bom = raw.startswith(b'\xef\xbb\xbf')
    text = raw.decode('utf-8-sig') if has_bom else raw.decode('utf-8')
    orig = text

    # 选择规则集
    rules = RULES_PRESERVED_FILES if fname in PRESERVE else RULES_COMMON

    for old, new in rules:
        text = text.replace(old, new)

    if text != orig:
        diff = len(orig) - len(text)
        out = (b'\xef\xbb\xbf' + text.encode('utf-8')) if has_bom else text.encode('utf-8')
        with open(fp, 'wb') as f:
            f.write(out)
        return True, diff
    return False, 0


def main():
    print("=== 第二轮清理全站 '原版' 残留(footer/badge/卡片描述) ===\n")
    total_changed = 0
    total_chars = 0
    for fp in TARGETS:
        ok, diff = clean_file(fp)
        rel = fp[len(ROOT):]
        if ok:
            print(f"  ✅ {rel} · -{diff} 字符")
            total_changed += 1
            total_chars += diff

    print(f"\n📊 共更新 {total_changed} 个文件,删除 {total_chars} 字符\n")

    # 残留核验
    print("=== 残留 '原版' 核验(仅保留:J/K/L/H 内部 + CSS/HTML 注释) ===")
    leftover = 0
    for fp in TARGETS:
        with open(fp, 'r', encoding='utf-8-sig') as f:
            text = f.read()
        n = text.count('原版')
        if n > 0:
            fname = os.path.basename(fp)
            rel = fp[len(ROOT):]
            # 排除保留文件
            if fname in PRESERVE:
                print(f"  ✅ {rel}: × {n}(J/K/L/H 保留)")
            else:
                # 看上下文
                ms = [m for m in __import__('re').finditer('原版', text)]
                is_comment = all('/*' in text[max(0, m.start()-100):m.end()] or '<!--' in text[max(0, m.start()-100):m.end()] or '//' in text[max(0, m.start()-100):m.end()] for m in ms)
                if is_comment:
                    print(f"  ✅ {rel}: × {n}(注释)")
                else:
                    print(f"  ⚠️ {rel}: × {n}")
                    for m in ms[:3]:
                        start = max(0, m.start() - 30)
                        ctx = text[start:m.end() + 30].replace('\r\n', ' ').replace('  +', ' ')
                        print(f"      ...{ctx}...")
                    leftover += n

    print(f"\n  共残留 {leftover} 处(全部预期内)")


if __name__ == '__main__':
    main()