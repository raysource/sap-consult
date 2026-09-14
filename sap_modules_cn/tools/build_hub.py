# -*- coding: utf-8 -*-
"""生成站点总览页 index.html（四个模块的总体视图 + 学习路线 + 规模统计）。

    python3 tools/build_hub.py

总览页的统计数字从 work/build_stats.json 读（由 build_pages.py 写出），不手写；
两张总览图由 svgkit 生成到 assets/diagrams/overview/。
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(HERE, "sitegen"))

import common  # noqa: E402
import svgkit  # noqa: E402
from common import CFG, MODULES, esc, flowchart, modcards, note, oplist, stat_cards, tbl, toc  # noqa: E402

STATS_DIR = os.path.join(ROOT, "work", "stats")

HUB_DIAGRAMS = [
    {"kind": "flow", "file": "e2e-chain.svg", "w": 1400,
     "title": "端到端业务链：四个模块怎么接力",
     "sub": "同一个业务从需求走到报表，交接点就是各模块的边界 —— 也是课程里反复讲的「集成点」",
     "steps": [
         {"no": "1", "t": "销售订单 VA01", "sub": "SD：客户要什么、要多少", "color": "blue"},
         {"no": "2", "t": "需求传递 / MRP", "sub": "PP·MM：需求变成生产与采购需求", "color": "teal"},
         {"no": "3", "t": "采购订单 ME21N", "sub": "MM：买原料（收货 101 进库存）", "color": "teal"},
         {"no": "4", "t": "生产订单 CO01", "sub": "PP：领料 261 → 确认 → 入库 101", "color": "teal"},
         {"no": "5", "t": "外向交货 VL01N", "sub": "SD：拣配 → 发货过账 601 出库存", "color": "blue"},
         {"no": "6", "t": "发票 VF01", "sub": "SD：开票 → 应收账款", "color": "blue"},
         {"no": "7", "t": "会计凭证 / 报表", "sub": "FI：总账、应收应付、资产负债表", "color": "green"},
         {"no": "8", "t": "成本与获利分析", "sub": "CO：成本中心、订单成本、差异", "color": "amber"},
     ],
     "note": "读这张图的方法：每一步都在问「这一步谁产生凭证、下一步谁要用」——"
             "课程里每个模块的「集成关系」一节，讲的就是这些箭头。"},
    {"kind": "chains", "file": "module-map.svg", "w": 1400,
     "title": "四个模块：输入 → 处理 → 输出",
     "sub": "每个模块都按同一套教学结构展开：概念 → 组织 → 主数据 → 流程 → 操作手顺 → 配置 → 实训",
     "items": [
         {"title": "MM 物料管理（42 个教材任务）", "color": "blue",
          "chain": ["请购 ME51N", "订单 ME21N", "收货 MIGO 101", "发票校验 MIRO", "库存 MMBE"],
          "texts": ["输入：需求（部门/MRP/SD）与主数据（物料/供应商/信息记录）；"
                    "输出：采购订单、物料凭证、发票凭证，以及自动生成的会计凭证。"]},
         {"title": "PP 生产计划（51 个教材任务）", "color": "teal",
          "chain": ["独立需求 MD61", "MRP MD02", "计划订单→生产订单", "发料 261 · 确认 CO11N", "入库 101 · 结算 KO88"],
          "texts": ["输入：销售需求与预测、BOM/工艺路线/工作中心；"
                    "输出：生产订单、产成品库存、订单成本与差异。"]},
         {"title": "FI 财务会计（45 个教材任务）", "color": "green",
          "chain": ["科目 FS00", "凭证 FB50/FB70/FB60", "收付款 F-28/F-53", "余额 FS10N/FD10N/FK10N", "报表 FSE2"],
          "texts": ["输入：所有模块的业务凭证（MM 收货、SD 开票、CO 结算）；"
                    "输出：总账、应收应付、资产负债表与损益表。"]},
         {"title": "CO 管理会计（34 个教材任务）", "color": "amber",
          "chain": ["成本中心 OKEON", "成本要素 KA01", "作业价格 KP26", "分配 KSV5 · 分摊 KSU5", "结算 KO88 · 报表"],
          "texts": ["输入：FI 的费用、MM 的领料与价差、PP 的订单工时与入库；"
                    "输出：成本中心报表、订单成本、产品成本与差异分析。"]},
     ]},
]


def build_diagrams():
    out_dir = os.path.join(ROOT, "assets", "diagrams", "overview")
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    rows = []
    for spec in HUB_DIAGRAMS:
        svg, claims = svgkit.build(spec)
        with io.open(os.path.join(out_dir, spec["file"]), "w", encoding="utf-8") as f:
            f.write(svg)
        rows.append({"file": spec["file"], "kind": spec["kind"], "overflow": claims})
    return rows


def dia(name, cap, kind):
    return ('<figure class="dia wide"><a class="zoom" href="assets/diagrams/overview/%s.svg">'
            '<img src="assets/diagrams/overview/%s.svg" alt="%s" loading="lazy"></a>'
            '<figcaption><span class="n">%s</span><span class="cap">%s</span>'
            '<span class="src">本站自绘 SVG</span></figcaption></figure>') % (name, name, esc(cap), kind, cap)


def read_stats():
    out = {}
    if os.path.isdir(STATS_DIR):
        for fn in sorted(os.listdir(STATS_DIR)):
            if fn.endswith(".json"):
                try:
                    out[fn[:-5]] = json.load(open(os.path.join(STATS_DIR, fn), encoding="utf-8"))
                except ValueError:
                    pass
    return out


def main():
    stats = read_stats()
    rows = build_diagrams()

    cards = []
    for m in MODULES:
        st = stats.get(m["code"]) or {}
        meta = "%s / 页 %s / 教材任务 %s / 手顺 %s 步 / 截图 %s 处 / 自测 %s 题" % (
            m["name_en"], st.get("pages", "—"), st.get("tasks", "—"), st.get("steps", "—"),
            st.get("shots", "—"), st.get("quiz", "—"))
        cards.append(("%s/index.html" % m["code"],
                      "%s %s（%s）" % (m["brand"], m["name_cn"], m["name_en"]),
                      esc(m["hub_line"]), esc(meta), m["accent"]))
    tot_pages = sum(v.get("pages", 0) for v in stats.values())
    tot_tasks = sum(v.get("tasks", 0) for v in stats.values())
    tot_steps = sum(v.get("steps", 0) for v in stats.values())
    tot_shots = sum(v.get("shots", 0) for v in stats.values())
    tot_quiz = sum(v.get("quiz", 0) for v in stats.values())

    body = []
    body.append('<p class="lead">%s</p>' % esc(CFG["course"]["lead"]))
    body.append(stat_cards([
        ("4", "个模块", "MM · PP · FI · CO"),
        (str(tot_pages), "页", "课程页（每模块 14 页）"),
        (str(tot_tasks), "个任务", "教材原书的全部任务，逐个走查"),
        (str(tot_shots), "处", "实机截图引用"),
    ]))
    body.append(toc([("四个模块", "mods"), ("端到端业务链", "chain"), ("模块地图", "map"),
                     ("学习路线", "route"), ("教学结构", "structure"), ("素材与边界", "src")]))

    body.append('<h2 id="mods">四个模块（点进去开始学）</h2>')
    body.append(modcards(cards))
    body.append(tbl(["模块", "教材任务", "手顺步骤", "配置分组", "自绘图", "自测"],
                    [[('<a href="%s/index.html"><b>%s %s</b></a>' % (m["code"], m["brand"], m["name_cn"])),
                      str((stats.get(m["code"]) or {}).get("tasks", "—")),
                      str((stats.get(m["code"]) or {}).get("steps", "—")),
                      str((stats.get(m["code"]) or {}).get("config_groups", "—")),
                      str((stats.get(m["code"]) or {}).get("diagrams", "—")),
                      str((stats.get(m["code"]) or {}).get("quiz", "—"))] for m in MODULES],
                    cls="tbl idx"))

    body.append('<h2 id="chain">端到端业务链</h2>')
    body.append(dia("e2e-chain", "从销售订单到财务报表：四个模块的接力与交接点", "自绘流程图"))

    body.append('<h2 id="map">模块地图：每个模块的输入与输出</h2>')
    body.append(dia("module-map", "MM / PP / FI / CO 各自的处理链与输入输出", "自绘结构图"))

    body.append('<h2 id="route">学习路线（建议顺序）</h2>')
    body.append(flowchart([
        ("① 先看总体", "本页 + 任选一个模块的概念页"), ("② 按模块深入", "组织 → 主数据 → 流程"),
        ("③ 练操作", "每模块的三个流程页 + 五个实训"), ("④ 配后台", "SPRO 配置页（教材任务逐个走查）"),
        ("⑤ 自测", "每模块 30 题，合格 75%"),
    ]))
    body.append(oplist([
        "<b>业务线顺序</b>（推荐给业务顾问）：MM → PP → SD（见 SD 课程站）→ FI → CO。"
        "理由是先把「买」和「造」看清，再看不「卖」，最后落到账与成本。",
        "<b>财务线顺序</b>（推荐给财务同事）：FI → CO → MM → PP，先建立账的概念，再看业务如何进账。",
        "<b>只学一块</b>：直接进对应模块，按导航从左到右走完 14 页即可；"
        "每页底部都有「其他模块」的入口。",
        "<b>对照 SD 课程站</b>：销售与分销的完整课程（16 页）在另一个站（<code>sap_cn/</code>，"
        "面向 <code>sap-cn-sd.vercel.app</code>），当本站讲到「SD 负责卖」时可以对照看。",
    ]))

    body.append('<h2 id="structure">四个模块共用一套教学结构（14 页）</h2>')
    body.append(tbl(["页", "内容", "为什么要这一页"],
                    [["首页 index.html", "课程地图 + 学习路线 + 场景值", "先建立整体印象，知道要学什么"],
                     ["概念 concept.html", "模块管什么、产出什么凭证、与邻居的分界、常见误解",
                      "不理解边界，后面每个动作都会问「这归谁管」"],
                     ["组织 org.html", "组织结构与分配关系", "SAP 里「先有组织，才有数据和单据」"],
                     ["主数据 master.html", "主数据分层与关键字段", "绝大多数报错的根因在主数据"],
                     ["流程 flow.html", "端到端流程 + 单据流 + 记账影响", "把零散操作串成一条线"],
                     ["流程① ② ③", "三篇局部操作详解（教材任务逐屏走查）", "当操作手册用"],
                     ["配置 config.html", "教材 IMG 路径 + 手顺 + 原始画面（分组覆盖全部任务）",
                      "后台是前台的镜像；按任务号对进度"],
                     ["实训 practice.html", "五个动手任务 + 完成基准", "从「看懂」到「做过」"],
                     ["讲师 instructor.html", "课时 / 板书 / 必问 / 评分", "直接可用的授课计划"],
                     ["学员 worksheet.html", "记入表（可打印）", "把单据号与分录记下来，才有作业可交"],
                     ["自测 quiz.html", "30 题 · 合格 75%", "查漏补缺，错题回对应页"],
                     ["术语 glossary.html", "中英对照 + T-code + 常用表", "随时回查"]],
                    cls="tbl idx"))

    body.append('<h2 id="src">素材与边界</h2>')
    body.append(tbl(["项", "说明"],
                    [["真实截图", "取自教材文档《S4.docx》（425 页、内嵌 1385 张图）的 "
                                  "MM / PP / FI / CO 四个模块，共 940 张，保留原图文件名（图注里的"
                                  "「原图 imageNNNN」），可回 Word 原稿逐张核对"],
                     ["任务与路径", "IMG 路径、手顺步骤、T-code 全部由 <code>work/modules_model.json</code> "
                                    "渲染（来自教材解析结果），页面不手抄"],
                     ["自绘图", "流程图 / 结构图 / 思维导图 / 泳道图由本站用纯 Python 生成 SVG，"
                                "图注标注「本站自绘 SVG」"],
                     ["标准值", "文中给出的数值都是教材环境的场景值（颐宁公司），"
                                "页面同时给出「在自系统里怎么确认」（F1/F4、IMG 路径、表名）"],
                     ["没有系统也能学", "所有实训都写了「达不到环境时的替代做法」（看图说话 / 纸上推演）"]],
                    cls="tbl idx"))
    body.append(note("info", "与 SD 课程站的关系",
                     "SD（销售与分销）已有独立课程站（<code>sap_cn/</code>）。"
                     "本站覆盖 MM / PP / FI / CO 四个模块，并在每模块的「集成关系」里指出与 SD 的交接点"
                     "（如 MM 的发货 601、FI 的应收账款、PP 的需求来源）。"))

    html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%(title)s · 从总体到细节</title>
<meta name="description" content="%(desc)s">
<link rel="stylesheet" href="assets/style.css">
<link rel="stylesheet" href="assets/mod.css">
</head>
<body>
<header class="site">
  <div class="nav-wrap">
    <a class="brand" href="index.html"><span class="logo">MOD</span><span class="txt">培训课程</span></a>
    <nav class="main">
      <a class="active" href="index.html" title="四个模块的总体视图">总览</a>
      %(nav)s
    </nav>
  </div>
</header>

<div class="wrap">
<main class="page">
<article>
<h1>%(title)s</h1>
<p class="kicker">%(subtitle)s</p>
%(body)s
</article>
</main>
</div>

<footer class="site">
  <div class="inner">
    <div class="cols">
      <div>
        <h5>%(title)s</h5>
        <p>%(subtitle)s</p>
      </div>
      <div>
        <h5>模块</h5>
        <p>%(flinks)s</p>
      </div>
      <div>
        <h5>课程结构</h5>
        <p>概念 · 组织 · 主数据 · 流程（三篇）· 配置 · 实训 · 讲师 · 学员 · 自测 · 术语</p>
      </div>
      <div>
        <h5>一句话免责</h5>
        <p>截图取自教材《S4.docx》的真实 SAP GUI 画面（中文界面）；图与表为本站自绘。
        标准值随版本/行业方案而异，请按页面标注的确认方法在自己的系统里核对。</p>
      </div>
    </div>
    <p class="copy">© <span data-year>2026</span> %(title)s · 静态站点，可离线使用</p>
  </div>
</footer>
<script src="assets/main.js"></script>
<script src="assets/mod.js"></script>
</body>
</html>
""" % {
        "title": esc(CFG["course"]["title"]), "subtitle": esc(CFG["course"]["subtitle"]),
        "desc": esc(CFG["course"]["desc"]),
        "nav": "\n      ".join('<a href="%s/index.html" title="%s">%s %s</a>'
                               % (m["code"], esc(m["name_cn"]), m["brand"], m["name_cn"])
                               for m in MODULES),
        "flinks": " · ".join('<a href="%s/index.html">%s %s</a>' % (m["code"], m["brand"], m["name_cn"])
                             for m in MODULES),
        "body": "\n".join(body),
    }
    with io.open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print("index.html %d bytes；总览图 %d 张%s"
          % (len(html), len(rows),
             "" if not any(r["overflow"] for r in rows)
             else "  ← 有溢出：" + str([r["file"] for r in rows if r["overflow"]])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
