# -*- coding: utf-8 -*-
"""sap_sd（SAP SD 受注処理 / Sales Order Processing）培训站 —— 公共骨架与组件。

页面 = 完整文档骨架（head + header/nav + wrap/article + footer），由本模块拼装。
nav 只在这里定义一次，所有页面共用（verify_site.py 要求各页 nav 完全一致且只有 1 个 active）。
"""

SITE_NAME = "SAP SD 受注処理（Sales Order Processing）实战训练站"
BRAND_LOGO = "SD"
BRAND_TXT = "受注処理 训练站"
CSS = ["assets/style.css", "assets/sd.css"]

# (file, 短标签) —— 顺序即导航顺序
NAV = [
    ("index.html", "总览"),
    ("concept.html", "概念与设计"),
    ("config.html", "配置手顺"),
    ("handson-1.html", "①受注登録"),
    ("handson-2.html", "②伝票変更"),
    ("handson-3.html", "③情報照会"),
    ("handson-4.html", "④出荷と請求"),
    ("handson-5.html", "⑤ツールと故障"),
    ("instructor.html", "讲师版"),
    ("worksheet.html", "学员版"),
    ("quiz.html", "能力测试"),
]

PAGE_TITLE = {
    "index.html": "总览",
    "concept.html": "概念与设计",
    "config.html": "配置手顺",
    "handson-1.html": "练习① 受注登録（VA01）",
    "handson-2.html": "练习② 伝票の変更と再決定",
    "handson-3.html": "练习③ 販売情報システム（Sales Summary）",
    "handson-4.html": "练习④ 出荷と請求",
    "handson-5.html": "练习⑤ ツール・発展・故障対応",
    "instructor.html": "讲师版",
    "worksheet.html": "学员版",
    "quiz.html": "能力测试",
}


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


# ---------------------------------------------------------------- 骨架
def header(active):
    items = []
    for f, label in NAV:
        cls = ' class="active"' if f == active else ""
        items.append('      <a%s href="%s">%s</a>' % (cls, f, label))
    return ('''<header class="site">
  <div class="nav-wrap">
    <a class="brand" href="index.html"><span class="logo">%s</span><span class="txt">%s</span></a>
    <nav class="main">
%s
    </nav>
  </div>
</header>''' % (BRAND_LOGO, BRAND_TXT, "\n".join(items)))


def footer(desc, next_html=None):
    nxt = ''
    if next_html:
        nxt = ('<div><h5>下一步</h5><p>%s</p></div>' % next_html)
    return ('''<footer class="site"><div class="inner">
  <div><h5>%s</h5><p>%s</p>%s</div>
  <div class="cols">
    <div><h5>练习</h5><a href="handson-1.html">① 受注登録（VA01）</a><br><a href="handson-2.html">② 与力価格と ATP</a><br><a href="handson-3.html">③ 特殊取引</a><br><a href="handson-4.html">④ 出荷と請求</a><br><a href="handson-5.html">⑤ 発展と故障対応</a></div>
    <div><h5>其他</h5><a href="index.html">总览</a><br><a href="concept.html">概念与设计</a><br><a href="config.html">配置手顺</a><br><a href="instructor.html">讲师版</a><br><a href="worksheet.html">学员版</a><br><a href="quiz.html">能力测试</a></div>
  </div>
</div></footer>''' % (SITE_NAME, desc, nxt))


def page(fname, title, desc, body, crumb=None, foot=None, foot_next=None, hero=None,
         has_figures=False, gui_note=True):
    """拼装一页。fname = 输出文件名，title = <title> 与 h1 之外的部分。"""
    links = "\n".join('<link rel="stylesheet" href="%s">' % c for c in CSS)
    cr = ('<div class="breadcrumb"><a href="index.html">总览</a> / %s</div>\n' % crumb) if crumb else ''
    herohtml = ''
    if hero:
        herohtml = '\n<div class="hero"><div class="hero-inner">%s</div></div>\n' % hero
    note = ''
    if has_figures and gui_note:
        note = GUI_NOTE
    return ('''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%s · %s</title>
<meta name="description" content="%s">
%s
</head>
<body>
%s
%s
<div class="wrap">
%s<main class="page"><article>

%s%s

</article>
</main>
</div>

%s
<script src="assets/main.js"></script>
<script src="assets/quiz.js"></script>
</body>
</html>
''' % (title, SITE_NAME, esc(desc).replace('"', "&quot;"), links, header(fname), herohtml,
       cr, note, body, footer(foot or "", foot_next)))


