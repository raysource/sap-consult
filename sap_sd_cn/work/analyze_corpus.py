#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Corpus analysis: IMG paths, T-codes, step quality."""
import json, re, os
from collections import Counter

mods = json.load(open('work/curriculum.json'))
paras = []
for m in mods:
    for t in m['tasks']:
        for bl in t['blocks']:
            paras.append((m['title'], t['title'], bl))
    for bl in m.get('blocks', []):
        paras.append((m['title'], '<module>', bl))
texts = [bl.get('text', '') for _, _, bl in paras if bl['kind'] in ('text', 'sub')]
print('paragraphs:', len(texts), 'nonempty:', sum(1 for t in texts if t.strip()))
print('with images:', sum(1 for _, _, bl in paras if bl.get('imgs')))
print('empty-text image paras:', sum(1 for _, _, bl in paras if bl.get('imgs') and not bl.get('text', '').strip()))

# menu paths (Japanese/Chinese full-width dash separated)
paths = [t for t in texts if t.count('－') >= 2 or t.count('->') >= 2 or t.count('→') >= 2]
print('\nmenu-path-looking paras:', len(paths))
for p in paths[:12]:
    print('   ', p[:120])

# SPRO image hints
spro = [t for t in texts if 'SPRO' in t or 'spro' in t]
print('\nSPRO mentions:', len(spro))
for p in spro[:8]:
    print('   ', p[:140])

TC = re.compile(r'(?<![A-Za-z0-9])([A-Z]{2,5}[0-9]{2,3}[A-Z]?|[A-Z]{3,5})(?![A-Za-z0-9])')
STOP = set('''SAP SPRO IMG RMB CNY USD EUR CN ZH MRP BOM FI CO MM PP SD HR ABAP IDES EHP SAPGUI GUI PDF EXCEL JPEG PNG PN
OK NG NO YES AA AB BC CD DE IT IS TO IN ON OR IF SO WE HE BY ID IP URL HTTP WWW ISO CIF FOB DDP EXW FCA CPT CIP DAP
KMAT MTO MTS ETO VC ATO PIR QM PM PS WM IM EWM WM CO PA PC CS LO BSX WRX GBB PRD KDM VBRK MSEG MARC MARA VBAK VBAP
LIPS LIKP VBRP BKPF BSEG BSID BSIK KNA1 LFA1 MSTA MAST STKO PLKO PLPO AUFK AFKO AUFP RESB AFRU COEP COSP COSS
F999 R999 A999 C999 P999 003 T001 T001K T001W T001L T024 T024E T024W T024D T024F T024L T134 T134M T023 T023T
MMSC EKPO EKKO EKBE EKET EKAB EINE EINA EORD EBAN EKAN RKWA MPOP MARC MBEW MARD MCHB MSKA MSLB
'''.split())
cands = Counter()
for t in texts:
    for mm in TC.finditer(t):
        cands[mm.group(1)] += 1
known = [c for c in cands if re.search(r'[0-9]', c) or c in STOP or len(c) == 4]
print('\nT-code-like tokens (top 80):')
print(sorted([(c, n) for c, n in cands.items() if c not in STOP], key=lambda x: -x[1])[:80])
