# -*- coding: utf-8 -*-
"""SAP 模块培训课程站（MM / PP / FI / CO）—— 公共骨架与组件。

设计原则（与训练目录里其它站一致）：
  - 纯静态 HTML，无外部依赖，file:// 直接可开
  - 真实截图取自教材文档 S4.docx（原文件名保留在 figcaption，可回 Word 原稿逐张核对）
  - 自绘图是本站用纯 Python 生成的 SVG（assets/diagrams/<模块>/*.svg），页面上标注「本站自绘」

目录布局：站点根 = sap_modules_cn/，每个模块一个子目录（mm/ pp/ fi/ co/），
共享 assets/ 在根下，所以模块页面里的资源路径前缀是 "../assets/…"。
"""
import html
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
WORK = os.path.join(ROOT, "work")

CFG = json.load(open(os.path.join(WORK, "modules.json"), encoding="utf-8"))
SLOTS = CFG["slots"]
MODULES = CFG["modules"]
BY_CODE = dict((m["code"], m) for m in MODULES)
MODEL = json.load(open(os.path.join(WORK, "modules_model.json"), encoding="utf-8"))
MANIFEST = json.load(open(os.path.join(WORK, "img_manifest.json"), encoding="utf-8"))

# 导航槽位 → 默认标签（proc1..3 由每个模块自己的 proc 定义覆盖）
SLOT_LABEL = CFG["slot_label"]

# 截图在 assets/img/ 下按模块分目录；教材里一个模块的任务偶尔会引用别的模块的画面
# （例如 MM 的发票校验任务里贴了 FI 的画面），所以路径要按「第一段是不是模块名」来判断。
IMG_ROOTS = set(m["code"] for m in MODULES) | {"prep"}


# --------------------------------------------------------------------------
# 模块上下文
# --------------------------------------------------------------------------
class Ctx(object):
    """一个模块的全部数据 + 页面里要用的取数/组件函数。"""

    def __init__(self, code):
        self.code = code
        self.meta = BY_CODE[code]
        self.tasks = MODEL[code]["tasks"]
        self.task_map = dict((t["no"], t) for t in self.tasks)
        self.img_pre = "../assets/img/"
        self.dia_pre = "../assets/diagrams/%s/" % code
        self.fig_no = 0          # 页面内「画面 N」的计数器（每页重置）

    # ---- 页面生命周期 ----
    def reset_fig(self):
        self.fig_no = 0

    def next_fig(self):
        self.fig_no += 1
        return self.fig_no

    # ---- 教材任务取数 ----
    def task(self, no):
        return self.task_map[no]

    def tasks_of(self, nos):
        return [self.task(n) for n in nos]

    def simg(self, no, step=1, k=0):
        """第 no 个任务、第 step 步、第 k 张截图的相对路径；没有则 None。"""
        steps = self.task(no)["steps"]
        if not steps:
            return None
        imgs = steps[min(step, len(steps)) - 1].get("imgs") or []
        if not imgs:
            return None
        return self.rel(imgs[min(k, len(imgs) - 1)])

    def scap(self, no, step=1):
        steps = self.task(no)["steps"]
        if not steps:
            return ""
        return steps[min(step, len(steps)) - 1].get("caption", "") or ""

    def spath(self, no):
        return self.task(no).get("path") or ""

    def stc(self, no):
        return self.task(no).get("tcodes") or []

    def ssteps(self, no):
        return self.task(no)["steps"]

    def snames(self, no):
        """任务里出现的画面（去重、保序）。"""
        out, seen = [], set()
        for i, st in enumerate(self.task(no)["steps"], 1):
            for p in st.get("imgs") or []:
                if p not in seen:
                    seen.add(p)
                    out.append((i, self.rel(p), st.get("caption", "") or ""))
        return out

    def src_ref(self, no):
        return "教材《S4.docx》· %s 任务 %02d %s" % (self.code.upper(), no, self.task(no)["title"])

    def task_nav(self, no, text=None):
        """指向配置页里该任务锚点的站内链接。"""
        return '<a href="config.html#t%02d">%s</a>' % (no, esc(text or ("任务 %02d %s" % (no, self.task(no)["title"]))))

    # ---- 组件（绑定本模块前缀）----
    def key(self, p):
        """统一成 assets/img/ 下的相对键：带模块前缀的原样保留，否则补本模块前缀。"""
        if not p:
            return p
        return p if p.split("/")[0] in IMG_ROOTS else "%s/%s" % (self.code, p)

    rel = key  # 兼容旧名

    def shot(self, rel, no=None, cap="", src="", cls="", task=None):
        return shot(self, self.key(rel), no=no, cap=cap, src=src, cls=cls, task=task)

    def shot_grid(self, items, cls=""):
        return shot_grid(self, items, cls=cls)

    def dia(self, name, cap="", kind="自绘流程图", alt=None, wide=False):
        return diagram(name, cap, kind=kind, pre=self.dia_pre, alt=alt, wide=wide)


