/* ============================================================
   漫剧制作教程站 · 教程页 JS
   - 左侧目录自动展开当前节
   - 右侧 TOC 自动从 <main> 的 H2 生成
   - 滚动时高亮当前章节
   ============================================================ */

// 9 大类目录数据(玉哥 PLAN.md 150 节) - v0.1 已写 24 节
// entry 字段:大类入口路径,用 {WEB_ROOT} 占位符表示 web 根(JS 自动反推)
// 这样无论部署到哪个路径,都能正确跳转
const SIDEBAR = [
  {
    code: 'A',
    title: '漫剧基础',
    entry: '{WEB_ROOT}tutorial/A-manju-basic/A-1.html',
    pages: [
      { id: 'A-1',  title: 'A-1 漫剧是啥' },
      { id: 'A-2',  title: 'A-2 漫剧和短剧区别' },
      { id: 'A-3',  title: 'A-3 一集怎么做出来' },
      { id: 'A-4',  title: 'A-4 必备工具清单' },
      { id: 'A-5',  title: 'A-5 一个人能不能做' },
      { id: 'A-6',  title: 'A-6 本地 vs 在线工具' },
      { id: 'A-7',  title: 'A-7 第一个练习项目' },
      { id: 'A-8',  title: 'A-8 漫剧基础测验' },
    ]
  },
  {
    code: 'B',
    label: 'B · 剧本专题',
    emoji: '📜',
    // B 是独立 SPA(在根目录),归到专题区 — 渲染时按字母序排在专题段第二位
    topic: true,
    entry: '{WEB_ROOT}剧本.html#view-1-1',
    pages: [
      { id: 'B-1', title: 'B-1 选题库',         external: true, href: '{WEB_ROOT}剧本.html#view-1-1' },
      { id: 'B-2', title: 'B-2 AI 辅助原创',    external: true, href: '{WEB_ROOT}剧本.html#view-1-2' },
      { id: 'B-3', title: 'B-3 爽点模板',       external: true, href: '{WEB_ROOT}剧本.html#view-1-3' },
      { id: 'B-4', title: 'B-4 改稿方法',       external: true, href: '{WEB_ROOT}剧本.html#view-1-4' },
      { id: 'B-5', title: 'B-5 怎么找授权',     external: true, href: '{WEB_ROOT}剧本.html#view-2-1' },
      { id: 'B-6', title: 'B-6 合同怎么看',     external: true, href: '{WEB_ROOT}剧本.html#view-2-2' },
      { id: 'B-7', title: 'B-7 改编流程',       external: true, href: '{WEB_ROOT}剧本.html#view-2-3' },
      { id: 'B-8', title: 'B-8 相似度检查',     external: true, href: '{WEB_ROOT}剧本.html#view-2-4' },
    ]
  },
  {
    code: 'C',
    title: '角色制作',
    entry: '{WEB_ROOT}tutorial/C-character/C-1.html',
    pages: [
      { id: 'C-1',  title: 'C-1 角色制作简介' },
      { id: 'C-2',  title: 'C-2 怎样选画风' },
      { id: 'C-3',  title: 'C-3 怎样设计角色外形' },
      { id: 'C-4',  title: 'C-4 FaceID 锁脸' },
      { id: 'C-5',  title: 'C-5 固定发型年龄' },
      { id: 'C-6',  title: 'C-6 固定服装配饰' },
      { id: 'C-7',  title: 'C-7 制作正面图' },
      { id: 'C-8',  title: 'C-8 侧面三视图' },
      { id: 'C-9',  title: 'C-9 制作表情图' },
      { id: 'C-10', title: 'C-10 多人角色' },
      { id: 'C-11', title: 'C-11 角色一致性' },
      { id: 'C-12', title: 'C-12 参考图保持一致' },
      { id: 'C-13', title: 'C-13 用 IP-Adapter' },
      { id: 'C-14', title: 'C-14 用 FaceID' },
      { id: 'C-15', title: 'C-15 用角色 LoRA' },
      { id: 'C-16', title: 'C-16 两个角色串脸' },
      { id: 'C-17', title: 'C-17 角色提示词速查' },
    ]
  },
  {
    code: 'D',
    title: '分镜',
    entry: '{WEB_ROOT}tutorial/D-storyboard/D-1.html',
    pages: [
      { id: 'D-1',  title: 'D-1 分镜简介' },
      { id: 'D-2',  title: 'D-2 剧本拆场' },
      { id: 'D-3',  title: 'D-3 场拆镜头' },
      { id: 'D-4',  title: 'D-4 景别 4 种' },
      { id: 'D-5',  title: 'D-5 镜头角度' },
      { id: 'D-6',  title: 'D-6 三角形构图' },
      { id: 'D-7',  title: 'D-7 人物视线' },
      { id: 'D-8',  title: 'D-8 动作设计' },
      { id: 'D-9',  title: 'D-9 镜头运动' },
      { id: 'D-10', title: 'D-10 对话镜头' },
      { id: 'D-11', title: 'D-11 动作镜头' },
      { id: 'D-12', title: 'D-12 首尾帧' },
      { id: 'D-13', title: 'D-13 镜头衔接' },
      { id: 'D-14', title: 'D-14 填写分镜表' },
      { id: 'D-15', title: 'D-15 一集完整实例' },
    ]
  },
  {
    code: 'E',
    title: 'AI 出图',
    entry: '{WEB_ROOT}tutorial/E-ai-image/E-1.html',
    pages: [
      { id: 'E-1',  title: 'E-1 AI 出图简介' },
      { id: 'E-16', title: 'E-16 SD WebUI' },
      { id: 'E-17', title: 'E-17 Midjourney' },
      { id: 'E-18', title: 'E-18 即梦(字节)' },
      { id: 'E-19', title: 'E-19 Flux 模型' },
      { id: 'E-20', title: 'E-20 提示词 5 原则' },
      { id: 'E-21', title: 'E-21 负面提示词' },
      { id: 'E-22', title: 'E-22 风格词速查' },
      { id: 'E-23', title: 'E-23 镜头词速查' },
      
      { id: 'E-25', title: 'E-25 工具选择决策树' },
      { id: 'E-26', title: 'E-26 LoRA 训练' },
      { id: 'E-27', title: 'E-27 LoRA 调用' },
      { id: 'E-28', title: 'E-28 批量出图' },
      { id: 'E-29', title: 'E-29 保存图片' },
      { id: 'E-30', title: 'E-30 Manager 装节点' },
      
      { id: 'E-32', title: 'E-32 工作流模板 4 套' },
      { id: 'E-33', title: 'E-33 出图质量检查' },
      { id: 'E-34', title: 'E-34 提示词 100 词库' },
      { id: 'E-35', title: 'E-35 节点参考手册' },
    ]
  },
  {
    code: 'F',
    title: 'AI 视频',
    entry: '{WEB_ROOT}tutorial/F-ai-video/F-1.html',
    pages: [
      { id: 'F-1',  title: 'F-1 图生视频简介' },
      { id: 'F-2',  title: 'F-2 文生 vs 图生' },
      { id: 'F-3',  title: 'F-3 首帧生成视频' },
      { id: 'F-4',  title: 'F-4 首尾帧视频' },
      { id: 'F-5',  title: 'F-5 动作提示词' },
      { id: 'F-6',  title: 'F-6 运镜提示词(眼神跟镜头)' },
      { id: 'F-8',  title: 'F-8 Wan 2.x' },
      { id: 'F-9',  title: 'F-9 HunyuanVideo' },
      { id: 'F-10', title: 'F-10 LTX-Video' },
      { id: 'F-11', title: 'F-11 4 模型横评' },
      { id: 'F-12', title: 'F-12 人物变形避坑' },
      { id: 'F-13', title: 'F-13 角色漂移' },
      { id: 'F-14', title: 'F-14 背景闪烁' },
      { id: 'F-15', title: 'F-15 延长视频' },
      { id: 'F-16', title: 'F-16 镜头转场' },
      { id: 'F-17', title: 'F-17 插帧 24→60fps' },
      { id: 'F-18', title: 'F-18 视频放大 4K' },
      { id: 'F-19', title: 'F-19 17 大失败模式' },
    ]
  },
  {
    code: 'G',
    title: '配音剪辑',
    entry: '{WEB_ROOT}tutorial/G-audio-edit/G-1.html',
    pages: [
      { id: 'G-1',  title: 'G-1 后期制作简介' },
      { id: 'G-2',  title: 'G-2 选角色声音' },
      { id: 'G-3',  title: 'G-3 AI 配音 4 工具' },
      { id: 'G-4',  title: 'G-4 多角色配音' },
      { id: 'G-5',  title: 'G-5 情绪语速' },
      { id: 'G-6',  title: 'G-6 旁白独白' },
      { id: 'G-7',  title: 'G-7 口型同步 Sync.so' },
      { id: 'G-8',  title: 'G-8 环境声音效' },
      { id: 'G-9',  title: 'G-9 背景音乐 BGM' },
      { id: 'G-10', title: 'G-10 自动字幕' },
      { id: 'G-11', title: 'G-11 字幕校对' },
      { id: 'G-12', title: 'G-12 剪映基础' },
      { id: 'G-13', title: 'G-13 15 种转场' },
      { id: 'G-14', title: 'G-14 节奏卡点' },
      { id: 'G-15', title: 'G-15 调色滤镜' },
      { id: 'G-16', title: 'G-16 封面 3 工具' },
      { id: 'G-17', title: 'G-17 导出设置' },
      { id: 'G-18', title: 'G-18 一集完整实例' },
    ]
  },
  {
    code: 'H',
    title: '发布运营',
    entry: '{WEB_ROOT}tutorial/H-publish/H-1.html',
    pages: [
      { id: 'H-1',  title: 'H-1 发布前检查' },
      { id: 'H-2',  title: 'H-2 视频尺寸 9:16' },
      { id: 'H-3',  title: 'H-3 标题 5 模板' },
      { id: 'H-4',  title: 'H-4 简介 3 模板' },
      { id: 'H-5',  title: 'H-5 封面爆款公式' },
      { id: 'H-6',  title: 'H-6 4 平台对比' },
      { id: 'H-7',  title: 'H-7 发布排期' },
      { id: 'H-8',  title: 'H-8 7 维数据' },
      { id: 'H-9',  title: 'H-9 复盘数据表' },
      { id: 'H-10', title: 'H-10 下一集迭代' },
    ]
  },
  {
    code: 'I',
    title: '附录速查',
    entry: '{WEB_ROOT}tutorial/I-appendix/I-1.html',
    pages: [
      { id: 'I-1',  title: 'I-1 术语速查' },
      { id: 'I-2',  title: 'I-2 景别运镜速查' },
      { id: 'I-3',  title: 'I-3 节点速查' },
      { id: 'I-4',  title: 'I-4 模型速查' },
      { id: 'I-5',  title: 'I-5 视频规格速查' },
      { id: 'I-6',  title: 'I-6 平台规格速查' },
      { id: 'I-7',  title: 'I-7 工具网址大全' },
      { id: 'I-8',  title: 'I-8 错误关键词' },
      { id: 'I-9',  title: 'I-9 开源仓库入口' },
    ]
  },
  {
    code: 'J', label: 'J · ComfyUI 专题', emoji: '🧩',
    topic: true,
    entry: '{WEB_ROOT}tutorial/J-comfyui/ComfyUI漫剧工作流.html',
    pages: [
      { id: 'J-comfyui', title: 'J ComfyUI 教程', external: true, href: '{WEB_ROOT}tutorial/J-comfyui/ComfyUI漫剧工作流.html' },
    ]
  },
  {
    code: 'K', label: 'K · 千川投流 SOP · 玉哥 v9.0', emoji: '🎯',
    topic: true,
    entry: '{WEB_ROOT}tutorial/K-投流/千川投流SOP.html',
    pages: [
      { id: 'K-qianchuan', title: 'K 千川投流 SOP v9.0', external: true, href: '{WEB_ROOT}tutorial/K-投流/千川投流SOP.html' },
    ]
  },
  {
    code: 'L', label: 'L · 短剧 AI 仓库 · 玉哥 v18 汇总', emoji: '📦',
    topic: true,
    entry: '{WEB_ROOT}tutorial/L-airepo/短剧AI仓库.html',
    pages: [
      { id: 'L-airepo', title: 'L 短剧 AI 仓库汇总', external: true, href: '{WEB_ROOT}tutorial/L-airepo/短剧AI仓库.html' },
    ]
  },
  {
    code: 'M', label: 'M · Seedance / 即梦 实操课', emoji: '🎬',
    topic: true,
    entry: '{WEB_ROOT}tutorial/M-seedance/Seedance即梦实操课.html',
    pages: [
      { id: 'M-seedance', title: 'M Seedance / 即梦 实操课 · 9 章 + 110 视频', external: true, href: '{WEB_ROOT}tutorial/M-seedance/Seedance即梦实操课.html' },
    ]
  },
  {
    code: 'N', label: 'N · AI 写小说实战课', emoji: '📖',
    topic: true,
    entry: '{WEB_ROOT}tutorial/N-aixiexiaoshuo/AI写小说实战课.html',
    pages: [
      { id: 'N-aixiexiaoshuo', title: 'N AI 写小说实战课 · 15 章 + 10 GitHub', external: true, href: '{WEB_ROOT}tutorial/N-aixiexiaoshuo/AI写小说实战课.html' },
    ]
  },
];

