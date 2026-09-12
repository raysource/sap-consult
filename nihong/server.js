/* ============================================================
   server.js — N2 道場 本地服务（Node 内置 http，零依赖）
     node server.js            → http://127.0.0.1:4397
   - 静态白名单（html/css/js/json/svg/png/ico/txt/map），防路径穿越
   - /api/*  同源 JSON 读写（内容 catalog / 进度 state / 各写接口 / 重置 / 迁移）
   - 首启自动 ensureSeeded()：内容表空 → 调 db/seed.js 灌库
   ============================================================ */
'use strict';
const http = require('http');
const fs = require('fs');
const path = require('path');
const { getDb, jpar } = require('./lib/db.js');

const ROOT = __dirname;
const PORT = Number(process.env.PORT) || 4397;
const SETTING_KEYS = ['theme', 'target', 'rate', 'blind'];
const STATIC_EXT = new Set(['.html', '.css', '.js', '.json', '.svg', '.png', '.ico', '.txt', '.map', '.webmanifest']);

/* ---------------- 首启灌库 ---------------- */
function ensureSeeded() {
  const db = getDb();
  const meta = db.prepare("SELECT COUNT(*) c FROM meta WHERE key='seeded_at'").get();
  const words = db.prepare('SELECT COUNT(*) c FROM words').get();
  if (!meta.c || !words.c) {
    console.log('[server] 内容库为空，执行 seed…');
    require('./db/seed.js').run(db);
  }
}

/* ---------------- catalog：DB → 与 js/data-*.js 完全同构 ---------------- */
function buildCatalog(db) {
  const cj = {};
  for (const row of db.prepare('SELECT key,data_json FROM content_json').all()) {
    cj[row.key] = jpar(row.data_json);
  }
  const wordsRows = db.prepare('SELECT * FROM words ORDER BY seq').all();

  const kanjiPool = [], refList = [];
  for (const r of wordsRows) {
    const o = { w: r.w, y: r.y || '', m: r.m };
    if (r.y) kanjiPool.push(o);
    if (r.src === 'ref') refList.push(o);
  }

  const banks = { orthoPool: [], contextPool: [], paraphPool: [], usagePool: [] };
  const bankOrder = { ortho: 'orthoPool', context: 'contextPool', paraph: 'paraphPool', usage: 'usagePool' };
  for (const row of db.prepare('SELECT kind,seq,body_json FROM vocab_bank ORDER BY seq').all()) {
    banks[bankOrder[row.kind]].push(jpar(row.body_json));
  }

  const list = db.prepare('SELECT * FROM grammar_pattern ORDER BY seq').all().map((g) => ({
    f: g.form, group: g.grp, cn: g.cn, jp: g.jp, conn: g.conn, ex: jpar(g.ex_json),
  }));
  const gbank = { quiz: [], arrange: [], passage: [] };
  for (const row of db.prepare('SELECT kind,seq,body_json FROM grammar_bank ORDER BY seq').all()) {
    gbank[row.kind].push(jpar(row.body_json));
  }

  /* reading */
  const rq = db.prepare('SELECT q.set_id sid, q.seq, q.q, q.opts_json, q.a, q.cn FROM reading_question q ORDER BY q.seq').all();
  const rqBy = {};
  for (const q of rq) (rqBy[q.sid] = rqBy[q.sid] || []).push({ q: q.q, opts: jpar(q.opts_json), a: q.a, cn: q.cn });
  const reading = { sets: db.prepare('SELECT * FROM reading_set ORDER BY seq').all().map((s) => {
    const o = { id: s.sid, type: s.type, typeJP: s.typeJP, typeCN: s.typeCN, title: s.title };
    if (s.texts_json != null) o.texts = jpar(s.texts_json); else o.text = s.text;
    o.questions = rqBy[s.id] || [];
    return o;
  }) };

  /* listening：属性有无须与原形一致（items/lines/q/share/scenario 按存在才附） */
  const ll = db.prepare('SELECT l.set_id sid, l.seq, l.sp, l.t FROM listening_line l ORDER BY l.seq').all();
  const li = db.prepare('SELECT it.set_id sid, it.seq, it.u, it.opts_json, it.a, it.cn FROM listening_item it ORDER BY it.seq').all();
  const lq = db.prepare('SELECT x.set_id sid, x.seq, x.text, x.opts_json, x.a, x.cn FROM listening_question x ORDER BY x.seq').all();
  const grp = (arr, key) => { const m = {}; for (const r of arr) (m[r.sid] = m[r.sid] || []).push(r); return m; };
  const llBy = grp(ll, 'sid'), liBy = grp(li, 'sid'), lqBy = grp(lq, 'sid');
  const listening = { sets: db.prepare('SELECT * FROM listening_set ORDER BY seq').all().map((s) => {
    const o = { id: s.sid, type: s.type, typeJP: s.typeJP, typeCN: s.typeCN, tipCN: s.tipCN, tipJP: s.tipJP };
    if (s.scenario != null) o.scenario = s.scenario;
    if (s.share != null) o.share = s.share;
    if (llBy[s.id]) o.lines = llBy[s.id].map((x) => ({ sp: x.sp, t: x.t }));
    if (liBy[s.id]) o.items = liBy[s.id].map((x) => ({ u: x.u, opts: jpar(x.opts_json), a: x.a, cn: x.cn }));
    if (lqBy[s.id]) o.q = { text: lqBy[s.id][0].text, opts: jpar(lqBy[s.id][0].opts_json), a: lqBy[s.id][0].a, cn: lqBy[s.id][0].cn };
    return o;
  }) };

  const words = wordsRows.map((r) => ({ w: r.w, y: r.y || '', m: r.m, pos: r.pos, src: r.src }));
  const withReading = kanjiPool.length;
  return {
    exam: cj.exam, plan: cj.plan,
    counts: { words: words.length, withReading, banks: 54 },
    words,
    vocab: { kanjiPool, orthoPool: banks.orthoPool, contextPool: banks.contextPool, paraphPool: banks.paraphPool, usagePool: banks.usagePool, refList },
    grammar: { list, quiz: gbank.quiz, arrange: gbank.arrange, passage: gbank.passage },
    reading, listening,
  };
}

