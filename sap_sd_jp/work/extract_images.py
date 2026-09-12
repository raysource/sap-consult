#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Copy docx media into assets/img/<mod>/t<NN>/ with semantic names.

- content-addressed dedupe (identical files referenced many times are stored once;
  the first (module, task, step) instance keeps the canonical path)
- drops icon-like images (w<90 or h<14) and records them for review
- writes work/curriculum_named.json (model with asset paths + dims) and work/images.json
"""
import json, os, re, shutil, hashlib, struct
from collections import OrderedDict

SRC = 'work/docx_extract/word/media'
DST = 'assets/img'
MODCODE = {'准备工作': 'prep', '财务会计 FI': 'fi', '管理会计 CO': 'co',
           '物料管理 MM': 'mm', '生产计划 PP（Production Plan）': 'pp',
           '销售与分销 SD': 'sd'}

def dims(p):
    with open(p, 'rb') as f:
        d = f.read(65536)
    if d[:8] == b'\x89PNG\r\n\x1a\n':
        return struct.unpack('>II', d[16:24])
    if d[:2] == b'\xff\xd8':
        i = 2
        full = open(p, 'rb').read()
        while i < len(full) - 9:
            if full[i] != 0xFF:
                i += 1
                continue
            m = full[i + 1]
            if m in (0xC0, 0xC1, 0xC2, 0xC3):
                h, w = struct.unpack('>HH', full[i + 5:i + 9])
                return w, h
            if m in (0xD8, 0xD9) or 0xD0 <= m <= 0xD7:
                i += 2
                continue
            i += 2 + struct.unpack('>H', full[i + 2:i + 4])[0]
    return None

mods = json.load(open('work/curriculum.json'))
byhash = {}
records = []
dropped = []
seq = 0
os.makedirs(DST, exist_ok=True)

for m in mods:
    code = MODCODE[m['title']]
    for ti, t in enumerate(m['tasks'], 1):
        tdir = f'{DST}/{code}/t{ti:02d}'
        stepno = 0
        for bl in t['blocks']:
            if not bl.get('imgs'):
                continue
            stepno += 1
            for ki, rel in enumerate(bl['imgs'], 1):
                src = 'work/docx_extract/' + rel
                if not rel or not os.path.exists(src):
                    dropped.append({'task': t['title'], 'file': rel, 'why': 'missing'})
                    continue
                d = dims(src)
                w, h = (d if d else (0, 0))
                if w < 90 or h < 14:
                    dropped.append({'task': t['title'], 'file': os.path.basename(rel), 'why': f'icon {w}x{h}'})
                    continue
                hh = hashlib.md5(open(src, 'rb').read()).hexdigest()
                seq += 1
                if hh in byhash:
                    path = byhash[hh]
                    dup = True
                else:
                    ext = os.path.splitext(rel)[1].lower()
                    name = f"{stepno:02d}_{ki}_{os.path.splitext(os.path.basename(rel))[0]}{ext}"
                    path = f'{code}/t{ti:02d}/{name}'
                    os.makedirs(tdir, exist_ok=True)
                    shutil.copy2(src, f'{DST}/{path}')
                    byhash[hh] = path
                    dup = False
                records.append({'seq': seq, 'module': m['title'], 'modcode': code,
                                'task': t['title'], 'taskno': ti, 'step': stepno,
                                'path': path, 'orig': os.path.basename(rel),
                                'w': w, 'h': h, 'dup': dup,
                                'bytes': os.path.getsize(src)})
                bl.setdefault('imgs_asset', []).append(path)

json.dump(mods, open('work/curriculum_named.json', 'w'), ensure_ascii=False, indent=1)
json.dump(records, open('work/images.json', 'w'), ensure_ascii=False, indent=1)

files = sorted(f"assets/img/{p}" for p in byhash.values())
tot = sum(os.path.getsize(f) for f in files)
print(f'refs={len(records)} unique_files={len(byhash)} dropped={len(dropped)} total={tot/1e6:.1f} MB')
from collections import Counter
print('dropped reasons:', Counter(d['why'].split()[0] for d in dropped))
print('dropped sample:', [d['file'] for d in dropped[:25]])

json.dump({'media_files_in_docx': len(os.listdir(SRC)),
           'refs_kept': len(records),
           'unique_files': len(byhash),
           'dropped_icons': len(dropped),
           'asset_bytes': tot,
           'dropped': dropped},
          open('work/images_summary.json', 'w'), ensure_ascii=False, indent=1)
