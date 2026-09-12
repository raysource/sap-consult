# -*- coding: utf-8 -*-
"""站点生成公共工具: 页面外壳 / 代码块 / 常见小组件"""
import html as _html

SITE_TITLE = "SAP BTP 开发者训练站"
NAV = [
    ("index.html", "首页", "index"),
    ("isuite.html", "Integration Suite", "isuite"),
    ("iflow.html", "iFlow 实战", "iflow"),
    ("rap.html", "RAP", "rap"),
    ("cap.html", "CAP", "cap"),
    ("fiori.html", "Fiori / UI5", "fiori"),
    ("dev-course.html", "全流程课件", "devcourse"),
    ("samples.html", "示例工程", "samples"),
]

DOC_LINKS = [
    ("SAP BTP 帮助中心", "https://help.sap.com/docs/btp"),
    ("Integration Suite", "https://help.sap.com/docs/integration-suite"),
    ("Cloud Integration", "https://help.sap.com/docs/cloud-integration"),
    ("CAP (capire)", "https://cap.cloud.sap/docs/"),
    ("SAPUI5", "https://sapui5.hana.ondemand.com/"),
    ("ABAP 开发用户指南", "https://help.sap.com/docs/btp/sap-abap-development-user-guide"),
]


def esc(s):
    return _html.escape(s, quote=True)


def pre(lang, src, label=None):
    """代码块(自动 HTML 转义)。lang 用于着色与角标。"""
    body = esc(src.rstrip("\n"))
    lang_name = {
        "xml": "XML", "json": "JSON", "cds": "CDS", "js": "JavaScript",
        "groovy": "Groovy", "java": "Java", "abap": "ABAP", "yaml": "YAML",
        "sql": "SQL", "bash": "Shell", "text": "Text", "csv": "CSV",
    }.get(lang, lang.upper())
    head = '<div class="code-head"><span class="lang">%s</span><button class="copy-btn" type="button">复制</button></div>' % lang_name
    return ('<pre class="hl"><div class="code-head"><span class="lang">%s</span>'
            '<button class="copy-btn" type="button">复制</button></div>'
            '<code class="lang-%s">%s</code></pre>') % (lang_name, lang, body)


def prex(lang, src, label=None):
    """无 lang 高亮需求的原始 <pre> 变体(文件树等)"""
    body = esc(src.rstrip("\n"))
    return '<pre class="hl"><div class="code-head"><span class="lang">%s</span><button class="copy-btn" type="button">复制</button></div><code class="lang-text">%s</code></pre>' % (label or lang.upper(), body)


def shell(title, desc, active_key, body_html):
    """完整 HTML 页面外壳: head / 导航 / 主体 / 页脚"""
    nav_links = []
    for fname, text, key in NAV:
        cls = ' class="active"' if key == active_key else ""
        nav_links.append('<a%s href="%s">%s</a>' % (cls, fname, text))
    doc_items = "".join('<li><a href="%s" target="_blank" rel="noopener">%s ↗</a></li>' % (u, t)
                        for t, u in DOC_LINKS)
    html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%s · %s</title>
<meta name="description" content="%s">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<header class="site">
  <div class="nav-wrap">
    <a class="brand" href="index.html"><span class="logo">SAP</span><span class="txt">%s</span></a>
    <nav class="main">%s</nav>
  </div>
</header>
%s
<footer class="site">
  <div class="inner">
    <div>
      <h5>%s</h5>
      <p>面向培训/自学的中文资料站 · 代码与数据见 “示例工程” 页<br>
      内容基于公开官方文档整理，非 SAP 官方交付物，请以 help.sap.com / cap.cloud.sap 为准。</p>
      <p>© <span data-year>2026</span> 学习用途</p>
    </div>
    <div class="cols">
      <div><h5>官方文档</h5><ul style="margin:0;padding-left:18px">%s</ul></div>
    </div>
  </div>
</footer>
<script src="assets/main.js"></script>
</body>
</html>""" % (title, SITE_TITLE, esc(desc), SITE_TITLE, "".join(nav_links), body_html, SITE_TITLE, doc_items)
    return html


def hero_html(kicker, h1, lead, crumb=""):
    return ('<div class="hero"><div class="hero-inner">'
            '<div class="kicker">%s</div><h1>%s</h1>'
            '<p class="lead">%s</p></div></div>') % (kicker, h1, lead)


def article(body, toc_anchors=None):
    """正文容器 + 可选的目录 chips"""
    toc = ""
    if toc_anchors:
        links = "".join('<a href="#%s">%s</a>' % (a, t) for t, a in toc_anchors)
        toc = '<div class="toc">%s</div>' % links
    return '<main class="page"><div class="wrap"><article>%s%s</article></div></main>' % (toc, body)


def box(kind, title, inner_html):
    kinds = {"info": "提示", "warn": "注意", "danger": "警告", "ok": "验证通过"}
    return ('<div class="box %s"><b class="t">%s%s</b>%s</div>'
            % (kind, kinds.get(kind, ""), (" · " + title if title else ""), inner_html))


def h2(anchor, text):
    return '<h2 id="%s">%s</h2>' % (anchor, text)


def h3(text):
    return "<h3>%s</h3>" % text


def p(text):
    return "<p>%s</p>" % text


def cards_html(items):
    """items: list of (title, href, desc, [tags])"""
    out = ['<div class="grid cards">']
    for title, href, desc, tags in items:
        tags_html = "".join('<span class="tag %s">%s</span>' % ("", t) for t in tags)
        out.append('<div class="card"><h3><a href="%s">%s</a></h3><p>%s</p>'
                   '<div class="tags">%s</div></div>' % (href, title, desc, tags_html))
    out.append("</div>")
    return "".join(out)


def flow_html(nodes):
    """流程示意图: nodes 为列表, 元素为字符串; 空串表示普通, 以 → 连接"""
    cells = []
    for i, n in enumerate(nodes):
        if i:
            cells.append('<span class="arrow">→</span>')
        dim = ""
        if isinstance(n, tuple):
            n, dim = n
            if dim:
                dim = " dim"
        cells.append('<span class="node%s">%s</span>' % (dim, n))
    return '<div class="flow">%s</div>' % "".join(cells)
