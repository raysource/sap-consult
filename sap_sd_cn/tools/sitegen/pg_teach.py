#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Teaching pages: instructor / worksheet / quiz."""
import os
import random

from common import (MODULES, MODEL, ROOT, esc, txt, page, breadcrumb, mod_of,
                    tasks_of, SEQ)

ALL_TASKS = [(m, t) for m in MODEL for t in m['tasks']]


# ------------------------------------------------------------ instructor
QA = [
    ('这套教材的配置从哪开始做？',
     '从「准备工作」的 <code>SPRO</code> 进后台，然后按 FI → CO → MM → PP → SD 的顺序。'
     'FI 的任务 01〜05（公司代码 / 会计科目表 / 会计年度变式 / 信贷控制范围 / 全局参数）是全部模块的公共前提，必须先做。'),
    ('为什么 FI 的第一个任务是「创建公司代码」而不是建科目？',
     '公司代码是「一个完整的会计实体」（原文档原话），后面所有科目、凭证、期间、报表都挂在这个公司代码上；'
     '教材建的是 <code>C999</code>「颐宁机械有限公司」。'),
    ('科目建好后，凭证里看不到某个字段（或字段是灰的）是怎么来的？',
     '由「科目组 + 字段状态变式」决定：任务 06 定义科目组及输入控制、任务 07 定义字段状态变式、任务 08 把变式分配给公司代码。'
     '所以讲科目之前必须先讲这两个。'),
    ('「材料采购科目」是干什么的？为什么又叫 GR/IR？',
     '原文档说明：收货时借「库存」贷「材料采购」，收发票时借「材料采购」贷「应付账款」，'
     '科目需要「逐笔逐清」，是收货与收发票之间的过渡科目（GR/IR），贷方余额挂在 <code>WRX</code> 事务码上。'),
    ('MM 里最容易出错的接缝在哪？',
     '物料主数据的「评估类」与自动记账 <code>OBYC</code>：评估类决定科目确定，评估类填错就会报'
     '「不可能为条目 A999 BSX CN01 确立帐户」。原文档的处理是删掉已建采购订单、改物料会计视图 1 的评估类'
     '（本期/上期/上一年度都要改），并建议在创建物料时就做对。'),
    ('税码报错 FS217 怎么处理？',
     '用 <code>FS00</code> 打开该总账科目，在「控制数据」里把税务类型放开：<code>-</code> 只允许进项税、'
     '<code>+</code> 只允许销项税、<code>*</code> 全部允许；改完退出 <code>MIRO</code> 重新进入。'),
    ('PP 里标准成本估算是哪几个 T-code、什么顺序？',
     '<code>CK11N</code> 估算 → <code>CK24</code> 标记 → <code>CK24</code> 发布。'
     '作业价格缺失（如「没有内部作业 LAB 1001 的价格可被确定」）时，先用 <code>KP26</code> 维护作业输出价格，'
     '再回 <code>CK11N</code>——原文档特别提示：维护完要<b>退出 CK11N 再重新执行 CK24</b>。'),
    ('生产订单从下达到结算，现场演示的顺序是什么？',
     '下达 <code>CO02</code> → 发货（对生产订单发货）→ 确认 <code>CO11N</code> → 收货 <code>MIGO</code> → '
     '成本显示 <code>CO03</code> → 技术性完成 <code>CO02</code> → 差异结算 <code>KO88</code> → 成本报表。'
     '（对应 PP 任务 42〜49）'),
    ('SD 里「销售范围」是什么？为什么订单一开始就要填？',
     '销售范围 = 销售组织 + 分销渠道 + 产品组，是 SD 的业务分区（任务 01〜07）。'
     '订单里的定价过程、交货、税确定、可供量都要靠它定位，所以不填销售范围什么都做不了。'),
    ('客户主数据里的合作伙伴为什么有 4 个？',
     '原文档给出的是：<code>SP</code> 售达方、<code>BP</code> 收票方、<code>PY</code> 付款方、<code>SH</code> 送达方。'
     '一个客户可以在不同角色上换别人（例如收货方 <code>K002</code> 作为送达方），订单里自动带出这些角色。'),
    ('一笔业务从报价走到会计凭证，演示哪几个 T-code？',
     '报价 <code>VA21</code> → 销售订单（参照报价创建）→ 交货 <code>VL01N</code> → 发票 <code>VF01</code> → '
     '过账 <code>VF02</code> → 会计凭证（点击原始凭证）→ 订单清单 <code>VA05</code> / 销售分析 <code>MCTA</code>。'),
    ('学员系统里的报错和教材不一样怎么办？',
     '先做「排错与踩坑」页的 6 项前提检查（期间开关、组织结构分配、评估类与 OBYC、价格标记发布、库存、主数据），'
     '教材里的报错大多落在这 6 类里；再不行就用 F1/F4 与 SPRO 的文档按钮确认字段 —— 不要照抄别人的标准值。'),
]


