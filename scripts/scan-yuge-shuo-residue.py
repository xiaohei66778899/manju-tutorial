# -*- coding: utf-8 -*-
"""精细扫描:每文件统计 '玉哥说' 节标题、callout 旁白、冗余标记
输出:每个文件 '玉哥说'(标题+旁白)出现次数,以及冗余位置
"""
import os, sys, re
sys.stdout.reconfigure(encoding='utf-8')

ROOT = r'E:\AIGC\课件\12小说'

# 排除路径
EXCLUDE = ['node_modules', '.git', 'backup', '_brainmap', '_debug-archives', '_trash-removed', 'legacy']

results = []
for root, dirs, files in os.walk(ROOT):
    if any(seg in root for seg in EXCLUDE):
        continue
    for f in files:
        if not f.endswith('.html'):
            continue
        fp = os.path.join(root, f)
        try:
            with open(fp, 'rb') as fh:
                raw = fh.read()
            has_bom = raw.startswith(b'\xef\xbb\xbf')
            text = raw.decode('utf-8-sig') if has_bom else raw.decode('utf-8')
        except:
            continue

        # 统计:节标题里的"玉哥说" / callout 里的"玉哥说"(宽松正则)
        title_shuo = len(re.findall(r'<h\d[^>]*>[^<]*?玉哥说', text))
        # callout:任意位置"玉哥说"出现但不在 h2/h3 标题里
        callout_shuo = 0
        for m in re.finditer(r'玉哥说', text):
            pos = m.start()
            # 检查前面 100 字符内是否有 <h\d 标签
            before = text[max(0, pos-200):pos]
            if '<h' not in before[-200:]:
                callout_shuo += 1
        total_shuo = title_shuo + callout_shuo

        # 统计:每个"玉哥说"位置
        shuo_positions = []
        for m in re.finditer(r'玉哥说', text):
            shuo_positions.append(m.start())

        if total_shuo > 0:
            results.append((fp, title_shuo, callout_shuo, total_shuo, shuo_positions))

results.sort(key=lambda x: -x[3])

print(f"\n{'文件':<55} {'标题':>4} {'callout':>7} {'合计':>5} {'冗余位置'}")
print('-' * 130)
for fp, t, c, total, positions in results:
    name = os.path.relpath(fp, ROOT)
    extra = ''
    if total > 2:
        extra = ' ⚠️ 冗余(超过 2 处)'
    print(f"{name:<55} {t:>4} {c:>7} {total:>5} {positions[:5]}{extra}")

# 单独列出 >2 冗余
print('\n\n=== 冗余文件(>2 处"玉哥说")===')
for fp, t, c, total, _ in results:
    if total > 2:
        name = os.path.relpath(fp, ROOT)
        print(f"  {name} (合计 {total}, 标题 {t} + callout {c})")