# -*- coding: utf-8 -*-
"""MM（物料管理）模块课程包：14 页内容 + 7 张自绘图 + 配置分组 + 术语表。

素材与数值都来自教材《S4.docx》的 MM 模块（42 个任务 / 168 个手顺步骤），
经 work/modules_model.json 提供；本文件只写「怎么讲」，不手抄教材的任务文本与路径。
教材环境（颐宁公司）场景值：公司代码 C999 / 工厂 P999 颐宁机械工厂 / 采购组织 Y999 /
采购组 PG1·PG2 / MRP 控制者 001·002 / 评估分组代码 CN01 / 评估类 3000·3100·7920 /
物料 R999-100 罩壳…R999-500 金属片 · T999-100 · F999-100 / 供应商 10000000 红星轴承厂。
"""
from common import (box, cards, diagram, esc, flowchart, href, modcards, note, oplist,
                    pathline, route, shot, shot_grid, stat_cards, steps_list, tbl, toc)
from walk import render_config, render_task
from mm_p2 import page_flow, page_master, page_org
from mm_p3 import page_inventory, page_invoice, page_purchase
from mm_p4 import (CONFIG_GROUPS, CONFIG_NOTES, DIAGRAMS, GLOSSARY, TABLES, TCODES_EXTRA,
                   page_config, page_glossary, page_instructor, page_practice, page_quiz,
                   page_worksheet)


