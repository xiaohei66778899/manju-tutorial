/* ============================================================
   导航栏 active 自动高亮 + 主题切换 + 搜索框 placeholder 统一
   - 根据 pathname 自动匹配 header nav a 的 href,加 class="active"
   - 给所有 .theme-toggle 绑 toggle 事件
   - 统一搜索框 placeholder
   ============================================================ */

(function() {
  'use strict';

  // 1. 导航 active 自动匹配
  function autoActive() {
    // 取当前路径(去掉 query string)
    var path = window.location.pathname.replace(/\?.*$/, '');
    // 例如:/site/tutorial/A-manju-basic/A-1.html
    var links = document.querySelectorAll('header.topbar nav a');
    if (!links.length) return;

    // 匹配规则:链接 href 的 basename 必须出现在 path 里
    // 例如 href="../index.html"  → basename "index.html"
    // 但 ../index.html 在 tutorial 子目录下,实际指向 /site/index.html
    // 我们看链接的"目标文件名",而不是 href 字面
    var matched = false;
    var bestLink = null;
    var bestLen = -1;

    links.forEach(function(a) {
      var href = a.getAttribute('href') || '';
      // 提取最后一段文件名(去掉 ../ 等)
      var basename = href.replace(/^[\.\/]+/, '').split('?')[0];
      // 也匹配纯路径形式
      if (basename === 'index.html' && path.match(/[\/]index\.html$/)) {
        // 首页 / 漫剧教程等都是 index.html,但要看是不是同目录
        // 简单办法:看 basename 是不是 'index.html' 且 path 也以 'index.html' 结尾
        // 但要排除掉其他 index.html:用更精确的目录匹配
      }
      // 检查 href 是否出现在 path 末尾
      if (path.endsWith('/' + basename) || path.endsWith(basename)) {
        // 优先选最长的 basename(更精确)
        if (basename.length > bestLen) {
          bestLink = a;
          bestLen = basename.length;
          matched = true;
        }
      }
    });

    // 特殊规则:路径包含 /tutorial/ 时,active 漫剧教程
    if (!matched && path.indexOf('/tutorial/') > -1) {
      links.forEach(function(a) {
        var href = a.getAttribute('href') || '';
        if (href.indexOf('tutorial/all-courses.html') > -1 || href === 'tutorial/all-courses.html') {
          a.classList.add('active');
        }
      });
      matched = true;
    }

    if (matched && bestLink) {
      bestLink.classList.add('active');
    }
  }

  // 2. 主题切换
  function bindTheme() {
    var btn = document.querySelector('.theme-toggle');
    if (!btn) return;
    // 读取 localStorage
    var saved = localStorage.getItem('yuge-theme');
    if (saved === 'dark') {
      document.documentElement.setAttribute('data-theme', 'dark');
      btn.textContent = '☀️';
    }
    btn.addEventListener('click', function() {
      var isDark = document.documentElement.getAttribute('data-theme') === 'dark';
      if (isDark) {
        document.documentElement.removeAttribute('data-theme');
        btn.textContent = '🌙';
        localStorage.setItem('yuge-theme', 'light');
      } else {
        document.documentElement.setAttribute('data-theme', 'dark');
        btn.textContent = '☀️';
        localStorage.setItem('yuge-theme', 'dark');
      }
    });
  }

  // 3. 统一搜索框 placeholder
  function unifyPlaceholder() {
    var input = document.querySelector('header.topbar .search input');
    if (input) {
      input.setAttribute('placeholder', '🔍 搜教程 / 工具 / Prompt…');
    }
  }

  // 执行
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      autoActive();
      bindTheme();
      unifyPlaceholder();
    });
  } else {
    autoActive();
    bindTheme();
    unifyPlaceholder();
  }
})();