#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Structure-preserving zh -> ja localization for the sap_sd_jp site generator.

Atom  = one line of natural-language text that must be translated.
        Anything that must NOT change (HTML tags, Python {placeholders}, &entities;)
        is pulled out into a per-literal token list and replaced by a marker
        U+27E6 n U+27E7 in the text handed to the translator, so a translation
        cannot break the markup; the marker multiset is verified on the way back in.

CLI
  python3 work/i18n.py collect src|model|all     # -> work/ja/{src,model}_atoms.json + refs
  python3 work/i18n.py batches [maxchars]        # -> work/ja/batches/bNN.json  (+ shared brief)
  python3 work/i18n.py merge                     # work/ja/out/*.json -> work/ja/{kind}_map.json
  python3 work/i18n.py apply src|model|all       # map -> real files (backups in work/ja/orig/)
  python3 work/i18n.py check                     # marker / coverage validation
  python3 work/i18n.py terms [n]                 # candidate term frequency list
"""
import hashlib
import io
import json
import os
import re
import sys
import tokenize
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JA = os.path.join(ROOT, 'work/ja')
BATCH = os.path.join(JA, 'batches')
OUT = os.path.join(JA, 'out')
ORIG = os.path.join(JA, 'orig')

SRC_FILES = [
    'tools/sitegen/common.py',
    'tools/sitegen/pg_module.py',
    'tools/sitegen/pg_static.py',
    'tools/sitegen/pg_teach.py',
    'tools/build_pages.py',
    'tools/make_jp_xlsx.py',
    'tools/verify_site_jp.py',
    'assets/s4jp.js',
    'assets/main.js',
    'assets/quiz.js',
]

CJK = re.compile(r'[\u2e80-\u9fff\uf900-\ufaff\uff66-\uff9f]')
TOKEN_RE = re.compile(r'(<[^<>]*>|\{[^{}]*\}|&[a-zA-Z#0-9]+;)')
LM, RM = '\u27e6', '\u27e7'
MARK_RE = re.compile(LM + r'(\d+)' + RM)


def md5(s):
    return hashlib.md5(s.encode('utf-8')).hexdigest()


def atom_id(text):
    return 't' + md5(text)[:10]


def has_cjk(s):
    return bool(CJK.search(s or ''))


def offsets(src):
    o = [0]
    for line in src.splitlines(True):
        o.append(o[-1] + len(line))
    return o


def pos2off(o, pos):
    row, col = pos
    return o[row - 1] + col


def mark(text):
    toks = []

    def rep(m):
        toks.append(m.group(0))
        return LM + str(len(toks) - 1) + RM

    return TOKEN_RE.sub(rep, text), toks


def unmark(marked, toks):
    seen = [int(x) for x in MARK_RE.findall(marked)]
    if sorted(seen) != list(range(len(toks))):
        raise ValueError('marker mismatch: seen=%s tokens=%d' % (seen, len(toks)))
    return MARK_RE.sub(lambda m: toks[int(m.group(1))], marked)


# ------------------------------------------------------------------ literals
def literal_spans(path, src):
    """[(start,end,inner_start,inner_end)] for python / js string literals."""
    out = []
    if path.endswith('.py'):
        try:
            toks = list(tokenize.generate_tokens(io.StringIO(src).readline))
        except Exception as e:
            print('  !! tokenize %s: %s' % (path, e), file=sys.stderr)
            return out
        o = offsets(src)
        for t in toks:
            if t.type != tokenize.STRING:
                continue
            raw = t.string
            pre = re.match(r'^[a-zA-Z]*', raw).group(0)
            body = raw[len(pre):]
            q = '"""' if body.startswith('"""') else "'''" if body.startswith("'''") else body[0]
            out.append((pos2off(o, t.start), pos2off(o, t.end),
                        pos2off(o, t.start) + len(pre) + len(q), pos2off(o, t.end) - len(q)))
    else:
        i, n = 0, len(src)
        while i < n:
            c = src[i]
            if c in '\'"`':
                q, j = c, i + 1
                while j < n:
                    if src[j] == '\\':
                        j += 2
                        continue
                    if src[j] == q:
                        break
                    j += 1
                out.append((i, j + 1, i + 1, j))
                i = j + 1
            elif src.startswith('//', i):
                k = src.find('\n', i)
                i = k if k > 0 else n
            elif src.startswith('/*', i):
                i = src.find('*/', i) + 2 if src.find('*/', i) > 0 else n
            else:
                i += 1
    return out


def collect_src():
    atoms, refs = {}, []
    for rel in SRC_FILES:
        path = os.path.join(ROOT, rel)
        if not os.path.exists(path):
            print('  -- missing %s' % rel)
            continue
        src = open(path, encoding='utf-8').read()
        for (s, e, is_, ie) in literal_spans(path, src):
            inner = src[is_:ie]
            if not has_cjk(inner):
                continue
            marked, toks = mark(inner)
            runs = []
            pos = 0
            for line in marked.split('\n'):
                ln = len(line)
                if has_cjk(line):
                    aid = atom_id(line)
                    atoms.setdefault(aid, line)
                    runs.append(dict(id=aid, start=is_ + pos, end=is_ + pos + ln))
                pos += ln + 1
            if runs:
                refs.append(dict(file=rel, lit=[s, e], inner=[is_, ie], tokens=toks,
                                 runs=runs, src_md5=md5(src)))
    _save(atoms, refs, 'src')
    return atoms


MODEL_FIELDS = ('title', 'caption', 'text', 'k', 'path', 'desc', 'rows')
MODEL_VALUE_FIELDS = ('v',)          # never translated: literal input values


def model_walk(node, path, out, parent=''):
    if isinstance(node, dict):
        for k, v in node.items():
            model_walk(v, path + [k], out, k)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            model_walk(v, path + [str(i)], out, parent)
    elif isinstance(node, str) and parent in MODEL_FIELDS and has_cjk(node):
        out.append(('.'.join(path), node))


def collect_model():
    model = json.load(open(os.path.join(ROOT, 'work/site_model.json'), encoding='utf-8'))
    found = []
    model_walk(model, [], found)
    atoms, refs = {}, []
    for p, text in found:
        # the model carries hard newlines; translate per line like the source files
        for line in text.split('\n'):
            if not has_cjk(line):
                continue
            aid = atom_id(line)
            atoms.setdefault(aid, line)
            refs.append(dict(path=p, id=aid))
    _save(atoms, refs, 'model', dedup_refs=True)
    return atoms


def _save(atoms, refs, kind, dedup_refs=False):
    os.makedirs(JA, exist_ok=True)
    json.dump(atoms, open(os.path.join(JA, kind + '_atoms.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=0, sort_keys=True)
    json.dump(refs, open(os.path.join(JA, kind + '_refs.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=0)
    print('%-6s %4d unique atoms / %6d refs / %6d chars'
          % (kind, len(atoms), len(refs), sum(len(v) for v in atoms.values())))


# ------------------------------------------------------------------- batches
def make_batches(maxchars=5000):
    os.makedirs(BATCH, exist_ok=True)
    index = []
    for kind in ('src', 'model'):
        p = os.path.join(JA, kind + '_atoms.json')
        if not os.path.exists(p):
            continue
        atoms = json.load(open(p, encoding='utf-8'))
        # biggest atoms first so the batches stay balanced
        items = sorted(atoms.items(), key=lambda kv: -len(kv[1]))
        n, cur, size = 0, {}, 0

        def flush(cur, size, n, kind=kind):
            if not cur:
                return n
            fn = '%s_%02d.json' % (kind, n)
            json.dump(cur, open(os.path.join(BATCH, fn), 'w', encoding='utf-8'),
                      ensure_ascii=False, indent=1)
            index.append(dict(batch=fn, kind=kind, n=len(cur),
                              chars=sum(len(v) for v in cur.values())))
            return n + 1

        for k, v in items:
            if size + len(v) > maxchars and cur:
                n = flush(cur, size, n)
                cur, size = {}, 0
            cur[k], size = v, size + len(v)
        n = flush(cur, size, n)
    json.dump(index, open(os.path.join(JA, 'batches_index.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    tot = sum(i['n'] for i in index)
    print('batches: %d files, %d atoms, %d chars'
          % (len(index), tot, sum(i['chars'] for i in index)))
    for i in index:
        print('  %-10s %-6s %4d atoms %6d chars' % (i['batch'], i['kind'], i['n'], i['chars']))


def normalize(t):
    """House style for the Japanese output (applied to every translation)."""
    t = t.replace('IMG設定', 'IMG 設定').replace('IMG设定', 'IMG 設定')
    t = t.replace('，', '、').replace('；', '；')
    t = re.sub(r' {2,}(?![ ]*⟦)', ' ', t)          # collapse doubled spaces
    t = t.replace('S4JP_', 'S4JP_').replace('S4CN', 'S4JP')
    return t


def merge_out():
    """work/ja/out/*.json (any of {id: text} shapes) -> per-kind maps."""
    os.makedirs(OUT, exist_ok=True)
    maps = {'src': {}, 'model': {}}
    files = sorted(f for f in os.listdir(OUT) if f.endswith('.json'))
    for f in files:
        try:
            data = json.load(open(os.path.join(OUT, f), encoding='utf-8'))
        except Exception as e:
            print('  !! %s: %s' % (f, e))
            continue
        if isinstance(data, dict) and 'items' in data and isinstance(data['items'], dict):
            data = data['items']
        if not isinstance(data, dict):
            print('  !! %s: not a dict' % f)
            continue
        for k, v in data.items():
            if not isinstance(v, str):
                continue
            for kind in ('src', 'model'):
                p = os.path.join(JA, kind + '_atoms.json')
                atoms = json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {}
                if k in atoms:
                    maps[kind][k] = normalize(v)
    for kind, m in maps.items():
        json.dump(m, open(os.path.join(JA, kind + '_map.json'), 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=0, sort_keys=True)
        atoms = json.load(open(os.path.join(JA, kind + '_atoms.json'), encoding='utf-8'))
        miss = [k for k in atoms if k not in m]
        print('%-6s translated %4d / %4d  (%d missing)'
              % (kind, len(m), len(atoms), len(miss)))
        if miss:
            json.dump(miss, open(os.path.join(JA, kind + '_missing.json'), 'w',
                                 encoding='utf-8'), ensure_ascii=False, indent=0)
            for k in miss[:5]:
                print('    MISSING %s %s' % (k, atoms[k][:60]))


# --------------------------------------------------------------------- apply
def backup(rel):
    dst = os.path.join(ORIG, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if not os.path.exists(dst):
        with open(os.path.join(ROOT, rel), 'rb') as fi, open(dst, 'wb') as fo:
            fo.write(fi.read())


def apply_src():
    m = json.load(open(os.path.join(JA, 'src_map.json'), encoding='utf-8'))
    refs = json.load(open(os.path.join(JA, 'src_refs.json'), encoding='utf-8'))
    byfile = {}
    for r in refs:
        byfile.setdefault(r['file'], []).append(r)
    bad = 0
    skipped = []
    for rel, rs in byfile.items():
        path = os.path.join(ROOT, rel)
        src = open(path, encoding='utf-8').read()
        want = rs[0].get('src_md5')
        if want and md5(src) != want:
            # the file was edited after `collect` (e.g. the structural patch pass);
            # splicing recorded offsets into it would corrupt it -> refuse.
            skipped.append(rel)
            continue
        backup(rel)
        # literals sorted descending so earlier offsets stay valid
        for r in sorted(rs, key=lambda x: -x['lit'][0]):
            s, e = r['inner']
            inner = src[s:e]
            marked, toks = mark(inner)
            lines = marked.split('\n')
            # walk runs and rebuild the marked text with translations
            pos = 0
            newl = []
            by_pos = {}
            for run in r['runs']:
                by_pos[(run['start'] - s, run['end'] - s)] = m[run['id']]
            for line in lines:
                ln = len(line)
                tr = by_pos.get((pos, pos + ln))
                newl.append(tr if tr is not None else line)
                pos += ln + 1
            newmarked = '\n'.join(newl)
            try:
                newinner = unmark(newmarked, toks)
            except ValueError as ex:
                print('  !! %s lit@%d: %s' % (rel, s, ex))
                bad += 1
                continue
            src = src[:s] + newinner + src[e:]
        open(path, 'w', encoding='utf-8').write(src)
        print('  patched %s' % rel)
    if skipped:
        print('src apply SKIPPED %d file(s) edited after collect: %s' % (len(skipped), skipped))
        print('  (restore them from work/ja/orig/ if you really want to re-splice the map)')
    print('src apply done (%d marker failures)' % bad)


def apply_model():
    m = json.load(open(os.path.join(JA, 'model_map.json'), encoding='utf-8'))
    src_path = os.path.join(ROOT, 'work/site_model.json')
    model = json.load(open(src_path, encoding='utf-8'))
    want = json.load(open(os.path.join(JA, 'model_refs.json'), encoding='utf-8'))
    want = want[0].get('src_md5') if want else None
    if want and md5(open(src_path, encoding='utf-8').read()) != want:
        print('model apply SKIPPED: work/site_model.json changed since collect')
        return

    def walk(node):
        if isinstance(node, dict):
            return {k: (walk(v) if k in MODEL_FIELDS or isinstance(v, (dict, list)) else v)
                    for k, v in node.items()}
        if isinstance(node, list):
            return [walk(v) for v in node]
        if isinstance(node, str) and has_cjk(node):
            return '\n'.join(m[atom_id(l)] if has_cjk(l) and atom_id(l) in m else l
                             for l in node.split('\n'))
        return node

    ja = walk(model)
    # 前后台 markers: the DATA value stays Chinese (the site code compares against it),
    # a Japanese display copy is added alongside.
    FB = {'后台': 'IMG設定（カスタマイズ）', '前台': '業務処理（トランザクション）'}

    def fbwalk(node):
        if isinstance(node, dict):
            out = {}
            for k, v in node.items():
                if k == 'fb' and isinstance(v, str):
                    out[k] = v
                    out['fb_ja'] = FB.get(v, v)
                else:
                    out[k] = fbwalk(v)
            return out
        if isinstance(node, list):
            return [fbwalk(v) for v in node]
        return node

    ja = fbwalk(ja)
    json.dump(ja, open(os.path.join(ROOT, 'work/site_model_ja.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    print('model apply done -> work/site_model_ja.json')


# ------------------------------------------------------------------- helpers
def check():
    for kind in ('src', 'model'):
        p = os.path.join(JA, kind + '_map.json')
        if not os.path.exists(p):
            continue
        m = json.load(open(p, encoding='utf-8'))
        atoms = json.load(open(os.path.join(JA, kind + '_atoms.json'), encoding='utf-8'))
        ident = [k for k, v in m.items() if k in atoms and v == atoms[k]]
        empty = [k for k, v in m.items() if not v.strip()]
        print('%-6s %4d translations; unchanged=%d empty=%d' % (kind, len(m), len(ident), len(empty)))
    # rebuild every literal exactly like apply_src does and validate the markers
    refs = json.load(open(os.path.join(JA, 'src_refs.json'), encoding='utf-8'))
    m = json.load(open(os.path.join(JA, 'src_map.json'), encoding='utf-8'))
    bad, ok = 0, 0
    for r in refs:
        src = open(os.path.join(ROOT, r['file']), encoding='utf-8').read()
        inner = src[r['inner'][0]:r['inner'][1]]
        marked, toks = mark(inner)
        lines = marked.split('\n')
        pos = 0
        new = []
        by_pos = {(run['start'] - r['inner'][0], run['end'] - r['inner'][0]): m[run['id']]
                  for run in r['runs']}
        for line in lines:
            ln = len(line)
            new.append(by_pos.get((pos, pos + ln), line))
            pos += ln + 1
        try:
            unmark('\n'.join(new), toks)
            ok += 1
        except Exception as ex:
            bad += 1
            print('  MARKER-FAIL %s @%d: %s' % (r['file'], r['inner'][0], ex))
    print('marker check: %d literals ok, %d failures' % (ok, bad))


def terms(n=400):
    cnt = Counter()
    for kind in ('src', 'model'):
        p = os.path.join(JA, kind + '_atoms.json')
        if not os.path.exists(p):
            continue
        for text in json.load(open(p, encoding='utf-8')).values():
            for w in re.findall(r'[\u4e00-\u9fff]{2,8}', text):
                cnt[w] += 1
    out = [(w, c) for w, c in cnt.most_common(n)]
    json.dump(out, open(os.path.join(JA, 'terms_candidates.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=0)
    for w, c in out:
        print('%5d  %s' % (c, w))


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'stats'
    if cmd == 'collect':
        what = sys.argv[2] if len(sys.argv) > 2 else 'all'
        collect_src() if what in ('src', 'all') else None
        collect_model() if what in ('model', 'all') else None
    elif cmd == 'batches':
        make_batches(int(sys.argv[2]) if len(sys.argv) > 2 else 7000)
    elif cmd == 'merge':
        merge_out()
    elif cmd == 'apply':
        what = sys.argv[2] if len(sys.argv) > 2 else 'all'
        apply_src() if what in ('src', 'all') else None
        apply_model() if what in ('model', 'all') else None
    elif cmd == 'check':
        check()
    elif cmd == 'terms':
        terms(int(sys.argv[2]) if len(sys.argv) > 2 else 400)
