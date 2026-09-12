#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Second structural pass: 前后台 markers.

The translator turned the code literal '后台' / '前台' into 'IMG 設定' / '業務処理'
(both in the comparisons and in the labels).  The DATA in work/site_model_ja.json keeps
the original Chinese value so the model stays comparable to the source model, and carries
a Japanese display copy in fb_ja.  So:
  * comparisons go back to the canonical Chinese constants (FB_IMG / FB_FRONT),
  * every display site goes through fb_label(t).

  python3 work/jp_finalize2.py
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HELPER = '''
FB_IMG, FB_FRONT = '后台', '前台'   # 原教材ドキュメントの表記（データ側の値）


def fb_label(t):
    """表示用の日本語ラベル（IMG 設定 / 業務処理）。"""
    return t.get('fb_ja') or t.get('fb') or ''
'''

FAIL = []


def patch(rel, pairs, regex_pairs=()):
    p = os.path.join(ROOT, rel)
    s = open(p, encoding='utf-8').read()
    for old, new in pairs:
        if old not in s:
            FAIL.append('%s: %r not found' % (rel, old[:60]))
            continue
        s = s.replace(old, new)
    for pat, new in regex_pairs:
        s, n = re.subn(pat, new, s)
        if not n:
            FAIL.append('%s: regex %r matched nothing' % (rel, pat[:60]))
    open(p, 'w', encoding='utf-8').write(s)
    print('  patched %s' % rel)


def main():
    # 1. helper in common.py
    rel = 'tools/sitegen/common.py'
    p = os.path.join(ROOT, rel)
    s = open(p, encoding='utf-8').read()
    if 'def fb_label' not in s:
        m = re.search(r'^def mod_of\(', s, re.M)
        s = s[:m.start()] + HELPER.lstrip('\n') + '\n\n' + s[m.start():]
    # display site in the task header
    s = s.replace("""    if t['fb']:
        tags.append(f'<span class="fb{" img" if t["fb"] == "前台" else ""}">{esc(t["fb"])}</span>')""",
                  """    if t['fb']:
        tags.append(f'<span class="fb{" img" if t["fb"] == FB_FRONT else ""}">{esc(fb_label(t))}</span>')""")
    open(p, 'w', encoding='utf-8').write(s)
    print('  patched %s' % rel)

    # 2. comparisons + displays
    patch('tools/sitegen/pg_module.py', [
        ("sum(1 for t in ts if t['fb'] == 'IMG 設定')", "sum(1 for t in ts if t['fb'] == FB_IMG)"),
        ("sum(1 for t in ts if t['fb'] == '業務処理')", "sum(1 for t in ts if t['fb'] == FB_FRONT)"),
        ("fb = esc(t['fb']) if t['fb'] else '—'", "fb = esc(fb_label(t)) if t['fb'] else '—'"),
    ])
    patch('tools/sitegen/pg_module.py', [], [
        (r"^from common import \(([^)]*)\)",
         lambda m: 'from common import (%s, FB_IMG, FB_FRONT, fb_label)' % m.group(1)),
    ])
    patch('tools/sitegen/pg_static.py', [
        ("sum(1 for t in ts if t['fb'] == 'IMG 設定')", "sum(1 for t in ts if t['fb'] == FB_IMG)"),
        ("sum(1 for t in ts if t['fb'] == '業務処理')", "sum(1 for t in ts if t['fb'] == FB_FRONT)"),
        ('f\'<td>{esc(t["fb"] or "—")}</td>\'', 'f\'<td>{esc(fb_label(t) or "—")}</td>\''),
    ])
    patch('tools/sitegen/pg_static.py', [], [
        (r"^from common import \(([^)]*)\)",
         lambda m: 'from common import (%s, FB_IMG, FB_FRONT, fb_label)' % m.group(1)),
    ])
    patch('tools/sitegen/pg_teach.py', [
        ("fb = esc(t['fb'] or '—')", "fb = esc(fb_label(t) or '—')"),
    ])
    patch('tools/sitegen/pg_teach.py', [], [
        (r"^from common import \(([^)]*)\)",
         lambda m: 'from common import (%s, FB_IMG, FB_FRONT, fb_label)' % m.group(1)),
    ])
    patch('tools/make_jp_xlsx.py', [
        ("sum(1 for t in ts if t['fb'] == 'IMG 設定')", "sum(1 for t in ts if t['fb'] == '后台')"),
        ("sum(1 for t in ts if t['fb'] == '業務処理')", "sum(1 for t in ts if t['fb'] == '前台')"),
        ("t['fb'] or ''", "(t.get('fb_ja') or t['fb'] or '')"),
    ])
    if FAIL:
        for f in FAIL:
            print('  FAIL:', f)
        sys.exit(1)
    print('finalize2 OK')


if __name__ == '__main__':
    main()
