# -*- coding: utf-8 -*-
"""
极致克制 footer(Apple/Netflix 风格参考):
- 单列居中纵向堆叠
- 5 条以内内容(品牌/副标题/QR/链接/版权)
- 链接 inline + · 分隔(更克制)
- 整体 max-width 540px 居中,大量留白
- 移动端自然垂直堆叠
"""
from pathlib import Path

ROOT = Path(r"E:\AIGC\课件\12小说")

NEW_FOOTER_SITE = '''<footer class="dock-run compact">
  <div class="compact-stack">

    <div class="c-title">玉哥漫剧教程</div>
    <div class="c-sub">玉哥带你从 0 做出一部能上线的漫剧</div>

    <div class="c-qr" title="后期放公众号二维码">
      <div class="qr-img">QR</div>
      <div class="qr-cap">扫码关注玉哥</div>
    </div>

    <ul class="c-links">
      <li><a href="changelog.html">📅 更新日志</a></li>
      <li><a href="mailto:yuge@local.demo">✉ 联系玉哥</a></li>
    </ul>

  </div>

  <div class="c-copy">
    © 2026 <strong>玉哥</strong> · 仅供学习交流 · 京 ICP 备 XXXXXXXX 号(待补)
    <div class="c-copy-sub">教程内容源自玉哥原版课件 + AI 辅助编排</div>
  </div>
</footer>'''

NEW_FOOTER_TUTORIAL = '''<footer class="dock-run compact">
  <div class="compact-stack">

    <div class="c-title">玉哥漫剧教程</div>
    <div class="c-sub">玉哥带你从 0 做出一部能上线的漫剧</div>

    <div class="c-qr" title="后期放公众号二维码">
      <div class="qr-img">QR</div>
      <div class="qr-cap">扫码关注玉哥</div>
    </div>

    <ul class="c-links">
      <li><a href="../index.html">🏠 回到首页</a></li>
      <li><a href="../changelog.html">📅 更新日志</a></li>
      <li><a href="mailto:yuge@local.demo">✉ 联系玉哥</a></li>
    </ul>

  </div>

  <div class="c-copy">
    © 2026 <strong>玉哥</strong> · 仅供学习交流 · 京 ICP 备 XXXXXXXX 号(待补)
    <div class="c-copy-sub">教程内容源自玉哥原版课件 + AI 辅助编排</div>
  </div>
</footer>'''

NEW_CSS = """
/* ============== 极致克制 footer(Apple/Netflix 风格参考 · 单列居中纵向堆叠) ============== */
footer.dock-run.compact {
  padding: 36px 24px 24px;
  border-top: 1px solid var(--line);
  background: var(--bg2);
  color: var(--muted);
}
footer.dock-run.compact .compact-stack {
  max-width: 540px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 14px;
  padding-bottom: 24px;
  border-bottom: 1px dashed var(--line);
}
footer.dock-run.compact .c-title {
  font-size: 18px;
  font-weight: 700;
  letter-spacing: 0.05em;
  color: var(--text);
  text-align: center;
  margin-bottom: 2px;
}
footer.dock-run.compact .c-sub {
  font-size: 13px;
  line-height: 1.7;
  color: var(--muted);
  text-align: center;
  max-width: 460px;
}
footer.dock-run.compact .c-qr {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  margin-top: 4px;
}
footer.dock-run.compact .c-qr .qr-img {
  width: 84px;
  height: 84px;
  border: 1.5px dashed var(--line);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.06em;
  color: var(--muted);
  background: var(--bg);
  transition: border-color .2s, color .2s;
}
footer.dock-run.compact .c-qr .qr-img:hover {
  border-color: var(--blue);
  color: var(--blue);
}
footer.dock-run.compact .c-qr .qr-cap {
  font-size: 11.5px;
  color: var(--muted);
  letter-spacing: 0.04em;
}
footer.dock-run.compact .c-links {
  list-style: none;
  margin: 6px 0 0;
  padding: 0;
  display: inline-flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 0;
  font-size: 13px;
}
footer.dock-run.compact .c-links li {
  display: inline-flex;
  align-items: center;
}
footer.dock-run.compact .c-links li + li::before {
  content: '·';
  display: inline-block;
  margin: 0 14px;
  color: var(--muted-2, #A1A1AA);
  pointer-events: none;
}
footer.dock-run.compact .c-links a {
  color: var(--muted);
  text-decoration: none;
  transition: color .15s;
}
footer.dock-run.compact .c-links a:hover {
  color: var(--blue);
}
footer.dock-run.compact .c-copy {
  max-width: 540px;
  margin: 18px auto 0;
  padding: 0 24px;
  font-size: 12.5px;
  color: var(--muted);
  text-align: center;
  line-height: 1.7;
}
footer.dock-run.compact .c-copy strong {
  color: var(--text);
  font-weight: 600;
}
footer.dock-run.compact .c-copy .c-copy-sub {
  margin-top: 6px;
  font-size: 11.5px;
  color: var(--muted-2, #A1A1AA);
}

/* 暗色主题适配 */
[data-theme="dark"] footer.dock-run.compact .c-title { color: #fff; }
[data-theme="dark"] footer.dock-run.compact .c-copy strong { color: #fff; }
[data-theme="dark"] footer.dock-run.compact .c-links a { color: var(--muted); }
[data-theme="dark"] footer.dock-run.compact .c-qr .qr-img {
  background: rgba(255,255,255,.04);
  border-color: rgba(255,255,255,.18);
}
"""


def replace_footer(p: Path, new_footer: str):
    src = p.read_text(encoding="utf-8")
    # 找旧的 compact footer 起点
    start = src.find('<footer class="dock-run compact">')
    if start < 0:
        start = src.find('<footer class="dock-run">')
    if start < 0:
        print(f"[SKIP] {p.name} no footer found")
        return False
    end = src.find('</footer>', start)
    if end < 0:
        return False
    end += len('</footer>')
    new_src = src[:start] + new_footer + src[end:]
    p.write_text(new_src, encoding="utf-8")
    print(f"[OK] {p.name} footer rewritten -> {len(new_footer)} bytes")
    return True


def replace_css(css_path: Path, new_css: str):
    cur = css_path.read_text(encoding="utf-8")
    # 查找旧 compact footer CSS 区段起点
    start = cur.find('/* ============== 克制 footer')
    if start < 0:
        # 直接追加
        css_path.write_text(cur.rstrip() + "\n" + new_css + "\n", encoding="utf-8")
        print(f"[OK] {css_path.name} CSS appended (no old section)")
        return True
    # 查找旧区段的结束 —— 找下一个 /* ============== 或文件尾
    end = cur.find('/* ==============', start + 30)
    if end < 0:
        end = len(cur)
    new = cur[:start].rstrip() + "\n" + new_css + "\n" + cur[end:]
    css_path.write_text(new, encoding="utf-8")
    print(f"[OK] {css_path.name} CSS replaced")
    return True


if __name__ == "__main__":
    replace_footer(ROOT / "site" / "index.html", NEW_FOOTER_SITE)
    replace_footer(ROOT / "site" / "tutorial" / "index.html", NEW_FOOTER_TUTORIAL)
    replace_css(ROOT / "site" / "assets" / "site.css", NEW_CSS)
    print("done")
