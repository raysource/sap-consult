#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
培训站索引页（ハブ）を生成する — 6 つのサイトへの入口を 1 枚にまとめる。

    python3 tools/make_hub_page.py            # → training/index.html を生成/更新（冪等）

数値（ページ数・手順ステップ数・画面数・Excel）は**実ファイルから数えて埋め込む**ので、
各サイトに追記しても再実行すれば最新になる（手書きの数字は持たない）。
デザインは各サイトと同じ（sapmto/assets/style.css・main.js をコピーして使う）。
"""
import glob
import json
import os
import re
import shutil
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SITES = [
    ("sap_sd_jp", "SAP S/4HANA 日本語実習サイト（全モジュール・日本語版）", "JP",
     "教材ドキュメント S4.docx（425 ページ・実機スクリーンショット 1385 枚）を日本語に翻訳・再構成した全モジュール手順サイト。"
     "FI / CO / MM / PP / SD の 6 大モジュール・222 タスクの日本語手順＋実機画面。画面は中国語インターフェースのまま収録し、"
     "各ステップに「原文（中国語）」折りたたみ、入力値表に「画面の中国語」列、用語対照表（日本語 ⇔ 中国語画面）を用意。講師用/受講者用/自習テスト付き。"),
    ("sap_sd_cn", "SAP S/4HANA 中文实训站（全模块手册・原文中文）", "中文",
     "教材文档 S4.docx（425 页・実機スクリーンショット 1385 枚）準拠の中国語站。FI / CO / MM / PP / SD の 6 大模块・222 任務の手顺＋実機画面。"
     "画面は生成図ではなく原文档の実機截图。T-code 速查・排錯・任務索引・讲师版/学员版/自测 付き。"),
    ("sap_cn", "SAP SD 培训课程（从概念到流程 / 总体到局部）", "SD 课程",
     "SD 专项课程站（16 页）：概念 → 组织结构 → 主数据 → 定价 → 端到端流程（询价·报价·订单·交货·发货·开票·收款）→ 配置（48 任务）→ 分析 → 实训。"
     "每个环节配真实 SAP GUI 中文界面截图（269 张，取自教材 S4.docx 的 SD 模块与准备章）与自绘的流程图/结构图/思维导图（7 张）。"
     "讲师版・学员记入表・30 题自测・术语/T-code 速查・Excel 8 表付き。"),
    ("sap_modules_cn", "SAP 全模块培训课件（MM / PP / FI / CO）", "全模块课程",
     "中文的 MM / PP / FI / CO 四模块课程（各 14 页 ＋ 总览页）：概念 → 组织结构 → 主数据 → 端到端流程 → "
     "三篇操作手顺（含教材全部 172 个任务的 IMG 路径与逐步画面）→ SPRO 配置 → 实训 → 讲师版/学员版/30 题自测/术语。"
     "画面全部取自教材 S4.docx 的这四个模块（940 张真实 SAP GUI 中文界面截图，保留原图文件名可回查），"
     "另有 32 张自绘 SVG（思维导图 / 组织树 / 数据结构 / 流程图 / 泳道图 / 集成图 / 决定链）。"),
    ("sap_sd", "SD 受注処理（Sales Order Processing）", "SD",
     "録画（SAP Education Unit 14）準拠。伝票データの 4 つの源泉・販売エリア導出・出荷プラントの優先順位・明細カテゴリ決定・変更時の再決定・Sales Summary（VC/2）。受注の「読み方」の土台。"),
    ("sapmto", "SD 受注生産（MTO）", "MTO",
     "受注在庫 E の決定链：品目 → VOV4 → 明細カテゴリ → 納入日程行カテゴリ → 所要量タイプ → 所要量クラス。受注が計画の起点。"),
    ("sapeto", "受注設計生産（ETO）", "ETO",
     "案件（WBS）× プロジェクト在庫 Q：評価付プロジェクト在庫・請求計画・予算と可用性管理・進捗→結果分析→決済。"),
    ("sapmts", "SD 見込生産（MTS）", "MTS",
     "予測（PIR）で作り自由在庫から納める：PIR と消費、MRP のネットチェンジ、標準原価と差異計算、欠品と ATP。"),
    ("sapvc", "バリアント設定付き受注生産（VC / AVC）", "VC",
     "1 品目で無数のバリエーション：特徴 CT04・クラス CL02・KMAT・設定プロファイル・依存関係で BOM と価格を制御。"),
    ("saporderflow", "受注形態の横断比較（講義）", "CMP",
     "MTS / MTO / ETO / ATO / VC を 9 维度で比較。E vs Q の STEP 対照表（同一受注を 2 通りで走らせる）と VC 概観。"),
]
ORDER = ["sap_sd_jp", "sap_sd_cn", "sap_cn", "sap_modules_cn", "sap_sd", "sapmto", "sapeto", "sapmts", "sapvc", "saporderflow"]


def count(site):
    d = os.path.join(ROOT, site)
    pages = sorted(os.path.basename(p) for p in glob.glob(os.path.join(d, "*.html")))
    cfg = os.path.join(d, "config.html")
    n_cfg = len(re.findall(r'<div class="steph"', open(cfg, encoding="utf-8").read())) if os.path.exists(cfg) else 0
    n_hs = 0
    for p in sorted(glob.glob(os.path.join(d, "handson-*.html"))):
        n_hs += len(re.findall(r'<div class="stepf|"stepfH"', ""))  # placeholder（未使用）
        n_hs += 0
    steps = None
    spec = os.path.join(d, "tools", "gui_spec.json")
    if os.path.exists(spec):
        try:
            sp = json.load(open(spec, encoding="utf-8"))
            steps = sum(len(v) for v in (sp.get("pages") or {}).values())
        except Exception:
            steps = None
    figs = len(glob.glob(os.path.join(d, "assets", "gui", "*.svg")))
    xl = [os.path.basename(p) for p in sorted(glob.glob(os.path.join(d, "*.xlsx")))]
    pdf = sorted(os.path.basename(p) for p in glob.glob(os.path.join(d, "*_講義用画面集.pdf")))
    pdf_student = sorted(os.path.basename(p) for p in glob.glob(os.path.join(d, "*_学员用記入シート.pdf")))
    pngs = len(glob.glob(os.path.join(d, "assets", "gui_png", "*.png")))
    zp = sorted(os.path.basename(p) for p in glob.glob(os.path.join(d, "*_画面PNG.zip")))
    rec = dict(pages=pages, n_pages=len(pages), n_cfg=n_cfg, n_steps=steps or 0, figs=figs, xlsx=xl,
               pdf=pdf, pdf_student=pdf_student, pngs=pngs, zip=zp, has_wbs=any("学習WBS" in x for x in xl))
    # 任意サイト用の上書き（SVG 画面イメージを作らない站は自前の数を申告できる）
    ov = os.path.join(d, "tools", "hub_stats.json")
    if os.path.exists(ov):
        try:
            o = json.load(open(ov, encoding="utf-8"))
            for k in ("n_pages", "n_steps", "figs", "n_cfg"):
                if k in o:
                    rec[k] = o[k]
            if o.get("has_wbs"):
                rec["has_wbs"] = True
        except Exception:
            pass
    return rec


def main():
    data = {s: count(s) for s, _, _, _ in SITES}
    # 共有アセット（各サイトと同じ見た目）
    dst = os.path.join(ROOT, "assets")
    os.makedirs(dst, exist_ok=True)
    for f in ("style.css", "main.js"):
        src = os.path.join(ROOT, "sapmto", "assets", f)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(dst, f))

    hub_css = """/* === 索引页の追加スタイル ============================ */
