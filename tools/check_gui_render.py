#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SVG（SAP GUI 画面イメージ）が実際に絵として描けているかを検証する。

Chrome headless で SVG → PNG にラスタライズし、PNG を純 Python（zlib）でデコードして
領域ごとのピクセル統計を見る。画像を目視できない環境でも「真っ白」「崩れ」を検出できる。

    python3 tools/check_gui_render.py sapmto            # 全 SVG
    python3 tools/check_gui_render.py sapmto --limit 3  # 先頭 3 枚だけ

判定:
  ・タイトルバー（上部 32px）に濃色ピクセルがあること
  ・本文（中段）の非背景ピクセルが 0.5% 以上あること
  ・ステータスバー（下部 34px）が描かれていること
  ・callouts がある SVG では赤系ピクセルが存在すること
"""
import argparse
import glob
import os
import re
import struct
import subprocess
import sys
import tempfile
import zlib

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def read_png(path):
    data = open(path, "rb").read()
    assert data[:8] == b"\x89PNG\r\n\x1a\n", "not png"
    pos, w, h, idat = 8, 0, 0, b""
    bd = ct = None
    while pos < len(data):
        (ln,) = struct.unpack(">I", data[pos:pos + 4])
        typ = data[pos + 4:pos + 8]
        body = data[pos + 8:pos + 8 + ln]
        if typ == b"IHDR":
            w, h, bd, ct = struct.unpack(">IIBB", body[:10])
        elif typ == b"IDAT":
            idat += body
        elif typ == b"IEND":
            break
        pos += 12 + ln
    raw = zlib.decompress(idat)
    ch = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[ct]
    stride = w * ch
    rows, prev, i = [], bytearray(stride), 0
    for _ in range(h):
        f = raw[i]; i += 1
        line = bytearray(raw[i:i + stride]); i += stride
        if f == 1:
            for x in range(ch, stride):
                line[x] = (line[x] + line[x - ch]) & 255
        elif f == 2:
            for x in range(stride):
                line[x] = (line[x] + prev[x]) & 255
        elif f == 3:
            for x in range(stride):
                a = line[x - ch] if x >= ch else 0
                line[x] = (line[x] + ((a + prev[x]) >> 1)) & 255
        elif f == 4:
            for x in range(stride):
                a = line[x - ch] if x >= ch else 0
                b = prev[x]
                c = prev[x - ch] if x >= ch else 0
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[x] = (line[x] + pr) & 255
        rows.append(line)
        prev = line
    return w, h, ch, rows


def stats(rows, ch, y0, y1):
    """領域の (平均輝度, 濃色ピクセル率, 赤ピクセル率)"""
    dark = red = tot = 0
    s = 0
    for y in range(y0, min(y1, len(rows))):
        line = rows[y]
        for x in range(0, len(line), ch):
            r, g, b = line[x], line[x + 1], line[x + 2]
            s += (r + g + b) / 3
            tot += 1
            if (r + g + b) / 3 < 120:
                dark += 1
            if r > 150 and g < 90 and b < 90:
                red += 1
    if not tot:
        return 0, 0, 0
    return s / tot, dark / tot, red / tot


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("site")
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()
    gdir = os.path.join(ROOT, a.site, "assets", "gui")
    files = sorted(glob.glob(os.path.join(gdir, "*.svg")))
    if a.limit:
        files = files[: a.limit]
    if not files:
        sys.exit("no svg in %s" % gdir)
    if not os.path.exists(CHROME):
        sys.exit("Chrome not found: %s" % CHROME)
    ng = []
    with tempfile.TemporaryDirectory() as td:
        for f in files:
            png = os.path.join(td, os.path.basename(f) + ".png")
            subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                            "--force-device-scale-factor=1", "--screenshot=" + png,
                            "--window-size=1180,760", "file://" + f],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=60)
            if not os.path.exists(png):
                ng.append((os.path.basename(f), "rasterize failed"))
                continue
            w, h, ch, rows = read_png(png)
            tb = stats(rows, ch, 0, 32)
            body = stats(rows, ch, 110, h - 40)
            sb = stats(rows, ch, h - 34, h)
            has_callout = "<circle" in open(f, encoding="utf-8").read()
            src = open(f, encoding="utf-8").read()
            reds = max(body[2], tb[2], stats(rows, ch, 0, h)[2])
            probs = []
            if w != 1180 or h != 760:
                probs.append("size %dx%d" % (w, h))
            if tb[1] < 0.3:
                probs.append("タイトルバーが薄い(%.2f)" % tb[1])
            if body[1] < 0.002 and body[0] > 250:
                probs.append("本文がほぼ空白")
            if sb[0] > 252:
                probs.append("ステータスバー無し")
            if has_callout and reds < 0.0002:
                probs.append("callout の赤が見えない")
            flag = "OK " if not probs else "NG "
            if probs:
                ng.append((os.path.basename(f), ", ".join(probs)))
            print("%s%-34s tb_dark=%.2f body_ink=%.3f sb_avg=%.0f red=%.5f %s"
                  % (flag, os.path.basename(f), tb[1], body[1], sb[0], reds, "" if not probs else "| " + ", ".join(probs)))
    print("\n%d 枚チェック / NG %d" % (len(files), len(ng)))
    sys.exit(1 if ng else 0)


if __name__ == "__main__":
    main()
