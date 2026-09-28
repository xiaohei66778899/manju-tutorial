/* ============================================================
 * 玉哥风格共享增强 · 自动注入到所有页面
 * 加载:在 </body> 之前加 <script src="../assets/site-enhance.js" defer></script>
 *
 * 自动注入:
 * 1. 顶部阅读进度条(全站统一 ComfyUI/千川/工具箱同款)
 * 2. 主题切换按钮(🌙/☀️)
 * 3. Logo 升级为玉哥风格(渐变方块 + 文字 + v3 副标题)
 * 4. 主题 localStorage 记忆 + 初始主题应用
 *
 * 设计原则:不破坏页面原有结构,只在 body 注入装饰元素
 * ============================================================ */
(function () {
  'use strict';

  // 工具函数
  function $(sel, root) { return (root || document).querySelector(sel); }
  function $$(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }
  function has(sel) { return !!document.querySelector(sel); }

  // 1. 顶部阅读进度条(全站统一)
  function injectProgressBar() {
    if (has('.read-progress')) return;
    var bar = document.createElement('div');
    bar.className = 'read-progress';
    bar.innerHTML = '<div class="bar"></div>';
    document.body.insertBefore(bar, document.body.firstChild);

    var fill = bar.querySelector('.bar');
    function update() {
      var doc = document.documentElement;
      var h = doc.scrollHeight - doc.clientHeight;
      var pct = h > 0 ? Math.min(100, Math.max(0, (doc.scrollTop / h) * 100)) : 0;
      fill.style.width = pct + '%';
    }
    window.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', update);
    update();
  }

  // 2. 主题切换(同时设 data-theme 属性 + html.dark 类)
  function applyTheme(t) {
    document.documentElement.setAttribute('data-theme', t);
    document.documentElement.classList.toggle('dark', t === 'dark');
    try { localStorage.setItem('yuge:theme', t); } catch (e) {}
    var btn = document.getElementById('yugeThemeBtn');
    if (btn) btn.textContent = t === 'dark' ? '☀️' : '🌙';
  }

  // 3. 主题切换按钮(顶栏右侧)
  function injectThemeToggle() {
    var existing = $('.theme-toggle');
    if (existing) {
      // 仅接管明确使用共享主题 ID 的按钮；其他页面可能已有独立监听器。
      if (existing.id === 'yugeThemeBtn' && existing.getAttribute('data-theme-bound') !== '1') {
        existing.setAttribute('data-theme-bound', '1');
        existing.addEventListener('click', function () {
          var cur = document.documentElement.getAttribute('data-theme') || 'light';
          applyTheme(cur === 'light' ? 'dark' : 'light');
        });
      }
      return;
    }
    var topbar = $('.topbar');
    if (!topbar) return;
    var btn = document.createElement('button');
    btn.className = 'theme-toggle';
    btn.id = 'yugeThemeBtn';
    btn.title = '深浅主题切换';
    btn.textContent = '🌙';
    btn.setAttribute('aria-label', '切换深浅主题');
    btn.setAttribute('data-theme-bound', '1');
    topbar.appendChild(btn);
    btn.addEventListener('click', function () {
      var cur = document.documentElement.getAttribute('data-theme') || 'light';
      applyTheme(cur === 'light' ? 'dark' : 'light');
    });
  }

  // 4. Logo 升级为玉哥风格(替换 .logo 旧版)
  function upgradeLogo() {
    var logo = $('.topbar .logo');
    if (!logo || logo.classList.contains('site-logo')) return;
    var text = logo.textContent.trim();
    // 提取站点名(去掉 emoji)
    var m = text.match(/^(\S+)\s+(.*)$/);
    var rawName = m ? m[2] : text;
    var siteName = rawName.replace(/\s*v\d+(?:\.\d+)?\s*·\s*玉哥\s*$/, '').trim();
    var versionMatch = text.match(/v(\d+)/);
    var version = versionMatch ? versionMatch[0] : 'v3';
    logo.outerHTML =
      '<div class="site-logo">' +
        '<div class="logo-mark">🎬</div>' +
        '<div class="logo-text">' + siteName + ' <small>' + version + ' · 玉哥</small></div>' +
      '</div>';
  }

  // 5. 导航栏 active 自动高亮(根据 URL)
  function autoActiveNav() {
    var links = $$('header.topbar nav a');
    if (!links.length) return;

    // 先清掉旧的 active(避免 HTML 写死的 active + JS 添加并存 → 双高亮)
    links.forEach(function(a) { a.classList.remove('active'); });

    var path = window.location.pathname.replace(/\?.*$/, '').replace(/\/index\.html$/, '/');
    try { path = decodeURIComponent(path); } catch (e) {}

    // 把链接 href 解析成完整路径(从当前页面出发)
    function resolveTarget(href) {
      href = href.split('?')[0];
      if (href.startsWith('http')) return '';
      // 当前页所在目录
      var curDir = path.replace(/\/$/, '').replace(/\/[^\/]+$/, '');
      var parts = href.split('/');
      var resolved = curDir;
      for (var i = 0; i < parts.length; i++) {
        var p = parts[i];
        if (p === '..') {
          resolved = resolved.replace(/\/[^\/]+$/, '');
        } else if (p !== '.' && p !== '') {
          resolved += '/' + p;
        }
      }
      // 去掉末尾的 index.html(让目录链接代表整个目录)
      if (resolved.endsWith('/index.html')) {
        resolved = resolved.slice(0, -'/index.html'.length);
      }
      return resolved;
    }

    var matched = false;
    var bestLink = null;
    var bestScore = -1;

    links.forEach(function(a) {
      var href = a.getAttribute('href') || '';
      var target = resolveTarget(href);
      if (!target) return;

      var score = 0;
      // 完全匹配:path 等于 target(精确)
      if (path === target || path + '/' === target + '/' || path === target + '/') {
        score = 1000;
      }
      // 子路径匹配:path 以 target + '/' 开头(子目录或子页面)
      else if (target && path.indexOf(target + '/') === 0) {
        score = target.length;  // 越长的目录前缀越精确
      }
      // 根目录特殊:target = '' 表示任意路径
      else if (target === '' && path === '/') {
        score = 100;
      }

      // 只有 score > 0 且严格大于当前 bestScore 才更新
      if (score > 0 && score > bestScore) {
        bestLink = a;
        bestScore = score;
        matched = true;
      }
    });

    // 剧本 SPA 属于“漫剧教程”，但文件位于 site 根目录，需显式归类。
    if (/\/剧本\.html$/.test(path)) {
      bestLink = Array.prototype.find.call(links, function(a) {
        return (a.getAttribute('href') || '').indexOf('tutorial/all-courses.html') >= 0;
      });
      matched = !!bestLink;
    }

    if (matched && bestLink) {
      bestLink.classList.add('active');
    }
  }

  // 6. 统一搜索框 placeholder
  function unifySearch() {
    var input = $('.topbar .search input');
    if (input && (!input.getAttribute('placeholder') || input.placeholder.indexOf('🔍') === -1)) {
      input.setAttribute('placeholder', '🔍 搜教程 / 工具 / Prompt…');
    }
  }

  // 7. 主入口
  function init() {
    upgradeLogo();
    injectProgressBar();
    injectThemeToggle();
    autoActiveNav();
    unifySearch();
    var saved = null;
    try { saved = localStorage.getItem('yuge:theme'); } catch (e) {}
    applyTheme(saved || 'light');
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
