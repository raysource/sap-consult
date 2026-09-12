#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
実機スクリーンショット差し替えツール（撮影した画像をページに反映する）

    1) 撮影リスト（<CODE>_画面撮影リスト.xlsx）を見ながら実機で撮る
    2) 撮った画像を <site>/assets/gui/ に「差し替え後」の名前で置く
       （例: config_s01_1.png ← 撮影リストの『差し替え後』列のとおり）
    3) このスクリプトで一括差し替え:

       python3 tools/swap_gui_images.py <site> --status     # いま何枚が実機画像か（進行状況）
       python3 tools/swap_gui_images.py <site>              # dry-run（何が変わるか表示）
       python3 tools/swap_gui_images.py <site> --apply       # src を .svg → .png に書き換え
       python3 tools/swap_gui_images.py <site> --revert      # .svg に戻す（元の生成図に戻す）

  差し替え後は `python3 tools/add_gui_note.py <site> --sync` を実行すると、
  「実機スクリーンショットではありません」の注意書きが**実機画像に置き換わったページから自動で外れます**。

対応形式: .png / .jpg / .jpeg / .webp（大文字拡張子も可）。PNG/JPEG は縦横比を検査し、
1180×760 と大きく違う場合は警告します（CSS は幅合わせなので表示は崩れませんが、
縦長のスクリーンショットは見づらくなります）。
"""
import argparse
import os
import re
import struct
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
PAGES = ["index.html", "concept.html", "config.html", "handson-1.html", "handson-2.html",
         "handson-3.html", "handson-4.html", "handson-5.html", "instructor.html",
         "worksheet.html", "quiz.html", "compare.html", "scenario-eq.html", "vc.html"]
CANVAS = (1180, 760)
EXTS = ["png", "jpg", "jpeg", "webp"]


def png_size(fp):
    with open(fp, "rb") as f:
        b = f.read(33)
    if len(b) < 24 or b[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    w, h = struct.unpack(">II", b[16:24])
    return w, h


def jpg_size(fp):
    with open(fp, "rb") as f:
        data = f.read()
    i = 2
    while i + 9 < len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        m = data[i + 1]
        if m in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            h, w = struct.unpack(">HH", data[i + 5:i + 9])
            return w, h
        if m in (0xD8, 0xD9) or 0xD0 <= m <= 0xD7:
            i += 2
            continue
        ln = struct.unpack(">H", data[i + 2:i + 4])[0]
        i += 2 + ln
    return None


def image_size(fp):
    e = fp.lower().rsplit(".", 1)[-1]
    try:
        if e == "png":
            return png_size(fp)
        if e in ("jpg", "jpeg"):
            return jpg_size(fp)
    except Exception:
        return None
    return None


def find_replacement(gdir, base, prefer):
    for e in ([prefer] + [x for x in EXTS if x != prefer]):
        p = os.path.join(gdir, "%s.%s" % (base, e))
        if os.path.exists(p):
            return "%s.%s" % (base, e), p
    return None, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("site")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--revert", action="store_true")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--prefer", default="png", choices=EXTS, help="同じベース名に複数形式がある場合の優先形式")
    ap.add_argument("--min-px", type=int, default=800, help="これより幅が小さい画像は警告（既定 800px）")
    a = ap.parse_args()
    site_dir = os.path.join(ROOT, a.site)
    gdir = os.path.join(site_dir, "assets", "gui")
    if not os.path.isdir(gdir):
        sys.exit("no gui dir: %s" % gdir)
    src_ext, dst_ext = ("svg", a.prefer) if not a.revert else (a.prefer, "svg")

    todo, missing, warn = {}, [], []
    for page in PAGES:
        p = os.path.join(site_dir, page)
        if not os.path.exists(p):
            continue
        s = open(p, encoding="utf-8").read()
        hits = sorted(set(re.findall(r'src="assets/gui/([^"?]+)\.%s"' % src_ext, s, re.I)))
        if not hits:
            continue
        conv = []
        for base in hits:
            new, path = find_replacement(gdir, base, dst_ext)
            if not new:
                missing.append((page, base + "." + dst_ext))
                continue
            sz = image_size(path)
            if sz:
                w, h = sz
                if w < a.min_px:
                    warn.append((page, new, "幅 %dpx は小さい（拡大表示で粗くなります）" % w))
                elif abs((w / h) - (CANVAS[0] / CANVAS[1])) / (CANVAS[0] / CANVAS[1]) > 0.35:
                    warn.append((page, new, "縦横比 %dx%d は 1180x760 と大きく違う（縦長スクリーンショット？）" % (w, h)))
            conv.append((base + "." + src_ext, new))
        if conv:
            todo[page] = conv

    n_all = sum(len(v) for v in todo.values())
    if a.status:
        if not todo:
            print("%s: 実機画像に差し替え済み 0 枚（すべて生成 SVG の状態）" % a.site)
            return
        print("%s: 実機画像に差し替えできる（＝同ベース名の画像がある）: %d 枚" % (a.site, n_all))
        for page, conv in todo.items():
            print("   %-20s %d 枚" % (page, len(conv)))
        return

    for page, conv in todo.items():
        print("%-20s %d 枚" % (page, len(conv)))
        for old, new in conv:
            print("    %s  ->  %s" % (old, new))
    if missing:
        print("\n未配置（同ベース名の .%s がまだ無い）: %d 枚" % (dst_ext, len(missing)))
        for page, f in missing[:8]:
            print("    %s : %s" % (page, f))
        if len(missing) > 8:
            print("    … 他 %d 枚" % (len(missing) - 8))
    for page, f, msg in warn:
        print("  [警告] %s / %s : %s" % (page, f, msg))
    if not (a.apply or a.revert):
        print("\n(dry-run) 実行するには --apply（戻すときは --revert）")
        return

    n = 0
    for page, conv in todo.items():
        p = os.path.join(site_dir, page)
        s = open(p, encoding="utf-8").read()
        for old, new in conv:
            s = s.replace('src="assets/gui/%s"' % old, 'src="assets/gui/%s"' % new)
            n += 1
        open(p, "w", encoding="utf-8").write(s)
    print("\n差し替えました: %d 枚（%s → %s）" % (n, src_ext, dst_ext))
    if n and not a.revert:
        print("次に: python3 tools/add_gui_note.py %s --sync   # 実機画像に置き換わったページの注意書きを自動で外す" % a.site)


if __name__ == "__main__":
    main()