// 已完成节标记(v1.1 全 149 节 2026-09-16)
const DONE_PAGES = new Set([
  // A 节 8 节
  'A-1','A-2','A-3','A-4','A-5','A-6','A-7','A-8',
  // B 节 17 节

  // C 节 17 节
  'C-1','C-2','C-3','C-4','C-5','C-6','C-7','C-8','C-9','C-10','C-11','C-12','C-13','C-14','C-15','C-16','C-17',
  // D 节 15 节
  'D-1','D-2','D-3','D-4','D-5','D-6','D-7','D-8','D-9','D-10','D-11','D-12','D-13','D-14','D-15',
  // E 节 21 节(E-2 ~ E-15 纯 ComfyUI 已删除,玉哥指示移至 J 大类)
  'E-1','E-16','E-17','E-18','E-19','E-20','E-21','E-22','E-23','E-25','E-26','E-27','E-28','E-29','E-30','E-32','E-33','E-34','E-35',
  // F 节 19 节
  'F-1','F-2','F-3','F-4','F-5','F-6','F-8','F-9','F-10','F-11','F-12','F-13','F-14','F-15','F-16','F-17','F-18','F-19',
  // G 节 18 节
  'G-1','G-2','G-3','G-4','G-5','G-6','G-7','G-8','G-9','G-10','G-11','G-12','G-13','G-14','G-15','G-16','G-17','G-18',
  // H 节 10 节
  'H-1','H-2','H-3','H-4','H-5','H-6','H-7','H-8','H-9','H-10',
  // I 节 9 节
  'I-1','I-2','I-3','I-4','I-5','I-6','I-7','I-8','I-9',
  // J 节 1 节(ComfyUI 原版 SPA,外链标记)
  'J-comfyui',
]);

