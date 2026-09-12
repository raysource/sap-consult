#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build an outline: headings + image counts + T-code-ish tokens + first text lines."""
import json, re, sys
from collections import Counter, OrderedDict

b = json.load(open('work/doc_stream.json'))
HEADS = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6}
out = []
cur = []
for i, x in enumerate(b):
    if x['t'] == 'tbl':
        out.append({'i': i, 'lvl': 0, 'kind': 'table', 'text': f"<table {len(x['rows'])}x{len(x['rows'][0]) if x['rows'] else 0}>",
                    'imgs': sum(len(c['images']) for r in x['rows'] for c in r),
                    'rowtext': [[c['text'] for c in r] for r in x['rows']]})
        continue
    if x['t'] != 'p':
        continue
    st = x.get('style')
    txt = x['text'].strip()
    nimg = len(x['images'])
    if st in HEADS:
        out.append({'i': i, 'lvl': HEADS[st], 'kind': 'head', 'text': txt, 'imgs': nimg,
                    'num': x.get('num')})
    elif st in ('10', '20') or (x.get('num') or {}).get('numId') == '4':
        out.append({'i': i, 'lvl': 9, 'kind': 'toc', 'text': txt, 'imgs': nimg})
    elif txt or nimg:
        out.append({'i': i, 'lvl': 0, 'kind': 'body', 'text': txt, 'imgs': nimg})

print('outline entries:', len(out))
print(Counter((o['kind'], o['lvl']) for o in out))
json.dump(out, open('work/outline.json', 'w'), ensure_ascii=False)

# Print the heading tree (skip toc)
print('\n===== HEADING TREE =====')
idx = 0
for o in out:
    if o['kind'] == 'toc':
        continue
    if o['kind'] == 'head':
        print(f"{'  ' * (o['lvl'] - 1)}[{'H' + str(o['lvl'])}] {o['text']}   (imgs {o['imgs']})")
    elif o['kind'] == 'table':
        print(f"    <TABLE {len(o['rowtext'])}x{len(o['rowtext'][0]) if o['rowtext'] else 0}>")
