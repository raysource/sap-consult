#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shared chrome + rendering helpers for the S/4HANA 中文实训站 generator."""
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SITE = os.path.basename(ROOT)

MODEL = json.load(open(os.path.join(ROOT, 'work/site_model.json')))
IMAGES = json.load(open(os.path.join(ROOT, 'work/images.json')))
SEQ = {}
for rec in IMAGES:
    SEQ.setdefault(rec['path'], rec['seq'])
DIM = {rec['path']: (rec['w'], rec['h']) for rec in IMAGES}
ORIG = {rec['path']: rec['orig'] for rec in IMAGES}
TOTAL_SHOTS = len(IMAGES)

# ---------------------------------------------------------------- module meta
MODULES = [
    dict(code='prep', file='prep.html', nav='准备', short='准备',
         title='准备工作 — 登录系统与进入后台',
         kicker='准备工作 · 客户端登录 · SPRO 后台入口',
         intro=[
             '全站的第一步：把 SAP GUI 连上系统，并打开配置后台（SPRO）。后面 FI / CO / MM / PP / SD 五个模块的所有配置，都是在这个后台里按「IMG 路径」一层层点进去做的。',
             '教材环境是一套中文界面的 S/4HANA（公司代码 <code>C999</code>、公司名 <code>颐宁机械有限公司</code>、工厂 <code>F999</code>、物料如 <code>T999-100</code> / <code>R999-100</code> / <code>F999-100</code>）。这些是原文档作者的系统取值，与你自己系统里的编号范围/组织结构不一定相同 —— 手顺的「操作顺序」可以照做，具体值请按自己系统填写。',
         ],
         focus=['客户端图标与登录页（系统/客户端/用户/口令/语言）',
                'SPRO 后台入口：事务代码 <code>SPRO</code> → SAP 参考 IMG → 各模块菜单树',
                '本站把「后台配置」与「前台操作」分开标注：<span class="fb">后台</span> = IMG 定制，<span class="fb img">前台</span> = 日常业务事务']),
    dict(code='fi', file='fi.html', nav='FI', short='FI',
         title='财务会计 FI（Financial Accounting）',
         kicker='财务会计 · 组织结构 · 科目主数据 · 应收应付 · 财务报表',
         intro=[
             'FI 主线是「先搭组织结构，再建科目，最后跑凭证与报表」：组织结构（公司代码 / 会计科目表 / 会计年度变式 / 信贷控制范围）→ 全局参数 → 科目组与字段状态变式 → 科目主数据（资产负债、统驭科目应收应付、材料采购 GR/IR、损益）→ 凭证号码范围与记账期间 → 过账容差组 → 总账凭证与余额 → 客户/供应商账户组、编号范围与主数据 → 应收应付（客户发票 / 收款 / 供应商发票 / 付款 / 余额）→ 财务报表结构（资产负债表与损益表）与报表运行。',
             '本站按原文档顺序保留 45 个任务，每个任务都给出 IMG 路径、T-code（文档中出现的）与原文档的实机画面。教材场景是「颐宁机械有限公司」从零建公司代码 <code>C999</code>，一直做到能出资产负债表和损益表。',
         ],
         focus=['组织结构四件套：公司代码 / 会计科目表 / 会计年度变式 / 信贷控制范围',
                '科目主数据：<code>FS00</code> 新建一般资产负债科目、统驭科目（应收/应付）、材料采购科目（GR/IR）、损益科目',
                '记账期间与凭证号码范围：开关账机制（关掉的期间不允许改凭证）',
                '应收应付闭环：客户发票 <code>FB70</code>、收款、供应商发票 <code>FB60</code>、付款、余额查询（<code>FD10N</code> / <code>FK10N</code>）']),
    dict(code='co', file='co.html', nav='CO', short='CO',
         title='管理会计 CO（Controlling）',
         kicker='管理会计 · 成本中心 · 成本要素 · 作业类型 · 分配分摊 · 内部订单',
         intro=[
             'CO 主线是「成本控制范围 → 成本中心 → 成本要素/作业类型 → 期末分摊 → 内部订单」：创建成本控制范围并把公司代码分进去 → 成本中心组与成本中心（<code>OKEON</code>）→ 初级/次级成本要素（<code>KA01</code> / <code>KA06</code>）与成本要素组 → 作业类型（<code>KL01</code>）与作业输出价格（<code>KP26</code>）→ 成本控制凭证编号范围 → 成本中心报表、重过账（<code>KB61</code>）→ 统计指标（<code>KK01</code>）与统计指标数量（<code>KB31N</code>）→ 分配循环（房租）与分摊循环（电费）→ 内部订单：订单类型与编号范围、结算参数文件与分配结构、创建订单（<code>KO04</code>）、费用发票、结算（<code>KO88</code>）与结算结果。',
             '教材场景把「行政部房租按面积分配给各成本中心」「电费按统计指标分摊」「内部订单归集费用后结算」三件事串起来讲，是理解 CO 期末结账最直观的一条线。',
         ],
         focus=['成本控制范围与公司代码的分配（<code>OX19</code>，注意与 FI 公司代码的一致）',
                '成本要素（初级 = 对应 FI 科目；次级 = 只在 CO 内部流动，如分摊/结算）',
                '分配（<code>分配循环</code>，按统计指标/追踪因素）与分摊（<code>分摊循环</code>）的区别',
                '内部订单：类型 → 结算参数文件 → 分配结构 → 创建 → 费用 → 结算 <code>KO88</code>']),
    dict(code='mm', file='mm.html', nav='MM', short='MM',
         title='物料管理 MM（Materials Management）',
         kicker='物料管理 · 组织结构 · 物料主数据 · 自动记账 · MRP · 采购流程',
         intro=[
             'MM 主线是「组织结构与工厂参数 → 物料主数据 → 自动记账 → MRP → 采购到发票校验」：工厂 / 库存地点 / 采购组织 / 采购组 / MRP 控制者 → 分配给公司代码与采购组织 → 物料组、计划边际码 → 工厂参数（库存预留、库存地点视图、税务代码缺省值、初始期间、MRP 参数）→ 激活 MRP、计划运行号码范围 → 物料类型属性、评估控制、评估类（科目确定的前提）→ 物料主数据（原材料 / 贸易商品 / 产成品，<code>MM01</code>）→ 供应商采购数据（<code>MK01</code>）与采购信息记录（<code>ME11</code>）→ 自动记账（<code>OBYC</code>）与存货科目只能自动记账 → 容差限制（价格差异 / 收货 / 发票冻结）→ MRP 运行（<code>MD03</code>）与库存需求清单（<code>MD04</code>）→ 采购申请（<code>ME51N</code>）→ 采购订单（<code>ME21N</code>）→ 收货（<code>MIGO</code>）→ 发票校验（<code>MIRO</code>）→ 冻结发票下达（<code>MRBR</code>）→ 发票与会计凭证 → 库存显示（<code>MMBE</code>）。',
             '其中「评估类 + 自动记账（OBYC/BSX/WRX）」是 MM 与 FI 的接缝，也是原文档反复排错的地方（见「排错与踩坑」页）。',
         ],
         focus=['组织结构四件套：工厂 / 库存地点 / 采购组织 / 采购组，及其分配关系',
                '物料主数据三类视图：基本数据、采购、MRP、会计（评估类决定记账科目）',
                '自动记账 <code>OBYC</code>：BSX（存货）、WRX（GR/IR）、GBB（费用/差异）等事务码的科目确定',
                '采购全流程：<code>ME51N</code> → <code>ME21N</code> → <code>MIGO</code> → <code>MIRO</code> → <code>MRBR</code>']),
    dict(code='pp', file='pp.html', nav='PP', short='PP',
         title='生产计划 PP（Production Planning）',
         kicker='生产计划 · BOM · 工作中心 · 工艺路线 · 成本估算 · 生产订单',
         intro=[
             'PP 主线是「主数据 → 计划 → 执行 → 成本」：生产计划参数文件、生产调度员、生产订单参数（排程 / 订单类型 / 确认）→ 物料清单 BOM（<code>CS01</code>，用处清单 <code>CS15</code>）→ 工作中心（负责人、控制码、能力 <code>CR11</code>、工时类别工作中心 <code>CR01</code>）→ 工艺路线（<code>CA01</code>）与工序拆分（<code>CA02</code>）→ 产成品生产计划视图 → 成本核算基础（成本构成结构、估计变式、日期控制、数量结构控制、成本核算变式 <code>PC01</code>）→ 产品成本估算（<code>CK11N</code>）→ 标记价格 / 发布价格（<code>CK24</code>）→ 实际成本核算估价变式与在制品结果分析版本 → 可用性检查（检查组、检查范围、检查规则 <code>PP01</code>/<code>PP02</code>）→ 计划策略组（<code>MM02</code>）与独立需求（<code>MD61</code>）→ MRP 运行（<code>MD02</code>）、MRP 清单 <code>MD05</code>、库存需求清单 <code>MD04</code> → 计划订单转生产订单 → 采购申请转采购订单 → 收货与发票 → 生产订单下达（<code>CO02</code>）/ 发货 / 工单确认（<code>CO11N</code>）/ 收货（<code>MIGO</code>）→ 成本显示（<code>CO03</code>）/ 技术性完成 / 差异结算（<code>KO88</code>）/ 成本报表 → 库存清单与移库。',
             '教材场景是一台「铸钢泵 170-230」从 BOM、工艺路线、标准成本估算，一路做到生产订单完工、结算和成本分析。',
         ],
         focus=['三大主数据：BOM（<code>CS01</code>）、工作中心（<code>CR01</code>/<code>CR11</code>）、工艺路线（<code>CA01</code>）',
                '标准成本估算与价格更新：<code>CK11N</code> 估算 → <code>CK24</code> 标记 → 发布',
                '计划策略组与独立需求（<code>MD61</code>）→ MRP（<code>MD02</code>）→ 计划订单转生产订单',
                '生产订单执行链：下达 <code>CO02</code> → 发货 → 确认 <code>CO11N</code> → 收货 <code>MIGO</code> → 结算 <code>KO88</code>']),
    dict(code='sd', file='sd.html', nav='SD', short='SD',
         title='销售与分销 SD（Sales and Distribution）',
         kicker='销售与分销 · 销售范围 · 定价 · 合作伙伴 · 销售流程 · 开票',
         intro=[
             'SD 主线是「销售组织结构 → 装运基础数据 → 定价与税 → 账户与更新组 → 主数据 → 销售流程」：销售组织 / 分销渠道 / 产品组及其分配 → 销售范围、销售办公室、销售组 → 装运（起运点、装载点、运送条件、装载组、拣配库存地点）→ 客户账户组的销售数据与合作伙伴确定 → 定价过程、客户与单据定价过程、定价过程确定 → 物料清单与排斥、销售单据物料确定 → 税收确定规则、客户与物料税分类、销项税税率（<code>VK11</code>）→ 物料账户分配组与销售收入科目 → 抬头/项目等级的更新组 → 主数据（物料销售视图 <code>MM01</code>、销售价格、订货方 <code>VD01</code>、收货方与分配 <code>VD02</code>）→ 销售流程（报价 <code>VA21</code> → 销售订单 → 外向交货 <code>VL01N</code> → 发票 <code>VF01</code> / 过账 <code>VF02</code> → 原始凭证 → 订单清单 <code>VA05</code> → 销售分析 <code>MCTA</code>）。',
             '教材场景是一家「远东造船厂」按「颐宁公司」的报价创建销售订单，然后走交货、开票、过账到财务会计的完整链条。',
         ],
         focus=['销售范围（销售组织 + 分销渠道 + 产品组）是 SD 里最基本的「业务分区」',
                '定价过程（条件类型、过程确定）与税收确定规则（客户税分类 + 物料税分类）',
                '合作伙伴确定（售达方 / 收票方 / 付款方 / 送达方）与客户账户组的功能分配',
                '销售流程：报价 <code>VA21</code> → 订单 → 交货 <code>VL01N</code> → 发票 <code>VF01</code>/<code>VF02</code> → 会计凭证']),
]