function getCurrentPageId() {
  // 从 URL 取文件名,如 A-1.html
  const path = window.location.pathname;
  const match = path.match(/([A-I])-(\d+)\.html/);
  if (match) return `${match[1]}-${match[2]}`;
  return null;
}

function getCategoryDir(pageId) {
  if (!pageId) return null;
  return `${pageId.charAt(0)}-manju-basic`;  // 默认映射,实际类别可扩展
}

// 计算当前页到 site/tutorial/all-courses.html 的相对路径
function getTutorialIndexPath() {
  const parts = window.location.pathname.split('/').filter(p => p);
  const siteIdx = parts.indexOf('site');
  const tutorialIdx = parts.indexOf('tutorial');

  // 情况 1:在 tutorial/ 下,兼容本地 /site/ 前缀和线上根目录部署
  if (tutorialIdx !== -1) {
    const afterTutorial = parts.slice(tutorialIdx + 1);
    if (afterTutorial.length === 1 && ['index.html', 'all-courses.html'].includes(afterTutorial[0])) {
      return '';
    }
    const isDirectory = window.location.pathname.endsWith('/');
    const upLevels = Math.max(0, afterTutorial.length - (isDirectory ? 0 : 1));
    return '../'.repeat(upLevels) + 'all-courses.html';
  }

  // 情况 2:在 site/ 下但不在 tutorial/ 下(如 site/index.html / site/changelog.html)
  if (siteIdx !== -1) {
    const afterSite = parts.slice(siteIdx + 1);
    if (afterSite.length === 1) {
      return 'tutorial/all-courses.html'; // site/index.html → 进 tutorial/
    }
    const upLevels = afterSite.length - 1 + 1; // +1 出 site/
    return '../'.repeat(upLevels) + 'tutorial/all-courses.html';
  }

  // 情况 3:部署根目录下的页面(如 /index.html、/剧本.html)
  return 'tutorial/all-courses.html';
}