def build_instructor():
    st = {m['code']: dict(tasks=len(m['tasks']), shots=sum(t['nimg'] for t in m['tasks']),
                          steps=sum(len(t['steps']) for t in m['tasks'])) for m in MODEL}
    total_tasks = len(ALL_TASKS)
    total_shots = sum(x['shots'] for x in st.values())

    body = [breadcrumb([('index.html', '首页'), (None, '讲师版')])]
    body.append('<h1>讲师版 — 授课设计、演示脚本与评分建议</h1>')
    body.append(f'''<p>面向用这套材料带班的讲师。本站素材来自教材文档 <code>S4.docx</code>：
<b>{total_tasks} 个任务 / {total_shots} 张实机画面</b>，全部画面都是原作者在真实系统里截的中文界面。</p>
<div class="box info"><b class="t">本站的口径（讲课时请同步声明）</b>
① 画面是原文档的实机截图，不是示意图；② 文档里的组织结构与主数据编号（<code>C999</code> / <code>F999</code> /
<code>R999-100</code> / <code>K001</code> …）属于原作者的教材环境，<b>操作顺序照做、取值换成学员系统的</b>；
③ 本站不补充原文档没有的标准值、字段清单与 SAP Note。</div>''')

    body.append('<h2 id="plan">1. 课时安排建议（按 5 天 / 30 小时）</h2>')
    body.append('''<p>任务数与画面数都很实在，讲不完是正常的 —— 建议「<b>配置讲主线、业务全演示</b>」：
每个模块的后台配置挑关键任务演示 1〜2 个，前台业务任务（创建订单、收货、开票）全部走一遍。</p>''')
    plan = [
        ('Day 1', '准备工作 + 财务会计 FI（上）', 'prep + fi 任务 01〜21',
         '登录与 SPRO；公司代码 / 科目表 / 会计年度变式 / 信贷控制范围；科目组与字段状态变式（重点演示）；'
         '建 4 类科目（资产负债 / 统驭 / 材料采购 GR-IR / 损益）；凭证号码范围与记账期间。'),
        ('Day 2', '财务会计 FI（下）+ 管理会计 CO', 'fi 任务 22〜45 + co 任务 01〜34',
         '客户/供应商账户组与主数据；应收（发票、全额/部分收款、余额）与应付（发票、付款、余额）；'
         ' CO 成本控制范围 → 成本中心 → 成本要素/作业类型 → 分配（房租）与分摊（电费）→ 内部订单与结算。'),
        ('Day 3', '物料管理 MM', 'mm 任务 01〜42',
         '工厂/库存地点/采购组织/采购组 → 物料类型与评估类（关键：与 OBYC 的关系）→ 三类物料主数据 →'
         ' 自动记账 OBYC → 容差限制 → MRP 运行 → 采购申请→订单→收货→发票校验→冻结发票下达。'),
        ('Day 4', '生产计划 PP', 'pp 任务 01〜51',
         'BOM / 工作中心 / 工艺路线 → 成本核算变式与成本构成 → CK11N 估算、CK24 标记发布 →'
         ' 可用性检查与计划策略组 → 独立需求 MD61 → MRP MD02 → 计划订单转生产订单 →'
         ' 下达/发货/确认/收货 → 成本显示、技术性完成、差异结算 KO88。'),
        ('Day 5', '销售与分销 SD + 综合排错与测验', 'sd 任务 01〜48 + 自测 30 题',
         '销售范围与装运主数据 → 定价过程与税确定 → 合作伙伴确定 → 物料/客户销售视图 →'
         ' 报价 VA21 → 订单 → 交货 VL01N → 发票 VF01/VF02 → 原始凭证 → 订单清单与销售分析；'
         '最后跑「排错与踩坑」与本页第 4 节的必出问答。'),
    ]
    body.append('<div class="tblwrap"><table class="tbl"><thead><tr><th>日程</th><th>内容</th>'
                '<th>对应任务</th><th>讲什么 / 演示什么</th></tr></thead><tbody>' +
                ''.join(f'<tr><td>{esc(a)}</td><td>{esc(b)}</td><td><code>{esc(c)}</code></td><td>{d}</td></tr>'
                        for a, b, c, d in plan) + '</tbody></table></div>')

    body.append('<h2 id="pick">2. 每个模块「一定要演示」的任务</h2>')
    body.append('<p>下面这些任务是各模块的骨架，现场演示一遍胜过讲十遍。其余任务可以让学员照着本站手顺自学。</p>')
    picks = {
        'fi': [1, 6, 7, 10, 12, 13, 18, 32, 33, 37, 39, 45],
        'co': [1, 2, 4, 5, 12, 20, 21, 23, 24, 31, 33],
        'mm': [1, 21, 22, 27, 28, 34, 36, 37, 38, 39, 40],
        'pp': [6, 12, 14, 22, 23, 25, 33, 36, 37, 42, 44, 45, 48],
        'sd': [1, 7, 21, 22, 24, 33, 34, 35, 40, 41, 42, 43, 44, 47],
        'prep': [1, 2],
    }
    for m in MODULES:
        ts = {t['no']: t for t in tasks_of(m['code'])}
        plist = [ts[n] for n in picks.get(m['code'], []) if n in ts]
        body.append(f'<h3>{esc(m["nav"])} — {esc(m["title"])}</h3>')
        body.append('<ul>' + ''.join(
            f'<li><a href="{m["file"]}#{t["anchor"]}">任务 {t["no"]:02d} {esc(t["title"])}</a>'
            + (f'　<span class="dim">IMG：<code>{esc(t["path"][:90])}</code></span>' if t['path'] else '')
            + f'　<span class="dim">{t["nimg"]} 张画面</span></li>' for t in plist) + '</ul>')

    body.append('<h2 id="qa">3. 必出问答（12 问，含标准答法）</h2>')
    body.append('<div class="tblwrap"><table class="tbl"><thead><tr><th>#</th><th>学员一定会问</th>'
                '<th>建议这样回答</th></tr></thead><tbody>' +
                ''.join(f'<tr><td>{i}</td><td>{q}</td><td>{a}</td></tr>'
                        for i, (q, a) in enumerate(QA, 1)) + '</tbody></table></div>')

    body.append('<h2 id="grading">4. 评分与验收建议</h2>')
    body.append('''<div class="tblwrap"><table class="tbl"><thead><tr><th>项目</th><th>权重</th><th>判定标准</th></tr></thead><tbody>
<tr><td>自测（<a href="quiz.html">quiz.html</a> 30 题）</td><td>30%</td><td>75% 以上合格（≥23 题）；错题回到对应任务重做。</td></tr>
<tr><td>手顺完成度（<a href="worksheet.html">学员版记入表</a>）</td><td>40%</td><td>FI 01〜21 + MM 21〜28 + PP 22〜25 + SD 34〜44 这些「关键链条任务」必须全部打勾。</td></tr>
<tr><td>排错题（<a href="issues.html">排错页</a> 的 10 个现象）</td><td>20%</td><td>能说出「现象 → 原因 → 处理 T-code」三要素，抽 5 题全对为满分。</td></tr>
<tr><td>口头复述链路</td><td>10%</td><td>能独立说出采购链（ME51N→ME21N→MIGO→MIRO→MRBR）与销售链（VA21→订单→VL01N→VF01→VF02）两串 T-code。</td></tr>
</tbody></table></div>''')
    body.append('<div class="box ok"><b class="t">一次课的最后 20 分钟这样收尾</b>'
                '① 让学员在学员版记入表里填「遇到的问题」栏；② 一起过排错页的现象表；'
                '③ 用自测页跑一遍并当场看错题；④ 布置「回自己系统把公司代码/工厂/销售范围换成自己的值」的作业。</div>')
    return page('instructor.html', '讲师版 · S/4HANA 中文实训站', '\n'.join(body),
                desc='S/4HANA 中文实训站讲师版：5 天课时安排、每模块必演示任务、12 个必出问答与评分建议。',
                active='instructor.html')