# --------------------------------------------------------------------------
# 小工具
# --------------------------------------------------------------------------
def esc(s):
    return html.escape(str(s), quote=False)


def href(file, anchor=None):
    return file + ("#" + anchor if anchor else "")


def _img_attrs(path):
    m = MANIFEST.get(path)
    if not m:
        raise KeyError("截图不在 manifest 中（assets/img/%s）：先跑 tools/prep_data.py" % path)
    return m["w"], m["h"], m["orig"]


def shot(ctx, rel, no=None, cap="", src="", cls="", task=None):
    """真实系统截图。rel 是 assets/img/ 下的相对键（如 mm/t22/01_1_image612.png），
    允许只写模块内部分（t22/01_1_image612.png），会自动补本模块前缀。"""
    full = ctx.key(rel) if hasattr(ctx, "key") else rel
    w, h, orig = _img_attrs(full)
    if no is None:
        no = ctx.next_fig()
    if not src:
        tno = task
        if tno is None:
            m = MANIFEST[full]
            tno = m.get("task")
        if tno and tno in ctx.task_map:
            src = "%s · 原图 %s" % (ctx.src_ref(tno), orig)
        else:
            src = "教材《S4.docx》· 原图 %s" % orig
    narrow = " narrow" if h <= 160 else ""
    return (
        '<figure class="shot%s%s">'
        '<a class="zoom" href="%s%s" title="点击放大（1×~4×，ESC 关闭）">'
        '<img src="%s%s" width="%d" height="%d" alt="%s" loading="lazy"></a>'
        '<figcaption><span class="n">画面 %s</span><span class="cap">%s</span>'
        '<span class="src">%s</span></figcaption></figure>'
    ) % (narrow, (" " + cls if cls else ""), ctx.img_pre, full, ctx.img_pre, full, w, h,
         esc(cap or "SAP GUI 实机截图"), no, cap, esc(src))


def shot_grid(ctx, items, cls=""):
    """items = [(rel, cap)] 并排小图，画面编号自动 +1。"""
    inner = "".join(shot(ctx, ctx.key(p), cap=c) for p, c in items)
    return '<div class="shot-grid%s">%s</div>' % (" " + cls if cls else "", inner)


def diagram(name, cap="", kind="自绘流程图", pre="", alt=None, wide=False):
    cls = "wide" if wide else ""
    return (
        '<figure class="dia%s"><a class="zoom" href="%s%s.svg">'
        '<img src="%s%s.svg" alt="%s" loading="lazy"></a>'
        '<figcaption><span class="n">%s</span><span class="cap">%s</span>'
        '<span class="src">本站自绘 SVG</span></figcaption></figure>'
    ) % ((" " + cls if cls else ""), pre, name, pre, name, esc(alt or cap or name), kind, cap)


def note(kind, title, text):
    return '<div class="note %s"><span class="t">%s</span>%s</div>' % (kind, esc(title), text)


def box(kind, title, inner):
    return '<div class="box %s"><b class="t">%s</b>%s</div>' % (kind, esc(title), inner)


def pathline(label, path, copyable=True):
    attr = ' data-copy="%s"' % esc(path) if copyable else ""
    return '<div class="pathline"%s><b>%s</b>%s</div>' % (attr, esc(label), esc(path))


def route(items):
    """一行「菜单路径」的紧凑写法：列表项按 → 连接。"""
    return '<div class="route">%s</div>' % " → ".join("<b>%s</b>" % esc(x) for x in items)