// 反推 web 根路径 — 从当前页面引用的 tutorial.js 路径反推
// 例:tutorial.js 路径 = "/site/assets/tutorial.js?v=..." → web 根 = "/site"
// 例:部署后 tutorial.js 路径 = "/ai-manju/assets/tutorial.js?v=..." → web 根 = "/ai-manju"
// 这样无论部署到哪,sidebar 链接都能正确跳转
function getWebRoot() {
  const scripts = document.querySelectorAll('script[src*="tutorial.js"]');
  for (const s of scripts) {
    try {
      const url = new URL(s.src, window.location.href);
      const m = url.pathname.match(/^(.*?)\/assets\/tutorial\.js/);
      if (m) {
        let root = m[1] || '';
        if (root !== '' && !root.endsWith('/')) root += '/';
        return root;
      }
    } catch (e) { /* ignore */ }
  }
  return ''; // 兜底:空字符串表示 web 根
}

// 替换 entry / href 里的 {WEB_ROOT} 占位符
function resolvePath(template) {
  if (!template) return '';
  const root = getWebRoot();
  return template.replace(/\{WEB_ROOT\}/g, root);
}

function renderSidebar() {
  const sidebar = document.getElementById('sidebar-left');
  if (!sidebar) return;

  const currentId = getCurrentPageId();
  const currentGroup = currentId ? currentId.charAt(0) : null;

  let html = `
    <div class="filter">
      <span style="color: var(--muted);">🔍</span>
      <input type="search" placeholder="过滤章节…" id="sidebar-filter" oninput="filterSidebar(this.value)">
    </div>
  `;

  // 第一段:普通教程(非 topic),按 SIDEBAR 原顺序
  // 第二段:专题(topic: true),放最底部,按 code 字母序排列
  const normalGroups = SIDEBAR.filter(g => !g.topic);
  const topicGroups = SIDEBAR
    .filter(g => g.topic)
    .slice()
    .sort((a, b) => ((a.code || a.id) || '').localeCompare((b.code || b.id) || ''));

  // 工具:渲染单个 group(普通/专题共用)
  const renderGroup = (group, isTopic) => {
    const groupCode = group.code || group.id;
    const groupLabel = group.title || group.label || (group.code || group.id);
    const entry = resolvePath(group.entry);

    // 当前大类默认展开,其他(包括 all-courses 这种没 ID 的页面)默认折叠
    const isCurrentGroup = currentGroup === groupCode;
    const groupOpenCls = isCurrentGroup ? '' : ' collapsed';

    let out = `<div class="sidebar-cat${isTopic ? ' is-topic' : ''}" data-code="${groupCode}">`;
    out += `<button type="button" class="cat-toggle${groupOpenCls}" data-code="${groupCode}" aria-label="折叠/展开">▸</button>`;
    out += `<button type="button" class="sidebar-cat-title${groupOpenCls}" data-code="${groupCode}">`;
    // 专题类显示 emoji
    const emojiPrefix = (isTopic && group.emoji) ? `${group.emoji} ` : '';
    out += `${emojiPrefix}${groupCode} · ${groupLabel.split(' · ')[1] || groupLabel}`;
    out += `</button>`;

    if (group.pages && group.pages.length > 0) {
      out += `<ul class="sidebar-pages${groupOpenCls}">`;
      group.pages.forEach(page => {
        let pageHref;
        if (page.href) {
          pageHref = resolvePath(page.href);
        } else {
          pageHref = resolvePath('{WEB_ROOT}tutorial/' + groupCodeToDirPath(groupCode) + '/' + page.id + '.html');
        }
        const isCurrentPage = (currentId === page.id);
        const pageCls = isCurrentPage ? ' class="current"' : '';
        out += `<li><a href="${pageHref}"${pageCls} data-page="${page.id}">${page.title}</a></li>`;
      });
      out += `</ul>`;
    }
    out += `</div>`;
    return out;
  };

  // 渲染普通教程段
  normalGroups.forEach(group => {
    html += renderGroup(group, false);
  });

  // 渲染专题段(如有)
  if (topicGroups.length > 0) {
    html += `<div class="sidebar-divider"><span>🔖 独立专题</span></div>`;
    topicGroups.forEach(group => {
      html += renderGroup(group, true);
    });
  }

  sidebar.innerHTML = html;

  // 折叠 / 展开交互:点箭头 OR 标题都触发(accordion 模式 — 同时只展开一个)
  // 标题不再跳转(子页面第一个就是 entry)
  sidebar.querySelectorAll('.cat-toggle, .sidebar-cat-title').forEach(el => {
    el.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      const cat = el.closest('.sidebar-cat');
      if (!cat) return;

      // 收起所有其他大类(accordion 互斥)
      sidebar.querySelectorAll('.sidebar-cat').forEach(otherCat => {
        if (otherCat !== cat) {
          otherCat.querySelector('.sidebar-pages')?.classList.add('collapsed');
          otherCat.querySelector('.sidebar-cat-title')?.classList.add('collapsed');
          otherCat.querySelector('.cat-toggle')?.classList.add('collapsed');
        }
      });

      // toggle 当前大类
      const ul = cat.querySelector('.sidebar-pages');
      const titleEl = cat.querySelector('.sidebar-cat-title');
      const btnEl = cat.querySelector('.cat-toggle');
      if (ul) ul.classList.toggle('collapsed');
      if (titleEl) titleEl.classList.toggle('collapsed');
      if (btnEl) btnEl.classList.toggle('collapsed');
    });
  });

  // 默认聚焦搜索框
  const filterInput = document.getElementById('sidebar-filter');
  if (filterInput && !filterInput.value) {
    filterInput.focus();
  }
}