# ------------------------------------------------------------ worksheet
def build_worksheet():
    body = [breadcrumb([('index.html', '首页'), (None, '学员版（记入表）')])]
    body.append('<h1>学员版 — 任务进度与取值记入表</h1>')
    body.append('''<p>用法：打印本页（或直接在屏幕上填写）。每完成一个任务，在「✓」栏打勾，
把你自己系统里的实际取值记到「我的系统取值」栏，遇到报错记到「问题记录」栏 —— 这张表交回来就是你的学习轨迹。</p>
<div class="box info"><b class="t">打印提示</b>
浏览器打印时建议 A4 横向、缩放 90%；页眉页脚会被本站的打印样式自动隐藏。
「文档给的 T-code / IMG 路径」一列是原教材的参考值，<b>不要照抄到系统里</b>，只作为「该去哪个配置点」的提示。</div>''')
    body.append('<div class="tblwrap"><table class="tbl"><thead><tr>'
                '<th>模块</th><th>总体完成</th><th>备注</th></tr></thead><tbody>' + ''.join(
                    f'<tr><td>{esc(m["nav"])} · {esc(m["title"].split("（")[0])}（{len(tasks_of(m["code"]))} 个任务）</td>'
                    '<td>＿＿＿ / ' + str(len(tasks_of(m['code']))) + '</td><td></td></tr>'
                    for m in MODULES) + '</tbody></table></div>')

    for m in MODULES:
        mtasks = tasks_of(m['code'])
        body.append(f'<h2 id="w-{m["code"]}">{esc(m["nav"])} · {esc(m["title"])}'
                    f'　<span class="dim">（{len(mtasks)} 个任务 / '
                    f'{sum(t["nimg"] for t in mtasks)} 张画面）</span></h2>')
        rows = []
        for t in mtasks:
            tc = ' '.join(f'<code>{esc(c)}</code>' for c in t['tcodes'][:4]) or '—'
            path = esc((t['path'] or '')[:70]) + ('…' if t['path'] and len(t['path']) > 70 else '')
            fb = esc(t['fb'] or '—')
            rows.append(f'<tr><td>{t["no"]:02d}</td>'
                        f'<td><a href="{m["file"]}#{t["anchor"]}">{esc(t["title"])}</a></td>'
                        f'<td>{fb}</td><td>{tc}</td><td><span class="dim">{path or "—"}</span></td>'
                        f'<td class="wblank"></td><td class="wblank"></td><td class="wblank"></td></tr>')
        body.append('<div class="tblwrap"><table class="tbl ws"><thead><tr><th>#</th><th>任务（点开看手顺）</th>'
                    '<th>前后台</th><th>文档给的 T-code</th><th>文档给的 IMG 路径</th>'
                    '<th>我的系统取值</th><th>问题记录</th><th>✓</th></tr></thead><tbody>'
                    + ''.join(rows) + '</tbody></table></div>')

    body.append('<h2 id="finish">修了判定（自己打勾）</h2>')
    checks = [
        '能在自己系统里用 <code>SPRO</code> 打开后台，并找到 FI 的「公司代码」配置点。',
        '能说出「科目组 + 字段状态变式」如何决定凭证画面里哪些字段可见/必输。',
        '能用 <code>FS00</code> 建一个总账科目，并说清「税务类型 <code>-</code>/<code>+</code>/<code>*</code>」的区别。',
        '能说明收货与收发票时「材料采购（GR/IR）」科目各自动什么凭证。',
        '能解释物料「评估类」与 <code>OBYC</code>（BSX/WRX）的关系，并知道评估类出错时怎么补救。',
        '能独立完成 采购申请 → 采购订单 → 收货 → 发票校验 四步（并说出四个 T-code）。',
        '能完成 独立需求 → MRP → 计划订单转生产订单 → 下达 → 发货 → 确认 → 收货 的 PP 主链条。',
        '能用 <code>CK11N</code>/<code>CK24</code> 完成一次标准成本估算、标记与发布。',
        '能完成 报价 → 销售订单 → 外向交货 → 发票 → 过账 的 SD 主链条（并说出五个 T-code）。',
        '遇到报错时，能按「排错与踩坑」页的 6 项前提检查逐项排查。',
    ]
    body.append('<ul class="check">' + ''.join(f'<li>{x}</li>' for x in checks) + '</ul>')
    body.append('''<div class="grid cards">
<div class="card"><b>自测成绩</b><span>＿＿＿ / 30 题（合格 75% = 23 题）</span></div>
<div class="card"><b>完成的模块</b><span>＿＿＿ / 6</span></div>
<div class="card"><b>未解决的问题</b><span>＿＿＿ 项（写在下表）</span></div>
</div>
<div class="tblwrap"><table class="tbl ws"><thead><tr><th>#</th><th>我遇到的问题（现象 / 报错号）</th><th>我怎么解决的（T-code）</th><th>还需请教讲师</th></tr></thead><tbody>'''
                + ''.join('<tr><td>%d</td><td class="wblank"></td><td class="wblank"></td><td class="wblank"></td></tr>' % i
                          for i in range(1, 11)) + '</tbody></table></div>')
    return page('worksheet.html', '学员版（记入表）· S/4HANA 中文实训站', '\n'.join(body),
                desc='S/4HANA 中文实训站学员版：222 个任务的进度打勾表、自系统取值记录栏与修了判定清单，可打印。',
                active='worksheet.html')


