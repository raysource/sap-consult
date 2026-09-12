/* ============================================================
   db/verify.js — 内容库完整性断言（非零退出即失败）。
   用法：node db/verify.js   （先 node db/seed.js）
   对照两个独立数据源：
     - db/seed/legacy/data-*.js（逐字节未改） → 条数 / 逐条回读
     - db/seed/words/*.json                  → 与 words 表合并后的规模
   只读：绝不写入任何表。
   ============================================================ */
'use strict';
const fs = require('fs');
const path = require('path');
const { DB_PATH, open, jpar } = require('../lib/db.js');

const LEGACY_DIR = path.join(__dirname, 'seed', 'legacy');
const WORDS_DIR = path.join(__dirname, 'seed', 'words');

let failures = 0;
function check(name, cond, extra) {
  if (cond) console.log('  ✓ ' + name);
  else { failures++; console.error('  ✗ FAIL ' + name + (extra ? ' — ' + extra : '')); }
}
/* 选项合法性：长度 4 且唯一、0≤a<len */
function checkOpts(where, opts, a) {
  const oks = Array.isArray(opts) && opts.length === 4 && new Set(opts).size === opts.length;
  check(where + ' opts 4 且唯一', oks, 'opts=' + JSON.stringify(opts));
  check(where + ' a∈[0,len)', Number.isInteger(a) && a >= 0 && a < (Array.isArray(opts) ? opts.length : -1), 'a=' + a);
}

/* ---------------- 载入独立源 ---------------- */
global.window = global; global.N2DATA = undefined;
for (const n of ['data-exam', 'data-vocab', 'data-grammar', 'data-reading', 'data-listening'])
  require(path.join(LEGACY_DIR, n + '.js'));
const SRC = global.N2DATA;
const coreArr = fs.readdirSync(WORDS_DIR).filter((f) => /^words-\d+-.+\.json$/.test(f)).sort()
  .flatMap((f) => JSON.parse(fs.readFileSync(path.join(WORDS_DIR, f), 'utf8')));

console.log('— 对照源规模 —');
console.log('  legacy vocab: kanjiPool ' + SRC.vocab.kanjiPool.length +
  ' / refList ' + SRC.vocab.refList.length +
  ' / banks ' + SRC.vocab.orthoPool.length + '+' + SRC.vocab.contextPool.length +
  '+' + SRC.vocab.paraphPool.length + '+' + SRC.vocab.usagePool.length);
console.log('  grammar: list ' + SRC.grammar.list.length + ' / quiz ' + SRC.grammar.quiz.length +
  ' / arrange ' + SRC.grammar.arrange.length + ' / passage ' + SRC.grammar.passage.length);
console.log('  reading sets ' + SRC.reading.sets.length + ' / questions ' +
  SRC.reading.sets.reduce((n, s) => n + s.questions.length, 0));
console.log('  listening sets ' + SRC.listening.sets.length + ' / lines ' +
  SRC.listening.sets.reduce((n, s) => n + (s.lines ? s.lines.length : 0), 0) +
  ' / items ' + SRC.listening.sets.reduce((n, s) => n + (s.items ? s.items.length : 0), 0) +
  ' / q ' + SRC.listening.sets.filter((s) => s.q).length);
console.log('  core words files ' + coreArr.length + ' 条');

/* ---------------- 开库 ---------------- */
const db = open(DB_PATH);
const one = (s, ...p) => db.prepare(s).get(...p);
const all = (s, ...p) => db.prepare(s).all(...p);
const n = (s, ...p) => one('SELECT COUNT(*) c FROM (' + s + ') t', ...p).c;

console.log('— 规模阈值 —');
check('words ≥ 2000', one('SELECT COUNT(*) c FROM words').c >= 2000);
check('with-reading(y<>"") ≥ 1800', one("SELECT COUNT(*) c FROM words WHERE y<>''").c >= 1800);
check('w 全局唯一', n('SELECT w FROM words') === n('SELECT DISTINCT w FROM words'));
check('m 非空', n('SELECT w FROM words WHERE trim(m)=\'\'') === 0);
{
  const ALLOW = new Set(['', '名', '動', '形', 'ナ形', '副', '接続', '他']);
  const bad = all('SELECT DISTINCT pos FROM words WHERE src=\'core\' AND pos NOT IN (\'名\',\'動\',\'形\',\'ナ形\',\'副\',\'接続\',\'他\')');
  check('core 词性 ∈ 白名单', bad.length === 0, JSON.stringify(bad));
  void ALLOW;
}