NAV = [('index.html', '首页')] + [(m['file'], m['nav']) for m in MODULES] + [
    ('tcode.html', 'T-code'),
    ('issues.html', '排错'),
    ('tasks.html', '索引'),
    ('instructor.html', '讲师'),
    ('worksheet.html', '学员'),
    ('quiz.html', '自测'),
]
SITE_TITLE = 'SAP S/4HANA 中文实训站'
SITE_SUB = '全模块配置与操作手顺 · 实机画面'


# ---------------------------------------------------------------- helpers
def esc(s):
    return html.escape(s or '', quote=True)


def mod_of(code):
    return [m for m in MODULES if m['code'] == code][0]


def tasks_of(code):
    return [m for m in MODEL if m['code'] == code][0]['tasks']


def txt(t):
    """Escape and keep the source's own line breaks."""
    t = esc(t)
    t = t.replace('\n', '<br>')
    return t


def cap_html(c):
    """Step caption → html, marking 解释/说明 lead-ins."""
    c = c.strip()
    if not c:
        return ''
    m = re.match(r'^(解释|说明|注意)([：:])\s*(.*)$', c, re.S)
    if m:
        return f'<span class="lead">{m.group(1)}{m.group(2)}</span> ' + txt(m.group(3))
    return txt(c)


def figure(path, caption='', alt_extra=''):
    w, h = DIM.get(path, (0, 0))
    seq = SEQ.get(path, '')
    orig = ORIG.get(path, os.path.basename(path))
    alt = esc((caption or '').replace('\n', ' ')[:160]) or esc(orig)
    if alt_extra:
        alt = esc(alt_extra) + '：' + alt
    cls = 'shot narrow' if h and h <= 100 else 'shot'
    return (f'<figure class="{cls}">'
            f'<a class="zoom" href="assets/img/{path}">'
            f'<img src="assets/img/{path}" alt="{alt}" loading="lazy" width="{w}" height="{h}">'
            f'</a>'
            f'<figcaption><span class="n">画面 {seq}</span>'
            f'<span class="src">{esc(orig)} · {w}×{h}</span></figcaption>'
            f'</figure>')


