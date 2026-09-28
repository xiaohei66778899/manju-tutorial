#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
恢复"重点提醒"section 的"玉哥说:"作者旁白风格。
策略:
  1. h2 标题: "重点提醒</h2>" → "玉哥说</h2>"
  2. callout 顶部: "玉哥说</h2>" 后第一个 "<p><br>" → "<p><strong>📢 玉哥说</strong>:<br>"
Windows \r\n 安全(用 find + slice,不依赖 regex)。
"""
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

DIR = r"E:\AIGC\课件\12小说\site\tutorial\A-manju-basic"


def restore_file(fp):
    with open(fp, 'rb') as f:
        raw = f.read()
    has_bom = raw.startswith(b'\xef\xbb\xbf')
    text = raw.decode('utf-8-sig') if has_bom else raw.decode('utf-8')

    orig = text

    # Step 1: h2 标题
    text = text.replace('重点提醒</h2>', '玉哥说</h2>')

    # Step 2: 找每个 "玉哥说</h2>" 后第一个 "<p><br>"
    # 每文件最多 1 处(已确认)
    needle = '玉哥说</h2>'
    p_marker = '<p><br>'
    new_p = '<p><strong>📢 玉哥说</strong>:<br>'

    idx = 0
    while True:
        h2_idx = text.find(needle, idx)
        if h2_idx == -1:
            break
        # 在 h2 后 1000 字符内找第一个 <p><br>
        p_idx = text.find(p_marker, h2_idx)
        if p_idx != -1 and (p_idx - h2_idx) < 1000:
            text = text[:p_idx] + new_p + text[p_idx + len(p_marker):]
        idx = h2_idx + len(needle)

    if text != orig:
        out = (b'\xef\xbb\xbf' + text.encode('utf-8')) if has_bom else text.encode('utf-8')
        with open(fp, 'wb') as f:
            f.write(out)
        return True
    return False


def count_markers(fp):
    with open(fp, 'r', encoding='utf-8-sig') as f:
        text = f.read()
    h2_count = text.count('玉哥说</h2>')
    callout_count = text.count('<strong>📢 玉哥说</strong>:<br>')
    other_junk = 0
    for p in ['玉哥学员首选', '玉哥学员常用', '玉哥推荐', '玉哥时间']:
        other_junk += text.count(p)
    return h2_count, callout_count, other_junk


def main():
    files = sorted(f for f in os.listdir(DIR)
                   if f.startswith('A-') and f.endswith('.html'))

    print("=== 恢复 '玉哥说' 作者旁白(只在'重点提醒'章节) ===\n")
    changed = 0
    for fn in files:
        fp = os.path.join(DIR, fn)
        if restore_file(fp):
            print(f"  ✅ {fn} 已恢复")
            changed += 1
        else:
            print(f"  ·  {fn} 无变化")

    print(f"\n📊 共更新 {changed}/{len(files)} 个文件\n")

    print("=== '玉哥说' 作者旁白分布 ===")
    print("(预期:每文件 1 个 h2 标题 + 1 个 callout 旁白 = 有调性的'作者旁白'风格)\n")
    for fn in files:
        fp = os.path.join(DIR, fn)
        h2, callout, junk = count_markers(fp)
        if h2 == 1 and callout == 1 and junk == 0:
            print(f"  ✅ {fn}: h2 标题×{h2}, 📢旁白×{callout}, 其它语气×{junk}")
        else:
            print(f"  ⚠️ {fn}: h2 标题×{h2}, 📢旁白×{callout}, 其它语气×{junk}")


if __name__ == '__main__':
    main()