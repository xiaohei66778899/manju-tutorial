#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理"-原版"后缀(从文件、JS、HTML 内容三层彻底清掉)。
玉哥原话:"-原版,删除"。
策略:
  1. 重命名 4 个文件 X-玉哥原版.html → X.html
  2. 改 .js 文件:X-玉哥原版.html → X.html,标题里的"玉哥原版" → ""
  3. 改 .html 文件:
     - X-玉哥原版 → X(任何残留引用)
     - X-原版.html → X.html
BOM 安全。
"""
import os
import sys
import shutil

sys.stdout.reconfigure(encoding='utf-8')

ROOT = r"E:\AIGC\课件\12小说"

# === Step 1: 重命名 4 个文件 ===
RENAMES = [
    ('ComfyUI漫剧工作流-玉哥原版.html', 'ComfyUI漫剧工作流.html'),
    ('千川投流SOP-玉哥原版.html', '千川投流SOP.html'),
    ('短剧AI仓库-玉哥原版.html', '短剧AI仓库.html'),
    ('短剧创业SOP-玉哥原版.html', '短剧创业SOP.html'),
]

# === Step 2: JS 文件替换 ===
JS_REPLACES = [
    # href 引用
    ('ComfyUI漫剧工作流-玉哥原版.html', 'ComfyUI漫剧工作流.html'),
    ('千川投流SOP-玉哥原版.html', '千川投流SOP.html'),
    ('短剧AI仓库-玉哥原版.html', '短剧AI仓库.html'),
    ('短剧创业SOP-玉哥原版.html', '短剧创业SOP.html'),
    # title 字段 "X 玉哥原版 Y" → "X Y"
    ('title: \'J 玉哥原版 ComfyUI 教程\'', 'title: \'J ComfyUI 教程\''),
    ('title: \'K 玉哥原版 千川投流 SOP v9.0\'', 'title: \'K 千川投流 SOP v9.0\''),
    ('title: \'L 玉哥原版 短剧 AI 仓库汇总\'', 'title: \'L 短剧 AI 仓库汇总\''),
    # label 字段 "X · Y · 玉哥原版" → "X · Y"
    ('J · ComfyUI 专题 · 玉哥原版', 'J · ComfyUI 专题'),
]

# === Step 3: HTML 文件替换 ===
HTML_REPLACES = [
    ('ComfyUI漫剧工作流-玉哥原版.html', 'ComfyUI漫剧工作流.html'),
    ('千川投流SOP-玉哥原版.html', '千川投流SOP.html'),
    ('短剧AI仓库-玉哥原版.html', '短剧AI仓库.html'),
    ('短剧创业SOP-玉哥原版.html', '短剧创业SOP.html'),
    # -原版.html 后缀(剩余)
    ('ComfyUI漫剧工作流-原版.html', 'ComfyUI漫剧工作流.html'),
    ('千川投流SOP-原版.html', '千川投流SOP.html'),
    ('短剧AI仓库-原版.html', '短剧AI仓库.html'),
    ('短剧创业SOP-原版.html', '短剧创业SOP.html'),
]


def step1_rename():
    print("=== Step 1: 重命名 4 个文件 ===\n")
    tutorial_dir = os.path.join(ROOT, 'site', 'tutorial')
    renamed = 0
    for old_name, new_name in RENAMES:
        # 找所有匹配文件
        for root, dirs, files in os.walk(tutorial_dir):
            if old_name in files:
                old_path = os.path.join(root, old_name)
                new_path = os.path.join(root, new_name)
                if os.path.exists(new_path):
                    print(f"  ⚠️ 已存在目标:{new_name}(跳过)")
                    continue
                shutil.move(old_path, new_path)
                print(f"  ✅ {old_name} → {new_name}")
                renamed += 1
    print(f"\n📊 共重命名 {renamed} 个文件\n")
    return renamed


def step2_clean_js():
    print("=== Step 2: 清理 JS 文件 ===\n")
    js_files = []
    for root, dirs, files in os.walk(os.path.join(ROOT, 'site')):
        for f in files:
            if f.endswith('.js'):
                js_files.append(os.path.join(root, f))

    total_replaced = 0
    for fp in js_files:
        with open(fp, 'rb') as f:
            raw = f.read()
        has_bom = raw.startswith(b'\xef\xbb\xbf')
        text = raw.decode('utf-8-sig') if has_bom else raw.decode('utf-8')
        orig = text
        for old, new in JS_REPLACES:
            text = text.replace(old, new)
        if text != orig:
            diff = sum(orig.count(o) for o, _ in JS_REPLACES if o in text) - sum(text.count(o) for o, _ in JS_REPLACES if o in text)
            # 简化统计:看 orig - text 中删除了多少字符(近似)
            out = (b'\xef\xbb\xbf' + text.encode('utf-8')) if has_bom else text.encode('utf-8')
            with open(fp, 'wb') as f:
                f.write(out)
            rel = fp[len(ROOT):]
            print(f"  ✅ {rel}")
            total_replaced += 1
    print(f"\n📊 共更新 {total_replaced} 个 JS\n")
    return total_replaced


def step3_clean_html():
    print("=== Step 3: 清理 HTML 文件内容 ===\n")
    targets = []
    for root, dirs, files in os.walk(os.path.join(ROOT, "site")):
        for f in files:
            if f.endswith(".html"):
                targets.append(os.path.join(root, f))
    JUBEN = os.path.join(ROOT, "剧本.html")
    if os.path.exists(JUBEN):
        targets.append(JUBEN)

    total_changed = 0
    for fp in targets:
        with open(fp, 'rb') as f:
            raw = f.read()
        has_bom = raw.startswith(b'\xef\xbb\xbf')
        text = raw.decode('utf-8-sig') if has_bom else raw.decode('utf-8')
        orig = text
        for old, new in HTML_REPLACES:
            text = text.replace(old, new)
        if text != orig:
            diff = orig.count('玉哥原版') - text.count('玉哥原版') + orig.count('-原版') - text.count('-原版')
            out = (b'\xef\xbb\xbf' + text.encode('utf-8')) if has_bom else text.encode('utf-8')
            with open(fp, 'wb') as f:
                f.write(out)
            rel = fp[len(ROOT):]
            print(f"  ✅ {rel} · -{diff}")
            total_changed += 1
    print(f"\n📊 共更新 {total_changed} 个 HTML\n")
    return total_changed


def verify():
    print("=== 残留核验 ===\n")
    targets = []
    for root, dirs, files in os.walk(os.path.join(ROOT, "site")):
        for f in files:
            if f.endswith(".html") or f.endswith(".js"):
                targets.append(os.path.join(root, f))
    JUBEN = os.path.join(ROOT, "剧本.html")
    if os.path.exists(JUBEN):
        targets.append(JUBEN)

    leftover_yu = 0
    leftover_yuanban = 0
    for fp in targets:
        with open(fp, 'r', encoding='utf-8-sig') as f:
            text = f.read()
        yu = text.count('玉哥原版')
        yb = text.count('-原版')
        if yu > 0:
            leftover_yu += yu
            rel = fp[len(ROOT):]
            print(f"  ⚠️ {rel}: '玉哥原版' × {yu}")
        if yb > 0:
            leftover_yuanban += yb
            rel = fp[len(ROOT):]
            print(f"  ⚠️ {rel}: '-原版' × {yb}")

    if leftover_yu == 0 and leftover_yuanban == 0:
        print(f"  ✅ 全部 {len(targets)} 个文件干净")
    else:
        print(f"\n  共残留:玉哥原版 {leftover_yu} / -原版 {leftover_yuanban}")


def main():
    step1_rename()
    step2_clean_js()
    step3_clean_html()
    verify()


if __name__ == '__main__':
    main()