# ------------------------------------------------------------ quiz
def auto_questions(n=12, seed=20260912):
    """T-code questions generated straight from the document's own task/T-code pairs."""
    rnd = random.Random(seed)
    pool = [(m, t) for m, t in ALL_TASKS if t['tcodes'] and t['nimg'] >= 2]
    # prefer tasks whose T-code is used by only a few tasks (less ambiguous)
    by_tc = {}
    for m, t in ALL_TASKS:
        for c in t['tcodes']:
            by_tc.setdefault(c, []).append(t['title'])
    pool = [(m, t) for m, t in pool if all(len(by_tc[c]) <= 3 for c in t['tcodes'])]
    rnd.shuffle(pool)
    all_tc = sorted({c for m, t in ALL_TASKS for c in t['tcodes']})
    qs = []
    seen = set()
    for m, t in pool:
        if len(qs) >= n:
            break
        if m['code'] in seen and len([q for q in qs if q['mod'] == m['code']]) >= 3:
            continue
        correct = t['tcodes'][0]
        others = [c for c in all_tc if c not in t['tcodes']]
        rnd.shuffle(others)
        opts = others[:3]
        if len(opts) < 3:
            continue
        rnd.shuffle(opts)
        keys = ['A', 'B', 'C', 'D']
        items = opts + [correct]
        rnd.shuffle(items)
        ans = keys[items.index(correct)]
        qs.append(dict(mod=mod_of(m['code'])['nav'], tag='T-code',
                       q=f'教材文档《S4.docx》中，「<a href="{mod_of(m["code"])["file"]}#{t["anchor"]}">{esc(t["title"])}</a>」'
                         f'这一步出现的是哪个 T-code？',
                       opts=[(k, f'<code>{esc(v)}</code>') for k, v in zip(keys, items)],
                       ans=ans,
                       exp=f'原文档在该任务的正文里出现 <code>{esc(correct)}</code>'
                           f'（该任务所属模块：{esc(mod_of(m["code"])["nav"])}，共 {t["nimg"]} 张实机画面）。'
                           f'其余三项出现在别的模块的任务里，可到 <a href="tcode.html">T-code 速查</a> 反查。'))
        seen.add(m['code'])
    return qs


