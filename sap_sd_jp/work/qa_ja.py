#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""QA: 生成した日本語ページに中国語（簡体字）が残っていないか確認する。

意図的に中国語を残している領域（原語の折りたたみ・中国語 IMG パス・用語対照表の
中国語列）は除外したうえで、簡体字特有の文字を数える。

  python3 work/qa_ja.py
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

PAGES = ['index.html', 'prep.html', 'fi.html', 'co.html', 'mm.html', 'pp.html', 'sd.html',
         'tcode.html', 'glossary.html', 'issues.html', 'tasks.html', 'instructor.html',
         'worksheet.html', 'quiz.html']

# 日本語（新字体）では使わない簡体字だけを並べる（例: 与・入・点・注・得 は日本語なので除く）
SIMPLIFIED = ('们这为个说时页单对开过还进选击钮确认录销订购货库输图实题问师员练习线报织经历级训达备观标记价据执专导产类总览规额'
              '应该让请谢获务权责见电东军农兴举龙阳阴齿龟决况净减划则创计结构术设备暂验让')

STRIP = [
    re.compile(r'<details class="orig">.*?</details>', re.S),
    re.compile(r'<div class="pathzh">.*?</div>', re.S),
    re.compile(r'<script.*?</script>', re.S),
    re.compile(r'<style.*?</style>', re.S),
]


def strip_parts(h):
    for rx in STRIP:
        h = rx.sub(' ', h)
    return h


def glossary_chinese_columns(h):
    """用語対照表の中国語列を落とす（<td><code>中文</code></td> と最終表の 3 列目）。"""
    h = re.sub(r'<td><code>[^<]*</code></td>', '<td></td>', h)
    h = re.sub(r'<td>(<a [^>]*>[^<]*</a>)</td><td>[^<]*</td>', r'<td>\1</td><td></td>', h)
    return h


def text_of(h):
    h = re.sub(r'<[^>]+>', ' ', h)
    h = h.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&nbsp;', ' ')
    return h


total = 0
for p in PAGES:
    if not os.path.exists(p):
        print('  -- missing', p)
        continue
    h = strip_parts(open(p, encoding='utf-8').read())
    if p == 'glossary.html':
        h = glossary_chinese_columns(h)
    t = text_of(h)
    hits = [(m.group(0), t[max(0, m.start() - 30):m.start() + 30].replace('\n', ' '))
            for m in re.finditer('[' + SIMPLIFIED + ']', t)]
    cjk = re.findall(r'[\u4e00-\u9fff]', t)
    print('%-18s 中国語候補 %4d 文字 (CJK 全体 %5d)  %.3f'
          % (p, len(hits), len(cjk), len(hits) / max(1, len(cjk))))
    for ch, ctx in hits[:6]:
        print('     %s … %s' % (ch, ctx.strip()[:80]))
    total += len(hits)
print('TOTAL 中国語候補 =', total)
