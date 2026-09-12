/* ============================================================
   db/seed.js — 从种子源重建「内容表」（课程库），进度表绝不触碰。
   用法：
     node db/seed.js           # 重建内容表（可重复；幂等）
     node db/seed.js --force   # 同上（历史参数，内容表 DROP 后 id 自稳定）
   server.js 首启自动调用 run()。
   数据源：
     - db/seed/legacy/data-*.js  （逐字节未改，仅依赖 window）
     - db/seed/words/*.json       （新增 N2 词库，src='core'）
   ============================================================ */
'use strict';
const fs = require('fs');
const path = require('path');
const { open, DB_PATH, transaction, jstr } = require('../lib/db.js');

const LEGACY_DIR = path.join(__dirname, 'seed', 'legacy');
const WORDS_DIR = path.join(__dirname, 'seed', 'words');

/* 内容表清单（DROP 重建用；子表先删，父表后删） */
const CONTENT_TABLES = [
  'listening_question', 'listening_item', 'listening_line', 'listening_set',
  'reading_question', 'reading_set',
  'grammar_bank', 'grammar_pattern',
  'vocab_bank', 'words', 'content_json', 'meta',
];

function loadLegacy() {
  // 旧 data-*.js 为 IIFE，写 window.N2DATA；逐字节未改，仅垫一个 window。
  global.window = global;
  global.N2DATA = undefined;
  for (const name of ['data-exam', 'data-vocab', 'data-grammar', 'data-reading', 'data-listening']) {
    require(path.join(LEGACY_DIR, name + '.js'));
  }
  const d = global.N2DATA;
  if (!d) throw new Error('legacy 数据未载入（window.N2DATA 为空）');
  return d;
}

function loadCoreWords() {
  const out = [];
  const names = fs.readdirSync(WORDS_DIR)
    .filter((f) => /^words-\d+-.+\.json$/.test(f))
    .sort();
  for (const f of names) {
    const arr = JSON.parse(fs.readFileSync(path.join(WORDS_DIR, f), 'utf8'));
    for (const e of arr) {
      if (!e || typeof e.w !== 'string' || !e.w) continue;
      out.push({ w: e.w, y: e.kana || '', m: e.mean || '', pos: e.pos || '', src: 'core' });
    }
  }
  return out;
}

