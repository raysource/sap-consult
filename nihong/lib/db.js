/* ============================================================
   lib/db.js — 唯一的 SQLite 适配点（Node v26 内置 node:sqlite）
   未来想换 better-sqlite3，只改本文件即可。
   - open(file)：打开并建表（幂等）
   - transaction(db, fn)：事务包装（node:sqlite 无 .transaction()）
   - jsonGet/jsonSet：JSON 列编码/解码
   常量与内容表结构见 createSchema()
   ============================================================ */
'use strict';
const path = require('path');
const { DatabaseSync } = require('node:sqlite');

const DB_PATH = path.join(__dirname, '..', 'db', 'n2.sqlite');

/* ---------------- 打开 / 建表 ---------------- */
function open(file) {
  const db = new DatabaseSync(file, { enableForeignKeyConstraints: true, timeout: 5000 });
  db.exec('PRAGMA journal_mode = WAL;');
  createSchema(db);
  return db;
}

function createSchema(db) {
  db.exec(`
    CREATE TABLE IF NOT EXISTS words(
      id   INTEGER PRIMARY KEY AUTOINCREMENT,
      w    TEXT NOT NULL UNIQUE,             -- 表记（surface）
      y    TEXT NOT NULL DEFAULT '',         -- 读音（kana；纯假名词可空）
      m    TEXT NOT NULL,                    -- 中文释义
      pos  TEXT NOT NULL DEFAULT '',         -- 词性 名/動/形/ナ形/副/接続/他（旧数据留空）
      src  TEXT NOT NULL,                    -- kanji(旧读音池) | ref(旧速查表) | core(新词条)
      seq  INTEGER NOT NULL
    );

    CREATE TABLE IF NOT EXISTS content_json(
      key       TEXT PRIMARY KEY,
      data_json TEXT NOT NULL                -- 'exam' / 'plan' 整 JSON 块
    );

    CREATE TABLE IF NOT EXISTS meta(
      key   TEXT PRIMARY KEY,
      value TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS vocab_bank(
      id        INTEGER PRIMARY KEY AUTOINCREMENT,
      kind      TEXT NOT NULL,               -- ortho | context | paraph | usage
      seq       INTEGER NOT NULL,
      body_json TEXT NOT NULL                -- 原题整对象（含 opts 数组）
    );

    CREATE TABLE IF NOT EXISTS grammar_pattern(
      id     INTEGER PRIMARY KEY AUTOINCREMENT,
      seq    INTEGER NOT NULL,
      form   TEXT NOT NULL,                  -- 句型，如「〜に伴って」
      grp    TEXT NOT NULL DEFAULT '',       -- 分组
      cn     TEXT NOT NULL DEFAULT '',
      jp     TEXT NOT NULL DEFAULT '',
      conn   TEXT NOT NULL DEFAULT '',
      ex_json TEXT NOT NULL                  -- [[日例, 中例], ...]
    );

    CREATE TABLE IF NOT EXISTS grammar_bank(
      id        INTEGER PRIMARY KEY AUTOINCREMENT,
      kind      TEXT NOT NULL CHECK(kind IN ('quiz','arrange','passage')),
      seq       INTEGER NOT NULL,
      body_json TEXT NOT NULL                -- 题整对象（arrange 含 head/parts/order/starPos/full）
    );

    CREATE TABLE IF NOT EXISTS reading_set(
      id         INTEGER PRIMARY KEY AUTOINCREMENT,
      sid        TEXT NOT NULL UNIQUE,       -- r1..r7
      seq        INTEGER NOT NULL,
      type       TEXT NOT NULL DEFAULT '',
      typeJP     TEXT NOT NULL DEFAULT '',
      typeCN     TEXT NOT NULL DEFAULT '',
      title      TEXT NOT NULL DEFAULT '',
      text       TEXT,                       -- 单篇正文（观点对比篇为 NULL）
      texts_json TEXT                        -- [{label,from,text},...] 观点对比篇
    );

    CREATE TABLE IF NOT EXISTS reading_question(
      id        INTEGER PRIMARY KEY AUTOINCREMENT,
      set_id    INTEGER NOT NULL REFERENCES reading_set(id),
      seq       INTEGER NOT NULL,
      q         TEXT NOT NULL DEFAULT '',
      opts_json TEXT NOT NULL,
      a         INTEGER NOT NULL,
      cn        TEXT NOT NULL DEFAULT ''
    );

    CREATE TABLE IF NOT EXISTS listening_set(
      id      INTEGER PRIMARY KEY AUTOINCREMENT,
      sid     TEXT NOT NULL UNIQUE,          -- l1..l6
      seq     INTEGER NOT NULL,
      type    TEXT NOT NULL DEFAULT '',
      typeJP  TEXT NOT NULL DEFAULT '',
      typeCN  TEXT NOT NULL DEFAULT '',
      tipCN   TEXT NOT NULL DEFAULT '',
      tipJP   TEXT NOT NULL DEFAULT '',
      scenario TEXT,                         -- 可空
      share   TEXT                           -- 复用上一组对话的 sid（l6→l5）
    );

    CREATE TABLE IF NOT EXISTS listening_line(
      id     INTEGER PRIMARY KEY AUTOINCREMENT,
      set_id INTEGER NOT NULL REFERENCES listening_set(id),
      seq    INTEGER NOT NULL,
      sp     TEXT,                           -- 说话人，可空
      t      TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS listening_item(
      id        INTEGER PRIMARY KEY AUTOINCREMENT,
      set_id    INTEGER NOT NULL REFERENCES listening_set(id),
      seq       INTEGER NOT NULL,
      u         TEXT NOT NULL,               -- 即时应答：待回应的一句话
      opts_json TEXT NOT NULL,
      a         INTEGER NOT NULL,
      cn        TEXT NOT NULL DEFAULT ''
    );

    CREATE TABLE IF NOT EXISTS listening_question(
      id        INTEGER PRIMARY KEY AUTOINCREMENT,
      set_id    INTEGER NOT NULL REFERENCES listening_set(id),
      seq       INTEGER NOT NULL,
      text      TEXT,                        -- 题干（可空）
      opts_json TEXT NOT NULL,
      a         INTEGER NOT NULL,
      cn        TEXT NOT NULL DEFAULT ''
    );

    /* ---------------- 进度表（仅经 API 写，seed 绝不触碰） ---------------- */
    CREATE TABLE IF NOT EXISTS settings(
      key   TEXT PRIMARY KEY,                -- theme | target | rate | blind
      value TEXT NOT NULL                    -- JSON 编码（'"dark"' / '"0.9"'）
    );

    CREATE TABLE IF NOT EXISTS done_task(
      task_id TEXT PRIMARY KEY,              -- 原 p0-1…（勾/取消 upsert）
      done_at INTEGER NOT NULL
    );

    CREATE TABLE IF NOT EXISTS known_word(
      w        TEXT PRIMARY KEY,
      word_id  INTEGER,                      -- 冗余参考（重建后可能失效，仅信息用）
      known_at INTEGER NOT NULL
    );

    CREATE TABLE IF NOT EXISTS attempts(
      id  INTEGER PRIMARY KEY AUTOINCREMENT,
      cat TEXT NOT NULL,                     -- 与 CAT 键一致（kanji/grammar/reading…）
      ok  INTEGER NOT NULL,                  -- 0/1
      ts  INTEGER NOT NULL
    );

    CREATE INDEX IF NOT EXISTS idx_words_y      ON words(y);
    CREATE INDEX IF NOT EXISTS idx_vb_kind      ON vocab_bank(kind);
    CREATE INDEX IF NOT EXISTS idx_rq_set       ON reading_question(set_id);
    CREATE INDEX IF NOT EXISTS idx_ll_set       ON listening_line(set_id);
    CREATE INDEX IF NOT EXISTS idx_li_set       ON listening_item(set_id);
    CREATE INDEX IF NOT EXISTS idx_lq_set       ON listening_question(set_id);
    CREATE INDEX IF NOT EXISTS idx_att_cat      ON attempts(cat);
    CREATE INDEX IF NOT EXISTS idx_att_ts       ON attempts(ts);
  `);
}

/* ---------------- 事务 ---------------- */
function transaction(db, fn) {
  db.exec('BEGIN');
  try {
    const r = fn();
    db.exec('COMMIT');
    return r;
  } catch (e) {
    try { db.exec('ROLLBACK'); } catch (_) { /* ignore */ }
    throw e;
  }
}

/* ---------------- JSON 列助手 ---------------- */
function jstr(v) { return v === undefined ? null : JSON.stringify(v); }
function jpar(s) {
  if (s === null || s === undefined) return null;
  try { return JSON.parse(s); } catch (e) { return null; }
}

/* ---------------- 进程级单例（供 server 复用） ---------------- */
let _db = null;
function getDb() {
  if (!_db) _db = open(DB_PATH);
  return _db;
}
function close() { if (_db) { try { _db.close(); } catch (_) {} _db = null; } }

process.on('exit', close);
process.on('SIGINT', function () { close(); process.exit(130); });
process.on('SIGTERM', function () { close(); process.exit(143); });

module.exports = { DB_PATH, open, createSchema, transaction, getDb, close, jstr, jpar };
