#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理首页 index.html 里冗余的"玉哥"和"原版"修饰。
策略:
  - 保留:title/description 里的"玉哥"(品牌)
  - 保留:footer 里的"玉哥漫剧教程/玉哥带你/扫码关注玉哥/联系玉哥/© 玉哥"(品牌动作)
  - 保留:CSS/HTML 注释里的"玉哥"(技术注释)
  - 清掉:卡片描述、统计项、徽章、修饰短语里的"玉哥"和"原版"
BOM 安全。
"""
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

ROOT = r"E:\AIGC\课件\12小说"
FP = os.path.join(ROOT, "site", "index.html")


# 规则:按精确字符串替换(顺序很重要:先长串,后短串)
RULES = [
    # 卡片描述里的修饰(玉哥截图直接要求)
    ('原版 · 17 章 / 6 部分 · 离线数字教科书',
     '17 章 / 6 部分 · 离线数字教科书'),
    ('原版 v9.0 · 14 章 + 16 课视频路径',
     'v9.0 · 14 章 + 16 课视频路径'),
    ('玉哥 v18 汇总 · 工具/项目/脚本/GitHub 资源清单',
     'v18 汇总 · 工具/项目/脚本/GitHub 资源清单'),
    ('玉哥 v16 · 团队搭建 / 项目流 / 月入 30 万路径',
     'v16 · 团队搭建 / 项目流 / 月入 30 万路径'),

    # lead 描述
    ('玉哥 4 大原版专题 + 12 大类 135 节全完成',
     '12 大类 135 节全完成'),

    # 4 大原版专题 → 4 大专题(多处)
    ('4 大原版专题', '4 大专题'),

    # 统计项
    ('<span class="item"><b>4</b> 原版</span>',
     '<span class="item"><b>4</b> 专题</span>'),

    # 徽章
    ('<i class="fas fa-bolt"></i>原版</span>',
     '<i class="fas fa-bolt"></i>专题</span>'),

    # footer 来源标注
    ('教程内容源自原版课件 + AI 辅助编排',
     '教程内容 + AI 辅助编排'),

    # logo "v3 · 玉哥"(brand,保留)— 不动

    # 12 大类 + 4 大原版专题 → 12 大类 + 4 大专题
    ('12 大类 + 4 大原版专题', '12 大类 + 4 大专题'),
]


def main():
    print("=== 清理首页 '玉哥' / '原版' 修饰 ===\n")
    with open(FP, 'rb') as f:
        raw = f.read()
    has_bom = raw.startswith(b'\xef\xbb\xbf')
    text = raw.decode('utf-8-sig') if has_bom else raw.decode('utf-8')

    orig = text
    applied = []
    for old, new in RULES:
        if old in text:
            n = text.count(old)
            text = text.replace(old, new)
            applied.append((old, new, n))
            print(f"  ✅ '{old[:40]}...' → '{new[:40]}...' × {n}")

    print(f"\n📊 共应用 {len(applied)} 条规则\n")

    if text != orig:
        out = (b'\xef\xbb\xbf' + text.encode('utf-8')) if has_bom else text.encode('utf-8')
        with open(FP, 'wb') as f:
            f.write(out)
        print("✅ index.html 已保存")
    else:
        print("·  无变化")

    # 残留核验
    print("\n=== 残留 '玉哥' / '原版' 位置(独立修饰) ===")
    # '原版' 在 index.html 的所有位置
    for kw in ['原版']:
        ms = [m for m in __import__('re').finditer(kw, text)]
        print(f"  '{kw}' 出现 {len(ms)} 次:")
        for m in ms:
            start = max(0, m.start() - 25)
            ctx = text[start:m.end() + 25].replace('\r\n', ' ').replace('  +', ' ')
            print(f"    ...{ctx}...")


if __name__ == '__main__':
    main()