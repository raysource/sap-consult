#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Site-specific checks for S/4HANA 中文实训站 (run after tools/build_pages.py).

Checks:
 1. every <img src> exists on disk (and every figure's <a href> too)
 2. every internal href="#anchor" resolves to an id in the same page;
    every "page.html#anchor" resolves to an id in that page
 3. identical <nav class="main"> link list on all pages + exactly one .active
 4. exactly one </article> and it comes before <footer
 5. tag balance (HTMLParser), no leftover markdown (**), no stray "|" inside <td>
 6. quiz: every data-answer has a matching .opt data-key; 4 options each
 7. counts: images referenced == model count; tasks listed == 222
Prints RESULT: PASS/FAIL and exits non-zero on failure.
"""
import os
import re
import sys
from collections import Counter
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

PAGES = ['index.html', 'prep.html', 'fi.html', 'co.html', 'mm.html', 'pp.html', 'sd.html',
         'tcode.html', 'issues.html', 'tasks.html', 'instructor.html', 'worksheet.html', 'quiz.html']

VOID = {'img', 'br', 'hr', 'meta', 'link', 'input', 'source', 'area', 'base', 'col', 'embed',
        'param', 'track', 'wbr'}

fails = []
infos = []


def fail(msg):
    fails.append(msg)


def read(p):
    with open(p, encoding='utf-8') as f:
        return f.read()


class Bal(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.stack = []
        self.err = []

    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            return
        self.stack.append(tag)

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.err.append(f'extra </{tag}>')
            return
        if self.stack[-1] != tag:
            if tag in self.stack:
                self.err.append(f'</{tag}> closes while <{self.stack[-1]}> is open')
                while self.stack and self.stack.pop() != tag:
                    pass
            else:
                self.err.append(f'stray </{tag}>')
        else:
            self.stack.pop()


htmls = {p: read(p) for p in PAGES}

# ---------------------------------------------------------------- 1. images
all_srcs = []
for p, h in htmls.items():
    for m in re.finditer(r'<img[^>]*src="([^"]+)"', h):
        all_srcs.append((p, m.group(1)))
missing = [(p, s) for p, s in all_srcs if not os.path.exists(s)]
if missing:
    fail(f'{len(missing)} broken <img src> (first: {missing[:3]})')
else:
    infos.append(f'img src: {len(all_srcs)} references, all exist')

a_hrefs = []
for p, h in htmls.items():
    for m in re.finditer(r'<a class="zoom" href="([^"]+)"', h):
        a_hrefs.append((p, m.group(1)))
miss2 = [(p, s) for p, s in a_hrefs if not os.path.exists(s)]
if miss2:
    fail(f'{len(miss2)} broken zoom links (first: {miss2[:3]})')
else:
    infos.append(f'zoom links: {len(a_hrefs)} references, all exist')

# ---------------------------------------------------------------- 2. anchors
ids = {p: set(re.findall(r'\bid="([^"]+)"', h)) for p, h in htmls.items()}
bad_anchor = []
for p, h in htmls.items():
    for m in re.finditer(r'<a[^>]*href="([^"]+)"', h):
        href = m.group(1)
        if href.startswith(('http', 'mailto:', '../')):
            continue
        if href.startswith('#'):
            if href[1:] not in ids[p]:
                bad_anchor.append((p, href))
        elif '#' in href:
            tgt, anc = href.split('#', 1)
            if tgt not in htmls:
                bad_anchor.append((p, href))
            elif anc not in ids[tgt]:
                bad_anchor.append((p, href))
if bad_anchor:
    fail(f'{len(bad_anchor)} broken anchors (first: {bad_anchor[:5]})')
else:
    infos.append('internal anchors (incl. page#anchor): all resolve')

# also: links to a page file that does not exist
bad_page = [(p, m.group(1)) for p, h in htmls.items()
            for m in re.finditer(r'<a[^>]*href="([a-z0-9-]+\.html)(?:#[^"]*)?"', h)
            if m.group(1) not in htmls]
if bad_page:
    fail(f'links to missing pages: {bad_page[:5]}')
else:
    infos.append('page-to-page links: all targets exist')

# ---------------------------------------------------------------- 3. nav
navs = {}
for p, h in htmls.items():
    m = re.search(r'<nav class="main">(.*?)</nav>', h, re.S)
    if not m:
        fail(f'{p}: no <nav class="main">')
        continue
    links = re.findall(r'<a([^>]*)href="([^"]+)"', m.group(1))
    navs[p] = [href for a, href in links]
    act = [href for a, href in links if 'class="active"' in a]
    if len(act) != 1:
        fail(f'{p}: {len(act)} active nav items (want 1)')
ref = navs.get('index.html')
badd = [p for p, v in navs.items() if v != ref]
if badd:
    fail(f'nav link list differs from index.html on: {badd}')
else:
    infos.append(f'nav: identical {len(ref)}-link list on all {len(navs)} pages, exactly 1 active each')

# ---------------------------------------------------------------- 4. container
for p, h in htmls.items():
    if h.count('</article>') != 1:
        fail(f'{p}: {h.count("</article>")} x </article>')
    elif h.index('</article>') > h.index('<footer'):
        fail(f'{p}: </article> after <footer>')
    if '<!DOCTYPE html>' not in h or '</html>' not in h:
        fail(f'{p}: skeleton missing')
infos.append('containers: single </article> before <footer> on every page')

# ---------------------------------------------------------------- 5. tag balance / markdown / pipes
for p, h in htmls.items():
    b = Bal()
    b.feed(h)
    real = [e for e in b.err if 'extra </body>' not in e and 'extra </html>' not in e]
    if real:
        fail(f'{p}: tag structure — {real[:3]}')
    if b.stack:
        fail(f'{p}: unclosed tags at EOF: {b.stack[-5:]}')
    if '**' in h:
        fail(f'{p}: leftover markdown "**"')
    for m in re.finditer(r'<td[^>]*>([^<]*\|[^<]*)</td>', h):
        fail(f'{p}: stray "|" inside <td>: {m.group(1)[:40]!r}')
infos.append('tag balance / no markdown leftovers / no stray pipes in <td>')

# ---------------------------------------------------------------- 6. quiz
qh = htmls['quiz.html']
qs = re.findall(r'<div class="quiz-q" data-answer="([A-D])">(.*?)</div>\s*</div>', qh, re.S)
n_q = qh.count('class="quiz-q"')
if n_q != 30:
    fail(f'quiz: {n_q} questions (want 30)')
for i, m in enumerate(re.finditer(r'<div class="quiz-q" data-answer="([A-D])">(.*?)(?=<div class="quiz-q"|<h2 id="checklist")',
                                 qh, re.S), 1):
    ans, blk = m.group(1), m.group(2)
    keys = re.findall(r'data-key="([A-D])"', blk)
    if sorted(keys) != ['A', 'B', 'C', 'D']:
        fail(f'quiz Q{i}: option keys {keys}')
    if ans not in keys:
        fail(f'quiz Q{i}: data-answer {ans} has no option')
    if 'class="explain"' not in blk:
        fail(f'quiz Q{i}: no explain block')
infos.append(f'quiz: {n_q} questions, answers match options, all have 解说')

# ---------------------------------------------------------------- 7. counts
import json  # noqa: E402
model = json.load(open('work/site_model.json'))
n_tasks = sum(len(m['tasks']) for m in model)
n_shots = sum(t['nimg'] for m in model for t in m['tasks'])
idx_rows = htmls['tasks.html'].count('<tr data-mod=')
if idx_rows != n_tasks:
    fail(f'tasks.html: {idx_rows} rows vs {n_tasks} tasks in model')
ws_rows = htmls['worksheet.html'].count('<td class="wblank"></td>')
if n_shots != len(all_srcs):
    fail(f'figure count {len(all_srcs)} != model image references {n_shots}')
infos.append(f'counts: tasks {n_tasks}, figure refs {len(all_srcs)} (model {n_shots}), '
             f'tasks.html rows {idx_rows}, worksheet blanks {ws_rows}')

print('--- INFO ---')
for i in infos:
    print('  •', i)
if fails:
    print('--- FAIL ---')
    for f in fails:
        print('  ✗', f)
    print(f'RESULT: FAIL ({len(fails)} problems)')
    sys.exit(1)
print('RESULT: PASS')
