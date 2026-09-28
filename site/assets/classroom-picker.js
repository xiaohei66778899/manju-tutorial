(function () {
  'use strict';

  var dialog = document.getElementById('classroomPicker');
  var openBtn = document.getElementById('openClassroomPicker');
  if (!dialog || !openBtn) return;

  var els = {
    close: document.getElementById('pickerClose'),
    fullscreen: document.getElementById('pickerFullscreen'),
    min: document.getElementById('pickerMin'),
    max: document.getElementById('pickerMax'),
    quantity: document.getElementById('pickerQuantity'),
    exclusions: document.getElementById('pickerExclusions'),
    unique: document.getElementById('pickerUnique'),
    sound: document.getElementById('pickerSound'),
    draw: document.getElementById('pickerDraw'),
    reset: document.getElementById('pickerReset'),
    demo: document.getElementById('pickerDemo'),
    number: document.getElementById('pickerNumber'),
    ball: document.getElementById('pickerBall'),
    status: document.getElementById('pickerStatus'),
    results: document.getElementById('pickerResults'),
    stage: document.querySelector('.picker-stage'),
    history: document.getElementById('pickerHistoryList'),
    aid: document.getElementById('pickerAid'),
    challenge: document.getElementById('pickerChallenge'),
    card: document.getElementById('pickerCardResult'),
    confetti: document.getElementById('pickerConfetti')
  };

  var STORAGE_KEY = 'yuge:classroom-picker:v1';
  var shell = dialog.querySelector('.picker-shell');
  var drawn = [];
  var rolling = false;
  var audioContext = null;
  var aidCards = [
    '🤝 搭档卡：邀请一位同学共同回答',
    '💡 提示一下：老师提供一个关键词',
    '✂️ 50:50：排除两个错误选项',
    '🙋 全班投票：请全班一起给出判断',
    '🌱 问题降级：换一道更基础的小问题',
    '⚡ 勇气加倍：挑战进阶题，成功获得双倍星星'
  ];
  var challengeCards = [
    '🎙 用播音腔读一句课堂内容',
    '🐾 模仿一种动物 5 秒钟',
    '😄 给大家分享一个冷笑话',
    '🧠 用三个关键词总结刚才的知识点',
    '🎭 用一个动作表达本题答案',
    '👩‍🏫 当 30 秒小老师，复述一个知识点',
    '🎤 用广告配音的方式说出答案',
    '🤝 邀请一位同学组成救援队',
    '🛡 幸运豁免：本次安全过关',
    '🌟 幸运星：把回答机会转交给下一位同学'
  ];

  function clamp(n, min, max) { return Math.min(max, Math.max(min, n)); }

  function secureIndex(length) {
    if (length <= 1) return 0;
    if (!window.crypto || !window.crypto.getRandomValues) return Math.floor(Math.random() * length);
    var maxUint = 0x100000000;
    var limit = maxUint - (maxUint % length);
    var box = new Uint32Array(1);
    do { window.crypto.getRandomValues(box); } while (box[0] >= limit);
    return box[0] % length;
  }

  function parseExclusions(text) {
    var out = [];
    String(text || '').replace(/[，、；;\s]+/g, ',').split(',').forEach(function (part) {
      var p = part.trim();
      if (!p) return;
      var range = p.match(/^(\d+)\s*[-~至]\s*(\d+)$/);
      if (range) {
        var a = Number(range[1]);
        var b = Number(range[2]);
        var start = Math.min(a, b);
        var end = Math.max(a, b);
        for (var i = start; i <= end && i - start < 500; i++) out.push(i);
      } else if (/^\d+$/.test(p)) out.push(Number(p));
    });
    return out.filter(function (n, i, arr) { return arr.indexOf(n) === i; });
  }

  function settings() {
    var min = clamp(parseInt(els.min.value, 10) || 1, 1, 9999);
    var max = clamp(parseInt(els.max.value, 10) || 30, min, 9999);
    var quantity = clamp(parseInt(els.quantity.value, 10) || 1, 1, 20);
    els.min.value = min;
    els.max.value = max;
    els.quantity.value = quantity;
    return { min: min, max: max, quantity: quantity, excluded: parseExclusions(els.exclusions.value), unique: els.unique.checked, sound: els.sound.value };
  }

  function makePool(cfg) {
    var blocked = {};
    cfg.excluded.forEach(function (n) { blocked[n] = true; });
    if (cfg.unique) drawn.forEach(function (n) { blocked[n] = true; });
    var pool = [];
    for (var n = cfg.min; n <= cfg.max; n++) if (!blocked[n]) pool.push(n);
    return pool;
  }

  function save() {
    var cfg = settings();
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify({ min: cfg.min, max: cfg.max, quantity: cfg.quantity, exclusions: els.exclusions.value, unique: cfg.unique, sound: cfg.sound, drawn: drawn.slice(-100) }));
    } catch (e) {}
  }

  function load() {
    try {
      var data = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
      if (data.min) els.min.value = data.min;
      if (data.max) els.max.value = data.max;
      if (data.quantity) els.quantity.value = data.quantity;
      if (typeof data.exclusions === 'string') els.exclusions.value = data.exclusions;
      if (typeof data.unique === 'boolean') els.unique.checked = data.unique;
      if (typeof data.sound === 'string') els.sound.value = data.sound;
      else if (typeof data.sound === 'boolean') els.sound.value = data.sound ? 'light' : 'off';
      if (Array.isArray(data.drawn)) drawn = data.drawn.filter(function (n) { return Number.isInteger(n); });
    } catch (e) {}
  }

  function renderHistory() {
    els.history.innerHTML = '';
    if (!drawn.length) {
      var empty = document.createElement('span');
      empty.className = 'picker-history-empty';
      empty.textContent = '还没有抽取记录';
      els.history.appendChild(empty);
      return;
    }
    drawn.slice().reverse().forEach(function (n) {
      var tag = document.createElement('span');
      tag.textContent = n;
      els.history.appendChild(tag);
    });
  }

  function renderResults(list) {
    els.results.innerHTML = '';
    els.results.classList.toggle('is-multi', list.length > 1);
    els.stage.classList.toggle('is-multi-result', list.length > 1);
    els.results.style.setProperty('--winner-count', Math.min(list.length, 5));
    list.forEach(function (n, index) {
      var tag = document.createElement('span');
      if (list.length > 1) {
        var number = document.createElement('strong');
        var label = document.createElement('small');
        number.textContent = n;
        label.textContent = '第 ' + (index + 1) + ' 位 · ' + n + ' 号';
        tag.appendChild(number);
        tag.appendChild(label);
      } else {
        tag.textContent = n + ' 号';
      }
      els.results.appendChild(tag);
    });
  }

  function tone(freq, delay, duration, volume, type) {
    if (els.sound.value === 'off') return;
    try {
      audioContext = audioContext || new (window.AudioContext || window.webkitAudioContext)();
      var osc = audioContext.createOscillator();
      var gain = audioContext.createGain();
      var start = audioContext.currentTime + (delay || 0);
      osc.type = type || 'sine';
      osc.frequency.value = freq;
      gain.gain.setValueAtTime(Math.max(.001, volume), start);
      gain.gain.exponentialRampToValueAtTime(0.001, start + duration);
      osc.connect(gain); gain.connect(audioContext.destination);
      osc.start(start); osc.stop(start + duration);
    } catch (e) {}
  }

  function playTick() {
    var mode = els.sound.value;
    if (mode === 'off') return;
    if (mode === 'hype') tone(160 + secureIndex(90), 0, .035, .018, 'sawtooth');
    else if (mode === 'game') tone(420 + secureIndex(240), 0, .035, .018, 'square');
    else tone(430 + secureIndex(120), 0, .028, .012, 'sine');
  }

  function playWinnerSound() {
    var mode = els.sound.value;
    if (mode === 'off') return;
    if (mode === 'hype') {
      /* 明亮大调庆典旋律：上升号角 + 柔和和弦收尾，热烈但不刺耳 */
      [392,523,659,784,1047].forEach(function (f, i) { tone(f, i * .11, .24, .045, 'triangle'); });
      [523,659,784].forEach(function (f) { tone(f, .53, .58, .035, 'sine'); });
      tone(262, 0, .2, .028, 'sine');
      tone(392, .22, .22, .028, 'sine');
      tone(523, .53, .58, .026, 'triangle');
    } else if (mode === 'game') {
      [523,659,784,1047].forEach(function (f, i) { tone(f, i * .105, .22, .045, 'square'); });
      tone(523, .46, .42, .04, 'triangle');
      tone(784, .46, .42, .035, 'triangle');
    } else {
      tone(660, 0, .14, .045, 'sine');
      tone(880, .11, .24, .04, 'sine');
    }
  }

  function playLowAlert() { tone(190, 0, .18, .035, 'triangle'); }

  function celebrate() {
    var colors = ['#635BFF', '#F47C3C', '#FBBF24', '#10B981', '#EC4899'];
    els.confetti.innerHTML = '';
    for (var i = 0; i < 34; i++) {
      var bit = document.createElement('i');
      bit.style.left = (5 + secureIndex(91)) + '%';
      bit.style.background = colors[secureIndex(colors.length)];
      bit.style.animationDelay = (secureIndex(250) / 1000) + 's';
      bit.style.setProperty('--drift', (secureIndex(181) - 90) + 'px');
      els.confetti.appendChild(bit);
    }
    window.setTimeout(function () { els.confetti.innerHTML = ''; }, 1800);
  }

  function pickMany(pool, amount) {
    var copy = pool.slice();
    var winners = [];
    for (var i = 0; i < amount && copy.length; i++) {
      var idx = secureIndex(copy.length);
      winners.push(copy[idx]);
      copy.splice(idx, 1);
    }
    return winners;
  }

  function draw() {
    if (rolling) return;
    var cfg = settings();
    var pool = makePool(cfg);
    if (!pool.length) {
      els.status.textContent = '本轮号码已经抽完，请点击“重新开始本轮”';
      playLowAlert();
      return;
    }
    var amount = Math.min(cfg.quantity, pool.length);
    var winners = pickMany(pool, amount);
    rolling = true;
    els.draw.disabled = true;
    els.card.textContent = '';
    els.results.innerHTML = '';
    els.results.classList.remove('is-multi');
    els.stage.classList.remove('is-multi-result');
    els.status.textContent = '正在公平摇号…';
    els.ball.classList.remove('is-winner');
    els.ball.classList.add('is-rolling');
    var started = Date.now();
    var ticker = window.setInterval(function () {
      els.number.textContent = pool[secureIndex(pool.length)];
      playTick();
      if (Date.now() - started > 1350) {
        window.clearInterval(ticker);
        window.setTimeout(function () {
          els.number.textContent = winners[0];
          els.ball.classList.remove('is-rolling');
          void els.ball.offsetWidth;
          els.ball.classList.add('is-winner');
          if (cfg.unique) drawn = drawn.concat(winners);
          else drawn.push.apply(drawn, winners);
          renderResults(winners);
          renderHistory();
          var remaining = makePool(settings()).length;
          els.status.textContent = winners.length === 1 ? '🎉 今天的幸运同学：' + winners[0] + ' 号 · 剩余 ' + remaining + ' 人' : '🎉 本次抽中 ' + winners.length + ' 人 · 剩余 ' + remaining + ' 人';
          playWinnerSound();
          celebrate();
          rolling = false;
          els.draw.disabled = false;
          save();
        }, 260);
      }
    }, 62);
  }

  function showCard(type) {
    var source = type === 'aid' ? aidCards : challengeCards;
    var title = type === 'aid' ? '求助卡' : '趣味挑战';
    els.card.innerHTML = '<strong>' + title + '</strong><br>' + source[secureIndex(source.length)];
    tone(type === 'aid' ? 540 : 720, 0, .15, .035, 'sine');
    tone(type === 'aid' ? 680 : 900, .09, .2, .03, 'sine');
  }

  function resetRound() {
    drawn = [];
    renderHistory();
    renderResults([]);
    els.number.textContent = '?';
    els.card.textContent = '';
    els.status.textContent = '本轮已重置，准备开始';
    save();
  }

  function openDialog() {
    if (typeof dialog.showModal === 'function') dialog.showModal();
    else dialog.setAttribute('open', '');
    settings();
    renderHistory();
    els.draw.focus();
  }

  function closeDialog() {
    dialog.classList.remove('is-app-fullscreen');
    if (document.fullscreenElement) document.exitFullscreen().catch(function () {});
    if (typeof dialog.close === 'function') dialog.close();
    else dialog.removeAttribute('open');
  }

  function toggleFullscreen() {
    if (document.fullscreenElement) {
      document.exitFullscreen && document.exitFullscreen();
      return;
    }
    if (dialog.classList.contains('is-app-fullscreen')) {
      dialog.classList.remove('is-app-fullscreen');
      syncFullscreenButton();
      return;
    }
    if (shell && shell.requestFullscreen) {
      shell.requestFullscreen().catch(function () {
        dialog.classList.add('is-app-fullscreen');
        syncFullscreenButton();
      });
    } else {
      dialog.classList.add('is-app-fullscreen');
      syncFullscreenButton();
    }
  }

  function syncFullscreenButton() {
    var active = !!document.fullscreenElement || dialog.classList.contains('is-app-fullscreen');
    els.fullscreen.textContent = active ? '↙' : '⛶';
    els.fullscreen.title = active ? '退出全屏' : '全屏投影';
    els.fullscreen.setAttribute('aria-label', active ? '退出全屏' : '全屏投影');
  }

  load();
  renderHistory();
  openBtn.addEventListener('click', openDialog);
  els.close.addEventListener('click', closeDialog);
  els.fullscreen.addEventListener('click', toggleFullscreen);
  document.addEventListener('fullscreenchange', syncFullscreenButton);
  els.draw.addEventListener('click', draw);
  els.reset.addEventListener('click', resetRound);
  els.demo.addEventListener('click', function () { els.min.value = 1; els.max.value = 30; els.quantity.value = 1; els.exclusions.value = ''; els.unique.checked = true; resetRound(); });
  els.aid.addEventListener('click', function () { showCard('aid'); });
  els.challenge.addEventListener('click', function () { showCard('challenge'); });
  [els.min, els.max, els.quantity, els.exclusions, els.unique, els.sound].forEach(function (el) { el.addEventListener('change', save); });
  dialog.addEventListener('click', function (e) { if (e.target === dialog) closeDialog(); });
  document.addEventListener('keydown', function (e) {
    if (!dialog.open) return;
    var tag = document.activeElement && document.activeElement.tagName;
    if (e.code === 'Space' && tag !== 'INPUT' && tag !== 'SELECT' && tag !== 'TEXTAREA') { e.preventDefault(); draw(); }
  });
})();
