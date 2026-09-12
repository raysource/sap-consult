#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUI 画像の「撮影リスト」を出力する（実機スクリーンショットに差し替えるための一覧）

    python3 tools/export_gui_capture_list.py                 # 全サイト → CSV + XLSX
    python3 tools/export_gui_capture_list.py sapmto sapeto    # 指定サイトだけ（CSV のみ）

出力先: <site>/<SITE>_画面撮影リスト.csv / .xlsx
列: # / サイト / ページ / ステップ / 画像ファイル（差し替え前） / 差し替え後(.png) /
    画面タイトル / T-code / キャプション / callout（見るべき点）/ 撮影メモ（自システムでの確認）

撮影後は <site>/assets/gui/ に同名 .png を置いて
    python3 tools/swap_gui_images.py <site> --apply
で一括差し替えできます。
"""
import csv
import glob
import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SITES = ["sap_sd", "sapmto", "sapeto", "sapmts", "sapvc", "saporderflow"]
HEAD = ["#", "サイト", "ページ", "ステップ", "画像ファイル", "差し替え後", "画面タイトル",
        "T-code", "キャプション", "callouts（見るべき点）", "撮影メモ"]


def rows_for(site):
    d = os.path.join(ROOT, site)
    spec = os.path.join(d, "tools", "gui_spec.json")
    if not os.path.exists(spec):
        return []
    data = json.load(open(spec, encoding="utf-8"))
    out = []
    for page, steps in (data.get("pages") or {}).items():
        for key, screens in steps.items():
            for sc in screens:
                fn = sc.get("file", "")
                if not os.path.exists(os.path.join(d, "assets", "gui", fn)):
                    continue
                cos = " / ".join("%d) %s" % (i, c[0]) for i, c in enumerate(sc.get("callouts") or [], 1))
                out.append([site, page, key, fn, fn.rsplit(".", 1)[0] + ".png",
                            sc.get("title", ""), sc.get("tx", ""), sc.get("caption", ""), cos,
                            sc.get("tip", "") or sc.get("note", "")])
    return out


def main():
    targets = sys.argv[1:] or SITES
    grand = 0
    for site in targets:
        rows = rows_for(site)
        if not rows:
            print("%-14s 撮影対象なし（spec / SVG なし）" % site)
            continue
        d = os.path.join(ROOT, site)
        code = {"sap_sd": "SD", "sapmto": "MTO", "sapeto": "ETO", "sapmts": "MTS", "sapvc": "VC", "saporderflow": "CMP"}.get(site, site)
        for i, r in enumerate(rows, 1):
            r.insert(0, i)
        csvp = os.path.join(d, "%s_画面撮影リスト.csv" % code)
        with open(csvp, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f)
            w.writerow(HEAD)
            w.writerows(rows)
        print("%-14s %3d 画面 -> %s" % (site, len(rows), os.path.basename(csvp)))
        grand += len(rows)
        try:
            from openpyxl import Workbook
            from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
            from openpyxl.utils import get_column_letter
            wb = Workbook(); ws = wb.active; ws.title = "撮影リスト"
            ws.merge_cells("A1:K1")
            c = ws.cell(1, 1, "SAP GUI 画面撮影リスト — %s（実機スクリーンショットに差し替えるための一覧）" % code)
            c.font = Font(name="微软雅黑", size=14, bold=True, color="FFFFFF")
            c.fill = PatternFill("solid", fgColor="0A6ED1")
            ws.row_dimensions[1].height = 26
            ws.merge_cells("A2:K2")
            ws.cell(2, 1, "撮影した画像は <site>/assets/gui/ に「差し替え後」のファイル名で置き、"
                          "python3 tools/swap_gui_images.py <site> --apply を実行してください。").font = Font(name="微软雅黑", size=9, color="6B7A8D")
            for j, h in enumerate(HEAD, 1):
                cc = ws.cell(3, j, h)
                cc.font = Font(name="微软雅黑", size=10, bold=True, color="FFFFFF")
                cc.fill = PatternFill("solid", fgColor="0A6ED1"); cc.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
            thin = Side(style="thin", color="C9D6E0")
            for i, r in enumerate(rows):
                for j, v in enumerate(r, 1):
                    cc = ws.cell(4 + i, j, v)
                    cc.font = Font(name="微软雅黑", size=10)
                    cc.alignment = Alignment(wrap_text=True, vertical="top")
                    cc.border = Border(left=thin, right=thin, top=thin, bottom=thin)
                    if i % 2:
                        cc.fill = PatternFill("solid", fgColor="F2F4F7")
                ws.row_dimensions[4 + i].height = 30
            for j, w in enumerate([4, 13, 15, 30, 22, 22, 34, 10, 34, 46, 46], 1):
                ws.column_dimensions[get_column_letter(j)].width = w
            ws.freeze_panes = ws.cell(4, 4)
            xp = os.path.join(d, "%s_画面撮影リスト.xlsx" % code)
            wb.save(xp)
            print("               -> %s" % os.path.basename(xp))
        except ImportError:
            pass
    print("合計 %d 画面" % grand)


if __name__ == "__main__":
    main()