HAND_QUESTIONS = [
    dict(mod='准备', tag='后台入口', q='教材里进「后台配置」用的入口是什么？',
         opts=[('A', '<code>SPRO</code>（SAP 参考 IMG）'), ('B', '<code>SE38</code>'),
               ('C', '<code>SM30</code>'), ('D', '<code>SU01</code>')], ans='A',
         exp='原文档：「在事务代码处输入 <code>spro</code>，进入后台配置页面」。SE38/SU01 是 ABAP 编辑器与用户维护，SM30 是表维护。'),
    dict(mod='FI', tag='组织结构', q='教材里第一次「建公司」是在哪个任务里做的？',
         opts=[('A', '创建会计科目表'), ('B', '创建公司代码'), ('C', '维护公司代码的全局参数'),
               ('D', '定义公司代码的字段状态变式')], ans='B',
         exp='FI 任务 01「创建公司代码」，IMG 路径为「企业结构 → 定义 → 财务会计 → 编辑/复制/删除/检查公司代码」，'
             '教材建的是公司代码 <code>C999</code>「颐宁机械有限公司」。'),
    dict(mod='FI', tag='字段控制', q='凭证画面里某个字段能不能输入，由下面哪两个配置决定？',
         opts=[('A', '科目组 + 字段状态变式'), ('B', '记账期间 + 凭证类型'),
               ('C', '容差组 + 税码'), ('D', '评估类 + 更新组')], ans='A',
         exp='FI 任务 06「定义科目组及输入控制」与任务 07「定义字段状态变式」是一组：科目组决定字段状态变式怎么选，'
             '变式里的每个字段可以设为必输/可选/隐藏。'),
    dict(mod='FI', tag='科目主数据', q='《S4.docx》里「材料采购科目」为什么要「逐笔逐清」？',
         opts=[('A', '它是收货与收发票之间的过渡科目（GR/IR）'),
               ('B', '它是客户的统驭科目'), ('C', '它是损益类科目，年结必须清零'),
               ('D', '它是银行科目')], ans='A',
         exp='原文档说明：收货时借库存、贷材料采购；收发票时借材料采购、贷应付账款，两边在这一科目上对冲，'
             '所以需要逐笔逐清，也就是常说的 GR/IR 过渡科目。'),
    dict(mod='FI', tag='记账期间', q='「已经关掉的会计期间不允许对凭证进行更改」，这是哪个机制？',
         opts=[('A', '记账期间变式与期间开关（设置记账期间）'), ('B', '凭证归档'),
               ('C', '容差组'), ('D', '科目组的输入控制')], ans='A',
         exp='原文档：「这是用来对凭证的开关。已经关掉的会计期间就不允许对凭证进行更改。多个公司代码可以被统一控制开账和关帐。」'
             '对应任务 16〜18（定义变式 → 分配给公司代码 → 设置记账期间，最后一步是前台操作）。'),
    dict(mod='MM', tag='评估与自动记账', q='报「不可能为条目 <code>A999 BSX CN01</code> 确立帐户」，原文档给的补救办法是？',
         opts=[('A', '删掉已建的采购订单，修改物料会计视图 1 的评估类（本期/上期/上一年度都要改）'),
               ('B', '重新建公司代码'), ('C', '改客户账户组'), ('D', '把汇率改掉')], ans='A',
         exp='原文档明确写了这个处理，并建议在创建物料时就把评估类一次做对；<code>BSX</code> 是自动记账里存货科目的事务码。'),
    dict(mod='MM', tag='自动记账', q='自动记账（科目确定）用哪个 T-code 维护？',
         opts=[('A', '<code>OBYC</code>'), ('B', '<code>FS00</code>'), ('C', '<code>MMSC</code>'), ('D', '<code>MPR1</code>')],
         ans='A',
         exp='原文档多处指向 <code>OBYC</code>（任务 28「维护物料管理的自动记帐」，原文亦写「通过 T-CODE OBYC，按照如下方式维护」）。'
             '<code>FS00</code> 是总账科目维护、<code>MMSC</code> 用于库存地点主数据。'),
    dict(mod='MM', tag='采购链', q='采购到发票校验的主链条，顺序正确的是？',
         opts=[('A', '采购申请 <code>ME51N</code> → 采购订单 <code>ME21N</code> → 收货 <code>MIGO</code> → 发票校验 <code>MIRO</code> → 冻结发票下达 <code>MRBR</code>'),
               ('B', '采购订单 → 采购申请 → 发票校验 → 收货'),
               ('C', '收货 → 采购申请 → 采购订单 → 发票校验'),
               ('D', '发票校验 → 收货 → 采购订单 → 采购申请')], ans='A',
         exp='这是 MM 任务 36〜40 的顺序，也是本站「任务索引」里按序号排下来的顺序；冻结发票必须在下达之后才会计入应付。'),
    dict(mod='MM', tag='MRP', q='教材里运行物料需求计划用的是什么？',
         opts=[('A', '<code>MD03</code> 单层计划（MM 模块）/ <code>MD02</code>（PP 模块）'),
               ('B', '<code>MB1C</code>'), ('C', '<code>MMBE</code>'), ('D', '<code>COOIS</code>')], ans='A',
         exp='原文档 MM 任务 34 说明：「由于 BOM 要等到生产计划模块维护，现在不能按 BOM 展开，所以是单层计划」→ <code>MD03</code>；'
             'PP 模块 BOM 建好后用 <code>MD02</code>。库存/需求清单是 <code>MD04</code>，库存总览是 <code>MMBE</code>。'),
    dict(mod='PP', tag='标准成本', q='标准成本估算的「估算 → 标记 → 发布」分别用什么？',
         opts=[('A', '<code>CK11N</code> → <code>CK24</code> → <code>CK24</code>'),
               ('B', '<code>CK24</code> → <code>CK11N</code> → <code>MM03</code>'),
               ('C', '<code>KP26</code> → <code>CK11N</code> → <code>CK40N</code>'),
               ('D', '<code>MM02</code> → <code>CK11N</code> → <code>CK24</code>')], ans='A',
         exp='PP 任务 22（新建产品成本估算 <code>CK11N</code>）→ 任务 23（标记价格 <code>CK24</code>）→ 任务 25（发布价格 <code>CK24</code>）；'
             '<code>MM03</code> 只是显示（任务 24/26 查看将来/已发布的计划价格）。'),
    dict(mod='PP', tag='排错', q='成本估算报「没有内部作业 <code>LAB 1001</code> 的价格可被确定」，原文档怎么处理？',
         opts=[('A', '通过 <code>CK11N</code> 维护价格，并<b>退出 CK11N 后重新执行 <code>CK24</code></b>'),
               ('B', '重建物料主数据'), ('C', '把工艺路线删掉重做'), ('D', '改公司代码')], ans='A',
         exp='原文档原文：「通过 CK11N 要，按照如下方式维护价格，即可」「退出 CK11N，然后重新执行 CK24」；'
             '作业价格本身在 <code>KP26</code>（任务 12 设置作业输出价格）维护。'),
    dict(mod='PP', tag='生产订单', q='生产订单下达后到结算，正确顺序是？',
         opts=[('A', '下达 <code>CO02</code> → 发货 → 确认 <code>CO11N</code> → 收货 <code>MIGO</code> → 差异结算 <code>KO88</code>'),
               ('B', '确认 → 下达 → 结算 → 收货 → 发货'),
               ('C', '收货 → 发货 → 下达 → 确认 → 结算'),
               ('D', '结算 → 收货 → 确认 → 发货 → 下达')], ans='A',
         exp='PP 任务 42〜48 的顺序：<code>CO02</code> 下达 → 对生产订单发货 → <code>CO11N</code> 工单确认 → '
             '<code>MIGO</code> 收货 → <code>CO03</code> 看成本 → <code>CO02</code> 技术性完成 → <code>KO88</code> 差异结算。'),
    dict(mod='CO', tag='分配与分摊', q='教材里「行政部房租按各成本中心占地面积分配」用的是哪一种？',
         opts=[('A', '分配循环（按统计指标的实际值确定追踪因素）'), ('B', '分摊循环'),
               ('C', '成本中心重过账 <code>KB61</code>'), ('D', '作业类型价格 <code>KP26</code>')], ans='A',
         exp='CO 任务 20「定义分配循环」（原文档：接收方追踪因素 = 物业租金面积统计指标的实际统计值）→ 任务 21「分配」；'
             '电费走的是任务 23「定义分摊循环」与任务 24「分摊」。'),
    dict(mod='CO', tag='成本要素', q='初级成本要素与次级成本要素的区别是？',
         opts=[('A', '初级对应财务会计科目，次级只在 CO 内部（分摊、结算等）流动'),
               ('B', '初级只能用于成本中心，次级只能用于内部订单'),
               ('C', '初级是收入类，次级是费用类'),
               ('D', '两者没有区别，只是叫法不同')], ans='A',
         exp='教材任务 05「新建初级成本要素」（<code>KA01</code>）与任务 06「建立次级成本要素」（<code>KA06</code>）：'
             '次级成本要素不产生 FI 凭证，用于 CO 内部的分摊/结算等再分配。'),
    dict(mod='CO', tag='内部订单', q='内部订单的费用归集完之后，用什么做结算？',
         opts=[('A', '<code>KO88</code>'), ('B', '<code>FB50</code>'), ('C', '<code>KK01</code>'), ('D', '<code>KB31N</code>')],
         ans='A',
         exp='CO 任务 33「内部订单的结算」＝<code>KO88</code>（PP 的差异结算也是它）；'
             '<code>KK01</code> 建统计指标、<code>KB31N</code> 录入统计指标数量、<code>FB50</code> 录总账凭证。'),
    dict(mod='SD', tag='销售范围', q='「销售范围」由哪三个要素组成？',
         opts=[('A', '销售组织 + 分销渠道 + 产品组'), ('B', '销售组织 + 工厂 + 库存地点'),
               ('C', '客户 + 物料 + 定价过程'), ('D', '公司代码 + 采购组织 + 销售办公室')], ans='A',
         exp='SD 任务 01〜07 的顺序就是先建这三个要素（销售组织/分销渠道/产品组），再「设置销售范围」；'
             '订单、定价、交货、税确定都靠销售范围定位。'),
    dict(mod='SD', tag='合作伙伴', q='原文档表格里，<code>BP</code> 对应哪个合作伙伴功能？',
         opts=[('A', '收票方'), ('B', '售达方'), ('C', '付款方'), ('D', '送达方')], ans='A',
         exp='原文档任务 33 的表格给出：<code>SP</code> 售达方、<code>BP</code> 收票方、<code>PY</code> 付款方、<code>SH</code> 送达方。'),
    dict(mod='SD', tag='销售链', q='从报价走到发票过账，正确的 T-code 顺序是？',
         opts=[('A', '报价 <code>VA21</code> → 销售订单 → 交货 <code>VL01N</code> → 发票 <code>VF01</code> → 过账 <code>VF02</code>'),
               ('B', '销售订单 → 报价 → 发票 → 交货'),
               ('C', '交货 → 报价 → 销售订单 → 发票'),
               ('D', '报价 → 交货 → 销售订单 → 发票')], ans='A',
         exp='SD 任务 40〜44：<code>VA21</code> 创建报价 → 参照创建销售订单 → <code>VL01N</code> 创建外向交货 → '
             '<code>VF01</code> 创建发票 → <code>VF02</code> 过账到财务会计。'),
    dict(mod='SD', tag='排错', q='<code>VL01N</code> 报「对于直到所选日期的交货没有到期的计划行」，原文档的解法是？',
         opts=[('A', '把选择日期改成与订单一致'), ('B', '改用 <code>VF01</code> 创建交货'),
               ('C', '删除销售订单重建'), ('D', '修改客户主数据')], ans='A',
         exp='原文档原文：「VL01N 时【对于直到所选日期的交货没有到期的计划行】解决方案将选择日期与订单保持一致」。'
             '另有相关一条：无法创建 <code>VL01N</code> 时可用 <code>MB1C</code> 501 录入期初库存解决（库存为 0）。'),
    dict(mod='综合', tag='环境差异', q='教材里的公司代码、工厂、物料编号（<code>C999</code> / <code>F999</code> / <code>R999-100</code>）意味着什么？',
         opts=[('A', '原文档作者的教材环境取值，操作顺序可以照做，编号要换成自己系统的'),
               ('B', 'SAP 出厂标准值，所有系统都一样'),
               ('C', '必须完全照抄才能通过配置'),
               ('D', '是随机生成的示例，没有意义')], ans='A',
         exp='这些值来自原作者的系统（本站每张画面都保留了原始文件名可对照 Word 原文）。'
             '新版/不同版本与不同行业方案下标准值可能不同，所以本站不把任何一个取值当作「必背的标准答案」。'),
]