def figures(imgs, caption, alt_extra):
    if not imgs:
        return ''
    out = ''.join(figure(p, caption, alt_extra) for p in imgs)
    if len(imgs) >= 3:
        return f'<div class="shot-grid">{out}</div>'
    return out


NOTE_LABEL = {'tip': '教材笔记', 'info': '原理说明', 'warn': '踩坑提醒', 'ref': '参考'}


def note_html(n):
    return (f'<div class="note {n["kind"]}"><b class="t">{NOTE_LABEL.get(n["kind"], "笔记")}</b>'
            f'{txt(n["text"])}</div>')


def render_task(code, t):
    """One task = .steph header + 说明 + IMG 路径 + 输入值 + 手顺(ol.oplist) + 笔记."""
    mod = mod_of(code)
    tno = t['no']
    tags = []
    if t['fb']:
        tags.append(f'<span class="fb{" img" if t["fb"] == "前台" else ""}">{esc(t["fb"])}</span>')
    for tc in t['tcodes'][:6]:
        tags.append(f'<span class="tc">{esc(tc)}</span>')
    tags.append(f'<span class="tc2">{t["nimg"]} 画面 / {len(t["steps"])} 步</span>')
    out = [f'<div class="steph" id="{t["anchor"]}">'
           f'<span class="no">任务 {tno:02d}</span><h3>{esc(t["title"])}</h3>'
           + ''.join(tags) + '</div>']
    if t['desc']:
        for d in t['desc']:
            out.append(f'<p>{txt(d)}</p>')
    if t['path']:
        out.append(f'<div class="pathline" data-copy="{esc(t["path"])}">'
                   f'<b>IMG 路径（后台菜单）</b>{esc(t["path"])}</div>')
    if t['values']:
        rows = ''.join(f'<tr><td>{esc(v["k"])}</td><td>{esc(v["v"])}</td></tr>' for v in t['values'])
        out.append('<table class="tbl vals"><thead><tr><th>项目</th><th>文档中的取值</th></tr></thead>'
                   f'<tbody>{rows}</tbody></table>')
    for n in t['notes']:
        if n['after'] == 0:
            out.append(note_html(n))
    if t['steps']:
        out.append('<ol class="oplist">')
        for i, s in enumerate(t['steps'], 1):
            cls = ' class="is-note"' if s.get('note') else ''
            out.append(f'<li{cls}>')
            if s['caption']:
                out.append(f'<p class="opcap">{cap_html(s["caption"])}</p>')
            elif not s.get('note'):
                out.append(f'<p class="opcap"><span class="sub">按上一屏继续操作（画面 {SEQ.get(s["imgs"][0], "")}）</span></p>')
            out.append(figures(s['imgs'], s['caption'], f'{esc(t["title"])} · 第 {i} 步' if t['nimg'] > 1 else esc(t['title'])))
            for n in t['notes']:
                if n['after'] == i:
                    out.append(note_html(n))
            out.append('</li>')
        out.append('</ol>')
    for n in t['notes']:
        if n['after'] > len(t['steps']):
            out.append(note_html(n))
    # sub-headings / tables that sat inside the task
    for s in t['subs']:
        if s['kind'] == 'head':
            out.append(f'<h4>{esc(s["text"])}</h4>')
        elif s['kind'] == 'table' and s['rows']:
            ncol = max(len(r) for r in s['rows'])
            head = ''.join(f'<th></th>' for _ in range(ncol))
            body = ''.join('<tr>' + ''.join(f'<td>{txt(c)}</td>' for c in r)
                           + ''.join('<td></td>' for _ in range(ncol - len(r))) + '</tr>'
                           for r in s['rows'])
            out.append(f'<div class="tblwrap"><table class="tbl"><thead><tr>{head}</tr></thead>'
                       f'<tbody>{body}</tbody></table></div>')
            if s.get('imgs'):
                out.append(figures(s['imgs'], t['title'], esc(t['title'])))
    return '\n'.join(x for x in out if x)