/* ---------------- state ---------------- */
function buildState(db) {
  const settings = {};
  for (const row of db.prepare('SELECT key,value FROM settings').all()) settings[row.key] = jpar(row.value);
  const done = db.prepare('SELECT task_id FROM done_task ORDER BY done_at').all().map((r) => r.task_id);
  const known = db.prepare('SELECT w FROM known_word').all().map((r) => r.w);
  const log = db.prepare('SELECT cat,ok,ts FROM attempts ORDER BY id DESC LIMIT 3000').all()
    .reverse().map((r) => ({ c: r.cat, ok: r.ok, t: r.ts }));
  return { settings, done, known, log };
}

/* ---------------- HTTP 装配 ---------------- */
function readBody(req) {
  return new Promise((resolve, reject) => {
    let n = 0; const chunks = [];
    req.on('data', (c) => { n += c.length; if (n > 2e6) { reject(new Error('body too large')); req.destroy(); return; } chunks.push(c); });
    req.on('end', () => resolve(Buffer.concat(chunks).toString('utf8')));
    req.on('error', reject);
  });
}
function jsonReq(req) {
  return readBody(req).then((s) => { if (!s) return {}; try { return JSON.parse(s); } catch (e) { return { _bad: true }; } });
}

async function handleApi(req, res, url) {
  const db = getDb();
  const send = (code, obj) => { const b = JSON.stringify(obj); res.writeHead(code, { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' }); res.end(b); };
  const bad = (m) => send(400, { error: m });
  const p = url.pathname;

  if (req.method === 'GET' && p === '/api/catalog') return send(200, buildCatalog(db));
  if (req.method === 'GET' && p === '/api/state') return send(200, buildState(db));

  if (req.method === 'DELETE' && p.indexOf('/api/reset/') === 0) {
    const table = p.slice('/api/reset/'.length);
    if (table === 'attempts') db.exec('DELETE FROM attempts');
    else if (table === 'done') db.exec('DELETE FROM done_task');
    else if (table === 'known') db.exec('DELETE FROM known_word');
    else return bad('unknown reset target');
    res.writeHead(204); return res.end();
  }

  if (req.method === 'POST') {
    return jsonReq(req).then((b) => {
      if (b._bad) return bad('invalid JSON');
      const t = Math.floor(Date.now() / 1000);
      if (p === '/api/attempts') {
        if (typeof b.cat !== 'string' || !(b.ok === true || b.ok === false || b.ok === 0 || b.ok === 1)) return bad('{cat,ok} 需要');
        db.prepare('INSERT INTO attempts(cat,ok,ts) VALUES(?,?,?)').run(b.cat, b.ok ? 1 : 0, t);
        res.writeHead(204); return res.end();
      }
      if (p === '/api/done') {
        if (typeof b.task !== 'string' || typeof b.done !== 'boolean') return bad('{task,done} 需要');
        if (b.done) db.prepare('INSERT OR REPLACE INTO done_task(task_id,done_at) VALUES(?,?)').run(b.task, t);
        else db.prepare('DELETE FROM done_task WHERE task_id=?').run(b.task);
        res.writeHead(204); return res.end();
      }
      if (p === '/api/known') {
        if (typeof b.word !== 'string' || typeof b.known !== 'boolean') return bad('{word,known} 需要');
        if (b.known) {
          const hit = db.prepare('SELECT id FROM words WHERE w=?').get(b.word);
          db.prepare('INSERT OR REPLACE INTO known_word(w,word_id,known_at) VALUES(?,?,?)').run(b.word, hit ? hit.id : null, t);
        } else db.prepare('DELETE FROM known_word WHERE w=?').run(b.word);
        res.writeHead(204); return res.end();
      }
      if (p === '/api/settings') {
        if (SETTING_KEYS.indexOf(b.key) === -1 || jpar(b.value) === null) return bad('settings key/value 不合法');
        db.prepare('INSERT OR REPLACE INTO settings(key,value) VALUES(?,?)').run(b.key, b.value);
        res.writeHead(204); return res.end();
      }
      if (p === '/api/migrate') {
        const merged = { settings: false, done: false, known: false, log: false };
        const tx = (fn) => { db.exec('BEGIN'); try { const r = fn(); db.exec('COMMIT'); return r; } catch (e) { try { db.exec('ROLLBACK'); } catch (_) {} throw e; } };
        tx(() => {
          const s = b.settings;
          if (s && typeof s === 'object' && db.prepare('SELECT COUNT(*) c FROM settings').get().c === 0) {
            for (const k of SETTING_KEYS) {
              if (k in s && jpar(s[k]) !== null) db.prepare('INSERT OR REPLACE INTO settings(key,value) VALUES(?,?)').run(k, String(s[k]));
            }
            merged.settings = true;
          }
          if (Array.isArray(b.done) && db.prepare('SELECT COUNT(*) c FROM done_task').get().c === 0) {
            const ins = db.prepare('INSERT OR REPLACE INTO done_task(task_id,done_at) VALUES(?,?)');
            b.done.forEach((id) => { if (typeof id === 'string') ins.run(id, t); });
            merged.done = true;
          }
          if (Array.isArray(b.known) && db.prepare('SELECT COUNT(*) c FROM known_word').get().c === 0) {
            const ins = db.prepare('INSERT OR REPLACE INTO known_word(w,word_id,known_at) VALUES(?,?,?)');
            b.known.forEach((w) => { if (typeof w === 'string') ins.run(w, null, t); });
            merged.known = true;
          }
          if (Array.isArray(b.log) && db.prepare('SELECT COUNT(*) c FROM attempts').get().c === 0) {
            const ins = db.prepare('INSERT INTO attempts(cat,ok,ts) VALUES(?,?,?)');
            b.log.forEach((e) => { if (e && typeof e.c === 'string' && typeof e.ok === 'boolean') ins.run(e.c, e.ok ? 1 : 0, Number.isFinite(e.t) ? e.t : t); });
            merged.log = true;
          }
        });
        return send(200, { merged });
      }
      return bad('unknown route');
    }).catch((e) => { res.writeHead(400); res.end(String(e && e.message)); });
  }
  return bad('unknown route');
}

function staticPath(url) {
  let p = decodeURIComponent(url.pathname);
  if (p === '/' || p === '') p = '/index.html';
  const ext = path.extname(p).toLowerCase();
  if (!STATIC_EXT.has(ext)) return null;
  const full = path.normalize(path.join(ROOT, p));
  if (full.indexOf(ROOT) !== 0) return null; // 穿越防护
  return full;
}

const server = http.createServer((req, res) => {
  const url = new URL(req.url, 'http://x');
  if (url.pathname === '/api' || url.pathname.indexOf('/api/') === 0) {
    handleApi(req, res, url).catch((e) => { try { res.writeHead(500); res.end(String(e)); } catch (_) {} });
    return;
  }
  if (req.method !== 'GET' && req.method !== 'HEAD') { res.writeHead(405); return res.end(); }
  const full = staticPath(url);
  if (!full || !fs.existsSync(full) || fs.statSync(full).isDirectory()) { res.writeHead(404); return res.end('404'); }
  const body = fs.readFileSync(full);
  const type = { '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.json': 'application/json; charset=utf-8', '.svg': 'image/svg+xml', '.png': 'image/png', '.ico': 'image/x-icon', '.txt': 'text/plain; charset=utf-8', '.map': 'application/json' }[path.extname(full).toLowerCase()] || 'application/octet-stream';
  res.writeHead(200, { 'Content-Type': type, 'Cache-Control': 'no-cache' });
  res.end(req.method === 'HEAD' ? undefined : body);
});

if (require.main === module) {
  ensureSeeded();
  server.listen(PORT, '127.0.0.1', () => {
    console.log('N2 道場 已启动 → http://127.0.0.1:' + PORT);
  });
}

module.exports = { buildCatalog, buildState, server, ensureSeeded };