.mini { font-size: 12px; color: #6b7a8d; }
.card .mini a { color: #0a4f9e; text-decoration: none; }
.card .mini a:hover { text-decoration: underline; }
.grid.cards { grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); }
.hero { background: linear-gradient(135deg, #12324f, #1b4a72); }
.hero h1 { color: #fff; }
.hero p.lead { color: #dbe7f2; }
table.tbl.wide td a { color: #0a4f9e; }
"""
    open(os.path.join(dst, "hub.css"), "w", encoding="utf-8").write(hub_css)

    tot_pages = sum(data[s]["n_pages"] for s in ORDER)
    tot_steps = sum(data[s]["n_steps"] for s in ORDER)
    tot_figs = sum(data[s]["figs"] for s in ORDER)
    real_figs = sum(data[s]["figs"] for s in ORDER if s in ("sap_sd_cn", "sap_sd_jp"))

    cards = []
    for slug, name, code, desc in SITES:
        c = data[slug]
        tags = "".join('<span class="tag %s">%s</span>' % (t, v) for t, v in
                       (("teal", "%d 页" % c["n_pages"]),
                        ("green", "%d 手顺ステップ" % c["n_steps"]),
                        ("amber", "%d 画面" % c["figs"]),
                        ("gray", "%d Excel" % len(c["xlsx"])),
                        *([("amber", "PNG %d 枚" % c["pngs"])] if c["pngs"] else []),
                        *([("teal", "画面集 PDF")] if c["pdf"] else [])))
        def pick(*names):
            for n in names:
                if n in c["pages"]:
                    return n
            return c["pages"][0]

        ent = [pick("index.html"), pick("config.html", "compare.html"), pick("quiz.html"), pick("instructor.html")]
        ent = list(dict.fromkeys(ent))[:3]
        pdf_link = "".join('<a href="%s/%s">画面集 PDF</a> ' % (slug, x) for x in c["pdf"])
        pdf_link += "".join('<a href="%s/%s">学员版 PDF</a>' % (slug, x) for x in c["pdf_student"])
        entry = " ／ ".join('<a href="%s/%s">%s</a>' % (slug, x, x.replace(".html", "")) for x in ent)
        if pdf_link:
            entry += "　／ " + pdf_link
        cards.append("""    <div class="card">
      <h3><a href="%s/index.html">%s</a></h3>
      <p>%s</p>
      <div class="tags">%s</div>
      <p class="mini">入口: %s</p>
    </div>""" % (slug, name, desc, tags, entry))

    rows = "".join(
        "<tr><td><a href=\"%s/index.html\">%s</a></td><td>%d</td><td>%d</td><td>%d</td><td>%s</td><td>%s</td></tr>"
        % (s, dict((x[0], x[1]) for x in SITES)[s], data[s]["n_pages"], data[s]["n_steps"], data[s]["figs"],
           "／".join(data[s]["xlsx"]) or "—",
           ("学習WBS" if data[s]["has_wbs"] else "—"))
        for s in ORDER)

    html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SAP S/4HANA 业务实务培训教材（索引）</title>
<meta name="description" content="SAP S/4HANA の業務実践トレーニング教材 5 本の索引：受注生産（MTO）／受注設計生産（ETO）／見込生産（MTS）／バリアント設定（VC）／受注形態の横断比較。各サイトは静的 HTML＋Excel＋SAP GUI 画面イメージ。">
<link rel="stylesheet" href="assets/style.css">
<link rel="stylesheet" href="assets/hub.css">
</head>
<body>
<header class="site">
  <div class="nav-wrap">
    <a class="brand" href="index.html"><span class="logo">SAP</span><span class="txt">培训教材 索引</span></a>
    <nav class="main">
      <a class="active" href="index.html">总览</a>
      <a href="#sites">%d 个站</a>
      <a href="#route">学习路线</a>
      <a href="#tools">工具与验证</a>
      <a href="#stance">立场与注意</a>
    </nav>
  </div>
</header>

<div class="hero">
  <div class="hero-inner">
    <div class="kicker">SAP S/4HANA · SD / PP / MM / PS / CO 横断</div>
    <h1>从受注处理到全模块手顺：%d 本立て的实战教材</h1>
    <p class="lead">生产形态不同，后工程的「库存归属・成本对象・请求方式・月末处理」就整体改变。本套教材把 5 种形态各做成一个站：
      <b>%d 页 HTML ＋ %d 个手顺步骤 ＋ %d 张画面 ＋ Excel</b>（うち %d 张は sap_sd_jp / sap_sd_cn の<b>実機スクリーンショット</b>、残りは生成した画面イメージ）（要件定義・手順書 / 学習WBS / 画面撮影リスト）。
      全部静态、无外部依赖、可离线打开。<span class="mini">数字由 tools/make_hub_page.py 自动统计</span></p>
  </div>
</div>

<div class="wrap">
<main class="page"><article>

<h2 id="sites">%d 个站（点击站名直接打开）</h2>
<div class="grid cards">
%s
    <div class="card">
      <h3><a href="tools/README.md">tools/（共通工具）</a></h3>
      <p>画面イメージの生成・検証、学習WBS と要件定義 Excel の生成、実機スクリーンショットへの差し替えまでを 11 のスクリプトで。</p>
      <div class="tags"><span class="tag gray">verify_all_sites</span><span class="tag gray">make_gui_mockups</span><span class="tag gray">swap_gui_images</span></div>
      <p class="mini"><a href="tools/README.md">tools/README.md</a> ／ <a href="tools/GUI_SPEC_FORMAT.md">GUI_SPEC_FORMAT.md</a> ／ <a href="PROGRESS.md">PROGRESS.md（進捗メモ）</a></p>
    </div>
</div>

<h2 id="route">推荐学习路线</h2>
<ol class="steps">
  <li><b>⓪ SAP S/4HANA 日本語実習サイト（sap_sd_jp）</b>——<b>日本語で読める全モジュール手順サイト</b>：FI / CO / MM / PP / SD の 6 大モジュール・222 タスクの手順と実機画面。画面は中国語インターフェースのため、各ステップに「原文（中国語）」の折りたたみと用語対照表を用意。先にここで「どの設定ポイントがあるか」の地図を持っておくと、以下の各站が速い。（中国語の原文で読みたい場合は <b>sap_sd_cn</b> が同一教材の原文版。）</li>
  <li><b>① SD 培训课程（sap_cn）</b>——<b>中文的 SD 专项课程</b>：从概念（为什么 SD 会这样设计）到端到端流程（询价·报价·订单·交货·发货过账·开票·收款）、再到 48 个配置任务。每个环节都配真实 SAP GUI 中文界面截图与自绘的思维导图/流程图/结构图，可当「上台讲课的底稿」直接用（讲师版・学员记入表・30 题自测・Excel 8 表）。</li>
  <li><b>①' 全模块培训课件（sap_modules_cn）</b>——中文的 <b>MM / PP / FI / CO 四模块课程</b>（每模块 14 页）：概念 → 组织结构 → 主数据 → 端到端流程 → 三篇操作手顺（教材全部 172 个任务逐个走查，含 IMG 路径与原始画面）→ SPRO 配置 → 实训 → 讲师版/学员版/自测/术语。与 ① sap_cn（SD）合起来，就是「除 SD 以外的模块」的课件。</li>
  <li><b>② SD 受注処理（sap_sd）</b>——先看录像（SAP Education Unit 14）配套的受注处理站：值从哪来（主数据／既存伝票／Customizing／ABAP）、出荷プラント的优先顺序、明細カテゴリ决定、变更时的再决定。后面的每一站都建立在这里。</li>
  <li><b>③ MTO（sapmto）</b>——接着把「决定链」和受注在庫 E 吃下来。这是所有形态的基准，之后每个形态都拿它对照。</li>
  <li><b>④ ETO（sapeto）</b>——同一件受注换成「案件（WBS）＋ プロジェクト在庫 Q」再走一遍，体会月末处理（進捗 → 結果分析 → 決済）的差别。</li>
  <li><b>⑤ 横断比较（saporderflow）</b>——E 与 Q 的 STEP 对照表 + 9 维度矩阵，把 ②③ 的经验整理成「选型判断」。</li>
  <li><b>⑥ MTS（sapmts）</b>——换成预测驱动（PIR・自由在庫・標準原価），理解「受注 vs 見込」的分界。</li>
  <li><b>⑦ VC（sapvc）</b>——最后学「构成引擎」：1 品目表现多种规格，靠依存关系控制 BOM 与价格。</li>
</ol>
<div class="box info"><b class="t">按角色的短路线</b>
<b>SD 担当</b>：<b>sap_cn</b>（中文课程：概念 → 流程 → 配置，可当讲课底稿）＋ sap_sd の全体（受注・変更・照会・出荷/請求）＋ 各站の concept ＋ 练习①〜③。<br>
<b>PP 担当</b>：各站的 concept ＋ 练习②〜④（MRP・指図・入出庫）。<br>
<b>CO / 管理会計</b>：ETO 的①〜⑤（予算・可用性管理・結果分析・決済）＋ MTS の標準原価と差異。<br>
<b>要件定義・コンサル</b>：saporderflow の横断比较 ＋ 各站の 讲师版（采分点・必出 Q&A）＋ 故障対照表。</div>

<h2 id="tools">工具与验证（每个站都能自检）</h2>
<div class="file-tree">
tools/
├── verify_all_sites.py          6 站一张表（结构＋GUI 覆盖＋容器健全性）
├── make_gui_mockups.py          spec → SVG → 手顺页面へ挿入（冪等）
├── verify_gui_figures.py        手顺ステップの網羅（spec 駆動）
├── check_gui_render.py          Chrome で栅格化して「本当に描けているか」を確認
├── check_gui_overlap.py         注記が文字に重なっていないか
├── pair_gui_figures.py          E / Q 対比を 2 カラムで並べる
├── add_gui_note.py              「実機スクリーンショットではない」注意書き
├── swap_gui_images.py           実機で撮った画像に一括差し替え（--apply / --revert）
├── export_gui_capture_list.py   画面撮影リスト（CSV / XLSX）
├── make_wbs_xlsx.py             学習WBS（受講者版）— 打勾式の進捗表
└── GUI_SPEC_FORMAT.md / README.md
</div>
<pre class="vals"># 一括検証（まずはこれ）
cd ~/Desktop/work/training
python3 tools/verify_all_sites.py

# 実機のスクリーンショットに差し替えるとき
① 撮影リスト（&lt;CODE&gt;_画面撮影リスト.xlsx）を見ながら実機で撮影
② 同じベース名の .png を &lt;site&gt;/assets/gui/ に置く
③ python3 tools/swap_gui_images.py &lt;site&gt; --apply</pre>

<h2 id="stance">立場と注意</h2>
<div class="box ok"><b class="t">sap_sd_jp / sap_sd_cn / sap_modules_cn / sap_cn の画面は実機スクリーンショット</b>
これらの站の画面は教材 Word 文档（S4.docx）から抽出した<b>実機のスクリーンショット</b>（中国語インターフェースの SAP GUI）です。sap_sd_jp はその日本語版（本文は日本語、画面は中国語のまま＋原文併記）、sap_sd_cn は原文の中国語版、sap_modules_cn は同じ教材の MM / PP / FI / CO 四模块を中文课程化したもの（各モジュール 14 页）、sap_cn はその SD 部分の中文课程です。残りの站（sap_sd / sapmto / sapeto / sapmts / sapvc / saporderflow）は下記のとおり生成した画面イメージです。</div>
<div class="box warn"><b class="t">画面イメージについて</b>
各ステップの画像は <b>SAP GUI の標準レイアウトを再現した図</b>で、<b>実機のスクリーンショットではありません</b>。
フィールド名・順序・ボタン位置はリリースとカスタマイズで変わります。各ページの「自システムでの確認」に確認用の T-code と表を書いています。</div>
<div class="box danger"><b class="t">標準値について</b>
業務サイトはコンパイル検証できないため、標準値は「出典付き」か「通常は〜（自システムで確認）」で記載しています。
断定を避けたフィールド名（例：所要量クラスの評価区分、<code>OVZI</code> の origin 値、変種価格のキー構造）は、実機での確認を前提にしてください。</div>

<h2>规模一览（自动统计）</h2>
<table class="tbl wide">
<tr><th>站</th><th>页数</th><th>手顺ステップ</th><th>画面イメージ</th><th>Excel</th><th>学習WBS</th></tr>
%s
<tr><td><b>合计</b></td><td><b>%d</b></td><td><b>%d</b></td><td><b>%d</b></td><td colspan="2">要件定義・手順書 / 講義テキスト ＋ 学習WBS（受講者版）＋ 画面撮影リスト</td></tr>
</table>

<div class="box ok"><b class="t">再生成の方法</b>
各站: <code>python3 tools/make_gui_mockups.py &lt;site&gt;</code>（画面）/ <code>cd &lt;site&gt; &amp;&amp; python3 tools/make_*_xlsx.py</code>（要件定義）/ <code>python3 tools/make_wbs_xlsx.py</code>（学習WBS）/ <code>python3 tools/make_hub_page.py</code>（この页）。</div>

</article>
</main>
</div>

<footer class="site"><div class="inner">
  <div><h5>SAP 培训教材 索引</h5><p>全モジュール手順（日本語版 / 中国語原文版）／受注処理（SD）／受注生産（MTO）／受注設計生産（ETO）／見込生産（MTS）／バリアント設定（VC）／受注形態の横断比較。</p></div>
  <div class="cols">
    <div><h5>站点</h5>
      <a href="sap_sd_jp/index.html">全モジュール（日本語）</a><br><a href="sap_sd_cn/index.html">全モジュール（中文）</a><br>
      <a href="sap_sd/index.html">受注処理</a><br><a href="sapmto/index.html">MTO</a><br><a href="sapeto/index.html">ETO</a><br>
      <a href="sapmts/index.html">MTS</a><br><a href="sapvc/index.html">VC</a><br><a href="saporderflow/index.html">横断比較</a></div>
    <div><h5>ドキュメント</h5>
      <a href="tools/README.md">tools/README.md</a><br><a href="tools/GUI_SPEC_FORMAT.md">GUI_SPEC_FORMAT.md</a><br><a href="PROGRESS.md">PROGRESS.md</a></div>
  </div>
</div></footer>
<script src="assets/main.js"></script>
</body>
</html>
""" % (len(ORDER), len(ORDER), tot_pages, tot_steps, tot_figs, real_figs, len(ORDER), "\n".join(cards), rows, tot_pages, tot_steps, tot_figs)

    out = os.path.join(ROOT, "index.html")
    open(out, "w", encoding="utf-8").write(html)
    print("generated: %s  (pages=%d, steps=%d, figures=%d)" % (os.path.relpath(out, ROOT), tot_pages, tot_steps, tot_figs))
    for s in ORDER:
        print("   %-14s pages=%2d steps=%2d figs=%3d xlsx=%d" % (s, data[s]["n_pages"], data[s]["n_steps"], data[s]["figs"], len(data[s]["xlsx"])))


if __name__ == "__main__":
    main()
