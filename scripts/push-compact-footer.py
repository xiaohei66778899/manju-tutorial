# -*- coding: utf-8 -*-
"""
批量同步极致克制 footer 到全站 HTML。
跳过已改:
- site/index.html
- site/tutorial/index.html
按层级计算前缀:
- 1 段: site/*.html          -> 同级
- 2 段: site/<dir>/*.html     -> ../
- 3 段: site/tutorial/<cat>/*.html -> ../../
"""
from pathlib import Path

ROOT = Path(r"E:\AIGC\课件\12小说")
SITE = ROOT / "site"

SKIP = {
    (SITE / "index.html"),
    (SITE / "tutorial" / "index.html"),
}


def depth_of(p: Path) -> int:
    rel = p.relative_to(SITE)
    return len(rel.parts)


def make_footer(file_path: Path) -> str:
    depth = depth_of(file_path)
    prefix = "../" * max(0, depth - 1) if depth > 0 else ""
    name = file_path.name

    items = []
    if name != "changelog.html":
        items.append(f'<li><a href="{prefix}changelog.html">📅 更新日志</a></li>')
    items.append('<li><a href="mailto:yuge@local.demo">✉ 联系玉哥</a></li>')
    links = "\n      ".join(items)

    return f'''<footer class="dock-run compact">
  <div class="compact-stack">

    <div class="c-title">玉哥漫剧教程</div>
    <div class="c-sub">玉哥带你从 0 做出一部能上线的漫剧</div>

    <div class="c-qr" title="后期放公众号二维码">
      <div class="qr-img">QR</div>
      <div class="qr-cap">扫码关注玉哥</div>
    </div>

    <ul class="c-links">
      {links}
    </ul>

  </div>

  <div class="c-copy">
    © 2026 <strong>玉哥</strong> · 仅供学习交流 · 京 ICP 备 XXXXXXXX 号(待补)
    <div class="c-copy-sub">教程内容源自玉哥原版课件 + AI 辅助编排</div>
  </div>
</footer>'''


def replace_one(p: Path):
    src = p.read_text(encoding="utf-8")
    # 宽松匹配任意 <footer ...> 起点
    start = src.find('<footer')
    if start < 0:
        return False, "no footer"

    # 找到对应的 </footer>
    end = src.find('</footer>', start)
    if end < 0:
        return False, "no end"

    # 已经是新版 compact-stack,跳过
    chunk = src[start:end]
    if 'compact-stack' in chunk or 'compact-row' in chunk:
        return False, "already compact-stack"

    end += len('</footer>')
    new_src = src[:start] + make_footer(p) + src[end:]
    p.write_text(new_src, encoding="utf-8")
    return True, "ok"


def main():
    count_ok = 0
    count_skip_existing = 0
    count_skip_no_footer = 0
    count_error = 0
    errors = []

    candidates = list(SITE.rglob("*.html"))
    for p in sorted(candidates):
        if p in SKIP:
            count_skip_existing += 1
            continue
        # 排除 _debug-archives
        if "_debug-archives" in str(p):
            continue
        try:
            ok, reason = replace_one(p)
            if ok:
                count_ok += 1
                print(f"[OK]    {p.relative_to(ROOT)}")
            elif reason == "already compact-stack":
                count_skip_existing += 1
            elif reason == "no footer":
                count_skip_no_footer += 1
            else:
                count_error += 1
                errors.append((p, reason))
        except Exception as e:
            count_error += 1
            errors.append((p, str(e)))

    print()
    print("=" * 60)
    print(f"  重写成功:    {count_ok}")
    print(f"  已新版跳过:  {count_skip_existing}")
    print(f"  无 footer:   {count_skip_no_footer}")
    print(f"  错误:        {count_error}")
    if errors:
        print()
        print("错误列表:")
        for p, msg in errors:
            print(f"  - {p.relative_to(ROOT)}: {msg}")


if __name__ == "__main__":
    main()
