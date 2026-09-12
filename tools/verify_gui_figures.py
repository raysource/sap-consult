#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
手顺ページの各ステップに SAP GUI 画面イメージが入っているかを検証する。

    python3 tools/verify_gui_figures.py sapmto

判定の考え方:
  ・`<site>/tools/gui_spec.json` があれば「**そのスペックに書かれたステップ**」を必須集合とする
    （講義サイトの『早見表』『判断フロー』のように、図を付けない節があるのは正しい）。
    スペックのキーが見出しと一致しない場合は MISS として報告する（キーの打ち間違い検出）。
  ・スペックが無いサイトは、config.html の全 C ステップと handson の全 h2 を必須とする。
  ・スペックにも無い・図も無い節は INFO（情報）として一覧するだけ（NG にしない）。

チェック内容:
  1. 必須ステップに <figure class="gui"> が 1 つ以上あるか
  2. 参照している assets/gui/*.svg|png が実在するか
  3. img に alt、figure に figcaption があるか
  4. SVG が XML として妥当か（viewBox が 1180x760 か）
  5. figure のキャプションに「画面イメージ」表記があるか（実機スクリーンショットとの混同防止）
"""
import json
import os
import re
import sys
import glob
import xml.etree.ElementTree as ET

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SKIP_H2 = re.compile(r"期待結果|期待结果|つまずき|故障|验收|完成基準|発展|参考|出典|チェックリスト|まとめ")
FIGSIZE = (1180, 760)


def plain(t):
    t = re.sub(r"<[^>]+>", "", t)
    return re.sub(r"\s+", " ", t.replace("&nbsp;", " ")).strip()


def sections(page, src):
    """[(key, start, end)] — config.html は div.steph、それ以外は h2"""
    out = []
    if page == "config.html":
        ms = list(re.finditer(r'<div class="steph" id="([^"]+)">', src))
        stops = [m.start() for m in ms]
        h2all = [m.start() for m in re.finditer(r"<h2[^>]*>", src)]
        for i, m in enumerate(ms):
            # 次の steph か次の h2 のどちらか早い方まで（重複計上を避ける）
            nxt = ([ms[i + 1].start()] if i + 1 < len(ms) else []) + [x for x in h2all if x > m.start()]
            end = min(nxt) if nxt else len(src)
            out.append((m.group(1), m.start(), end))
        # h2 節（配置前的准备・チェックリスト・Cloud 対照など、steph を持たない節）も見出しとして扱う
        h2s = list(re.finditer(r"<h2[^>]*>(.*?)</h2>", src, re.S))
        for i, m in enumerate(h2s):
            title = plain(m.group(1))
            if not title:
                continue
            nxt = [x.start() for x in h2s[i + 1:i + 2]] + [x for x in stops if x > m.start()]
            end = min(nxt) if nxt else len(src)
            out.append((title, m.start(), end))
    else:
        ms = list(re.finditer(r"<h2[^>]*>(.*?)</h2>", src, re.S))
        for i, m in enumerate(ms):
            title = plain(m.group(1))
            end = ms[i + 1].start() if i + 1 < len(ms) else len(src)
            out.append((title, m.start(), end))
    return out


def load_required(site_dir):
    p = os.path.join(site_dir, "tools", "gui_spec.json")
    if not os.path.exists(p):
        return None
    spec = json.load(open(p, encoding="utf-8"))
    req = {}
    for page, steps in (spec.get("pages") or {}).items():
        req[page] = {k: len(v) for k, v in steps.items()}
    return req


def main():
    site = sys.argv[1] if len(sys.argv) > 1 else None
    if not site:
        sys.exit("usage: verify_gui_figures.py <site>")
    site_dir = os.path.join(ROOT, site)
    req = load_required(site_dir)
    strict = req is None
    req = req or {}
    total_req = total_hit = total_figs = 0
    missing, refs_missing, a11y, svg_bad, mismatch, info_no_fig = [], [], [], [], [], []
    seen_pages = set()
    for p in sorted(glob.glob(os.path.join(site_dir, "*.html"))):
        page = os.path.basename(p)
        if page in ("instructor.html", "worksheet.html", "quiz.html"):
            continue
        src = open(p, encoding="utf-8").read()
        secs = sections(page, src)
        if not secs:
            continue
        seen_pages.add(page)
        page_req = dict(req.get(page, {}))
        page_req_default = strict
        for key, s0, e0 in secs:
            block = src[s0:e0]
            figs = re.findall(r'<figure class="gui">.*?</figure>', block, re.S)
            # 必須判定
            matched_key = None
            for k in list(page_req.keys()):
                if key == k or key.startswith(k) or k.startswith(key):
                    matched_key = k
                    break
            is_required = matched_key is not None or (page_req_default and not SKIP_H2.search(key))
            if matched_key:
                page_req.pop(matched_key)
                total_req += 1
            elif is_required:
                total_req += 1
            if figs:
                total_figs += len(figs)
                if matched_key or is_required:
                    total_hit += 1
            else:
                if matched_key:
                    missing.append((page, matched_key))
                elif is_required:
                    missing.append((page, key))
                else:
                    info_no_fig.append((page, key))
            for f in figs:
                m = re.search(r'<img src="([^"]+)"', f)
                if not m:
                    a11y.append((page, key, "img なし"))
                    continue
                ref = m.group(1)
                if 'alt="' not in f or "<figcaption>" not in f:
                    a11y.append((page, key, "alt / figcaption なし"))
                if "画面イメージ" not in f and ".png" not in ref:
                    a11y.append((page, key, "「画面イメージ」表記なし"))
                fp = os.path.join(site_dir, ref)
                if not os.path.exists(fp):
                    refs_missing.append((page, key, ref))
        for k, n in page_req.items():
            mismatch.append((page, k, n))
            total_req += 1
    gdir = os.path.join(site_dir, "assets", "gui")
    if os.path.isdir(gdir):
        for f in sorted(glob.glob(os.path.join(gdir, "*.svg"))):
            try:
                root = ET.parse(f).getroot()
                vb = root.get("viewBox", "")
                if vb.split()[-2:] != [str(FIGSIZE[0]), str(FIGSIZE[1])]:
                    svg_bad.append((os.path.basename(f), "viewBox=%s" % vb))
            except ET.ParseError as ex:
                svg_bad.append((os.path.basename(f), str(ex)))
    n_svg = len(glob.glob(os.path.join(gdir, "*.svg"))) if os.path.isdir(gdir) else 0
    n_png = len(glob.glob(os.path.join(gdir, "*.png"))) if os.path.isdir(gdir) else 0
    print("site=%s  mode=%s  必須ステップ=%d  図あり=%d  図=%d  SVG=%d  PNG=%d"
          % (site, "spec" if not strict else "全見出し", total_req, total_hit, total_figs, n_svg, n_png))
    for label, rows in (("図が無い必須ステップ", missing), ("spec のキーが見出しと一致しない", mismatch),
                        ("参照先が無い", refs_missing), ("alt/figcaption/表記 不足", a11y), ("SVG 異常", svg_bad)):
        if rows:
            print("  [NG] %s: %d 件" % (label, len(rows)))
            for r in rows[:20]:
                print("       ", " / ".join(str(x) for x in r))
            if len(rows) > 20:
                print("        … 他 %d 件" % (len(rows) - 20))
    if info_no_fig:
        print("  [INFO] 図を付けていない節（スペック対象外）: %d 件 — %s"
              % (len(info_no_fig), ", ".join("%s/%s" % (p, k[:22]) for p, k in info_no_fig[:6])))
    ok = not (missing or refs_missing or a11y or svg_bad or mismatch) and total_req > 0 and total_hit == total_req
    print("RESULT:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
