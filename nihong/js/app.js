/* ============================================================
   N2 道場 — 应用逻辑
   视图路由 · 练习引擎 · 闪卡 · 模拟考 · 进度统计 · 倒计时 · TTS
   ============================================================ */
(function () {
  'use strict';
  var D = window.N2DATA;

  /* ---------------- 进度镜像 + 服务端同步 ---------------- */
  // 内存镜像为唯一读写源（进度已在服务端落库）；theme 另留一条 localStorage 快照供启动前上色。
  var KEY = { theme: 'n2.theme', target: 'n2.target', log: 'n2.log', done: 'n2.done', known: 'n2.known', rate: 'n2.rate', blind: 'n2.blind' };
  var _mem = {};
  function apiPost(p, b) {
    try { fetch(p, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(b), keepalive: true })
      .catch(function (e) { console.warn('[sync] 写失败', p, e); }); } catch (e) { console.warn('[sync]', e); }
  }
  function apiDel(p) {
    try { fetch(p, { method: 'DELETE', keepalive: true })
      .catch(function (e) { console.warn('[sync] 清空失败', p, e); }); } catch (e) { console.warn('[sync]', e); }
  }
  function cacheTheme(t) { try { localStorage.setItem(KEY.theme, JSON.stringify(t)); } catch (e) {} }
  // 「认识」一词：镜像 + 服务端（known 只小批量，逐词上报）
  function setKnown(w, on) {
    var a = LS.get(KEY.known, []);
    var ix = a.indexOf(w);
    if (on && ix === -1) a.push(w);
    if (!on && ix !== -1) a.splice(ix, 1);
    LS.set(KEY.known, a);
    apiPost('/api/known', { word: w, known: !!on });
    return a;
  }
  function clearKnown() { apiDel('/api/reset/known'); LS.set(KEY.known, []); }
  var LS = {
    get: function (k, d) { return (k in _mem) ? _mem[k] : d; },
    set: function (k, v) {
      _mem[k] = v;
      // log/done/known 只写镜像，落库由各自入口（logRes/toggleTask/setKnown/重置按钮）负责；
      // 四项设置镜像即上报（theme 另写本地快照供首屏防闪）。
      if (k === KEY.theme) { cacheTheme(v); apiPost('/api/settings', { key: 'theme', value: JSON.stringify(v) }); }
      else if (k === KEY.target) apiPost('/api/settings', { key: 'target', value: JSON.stringify(v) });
      else if (k === KEY.rate) apiPost('/api/settings', { key: 'rate', value: JSON.stringify(v) });
      else if (k === KEY.blind) apiPost('/api/settings', { key: 'blind', value: JSON.stringify(v) });
    },
    // 用 /api/state 的结果预置镜像（迁移后也会重新 fetch state 再 hydrate）
    _hydrate: function (st) {
      var s = st.settings || {};
      _mem[KEY.log] = st.log || [];
      _mem[KEY.done] = st.done || [];
      _mem[KEY.known] = st.known || [];
      if ('theme' in s) { _mem[KEY.theme] = s.theme; cacheTheme(s.theme); }
      if ('target' in s) _mem[KEY.target] = s.target;
      if ('rate' in s) _mem[KEY.rate] = s.rate;
      if ('blind' in s) _mem[KEY.blind] = s.blind;
    }
  };
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; });
  }
  function shuffle(a) {
    a = a.slice();
    for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; }
    return a;
  }
  function sample(arr, n) { return shuffle(arr).slice(0, Math.min(n, arr.length)); }

  /* ---------------- 统计 ---------------- */
  var CAT = {
    kanji: { cn: '汉字读音', jp: '漢字読み' }, ortho: { cn: '表记选字', jp: '表記' },
    context: { cn: '语境选词', jp: '文脈規定' }, paraph: { cn: '近义替换', jp: '言い換え' },
    usage: { cn: '用法判断', jp: '用法' }, grammar: { cn: '语法形式', jp: '文法形式' },
    arrange: { cn: '句子组合', jp: '文の組み立て' }, passage: { cn: '篇章语法', jp: '文章の文法' },
    reading: { cn: '阅读', jp: '読解' }, listening: { cn: '听力', jp: '聴解' }
  };
  function logRes(cat, ok) {
    apiPost('/api/attempts', { cat: cat, ok: !!ok });   // 逐条上报，绝不整条 log 上传
    var a = LS.get(KEY.log, []);
    a.push({ c: cat, ok: ok, t: Date.now() });
    if (a.length > 4000) a = a.slice(-3000);
    LS.set(KEY.log, a);
  }
  function statsAll() {
    var m = {};
    LS.get(KEY.log, []).forEach(function (e) {
      m[e.c] = m[e.c] || { t: 0, ok: 0 };
      m[e.c].t++; if (e.ok) m[e.c].ok++;
    });
    return m;
  }

  /* ---------------- 主题 / 语音 ---------------- */
  function applyTheme() {
    var t = LS.get(KEY.theme, '');
    document.documentElement.setAttribute('data-theme', t);
    $('#themeBtn').textContent = t === 'dark' ? '☀️' : t === 'light' ? '🌙' : '🌓';
  }
  function pickVoice() {
    if (!('speechSynthesis' in window)) return null;
    var vs = speechSynthesis.getVoices();
    return vs.filter(function (v) { return /ja/i.test(v.lang); })[0] || null;
  }
  function speak(text, rate) {
    if (!('speechSynthesis' in window)) { alert('浏览器不支持语音合成 speechSynthesis。'); return; }
    var u = new SpeechSynthesisUtterance(text);
    u.lang = 'ja-JP';
    var v = pickVoice(); if (v) u.voice = v;
    u.rate = rate || LS.get(KEY.rate, 0.9);
    speechSynthesis.cancel();
    speechSynthesis.speak(u);
  }
  function stopSpeak() { if ('speechSynthesis' in window) speechSynthesis.cancel(); }

  /* ---------------- 倒计时 ---------------- */
  function targetDate() {
    var s = LS.get(KEY.target, D.exam.target).split('-');
    return new Date(+s[0], +s[1] - 1, +s[2]);
  }
  function daysLeft() {
    var n = new Date(); n.setHours(0, 0, 0, 0);
    var t = targetDate(); t.setHours(0, 0, 0, 0);
    return Math.max(0, Math.round((t - n) / 86400000));
  }
  function updateCd() {
    var chip = $('#cdChip');
    if (chip) chip.innerHTML = '🗓 <span class="cd-label">距考试</span> <b>' + daysLeft() + '</b> 天';
  }

  /* ---------------- 题目归一化 ---------------- */
  // 统一题：{stem, options[], correct, exp, cat, audio?}
  function kanjiItems(n) {
    return sample(D.vocab.kanjiPool, n).map(function (it) {
      var others = shuffle(D.vocab.kanjiPool.filter(function (o) { return o.y !== it.y; }));
      var opts = [it.y];
      for (var i = 0; i < others.length && opts.length < 4; i++) if (opts.indexOf(others[i].y) === -1) opts.push(others[i].y);
      opts = shuffle(opts);
      return {
        cat: 'kanji',
        stem: '<div class="center"><span style="font-family:var(--sans-jp);font-size:48px;font-weight:700">' + esc(it.w) + '</span></div>' +
          '<p class="center faint">次の漢字の読み方として最もよいものを選びなさい。／ 请选出该汉字的正确读音。</p>',
        options: opts, correct: opts.indexOf(it.y),
        exp: '正解：<b>' + esc(it.y) + '</b>（' + esc(it.m) + '）'
      };
    });
  }
  function fromPool(cat, pool, pre) {
    return pool.map(function (it) {
      var options = shuffle(it.opts);
      var ans = it.opts[it.a];
      return {
        cat: cat,
        stem: (pre ? pre(it) : '') + '<p class="qstem">' + it.q + '</p>',
        options: options, correct: options.indexOf(ans),
        exp: it.cn + (it.jp ? '<div class="ja faint">' + it.jp + '</div>' : '')
      };
    });
  }
  function arrangeItems(pool) {
    return pool.map(function (a) {
      var starNo = a.order[a.starPos];
      var star = a.parts.filter(function (p) { return p.no === starNo; })[0];
      var seqLabels = a.order.map(function (no, i) {
        var p = a.parts.filter(function (x) { return x.no === no; })[0];
        return (i === a.starPos) ? '<span class="abx star">★</span>' : '<span class="abx">（&nbsp;' + (i + 1) + '&nbsp;）</span>';
      }).join(' ');
      var opts = a.parts.map(function (p) { return p.no + '．' + p.t; });
      var correct = opts.indexOf(star.no + '．' + star.t);
      var orderCn = a.order.map(function (no, i) {
        var p = a.parts.filter(function (x) { return x.no === no; })[0];
        return p.t;
      }).join(' → ');
      return {
        cat: 'arrange',
        stem: '<p class="qstem"><b>请排出正确顺序，并选出放在 ★ 处的语块编号。／ 並べ替えて ★ に入る語を選びなさい。</b></p>' +
          '<div class="arrange-row"><span class="head">' + esc(a.head) + '</span> ' + seqLabels + '</div>' +
          '<div class="arrange-words">' + a.parts.map(function (p) { return '<span class="aw">' + p.no + '．' + esc(p.t) + '</span>'; }).join(' ') + '</div>',
        options: opts, correct: correct,
        exp: '<b>正确语序：</b>' + orderCn + '<br><b>完整句：</b>' + esc(a.full) + '<div class="faint">' + a.cn + '</div>'
      };
    });
  }

  /* ---------------- 通用练习会话 ---------------- */
  function runQuiz(host, items, onExit) {
    var i = 0, correct = 0, answered = 0;
    host.innerHTML = '';
    function finish() {
      var acc = answered ? Math.round(correct / answered * 100) : 0;
      host.innerHTML = '<div class="card center reveal-anim"><h2>练习结束 ／ 終了</h2>' +
        '<div class="stat-grid mt2"><div class="stat"><div class="v">' + correct + ' / ' + answered + '</div><div class="l">答对 正解数</div></div>' +
        '<div class="stat"><div class="v">' + acc + '%</div><div class="l">正确率 正答率</div></div></div>' +
        '<p class="faint mt2">' + (answered < items.length ? '中途退出：' + (items.length - answered) + ' 题未作答。／ 途中でやめました。' : '本次题目共 ' + items.length + ' 题。') + '</p>' +
        '<div class="row center mt2" style="justify-content:center">' +
        '<button class="btn indigo" id="qRetry">↻ 再练一轮 もう一度</button>' +
        '<button class="btn" id="qExit">返回 もどる</button></div></div>';
      $('#qRetry').onclick = function () { runQuiz(host, items, onExit); };
      $('#qExit').onclick = function () { onExit && onExit(); };
    }
    function step() {
      if (i >= items.length) { finish(); return; }
      var it = items[i];
      host.innerHTML = '';
      var card = drawQ(it, i, items.length, function (ok) {
        answered++; if (ok) correct++;
        logRes(it.cat, ok);
        bindNext();
      }, finish);
      host.appendChild(card);
      function bindNext() {
        var b = host.querySelector('#nxt');
        b.onclick = function () { i++; step(); };
      }
    }
    step();
  }
  // 返回一张答题卡；onAnswer(ok)；onSkip 直接结束（退出）
  function drawQ(it, idx, total, onAnswer, onQuit) {
    var w = document.createElement('div');
    w.className = 'card reveal-anim';
    var cat = CAT[it.cat] || { cn: it.cat, jp: '' };
    var h = '<div class="spread"><span class="pill b">' + esc(cat.cn) + ' <span class="ja faint">' + esc(cat.jp) + '</span></span>' +
      '<span class="faint">' + (idx + 1) + ' / ' + total + '</span></div>' +
      '<div class="bar mt1" style="height:6px"><i style="width:' + Math.round(idx / total * 100) + '%"></i></div>' +
      '<div class="mt2">' + (it.audio ? '<div class="row mb1"><button class="btn sm indigo" data-say="' + esc(it.audio) + '">▶ 播放 再生</button></div>' : '') + it.stem + '</div>' +
      '<div class="opts mt1"></div><div class="ansbox"></div>' +
      '<div class="row mt2" style="justify-content:space-between">' +
      '<button class="btn ghost sm" id="qquit">退出 やめる</button>' +
      '<button class="btn primary hidden" id="nxt">下一题 次へ →</button></div>';
    w.innerHTML = h;
    var optsBox = w.querySelector('.opts');
    var answered = false;
    it.options.forEach(function (txt, j) {
      var b = document.createElement('button');
      b.className = 'opt';
      b.setAttribute('data-j', j);
      b.innerHTML = '<span class="k">' + (j + 1) + '</span><span class="t">' + esc(txt) + '</span>';
      b.onclick = function () {
        if (answered) return;
        answered = true;
        var ok = j === it.correct;
        onAnswer(ok);
        $$('.opt', optsBox).forEach(function (x) {
          var jx = +x.getAttribute('data-j');
          x.classList.add('done');
          if (jx === it.correct) x.classList.add('right');
          else if (x === b) x.classList.add('wrong');
          else x.classList.add('dim');
        });
        w.querySelector('.ansbox').innerHTML =
          '<div class="explain">' + (ok ? '<span class="pill g">✓ 正解</span>' : '<span class="pill r">✗ 不正解　正解は ' + esc(it.options[it.correct]) + '</span>') +
          '<div style="margin-top:6px">' + it.exp + '</div></div>';
        var n = w.querySelector('#nxt');
        n.classList.remove('hidden');
      };
      optsBox.appendChild(b);
    });
    w.querySelector('#qquit').onclick = function () {
      if (confirm('退出本次练习？／ 練習をやめますか？')) onQuit();
    };
    if (it.audio) { var pb = w.querySelector('[data-say]'); if (pb) pb.onclick = function () { speak(it.audio); }; }
    return w;
  }

  /* ---------------- 视图容器 ---------------- */
  var view = $('#view');
  function go(r) { location.hash = r; }
  function render() {
    stopSpeak();
    var h = location.hash.replace(/^#\/?/, '');
    var parts = h.split('/');
    var page = parts[0] || 'home', arg = parts[1] || '';
    setActiveNav(page);
    view.classList.remove('reveal-anim'); void view.offsetWidth; view.classList.add('reveal-anim');
    if (page === 'home') viewHome();
    else if (page === 'exam') viewExam();
    else if (page === 'plan') viewPlan();
    else if (page === 'vocab') viewVocab(arg);
    else if (page === 'grammar') viewGrammar(arg);
    else if (page === 'reading') viewReading(arg);
    else if (page === 'listening') viewListening(arg);
    else if (page === 'mock') viewMock();
    else if (page === 'stats') viewStats();
    else { location.hash = '#/home'; }
  }

  /* ---------------- 导航 ---------------- */
  var NAV = [
    { sec: '备考 ／ 学習', items: [
      { r: 'home', n: '首页', j: 'ホーム', x: '🏠' },
      { r: 'exam', n: '考试介绍', j: '試験の仕組み', x: '📘' },
      { r: 'plan', n: '学习计划', j: '学習プラン', x: '🗓️' }
    ] },
    { sec: '四大模块 ／ 4分野', items: [
      { r: 'vocab', n: '文字·词汇', j: '語彙', x: '🈳' },
      { r: 'grammar', n: '语法', j: '文法', x: '🈴' },
      { r: 'reading', n: '阅读', j: '読解', x: '📖' },
      { r: 'listening', n: '听力', j: '聴解', x: '🎧' }
    ] },
    { sec: '实战 ／ 実戦', items: [
      { r: 'mock', n: '综合模拟考', j: '総合模試', x: '✍️' },
      { r: 'stats', n: '学习报告', j: '学習記録', x: '📊' }
    ] }
  ];
  function buildNav() {
    $('#sideInner').innerHTML = NAV.map(function (g) {
      return '<div class="nav-sec">' + esc(g.sec) + '</div>' + g.items.map(function (it) {
        return '<a class="nav-link" href="#/' + it.r + '" data-r="' + it.r + '"><span class="nx">' + it.x + '</span>' +
          '<span>' + esc(it.n) + '<small class="ja faint" style="display:block;font-size:11px">' + esc(it.j) + '</small></span></a>';
      }).join('');
    }).join('');
  }
  function setActiveNav(page) {
    $$('.nav-link', $('#sideInner')).forEach(function (a) { a.classList.toggle('active', a.getAttribute('data-r') === page); });
    closeDrawer();
  }
  function closeDrawer() { $('#side').classList.remove('open'); $('#scrim').classList.remove('on'); }

  /* ---------------- 首页 ---------------- */
  function viewHome() {
    var st = statsAll();
    var tot = 0, ok = 0;
    Object.keys(st).forEach(function (k) { tot += st[k].t; ok += st[k].ok; });
    var acc = tot ? Math.round(ok / tot * 100) : 0;
    var phase = currentPhase();
    var undone = phase ? undoneTasks(phase) : [];
    var cell = function (v, l) { return '<div class="cd-cell"><div class="v">' + v + '</div><div class="l">' + l + '</div></div>'; };
    var hero = '<section class="hero"><div><h1>日本語能力試験 <span style="letter-spacing:2px">N2</span> 道場</h1>' +
      '<p class="sub">目标 2027年7月 N2 合格 ／ 合格を目指す自習サイトです。</p></div>' +
      '<div class="cd-grid">' +
      cell(daysLeft(), '距考试 残り日数') + cell(tot, '已练 練習数') + cell(acc + '%', '正确率 正答率') +
      cell('90/180', '合格线 合格ライン') +
      '</div></section>';

    var phaseCard = '';
    if (phase) {
      phaseCard = '<div class="card"><h3>📍 当前阶段 ／ 今の時期</h3>' +
        '<p><b>' + esc(phase.titleCN) + '</b> <span class="pill gold">' + esc(phase.spanCN) + '</span> <span class="ja faint">' + esc(phase.titleJP) + '</span></p>' +
        '<p class="small muted">' + phase.goals.map(function (g) { return '🎯 ' + g.cn; }).join('<br>') + '</p>' +
        (undone.length ? '<ul class="plist mt1">' + undone.slice(0, 3).map(function (t) {
          return '<li><span class="checkbox" data-t="' + t.id + '"></span><span>' + esc(t.cn) + '<div class="ja faint">' + esc(t.jp) + '</div></span></li>';
        }).join('') + '</ul><button class="btn sm indigo mt1" id="toPlan">去学习计划 › プランへ</button>' : '<p class="small muted">本阶段任务已全部完成 🎉</p>') + '</div>';
    }
    var weak = weakSections(st);
    var weakCard = weak
      ? '<div class="card"><h3>⚡ 相对薄弱 ／ 強化すべき分野</h3>' + weak.bars + '</div>'
      : '<div class="card"><h3>⚡ 学习报告</h3><p class="muted small">完成足够练习后，这里会标出需要加强的分野。</p>' +
        '<button class="btn sm mt1" data-go="stats">查看报告 ›</button></div>';
    var mods = [
      ['🈳', '文字·词汇', '語彙', '汉字读音 · 语境选词 · 近义 · 用法', 'vocab'],
      ['🈴', '语法', '文法', 'N2 句型体系 + 三类题型', 'grammar'],
      ['📖', '阅读', '読解', '短文 → 中文 → 长文 → 统合 → 检索', 'reading'],
      ['🎧', '听力', '聴解', '五类听解 + 语音朗读', 'listening']
    ].map(function (m) {
      return '<div class="card modcard" data-go="' + m[4] + '"><h3>' + m[0] + ' ' + esc(m[1]) + ' <span class="pill i ja">' + esc(m[2]) + '</span></h3><p class="small muted">' + esc(m[3]) + '</p></div>';
    }).join('');

    view.innerHTML = hero +
      '<div class="grid g2 mt2">' + phaseCard + weakCard + '</div>' +
      '<h2 class="mt2">开始学习 ／ 学習を始める</h2><div class="grid g2 mt1">' + mods + '</div>' +
      '<h2 class="mt2">备考三步走 ／ 学習の流れ</h2><div class="card">' +
      '<div class="step"><div class="no">1</div><div class="bd"><b>看懂考试 出題を知る</b><div class="small muted">「考试介绍」一次看完六大题型、时长与合格规则。</div></div></div>' +
      '<div class="step"><div class="no">2</div><div class="bd"><b>跟着计划学 プランで学ぶ</b><div class="small muted">十个月分阶段：语法→词汇→阅读→听力，最后模拟冲刺。</div></div></div>' +
      '<div class="step"><div class="no">3</div><div class="bd"><b>刷题看报告 演習と記録</b><div class="small muted">练习自动记入「学习报告」，按弱项补强即可。</div></div></div>' +
      '</div>';
    if ($('#toPlan')) $('#toPlan').onclick = function () { go('plan'); };
    bindCheckboxes();
    bindGoCards();
  }
  function weakSections(st) {
    var order = ['kanji', 'grammar', 'reading', 'listening', 'context', 'arrange', 'usage'];
    var rows = [];
    order.forEach(function (k) { if (st[k] && st[k].t >= 3) rows.push({ k: k, ok: st[k].ok, t: st[k].t }); });
    if (rows.length < 2) return null;
    rows.sort(function (a, b) { return (a.ok / a.t) - (b.ok / b.t); });
    return { bars: rows.slice(0, 3).map(function (r) {
      var p = Math.round(r.ok / r.t * 100);
      return '<div class="mt1"><div class="spread"><span>' + esc(CAT[r.k].cn) + ' <span class="ja faint">' + esc(CAT[r.k].jp) + '</span></span><b>' + p + '%</b></div>' +
        '<div class="bar ' + (p >= 60 ? 'g' : '') + '"><i style="width:' + p + '%"></i></div></div>';
    }).join('') };
  }
  function bindCheckboxes() {
    $$('#view .checkbox').forEach(function (c) {
      var id = c.getAttribute('data-t');
      if (!id) return;
      c.onclick = function () { toggleTask(id); c.classList.toggle('on'); };
    });
  }
  function bindGoCards() {
    $$('#view [data-go]').forEach(function (el) {
      el.onclick = function () { go(el.getAttribute('data-go')); };
    });
  }

  /* ---------------- 计划 ---------------- */
  var PLAN_START = new Date(2026, 8, 15);
  var CUM = [2, 8, 14, 20, 26, 32, 40, 44];
  function currentPhase() {
    var wk = Math.max(0, Math.floor((Date.now() - PLAN_START.getTime()) / 604800000));
    var ps = D.plan.phases;
    for (var i = 0; i < CUM.length; i++) if (wk < CUM[i]) return ps[i];
    return ps[ps.length - 1];
  }
  function isDone(id) { return LS.get(KEY.done, []).indexOf(id) !== -1; }
  function toggleTask(id) {
    var a = LS.get(KEY.done, []);
    var ix = a.indexOf(id);
    var adding = ix === -1;
    if (adding) a.push(id); else a.splice(ix, 1);
    LS.set(KEY.done, a);
    apiPost('/api/done', { task: id, done: adding });
  }
  function undoneTasks(p) { return p.tasks.filter(function (t) { return !isDone(t.id); }); }
  var TAGC = { vocab: ['词汇', '語彙'], grammar: ['语法', '文法'], reading: ['阅读', '読解'], listening: ['听力', '聴解'], mock: ['模拟', '模試'], foundation: ['备考', '学習'] };
  function viewPlan() {
    var phaseCards = D.plan.phases.map(function (p) {
      var all = p.tasks;
      var dn = all.filter(function (t) { return isDone(t.id); }).length;
      var pct = all.length ? Math.round(dn / all.length * 100) : 0;
      var cur = currentPhase().id === p.id;
      return '<div class="card mt2"><div class="spread"><div><h3 style="display:inline">' + (cur ? '📍 ' : '') + esc(p.titleCN) +
        ' <span class="ja faint">' + esc(p.titleJP) + '</span></h3> <span class="pill gold">' + esc(p.spanCN) + '</span></div>' +
        '<span class="faint">' + dn + '/' + all.length + '</span></div>' +
        '<div class="bar ' + (pct === 100 ? 'g' : '') + '"><i style="width:' + pct + '%"></i></div>' +
        '<div class="row mt1">' + p.goals.map(function (g) { return '<span class="pill i">🎯 ' + esc(g.cn) + '</span>'; }).join('') + '</div>' +
        '<ul class="plist mt1">' + all.map(function (t) {
          var tg = TAGC[t.tag] || ['', ''];
          return '<li><span class="checkbox' + (isDone(t.id) ? ' on' : '') + '" data-t="' + t.id + '"></span>' +
            '<span><span class="pill" style="font-size:11px">' + tg[0] + '</span> ' + esc(t.cn) +
            '<div class="ja faint">' + esc(t.jp) + '</div></span></li>';
        }).join('') + '</ul></div>';
    }).join('');
    var rhythm = '<div class="card"><h3>⏱ 每周节奏参考 ／ 週間リズム</h3><table class="tbl">' +
      '<tr><th>周一</th><td>语法新句型（15～20条）</td><td class="ja faint">文法</td></tr>' +
      '<tr><th>周二</th><td>词汇背诵 + 汉字读音练习</td><td class="ja faint">語彙</td></tr>' +
      '<tr><th>周三</th><td>阅读限时（短文/长文各1篇）</td><td class="ja faint">読解</td></tr>' +
      '<tr><th>周四</th><td>复习错题 + 词汇闪卡</td><td class="ja faint">復習</td></tr>' +
      '<tr><th>周五</th><td>听力磨耳 30 分钟</td><td class="ja faint">聴解</td></tr>' +
      '<tr><th>周六</th><td>整套模拟 + 复盘</td><td class="ja faint">模試</td></tr>' +
      '<tr><th>周日</th><td>错题整理 · 轻松休息</td><td class="ja faint">休養</td></tr>' +
      '</table></div>';
    view.innerHTML = '<h1>学习计划 ／ 学習プラン</h1>' +
      '<div class="row"><span class="pill gold">距目标考试还有 ' + daysLeft() + ' 天</span>' +
      '<span class="faint">目标：2027年7月（第1回）</span><button class="btn sm" id="setT">修改目标日期</button></div>' +
      '<div class="grid g2 mt2"><div>' + rhythm + '</div><div class="card"><h3>📏 每日 1.5～2 小时怎么分</h3><ul class="plist">' +
      '<li><b>30分</b> 复习昨日内容 復習</li><li><b>40分</b> 新知识（语法/词汇轮流）</li>' +
      '<li><b>30分</b> 阅读或听力专项</li><li><b>20分</b> 错题 + 生词记录</li></ul>' +
      '<p class="faint">通勤等碎片时间可用闪卡巩固词汇。</p></div></div>' +
      '<h2 class="mt2">阶段清单 ／ フェーズ一覧</h2>' + phaseCards +
      '<button class="btn ghost mt2" id="resetP">重置全部进度 リセット</button>';
    $('#setT').onclick = function () {
      var cur = targetDate();
      var s = prompt('目标考试日期（YYYY-MM-DD）／ 目標日を入力', cur.toISOString().slice(0, 10));
      if (s && /^\d{4}-\d{2}-\d{2}$/.test(s)) { LS.set(KEY.target, s); updateCd(); location.hash = '#/plan'; }
    };
    $('#resetP').onclick = function () {
      if (confirm('确定清除学习记录与进度？／ 全データを消去しますか？')) {
        apiDel('/api/reset/done'); apiDel('/api/reset/attempts'); apiDel('/api/reset/known');
        LS.set(KEY.done, []); LS.set(KEY.log, []); LS.set(KEY.known, []);
        location.hash = '#/home';
      }
    };
    bindCheckboxes();
  }

  /* ---------------- 考试介绍 ---------------- */
  function viewExam() {
    var e = D.exam;
    var timing = e.timing.map(function (t) {
      return '<tr><td><b>' + esc(t.secCN) + '</b><div class="ja faint">' + esc(t.secJP) + '</div></td>' +
        '<td class="num">' + esc(t.timeCN) + '<div class="ja faint">' + esc(t.timeJP) + '</div></td>' +
        '<td class="small">' + esc(t.noteCN) + '<div class="ja faint">' + esc(t.noteJP) + '</div></td></tr>';
    }).join('');
    var sections = e.sections.map(function (s) {
      var qs = s.qtypes.map(function (q) {
        return '<div class="card" style="margin-top:10px"><div class="spread">' +
          '<div><b class="ja">' + esc(q.nameJP) + '</b> <span class="pill b" style="font-size:11px">' + esc(q.nameCN) + '</span></div>' +
          '<span class="pill">' + esc(q.approxCN) + '</span></div>' +
          '<p class="small muted mt1">' + esc(q.dCN) + '<span class="ja faint">　' + esc(q.dJP) + '</span></p>' +
          '<p class="small">💡 ' + esc(q.tip) + '</p></div>';
      }).join('');
      return '<div class="pc-sec"><h3>' + esc(s.nameCN) + ' <span class="pill i ja">' + esc(s.nameJP) + '</span></h3>' + qs + '</div>';
    }).join('');
    var strat = e.strategy.map(function (s2) {
      return '<div class="card"><div class="spread"><b>' + esc(s2.c) + ' <span class="ja faint">' + esc(s2.j) + '</span></b><span>' + s2.p + '%</span></div>' +
        '<div class="bar i" style="margin:6px 0"><i style="width:' + s2.p + '%"></i></div>' +
        '<div class="small muted">' + esc(s2.cn) + '<div class="ja faint">' + esc(s2.jp) + '</div></div></div>';
    }).join('');
    view.innerHTML = '<h1>考试介绍 ／ 試験の仕組み</h1>' +
      '<p class="muted">JLPT 每年 7 月与 12 月举行。N2 满分 180，总分合格线 90，且「语言知识」「阅读」「听力」三区分都须≥19。这里一次看清全部题型。</p>' +
      '<div class="grid g2 mt2"><div class="card"><h3>📋 试卷结构 ／ 試験の構成</h3><table class="tbl">' +
      '<thead><tr><th>科目 区分</th><th>时长 時間</th><th>说明</th></tr></thead><tbody>' + timing + '</tbody></table>' +
      '<div class="explain mt2"><b>合格条件 ／ 合格ライン：</b>' + esc(e.score.noteCN) + '<div class="ja faint">' + esc(e.score.noteJP) + '</div></div></div>' +
      '<div><h3>🏅 三大板块配分目安</h3><div class="grid g3">' + strat + '</div>' +
      '<div class="card mt2"><h3>📈 拿分策略</h3><ul class="plist">' +
      '<li>汉字读音・语法形式・即时应答是“性价比”最高的题型，优先刷到高正确率。</li>' +
      '<li>阅读速度靠限时训练；每天读一篇日文文章比周末突击更有效。</li>' +
      '<li>听力用「盲听→对稿→跟读」三步法，别边看边听。</li></ul></div></div></div>' +
      '<h2 class="mt2">逐题拆解 ／ 出題形式の解説</h2>' + sections;
  }

  /* ---------------- 词汇 ---------------- */
  var VOB_TABS = [['reading', '汉字读音', '漢字読み'], ['orthography', '表记选字', '表記'], ['context', '语境选词', '文脈規定'], ['paraphrase', '近义替换', '言い換え類義'], ['usage', '用法判断', '用法'], ['library', '词汇库', '単語リスト']];
  function vocabPoolItems(kind) {
    if (kind === 'reading') return kanjiItems(10);
    if (kind === 'orthography') return fromPool('ortho', D.vocab.orthoPool);
    if (kind === 'context') return fromPool('context', D.vocab.contextPool);
    if (kind === 'usage') return fromPool('usage', D.vocab.usagePool.map(function (u) {
      return { q: '「' + u.w + '」の使い方として最も正しいものを選びなさい。<span class="faint">（哪句用法正确？）</span>', opts: u.opts, a: u.a, cn: u.cn };
    }));
    if (kind === 'paraphrase') return D.vocab.paraphPool.map(function (it) {
      var options = shuffle(it.opts);
      return {
        cat: 'paraph',
        stem: '<p class="qstem">「<b class="ja">' + esc(it.w) + '</b>」の意味に最も近いものを選びなさい。／ 选最接近的词义。</p><p class="muted small">例句 例文：<span class="ja">' + esc(it.sent) + '</span></p>',
        options: options, correct: options.indexOf(it.opts[it.a]),
        exp: it.cn + (it.jp ? '<div class="ja faint">' + it.jp + '</div>' : '')
      };
    });
    return kanjiItems(10);
  }
  var VOB_INTRO = {
    reading: '看汉字选读音。汉字读音是 N2 的拿分重点，每天 10 题保持手感。',
    orthography: '看假名选正确汉字。注意同音异字（下ろす／降ろす／卸す…）。',
    context: '读懂句子选出最合适的词——真题「文脈規定」风格。',
    paraphrase: '选出与指定词含义最接近的词（言い換え類義）。',
    usage: '四个句子中哪一句用法正确？考搭配与使用语境。',
    library: 'N2 全词库检索：按表记／读音／含义搜索、按词性筛选；标记「已认」后从闪卡中排除。'
  };
  function viewVocab(kind) {
    var k = VOB_TABS.some(function (t) { return t[0] === kind; }) ? kind : 'reading';
    var tabs = VOB_TABS.map(function (t) {
      return '<button class="tab' + (t[0] === k ? ' on' : '') + '" data-k="' + t[0] + '">' + t[1] + ' <span class="ja faint">' + t[2] + '</span></button>';
    }).join('');
    view.innerHTML = '<div class="spread"><div><h1>文字·词汇 ／ 文字・語彙</h1><p class="muted">覆盖全部 5 种出题形式的专项练习。／ 出題5形式の対策。</p></div>' +
      '<button class="btn indigo" id="fcBtn">🎴 词表闪卡 Flashcards</button></div>' +
      '<div class="tabs mt2">' + tabs + '</div>' +
      '<div class="card"><p class="muted">' + VOB_INTRO[k] + '</p><div id="vpane"></div></div>' +
      '<h2 class="mt2">高频副词 · 接续词速查（' + D.vocab.refList.length + ' 词）</h2>' +
      '<div class="card"><div style="max-height:380px;overflow:auto">' +
      '<table class="tbl"><thead><tr><th>词</th><th>读音</th><th>含义</th></tr></thead><tbody>' +
      D.vocab.refList.map(function (w) {
        return '<tr><td class="ja"><b>' + esc(w.w) + '</b></td>' + (w.y ? '<td class="ja faint">' + esc(w.y) + '</td>' : '<td></td>') + '<td>' + esc(w.m) + '</td></tr>';
      }).join('') + '</tbody></table></div></div>';
    $$('#view .tab').forEach(function (b) {
      b.onclick = function () { go('vocab/' + b.getAttribute('data-k')); };
    });
    $('#fcBtn').onclick = openFlash;
    if (k === 'library') renderVocabLib(); else runQuiz($('#vpane'), vocabPoolItems(k), function () { go('vocab'); });
  }
  /* ---------------- 词汇库（server 版：全词库检索） ---------------- */
  var VPOS_LIST = ['名', '動', '形', 'ナ形', '副', '接続', '他'];
  function renderVocabLib() {
    var q = '', pos = '', page = 1, pane = $('#vpane');
    function optsHtml() {
      return '<option value="">全部词性 すべて</option>' + VPOS_LIST.map(function (p2) {
        return '<option value="' + p2 + '"' + (p2 === pos ? ' selected' : '') + '>' + p2 + '</option>';
      }).join('');
    }
    function pagerHtml(pg, pages) {
      if (pages <= 1) return '';
      var win = [];
      for (var p = 1; p <= pages; p++) {
        if (p === 1 || p === pages || (p >= pg - 2 && p <= pg + 2)) win.push(p);
        else if (win[win.length - 1] !== '…') win.push('…');
      }
      return '<div class="pager">' + win.map(function (p) {
        return p === '…' ? '<span class="faint pg">…</span>'
          : '<button class="btn sm pg' + (p === pg ? ' cur' : '') + '" data-p="' + p + '">' + p + '</button>';
      }).join('') + '</div>';
    }
    function row(w, known) {
      var on = known.indexOf(w.w) !== -1;
      return '<tr><td class="ja"><b style="font-size:16px">' + esc(w.w) + '</b></td>' +
        '<td class="ja faint">' + esc(w.y || '—') + '</td>' +
        '<td>' + esc(w.m) + '</td>' +
        '<td>' + (w.pos ? '<span class="pos">' + esc(w.pos) + '</span>' : '<span class="faint">·</span>') + '</td>' +
        '<td class="vb-known"><button class="knob' + (on ? ' on' : '') + '" data-w="' + esc(w.w) + '" title="已认 認識済み">✓</button></td></tr>';
    }
    function draw() {
      var known = LS.get(KEY.known, []);
      var all = D.words || [];
      var kw = q.toLowerCase();
      var list = all.filter(function (w) {
        if (pos && w.pos !== pos) return false;
        if (!kw) return true;
        return (w.w + ' ' + w.y + ' ' + w.m + ' ' + (w.pos || '')).toLowerCase().indexOf(kw) !== -1;
      });
      var P = 50, pages = Math.max(1, Math.ceil(list.length / P));
      if (page > pages) page = pages;
      var slice = list.slice((page - 1) * P, page * P);
      pane.innerHTML = '<div class="card">' +
        '<div class="vb-tools">' +
        '<input id="vlibQ" type="search" placeholder="搜索 词／读音／含义… 語彙を検索" value="' + esc(q) + '">' +
        '<select id="vlibPos">' + optsHtml() + '</select>' +
        '<span class="vlib-count faint">全库 <b>' + all.length + '</b> 词 · 命中 ' + list.length + '</span></div>' +
        '<div class="vb-wrap"><table class="tbl"><thead><tr>' +
        '<th style="width:150px">表记 語</th><th style="width:130px">读音 読み</th><th>含义 意味</th>' +
        '<th style="width:70px">词性 品詞</th><th class="vb-known">已认 ✓</th></tr></thead><tbody>' +
        (slice.map(function (w) { return row(w, known); }).join('') || '<tr><td colspan="5" class="faint">没有匹配词条。</td></tr>') +
        '</tbody></table></div>' + pagerHtml(page, pages) + '</div>';
      var iq = $('#vlibQ'), is = $('#vlibPos');
      if (iq) iq.oninput = function () { q = iq.value; page = 1; draw(); };
      if (is) is.onchange = function () { pos = is.value; page = 1; draw(); };
      $$('#vpane .pager .pg[data-p]').forEach(function (b) { b.onclick = function () { page = +b.getAttribute('data-p'); draw(); }; });
      $$('#vpane .knob').forEach(function (b) {
        b.onclick = function () { setKnown(b.getAttribute('data-w'), !b.classList.contains('on')); draw(); };
      });
    }
    draw();
  }
  function openFlash() {
    var known = LS.get(KEY.known, []);
    var deck = shuffle(D.vocab.kanjiPool.filter(function (it) { return known.indexOf(it.w) === -1; }));
    var host = $('#vpane');
    if (deck.length === 0) {
      host.innerHTML = '<div class="center"><p class="muted">词表闪卡已全部掌握 🎉</p>' +
        '<button class="btn sm" id="fcReset">重置已掌握 リセット</button></div>';
      $('#fcReset').onclick = function () { clearKnown(); openFlash(); };
      return;
    }
    var i = 0;
    function done() {
      host.innerHTML = '<div class="center mt2"><h3>🎉 本轮完成！</h3><p class="muted">已掌握 ' + known.length + ' 词。清除「已掌握」即可重新洗牌复习。</p>' +
        '<button class="btn indigo" id="fcAgain">再来一轮 もう一度</button></div>';
      $('#fcAgain').onclick = function () { clearKnown(); openFlash(); };
    }
    function renderCard() {
      if (i >= deck.length) { done(); return; }
      var it = deck[i];
      host.innerHTML = '<div class="fc-wrap mt2"><div class="fc" id="fcCard" style="height:230px">' +
        '<div class="fc-face fc-front"><span class="fc-hint">点击翻面 クリック</span><span class="big">' + esc(it.w) + '</span></div>' +
        '<div class="fc-face fc-back"><span class="yomi">' + esc(it.y) + '</span><span class="mean">' + esc(it.m) + '</span></div></div></div>' +
        '<div class="row mt2" style="justify-content:center">' +
        '<button class="btn" id="fcSkip">不认识 スキップ</button>' +
        '<button class="btn primary" id="fcGot">认识 ✓ 覚えた</button></div>' +
        '<div class="center faint mt1">剩余 残り：' + (deck.length - i) + ' 张</div>';
      $('#fcCard').onclick = function () { this.classList.toggle('flip'); };
      $('#fcSkip').onclick = function () { i++; renderCard(); };
      $('#fcGot').onclick = function () {
        known = setKnown(it.w, true); i++; renderCard();
      };
    }
    renderCard();
  }

  /* ---------------- 语法 ---------------- */
  var GR_TABS = [['browse', '语法参考', '文法リスト'], ['quiz', '语法选择', '文法形式の判断'], ['arrange', '句子组合', '文の組み立て'], ['passage', '篇章语法', '文章の文法']];
  function viewGrammar(kind) {
    var k = GR_TABS.some(function (t) { return t[0] === kind; }) ? kind : 'browse';
    var tabs = GR_TABS.map(function (t) {
      return '<button class="tab' + (t[0] === k ? ' on' : '') + '" data-g="' + t[0] + '">' + t[1] + ' <span class="ja faint">' + t[2] + '</span></button>';
    }).join('');
    view.innerHTML = '<div class="spread"><div><h1>语法 ／ 文法</h1><p class="muted">N2 核心句型参考（' + D.grammar.list.length + ' 条）＋ 三种真题题型。</p></div></div>' +
      '<div class="tabs mt2">' + tabs + '</div><div id="gpane"></div>';
    $$('#view .tab').forEach(function (b) { b.onclick = function () { go('grammar/' + b.getAttribute('data-g')); }; });
    var pane = $('#gpane');
    if (k === 'browse') {
      var groups = [];
      D.grammar.list.forEach(function (g) { if (groups.indexOf(g.group) === -1) groups.push(g.group); });
      pane.innerHTML = '<div class="card"><div class="row">' +
        '<input id="gSearch" placeholder="搜索句型 / 含义… 文型を検索" style="flex:1;min-width:170px;padding:9px 12px;border-radius:10px;border:1px solid var(--line);background:var(--surface);color:var(--ink)">' +
        '<select id="gGroup" style="padding:9px;border-radius:10px;border:1px solid var(--line);background:var(--surface);color:var(--ink)">' +
        '<option value="">全部分组 すべて</option>' + groups.map(function (g) { return '<option value="' + esc(g) + '">' + esc(g) + '</option>'; }).join('') + '</select></div>' +
        '<div class="mt1" id="gList"></div></div>';
      function apply() {
        var q = ($('#gSearch').value || '').trim();
        var g = $('#gGroup').value;
        var list = D.grammar.list.filter(function (x) {
          if (g && x.group !== g) return false;
          return !q || (x.f + x.cn + x.jp + x.conn + x.group).indexOf(q) !== -1;
        });
        $('#gList').innerHTML = list.length ? list.map(grammarCard).join('') : '<p class="muted">没有匹配条目。</p>';
      }
      $('#gSearch').oninput = apply;
      $('#gGroup').onchange = apply;
      apply();
    } else if (k === 'quiz') {
      pane.innerHTML = '<div class="card"><p class="muted">真题「文法形式の判断」风格：选出使句子成立的一项。</p><div id="q2"></div></div>';
      runQuiz($('#q2'), fromPool('grammar', D.grammar.quiz), function () { go('grammar'); });
    } else if (k === 'arrange') {
      pane.innerHTML = '<div class="card"><p class="muted">语块排序题：先排出正确语序，再指出 ★ 处应选哪个编号。／ 語句を並べ替え、★に入るものを選びます。</p><div id="q3"></div></div>';
      runQuiz($('#q3'), arrangeItems(D.grammar.arrange), function () { go('grammar'); });
    } else if (k === 'passage') {
      pane.innerHTML = '<div class="card"><p class="muted">短文里选衔接表达，考语篇逻辑（接续词、指示词、呼应）。</p><div id="q4"></div></div>';
      var items = D.grammar.passage.map(function (p) {
        var options = shuffle(p.opts);
        return {
          cat: 'passage',
          stem: '<div class="passage">' + esc(p.text).replace('＿＿＿', '<u style="text-decoration:none;border-bottom:2px solid var(--accent)">＿＿＿</u>') + '</div>',
          options: options, correct: options.indexOf(p.opts[p.a]),
          exp: p.cn + '<div class="ja faint">' + esc(p.text.replace('＿＿＿', '(' + p.opts[p.a] + ')')) + '</div>'
        };
      });
      runQuiz($('#q4'), items, function () { go('grammar'); });
    }
  }
  function grammarCard(g) {
    var ex = g.ex.map(function (e) {
      return '<div style="padding:6px 2px;border-top:1px dashed var(--line)"><div class="ja">' + esc(e[0]) + '</div><div class="small muted">' + esc(e[1]) + '</div></div>';
    }).join('');
    return '<div class="card gram-block" style="margin-bottom:12px"><div class="spread"><b class="ja" style="font-size:19px">' + esc(g.f) + '</b>' +
      '<span class="pill gold">' + esc(g.group) + '</span></div>' +
      '<p class="mt1">' + esc(g.cn) + '<span class="ja faint">　' + esc(g.jp) + '</span></p>' +
      '<p><span class="pill i">接续 接続</span> <span class="ja">' + esc(g.conn) + '</span></p>' + ex + '</div>';
  }

  /* ---------------- 阅读 ---------------- */
  function viewReading(arg) {
    var sets = D.reading.sets;
    var idx = parseInt(arg, 10);
    if (!(idx >= 0 && idx < sets.length)) {
      var cards = sets.map(function (s, i) {
        return '<div class="card modcard" data-go="reading/' + i + '"><div class="spread"><b class="ja">' + esc(s.typeJP) + '</b>' +
          '<span class="pill b" style="font-size:11px">' + esc(s.typeCN) + '</span></div>' +
          '<h3 class="mt1">' + esc(s.title) + '</h3>' +
          '<p class="faint mt1">' + s.questions.length + ' 问 · 点击开始 →</p></div>';
      }).join('');
      view.innerHTML = '<h1>阅读 ／ 読解</h1>' +
        '<p class="muted">按题型逐类击破：短文 → 中文 → 长文 → 综合 → 主张 → 信息检索。限时参考：短文 5 分钟、长篇 8 分钟以内。</p>' +
        '<div class="grid g2 mt2">' + cards + '</div>';
      bindGoCards();
      return;
    }
    var s = sets[idx];
    var texts = s.texts
      ? s.texts.map(function (t) {
        return '<div class="rtag pill i">' + esc(t.label) + '（' + esc(t.from) + '）</div><div class="passage mt1">' + esc(t.text) + '</div>';
      }).join('<div style="height:12px"></div>')
      : '<div class="passage">' + esc(s.text) + '</div>';
    var qHtml = s.questions.map(function (q, qi) {
      return '<div class="questbox" data-qi="' + qi + '"><p class="rtag">問' + (qi + 1) + '</p>' +
        '<p><b>' + esc(q.q) + '</b></p><div class="opts">' +
        q.opts.map(function (o, oi) {
          return '<button class="opt" data-a="' + oi + '"><span class="k">' + (oi + 1) + '</span><span class="t">' + esc(o) + '</span></button>';
        }).join('') + '</div><div class="rans"></div></div>';
    }).join('');
    view.innerHTML = '<div class="row"><button class="btn ghost sm" id="backR">← 题型列表</button>' +
      '<span class="faint">' + (idx + 1) + ' / ' + sets.length + '</span>' +
      (idx < sets.length - 1 ? '<button class="btn sm indigo" style="margin-left:auto" data-go="reading/' + (idx + 1) + '">下一篇 →</button>' : '') + '</div>' +
      '<div class="card mt2"><div class="spread"><h2>' + esc(s.title) + '</h2><span class="pill b">' + esc(s.typeCN) + '</span></div>' +
      '<p class="faint">' + esc(s.typeJP) + '</p>' + texts + '</div>' +
      '<div class="card mt2"><div class="spread"><h3>回答问题 ／ 問題に答える</h3></div>' + qHtml + '</div>' +
      (idx > 0 ? '<div class="row mt2"><button class="btn ghost" data-go="reading/' + (idx - 1) + '">← 上一篇</button></div>' : '');
    $('#backR').onclick = function () { go('reading'); };
    bindGoCards();
    $$('#view .questbox').forEach(function (box) {
      $$('.opt', box).forEach(function (b) {
        b.onclick = function () {
          if (b.classList.contains('done')) return;
          var qi = +box.getAttribute('data-qi');
          var q = s.questions[qi];
          var chosen = +b.getAttribute('data-a');
          var ok = chosen === q.a;
          logRes('reading', ok);
          $$('.opt', box).forEach(function (x) {
            x.classList.add('done');
            if (+x.getAttribute('data-a') === q.a) x.classList.add('right');
            else if (x === b) x.classList.add('wrong');
            else x.classList.add('dim');
          });
          box.querySelector('.rans').innerHTML =
            '<div class="explain">' + (ok ? '<span class="pill g">✓ 正解</span>' : '<span class="pill r">✗ 不正解</span>') +
            '<div style="margin-top:6px">' + esc(q.cn) + '</div></div>';
        };
      });
    });
  }

  /* ---------------- 听力 ---------------- */
  function rateSelect() {
    return ['0.75', '0.9', '1', '1.15', '1.3'].map(function (r) {
      return '<option value="' + r + '">' + r + '×</option>';
    }).join('');
  }
  function viewListening(arg) {
    var sets = D.listening.sets;
    var idx = parseInt(arg, 10);
    if (!(idx >= 0 && idx < sets.length)) {
      var cards = sets.map(function (s, i) {
        return '<div class="card modcard" data-go="listening/' + i + '"><div class="spread"><b class="ja">' + esc(s.typeJP) + '</b>' +
          '<span class="pill b" style="font-size:11px">' + esc(s.typeCN) + '</span></div>' +
          '<p class="small muted mt1">' + esc(s.tipCN) + '</p><p class="faint mt1">点击开始 →</p></div>';
      }).join('');
      view.innerHTML = '<h1>听力 ／ 聴解</h1>' +
        '<p class="muted">真题只念一遍。推荐练习法：<b>先盲听 → 作答 → 对稿 → 跟读</b>。本站用浏览器日语朗读（TTS）模拟播放。</p>' +
        '<div class="card"><div class="row">' +
        '<label class="small">语速 速度：</label><select id="rateSel">' + rateSelect() + '</select>' +
        '<label class="small" style="margin-left:auto"><input type="checkbox" id="blindChk" ' + (LS.get(KEY.blind, false) ? 'checked' : '') + '> 盲听模式（隐藏文字稿）</label></div></div>' +
        '<div class="grid g2 mt2">' + cards + '</div>';
      bindGoCards();
      var cur = String(LS.get(KEY.rate, 0.9));
      $('#rateSel').value = cur;
      $('#rateSel').onchange = function () { LS.set(KEY.rate, parseFloat(this.value)); };
      $('#blindChk').onchange = function () { LS.set(KEY.blind, this.checked); };
      return;
    }
    var s = sets[idx];
    var blind = LS.get(KEY.blind, false);
    var body = '';
    if (s.items) {
      body = '<p class="muted">听一句，选最自然的应答。／ 短い言葉に自然な返事を選んでください。</p>' +
        s.items.map(function (it, ii) {
          return '<div class="card mt1" data-immi="' + ii + '"><div class="row">' +
            '<button class="btn sm indigo" data-say="' + esc(it.u) + '">▶ 播放 再生</button>' +
            '<button class="btn sm ghost" data-tog="' + ii + '">显示原句 文字を見る</button></div>' +
            '<div class="script hidden mt1" data-line="' + ii + '">' + esc(it.u) + '</div>' +
            '<div class="opts mt1">' + optHtml(it.opts, 'imm' + ii) + '</div><div class="rans"></div></div>';
        }).join('');
    } else {
      // 統合理解第2问复用同一段对话（share 指向上一组 id）
      var lines = s.lines;
      if (!lines && s.share) {
        for (var li = 0; li < sets.length; li++) {
          if (sets[li].id === s.share && sets[li].lines) lines = sets[li].lines;
        }
      }
      var qCard = '<div class="card mt2"><p class="faint">📻 ' + esc(s.scenario) + '</p><p><b>' + esc(s.q.text) + '</b></p>' +
        '<div class="opts">' + optHtml(s.q.opts, 'q' + idx) + '</div><div class="rans"></div></div>';
      if (lines) {
        var lrows = lines.map(function (l) {
          var who = l.sp ? '<b>【' + esc(l.sp) + '】</b>' : '';
          return '<div class="lrow"><span class="playln" data-say="' + esc(l.t) + '">▶</span>' + who + esc(l.t) + '</div>';
        }).join('');
        body = '<div class="card mt2"><div class="row">' +
          '<button class="btn indigo" id="playAll">▶ 播放全文 再生</button>' +
          '<button class="btn" id="toggleScript">' + (blind ? '查看文字稿' : '隐藏文字稿') + '</button></div>' +
          '<div class="script mt2 ' + (blind ? 'hidden' : '') + '" id="scriptBlock">' + lrows + '</div></div>' + qCard;
      } else {
        body = qCard;
      }
    }
    var prev = idx > 0 ? '<button class="btn ghost sm" data-go="listening/' + (idx - 1) + '">← 上一类</button>' : '';
    var next = idx < sets.length - 1 ? '<button class="btn indigo sm" style="margin-left:auto" data-go="listening/' + (idx + 1) + '">下一类 →</button>' : '';
    view.innerHTML = '<div class="row"><button class="btn ghost sm" id="backL">← 返回</button>' + prev + next + '</div>' +
      '<div class="card mt2"><div class="spread"><h2>' + esc(s.typeCN) + ' <span class="ja">' + esc(s.typeJP) + '</span></h2></div>' +
      '<p class="small">💡 ' + esc(s.tipCN) + '</p><p class="ja faint">' + esc(s.tipJP) + '</p></div>' + body;
    $('#backL').onclick = function () { go('listening'); };
    bindGoCards();
    bindSayAll();
    if ($('#playAll')) $('#playAll').onclick = function () {
      speak((lines || []).map(function (l) { return l.t; }).join('。'));
    };
    if ($('#toggleScript')) $('#toggleScript').onclick = function () {
      $('#scriptBlock').classList.toggle('hidden');
    };
    if (s.items) {
      // 原句开关
      $$('#view [data-tog]').forEach(function (b) {
        b.onclick = function () {
          var li = b.getAttribute('data-tog');
          var el = $('#view [data-line="' + li + '"]');
          if (el) el.classList.toggle('hidden');
        };
      });
      // 作答
      s.items.forEach(function (it, ii) {
        $$('#view .opt', $('#view [data-immi="' + ii + '"]')).forEach(function (ob) {
          ob.onclick = function () { gradeOpt(ob, it, function (ok) { logRes('listening', ok); }); };
        });
      });
    } else {
      $$('#view .card:last-child .opt').forEach(function (ob) {
        ob.onclick = function () { gradeOpt(ob, s.q, function (ok) { logRes('listening', ok); }); };
      });
    }
  }
  function optHtml(opts, tag) {
    return opts.map(function (o, i) {
      return '<button class="opt" data-o="' + i + '" data-tag="' + tag + '"><span class="k">' + (i + 1) + '</span><span class="t">' + esc(o) + '</span></button>';
    }).join('');
  }
  function gradeOpt(ob, owner, onLog) {
    if (ob.classList.contains('done')) return;
    var chosen = +ob.getAttribute('data-o');
    var ok = chosen === owner.a;
    if (onLog) onLog(ok);
    var wrap = ob.closest('.card');
    var scope = wrap || ob.parentElement.parentElement;
    $$('.opt', scope).forEach(function (x) {
      x.classList.add('done');
      if (+x.getAttribute('data-o') === owner.a) x.classList.add('right');
      else if (x === ob) x.classList.add('wrong');
      else x.classList.add('dim');
    });
    var exp = owner.cn || owner.exp || '';
    var rans = scope.querySelector('.rans');
    if (rans) rans.innerHTML = '<div class="explain">' + (ok ? '<span class="pill g">✓ 正解</span>' : '<span class="pill r">✗ 不正解　正解は ' + esc(owner.opts[owner.a]) + '</span>') + '<div style="margin-top:6px">' + esc(exp) + '</div></div>';
  }
  function bindSayAll() {
    $$('#view [data-say]').forEach(function (b) {
      b.onclick = function () { speak(b.getAttribute('data-say')); };
    });
  }

  /* ---------------- 模拟考 ---------------- */
  var MPART = [
    { key: 'vocab', nameCN: '文字·词汇', nameJP: '文字・語彙' },
    { key: 'grammar', nameCN: '语法', nameJP: '文法' },
    { key: 'reading', nameCN: '阅读', nameJP: '読解' },
    { key: 'listening', nameCN: '听力', nameJP: '聴解' }
  ];
  function buildMock() {
    var items = [];
    var add = function (it) { items.push(it); };
    var v = function (it) { it.sec = 0; return it; };
    kanjiItems(3).forEach(function (it) { add(v(it)); });
    fromPool('ortho', sample(D.vocab.orthoPool, 2)).forEach(function (it) { add(v(it)); });
    fromPool('context', sample(D.vocab.contextPool, 3)).forEach(function (it) { add(v(it)); });
    sample(D.vocab.paraphPool, 1).forEach(function (p) {
      var opts = shuffle(p.opts);
      add(v({ stem: '<p class="qstem">「<b class="ja">' + esc(p.w) + '</b>」の意味に最も近いものを選びなさい。</p><p class="muted small">例文：<span class="ja">' + esc(p.sent) + '</span></p>', options: opts, correct: opts.indexOf(p.opts[p.a]), exp: p.cn, cat: 'paraph' }));
    });
    sample(D.vocab.usagePool, 2).forEach(function (u) {
      fromPool('usage', [{ q: '「' + u.w + '」の使い方として最も正しいものを選びなさい。<span class="faint">（哪句用法正确？）</span>', opts: u.opts, a: u.a, cn: u.cn }]).forEach(function (it) { add(v(it)); });
    });
    fromPool('grammar', sample(D.grammar.quiz, 5)).forEach(function (it) { it.sec = 1; add(it); });
    var ar = sample(D.grammar.arrange, 1);
    arrangeItems(ar).forEach(function (it) { it.sec = 1; add(it); });
    // 阅读三题（含原文）
    var rd = [{ s: D.reading.sets[0], qi: 0 }, { s: D.reading.sets[2], qi: 0 }, { s: D.reading.sets[6], qi: 1 }];
    rd.forEach(function (rr) {
      var q = rr.s.questions[rr.qi];
      var opts = shuffle(q.opts);
      add({ stem: '<div class="passage">' + esc(rr.s.text) + '</div><p class="mt1"><b>' + esc(q.q) + '</b></p>', options: opts, correct: opts.indexOf(q.opts[q.a]), exp: q.cn, cat: 'reading', sec: 2 });
    });
    // 听力
    var l0 = D.listening.sets[0];
    (function () {
      var opts = shuffle(l0.q.opts);
      add({ audio: l0.lines.map(function (x) { return x.t; }).join('。') + '。', stem: '<p class="faint small">📻 ' + esc(l0.scenario) + '</p><p><b>' + esc(l0.q.text) + '</b></p>', options: opts, correct: opts.indexOf(l0.q.opts[l0.q.a]), exp: l0.q.cn, cat: 'listening', sec: 3 });
    })();
    sample(D.listening.sets[3].items, 2).forEach(function (it) {
      var opts = shuffle(it.opts);
      add({ audio: it.u, stem: '<p class="muted small">▶ 播放后选择最自然的应答。</p>', options: opts, correct: opts.indexOf(it.opts[it.a]), exp: it.cn, cat: 'listening', sec: 3 });
    });
    return shuffle(items);
  }
  function viewMock() {
    var items = buildMock();
    var secCount = [0, 0, 0, 0];
    items.forEach(function (it) { secCount[it.sec]++; });
    var heads = MPART.map(function (p, i) {
      return '<div class="card"><div class="spread"><b>' + esc(p.nameCN) + ' <span class="ja faint">' + esc(p.nameJP) + '</span></b><span class="pill">' + secCount[i] + ' 问</span></div></div>';
    }).join('');
    view.innerHTML = '<div class="spread"><div><h1>综合模拟考 ／ 総合模試</h1>' +
      '<p class="muted">从四大模块随机抽题组成的练习卷。先答完全部再交卷，交卷后自动评分（非真实尺度计分）。</p></div>' +
      '<button class="btn primary" id="mockSubmit">✍️ 交卷 採点</button></div>' +
      '<div class="mt2" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px">' + heads + '</div>' +
      '<div id="mockSheet"></div><div id="mockReport"></div>';
    var sheet = $('#mockSheet');
    var answers = {};
    sheet.innerHTML = items.map(function (it, i) {
      var audio = it.audio ? '<div class="row mb1"><button class="btn sm indigo" data-mplay="' + i + '">▶ 播放 再生</button></div>' : '';
      return '<div class="card mt2" data-mcard="' + i + '"><div class="spread"><span class="pill b">' + esc(MPART[it.sec].nameCN) + '</span>' +
        '<span class="faint">第 ' + (i + 1) + ' 问 ／ ' + items.length + '</span></div>' + audio + '<div class="mt1">' + it.stem + '</div>' +
        '<div class="opts mt1">' + it.options.map(function (o, oi) {
          return '<button class="opt" data-i="' + oi + '"><span class="k">' + (oi + 1) + '</span><span class="t">' + esc(o) + '</span></button>';
        }).join('') + '</div><div class="rans"></div></div>';
    }).join('');
    sheet.addEventListener('click', function (e) {
      var mp = e.target.closest('[data-mplay]');
      if (mp) { speak(items[+mp.getAttribute('data-mplay')].audio); return; }
      var ob = e.target.closest('.opt');
      if (!ob) return;
      var card = ob.closest('[data-mcard]');
      if (!card || card.classList.contains('locked')) return;
      var mi = +card.getAttribute('data-mcard');
      answers[mi] = +ob.getAttribute('data-i');
      $$('.opt', card).forEach(function (x) {
        x.classList.remove('chosen');
        x.style.borderColor = '';
        x.style.background = '';
      });
      ob.classList.add('chosen');
      ob.style.borderColor = 'var(--accent)';
      ob.style.background = 'color-mix(in srgb, var(--accent) 12%, var(--surface))';
    });
    $('#mockSubmit').onclick = function () {
      var missing = [];
      items.forEach(function (it, i) { if (answers[i] === undefined) missing.push(i + 1); });
      if (missing.length && !confirm('还有 ' + missing.length + ' 题未作答，确定交卷吗？／ 未回答の問題があります。')) return;
      var sec = [[0, 0], [0, 0], [0, 0], [0, 0]], right = 0;
      items.forEach(function (it, i) {
        var ok = answers[i] === it.correct;
        if (ok) right++;
        sec[it.sec][0]++; if (ok) sec[it.sec][1]++;
        logRes(it.cat, ok);
        var card = sheet.querySelector('[data-mcard="' + i + '"]');
        card.classList.add('locked');
        var chosen = card.querySelector('.opt.chosen');
        $$('.opt', card).forEach(function (x) {
          x.classList.add('done');
          if (+x.getAttribute('data-i') === it.correct) x.classList.add('right');
          else if (x === chosen) x.classList.add('wrong');
          else x.classList.add('dim');
        });
        var rans = card.querySelector('.rans');
        if (rans) rans.innerHTML = '<div class="explain">' + (ok ? '<span class="pill g">✓</span>' : '<span class="pill r">✗ 正解は ' + esc(it.options[it.correct]) + '</span>') + '<div style="margin-top:6px">' + it.exp + '</div></div>';
      });
      var over = Math.round(right / items.length * 100);
      var secHtml = MPART.map(function (p, i) {
        var pc = sec[i][0] ? Math.round(sec[i][1] / sec[i][0] * 100) : 0;
        var col = pc >= 60 ? 'g' : pc >= 40 ? 'i' : '';
        return '<div class="card"><div class="spread"><b>' + esc(p.nameCN) + '</b><b>' + pc + '%</b></div>' +
          '<div class="bar ' + col + '"><i style="width:' + pc + '%"></i></div><div class="faint">' + sec[i][1] + '/' + sec[i][0] + ' 题</div></div>';
      }).join('');
      var advice = over >= 70 ? '状态不错！建议开始整套真题限时训练（105 分钟 + 50 分钟）。'
        : over >= 55 ? '接近合格线。针对最弱的部分专项突破后再来检验。'
        : '先别急。从「学习计划」第 2 阶段开始系统过语法与词汇。';
      $('#mockReport').innerHTML = '<div class="card mt2 reveal-anim"><h2>成绩单 ／ 結果</h2>' +
        '<div class="mt1" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px">' + secHtml + '</div>' +
        '<div class="explain mt2"><b>综合正确率：' + over + '%</b>（' + right + '/' + items.length + '）　参考建议：' + advice +
        '<div class="faint mt1">※ 真实 JLPT 采用“尺度得分”，本卷仅按正确率提供备考参考。</div></div>' +
        '<div class="row mt2"><button class="btn indigo" id="mockAgain">↻ 再抽一套</button>' +
        '<button class="btn" id="mockStats">学习报告 ›</button></div></div>';
      $('#mockAgain').onclick = function () { go('mock'); };
      $('#mockStats').onclick = function () { go('stats'); };
      $('#mockSubmit').disabled = true;
    };
  }

  /* ---------------- 学习报告 ---------------- */
  function viewStats() {
    var st = statsAll();
    var keys = Object.keys(st);
    if (!keys.length) {
      view.innerHTML = '<div class="card center"><h1>学习报告 ／ 学習記録</h1><p class="muted">还没有记录——先做几组练习吧！</p>' +
        '<div class="row center mt2" style="justify-content:center"><button class="btn primary" id="goV">词汇练习 ›</button>' +
        '<button class="btn" id="goG">语法 ›</button></div></div>';
      $('#goV').onclick = function () { go('vocab'); };
      $('#goG').onclick = function () { go('grammar'); };
      return;
    }
    var tot = 0, okc = 0;
    keys.forEach(function (k) { tot += st[k].t; okc += st[k].ok; });
    var overall = tot ? Math.round(okc / tot * 100) : 0;
    var bars = keys.sort(function (a, b) { return st[b].t - st[a].t; }).map(function (k) {
      var p = Math.round(st[k].ok / st[k].t * 100);
      return '<div class="mt1"><div class="spread"><span>' + esc(CAT[k].cn) + ' <span class="ja faint">' + esc(CAT[k].jp) + '</span></span>' +
        '<span class="faint">' + st[k].ok + ' / ' + st[k].t + '（' + p + '%）</span></div>' +
        '<div class="bar ' + (p >= 60 ? 'g' : p >= 40 ? 'i' : '') + '"><i style="width:' + p + '%"></i></div></div>';
    }).join('');
    view.innerHTML = '<h1>学习报告 ／ 学習記録</h1>' +
      '<div class="stat-grid mt2"><div class="stat"><div class="v">' + tot + '</div><div class="l">累计练习 総練習数</div></div>' +
      '<div class="stat"><div class="v">' + okc + '</div><div class="l">累计答对 正解数</div></div>' +
      '<div class="stat"><div class="v">' + overall + '%</div><div class="l">总正确率 正答率</div></div>' +
      '<div class="stat"><div class="v">' + (targetDate().getFullYear()) + '年</div><div class="l">目标考试 目標</div></div></div>' +
      '<div class="card mt2"><h3>分项正确率 ／ 分野別正答率</h3>' + bars + '</div>' +
      '<div class="card mt2"><p class="muted">💡 正确率低于 60% 的分类值得回炉：回「语法参考」重温句型，或把对应题型再做一轮。</p></div>' +
      '<button class="btn ghost mt2" id="clrLog">清除练习记录 履歴を消去</button>';
    $('#clrLog').onclick = function () {
      if (confirm('确定清除全部练习记录？／ 記録を消去しますか？')) {
        apiDel('/api/reset/attempts'); LS.set(KEY.log, []); go('stats');
      }
    };
  }

  /* ---------------- 初始化 ---------------- */
  function init() {
    buildNav();
    applyTheme();
    updateCd();
    window.addEventListener('hashchange', function () { updateCd(); render(); });
    $('#themeBtn').onclick = function () {
      var t = LS.get(KEY.theme, '');
      LS.set(KEY.theme, t === 'dark' ? 'light' : t === 'light' ? '' : 'dark');
      applyTheme();
    };
    $('#navToggle').onclick = function () {
      $('#side').classList.toggle('open');
      $('#scrim').classList.toggle('on', $('#side').classList.contains('open'));
    };
    $('#scrim').onclick = closeDrawer;
    if ('speechSynthesis' in window) { speechSynthesis.getVoices(); speechSynthesis.onvoiceschanged = function () {}; }
    render();
  }
  /* ---------------- 启动（server 版：catalog/state → 迁移 → 渲染） ---------------- */
  function showConnError() {
    view.innerHTML = '<div class="card conn-err"><div class="big">📡</div><h2>无法连接本地服务 ／ 接続できません</h2>' +
      '<p class="muted">本站课程数据由本地 Node 服务提供，请先启动服务：</p>' +
      '<p><code>node server.js</code></p>' +
      '<p class="small faint">然后访问 http://127.0.0.1:4397 并回到本页重试。</p>' +
      '<button class="btn primary" id="retryBoot">↻ 重试 再試行</button></div>';
    $('#retryBoot').onclick = function () { view.innerHTML = '<p class="muted center">连接中… 読込中</p>'; boot(); };
  }
  function legacyPayload() {
    function rd(k) { try { var v = localStorage.getItem(k); return v === null ? undefined : JSON.parse(v); } catch (e) { return undefined; } }
    var any = [KEY.theme, KEY.target, KEY.rate, KEY.blind].some(function (k) { return localStorage.getItem(k) !== null; }) ||
      localStorage.getItem(KEY.done) !== null || localStorage.getItem(KEY.known) !== null || localStorage.getItem(KEY.log) !== null;
    if (!any) return null;
    var payload = {};
    var done = rd(KEY.done); if (Array.isArray(done)) payload.done = done;
    var known = rd(KEY.known); if (Array.isArray(known)) payload.known = known;
    var log = rd(KEY.log); if (Array.isArray(log)) payload.log = log;
    var settings = {};
    [KEY.theme, KEY.target, KEY.rate, KEY.blind].forEach(function (k) {
      var v = rd(k); if (v !== undefined) settings[k.slice(3)] = JSON.stringify(v);
    });
    if (Object.keys(settings).length) payload.settings = settings;
    return payload;
  }
  function boot() {
    function get(p) { return fetch(p).then(function (r) { if (!r.ok) throw new Error(p + ' HTTP ' + r.status); return r.json(); }); }
    Promise.all([get('/api/catalog'), get('/api/state')]).then(function (d) {
      var cat = d[0], k;
      for (k in cat) if (Object.prototype.hasOwnProperty.call(cat, k)) window.N2DATA[k] = cat[k];
      var pl = legacyPayload();
      if (pl) {
        return fetch('/api/migrate', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(pl), keepalive: true })
          .then(function () { return get('/api/state'); });
      }
      return d[1];
    }).then(function (st) { LS._hydrate(st); init(); })
      .catch(function (e) { console.warn('boot 失败：', e); showConnError(); });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
