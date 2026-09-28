#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量清理 tutorial.js 里 SIDEBAR 类目标题的"· N 节"/"· 8 大子页面"尾巴。
按玉哥"调性"原则:只保留类目名,删节数统计。
BOM 安全,纯字符串替换。
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

FP = r"E:\AIGC\课件\12小说\site\assets\tutorial.js"

RULES = [
    # SIDEBAR 类目标题
    ("title: '剧本 · 8 大子页面',",
     "title: '剧本',"),
    ("title: '角色制作 · 17 节',",
     "title: '角色制作',"),
    ("title: '分镜 · 15 节',",
     "title: '分镜',"),
    ("title: 'AI 出图 · 35 节',",
     "title: 'AI 出图',"),
    ("title: 'AI 视频 · 19 节',",
     "title: 'AI 视频',"),
    ("title: '配音剪辑 · 18 节',",
     "title: '配音剪辑',"),
    ("title: '发布运营 · 10 节',",
     "title: '发布运营',"),
    ("title: '附录速查 · 9 节',",
     "title: '附录速查',"),

    # B 模块的子项
    ("title: 'B · 剧本板块(8 大子页面)'",
     "title: 'B · 剧本板块'"),
]


def main():
    with open(FP, 'rb') as f:
        raw = f.read()
    has_bom = raw.startswith(b'\xef\xbb\xbf')
    text = raw.decode('utf-8-sig') if has_bom else raw.decode('utf-8')

    orig = text
    print("=== 批量清理 SIDEBAR 类目尾巴 ===\n")
    for old, new in RULES:
        if old in text:
            text = text.replace(old, new)
            print(f"  ✅ 已改: {old}")
        else:
            print(f"  ·  未找到: {old}")

    if text != orig:
        out = (b'\xef\xbb\xbf' + text.encode('utf-8')) if has_bom else text.encode('utf-8')
        with open(FP, 'wb') as f:
            f.write(out)
        print(f"\n✅ tutorial.js 已保存")
    else:
        print("\n·  无变化")

    # 校验
    print("\n=== 清理后剩余 '· N 节' / '· 8 大子页面' ===")
    print("(应只剩 B 板块本身的子项链接)")
    import re
    leftovers = re.findall(r"title: '[^']*·[^']*'", text)
    for l in leftovers:
        print(f"  · {l}")


if __name__ == '__main__':
    main()