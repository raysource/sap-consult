#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全サイト一括検証（読み取り専用）— 5 つの培训站を 1 コマンドで棚卸しする。

    python3 tools/verify_all_sites.py                 # 全サイト
    python3 tools/verify_all_sites.py sapmto sapeto   # 指定サイトだけ
    python3 tools/verify_all_sites.py --render        # GUI のラスタライズ検証まで（遅い）

出力するもの（サイトごと）:
  ページ数 / config ステップ数 / handson STEP 数 / quiz 問題数 / GUI 図数・SVG 数 /
  Excel（要件定義・手順書、学習WBS）とそのシート数 / verify_site.py の結果 /
  verify_gui_figures.py の結果 / 学習WBS のタスク数
"""
import argparse
import glob
import os
import re
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SITES = ["sap_sd", "sapmto", "sapeto", "sapmts", "sapvc", "saporderflow"]
SKILL = os.path.expanduser("~/.hermes/skills/productivity/sap-training-sites/scripts/verify_site.py")
SKIP_H2 = re.compile(r"期待結果|期待结果|つまずき|故障|验收|完成基準|発展|参考|出典|チェックリスト|まとめ|使い方")


def pages_of(site_dir):
    return sorted(os.path.basename(p) for p in glob.glob(os.path.join(site_dir, "*.html")))


def count_config_steps(site_dir):
    p = os.path.join(site_dir, "config.html")
    if not os.path.exists(p):
        return 0
    return len(re.findall(r'<div class="steph"', open(p, encoding="utf-8").read()))


def count_handson_steps(site_dir):
    n = 0
    for p in sorted(glob.glob(os.path.join(site_dir, "handson-*.html"))):
        s = open(p, encoding="utf-8").read()
        for m in re.finditer(r"<h2[^>]*>(.*?)</h2>", s, re.S):
            t = re.sub(r"<[^>]+>", "", m.group(1)).strip()
            if t and not SKIP_H2.search(t):
                n += 1
    return n


def count_quiz(site_dir):
    p = os.path.join(site_dir, "quiz.html")
    if not os.path.exists(p):
        return 0, 0
    s = open(p, encoding="utf-8").read()
    return s.count('class="quiz-q"'), len(re.findall(r'data-key="[A-D]"', s)) // 4


def container_issue(site_dir):
    """</article> が 1 回だけ・footer より前にあるか（閉じ位置が途中に飛んでいないか）"""
    bad = []
    for fp in sorted(glob.glob(os.path.join(site_dir, "*.html"))):
        t = open(fp, encoding="utf-8").read()
        n, a, f = t.count("</article>"), t.find("</article>"), t.find("<footer")
        if n != 1 or (f >= 0 and a > f):
            bad.append("%s (article=%d)" % (os.path.basename(fp), n))
    return bad


def spec_steps(site_dir):
    """gui_spec.json があれば必須ステップ数（＝図を付けると宣言した手顺ステップ）を返す"""
    import json
    fp = os.path.join(site_dir, "tools", "gui_spec.json")
    if not os.path.exists(fp):
        return None
    try:
        sp = json.load(open(fp, encoding="utf-8"))
    except Exception:
        return None
    return sum(len(v) for v in (sp.get("pages") or {}).values())


def count_figs(site_dir):
    figs = 0
    for p in glob.glob(os.path.join(site_dir, "*.html")):
        figs += open(p, encoding="utf-8").read().count('<figure class="gui"')
    svgs = len(glob.glob(os.path.join(site_dir, "assets", "gui", "*.svg")))
    pngs = len(glob.glob(os.path.join(site_dir, "assets", "gui", "*.png")))
    return figs, svgs, pngs


def xlsx_info(site_dir, name_hint):
    out = []
    for p in sorted(glob.glob(os.path.join(site_dir, "*.xlsx"))):
        base = os.path.basename(p)
        if name_hint and name_hint not in base:
            continue
        sheets = "?"
        try:
            from openpyxl import load_workbook
            sheets = len(load_workbook(p, read_only=True).sheetnames)
        except Exception:
            pass
        out.append("%s (%d sheet)" % (base, sheets) if isinstance(sheets, int) else base)
    return out


def run(cmd, cwd):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return (r.stdout or "").strip().splitlines()[-1] if (r.stdout or "").strip() else (r.stderr or "").strip().splitlines()[-1] if (r.stderr or "").strip() else "(no output)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sites", nargs="*")
    ap.add_argument("--render", action="store_true", help="check_gui_render.py も実行（遅い）")
    ap.add_argument("--wbs", action="store_true", help="学習WBS を再生成してタスク数を確認")
    a = ap.parse_args()
    sites = a.sites or SITES
    rows, problems = [], []
    for s in sites:
        d = os.path.join(ROOT, s)
        if not os.path.isdir(d):
            rows.append((s, "NOT FOUND", "", "", "", "", "", "", ""))
            problems.append("%s: ディレクトリがありません" % s)
            continue
        pgs = pages_of(d)
        ncfg, nhs = count_config_steps(d), count_handson_steps(d)
        nq, nqopt = count_quiz(d)
        figs, svgs, pngs = count_figs(d)
        xr = xlsx_info(d, None)   # 要件定義・手順書 / 講義テキスト など、そのサイトの成果物 xlsx
        xw = xlsx_info(d, "WBS")  # 学習WBS（受講者版）
        vs = run([sys.executable, SKILL, "."], d) if os.path.exists(SKILL) else "(skill script missing)"
        vg = run([sys.executable, os.path.join(ROOT, "tools", "verify_gui_figures.py"), s], ROOT)
        # 期待ステップ数（config + handson）に対する図の被覆
        need = spec_steps(d) if spec_steps(d) is not None else (ncfg + nhs)
        cover = "%d/%d" % (min(figs, need), need) if need else "—"
        rows.append((s, len(pgs), ncfg, nhs, nq, "%d figs / %d svg" % (figs, svgs), cover,
                     "; ".join(xr) or "—", "; ".join(xw) or "—"))
        if not vs.startswith("PASS") and pgs:
            problems.append("%s: verify_site → %s" % (s, vs[:90]))
        if need and figs < need:
            problems.append("%s: GUI 図が不足（%s）" % (s, cover))
        if vg.startswith("RESULT: FAIL") or "NG" in vg.split("RESULT")[0] and "NG 0" not in vg:
            problems.append("%s: verify_gui_figures → %s" % (s, vg[:90]))
        if not pgs:
            problems.append("%s: HTML がありません" % s)
        ci = container_issue(d)
        if ci:
            problems.append("%s: コンテナ閉じ位置が異常 → %s" % (s, ", ".join(ci[:4])))
        if not xr:
            problems.append("%s: 要件定義 Excel がありません" % s)
        if a.render and svgs:
            rc = run([sys.executable, os.path.join(ROOT, "tools", "check_gui_render.py"), s], ROOT)
            print("  render %s: %s" % (s, rc))
        if a.wbs:
            print("  wbs    %s: %s" % (s, run([sys.executable, os.path.join(ROOT, "tools", "make_wbs_xlsx.py"), s], ROOT)))
        print("  verify_site[%s]: %s" % (s, vs[:110]))
        print("  gui_check  [%s]: %s" % (s, vg[:110]))

    print()
    hdr = ("site", "pages", "config", "handson", "quiz", "gui", "coverage", "要件定義xlsx", "WBS xlsx")
    widths = [13, 6, 7, 8, 6, 20, 10, 34, 30]
    print(" | ".join(h.ljust(w) for h, w in zip(hdr, widths)))
    print("-" * (sum(widths) + 3 * len(widths)))
    for r in rows:
        print(" | ".join(str(c).ljust(w) for c, w in zip(r, widths)))
    print()
    if problems:
        print("要対応 %d 件:" % len(problems))
        for p in problems:
            print("  -", p)
    else:
        print("すべてのサイトで構造検証・GUI 図カバレッジとも OK")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
