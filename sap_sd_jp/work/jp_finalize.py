#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Post-translation structural patch for sap_sd_jp.

The translation pass only rewrites natural-language text; everything that is *code*
(file names, html lang, the model path, nav entries, the glossary page) has to be
switched over here.  Run once after `python3 work/i18n.py apply all`.

  python3 work/jp_finalize.py
"""
import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAIL = []


def edit(rel, pairs, count=None):
    p = os.path.join(ROOT, rel)
    s = open(p, encoding='utf-8').read()
    for old, new in pairs:
        if old not in s:
            FAIL.append('%s: anchor not found: %r' % (rel, old[:70]))
            continue
        if s.count(old) > 1 and count is None:
            FAIL.append('%s: anchor not unique (%d): %r' % (rel, s.count(old), old[:70]))
            continue
        s = s.replace(old, new, 1 if count is None else count)
    open(p, 'w', encoding='utf-8').write(s)
    print('  patched %s' % rel)


# ---------------------------------------------------------------- common.py
def common():
    rel = 'tools/sitegen/common.py'
    p = os.path.join(ROOT, rel)
    s = open(p, encoding='utf-8').read()
    rep = [
        ('lang="zh-CN"', 'lang="ja"'),
        ('assets/s4cn.css', 'assets/s4jp.css'),
        ('assets/s4cn.js', 'assets/s4jp.js'),
        ("'work/site_model.json'", "'work/site_model_ja.json'"),
        ('"work/site_model.json"', '"work/site_model_ja.json"'),
    ]
    for old, new in rep:
        if old in s:
            s = s.replace(old, new)
        else:
            FAIL.append('%s: %r missing' % (rel, old))
    if 'MODEL_ZH' not in s:
        # add the Chinese model (kept for 「原文（中国語）」 and the term table)
        import re
        m = re.search(r'^MODEL = .*$', s, re.M)
        if not m:
            FAIL.append('%s: MODEL = line not found' % rel)
        else:
            ins = ("\nMODEL_ZH = json.load(open(os.path.join(ROOT, 'work/site_model.json')))"
                   "   # 原教材の中国語モデル（原文表示・対照表用）")
            s = s[:m.end()] + ins + s[m.end():]
    # nav: the glossary page (inserted right after the T-code entry)
    if 'glossary.html' not in s:
        import re
        m = re.search(r"^\s*\('tcode\.html',[^\n]*\n", s, re.M)
        if not m:
            FAIL.append('%s: nav tcode entry not found' % rel)
        else:
            s = s[:m.end()] + "    ('glossary.html', '用語'),\n" + s[m.end():]
    open(p, 'w', encoding='utf-8').write(s)
    print('  patched %s' % rel)


# ---------------------------------------------------------------- assets
def assets():
    edit('assets/s4jp.js', [('s4cn-lightbox', 's4jp-lightbox'), ('s4cn-shot-scale', 's4jp-shot-scale')])
    edit('assets/s4jp.css', [('#s4cn-lightbox', '#s4jp-lightbox')], count=99)
    # glossary filter (the same local-filter pattern as the task index)
    p = os.path.join(ROOT, 'assets/s4jp.js')
    s = open(p, encoding='utf-8').read()
    if 'initGlossFilter' not in s:
        fn = '''
  /* ---------------- 用語対照表の絞り込み ---------------- */
  function initGlossFilter() {
    var box = document.getElementById("glossfilter");
    var tbl = document.getElementById("glosstable");
    if (!box || !tbl) return;
    var rows = [].slice.call(tbl.querySelectorAll("tbody tr"));
    var count = document.getElementById("glosscount");
    function apply() {
      var q = box.value.trim().toLowerCase();
      var n = 0;
      rows.forEach(function (tr) {
        var ok = !q || (tr.getAttribute("data-key") || "").toLowerCase().indexOf(q) >= 0;
        tr.style.display = ok ? "" : "none";
        if (ok) n++;
      });
      if (count) count.textContent = n + " / " + rows.length + " 語を表示";
    }
    box.addEventListener("input", apply);
    apply();
  }
'''
        s = s.replace('  document.addEventListener("DOMContentLoaded", function () {',
                      fn + '\n  document.addEventListener("DOMContentLoaded", function () {')
        s = s.replace('    initSizer();', '    initSizer();\n    initGlossFilter();')
        open(p, 'w', encoding='utf-8').write(s)
        print('  added initGlossFilter() to assets/s4jp.js')


# ---------------------------------------------------------------- build pages
def build_pages():
    rel = 'tools/build_pages.py'
    p = os.path.join(ROOT, rel)
    s = open(p, encoding='utf-8').read()
    if 'pg_glossary' not in s:
        s = s.replace('import pg_static  # noqa: E402',
                      'import pg_static  # noqa: E402\nimport pg_glossary  # noqa: E402')
    if "write('glossary.html'" not in s:
        s = s.replace("    if want('issues'):",
                      "    if want('glossary'):\n        write('glossary.html', pg_glossary.build())\n"
                      "    if want('issues'):")
    s = s.replace("['index.html', 'tasks.html', 'tcode.html', 'issues.html',\n"
                  "             'instructor.html', 'worksheet.html', 'quiz.html']",
                  "['index.html', 'tasks.html', 'tcode.html', 'issues.html',\n"
                  "             'glossary.html', 'instructor.html', 'worksheet.html', 'quiz.html']")
    s = s.replace('verify_site_cn.py', 'verify_site_jp.py')
    open(p, 'w', encoding='utf-8').write(s)
    print('  patched %s' % rel)


# ---------------------------------------------------------------- excel
def xlsx():
    rel = 'tools/make_jp_xlsx.py'
    p = os.path.join(ROOT, rel)
    s = open(p, encoding='utf-8').read()
    s = s.replace('S4CN_手順書_学習WBS.xlsx', 'S4JP_手順書_学習WBS.xlsx')
    s = s.replace("'work/site_model.json'", "'work/site_model_ja.json'")
    open(p, 'w', encoding='utf-8').write(s)
    print('  patched %s' % rel)
    rel = 'tools/verify_site_jp.py'
    p = os.path.join(ROOT, rel)
    s = open(p, encoding='utf-8').read()
    s = s.replace("'work/site_model.json'", "'work/site_model_ja.json'")
    s = s.replace('S4CN_手順書_学習WBS.xlsx', 'S4JP_手順書_学習WBS.xlsx')
    if 'glossary.html' not in s:
        s = s.replace("'tcode.html', 'issues.html', 'tasks.html',",
                      "'tcode.html', 'glossary.html', 'issues.html', 'tasks.html',")
    open(p, 'w', encoding='utf-8').write(s)
    print('  patched %s' % rel)


if __name__ == '__main__':
    common()
    assets()
    build_pages()
    xlsx()
    if FAIL:
        print('\nFAILURES (%d):' % len(FAIL))
        for f in FAIL:
            print('  -', f)
        sys.exit(1)
    print('finalize OK')