/* 组装全部行数据（不落库），返回 { words, banks, grammar, reading, listening, content } */
function buildRows(legacy, core) {
  const v = legacy.vocab;
  const words = [];
  const seen = new Set();
  const addWord = (w, y, m, pos, src) => {
    if (seen.has(w)) return false;
    seen.add(w);
    words.push({ w, y: y || '', m, pos: pos || '', src });
    return true;
  };
  // 旧读音池（src='kanji'，全有读音）→ 旧速查表（src='ref'，可空读音）→ 新词 core
  for (const p of v.kanjiPool || []) addWord(p.w, p.y, p.m, '', 'kanji');
  for (const p of v.refList || []) addWord(p.w, p.y, p.m, '', 'ref');
  let skippedCore = 0;
  for (const c of core) if (!addWord(c.w, c.y, c.m, c.pos, 'core')) skippedCore++;
  if (skippedCore > 0) {
    console.warn(`[seed] 跳过 ${skippedCore} 条与旧数据重复的新增词（旧数据优先）`);
  }

  /* vocab_bank：kind 顺序 ortho/context/paraph/usage */
  const banks = [];
  for (const kind of ['ortho', 'context', 'paraph', 'usage']) {
    const arr = v[kind + 'Pool'] || [];
    arr.forEach((body, i) => banks.push({ kind, seq: i + 1, body }));
  }

  /* grammar */
  const g = legacy.grammar;
  const patterns = (g.list || []).map((p, i) => ({
    seq: i + 1,
    form: p.f || '',
    grp: p.group || '',
    cn: p.cn || '',
    jp: p.jp || '',
    conn: p.conn || '',
    ex: p.ex || [],
  }));
  const grammarBank = [];
  for (const [kind, arr] of [['quiz', g.quiz], ['arrange', g.arrange], ['passage', g.passage]]) {
    (arr || []).forEach((body, i) => grammarBank.push({ kind, seq: i + 1, body }));
  }

  /* reading：set + questions；单篇存 text，多篇(r5)存 texts_json */
  const readingSets = [];
  const readingQuestions = [];
  (legacy.reading.sets || []).forEach((s, i) => {
    const setId = readingSets.push({
      sid: s.id, seq: i + 1,
      type: s.type || '', typeJP: s.typeJP || '', typeCN: s.typeCN || '',
      title: s.title || '',
      text: s.texts ? null : (s.text ?? null),
      texts: s.texts || null,
    }) - 1;
    const qs = Array.isArray(s.questions) ? s.questions : [];
    qs.forEach((q, j) => {
      readingQuestions.push({ setKey: setId, seq: j + 1, q: q.q || '', opts: q.opts || [], a: q.a, cn: q.cn || '' });
    });
  });

  /* listening：set + lines(共享台词) + q 单题 / items(l4) */
  const listeningSets = [];
  const listeningLines = [];
  const listeningItems = [];
  const listeningQuestions = [];
  (legacy.listening.sets || []).forEach((s, i) => {
    const setKey = listeningSets.push({
      sid: s.id, seq: i + 1,
      type: s.type || '', typeJP: s.typeJP || '', typeCN: s.typeCN || '',
      tipCN: s.tipCN || '', tipJP: s.tipJP || '',
      scenario: s.scenario ?? null,
      share: s.share ?? null,
    }) - 1;
    if (Array.isArray(s.lines)) {
      s.lines.forEach((ln, j) => listeningLines.push({ setKey, seq: j + 1, sp: ln.sp ?? null, t: ln.t || '' }));
    }
    if (Array.isArray(s.items)) {
      s.items.forEach((it, j) => {
        listeningItems.push({ setKey, seq: j + 1, u: it.u || '', opts: it.opts || [], a: it.a, cn: it.cn || '' });
      });
    }
    if (s.q) {
      listeningQuestions.push({ setKey, seq: 1, text: s.q.text ?? null, opts: s.q.opts || [], a: s.q.a, cn: s.q.cn || '' });
    }
  });

  return { words, banks, patterns, grammarBank, readingSets, readingQuestions, listeningSets, listeningLines, listeningItems, listeningQuestions };
}