# ---------------------------------------------------------------- 页面函数
def page_index(ctx, stats):
    s = []
    s.append('<p class="lead">%s</p>' % esc(
        "MM（物料管理）管的是「企业的物料从哪来、存在哪、花多少钱」：采购申请与采购订单、"
        "收货与库存移动、发票校验与自动记账。本站按「概念 → 组织 → 主数据 → 端到端流程 → "
        "分步操作手顺 → SPRO 配置 → 实训」讲，每个环节都配教材原书的真实 SAP GUI 画面。"))
    s.append(stat_cards([
        (str(stats.get("pages", 14)), "页", "课程页数"),
        ("42", "个任务", "教材 MM 全部任务，逐个走查"),
        (str(stats.get("steps", 168)), "步", "手顺步骤（含截图）"),
        (str(stats.get("shots", 0)), "处", "实机截图引用"),
    ]))
    s.append(toc([("学习路线", "route"), ("模块地图", "map"), ("六大板块", "blocks"),
                  ("集成关系", "star"), ("教材场景", "scene"), ("代表性画面", "shots"),
                  ("怎么用这个站", "how")]))

    s.append('<h2 id="route">学习路线：从总体到细节</h2>')
    s.append(flowchart([
        ("① 概念", "MM 管什么、和谁交接"), ("② 组织", "公司代码 / 工厂 / 采购组织"),
        ("③ 主数据", "物料 / 供应商 / 信息记录"), ("④ 流程", "P2P 端到端 + 单据流"),
        ("⑤ 操作手顺", "采购 · 库存 · 发票校验"), ("⑥ 配置", "SPRO 42 个任务"),
        ("⑦ 实训", "五个动手任务"), ("⑧ 自测", "30 题 · 合格 75%"),
    ]))
    s.append(note("tip", "建议的学法",
                  "先看 <a href=\"concept.html\">概念</a> 建立「谁产生什么凭证」的整体印象，"
                  "再按 <a href=\"org.html\">组织</a> → <a href=\"master.html\">主数据</a> 把数据坐标立起来，"
                  "然后走一遍 <a href=\"flow.html\">端到端流程</a>；最后拿 <a href=\"purchase.html\">采购</a>、"
                  "<a href=\"inventory.html\">库存</a>、<a href=\"invoice.html\">发票校验</a> 三篇当操作手册，"
                  "在系统里照着做；<a href=\"config.html\">配置篇</a> 是后台的完整索引。"))

    s.append('<h2 id="map">模块地图</h2>')
    s.append(ctx.dia("mindmap", "MM 知识地图：从左到右依次是概念、组织、主数据、流程、配置与集成",
                     kind="自绘思维导图", wide=True))

    s.append('<h2 id="blocks">六大板块</h2>')
    s.append(cards([
        ("① 概念与定位", "MM 的三大职能、五类凭证、与 FI/PP/SD/CO 的分界；12 个常见误解"),
        ("② 组织结构", "公司代码 / 工厂 / 库存地点、采购组织 / 采购组、MRP 控制者与它们的分配"),
        ("③ 主数据", "物料主数据（20+ 视图按组织层拆）、供应商（三层）、采购信息记录"),
        ("④ 端到端流程", "请购 → 采购订单 → 收货 → 发票校验 → 付款，以及每步的凭证与记账"),
        ("⑤ 操作手顺", "三篇局部详解：采购、库存（移动类型）、发票校验（差异与冻结）"),
        ("⑥ 配置与实训", "SPRO 42 个任务（IMG 路径 + 手顺 + 截图）、五个实训、30 题自测"),
    ]))

    s.append('<h2 id="star">集成关系：MM 不是孤岛</h2>')
    s.append(ctx.dia("star", "MM 与 SD / PP / FI / CO 的交接：谁给 MM 什么、MM 给谁什么",
                     kind="自绘集成图", wide=True))
    s.append(tbl(["邻居模块", "给它（MM 提供）", "它给 MM", "典型凭证/接口"],
                 [["<b>FI</b> 财务会计",
                   "物料凭证牵动的会计凭证（存货、GR/IR、成本、差异）",
                   "总账科目主数据、自动记账科目、容差组、付款",
                   "BKPF/BSEG；科目确定 BSX/WRX/GBB"],
                  ["<b>PP</b> 生产计划",
                   "原料库存、采购到料进度（MD04 里的采购申请/订单）",
                   "生产订单的领料需求、收货（产成品入库）、261/101 移动",
                   "预留、采购申请（MRP 转换）"],
                  ["<b>SD</b> 销售与分销",
                   "可用库存（ATP）、发货时的库存减少（601）",
                   "销售订单需求（需求传递到 MRP）",
                   "VL02N 发货过账 → 物料凭证 + 会计凭证"],
                  ["<b>CO</b> 管理会计",
                   "采购价差、生产订单差异（进入成本报表）",
                   "成本中心/订单的领用科目与成本要素",
                   "PRD/DIF 差异科目、成本要素"]],
                 cls="tbl idx"))

    s.append('<h2 id="scene">教材场景（颐宁公司）</h2>')
    s.append('<p>本站所有示例值都来自教材《S4.docx》MM 模块的画面，不是标准值 —— '
             '换到自己的系统请按页面里写的「怎么确认」核对。</p>')
    s.append(tbl(["对象", "教材值", "说明"],
                 [["公司代码", "<code>C999</code>", "颐宁公司（教材示例）"],
                  ["工厂", "<code>P999</code>", "颐宁机械工厂"],
                  ["库存地点", "<code>0001</code> 仓库 / <code>0002</code> 生产 / <code>0003</code> 运输",
                   "教材任务 02 建立；MIGO 画面里显示为 001"],
                  ["采购组织", "<code>Y999</code>", "颐宁采购组织"],
                  ["采购组", "<code>PG1</code> 原材料和运营供应 / <code>PG2</code> 贸易商品", "任务 04"],
                  ["MRP 控制者", "<code>001</code> 自制品 / <code>002</code> 贸易商品", "任务 05"],
                  ["评估分组代码", "<code>CN01</code>", "把工厂 P999 归组，统一自动记账规则"],
                  ["物料", "<code>R999-100</code> 罩壳 · <code>R999-200</code> 飞轮 · "
                          "<code>R999-300</code> 管轴 · <code>R999-400</code> 支撑架 · "
                          "<code>R999-500</code> 金属片 · <code>T999-100</code> 贸易商品",
                   "原材料（ROH）/ 贸易商品（HAWA）"],
                  ["供应商", "<code>10000000</code> 红星轴承厂", "任务 26 维护采购数据"],
                  ["信息记录", "管轴 50 件 / 净价 1700 元 / 3 天交货", "ME11，任务 27"]],
                 cls="tbl idx"))

    s.append('<h2 id="shots">代表性画面（先建立整体印象）</h2>')
    s.append('<p>下面六张是教材原书 MM 主线上的关键画面，按「主数据 → 请购 → 订单 → 收货 → 发票校验 → 库存」'
             '排列；后面每一页都会逐屏展开（每张图都带「画面 N」编号与原图文件名）。</p>')
    s.append(ctx.shot_grid([
        (ctx.simg(22, 3), "任务 22 建原材料：物料类型 ROH 决定没有销售视图"),
        (ctx.simg(36, 4), "任务 36 ME51N 采购申请"),
        (ctx.simg(37, 6), "任务 37 ME21N 采购订单（参照请购创建）"),
        (ctx.simg(38, 4), "任务 38 MIGO 收货（101，生成 FI 凭证）"),
        (ctx.simg(39, 3), "任务 39 MIRO 发票校验（三单匹配）"),
        (ctx.simg(42, 1), "任务 42 MMBE 库存总览"),
    ]))

    s.append('<h2 id="how">怎么用这个站</h2>')
    s.append(oplist([
        "带「画面 N」编号的图 = 教材原书的 SAP GUI 实机截图（中文界面），图注里保留原图文件名，"
        "可回 Word 原稿逐张核对。",
        "图注写「本站自绘 SVG」的 = 我们画的流程图/结构图/思维导图，用于讲清结构与顺序；"
        "图上的数值是课程场景值。",
        "每页底部都有「其他模块」的入口；顶部横条可以在 MM / PP / FI / CO 与总览之间跳转。",
        ("配置篇的每个任务都给出「IMG 路径 + 手顺步骤 + 教材画面」，路径可以点击左侧小图标复制。",
         "note"),
    ]))
    return s


