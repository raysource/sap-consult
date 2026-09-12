#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the curriculum model: modules -> tasks -> ordered steps(text + images)."""
import json, re, os
from collections import OrderedDict

b = json.load(open('work/doc_stream2.json'))
EX = 'work/docx_extract'
HEADS = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6}
NOTE = '马老师学习笔记'

def clean(t):
    t = t.replace('\u00a0', ' ').replace('\u3000', ' ')
    t = re.sub(r'[ \t]+', ' ', t)
    return t.strip()

modules = []
cur_mod = None
cur_task = None
for x in b:
    if x['t'] == 'tbl':
        rows = [[clean(c['text']) for c in r] for r in x['rows']]
        imgs = [im for r in x['rows'] for c in r for im in c['images']]
        if cur_task is not None:
            cur_task['blocks'].append({'kind': 'table', 'rows': rows,
                                       'imgs': [im['file'] for im in imgs]})
        continue
    if x['t'] != 'p':
        continue
    st = x.get('style')
    txt = clean(x['text'])
    numid = (x.get('num') or {}).get('numId')
    if numid == '4' or st in ('10', '20'):
        continue  # TOC
    imgs = [im['file'] for im in x.get('images', [])]
    is_note = txt.startswith(NOTE)
    if is_note:
        txt = clean(txt[len(NOTE):])
    if st in HEADS:
        lvl = HEADS[st]
        if lvl == 2:
            cur_mod = {'title': txt, 'tasks': [], 'tilvl': 2}
            modules.append(cur_mod)
            cur_task = None
            continue
        if lvl == 4:
            if cur_mod is None:
                cur_mod = {'title': 'MISC', 'tasks': []}
                modules.append(cur_mod)
            cur_task = {'title': txt, 'blocks': [], 'lvl': 4, 'notes': []}
            cur_mod['tasks'].append(cur_task)
            continue
        # H1/H3/H5/H6 -> sub block inside the task (or module-level)
        target = cur_task if cur_task is not None else None
        blk = {'kind': 'sub', 'level': lvl, 'text': txt, 'imgs': imgs, 'note': is_note}
        if target is not None:
            target['blocks'].append(blk)
        else:
            cur_mod.setdefault('blocks', []).append(blk)
        continue
    # body
    if not txt and not imgs:
        continue
    blk = {'kind': 'text', 'text': txt, 'imgs': imgs, 'note': is_note}
    if cur_task is not None:
        cur_task['blocks'].append(blk)
    elif cur_mod is not None:
        cur_mod.setdefault('blocks', []).append(blk)

# stats
print('modules:', len(modules))
tot_tasks = tot_imgs = 0
for m in modules:
    imgs = sum(len(bl.get('imgs', [])) for t in m['tasks'] for bl in t['blocks'])
    imgs += sum(len(bl.get('imgs', [])) for bl in m.get('blocks', []))
    tot_tasks += len(m['tasks'])
    tot_imgs += imgs
    print(f"  {m['title']}: tasks={len(m['tasks'])} imgs={imgs}")
print('TOTAL tasks', tot_tasks, 'imgs', tot_imgs)
json.dump(modules, open('work/curriculum.json', 'w'), ensure_ascii=False, indent=1)

# sample dump of one task
def dump(modname, taskname, limit=200):
    for m in modules:
        if modname in m['title']:
            for t in m['tasks']:
                if taskname in t['title']:
                    print(f"\n### {m['title']} / {t['title']}")
                    for i, bl in enumerate(t['blocks'][:limit]):
                        if bl['kind'] == 'table':
                            print(f"  [{i}] TABLE {bl['rows']}")
                        else:
                            tag = 'NOTE' if bl.get('note') else bl['kind']
                            print(f"  [{i}] <{tag}> {bl.get('text','')!r} imgs={[os.path.basename(x) for x in bl.get('imgs',[])]}")
                    return
dump('销售与分销', '创建销售订单')
dump('财务会计', '创建公司代码')