def tbl(headers, rows, cls="tbl", row_attrs=None, tid=None, first_mono=False):
    th = "".join("<th>%s</th>" % h for h in headers)
    trs = []
    for i, r in enumerate(rows):
        tds = []
        for c in r:
            if isinstance(c, tuple):
                c, klass = c
            else:
                klass = ""
            tds.append('<td%s>%s</td>' % (' class="%s"' % klass if klass else "", c))
        ra = ""
        if row_attrs is not None and i < len(row_attrs) and row_attrs[i]:
            ra = " " + row_attrs[i]
        trs.append("<tr%s>%s</tr>" % (ra, "".join(tds)))
    klass = cls + (" idx" if first_mono else "")
    idattr = ' id="%s"' % tid if tid else ""
    return ('<div class="tblwrap"><table class="%s"%s><thead><tr>%s</tr></thead>'
            '<tbody>%s</tbody></table></div>') % (klass, idattr, th, "".join(trs))


def oplist(items, start=1):
    lis = []
    for it in items:
        if isinstance(it, tuple):
            txt, kind = it
        else:
            txt, kind = it, ""
        lis.append('<li class="%s">%s</li>' % ("is-note" if kind == "note" else "", txt))
    return '<ol class="oplist" start="%d">%s</ol>' % (start, "".join(lis))


def steps_list(items, cls=""):
    return '<ol class="steps%s">%s</ol>' % ((" " + cls if cls else ""),
                                            "".join("<li>%s</li>" % x for x in items))


def steph(no, title, tags=None, anchor=None):
    t = "".join('<span class="%s">%s</span>' % (k, esc(v)) for k, v in (tags or []))
    return ('<div class="steph" id="%s"><span class="no">%s</span><h3>%s</h3>%s</div>'
            % (anchor or ("s" + str(no)), esc(no), esc(title), t))


def toc(items):
    return '<div class="toc">%s</div>' % "".join(
        '<a href="#%s">%s</a>' % (a, esc(t)) for t, a in items)


def cards(items):
    inner = "".join('<div class="card"><b>%s</b><span>%s</span></div>' % (b, s) for b, s in items)
    return '<div class="grid cards">%s</div>' % inner


def stat_cards(items):
    """[(数字, 单位, 说明)] -> 统计卡"""
    inner = ""
    for n, unit, desc in items:
        inner += ('<div class="card"><b>%s</b><span>%s</span><small>%s</small></div>'
                  % (n, unit, desc))
    return '<div class="grid cards stats">%s</div>' % inner


def modcards(items):
    """模块卡片（首页/枢纽页用）。items = [(href, 标题, 正文, meta, 配色类)]"""
    inner = ""
    for h, title, body, meta, accent in items:
        inner += ('<div class="modcard %s"><h3><a href="%s">%s</a></h3><p>%s</p>'
                  '<div class="meta">%s</div></div>') % (accent, h, title, body, meta)
    return '<div class="modlist">%s</div>' % inner


def flowchart(items):
    """横向流程图（共享 style.css 的 .flow/.node/.arrow）。

    items = [(标题, 说明)]，最后一项之后不画箭头。
    """
    out = []
    for i, it in enumerate(items):
        title, sub = (it if isinstance(it, tuple) else (it, ""))
        out.append('<span class="node"><b>%s</b>%s</span>' % (title, sub))
        if i < len(items) - 1:
            out.append('<span class="arrow">→</span>')
    return '<div class="flow">%s</div>' % "".join(out)


# --------------------------------------------------------------------------
# 导航 / 页面骨架
# --------------------------------------------------------------------------
def nav_of(ctx, pages):
    """pages = 模块的 PAGES 列表（按教学顺序）。返回 [(file, label, tip)]。"""
    procs = dict((p["file"], p) for p in ctx.meta["procs"])
    out = []
    for pg in pages:
        slot = pg["slot"]
        if slot.startswith("proc"):
            p = procs[pg["file"]]
            label, tip = p["nav"], p["tip"]
        else:
            label = SLOT_LABEL[slot]
            tip = pg.get("tip", "")
        out.append((pg["file"], label, tip))
    return out


