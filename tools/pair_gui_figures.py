#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
E / Q 対比の図を 2 カラムに並べる（比較サイト用の後処理）

`make_gui_mockups.py` が挿入した `<figure class="gui">` のうち、キャプションが
「【E】…」「【Q】…」で始まるものを連続 2 枚ずつ `<div class="gui-pair">` で包み、
2 カラム表示にします（冪等：実行のたびに包み直すので、生成器を再実行しても壊れません）。

    python3 tools/pair_gui_figures.py saporderflow
"""
import argparse
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
PAGES = ["compare.html", "scenario-eq.html", "vc.html", "index.html"]

CSS = """
/* === E / Q 対比（2 カラム） ============================================= */
div.gui-pair { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 18px 0 22px; }
div.gui-pair figure.gui { margin: 0; }
div.gui-pair figure.gui figcaption { font-size: 12px; }
div.gui-pair figure.gui .gui-legend li { font-size: 12px; }
@media (max-width: 980px) { div.gui-pair { grid-template-columns: 1fr; } }
"""

WRAP_RE = re.compile(r'<div class="gui-pair">\s*((?:<figure class="gui">.*?</figure>\s*)+)</div>', re.S)
FIG_RE = re.compile(r'<figure class="gui">.*?</figure>', re.S)


def caption_of(fig):
    m = re.search(r'<figcaption><b class="t">(.*?)</b>', fig, re.S)
    return m.group(1) if m else ""


def unwrap(s):
    return WRAP_RE.sub(lambda m: m.group(1).strip(), s)


def wrap(s):
    """連続する 【E】→【Q】 の figure を 2 カラム用に包む。
    位置を先に全部集めてから 1 パスで組み立てる（挿入しながら走査するとオフセットがずれる）。"""
    figs = [(m.start(), m.end(), caption_of(m.group(0))) for m in FIG_RE.finditer(s)]
    pairs, i = [], 0
    while i < len(figs) - 1:
        a, b = figs[i], figs[i + 1]
        if a[2].startswith("【E】") and b[2].startswith("【Q】") and not s[a[1]:b[0]].strip():
            pairs.append((a[0], b[1]))
            i += 2
        else:
            i += 1
    if not pairs:
        return s, 0
    out, prev = [], 0
    for st, en in pairs:
        out.append(s[prev:st])
        out.append('<div class="gui-pair">\n' + s[st:en] + "\n</div>")
        prev = en
    out.append(s[prev:])
    return "".join(out), len(pairs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("site")
    a = ap.parse_args()
    site_dir = os.path.join(ROOT, a.site)
    total = 0
    for page in PAGES:
        p = os.path.join(site_dir, page)
        if not os.path.exists(p):
            continue
        s = open(p, encoding="utf-8").read()
        if '<figure class="gui">' not in s:
            continue
        s = unwrap(s)
        s, n = wrap(s)
        open(p, "w", encoding="utf-8").write(s)
        total += n
        print("%-18s pair %d" % (page, n))
    css = None
    for cand in ("cmp.css", "mto.css", "eto.css", "mts.css", "vc.css"):
        cp = os.path.join(site_dir, "assets", cand)
        if os.path.exists(cp):
            css = cp
            break
    if css:
        c = open(css, encoding="utf-8").read()
        marker = "/* === E / Q 対比（2 カラム）"
        if marker in c:
            c = c[:c.index(marker)].rstrip() + "\n"
        open(css, "w", encoding="utf-8").write(c.rstrip() + "\n" + CSS)
        print("css:", os.path.relpath(css, ROOT))
    print("pair total: %d" % total)


if __name__ == "__main__":
    main()