// 从大类字母反推目录名(J/K/L 是专题目录,字母可能不同)
function groupCodeToDirPath(code) {
  const map = {
    A: 'A-manju-basic',
    B: 'B-novel-to-script',  // 实际 B 是根目录 SPA,但兼容 fallback
    C: 'C-character',
    D: 'D-storyboard',
    E: 'E-ai-image',
    F: 'F-ai-video',
    G: 'G-audio-edit',
    H: 'H-publish',
    I: 'I-appendix',
    J: 'J-comfyui',
    K: 'K-投流',
    L: 'L-airepo',
  };
  return map[code] || 'A-manju-basic';
}

// 切换侧栏分组的展开/折叠
function toggleGroup(titleEl) {
  if (!titleEl || !titleEl.nextElementSibling) return;
  const ul = titleEl.nextElementSibling;
  // 同步 ul.collapsed 和 group-title.collapsed(箭头方向)
  const willCollapse = !ul.classList.contains('collapsed');
  ul.classList.toggle('collapsed');
  titleEl.classList.toggle('collapsed');
}

function groupCodeToDir(code) {
  const map = {
    A: 'manju-basic',
    B: 'novel-to-script',
    C: 'character',
    D: 'storyboard',
    E: 'ai-image',
    F: 'ai-video',
    G: 'audio-edit',
    H: 'publish',
    I: 'appendix',
  };
  return map[code] || 'manju-basic';
}

