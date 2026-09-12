#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
画面イメージを PNG に書き出す（スライド・Word・印刷用）＋ 講義用の画面集 PDF を作る。

    python3 tools/export_gui_png.py <site>              # assets/gui/*.svg → assets/gui_png/*.png（2 倍解像度）
    python3 tools/export_gui_png.py <site> --scale 3    # 3 倍（印刷向け）
    python3 tools/export_gui_png.py <site> --zip        # まとめて <CODE>_画面PNG.zip にする
    python3 tools/make_handout_pdf.py <site>            # 手顺ごとに 1 セクションの画面集 PDF（講義配布用）

なぜ必要か: SVG はブラウザでは綺麗に出るが、PowerPoint / Word / 印刷では扱いが面倒なことが多い。
PNG にしておけばそのまま貼れる。写真（実機スクリーンショット）が無くても、
ここまでの生成図だけで講義資料が完結するようにするための出力です。

出力:
    <site>/assets/gui_png/<name>.png          画面 1 枚ごとの PNG
    <site>/<CODE>_画面PNG.zip                 PNG 一式（--zip のとき）
    <site>/<CODE>_講義用画面集.pdf            画面集（make_handout_pdf.py）
"""
import argparse
import glob
import json
import os
import re
import subprocess
import sys
import tempfile
import zipfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
CODES = {"sap_sd": "SD", "sapmto": "MTO", "sapeto": "ETO", "sapmts": "MTS", "sapvc": "VC", "saporderflow": "CMP"}
TITLES = {"sap_sd": "SD 受注処理（Sales Order Processing）", "sapmto": "SD 受注生産（MTO）", "sapeto": "受注設計生産（ETO）", "sapmts": "SD 見込生産（MTS）",
          "sapvc": "バリアント設定付き受注生産（VC）", "saporderflow": "受注形態の横断比較（講義）"}


def chrome_png(svg, out, scale, w=1180, h=760):
    cmd = [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
           "--force-device-scale-factor=%d" % scale,
           "--window-size=%d,%d" % (w, h), "--default-background-color=FFFFFFFF",
           "--screenshot=" + out, "file://" + svg]
    r = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=90)
    return os.path.exists(out)


def export_png(site, scale=2, zipit=False):
    d = os.path.join(ROOT, site)
    svgs = sorted(glob.glob(os.path.join(d, "assets", "gui", "*.svg")))
    if not svgs:
        sys.exit("no svg in %s/assets/gui" % d)
    outdir = os.path.join(d, "assets", "gui_png")
    os.makedirs(outdir, exist_ok=True)
    ok = fail = 0
    for svg in svgs:
        out = os.path.join(outdir, os.path.basename(svg)[:-4] + ".png")
        if chrome_png(svg, out, scale) and os.path.getsize(out) > 2000:
            ok += 1
        else:
            fail += 1
            print("   FAIL:", os.path.basename(svg))
    print("%-14s PNG %d 枚（失敗 %d）→ %s (scale %dx)" % (site, ok, fail, os.path.relpath(outdir, ROOT), scale))
    if zipit:
        zp = os.path.join(d, "%s_画面PNG.zip" % CODES.get(site, site))
        with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
            for p in sorted(glob.glob(os.path.join(outdir, "*.png"))):
                z.write(p, os.path.basename(p))
        print("   zip: %s (%.1f MB)" % (os.path.relpath(zp, ROOT), os.path.getsize(zp) / 1048576))
    return ok, fail


# --------------------------------------------------------------------------
# 講義用の画面集 PDF（手顺ごとに 1 セクション、画面＋キャプション＋注記）
# --------------------------------------------------------------------------
def figures_of(site):
    """HTML から (page, 直前の見出し, img src, caption, callouts, tip) を取り出す順序つきリスト"""
    out = []
    for page in ["config.html", "handson-1.html", "handson-2.html", "handson-3.html",
                 "handson-4.html", "handson-5.html", "compare.html", "scenario-eq.html", "vc.html"]:
        p = os.path.join(ROOT, site, page)
        if not os.path.exists(p):
            continue
        s = open(p, encoding="utf-8").read()
        heads = [(m.start(), re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(1))).strip())
                 for m in re.finditer(r"<h[23][^>]*>(.*?)</h[23]>", s, re.S)]
        for m in re.finditer(r'<figure class="gui">(.*?)</figure>', s, re.S):
            blk = m.group(1)
            src = re.search(r'src="([^"]+)"', blk)
            cap = re.search(r'<b class="t">(.*?)</b>', blk, re.S)
            tx = re.search(r'<span class="tx">(.*?)</span>', blk, re.S)
            cos = re.findall(r"<li><b>\d+</b>\s*(.*?)</li>", blk, re.S)
            tip = re.search(r'<p class="gui-tip">(.*?)</p>', blk, re.S)
            head = ""
            for pos, t in heads:
                if pos < m.start():
                    head = t
                else:
                    break
            out.append(dict(page=page, head=head,
                            src=src.group(1) if src else "",
                            cap=re.sub(r"<[^>]+>", "", cap.group(1)).strip() if cap else "",
                            tx=re.sub(r"<[^>]+>", "", tx.group(1)).strip() if tx else "",
                            callouts=[re.sub(r"<[^>]+>", "", c).strip() for c in cos],
                            tip=re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", tip.group(1))).strip() if tip else ""))
    return out


def make_handout(site):
    d = os.path.join(ROOT, site)
    figs = figures_of(site)
    if not figs:
        sys.exit("no figures in %s" % d)
    code = CODES.get(site, site)
    title = TITLES.get(site, site)
    parts = ["""<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8"><title>%s 画面集</title>