def build_quiz():
    autos = auto_questions(12)
    qs = []
    for q in autos:
        qs.append(q)
    qs.extend(HAND_QUESTIONS[:18])
    body = [breadcrumb([('index.html', '首页'), (None, '自测')])]
    body.append('<h1>自测 30 题（自动评分，75% 为合格）</h1>')
    body.append(f'''<p>前 12 题来自教材文档 <code>S4.docx</code> 里「任务 ↔ T-code」的真实对应（点题号里的任务名可以看到该任务的手顺与画面），
后 18 题覆盖组织结构、字段控制、自动记账、分配/分摊、生产与销售链条、以及原文档记录的排错处理。
点选项立刻判分并显示解说；一题只能答一次，可以用「全部重做」重来。</p>
<div class="box info"><b class="t">评分</b>
30 题：75%（23 题）合格，90%（27 题）以上优秀。错题请回到对应模块的手顺页重做一遍，再到「排忧与踩坑」页核对报错处理。</div>''')
    for i, q in enumerate(qs, 1):
        opts = ''.join(f'<div class="opt" data-key="{k}">{v}</div>' for k, v in q['opts'])
        body.append(f'''<div class="quiz-q" data-answer="{q['ans']}">
  <div class="q-meta"><span class="tag gray">{esc(q['mod'])}</span><span class="tag">{esc(q['tag'])}</span></div>
  <h4>{i}. {q['q']}</h4>
  <div class="opts">{opts}</div>
  <div class="explain">{q['exp']}</div>
</div>''')
    body.append('''<h2 id="checklist">实机验收清单（做完自测再逐项打勾）</h2>
<ul class="check">
<li>能在自己系统里用 <code>SPRO</code> 打开后台，并找到本教材讲的任意一个配置点。</li>
<li>能用 <code>FS00</code> 建一个总账科目，并解释「税务类型」三个符号的含义。</li>
<li>能说出采购链与销售链各 5 个 T-code，并说明每一步产生的凭证/单据。</li>
<li>能说明物料「评估类」与自动记账 <code>OBYC</code> 的关系，以及评估类出错时的补救顺序。</li>
<li>能用 <code>CK11N</code>/<code>CK24</code> 完成估算、标记、发布，并解释「标记」与「发布」的区别。</li>
<li>遇到教材里的 10 个报错现象，能说出「现象 → 原因 → 处理 T-code」。</li>
</ul>
<div class="box ok"><b class="t">合格判定</b>自测正确率 ≥75% <b>且</b> 实机验收清单 6 项全部打勾 = 具备独立跟做本教材全套配置与操作的能力。</div>''')
    return page('quiz.html', '自测 30 题 · S/4HANA 中文实训站', '\n'.join(body),
                desc='S/4HANA 中文实训站自测：30 题自动评分测验，覆盖 T-code、后台路径、组织结构、自动记账、生产与销售链条与排错。',
                active='quiz.html')