function filterSidebar(q) {
  q = q.trim().toLowerCase();
  const sidebar = document.getElementById('sidebar-left');
  if (!sidebar) return;
  // 空查询:恢复所有分组 + 所有子页面
  if (q === '') {
    sidebar.querySelectorAll('.sidebar-cat').forEach(cat => {
      cat.style.display = '';
    });
    sidebar.querySelectorAll('.sidebar-pages li').forEach(li => {
      li.style.display = '';
    });
    return;
  }
  // 有查询:大类+子页面任意命中即显示,自动展开命中分组
  sidebar.querySelectorAll('.sidebar-cat').forEach(cat => {
    const catText = cat.textContent.toLowerCase();
    const hit = catText.includes(q);
    let anyPageHit = false;
    const pageLiList = cat.querySelectorAll('.sidebar-pages li');
    pageLiList.forEach(li => {
      const liText = li.textContent.toLowerCase();
      const liHit = liText.includes(q);
      li.style.display = liHit ? '' : 'none';
      if (liHit) anyPageHit = true;
    });
    // 大类自身或任一子页面命中 → 显示 + 展开
    cat.style.display = (hit || anyPageHit) ? '' : 'none';
    if (hit || anyPageHit) {
      const ul = cat.querySelector('.sidebar-pages');
      const titleEl = cat.querySelector('.sidebar-cat-title');
      const btnEl = cat.querySelector('.cat-toggle');
      if (ul) ul.classList.remove('collapsed');
      if (titleEl) titleEl.classList.remove('collapsed');
      if (btnEl) btnEl.classList.remove('collapsed');
    }
  });
}

