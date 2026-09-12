#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Parse S4.docx document.xml -> ordered stream of blocks (heading/para/list/table/image).

Stdlib only. Walks <w:p>, <w:tbl>, and captures <w:drawing>/<a:blip r:embed> image refs
plus <wp:docPr name/descr> captions, and the drawing's extent (size in EMU).
"""
import re, json, sys, os
from xml.etree import ElementTree as ET

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
R = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'
A = '{http://schemas.openxmlformats.org/drawingml/2006/main}'
WP = '{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}'
V = '{urn:schemas-microsoft-com:vml}'

SRC = sys.argv[1] if len(sys.argv) > 1 else 'work/docx_extract/word/document.xml'
OUT = sys.argv[2] if len(sys.argv) > 2 else 'work/doc_stream.json'

print('parsing', SRC, os.path.getsize(SRC) / 1e6, 'MB')
raw = open(SRC, 'rb').read()

# strip the huge base64/embedded parts? none in document.xml. Parse with iterparse.
tree = ET.fromstring(raw)
print('root', tree.tag)

def para_text(p):
    """Concatenate w:t, mark tabs/breaks."""
    out = []
    for node in p.iter():
        if node.tag == W + 't':
            out.append(node.text or '')
        elif node.tag == W + 'tab':
            out.append('\t')
        elif node.tag == W + 'br':
            out.append('\n')
        elif node.tag == W + 'cr':
            out.append('\n')
    return ''.join(out)

def para_style(p):
    ppr = p.find(W + 'pPr')
    name = None
    if ppr is not None:
        ps = ppr.find(W + 'pStyle')
        if ps is not None:
            name = ps.get(W + 'val')
    return name

def para_num(p):
    ppr = p.find(W + 'pPr')
    if ppr is None:
        return None
    npr = ppr.find(W + 'numPr')
    if npr is None:
        return None
    ilvl = npr.find(W + 'ilvl')
    nid = npr.find(W + 'numId')
    return {'ilvl': ilvl.get(W + 'val') if ilvl is not None else None,
            'numId': nid.get(W + 'val') if nid is not None else None}

def images_in(el):
    imgs = []
    for blip in el.iter(A + 'blip'):
        rid = blip.get(R + 'embed')
        if rid:
            imgs.append({'rid': rid, 'kind': 'blip'})
    for im in el.iter(V + 'imagedata'):
        rid = im.get(R + 'id')
        if rid:
            imgs.append({'rid': rid, 'kind': 'vml'})
    # docPr caption / size
    caps = []
    for dp in el.iter(WP + 'docPr'):
        caps.append({'name': dp.get('name'), 'descr': dp.get('descr')})
    sizes = []
    for ext in el.iter(WP + 'extent'):
        try:
            sizes.append({'cx': int(ext.get('cx')), 'cy': int(ext.get('cy'))})
        except (TypeError, ValueError):
            pass
    for i, im in enumerate(imgs):
        im['docPr'] = caps[i] if i < len(caps) else (caps[0] if caps else {})
        im['extent'] = sizes[i] if i < len(sizes) else (sizes[0] if sizes else {})
    return imgs

blocks = []
body = tree.find(W + 'body')
print('top-level children:', len(list(body)))

def walk(container, depth, path):
    for idx, ch in enumerate(container):
        if ch.tag == W + 'p':
            txt = para_text(ch)
            imgs = images_in(ch)
            blocks.append({'t': 'p', 'd': depth, 'path': path + [idx], 'text': txt,
                           'style': para_style(ch), 'num': para_num(ch), 'images': imgs})
        elif ch.tag == W + 'tbl':
            rows = []
            for tr in ch.findall(W + 'tr'):
                cells = []
                for tc in tr.findall(W + 'tc'):
                    ctext = '\n'.join(para_text(p) for p in tc.findall(W + 'p'))
                    cimgs = images_in(tc)
                    cells.append({'text': ctext, 'images': cimgs})
                rows.append(cells)
            blocks.append({'t': 'tbl', 'd': depth, 'path': path + [idx], 'rows': rows})
        elif ch.tag == W + 'sdt':
            content = ch.find(W + 'sdtContent')
            if content is not None:
                walk(content, depth + 1, path + [idx])
        elif ch.tag == W + 'sectPr':
            blocks.append({'t': 'sect', 'path': path + [idx]})

walk(body, 0, [])
print('blocks:', len(blocks))
from collections import Counter
print(Counter(b['t'] for b in blocks))
json.dump(blocks, open(OUT, 'w'), ensure_ascii=False)
print('wrote', OUT, os.path.getsize(OUT) / 1e6, 'MB')
