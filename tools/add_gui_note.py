#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
手顺ページの冒頭に「画面イメージは実機スクリーンショットではありません」の注意書きを入れる／外す（冪等）。

    python3 tools/add_gui_note.py sapmto            # 図があるページに注意書きを入れる
    python3 tools/add_gui_note.py sapmto --remove   # 全部外す
    python3 tools/add_gui_note.py sapmto --sync     # ページごとに自動判定：
                                                    #   生成 SVG が 1 枚でも残っていれば「入れる」
                                                    #   すべて実機画像(.png 等)に置き換わっていれば「外す」
    python3 tools/add_gui_note.py --all --sync      # 全サイト一括

実機スクリーンショットに差し替えたあと（tools/swap_gui_images.py <site> --apply）に --sync を実行すると、
注意書きの有無が実際のページ内容と一致します。
"""
import argparse
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
KNOWN = ["sap_sd", "sapmto", "sapeto", "sapmts", "sapvc", "saporderflow"]
PAGES = ["config.html", "handson-1.html", "handson-2.html", "handson-3.html",
         "handson-4.html", "handson-5.html", "compare.html", "scenario-eq.html", "vc.html"]
MARK = '<div class="gui-note" data-gui-note="1">'
NOTE = (MARK + '<b>关于本页的「画面イメージ」</b>：这些图是按 SAP GUI 标准布局重绘的'
        '<b>示意图</b>，不是实机截图。字段名、字段顺序、按钮位置会因版本与自定义而不同，'
        '请以自系统的画面为准（各 STEP 的「自系统での確認方法」里写了确认用的 T-code 与表）。'
        '若是想换成实机截图，把同名 <code>.png</code> 放进 <code>assets/gui/</code> 后执行 '
        '<code>python3 tools/swap_gui_images.py &lt;site&gt; --apply</code> 即可一键替换。</div>')


def has_svg_figure(src):
    return bool(re.search(r'src="assets/gui/[^"]+\.svg"', src, re.I))


def process(site, remove=False, sync=False):
    add = rem = 0
    for page in PAGES:
        p = os.path.join(ROOT, site, page)
        if not os.path.exists(p):
            continue
        s = open(p, encoding="utf-8").read()
        has_fig = '<figure class="gui">' in s
        if not has_fig:
            continue
        want = (not remove) and (has_svg_figure(s) if sync else True)
        present = MARK in s
        if want and not present:
            m = re.search(r"</h1>", s)
            if not m:
                continue
            s = s[:m.end()] + "\n" + NOTE + "\n" + s[m.end():]
            open(p, "w", encoding="utf-8").write(s)
            add += 1
        elif (not want) and present:
            s = re.sub(re.escape(MARK) + r".*?</div>\s*", "", s, flags=re.S)
            open(p, "w", encoding="utf-8").write(s)
            rem += 1
    print("%-14s %s: 追加 %d ページ / 削除 %d ページ" % (site, "sync" if sync else ("remove" if remove else "add"), add, rem))
    return add, rem


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sites", nargs="*")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--remove", action="store_true")
    ap.add_argument("--sync", action="store_true")
    a = ap.parse_args()
    sites = KNOWN if a.all else a.sites
    if not sites:
        sys.exit("usage: add_gui_note.py <site> […] | --all  [--remove | --sync]")
    for s in sites:
        if not os.path.isdir(os.path.join(ROOT, s)):
            print("skip (not found):", s)
            continue
        process(s, remove=a.remove, sync=a.sync)


if __name__ == "__main__":
    main()
