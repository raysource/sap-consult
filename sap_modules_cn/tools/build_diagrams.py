# -*- coding: utf-8 -*-
"""生成各模块的自绘图 SVG。

    python3 tools/build_diagrams.py            # 全部模块
    python3 tools/build_diagrams.py mm         # 只建 MM
    python3 tools/build_diagrams.py --check    # 只检查（XML 合法性 + 文字是否溢出方框）

每个模块包用 DIAGRAMS 提供「图的数据」（dict），排版由 tools/sitegen/svgkit.py 负责。
检查结果（含溢出问题）写入 work/diagram_qa.json，方便复现与回归。
"""
import importlib
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(HERE, "sitegen"))

import common  # noqa: E402
import svgkit  # noqa: E402


def build(code, write=True):
    pack = importlib.import_module("pack_%s" % code)
    specs = getattr(pack, "DIAGRAMS", [])
    out_dir = os.path.join(ROOT, "assets", "diagrams", code)
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    rows = []
    for spec in specs:
        svg, claims = svgkit.build(spec)
        name = spec["file"]
        if write:
            with io.open(os.path.join(out_dir, name), "w", encoding="utf-8") as f:
                f.write(svg)
        rows.append({"file": name, "kind": spec["kind"], "title": spec["title"],
                     "bytes": len(svg), "overflow": [list(c) for c in claims]})
    return rows


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("-")]
    check_only = "--check" in argv
    codes = args or [m["code"] for m in common.MODULES]
    qa, bad = {}, 0
    for code in codes:
        rows = build(code, write=not check_only)
        qa[code] = rows
        for r in rows:
            flag = ""
            if r["overflow"]:
                bad += 1
                flag = "  ← 溢出 %d 处：%s" % (len(r["overflow"]), r["overflow"][:2])
            print("[%s] %-22s %-9s %7d bytes%s" % (code, r["file"], r["kind"], r["bytes"], flag))
    path = os.path.join(ROOT, "work", "diagram_qa.json")
    if os.path.exists(path):
        try:
            old = json.load(open(path, encoding="utf-8"))
            for k in old:
                if k not in qa:
                    qa[k] = old[k]
        except ValueError:
            pass
    json.dump(qa, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("diagrams: %d，溢出图 %d" % (sum(len(v) for v in qa.values()), bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
