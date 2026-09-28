# -*- coding: utf-8 -*-
"""全站 '玉哥' 完整分类清单
- 品牌动作:logo / footer / QR / 联系 / 版权 → 保留
- 方法论署名:玉哥 5 原则 / 玉哥 SOP / 玉哥拆解 等 → 保留
- 语气标记:玉哥说 / 玉哥整理 等 → 已控制 ≤2 处/文件
- 元数据/版本:玉哥 v\d / v\d+ 等 → 已清理
"""
import os, sys, re
sys.stdout.reconfigure(encoding='utf-8')

ROOT = r'E:\AIGC\课件\12小说'
EXCLUDE = ['node_modules', '.git', 'backup', '_brainmap', '_debug-archives', '_trash-removed', 'legacy']

BRAND_PATTERNS = [
    r'<small>v\d+\s*·\s*玉哥</small>',  # logo v3 · 玉哥
    r'<div class="c-title">玉哥漫剧教程</div>',  # footer
    r'<div class="c-sub">玉哥带你',  # footer
    r'src="[^"]*qr-yuge\.png"[^>]*alt="扫码关注玉哥"',  # QR alt
    r'<div class="qr-cap">扫码关注玉哥</div>',  # QR cap
    r'<a[^>]*mailto:yuge[^>]*>[^<]*联系玉哥</a>',  # 联系玉哥
    r'<strong>玉哥</strong>\s*·\s*仅供学习交流',  # 版权 © 玉哥
]

# 统计每个文件每个"玉哥"的分类
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
        total = text.count('玉哥')
        if total == 0:
            continue

        # 统计品牌动作数量
        brand_count = 0
        for pat in BRAND_PATTERNS:
            brand_count += len(re.findall(pat, text))
        # 版权 © 玉哥 也会被品牌动作匹配
        # 实际上版权里也有"玉哥"两次("玉哥"出现 + strong)
        # 实际上版权位置是 © 2026 <strong>玉哥</strong>,只算 1 次

        # 计算非品牌"玉哥"
        non_brand = total - brand_count

        name = os.path.relpath(fp, ROOT)
        if non_brand > 7:  # 正常教程页有 ~7 处 footer 品牌动作,超 7 的就是方法论/语气标记
            print(f"📊 {name:<55} 总:{total:>3} 品牌:{brand_count:>2} 非品牌:{non_brand:>3}")