function renderTOC() {
  const aside = document.getElementById('sidebar-right');
  if (!aside) return;

  const main = document.querySelector('.content');
  if (!main) return;

  const h2s = main.querySelectorAll('h2');
  if (h2s.length === 0) {
    aside.style.display = 'none';
    return;
  }

  let html = `<div class="toc-title">本文内容</div><ul>`;
  h2s.forEach(h => {
    const id = h.id || ('sec-' + Math.random().toString(36).slice(2, 8));
    h.id = id;
    // 提取纯文本(去掉 # 号)
    const text = h.textContent.replace(/^#+\s*/, '').trim();
    html += `<li><a href="#${id}">${text}</a></li>`;
  });
  html += `</ul><a href="#" class="back-top">↑ 返回顶部</a>`;
  aside.innerHTML = html;

  // 滚动监听:高亮当前章节
  const tocLinks = aside.querySelectorAll('a[href^="#sec-"]');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        tocLinks.forEach(l => l.classList.remove('current'));
        const link = aside.querySelector(`a[href="#${entry.target.id}"]`);
        if (link) link.classList.add('current');
      }
    });
  }, {
    rootMargin: '-80px 0px -70% 0px',
    threshold: 0
  });
  h2s.forEach(h => observer.observe(h));
}

document.addEventListener('DOMContentLoaded', () => {
  renderSidebar();
  renderTOC();
  setupMobileMenu();
});

// 手机端菜单按钮 + 抽屉切换
function setupMobileMenu() {
  const topbar = document.querySelector('.topbar') || document.querySelector('header');
  const sidebar = document.getElementById('sidebar-left');
  if (!topbar || !sidebar) return;

  // 注入按钮(只手机端 CSS 可见)
  let btn = topbar.querySelector('.menu-toggle');
  if (!btn) {
    btn = document.createElement('button');
    btn.className = 'menu-toggle';
    btn.type = 'button';
    btn.setAttribute('aria-label', '打开目录');
    btn.textContent = '☰';
    topbar.insertBefore(btn, topbar.firstChild);
  }

  btn.addEventListener('click', () => {
    const isOpen = sidebar.classList.toggle('is-open');
    document.body.classList.toggle('sidebar-open', isOpen);
  });

  // 点击主区域自动关闭抽屉
  document.querySelector('.tut-main, .content, main')?.addEventListener('click', () => {
    if (sidebar.classList.contains('is-open')) {
      sidebar.classList.remove('is-open');
      document.body.classList.remove('sidebar-open');
    }
  });

  // ESC 关闭
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && sidebar.classList.contains('is-open')) {
      sidebar.classList.remove('is-open');
      document.body.classList.remove('sidebar-open');
    }
  });
}


