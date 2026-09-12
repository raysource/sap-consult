#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
講義用 PDF を 2 種類つくる（讲师版 / 学员版）

    python3 tools/make_handout_pdf.py <site>              # 讲师版（画面＋キャプション＋注記＋確認T-code）
    python3 tools/make_handout_pdf.py <site> --student     # 学员版（同じ画面、注記は空白欄＝自分で書き込む）
    python3 tools/make_handout_pdf.py <site> --both

出力:
    <site>/<CODE>_講義用画面集.pdf     ← 讲师用（既存）
    <site>/<CODE>_学员用記入シート.pdf  ← 受講者用（画面＋空欄メモ欄）

実装は export_gui_png.py の make_handout() を呼び、--student のときだけテンプレートを差し替えます。
画面は assets/gui_png/*.png（2 倍解像度）を使うので、先に
`python3 tools/export_gui_png.py <site>` を実行しておいてください。
"""
import argparse
import importlib.util
import os
import subprocess
import sys
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def load_exporter():
    p = os.path.join(ROOT, "tools", "export_gui_png.py")
    spec = importlib.util.spec_from_file_location("exporter", p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def build_student_html(ex, site, figs, code, title):
    """学员版：画面は同じ、注記は「自分で書く欄」にする"""
    parts = [f"""<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8"><title>{title} 記入シート</title>
<style>
@page {{ size: A4 landscape; margin: 10mm 10mm; }}
body {{ font-family: -apple-system, "Hiragino Sans", "Noto Sans CJK JP", Meiryo, sans-serif; color: #1d2d3e; margin: 0; }}
/* 讲师版と同じ「1 画面 = 1 ページ」の固定高ページ方式（Chrome の自動改ページに任せない） */
.page {{ height: 188mm; overflow: hidden; page-break-after: always; display: flex; flex-direction: column; }}
.cover {{ padding: 30mm 16mm; height: 188mm; page-break-after: always; }}
.cover h1 {{ font-size: 28pt; margin: 0 0 6mm; }}
.cover p {{ font-size: 11.5pt; color: #5b6b7c; line-height: 1.8; }}
.sec-head {{ border-bottom: 2px solid #0A6ED1; padding-bottom: 1.5mm; margin: 0 0 3mm; }}
.sec-head h2 {{ font-size: 14pt; margin: 0; }}
figure {{ margin: 0; flex: 1 1 auto; display: flex; flex-direction: column; min-height: 0; }}
figure img {{ display: block; margin: 0 auto; width: auto; max-width: 100%; max-height: 106mm;
  border: 1px solid #c9d6e0; border-radius: 4px; }}
figcaption {{ font-size: 10pt; font-weight: 600; margin: 1.5mm 0 1.5mm; }}
.tx {{ font-family: Menlo, monospace; color: #0a4f9e; margin-left: 3mm; }}
.hint {{ font-size: 8.5pt; color: #8a94a0; margin: 0 0 1mm; }}
.wl {{ border: 1px solid #c3ccd6; border-radius: 3px; height: 26mm; margin-top: 1mm; flex: 0 0 auto;
  background: repeating-linear-gradient(to bottom, #fff 0, #fff 8.2mm, #eef1f4 8.2mm, #eef1f4 8.6mm); }}
.wl b {{ font-size: 8.5pt; color: #6b7a8d; padding-left: 2mm; }}
</style></head><body>
<div class="cover"><h1>{title}<br>受講者記入シート（{len(figs)} 画面）</h1>
<p>各画面を見ながら、<b>「この画面で何を確認するか」「今の自分のシステムではどうなっているか」</b>を空欄に記入してください。<br>
講師の説明を聞く前に、まず自分で埋めてみると定着が変わります。</p>
</div>"""]
    cur = None
    head = ""
    for f in figs:
        key = (f["page"], f["head"])
        if key != cur:
            cur = key
            head = '<div class="sec-head"><h2>%s</h2></div>' % (f["head"] or f["page"])
        parts.append(f"""<div class="page">{head}<figure><img src="__SRC__"><figcaption>{f['cap'] or f['head']}<span class="tx">{f['tx']}</span></figcaption>
<p class="hint">確認したこと／気づいたこと（自システムでは：　　　　　　　　　　　　）</p>
<div class="wl"><b>メモ・伝票番号・数値</b></div></figure></div>""")
        head = ""                      # 見出しは節の最初のページだけ
    parts.append("</body></html>")
    html = "\n".join(parts)
    pngdir = os.path.join(ROOT, site, "assets", "gui_png")
    for f in figs:
        base = os.path.basename(f["src"])[:-4]
        png = os.path.join(pngdir, base + ".png")
        src = png if os.path.exists(png) else os.path.join(ROOT, site, f["src"])
        html = html.replace("__SRC__", "file://" + src, 1)
    return html


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("site")
    ap.add_argument("--student", action="store_true")
    ap.add_argument("--both", action="store_true")
    a = ap.parse_args()
    ex = load_exporter()
    if a.student or a.both:
        d = os.path.join(ROOT, a.site)
        figs = ex.figures_of(a.site)
        if not figs:
            sys.exit("no figures in %s" % d)
        html = build_student_html(ex, a.site, figs, ex.CODES.get(a.site, a.site), ex.TITLES.get(a.site, a.site))
        tmp = tempfile.mkdtemp()
        hp = os.path.join(tmp, "student.html")
        open(hp, "w", encoding="utf-8").write(html)
        pdf = os.path.join(d, "%s_学员用記入シート.pdf" % ex.CODES.get(a.site, a.site))
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                        "--print-to-pdf=" + pdf, "--virtual-time-budget=20000", "file://" + hp],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=600)
        print("%-14s 学员版: %s (%.1f MB / %d 画面)" % (a.site, os.path.relpath(pdf, ROOT),
                                                     os.path.getsize(pdf) / 1048576 if os.path.exists(pdf) else 0, len(figs)))
    if not a.student or a.both:
        ex.make_handout(a.site)


if __name__ == "__main__":
    main()
