#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

with open(r"E:\AIGC\课件\12小说\site\tutorial\C-character\C-4.html", 'rb') as f:
    raw = f.read()

print('Total bytes:', len(raw))
print('Starts with BOM:', raw[:3] == b'\xef\xbb\xbf')
print('First 50 bytes hex:', raw[:50].hex())

# decode
text = raw.decode('utf-8-sig')  # 处理 BOM
print('After BOM-strip, len:', len(text))

# 找 sec-3
idx = text.find('ComfyUI 装 FaceID 步骤')
print('sec-3 found at:', idx)
if idx >= 0:
    snippet = text[idx-30:idx+50]
    print('snippet repr:', repr(snippet))
    # 字节级
    print('snippet bytes:', snippet.encode('utf-8').hex())

# 测试直白匹配
heading = 'ComfyUI 装 FaceID 步骤'
print('heading bytes:', heading.encode('utf-8').hex())
print('contains heading:', heading in text)

# 测试简单正则
p = re.compile(re.escape(heading))
print('search with escape:', p.search(text) is not None)

# 测试 h2 全模式
p2 = re.compile(r'<h2 id="sec-3">' + re.escape(heading) + r'</h2>')
print('search with h2:', p2.search(text) is not None)

# 加 .\s*
p3 = re.compile(r'<h2 id="sec-3">.*?' + re.escape(heading) + r'.*?</h2>', re.DOTALL)
print('search with .*?:', p3.search(text) is not None)