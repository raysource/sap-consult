#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, re
from collections import Counter
b = json.load(open('work/doc_stream.json'))
print('blocks', len(b))
imgblocks = [x for x in b if x['t'] == 'p' and x['images']]
print('blocks with images:', len(imgblocks))
tot = sum(len(x['images']) for x in imgblocks)
print('total image refs:', tot)
print('styles:', Counter(x.get('style') for x in b if x['t'] == 'p').most_common(30))
print('--- first 60 blocks ---')
for x in b[:60]:
    if x['t'] == 'p':
        print(f"[p d{x['d']} st={x.get('style')} n={x.get('num')}] {x['text'][:160]!r} imgs={len(x['images'])}")
    else:
        print(f"[{x['t']} d{x['d']}] rows={len(x['rows'])}")
print('--- image block sample ---')
for x in imgblocks[:5]:
    print(x['path'], x['text'][:80], json.dumps(x['images'])[:400])
print('--- last 30 blocks ---')
for x in b[-30:]:
    if x['t'] == 'p':
        print(f"[p d{x['d']} st={x.get('style')}] {x['text'][:160]!r} imgs={len(x['images'])}")
    else:
        print(f"[{x['t']}] rows={len(x['rows'])}")