console.log('— 语法 —');
check('grammar_pattern = 72', one('SELECT COUNT(*) c FROM grammar_pattern').c === 72, '源 ' + SRC.grammar.list.length);
const patBad = all('SELECT form FROM grammar_pattern WHERE trim(form)=\'\' OR ex_json IS NULL');
check('form 非空 / ex 可解析', patBad.length === 0);
for (const kind of [['quiz', 22], ['arrange', 7], ['passage', 6]]) {
  const c = one('SELECT COUNT(*) c FROM grammar_bank WHERE kind=?', kind[0]).c;
  check('grammar_bank ' + kind[0] + ' = ' + kind[1], c === kind[1], '实际 ' + c);
}
{
  const ok = all('SELECT body_json FROM grammar_bank WHERE kind=\'arrange\'');
  for (const row of ok) {
    const b = jpar(row.body_json);
    const parts = b && Array.isArray(b.parts) ? b.parts : [];
    const nos = parts.map((p) => p.no);
    const isPerm = Array.isArray(b.order) && b.order.length === parts.length &&
      new Set(b.order).size === parts.length && b.order.every((x) => nos.includes(x));
    check('arrange order 为 parts 排列', isPerm);
    check('arrange starPos∈[0,len)', Number.isInteger(b.starPos) && b.starPos >= 0 && b.starPos < parts.length);
    // head 可为空（整句在 parts/full），但 full 必须成句、parts 非空
    check('arrange full 成句 / parts 非空', b && typeof b.head === 'string' && !!b.full && parts.length > 0);
  }
  const qp = all('SELECT body_json FROM grammar_bank WHERE kind IN (\'quiz\',\'passage\')');
  qp.forEach((row, i) => { const b = jpar(row.body_json); checkOpts('文法题#' + i, b && b.opts, b && b.a); });
}

console.log('— 词汇小库 —');
{
  const exp = { ortho: 14, context: 18, paraph: 12, usage: 10 };
  for (const k of Object.keys(exp)) {
    const c = one('SELECT COUNT(*) c FROM vocab_bank WHERE kind=?', k).c;
    check('vocab_bank ' + k + ' = ' + exp[k], c === exp[k], '实际 ' + c);
  }
  const rows = all('SELECT kind,body_json FROM vocab_bank ORDER BY kind,seq');
  rows.forEach((r) => {
    const b = jpar(r.body_json);
    check('vocab_bank ' + r.kind + ' 整对象可解析', !!b && typeof b === 'object');
    checkOpts('vocab_bank ' + r.kind + ' opts', b && b.opts, b && b.a);
  });
}

console.log('— 阅读 —');
check('reading_set = 7', one('SELECT COUNT(*) c FROM reading_set').c === 7, '源 ' + SRC.reading.sets.length);
check('reading_question = 16', one('SELECT COUNT(*) c FROM reading_question').c === 16,
  '源 ' + SRC.reading.sets.reduce((n2, s) => n2 + s.questions.length, 0));
{
  const bySet = all('SELECT s.sid sid,COUNT(q.id) c FROM reading_set s LEFT JOIN reading_question q ON q.set_id=s.id GROUP BY s.id ORDER BY s.seq');
  SRC.reading.sets.forEach((s) => {
    const row = bySet.find((x) => x.sid === s.id);
    check('reading ' + s.id + ' 题数=' + s.questions.length, !!row && row.c === s.questions.length,
      'DB ' + (row && row.c) + ' vs 源 ' + s.questions.length);
  });
  const setRows = all('SELECT * FROM reading_set ORDER BY seq');
  for (const r of setRows) {
    if (r.text === null) {
      const arr = jpar(r.texts_json);
      check('reading ' + r.sid + ' texts_json 可解析', Array.isArray(arr) && arr.every((x) => x.text));
    } else {
      check('reading ' + r.sid + ' 有正文', !!r.text);
    }
  }
  const qs = all('SELECT * FROM reading_question');
  qs.forEach((q, i) => { check('reading题#' + i + ' q 非空', !!q.q); checkOpts('reading题#' + i, jpar(q.opts_json), q.a); });
}