def page(fname, title, body, desc='', active=None, extra_head='', hero=''):
    nav = []
    for href, label in NAV:
        cls = ' class="active"' if (active or fname) == href else ''
        nav.append(f'<a{cls} href="{href}">{label}</a>')
    nav = '\n      '.join(nav)
    year = 2026
    foot_links = '\n'.join(f'      <a href="{h}">{l}</a><br>' for h, l in NAV if h != 'index.html')
    mods_links = '\n'.join(
        f'      <a href="{m["file"]}">{m["nav"]} — {esc(m["title"].split("（")[0])}</a><br>'
        for m in MODULES)
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="stylesheet" href="assets/style.css">
<link rel="stylesheet" href="assets/s4cn.css">
</head>
<body>
<header class="site">
  <div class="nav-wrap">
    <a class="brand" href="index.html"><span class="logo">S4</span><span class="txt">中文实训站</span></a>
    <nav class="main">
      {nav}
    </nav>
  </div>
</header>
{hero}
<div class="wrap">
<main class="page"><article>
{body}
</article></main>
</div>
<footer class="site"><div class="inner">
  <div><h5>{SITE_TITLE} — {SITE_SUB}</h5>
  <p>内容依据同目录教材文档 <code>S4.docx</code>（425 页 · 6 大模块 · 222 个任务 · 1385 张实机截图）整理。全部页面可离线打开，无外部依赖。</p>
  <div><h5>关于画面</h5><p>站内所有截图都是<b>原教材文档中的实机画面</b>（中文界面 SAP GUI），不是示意图、也不是模拟生成图；文件名保留原文档编号以便与 Word 原文对照。文档中的示例值（公司代码 <code>C999</code>、工厂 <code>F999</code>、物料 <code>R999-100</code> 等）属于原作者的教材环境，请以自己系统的组织结构与编号范围为准。</p></div></div>
  <div class="cols">
    <div><h5>模块</h5>
{mods_links}    </div>
    <div><h5>全站</h5>
{foot_links}    </div>
  </div>
</div></footer>
<script src="assets/main.js"></script>
<script src="assets/s4cn.js"></script>
</body>
</html>
'''


def breadcrumb(parts):
    items = []
    for i, (href, label) in enumerate(parts):
        if href:
            items.append(f'<a href="{href}">{esc(label)}</a>')
        else:
            items.append(f'<span>{esc(label)}</span>')
    return '<p class="breadcrumb">' + ' / '.join(items) + '</p>'