<style>
@page { size: A4 landscape; margin: 10mm 10mm; }
* { box-sizing: border-box; }
body { font-family: -apple-system, "Hiragino Sans", "Noto Sans CJK JP", Meiryo, sans-serif; margin: 0; color: #1d2d3e; }
.page { height: 188mm; overflow: hidden; page-break-after: always; break-after: page;
  display: flex; flex-direction: column; }
.cover { padding: 30mm 16mm; height: 188mm; page-break-after: always; }
.cover h1 { font-size: 28pt; margin: 0 0 7mm; }
.cover p { font-size: 11.5pt; color: #5b6b7c; line-height: 1.8; }
.sec-head { border-bottom: 2px solid #0A6ED1; padding-bottom: 1.5mm; margin: 0 0 3mm; }
.sec-head h2 { font-size: 14pt; margin: 0; }
.sec-head .meta { font-size: 9pt; color: #6b7a8d; margin: 1mm 0 0; }
figure { margin: 0; flex: 1 1 auto; display: flex; flex-direction: column; min-height: 0; }
figure img { display: block; margin: 0 auto; width: auto; max-width: 100%%; max-height: 122mm;
  border: 1px solid #c9d6e0; border-radius: 4px; }
figcaption { font-size: 10pt; font-weight: 600; margin: 2mm 0 1mm; }
.tx { font-family: Menlo, monospace; font-weight: 700; color: #0a4f9e; margin-left: 4mm; }
.legend { font-size: 8.5pt; color: #38424e; margin: 0; padding-left: 0; list-style: none; }
.legend li { margin: 0.5mm 0; }
.legend b { display: inline-block; min-width: 5mm; height: 5mm; line-height: 5mm; text-align: center;
  border: 1.2px solid #d32f2f; border-radius: 3mm; color: #d32f2f; font-size: 8pt; margin-right: 2mm; }
.tip { font-size: 8pt; color: #6b7a8d; margin: 1mm 0 0; }
.note { font-size: 9pt; color: #6b5426; background: #fff8e6; border-left: 3px solid #d9a431; padding: 2mm 3mm; margin: 4mm 0 0; }
</style></head><body>
<div class="cover"><h1>%s<br>画面集（%d 画面）</h1>
<p>手顺（config の各 STEP と各練習）に対応する画面イメージを、ページ順に並べた講義配布用資料です。<br>
各画面には「なぜそこを見るのか」の注記（赤番号）と、自システムで確認するための T-code を付けています。<br>
1 画面 = 1 ページです。</p>
<div class="note"><b>この画面は SAP GUI の標準レイアウトを再現した図であり、実機のスクリーンショットではありません。</b>
フィールド名・順序・ボタン位置はリリースとカスタマイズで変わります。実機の画面と合わせて確認してください。</div>
</div>""" % (title, title, len(figs))]

    cur = None
    for f in figs:
        key = (f["page"], f["head"])
        head = ""
        if key != cur:
            cur = key
            head = '<div class="sec-head"><h2>%s</h2><p class="meta">%s ／ %s</p></div>' % (
                f["head"] or f["page"], f["page"], f["tx"])
        leg = "".join("<li><b>%d</b>%s</li>" % (i, c) for i, c in enumerate(f["callouts"], 1))
        parts.append('<div class="page">%s<figure><img src="%s"><figcaption>%s<span class="tx">%s</span></figcaption>%s%s</figure></div>'
                     % (head, f["src"], f["cap"] or f["head"], f["tx"],
                        '<ul class="legend">%s</ul>' % leg if leg else "",
                        '<p class="tip">%s</p>' % f["tip"] if f["tip"] else ""))
    parts.append("</body></html>")

    tmp = tempfile.mkdtemp()
    hp = os.path.join(tmp, "handout.html")
    # 画像は絶対パスに置き換える（file:// 経由で読ませるため）
    pngdir = os.path.join(d, "assets", "gui_png")
    html = "\n".join(parts)
    for f in figs:
        src = f["src"]                                   # assets/gui/xxx.svg
        base = os.path.basename(src)[:-4]
        png = os.path.join(pngdir, base + ".png")        # 2x PNG があればそちらを使う（PDF が軽くなる）
        abs_src = png if os.path.exists(png) else os.path.join(d, src)
        html = html.replace('src="%s"' % src, 'src="file://%s"' % abs_src)
    # セクションの閉じタグを整える（最後に </div> を足す）
    open(hp, "w", encoding="utf-8").write(html.replace("</body></html>", "</div></body></html>"))
    pdf = os.path.join(d, "%s_講義用画面集.pdf" % code)
    r = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                        "--print-to-pdf=" + pdf, "--virtual-time-budget=20000", "file://" + hp],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=300)
    if os.path.exists(pdf):
        print("%-14s 画面集 PDF: %s (%.1f MB / %d 画面)" % (site, os.path.relpath(pdf, ROOT),
                                                          os.path.getsize(pdf) / 1048576, len(figs)))
    else:
        print("%-14s PDF 生成に失敗" % site)
        return None
    return pdf


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("site")
    ap.add_argument("--scale", type=int, default=2)
    ap.add_argument("--zip", action="store_true")
    ap.add_argument("--pdf-only", action="store_true")
    a = ap.parse_args()
    if not a.pdf_only:
        export_png(a.site, a.scale, a.zip)
    make_handout(a.site)


if __name__ == "__main__":
    main()