def page_concept(ctx, stats):
    s = []
    s.append('<p class="lead">先回答三个问题：MM 到底管什么？它产出什么凭证？它的边界在哪里。</p>')
    s.append(toc([("一句话定义", "def"), ("三大职能", "func"), ("五类凭证", "docs"),
                  ("凭证流向一张图", "chain"), ("与邻居模块的分界", "star"),
                  ("12 个常见误解", "mistakes"), ("教材画面", "shots")]))

    s.append('<h2 id="def">一句话定义</h2>')
    s.append(box("info", "MM = Materials Management（物料管理）",
                 "<p>管「物料的取得与持有」：<b>买什么（采购）、有多少（库存）、花了多少钱（发票校验与物料评估）</b>。"
                 "它不负责卖（那是 SD），不负责造（那是 PP），但它的每一步动作都会在 FI 里留下会计凭证。</p>"
                 "<p>所以 MM 是典型的「业务前台 + 财务后台」双层模块：前台动作（请购/订单/收货/发票）"
                 "产生物料凭证与发票凭证，系统再按后台配置的<b>自动记账规则</b>生成会计凭证。</p>"))
    s.append(shot(ctx, ctx.simg(42, 1), cap="库存总览 MMBE：MM 最直观的「我有多少料」画面（任务 42，教材画面）", task=42))

    s.append('<h2 id="func">三大职能</h2>')
    s.append(tbl(["职能", "管什么", "典型前台事务", "产出的凭证"],
                 [["<b>采购 Purchasing</b>",
                   "需求 → 请购 → 询价/报价 → 采购订单 → 框架协议（合同/计划协议）→ 货源（信息记录/货源清单）",
                   "<code>ME51N</code> 请购 · <code>ME21N</code> 采购订单 · <code>ME11</code> 信息记录",
                   "采购申请、采购订单"],
                  ["<b>库存管理 Inventory Management</b>",
                   "收货、发货、转储、库存类型与状态、盘点、库存总览；移动类型决定记账方式",
                   "<code>MIGO</code> 收货 · <code>MB1A</code> 发货 · <code>MB1B</code> 转储 · <code>MMBE</code> 库存",
                   "物料凭证（+ 会计凭证）"],
                  ["<b>发票校验 Logistics Invoice Verification</b>",
                   "三单匹配（订单/收货/发票）、差异与容差、发票冻结与下达、后续借项贷项",
                   "<code>MIRO</code> 输入发票 · <code>MRBR</code> 下达 · <code>MIR4</code> 显示",
                   "发票凭证（+ 会计凭证）"]],
                 cls="tbl idx"))

    s.append('<h2 id="docs">五类凭证：MM 的「证据链」</h2>')
    s.append(tbl(["凭证", "谁产生", "事务码", "它的作用", "对财务的影响"],
                 [["采购申请 Purchase Requisition", "需求部门 / MRP",
                   "<code>ME51N</code>", "内部需求，尚未对供应商承诺", "无"],
                  ["采购订单 Purchase Order", "采购部门", "<code>ME21N</code>",
                   "对供应商的承诺（价格、数量、交期）", "无（承诺，称「订单预算」）"],
                  ["物料凭证 Material Document", "仓库 / 收货", "<code>MIGO</code>",
                   "库存变动的原始凭证（101 收货 / 261 领料…）", "自动生成 FI 凭证：借存货、贷 GR/IR"],
                  ["发票凭证 Invoice Document", "财务 / 采购", "<code>MIRO</code>",
                   "记录供应商发票、校验差异", "自动生成 FI 凭证：借 GR/IR、贷应付"],
                  ["会计凭证 Accounting Document", "系统自动 / 财务", "<code>FB03</code>",
                   "最终落到总账与应收应付", "—"]],
                 cls="tbl idx"))
    s.append(note("warn", "最容易混的一点",
                  "「收货」不等于「付款」：收货先把钱挂在 <b>GR/IR（材料采购）</b> 中间科目上，"
                  "发票校验才把 GR/IR 冲平、把应付立起来，真正的现金流出在 FI 的付款（<code>F-53</code>/自动付款）。"
                  "三张单据（订单、收货、发票）数量金额一致，账才平。"))

    s.append('<h2 id="chain">凭证流向一张图</h2>')
    s.append(ctx.dia("doctypechain", "单据与凭证流：请购 → 订单 → 收货（物料凭证+FI）→ 发票（发票凭证+FI）→ 付款",
                     kind="自绘流程图", wide=True))

    s.append('<h2 id="star">与邻居模块的分界</h2>')
    s.append(ctx.dia("star", "MM 的四个接口方向（本图与首页同一张）：谁给 MM 输入、MM 给谁输出",
                     kind="自绘集成图", wide=True))
    s.append(tbl(["情况", "该找谁"],
                 [["要改销售订单的价格、交货期", "SD（VA02），MM 不管销售侧"],
                  ["要建物料主数据的销售视图/销售价格", "SD（MM01 里选销售视图 / VK11 条件）"],
                  ["要建生产订单、看 BOM、报工", "PP（CO01/CS01/CO11N）"],
                  ["费用要分摊到成本中心、内部订单", "CO（KB11N/KO88）"],
                  ["供应商发票要付款、看应付余额", "FI（FB60 记应付 / F-53 付款 / FK10N 余额）"],
                  ["会计科目要设置成「只能自动记账」", "FI 的 FS00（教材任务 29 就是这一步）"]],
                 cls="tbl"))

    s.append('<h2 id="mistakes">12 个常见误解</h2>')
    s.append(tbl(["#", "常见说法", "实际上"],
                 [["1", "「采购订单保存了就占库存了」",
                   "订单不动库存，也不记账；它只是对供应商的承诺。库存和会计凭证在<b>收货过账（101）</b>时才产生。"],
                  ["2", "「收货就付款了」",
                   "收货挂 GR/IR 中间科目；付款在 FI，需要发票校验 + 付款流程。"],
                  ["3", "「库存地点可以随便填」",
                   "收货时必须选对库存地点（教材用 0001 仓库 / 0002 生产 / 0003 运输），"
                   "它会写进物料凭证的库存地点字段，也是物料主数据库存地点视图的键。"],
                  ["4", "「物料主数据建一次就够了」",
                   "物料主数据是<b>分层的</b>：基本数据（跨组织）→ 工厂层 → 存储地点层；"
                   "评估类、价格控制这类字段会决定记账，缺了就收货失败。"],
                  ["5", "「评估类无所谓」",
                   "评估类（教材用 3000 原材料/贸易商品、3100、7920）与工厂（评估范围）一起决定"
                   "自动记账找哪个存货科目；教材还特别提示书里原来的评估类有误。"],
                  ["6", "「移动类型只是编号」",
                   "移动类型决定：库存增减方向、是否产生 FI 凭证、用哪组科目（BSX/WRX/GBB）、"
                   "是否更新数量/价值。101 收货、102 冲销、261 生产领料、301 工厂间转储…"],
                  ["7", "「发票金额比订单大一点没关系」",
                   "超容差会触发<b>发票冻结</b>（教材任务 32 配置了 14 个容差码），"
                   "必须有人用 MRBR 下达才能付款。"],
                  ["8", "「发票校验只看金额」",
                   "MIRO 做的是三单匹配：数量（对收货）、金额（对订单）、税额；"
                   "还要注意采购订单的<b>收货行</b>与<b>发票行</b>是否一一对应。"],
                  ["9", "「采购组织就是采购部门」",
                   "采购组织（Y999）是一个<b>法律/组织</b>概念，决定物料主数据的采购视图与订单的归属；"
                   "采购组（PG1/PG2）才是「哪个人/哪一组负责」。"],
                  ["10", "「MRP 是 PP 的事」",
                   "教材里 MM 也运行 MRP（<code>MD03</code> 单层，任务 34），把安全库存缺口变成采购申请；"
                   "BOM 展开要多层计划，那属于 PP。"],
                  ["11", "「收货容差和发票容差是一回事」",
                   "不是：收货容差（B1/B2）管「定价数量 vs 订单数量」，"
                   "发票容差管价格/数量/税额差异，配置的容差码完全不同。"],
                  ["12", "「MM 的表不用看」",
                   "查问题几乎都落到表：<code>EKKO/EKPO</code> 订单、<code>MSEG/MKPF</code> 物料凭证、"
                   "<code>RSEG</code> 发票行、<code>EINA/EINE</code> 信息记录、<code>MBEW</code> 物料评估。"]],
                 cls="tbl idx"))

    s.append('<h2 id="shots">教材画面（先建立整体印象）</h2>')
    s.append(shot_grid(ctx, [
        (ctx.simg(25, 1), "MM60 物料清单：看主数据是否建齐（任务 25）"),
        (ctx.simg(36, 4), "ME51N 采购申请：需求从部门进来（任务 36）"),
        (ctx.simg(37, 6), "ME21N 采购订单：对供应商的承诺（任务 37）"),
        (ctx.simg(38, 4), "MIGO 收货：库存与会计凭证的起点（任务 38）"),
        (ctx.simg(39, 3), "MIRO 发票校验：三单匹配与容差（任务 39）"),
        (ctx.simg(42, 1), "MMBE 库存总览：随时回答「有多少」（任务 42）"),
    ]))
    return s


