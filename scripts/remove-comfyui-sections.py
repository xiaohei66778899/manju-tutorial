#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
删除 C/D/E/F/G 目录中所有讲 ComfyUI 的板块。
规则:
  - 整章 ComfyUI 主题 -> 替换 main 内容为跳转占位
  - 整节 ComfyUI 主题 -> 删除该 h2 节
  - 单行 ComfyUI 提及 -> 替换 "ComfyUI" 为 "本地出图工具" (避免读者以为本站讲 ComfyUI)
"""
import re
import sys
from pathlib import Path

ROOT = Path(r"E:\AIGC\课件\12小说\site\tutorial")

# 整章 ComfyUI 主题 -> 替换为跳转占位
WHOLE_CHAPTER_REPLACE = {
    "E-ai-image/E-24.html": "本地出图工具横评(已并入 ComfyUI 专题)",
    "E-ai-image/E-31.html": "ComfyUI 工作流分享与社区(已并入 ComfyUI 专题)",
    "F-ai-video/F-7.html": "AnimateDiff 简介(已并入 ComfyUI 专题)",
}

# 整节 ComfyUI 主题 -> 删除该 h2 节 (从 h2 标题到下一个 h2 之前)
# 格式: (file, 节标题或关键词)
SECTION_REMOVE = {
    "E-ai-image/E-33.html": ["工作流问题"],
    "C-character/C-4.html": ["ComfyUI 装 FaceID 步骤"],
    "C-character/C-13.html": ["ComfyUI 装 IP-Adapter"],
    "C-character/C-12.html": ["ComfyUI IP-Adapter 接法"],
    "C-character/C-16.html": ["ComfyUI 解决方案"],
    "F-ai-video/F-8.html": ["Wan 工作流"],
    "F-ai-video/F-9.html": ["工作流"],  # F-9 sec-4 标题
}

# 单行 ComfyUI 提及 -> 把 "ComfyUI" 替换为中性表述
LINE_REPLACE = {
    "E-ai-image/E-1.html": True,
    "E-ai-image/E-20.html": True,
    "E-ai-image/E-25.html": True,
    "E-ai-image/E-26.html": True,
    "E-ai-image/E-29.html": True,
    "E-ai-image/E-34.html": True,
    "C-character/C-2.html": True,
    "C-character/C-8.html": True,
    "C-character/C-10.html": True,
    "C-character/C-14.html": True,
    "D-storyboard/D-12.html": True,
    "F-ai-video/F-1.html": True,
    "F-ai-video/F-2.html": True,
    "F-ai-video/F-3.html": True,
    "F-ai-video/F-4.html": True,
    "F-ai-video/F-17.html": True,
    "F-ai-video/F-18.html": True,
}

REDIRECT_BLOCK = """
    <div class="callout warn" style="margin-top:48px"><span class="ico">📦</span>
      <p><strong>本节已并入 ComfyUI 专题</strong> · 不再在本教程展开。<br>
      ComfyUI 安装 / 工作流 / 节点 / 调试全集中在 <a href="../../../comfyui/index.html">ComfyUI 专题</a>,避免重复。</p>
    </div>
