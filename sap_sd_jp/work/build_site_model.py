#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Turn curriculum_named.json into the final rendering model: modules -> tasks -> steps.

v2: strips note prefixes before path detection, removes the path line from the
description list, detects 入力値 (field + value) lines, keeps sub-headings, and
writes work/site_model.json.
"""
import json, re, os
from collections import OrderedDict, Counter

mods = json.load(open('work/curriculum_named.json'))
NOTE_PREFIX = re.compile(r'^(?:马老师学习笔记)+')
PATH_SPLIT = re.compile(r'\s*(?:－|->|→|—|–|＞|>)\s*')
FB_MARK = re.compile(r'^(前台|后台|前台操作|后台配置)[（(]?.*$')

def note_kind(t):
    if re.search(r'问题|错误|不允许|不能|无法|失败|解决|报错|无效|不存在|警告', t):
        return 'warn'
    if t.startswith('解释') or t.startswith('说明') or t.startswith('注意'):
        return 'info'
    return 'tip'


def weird_ratio(t):
    """Share of characters that cannot be real Chinese/SAP text (OCR garble detector)."""
    t = t.strip()
    if not t:
        return 0.0
    w = 0
    for c in t:
        o = ord(c)
        if c == '\ufffd':
            w += 1
        elif o < 0x80:
            if not (c.isalnum() or c in ' .,:;!?-()/%+*=<>#$&@[]{}"\'+/'):
                w += 1
        elif not (0x3000 <= o <= 0x303f or 0x4e00 <= o <= 0x9fff or 0xff00 <= o <= 0xffef
                  or 0x2100 <= o <= 0x27ff
                  or o in (0x2018, 0x2019, 0x201c, 0x201d, 0x2014, 0x2026, 0x00b7, 0x00a0)):
            w += 1
    return w / len(t)


def looks_garbled(t):
    """OCR garble from the scanned tail page: mostly ASCII/punctuation, no CJK at all."""
    t = t.strip()
    if not t:
        return False
    if any(0x4e00 <= ord(c) <= 0x9fff for c in t):
        return False
    if len(t) < 10:
        return False
    ok = sum(1 for c in t if c.isalnum() or c in ' .,:;()/%-+=<>#&@[]{}"\'*')
    return (ok / len(t)) < 0.85


def strip_note(t):
    return NOTE_PREFIX.sub('', t or '').strip()

def looks_like_path(t):
    return len(PATH_SPLIT.split(t)) >= 3 and len(t) < 170

def clean_path(t):
    t = re.sub(r'^路径[:：]?\s*', '', strip_note(t))
    parts = [p.strip(' ，,、。') for p in PATH_SPLIT.split(t) if p.strip()]
    return ' → '.join(parts)

STOP = set('''SAP SPRO IMG RMB CNY USD EUR CN ZH MRP BOM FI CO MM PP SD HR ABAP IDES EHP GUI PDF Excel
OK NG NO YES AA AB BC CD DE IT IS TO IN ON OR IF SO WE HE BY ID IP URL HTTP WWW ISO CIF FOB DDP EXW FCA CPT CIP DAP
KMAT MTO MTS ETO VC ATO PIR QM PM PS WM IM EWM PA PC CS LO PRD ALR SET MIN MAX CN01
F999 R999 A999 C999 P999 T001 T001K T001W T001L T024 T024E T024W T024D T024F T024L
T134 T134M T023 T023T T134G T156 T156X T156S T157 T685 T685A T685B T681 T681A T681V
MMSC EKPO EKKO EKBE EKET EKAB EINE EINA EORD EBAN EKAN RKWA MPOP MARC MBEW MARD MCHB MSKA MSLB
MWST RAA ZRAA VAX PRI CTRL RENT PMKT GROFF LAB BSX WRX GBB MFG MPS BSA TCODE
PR00 HAWA ROH FERT FTTY HERS NLAG DIEN VERP KDM ZEXP ZGBS ZMMA ZREV
VBRK VBAP MSEG MARA MSTA MAST STKO PLKO PLPO AUFK AFKO RESB AFRU COEP COSP COSS
CODE COPY CLIENT UI114 WJ14 FS217 TCODE SAPGUI RKUPD RK811UPD RK811XUP SE38
'''.split())
TCODE_RE = re.compile(r'(?<![A-Za-z0-9_])([A-Z]{2,6}[0-9]{2,3}[A-Z]?|[A-Z]{4,6})(?![A-Za-z0-9_])')

def tcodes_in(texts):
    found = OrderedDict()
    for t in texts:
        for mm in TCODE_RE.finditer(t):
            c = mm.group(1)
            if c in STOP or c in found:
                continue
            if re.fullmatch(r'[A-Z]{4,6}', c) or re.search(r'[0-9]', c):
                found[c] = True
    return list(found)

VAL_RE = re.compile(r'^([\u4e00-\u9fffA-Za-z（）()/\-＋+ ]{2,22})\s+([A-Za-z0-9][A-Za-z0-9/\-\.]{0,28})$')
def is_value_line(t):
    if not VAL_RE.match(t):
        return False
    if looks_like_path(t) or t.endswith('，') or t.endswith(','):
        return False
    if len(t) > 60:
        return False
    return True

out = []
for m in mods:
    tasks = []
    for ti, t in enumerate(m['tasks'], 1):
        desc, notes, steps, subs, values = [], [], [], [], []
        pending, cur = [], None
        fb = None
        alltext = []
        path_cands = []

        def addnote(body, after):
            body = (body or '').strip()
            if not body:
                return
            if looks_like_path(body):
                path_cands.append(body)
                return
            notes.append({'kind': note_kind(body), 'text': body, 'after': after})

        for bl in t['blocks']:
            if bl['kind'] == 'table':
                subs.append({'kind': 'table', 'rows': bl['rows'],
                             'imgs': bl.get('imgs_asset', bl.get('imgs', []))})
                cur = None
                pending = []
                continue
            raw = (bl.get('text') or '').strip()
            txt = strip_note(raw)
            imgs = bl.get('imgs_asset', [])
            is_note = raw.startswith('马老师学习笔记') or bl.get('note')
            if txt:
                alltext.append(txt)
            if is_note:
                if imgs:
                    steps.append({'caption': txt, 'note': True, 'imgs': imgs})
                    cur = None
                else:
                    addnote(txt, len(steps))
                continue
            if bl['kind'] == 'sub' and txt:
                subs.append({'kind': 'head', 'level': bl.get('level', 5), 'text': txt})
                cur = None
                if imgs:
                    steps.append({'caption': txt, 'imgs': imgs})
                continue
            if imgs:
                cap = '\n'.join(pending).strip() if pending else txt
                if not cap and cur is not None and cur.get('mergeable'):
                    cur['imgs'].extend(imgs)
                else:
                    cur = {'caption': cap, 'imgs': list(imgs), 'mergeable': not cap}
                    steps.append(cur)
                pending = []
            elif txt:
                if FB_MARK.match(txt) and len(txt) <= 12:
                    fb = FB_MARK.match(txt).group(1)
                    continue
                if is_value_line(txt):
                    mm2 = VAL_RE.match(txt)
                    values.append({'k': mm2.group(1).strip(), 'v': mm2.group(2).strip()})
                    continue
                pending.append(txt)
                if len(pending) > 2:
                    desc.append(pending[0])
                    pending = pending[1:]
        # the source doc's tail section is a scanned page: a RUN of non-CJK OCR garble.
        # Drop such runs, but keep an isolated English line (e.g. "T-CODE OBYC").
        def no_cjk(x):
            return not any(0x4e00 <= ord(c) <= 0x9fff for c in x)

        if len([x for x in desc if no_cjk(x)]) >= 3:
            desc = [x for x in desc if not no_cjk(x)]
        if len([s for s in steps if s['caption'] and no_cjk(s['caption'])]) >= 3:
            for s in steps:
                if s['caption'] and no_cjk(s['caption']):
                    s['caption'] = ''
        if pending:
            for p in pending:
                addnote(p, len(steps))
        path = None
        for cand in [strip_note(x) for x in alltext[:8]] + path_cands:
            if looks_like_path(cand):
                path = clean_path(cand)
                break
        desc = [d for d in desc if not looks_like_path(d)]
        tasks.append({
            'no': ti, 'title': strip_note(re.sub(r'^马老师学习笔记', '', t['title'])),
            'anchor': f't{ti:02d}', 'desc': desc, 'notes': notes, 'steps': steps,
            'subs': subs, 'path': path, 'tcodes': tcodes_in(alltext), 'values': values,
            'fb': fb,
            'nimg': sum(len(s['imgs']) for s in steps) + sum(len(s.get('imgs', [])) for s in subs),
        })
    out.append({'title': m['title'], 'tasks': tasks, 'blocks': m.get('blocks', [])})

CODE = {'准备工作': 'prep', '财务会计 FI': 'fi', '管理会计 CO': 'co', '物料管理 MM': 'mm',
        '生产计划 PP（Production Plan）': 'pp', '销售与分销 SD': 'sd'}
for m in out:
    m['code'] = CODE[m['title']]

json.dump(out, open('work/site_model.json', 'w'), ensure_ascii=False, indent=1)

print('modules', len(out), 'tasks', sum(len(m['tasks']) for m in out),
      'steps', sum(len(t['steps']) for m in out for t in m['tasks']),
      'imgs', sum(t['nimg'] for m in out for t in m['tasks']))
print('paths', sum(1 for m in out for t in m['tasks'] if t['path']),
      'tcodes', sum(1 for m in out for t in m['tasks'] if t['tcodes']),
      'values', sum(len(t['values']) for m in out for t in m['tasks']))
print('steps with caption', sum(1 for m in out for t in m['tasks'] for s in t['steps'] if s['caption']))
print('steps without caption', sum(1 for m in out for t in m['tasks'] for s in t['steps'] if not s['caption']))

def show(modcode, taskno, maxsteps=20):
    m = [x for x in out if x['code'] == modcode][0]
    t = m['tasks'][taskno - 1]
    print(f"\n===== [{m['title']}] {t['no']:02d}. {t['title']}  (imgs {t['nimg']}, tcode {t['tcodes']})")
    print('  PATH:', t['path'])
    print('  VALUES:', t['values'][:8])
    for d in t['desc'][:4]:
        print('  DESC:', d[:140])
    for i, s in enumerate(t['steps'][:maxsteps], 1):
        print(f"  STEP{i}: {s['caption'][:140]!r} imgs={len(s['imgs'])}")
    for s in t['subs'][:4]:
        print('  SUB:', s)
    if t['notes']:
        print('  NOTES:', [n[:70] for n in t['notes'][:5]])

for args in [('fi', 1), ('fi', 12), ('co', 20), ('mm', 30), ('mm', 34), ('pp', 30), ('pp', 45), ('sd', 33), ('sd', 42), ('prep', 1)]:
    show(*args)