# ==========================================================================
# 页面清单（教学顺序 = 导航顺序 = 构建顺序）
# ==========================================================================
PAGES = [
    dict(slot="index", file="index.html", title="首页 · 课程地图与学习路线",
         kicker="MM 管什么 · 怎么学 · 学完能做什么",
         tip="课程地图与学习路线", fn=page_index),
    dict(slot="concept", file="concept.html", title="概念与定位",
         kicker="MM 是什么：三大职能、五类凭证、与邻居模块的分界",
         tip="MM 是什么、三大职能、五类凭证", fn=page_concept),
    dict(slot="org", file="org.html", title="组织结构",
         kicker="公司代码 / 工厂 / 库存地点 / 采购组织 / 采购组 —— 先给数据定坐标",
         tip="企业结构 / 采购结构 / 计划与评估结构", fn=page_org),
    dict(slot="master", file="master.html", title="主数据",
         kicker="物料主数据（视图 × 组织层）· 供应商（三层）· 采购信息记录",
         tip="物料 / 供应商 / 采购信息记录", fn=page_master),
    dict(slot="flow", file="flow.html", title="端到端流程",
         kicker="从需求到付款（P2P）：泳道图、单据流与记账影响",
         tip="端到端采购流程与单据流", fn=page_flow),
    dict(slot="proc1", file="purchase.html", title="流程① 采购",
         kicker="请购 ME51N → 采购订单 ME21N → 货源与信息记录",
         tip="请购 · 采购订单 · 货源与信息记录", fn=page_purchase),
    dict(slot="proc2", file="inventory.html", title="流程② 库存管理",
         kicker="收货 MIGO（101）· 物料凭证与会计凭证 · 移动类型 · MMBE · 盘点",
         tip="收货 · 发货 · 转储 · 移动类型与库存总览", fn=page_inventory),
    dict(slot="proc3", file="invoice.html", title="流程③ 发票校验",
         kicker="MIRO 三单匹配 · 容差与冻结 · MRBR 下达 · MIR4 凭证 · 与 FI 的衔接",
         tip="MIRO · 差异与容差 · 冻结发票下达", fn=page_invoice),
    dict(slot="config", file="config.html", title="配置路线（42 个任务）",
         kicker="教材 IMG 路径 + 手顺 + 原始画面，按 A–F 六组整理",
         tip="SPRO 配置路线（42 个任务）", fn=page_config),
    dict(slot="practice", file="practice.html", title="实训：五个动手任务",
         kicker="做什么 · 完成基准 · 常见错误 · 对应画面",
         tip="动手任务与完成基准", fn=page_practice),
    dict(slot="instructor", file="instructor.html", title="讲师版",
         kicker="课时分配 · 板书路线 · 必问 12 题与答案 · 评分标准",
         tip="课时 / 板书 / 必问 / 评分", fn=page_instructor),
    dict(slot="worksheet", file="worksheet.html", title="学员版（记入表）",
         kicker="可打印：把组织值、单据号、凭证号、科目分录记下来",
         tip="记入表（可打印）", fn=page_worksheet),
    dict(slot="quiz", file="quiz.html", title="自测（30 题）",
         kicker="概念 5 · 组织 5 · 主数据 6 · 流程 8 · 配置 3 · 集成 3（合格 75%）",
         tip="30 题自评（合格 75%）", fn=page_quiz),
    dict(slot="glossary", file="glossary.html", title="术语与 T-code 速查",
         kicker="中英对照 · 事务码 · 常用表 · 教材任务总索引",
         tip="中英对照 / T-code / 常用表", fn=page_glossary),
]