def nav_html(nav, active):
    return "\n      ".join(
        '<a%s href="%s" title="%s">%s</a>' % (' class="active"' if f == active else "", f, esc(t), esc(l))
        for f, l, t in nav)


def mod_switch(ctx, active_code=None):
    """顶部模块切换条：MM / PP / FI / CO + 课程总览。"""
    active_code = active_code or ctx.code
    out = []
    for m in MODULES:
        cls = " chip on" if m["code"] == active_code else " chip"
        out.append('<a class="%s" href="../%s/index.html" title="%s">%s %s</a>'
                   % (cls.strip(), m["code"], esc(m["site_title"]), m["brand"], m["name_cn"]))
    out.append('<a class="chip" href="../index.html" title="四个模块的总体视图与学习路线">总览</a>')
    return '<div class="filterbar modsw">%s</div>' % "".join(out)


def shell(ctx, pages, file, title, kicker, body, desc=None, breadcrumb=None):
    nav = nav_of(ctx, pages)
    assert any(f == file for f, _l, _t in nav), "页面 %s 不在 PAGES 里" % file
    meta = ctx.meta
    others = "".join('<a href="../%s/index.html">%s %s</a> · ' % (m["code"], m["brand"], m["name_cn"])
                     for m in MODULES if m["code"] != ctx.code)
    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%(title)s · %(stitle)s</title>
<meta name="description" content="%(desc)s">
<link rel="stylesheet" href="../assets/style.css">
<link rel="stylesheet" href="../assets/mod.css">
</head>
<body>
<header class="site">
  <div class="nav-wrap">
    <a class="brand" href="index.html"><span class="logo">%(logo)s</span><span class="txt">培训课程</span></a>
    <nav class="main">
      %(nav)s
    </nav>
  </div>
</header>

<div class="wrap">
<main class="page">
<article>
<p class="breadcrumb">%(crumb)s</p>
%(modsw)s
<h1>%(title)s</h1>
<p class="kicker">%(kicker)s</p>
%(body)s
</article>
</main>
</div>

<footer class="site">
  <div class="inner">
    <div class="cols">
      <div>
        <h5>%(stitle)s</h5>
        <p>%(subtitle)s</p>
        <p>课程总览：<a href="../index.html">SAP 模块培训课程（MM · PP · FI · CO）</a></p>
      </div>
      <div>
        <h5>课程板块</h5>
        <p><a href="concept.html">概念</a> · <a href="org.html">组织</a> ·
        <a href="master.html">主数据</a> · <a href="flow.html">流程</a> ·
        <a href="%(proc1)s">%(proc1nav)s</a> · <a href="config.html">配置</a></p>
      </div>
      <div>
        <h5>课堂配套</h5>
        <p><a href="practice.html">实训任务</a> · <a href="instructor.html">讲师版</a> ·
        <a href="worksheet.html">学员版</a> · <a href="quiz.html">自测</a> ·
        <a href="glossary.html">术语表</a></p>
      </div>
      <div>
        <h5>看图说话</h5>
        <p>截图取自教材《S4.docx》的真实 SAP GUI 画面（中文界面，保留原文件名可回查）；
        流程图、结构图、思维导图为本站自绘 SVG。标准值随版本/行业方案而异，
        页面标注的「在自系统里怎么确认」请在自己的系统里核对。</p>
        <p>其他模块：%(others)s</p>
      </div>
    </div>
    <p class="copy">© <span data-year>2026</span> %(stitle)s · 静态站点，可离线使用</p>
  </div>
</footer>
<script src="../assets/main.js"></script>
<script src="../assets/quiz.js"></script>
<script src="../assets/mod.js"></script>
</body>
</html>
""" % {
        "title": esc(title), "stitle": esc(meta["site_title"]), "subtitle": esc(meta["subtitle"]),
        "desc": esc(desc or meta["desc"]), "logo": meta["brand"], "nav": nav_html(nav, file),
        "modsw": mod_switch(ctx), "crumb": breadcrumb or ('<a href="index.html">课程地图</a> / <span>%s</span>' % esc(title)),
        "kicker": esc(kicker), "body": body, "proc1": meta["procs"][0]["file"],
        "proc1nav": meta["procs"][0]["nav"], "others": others,
    }
