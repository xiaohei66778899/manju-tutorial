# -*- coding: utf-8 -*-
"""
精简 footer(方案 D):
- 品牌区(玉哥漫剧教程 + 一句话)
- 链接区(更新日志 + 联系玉哥)
- 版权(© 2026 · 仅供学习 · 备案占位 · 不展示版本号)
- 抛弃原 4 列 dl 布局 → flex 简洁布局
"""
from pathlib import Path

ROOT = Path(r"E:\AIGC\课件\12小说")

# 两个文件 footer 要替换的起止标记
TARGETS = [
    {
        "path": ROOT / "site" / "index.html",
        "start_marker": '<footer class="dock-run">',
        "end_marker": "</footer>",
        "new_footer": '''<footer class="dock-run compact">
  <div class="compact-wrap">

    <div class="c-brand">
      <div class="c-title">玉哥漫剧教程</div>
      <div class="c-sub">玉哥带你从 0 做出一部能上线的漫剧</div>
    </div>

    <ul class="c-links">
      <li><a href="changelog.html">📅 更新日志</a></li>
      <li><a href="mailto:yuge@local.demo">✉ 联系玉哥</a></li>
    </ul>

    <div class="c-qr" title="后期放公众号二维码">
      <div class="qr-img">QR</div>
      <div class="qr-cap">扫码关注玉哥</div>
    </div>

  </div>

  <div class="c-copy">
    © 2026 <strong>玉哥</strong> · 仅供学习交流 · 京 ICP 备 XXXXXXXX 号(待补)
    <div class="c-copy-sub">教程内容源自玉哥原版课件 + AI 辅助编排</div>
  </div>
</footer>''',
        "script_path": 'site/assets/site-enhance.js',
    },
    {
        "path": ROOT / "site" / "tutorial" / "index.html",
        "start_marker": '<footer class="dock-run">',
        "end_marker": "</footer>",
        "new_footer": '''<footer class="dock-run compact">
  <div class="compact-wrap">

    <div class="c-brand">
      <div class="c-title">玉哥漫剧教程</div>
      <div class="c-sub">玉哥带你从 0 做出一部能上线的漫剧</div>
    </div>

    <ul class="c-links">
      <li><a href="../index.html">🏠 回到首页</a></li>
      <li><a href="../changelog.html">📅 更新日志</a></li>
      <li><a href="mailto:yuge@local.demo">✉ 联系玉哥</a></li>
    </ul>

    <div class="c-qr" title="后期放公众号二维码">
      <div class="qr-img">QR</div>
      <div class="qr-cap">扫码关注玉哥</div>
    </div>

  </div>

  <div class="c-copy">
    © 2026 <strong>玉哥</strong> · 仅供学习交流 · 京 ICP 备 XXXXXXXX 号(待补)
    <div class="c-copy-sub">教程内容源自玉哥原版课件 + AI 辅助编排</div>
  </div>
</footer>''',
        "script_path": 'assets/site-enhance.js',
    },
]

# 追加的 CSS(克制 footer 样式)
APPEND_CSS = """

/* ============== 克制 footer(方案 D · 2 链接 + 品牌 + 版权) ============== */
footer.dock-run.compact {
  padding: 32px 24px 22px;
}
footer.dock-run.compact .compact-wrap {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 32px;
  padding-bottom: 22px;
  border-bottom: 1px dashed var(--line);
  flex-wrap: wrap;
}
footer.dock-run.compact .c-brand {
  flex: 1 1 320px;
  min-width: 260px;
}
footer.dock-run.compact .c-title {
  font-size: 18px;
  font-weight: 700;
  letter-spacing: 0.02em;
  color: var(--text);
  margin-bottom: 6px;
}
footer.dock-run.compact .c-sub {
  font-size: 13px;
  line-height: 1.6;
  color: var(--muted);
  max-width: 380px;
}
footer.dock-run.compact .c-links {
  list-style: none;
  margin: 0;
  padding: 8px 0 0;
  display: flex;
  gap: 28px;
  flex-wrap: wrap;
  font-size: 13.5px;
}
footer.dock-run.compact .c-links li { margin: 0; }
footer.dock-run.compact .c-links a {
  color: var(--muted);
  text-decoration: none;
  transition: color .15s;
  border-bottom: 1px dotted transparent;
}
footer.dock-run.compact .c-links a:hover {
  color: var(--blue);
  border-bottom-color: var(--blue);
}
footer.dock-run.compact .c-copy {
  max-width: 1200px;
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
@media (max-width: 700px) {
  footer.dock-run.compact .compact-wrap {
    flex-direction: column;
    gap: 16px;
  }
  footer.dock-run.compact .c-links {
    padding-top: 0;
    gap: 18px;
  }
}

/* 暗色主题适配 */
[data-theme="dark"] footer.dock-run.compact .c-title { color: #fff; }
[data-theme="dark"] footer.dock-run.compact .c-copy strong { color: #fff; }
[data-theme="dark"] footer.dock-run.compact .c-links a { color: var(--muted); }
"""


def replace_footer(target):
    p = Path(target["path"])
    src = p.read_text(encoding="utf-8")

    # 找 footer 起止
    start_idx = src.find(target["start_marker"])
    if start_idx < 0:
        print(f"[WARN] {p.name} footer start not found, skip")
        return False

    # 从 start_idx 之前的换行开始截,前面留换行
    # end_marker 是 </footer>,我们要替换 ...整个...</footer>
    end_idx = src.find(target["end_marker"], start_idx)
    if end_idx < 0:
        print(f"[WARN] {p.name} footer end not found, skip")
        return False
    end_idx += len(target["end_marker"])

    new_src = src[:start_idx] + target["new_footer"] + src[end_idx:]
    p.write_text(new_src, encoding="utf-8")
    print(f"[OK] {p} footer rewritten ({end_idx - start_idx} -> {len(target['new_footer'])} bytes)")
    return True


def append_css(css_path, css_chunk):
    p = Path(css_path)
    if not p.exists():
        print(f"[WARN] {css_path} not found")
        return False
    cur = p.read_text(encoding="utf-8")
    if "footer.dock-run.compact" in cur:
        print(f"[SKIP] {css_path} already has compact footer CSS")
        return True
    p.write_text(cur.rstrip() + "\n" + css_chunk + "\n", encoding="utf-8")
    print(f"[OK] {css_path} compact CSS appended ({len(css_chunk)} bytes)")
    return True


if __name__ == "__main__":
    print("=" * 60)
    print("rewrite footer(方案 D)")
    print("=" * 60)

    for t in TARGETS:
        replace_footer(t)

    append_css(ROOT / "site" / "assets" / "site.css", APPEND_CSS)

    print("=" * 60)
    print("done")
