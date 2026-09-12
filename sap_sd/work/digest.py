#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Turn the per-chunk frame inventories into one deduplicated curriculum digest.

Usage: python3 digest.py <workdir> [--full]
Writes curriculum.md (distinct screens in chronological order) and prints a summary.
"""
import glob
import json
import os
import sys

WORK = sys.argv[1] if len(sys.argv) > 1 else "/Users/jason/Desktop/work/training/sap_sd/work"
FULL = "--full" in sys.argv

frames = []
for f in sorted(glob.glob(os.path.join(WORK, "inv_*.json"))):
    d = json.load(open(f, encoding="utf-8"))
    for fr in d.get("frames", []):
        fr["_chunk"] = d.get("chunk")
        frames.append(fr)
frames.sort(key=lambda x: x.get("ts_sec", 0))

# dedupe: consecutive frames with the same title+kind collapse into one screen entry
screens = []
for fr in frames:
    key = ((fr.get("title") or "").strip().lower(), fr.get("kind"))
    lines = [l.strip() for l in (fr.get("text") or []) if l and l.strip()]
    if screens and screens[-1]["key"] == key:
        s = screens[-1]
        s["last"] = fr.get("ts_sec")
        s["n"] += 1
        for l in lines:
            if l not in s["lines"]:
                s["lines"].append(l)
    else:
        screens.append({"key": key, "title": (fr.get("title") or "(no title)").strip(),
                        "kind": fr.get("kind"), "tcode": (fr.get("tcode") or "").strip(),
                        "first": fr.get("ts_sec"), "last": fr.get("ts_sec"), "n": 1,
                        "lines": lines, "notes": (fr.get("notes") or "").strip()})

# drop slide-window chrome (IE title bar text) and pure-boilerplate lines
DROP = {"SAP Education - Windows Internet Explorer", "SAP Education", "SAP", "Menu"}
for s in screens:
    s["lines"] = [l for l in s["lines"] if l not in DROP]
    s["lines"] = [l for l in s["lines"] if not l.startswith("SAP Education") or ":" in l]

out = []
out.append("# 视频内容摘录（deduped screens） 源: 录像45 Sales order processing.mp4\n")
out.append("共 %d 个不同画面（%d 帧原始记录）。\n" % (len(screens), len(frames)))
for i, s in enumerate(screens, 1):
    mm, ss = divmod(int(s["first"]), 60)
    mm2, ss2 = divmod(int(s["last"]), 60)
    tcs = (" T-code=%s" % s["tcode"]) if s["tcode"] else ""
    out.append("\n## %d. [%02d:%02d-%02d:%02d] %s (%s%s)" % (i, mm, ss, mm2, ss2, s["title"], s["kind"], tcs))
    lim = 40 if FULL else 14
    for l in s["lines"][:lim]:
        out.append("- " + l)
    if s["notes"]:
        out.append("- _(notes)_ " + s["notes"][:200])

path = os.path.join(WORK, "curriculum.md")
open(path, "w", encoding="utf-8").write("\n".join(out) + "\n")
print("wrote", path, "screens:", len(screens))
kinds = {}
for s in screens:
    kinds[s["kind"]] = kinds.get(s["kind"], 0) + 1
print("kinds:", kinds)
