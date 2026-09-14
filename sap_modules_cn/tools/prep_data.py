# -*- coding: utf-8 -*-
"""把教材 S4.docx 的解析结果里「本站要用的 4 个模块」抽出来，并给每张截图量尺寸。

    python3 tools/prep_data.py

产出（都在 work/ 下，可重复执行）：
  modules_model.json … MM / PP / FI / CO 四个模块的任务（标题 / IMG 路径 / 手顺 / 截图 / T-code）
  img_manifest.json  … 每张真实截图的宽高 + 原文件名 + 所属任务（页面用它写 <img width height>）
  copy_report.json   … 从 sap_sd_cn 复制了多少张截图、有没有缺图

数据来源：`../sap_sd_cn/work/site_model.json`（由教材 S4.docx 解析而来，见 sap_sd_cn/README.md）。
本脚本不重新解析 docx，只做筛选与建档 —— 保证「站上的图 = 教材原图」这条路是短的、可核对的。
"""
import json
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
SRC = os.path.abspath(os.path.join(ROOT, "..", "sap_sd_cn"))
WORK = os.path.join(ROOT, "work")
MODS = ["mm", "pp", "fi", "co"]


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(24)
    if len(head) < 24 or head[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    w, h = struct.unpack(">II", head[16:24])
    return w, h


def jpeg_size(path):
    with open(path, "rb") as f:
        data = f.read()
    if data[:2] != b"\xff\xd8":
        return None
    i = 2
    n = len(data)
    while i + 9 < n:
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
            i += 2
            continue
        seglen = struct.unpack(">H", data[i + 2:i + 4])[0]
        if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
            h, w = struct.unpack(">HH", data[i + 5:i + 9])
            return w, h
        i += 2 + seglen
    return None


def gif_size(path):
    with open(path, "rb") as f:
        head = f.read(10)
    if head[:3] != b"GIF":
        return None
    w, h = struct.unpack("<HH", head[6:10])
    return w, h


def img_size(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".png":
        return png_size(path)
    if ext in (".jpg", ".jpeg"):
        return jpeg_size(path)
    if ext == ".gif":
        return gif_size(path)
    return None


def main():
    src_model = json.load(open(os.path.join(SRC, "work", "site_model.json"), encoding="utf-8"))
    out = {}
    for mod in src_model:
        if mod["code"] not in MODS:
            continue
        out[mod["code"]] = {
            "code": mod["code"],
            "title": mod["title"],
            "tasks": mod["tasks"],
        }
    json.dump(out, open(os.path.join(WORK, "modules_model.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    # ---- 截图清单 -------------------------------------------------------
    manifest, missing, total = {}, [], 0
    for mod in MODS:
        base = os.path.join(ROOT, "assets", "img", mod)
        for dirpath, _dirnames, filenames in os.walk(base):
            for fn in sorted(filenames):
                if fn.startswith("."):
                    continue
                full = os.path.join(dirpath, fn)
                rel = os.path.relpath(full, os.path.join(ROOT, "assets", "img")).replace(os.sep, "/")
                size = img_size(full)
                if not size:
                    missing.append(rel)
                    continue
                tdir = rel.split("/")[1] if len(rel.split("/")) > 2 else ""
                try:
                    task = int(tdir[1:])
                except ValueError:
                    task = 0
                step = 0
                parts = fn.split("_")
                if parts and parts[0].isdigit():
                    step = int(parts[0])
                manifest[rel] = {"w": size[0], "h": size[1], "orig": fn, "task": task,
                                 "mod": mod, "step": step}
                total += 1
    json.dump(manifest, open(os.path.join(WORK, "img_manifest.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=0)

    # ---- 教材里引用的图 vs 磁盘上实际的图 --------------------------------
    referenced = set()
    for mod in MODS:
        for t in out[mod]["tasks"]:
            for st in t["steps"]:
                for p in st.get("imgs") or []:
                    referenced.add(p)
    on_disk = set(manifest)
    report = {
        "modules": {m: {"tasks": len(out[m]["tasks"]),
                        "steps": sum(len(t["steps"]) for t in out[m]["tasks"]),
                        "images_on_disk": sum(1 for k in manifest if k.startswith(m + "/"))}
                    for m in MODS},
        "images_total": total,
        "referenced_by_book": len(referenced),
        "referenced_missing_on_disk": sorted(referenced - on_disk)[:40],
        "referenced_missing_count": len(referenced - on_disk),
        "unreadable": missing,
    }
    json.dump(report, open(os.path.join(WORK, "copy_report.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(json.dumps(report, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