GUI_NOTE = ('<div class="gui-note" data-gui-note="1"><b>关于本页的「画面イメージ」</b>：'
            '这些图是按 SAP GUI 标准布局重绘的<b>示意图</b>，不是实机截图。'
            '字段名、字段顺序、按钮位置会因版本与自定义而不同，请以自系统的画面为准'
            '（各 STEP 的「自系统での確認方法」里写了确认用的 T-code 与表）。'
            '录像里的画面同样可能与你的版本不同。若要换成实机截图，把同名 <code>.png</code> 放进 '
            '<code>assets/gui/</code> 后执行 <code>python3 tools/swap_gui_images.py &lt;site&gt; --apply</code> 一键替换。</div>')


# ---------------------------------------------------------------- 组件
def steph(cid, no, title, tcode=""):
    tc = ('<span class="tc">%s</span>' % tcode) if tcode else ''
    return ('<div class="steph" id="%s"><span class="no">%s</span><h3>%s</h3>%s</div>'
            % (cid, no, title, tc))


def kv(pairs):
    out = ['<dl class="kv">']
    for k, v in pairs:
        out.append('  <dt>%s</dt>\n  <dd>%s</dd>' % (k, v))
    out.append('</dl>')
    return "\n".join(out)


def steps(items):
    return '<ol class="steps">\n' + "\n".join('  <li>%s</li>' % i for i in items) + '\n</ol>'


def box(kind, title, html):
    return '<div class="box %s"><b class="t">%s</b>\n%s</div>' % (kind, title, html)


def task(html):
    return '<div class="task"><b class="t">練習課題</b>%s</div>' % html


def checklist(items):
    return '<ul class="check">\n' + "\n".join('  <li>%s</li>' % i for i in items) + '\n</ul>'


def tbl(headers, rows, cls="tbl wide", first_nowrap=True):
    h = "".join('<th>%s</th>' % x for x in headers)
    out = ['<table class="%s">' % cls, '<tr>%s</tr>' % h]
    for r in rows:
        out.append('<tr>' + "".join('<td>%s</td>' % c for c in r) + '</tr>')
    out.append('</table>')
    return "\n".join(out)


def vals(text):
    return '<pre class="vals">%s</pre>' % esc(text)


def h2(text, hid=None):
    i = ' id="%s"' % hid if hid else ''
    return '<h2%s>%s</h2>' % (i, text)


def h3(text):
    return '<h3>%s</h3>' % text


def toc(pairs):
    return '<div class="toc">\n' + "\n".join('  <a href="#%s">%s</a>' % (a, t) for a, t in pairs) + '\n</div>'


def flow(nodes):
    parts = []
    for i, n in enumerate(nodes):
        if i:
            parts.append('<div class="arrow">→</div>')
        parts.append('<div class="node">%s</div>' % n)
    return '<div class="flow">\n  ' + "\n  ".join(parts) + '\n</div>'


def quiz_q(n, tag, tagcls, question, options, answer, explain):
    opts = "\n".join('    <div class="opt" data-key="%s">%s</div>' % (k, v) for k, v in options)
    return ('''<div class="quiz-q" data-answer="%s">
  <div class="q-meta"><span class="tag %s">%s</span></div>
  <h4>%d. %s</h4>
  <div class="opts">
%s
  </div>
  <div class="explain">%s</div>
</div>''' % (answer, tagcls, tag, n, question, opts, explain))


def cards(items):
    out = ['<div class="grid cards">']
    for title, body, tags in items:
        tg = "".join('<span class="tag %s">%s</span>' % (c, t) if c else '<span>%s</span>' % t
                     for t, c in tags)
        out.append('  <div class="card">\n    <h3>%s</h3>\n    <p>%s</p>\n    <div class="tags">%s</div>\n  </div>'
                   % (title, body, tg))
    out.append('</div>')
    return "\n".join(out)