"""


def replace_main(content: str, label: str) -> str:
    """把 <main class="content">...</main> 内容替换为跳转占位,但保留 h1 + breadcrumb。"""
    # 找到 <main class="content"> 开始
    m = re.search(r'(<main class="content">)(.*?)(</main>)', content, re.DOTALL)
    if not m:
        return content
    inner = m.group(2)

    # 提取 breadcrumb 行
    bc = re.search(r'<div class="breadcrumb">.*?</div>', inner, re.DOTALL)
    bc_html = bc.group(0) if bc else ""

    # 提取 h1
    h1 = re.search(r'<h1>.*?</h1>', inner, re.DOTALL)
    h1_html = h1.group(0) if h1 else ""

    # 保留 prev/next 底部导航
    bnav = re.search(r'<nav class="bottom-nav">.*?</nav>', inner, re.DOTALL)
    bnav_html = bnav.group(0) if bnav else ""

    new_inner = (
        bc_html + "\n    " + h1_html + "\n"
        + f'    <p class="meta">{label} · 内容已迁移</p>\n'
        + REDIRECT_BLOCK
        + "\n    " + bnav_html
    )
    return content[:m.start()] + m.group(1) + new_inner + m.group(3) + content[m.end():]


def remove_h2_sections(content: str, headings: list) -> tuple[str, int]:
    """删除指定 h2 标题所在的 h2 节(从该 h2 到下一个 h2 之前)。返回 (新内容, 删除节数)。"""
    removed = 0
    for heading in headings:
        # 匹配 <h2 id="...">标题文字</h2> 一直到下一个 <h2 或 <nav class="bottom-nav">
        # 用 \n\s*<h2 兼容 1 个或多个换行 + 任意空白
        pattern = re.compile(
            r'\n\s*<h2 id="[^"]+">' + re.escape(heading) + r'.*?</h2>(.*?)(?=\n\s*<h[12]|\n\s*<nav class="bottom-nav">|\Z)',
            re.DOTALL
        )
        new_content, n = pattern.subn("", content, count=1)
        if n > 0:
            content = new_content
            removed += 1
            print(f"    - removed h2: {heading}")
        else:
            print(f"    [WARN] no match for h2: {heading}")
    return content, removed


def replace_comfyui_lines(content: str) -> tuple[str, int]:
    """把文件中所有 ComfyUI 提及替换为中性表述。"""
    # 各种 ComfyUI 表述 -> 中性词
    replacements = [
        ("ComfyUI-Impact-Pack", "Impact-Pack 节点"),
        ("ComfyUI-IPAdapter", "IPAdapter 节点"),
        ("ComfyUI-AnimateDiff-Evolved", "AnimateDiff-Evolved 节点"),
        ("ComfyUI-Manager", "节点管理器"),
        ("ComfyUI Manager", "节点管理器"),
        ("ComfyUI 工作流", "节点工作流"),
        ("ComfyUI 工作流分享", "工作流分享"),
        ("ComfyUI workflow", "节点 workflow"),
        ("ComfyUI/models/", "本地 models/"),
        ("ComfyUI/custom_nodes/", "本地 custom_nodes/"),
        ("ComfyUI 装", "本地安装 "),
        ("ComfyUI 加", "本地加 "),
        ("ComfyUI 节点", "节点"),
        ("ComfyUI 加载", "本地加载"),
        ("ComfyUI 测试", "本地测试"),
        ("ComfyUI 反推", "本地反推"),
        ("ComfyUI 混合", "本地混合"),
        ("ComfyUI 跑", "本地跑"),
        ("ComfyUI 出", "本地出"),
        ("ComfyUI 有", "本地工作流有"),
        ("ComfyUI 是", "本地工作流是"),
        ("重启 ComfyUI", "重启本地"),
        ("拖入 ComfyUI", "拖入本地"),
        ("ComfyUI", "本地出图工具"),
    ]
    total = 0
    for old, new in replacements:
        if old in content:
            count = content.count(old)
            content = content.replace(old, new)
            total += count
    return content, total


def process_file(rel: str) -> dict:
    path = ROOT / rel
    if not path.exists():
        return {"file": rel, "error": "not found"}

    original = path.read_text(encoding="utf-8")
    content = original

    log = {"file": rel}

    # 1. 整章替换
    if rel in WHOLE_CHAPTER_REPLACE:
        content = replace_main(content, WHOLE_CHAPTER_REPLACE[rel])
        log["action"] = "redirect-placeholder"
        log["label"] = WHOLE_CHAPTER_REPLACE[rel]

    # 2. 整节删除
    elif rel in SECTION_REMOVE:
        content, removed = remove_h2_sections(content, SECTION_REMOVE[rel])
        log["action"] = "remove-sections"
        log["removed_count"] = removed

    # 3. 单行替换
    elif rel in LINE_REPLACE:
        content, replaced = replace_comfyui_lines(content)
        log["action"] = "replace-lines"
        log["replaced_count"] = replaced

    else:
        log["action"] = "skip"
        return log

    if content != original:
        path.write_text(content, encoding="utf-8")
        log["changed"] = True
    else:
        log["changed"] = False
    return log


def main():
    files = sorted(set(WHOLE_CHAPTER_REPLACE) | set(SECTION_REMOVE) | set(LINE_REPLACE))
    print(f"Total files: {len(files)}\n")

    total_removed_sections = 0
    total_replaced_lines = 0
    total_redirects = 0

    for rel in files:
        log = process_file(rel)
        if "error" in log:
            print(f"❌ {rel}: {log['error']}")
            continue
        action = log.get("action")
        if action == "redirect-placeholder":
            total_redirects += 1
            print(f"📦 {rel}: redirect → {log.get('label')}")
        elif action == "remove-sections":
            n = log.get("removed_count", 0)
            total_removed_sections += n
            print(f"🗑️  {rel}: removed {n} section(s)")
        elif action == "replace-lines":
            n = log.get("replaced_count", 0)
            total_replaced_lines += n
            print(f"✏️  {rel}: replaced {n} ComfyUI mentions")
        elif action == "skip":
            print(f"⏭  {rel}: skipped")

    print(f"\n========================================")
    print(f"📦 Redirect placeholders: {total_redirects}")
    print(f"🗑️  Sections removed: {total_removed_sections}")
    print(f"✏️  Line replacements: {total_replaced_lines}")


if __name__ == "__main__":
    main()