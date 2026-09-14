#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把生成的 HTML 用 Chrome headless 拍成 PNG，用于人工看排版（CSS 回归）。

    python3 tools/shoot_pages.py mm/index.html mm/org.html
    python3 tools/shoot_pages.py --all mm            # 该模块的 14 页
    python3 tools/shoot_pages.py --h 2600 mm/quiz.html

输出到 work/shots/<模块>_<页>.png。注意：这台机器上同时只跑一个 Chrome 任务
（两个并行会卡住），所以本脚本一次只处理一个参数列表。
"""
import glob
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT = os.path.join(ROOT, "work", "shots")


def shoot(rel, height=2000, width=1440):
    src = os.path.join(ROOT, rel)
    if not os.path.exists(src):
        print("SKIP（不存在）", rel)
        return None
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    name = rel.replace("/", "_").replace(".html", "") + ".png"
    dst = os.path.join(OUT, name)
    cmd = [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
           "--force-device-scale-factor=1", "--window-size=%d,%d" % (width, height),
           "--screenshot=%s" % dst, "file://" + src]
    r = subprocess.run(cmd, capture_output=True)
    if not os.path.exists(dst):
        print("FAIL", rel, r.stderr.decode()[-300:])
        return None
    print("%-28s -> %s (%d KB)" % (rel, os.path.relpath(dst, ROOT), os.path.getsize(dst) // 1024))
    return dst


def main(argv):
    args = [a for a in argv[1:]]
    height = 2000
    if "--h" in args:
        i = args.index("--h")
        height = int(args[i + 1])
        del args[i:i + 2]
    if args and args[0] == "--all":
        mod = args[1]
        args = sorted(os.path.relpath(p, ROOT) for p in glob.glob(os.path.join(ROOT, mod, "*.html")))
    if not args:
        print(__doc__)
        return 1
    for rel in args:
        shoot(rel, height)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
