#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Resolve rIds -> media files, attach sizes, build a per-task step model."""
import json, re, os, sys
from xml.etree import ElementTree as ET

EX = 'work/docx_extract'
rels = ET.fromstring(open(f'{EX}/word/_rels/document.xml.rels', 'rb').read())
RMAP = {}
for r in rels:
    RMAP[r.get('Id')] = r.get('Target')

b = json.load(open('work/doc_stream.json'))
HEADS = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6}

for x in b:
    if x['t'] != 'p':
        continue
    for im in x.get('images', []):
        tgt = RMAP.get(im['rid'], '')
        im['file'] = 'word/' + tgt if tgt else None

json.dump(b, open('work/doc_stream2.json', 'w'), ensure_ascii=False)
print('resolved. missing:', sum(1 for x in b if x['t'] == 'p' for i in x.get('images', []) if not i.get('file')))

# size stats
sizes = {}
for x in b:
    if x['t'] != 'p':
        continue
    for im in x.get('images', []):
        f = f"{EX}/{im['file']}"
        if im['file'] and os.path.exists(f):
            sizes[im['file']] = os.path.getsize(f)
print('unique media used:', len(sizes), 'total MB', round(sum(sizes.values()) / 1e6, 1))
allmedia = os.listdir(f'{EX}/word/media')
print('media files on disk:', len(allmedia))
print('used by doc:', sum(1 for f in allmedia if 'word/media/' + f in sizes) if False else len(sizes))
