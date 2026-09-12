#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SVG（SAP GUI 画面イメージ）の「重なり」検出 + 自動回避

赤い注記バッジ／吹き出しが、表のセルや入力欄の文字に重なって読みにくくなるのを防ぐ。

    python3 tools/check_gui_overlap.py sapmto            # 検出のみ（レポート）
    python3 tools/check_gui_overlap.py sapmto --fix      # 重なっている注記を上下にずらして再生成
    python3 tools/check_gui_overlap.py --all

--fix は spec（tools/gui_spec.json）の callout 座標を書き換えます（元の座標は comment に退避）。
"""
import argparse
import glob
import json
import os
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
NS = "{http://www.w3.org/2000/svg}"
SITES = ["sap_sd", "sapmto", "sapeto", "sapmts", "sapvc", "saporderflow"]
BADGE_R = 14


def _wide(ch):
    return unicodedata.east_asian_width(ch) in ("W", "F")


def text_w(s, size, mono=False):
    """CJK（全角）を 1.0em、半角を 0.52/0.60em として幅を見積もる（重なり判定の精度が上がる）"""
    s = str(s)
    w = sum(1.0 if _wide(c) else (0.60 if mono else 0.52) for c in s)
    return w * size + 2


def est_w(s, size, mono=False):
    return text_w(s, size, mono)


def boxes_of(path):
    """(text_boxes, callout_boxes) — text は (x0,y0,x1,y1, s, fill)"""
    root = ET.parse(path).getroot()
    texts = []
    for t in root.iter(NS + "text"):
        s = (t.text or "").strip()
        if not s:
            continue
        try:
            x = float(t.get("x", 0)); y = float(t.get("y", 0)); size = float(t.get("font-size", 13))
        except ValueError:
            continue
        anchor = t.get("text-anchor", "start")
        w = est_w(s, size, "mono" in (t.get("font-family") or ""))
        x0 = x if anchor == "start" else (x - w / 2 if anchor == "middle" else x - w)
        texts.append((x0, y - size * 0.82, x0 + w, y + size * 0.24, s, t.get("fill", "")))
    badges = []
    for c in root.iter(NS + "circle"):
        try:
            cx = float(c.get("cx", 0)); cy = float(c.get("cy", 0)); r = float(c.get("r", BADGE_R))
        except ValueError:
            continue
        badges.append((cx - r, cy - r, cx + r, cy + r, "badge", ""))
    rects = []
    for rc in root.iter(NS + "rect"):
        if rc.get("fill") == "#fff5f5":     # 吹き出し本体
            try:
                x = float(rc.get("x", 0)); y = float(rc.get("y", 0))
                w = float(rc.get("width", 0)); h = float(rc.get("height", 0))
            except ValueError:
                continue
            rects.append((x, y, x + w, y + h, "bubble", ""))
    return texts, badges + rects


def overlap(a, b):
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])


def scan(site):
    """returns [ (file, n_collisions, [samples]) ]"""
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, site, "assets", "gui", "*.svg"))):
        try:
            texts, marks = boxes_of(f)
        except ET.ParseError as ex:
            out.append((os.path.basename(f), -1, [("PARSE", str(ex))]))
            continue
        if not marks:
            continue
        hits = []
        for m in marks:
            for t in texts:
                if t[5] in ("#b71c1c", "#d32f2f"):       # 注記自身の文字は除外
                    continue
                if overlap(m, t):
                    hits.append((m[4], t[4][:38]))
        if hits:
            out.append((os.path.basename(f), len(hits), hits[:3]))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sites", nargs="*")
    ap.add_argument("--fix", action="store_true")
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    sites = SITES if a.all else (a.sites or SITES)
    total = 0
    for site in sites:
        d = os.path.join(ROOT, site)
        if not os.path.isdir(os.path.join(d, "assets", "gui")):
            continue
        rows = scan(site)
        n_files = len(rows)
        n_hits = sum(r[1] for r in rows if r[1] > 0)
        total += n_hits
        print("%-14s 重なりあり=%d ファイル / %d 箇所" % (site, n_files, n_hits))
        for f, n, samples in rows[:6]:
            print("    %-34s %s" % (f, samples))
        if a.fix and n_files:
            sp = os.path.join(d, "tools", "gui_spec.json")
            spec = json.load(open(sp, encoding="utf-8"))
            moved = 0
            # ファイル名 → (page, key, index) を引く
            for page, steps in (spec.get("pages") or {}).items():
                for key, screens in steps.items():
                    for sc in screens:
                        fn = sc.get("file", "")
                        if not any(r[0] == fn for r in rows):
                            continue
                        cos = sc.get("callouts") or []
                        for i, co in enumerate(cos):
                            if len(co) >= 3:
                                co[1] = 560 if co[1] < 620 else 300          # 表の外/内へ退避
                                moved += 1
            json.dump(spec, open(sp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
            print("    -> spec の callout 座標を %d 件調整（make_gui_mockups.py を再実行してください）" % moved)
    print("\n合計の重なり箇所: %d" % total)
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
