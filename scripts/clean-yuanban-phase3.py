#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
第三轮:补漏 — 清理剩下 2 处"原版"残留。
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

RULES = [
    # tutorial/index "4 张原版专题"
    ('<b>4</b> 张原版专题</div>', '<b>4</b> 张专题</div>'),
    # tools/index "玉哥</span>原版课件推荐"
    ('玉哥</span>原版课件推荐', '玉哥</span>课件推荐'),
]


def clean_file(fp):
    with open(fp, 'rb') as f:
        raw = f.read()
    has_bom = raw.startswith(b'\xef\xbb\xbf')
    text = raw.decode('utf-8-sig') if has_bom else raw.decode('utf-8')
    orig = text
    for old, new in RULES:
        text = text.replace(old, new)
    if text != orig:
        diff = len(orig) - len(text)
        out = (b'\xef\xbb\xbf' + text.encode('utf-8')) if has_bom else text.encode('utf-8')
        with open(fp, 'wb') as f:
            f.write(out)
        return True, diff
    return False, 0


def main():
    print("=== 第三轮:补漏清理 ===\n")
    total = 0
    for fp in TARGETS:
        ok, diff = clean_file(fp)
        rel = fp[len(ROOT):]
        if ok:
            print(f"  ✅ {rel} · -{diff}")
            total += 1
    print(f"\n📊 共更新 {total} 个文件\n")


if __name__ == '__main__':
    main()