function run(db) {
  const legacy = loadLegacy();
  const core = loadCoreWords();
  const R = buildRows(legacy, core);

  const d = db || open(DB_PATH);
  transaction(d, () => {
    // 重建内容表
    for (const t of CONTENT_TABLES) d.exec(`DROP TABLE IF EXISTS ${t};`);
    const { createSchema } = require('../lib/db.js');
    createSchema(d);

    /* words */
    {
      const ins = d.prepare('INSERT INTO words(w,y,m,pos,src,seq) VALUES(?,?,?,?,?,?)');
      R.words.forEach((w, i) => ins.run(w.w, w.y, w.m, w.pos, w.src, i + 1));
    }

    /* content_json + meta */
    {
      const set = d.prepare('INSERT OR REPLACE INTO content_json(key,data_json) VALUES(?,?)');
      set.run('exam', jstr(legacy.exam));
      set.run('plan', jstr(legacy.plan));
      const metaIns = d.prepare('INSERT OR REPLACE INTO meta(key,value) VALUES(?,?)');
      const counts = {
        words: R.words.length,
        withReading: R.words.filter((w) => w.y).length,
        core: R.words.filter((w) => w.src === 'core').length,
        vocabBank: R.banks.length,
        grammarPattern: R.patterns.length,
        grammarBank: R.grammarBank.length,
        readingSet: R.readingSets.length,
        readingQuestion: R.readingQuestions.length,
        listeningSet: R.listeningSets.length,
        listeningQuestion: R.listeningQuestions.length,
        listeningItem: R.listeningItems.length,
        listeningLine: R.listeningLines.length,
      };
      metaIns.run('seeded_at', new Date().toISOString());
      metaIns.run('seed_counts', JSON.stringify(counts));
    }

    /* vocab_bank */
    {
      const ins = d.prepare('INSERT INTO vocab_bank(kind,seq,body_json) VALUES(?,?,?)');
      for (const b of R.banks) ins.run(b.kind, b.seq, jstr(b.body));
    }

    /* grammar */
    {
      const ip = d.prepare('INSERT INTO grammar_pattern(seq,form,grp,cn,jp,conn,ex_json) VALUES(?,?,?,?,?,?,?)');
      for (const p of R.patterns) ip.run(p.seq, p.form, p.grp, p.cn, p.jp, p.conn, jstr(p.ex));
      const ib = d.prepare('INSERT INTO grammar_bank(kind,seq,body_json) VALUES(?,?,?)');
      for (const b of R.grammarBank) ib.run(b.kind, b.seq, jstr(b.body));
    }

    /* reading */
    {
      const iset = d.prepare('INSERT INTO reading_set(sid,seq,type,typeJP,typeCN,title,text,texts_json) VALUES(?,?,?,?,?,?,?,?)');
      const iq = d.prepare('INSERT INTO reading_question(set_id,seq,q,opts_json,a,cn) VALUES(?,?,?,?,?,?)');
      R.readingSets.forEach((s, setKey) => {
        const { lastInsertRowid } = iset.run(s.sid, s.seq, s.type, s.typeJP, s.typeCN, s.title, s.text, s.texts ? jstr(s.texts) : null);
        const set_id = Number(lastInsertRowid);
        R.readingQuestions.filter((q) => q.setKey === setKey)
          .forEach((q) => iq.run(set_id, q.seq, q.q, jstr(q.opts), q.a, q.cn));
      });
    }

    /* listening */
    {
      const iset = d.prepare('INSERT INTO listening_set(sid,seq,type,typeJP,typeCN,tipCN,tipJP,scenario,share) VALUES(?,?,?,?,?,?,?,?,?)');
      const iln = d.prepare('INSERT INTO listening_line(set_id,seq,sp,t) VALUES(?,?,?,?)');
      const iit = d.prepare('INSERT INTO listening_item(set_id,seq,u,opts_json,a,cn) VALUES(?,?,?,?,?,?)');
      const iq = d.prepare('INSERT INTO listening_question(set_id,seq,text,opts_json,a,cn) VALUES(?,?,?,?,?,?)');
      R.listeningSets.forEach((s, setKey) => {
        const { lastInsertRowid } = iset.run(s.sid, s.seq, s.type, s.typeJP, s.typeCN, s.tipCN, s.tipJP, s.scenario, s.share);
        const set_id = Number(lastInsertRowid);
        R.listeningLines.filter((l) => l.setKey === setKey).forEach((l) => iln.run(set_id, l.seq, l.sp, l.t));
        R.listeningItems.filter((l) => l.setKey === setKey).forEach((l) => iit.run(set_id, l.seq, l.u, jstr(l.opts), l.a, l.cn));
        R.listeningQuestions.filter((q) => q.setKey === setKey).forEach((q) => iq.run(set_id, q.seq, q.text, jstr(q.opts), q.a, q.cn));
      });
    }
  });

  const counts = countsOf(d);
  if (!db) { try { d.close(); } catch (_) {} }
  return counts;
}

function countsOf(db) {
  const m = db.prepare('SELECT value FROM meta WHERE key=?').get('seed_counts');
  return m ? JSON.parse(m.value) : null;
}

if (require.main === module) {
  // CLI：直接跑一次
  const db = open(DB_PATH);
  const counts = run(db);
  db.close();
  console.log('seed OK', counts ? JSON.stringify(counts) : '');
}

module.exports = { run, CONTENT_TABLES };