console.log('— 听力 —');
check('listening_set = 6', one('SELECT COUNT(*) c FROM listening_set').c === 6, '源 ' + SRC.listening.sets.length);
check('listening_question = 5', one('SELECT COUNT(*) c FROM listening_question').c === 5);
check('listening_item = 5', one('SELECT COUNT(*) c FROM listening_item').c === 5);
check('listening_line = 20', one('SELECT COUNT(*) c FROM listening_line').c === 20);
{
  const bySet = all('SELECT s.sid sid, COUNT(DISTINCT ln.id) lines, COUNT(DISTINCT it.id) items, COUNT(DISTINCT q.id) qs ' +
    'FROM listening_set s LEFT JOIN listening_line ln ON ln.set_id=s.id ' +
    'LEFT JOIN listening_item it ON it.set_id=s.id LEFT JOIN listening_question q ON q.set_id=s.id ' +
    'GROUP BY s.id ORDER BY s.seq');
  SRC.listening.sets.forEach((s) => {
    const row = bySet.find((x) => x.sid === s.id);
    check('listening ' + s.id + ' lines=' + (s.lines ? s.lines.length : 0) +
      ' items=' + (s.items ? s.items.length : 0) + ' q=' + (s.q ? 1 : 0),
      !!row && row.lines === (s.lines ? s.lines.length : 0) &&
      row.items === (s.items ? s.items.length : 0) && row.qs === (s.q ? 1 : 0),
      JSON.stringify(row));
  });
  const sh = one("SELECT * FROM listening_set WHERE share IS NOT NULL");
  check('l6.share=\'l5\' 且 l5 存在', sh && sh.share === 'l5' && one('SELECT COUNT(*) c FROM listening_set WHERE sid=\'l5\'').c === 1,
    JSON.stringify(sh));
  all('SELECT * FROM listening_line').forEach((l) => { check('line 文本非空', !!l.t); });
  all('SELECT * FROM listening_item').forEach((it, i) => { check('item#' + i + ' u 非空', !!it.u); checkOpts('item#' + i, jpar(it.opts_json), it.a); });
  all('SELECT * FROM listening_question').forEach((qq, i) => { checkOpts('听力题#' + i, jpar(qq.opts_json), qq.a); });
}

console.log('— 旧数据逐条回读（src=kanji/ref）—');
{
  const src = (pools) => pools.reduce((a, p) => a.concat(p), []);
  const srcKanji = src([SRC.vocab.kanjiPool]);
  const srcRef = src([SRC.vocab.refList]);
  const dbRows = all('SELECT * FROM words WHERE src IN (\'kanji\',\'ref\') ORDER BY seq');
  check('kanji+ref 总数 = ' + (srcKanji.length + srcRef.length), dbRows.length === srcKanji.length + srcRef.length,
    'DB ' + dbRows.length);
  const rowEq = (r, s) => r.w === s.w && (r.y || '') === (s.y || '') && r.m === s.m;
  let ok = true; const bads = [];
  dbRows.forEach((r, i) => {
    const s = i < srcKanji.length ? srcKanji[i] : srcRef[i - srcKanji.length];
    if (!rowEq(r, s)) { ok = false; bads.push(r.w); }
  });
  check('kanji/ref 每行与旧数据逐条一致（含顺序）', ok, '差异 ' + bads.join(','));
}

console.log('— 说明性 JSON（content_json）—');
for (const k of ['exam', 'plan']) {
  const row = one('SELECT data_json FROM content_json WHERE key=?', k);
  const obj = row && jpar(row.data_json);
  check('content_json.' + k + ' 存在且为对象', !!obj && typeof obj === 'object' && !Array.isArray(obj));
}

db.close();
console.log(failures === 0 ? '\nverify OK ✔' : '\nverify FAILED ✗ (' + failures + ')');
process.exit(failures === 0 ? 0 : 1);
