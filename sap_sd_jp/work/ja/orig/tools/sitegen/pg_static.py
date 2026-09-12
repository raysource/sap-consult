#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Static pages: index / tasks (index+filter) / tcode / issues."""
import json
import os
import re
from collections import OrderedDict, Counter

from common import (MODULES, MODEL, ROOT, esc, txt, page, breadcrumb, IMAGES,
                    TOTAL_SHOTS, mod_of, tasks_of)

SUMMARY = {}
_sp = os.path.join(ROOT, 'work/images_summary.json')
if os.path.exists(_sp):
    SUMMARY = json.load(open(_sp))

ALL_TASKS = [(m, t) for m in MODEL for t in m['tasks']]

# short, hand-checked labels for T-codes that appear in the document (用途 column
# is derived from the tasks where the doc uses them - see build_tcode())
STEPS_TOTAL = sum(len(t['steps']) for m in MODEL for t in m['tasks'])


def stats():
    return dict(modules=len(MODEL), tasks=len(ALL_TASKS),
                steps=sum(len(t['steps']) for m in MODEL for t in m['tasks']),
                shots=sum(t['nimg'] for m in MODEL for t in m['tasks']),
                kept=SUMMARY.get('refs_kept', TOTAL_SHOTS),
                files=SUMMARY.get('unique_files', 0),
                docx_media=SUMMARY.get('media_files_in_docx', 0),
                dropped=SUMMARY.get('dropped_icons', 0),
                size_mb=round(SUMMARY.get('asset_bytes', 0) / 1e6, 1),
                paths=sum(1 for m in MODEL for t in m['tasks'] if t['path']),
                tcode_tasks=sum(1 for m in MODEL for t in m['tasks'] if t['tcodes']))


# ------------------------------------------------------------------ index
def build_index():
    st = stats()
    body = []
    hero = f'''<div class="hero"><div class="hero-inner">
  <div class="kicker">SAP S/4HANA · 全模块配置与操作 · 中文版 · 依据教材文档 <code>S4.docx</code>（{st['docx_media']} 张内嵌图片 / 425 页）</div>
  <h1>SAP S/4HANA 中文实训站</h1>
  <p class="lead">本站把一份 425 页的中文 S/4HANA 教材文档（<code>S4.docx</code>）整理成可离线浏览的训练网站：
  <b>{st['modules']} 大模块 · {st['tasks']} 个任务 · {st['steps']} 个手顺步骤 · {st['shots']} 张实机操作画面</b>。
  每个任务都给出<b>原文档的 IMG 后台菜单路径</b>、<b>文档中出现的 T-code</b>、<b>逐步手顺</b>，
  以及<b>原文档作者在真实系统里截取的中文界面画面</b>（红色方框是原作者标注的要填/要选的位置）。</p>
  <p class="lead">覆盖范围：<b>准备工作（登录 / SPRO 后台）→ 财务会计 FI → 管理会计 CO → 物料管理 MM →
  生产计划 PP → 销售与分销 SD</b>，并按原文档顺序保留从组织结构、主数据、配置参数一路做到业务操作与报表的完整链条。</p>
  <div class="toc">
    <a href="#what">1. 这个站是什么</a>
    <a href="#scale">2. 规模与构成</a>
    <a href="#route">3. 学习路线</a>
    <a href="#cards">4. 六个模块</a>
    <a href="#howto">5. 页面使用说明</a>
    <a href="#tools">6. 配套页面（讲师/学员/自测）</a>
    <a href="#truth">7. 关于画面与取值的说明</a>
    <a href="#sisters">8. 同目录的姊妹站</a>
  </div></div></div>'''


    body.append('<h2 id="what">1. 这个站是什么</h2>')
    body.append('''<p>这不是一份「概念讲义」，而是一份<b>照着能做出来的操作手册</b>。原文档 <code>S4.docx</code> 的形态是
「一段文字说明 + 一串实机截图」，作者（原文档署名「马老师学习笔记」）把每个配置点和每笔业务都用画面记了下来。
本站保留了这个形态，并补上三样原文不方便检索的东西：</p>
<ul>
<li><b>IMG 后台路径单独抽出来</b>（原文档中 {paths} 个任务给出了菜单路径），可以点击复制，直接照着在 SPRO 里点；</li>
<li><b>T-code 单独抽出来</b>（{tc} 个任务的正文里出现了事务代码），汇总成 <a href="tcode.html">T-code / IMG 路径速查</a>；</li>
<li><b>任务索引 + 过滤</b>（<a href="tasks.html">{tasks} 个任务</a>），可以按模块或关键词（任务名、T-code）筛选。</li>
</ul>
<div class="box info"><b class="t">原始素材的形态</b>
原文档是「配置手册式」的：说明偏短，重点在画面上。所以本站的每个手顺步骤 = <b>原文的说明 + 该步骤对应的画面</b>；
原文没写文字、只放了画面的步骤，本站标注为「按上一屏继续操作（画面 N）」，不做臆测补充。</div>'''.format(
        paths=st['paths'], tc=st['tcode_tasks'], tasks=st['tasks']))

    body.append('<h2 id="scale">2. 规模与构成</h2>')
    rows = []
    for m in MODULES:
        ts = tasks_of(m['code'])
        shots = sum(t['nimg'] for t in ts)
        steps = sum(len(t['steps']) for t in ts)
        back = sum(1 for t in ts if t['fb'] == '后台')
        front = sum(1 for t in ts if t['fb'] == '前台')
        rows.append(f'<tr><td><a href="{m["file"]}">{esc(m["title"])}</a></td><td>{len(ts)}</td>'
                    f'<td>{steps}</td><td>{shots}</td><td>{back} / {front}</td></tr>')
    body.append('<div class="tblwrap"><table class="tbl"><thead><tr><th>模块</th><th>任务</th>'
                '<th>手顺步骤</th><th>实机画面</th><th>后台 / 前台（原文档标注）</th></tr></thead><tbody>'
                + ''.join(rows) +
                f'</tbody><tfoot><tr><th>合计</th><th>{st["tasks"]}</th><th>{st["steps"]}</th>'
                f'<th>{st["shots"]}</th><th>—</th></tr></tfoot></table></div>')
    body.append(f'''<div class="grid cards">
  <div class="card"><b>{st['docx_media']}</b><span>原文档内嵌图片总数</span></div>
  <div class="card"><b>{st['kept']}</b><span>本站收录的画面引用</span></div>
  <div class="card"><b>{st['files']}</b><span>去重后的图片文件</span></div>
  <div class="card"><b>{st['size_mb']} MB</b><span>图片体积（离线可用）</span></div>
</div>''')
    body.append(f'<p>原文档内嵌 {st["docx_media"]} 张图片中，有 {st["dropped"]} 张是图标/装饰（尺寸 90×14 以下），'
                f'不构成操作画面，本站已排除；其余 {st["kept"]} 处引用全部保留（同一张图在多个步骤复用时只存一份文件）。'
                '每张图下方都标注了<b>原文档文件名</b>（如 <code>image1301.png</code>）与像素尺寸，方便与 Word 原文逐张核对。</p>')

    body.append('<h2 id="route">3. 学习路线</h2>')
    body.append('''<p>原文档的顺序本身就是一条可执行的路线 —— 从「建公司」开始，依次把财务、成本、物料、生产、销售的
组织结构与主数据配好，再跑业务。建议按下面的顺序走，不要跳：</p>''')
    route = [
        ('prep', '先把客户端连上、学会进 SPRO 后台', '后面所有配置都在 SPRO 里点，先熟悉这个入口。'),
        ('fi', '财务会计 FI（组织结构 → 科目 → 凭证 → 应收应付 → 报表）', 'FI 的组织结构（公司代码/科目表/会计年度）是 CO、MM、SD 的公共前提。'),
        ('co', '管理会计 CO（成本控制范围 → 成本中心 → 成本要素/作业类型 → 分配分摊 → 内部订单）', 'CO 依赖 FI 的科目与公司代码，放在 FI 之后最顺。'),
        ('mm', '物料管理 MM（工厂/采购组织 → 物料主数据 → 自动记账 → MRP → 采购流程）', 'MM 是 PP 和 SD 的数据来源：物料主数据、工厂、库存地点。'),
        ('pp', '生产计划 PP（BOM/工作中心/工艺路线 → 成本估算 → MRP → 生产订单 → 结算）', 'PP 要用到 MM 的物料与采购，也用到 CO 的成本要素与作业类型。'),
        ('sd', '销售与分销 SD（销售范围 → 定价/税 → 主数据 → 报价→订单→交货→发票）', 'SD 处在最后：它消费前面配好的物料、客户、会计科目与更新组。'),
    ]
    body.append('<div class="grid cards">' + ''.join(
        f'<div class="card"><b>{i + 1}　{esc(mod_of(c)["nav"])}</b><span>{esc(t1)}</span>'
        f'<span class="dim">{esc(t2)}</span><a href="{mod_of(c)["file"]}">进入 {esc(mod_of(c)["nav"])} →</a></div>'
        for i, (c, t1, t2) in enumerate(route)) + '</div>')

    body.append('<h2 id="cards">4. 六个模块</h2>')
    cards = []
    for m in MODULES:
        ts = tasks_of(m['code'])
        shots = sum(t['nimg'] for t in ts)
        tcs = []
        for t in ts:
            for c in t['tcodes']:
                if c not in tcs:
                    tcs.append(c)
        cards.append(
            f'<div class="card"><b>{esc(m["nav"])} · {esc(m["title"].split("（")[0])}</b>'
            f'<span>{esc(m["kicker"])}</span>'
            f'<span class="dim">{len(ts)} 个任务 · {sum(len(t["steps"]) for t in ts)} 步 · {shots} 张画面</span>'
            f'<span class="tags">' + ' '.join(f'<span class="tag gray">{esc(c)}</span>' for c in tcs[:8]) + '</span>'
            f'<a href="{m["file"]}">打开模块手顺 →</a></div>')
    body.append('<div class="grid cards">' + ''.join(cards) + '</div>')

    body.append('<h2 id="howto">5. 页面使用说明</h2>')
    body.append('''<div class="tblwrap"><table class="tbl"><thead><tr><th>页面上看到的</th><th>含义</th></tr></thead><tbody>
<tr><td><span class="fb">后台</span> / <span class="fb img">前台</span></td><td>原文档标注的配置/操作性质：后台 = IMG 定制（SPRO），前台 = 日常业务事务。没有标注的任务原文未说明，请按任务名判断。</td></tr>
<tr><td><b>IMG 路径（后台菜单）</b></td><td>原文档给出的菜单层级，已用 <code>→</code> 归一化分隔；点击可复制。</td></tr>
<tr><td><span class="tc">T-code</span></td><td>该任务正文里出现的事务代码（原文档中作者直接给出的）。</td></tr>
<tr><td><b>手顺步骤（编号圆点）</b></td><td>原文的顺序片段：一步 = 一段说明 + 该步骤的画面。含义不明的「按上一屏继续操作」= 原文只有画面没有文字。</td></tr>
<tr><td><b>画面 N</b></td><td>该截图在原文档中的出现序号（1 起），可用它与 Word 原文对照。</td></tr>
<tr><td><b>教材笔记 / 原理说明 / 踩坑提醒</b></td><td>原文档中「马老师学习笔记」以及「解释：…」类文字，本站按性质分色呈现；含报错的另见 <a href="issues.html">排错与踩坑</a>。</td></tr>
<tr><td>点击画面</td><td>打开灯箱放大：1× / 2× / 3×，ESC 关闭。另存图片可直接用于讲义。</td></tr>
</tbody></table></div>''')

    body.append('<h2 id="tools">6. 配套页面（讲师 / 学员 / 自测）</h2>')
    body.append('''<div class="grid cards">
<div class="card"><b>任务索引（222 个任务）</b><span><a href="tasks.html">tasks.html</a> — 按模块或关键词（任务名 / T-code）过滤，点进任意任务的手顺。</span></div>
<div class="card"><b>T-code 与 IMG 路径速查</b><span><a href="tcode.html">tcode.html</a> — 文档中出现的全部事务代码 + 203 条后台菜单路径。</span></div>
<div class="card"><b>排错与踩坑</b><span><a href="issues.html">issues.html</a> — 原文档记录的报错现象与处理办法（税码 J1/FS217、评估类与 BSX、OBYC、VL01N 日期、CK11N/CK24 等）。</span></div>
<div class="card"><b>讲师版</b><span><a href="instructor.html">instructor.html</a> — 授课路线、时间安排、讲解顺序、必出问答与评分建议。</span></div>
<div class="card"><b>学员版（记入表）</b><span><a href="worksheet.html">worksheet.html</a> — 222 个任务的打勾进度表 + 自己系统里的取值记录栏，可直接打印。</span></div>
<div class="card"><b>自测（30 题）</b><span><a href="quiz.html">quiz.html</a> — 覆盖 T-code、后台路径、前后台判断与排错的自动评分测验，75% 为合格线。</span></div>
</div>''')

    body.append('<h2 id="truth">7. 关于画面与取值的说明</h2>')
    body.append('''<div class="box ok"><b class="t">画面是实机截图，不是示意图</b>
本站所有操作画面都是原教材文档 <code>S4.docx</code> 中作者在真实 S/4HANA 系统里截取的中文界面画面，
本站只做抽取与排版，没有重绘、没有生成、也没有模拟。原始文件名（<code>imageNNN.png</code>）在图注中保留，
可与 Word 原文逐张对照。</div>
<div class="box warn"><b class="t">示例值属于原作者的教材环境</b>
公司代码 <code>C999</code>、公司名「颐宁机械有限公司」、工厂 <code>F999</code>、库存地点 <code>P999</code>、
物料 <code>R999-100</code> / <code>T999-100</code> / <code>F999-100</code>、客户 <code>K001</code> / <code>K002</code>、
成本中心「行政部 / 制造部」、财务报表版本 <code>F999</code> 等，都是原文档作者在自己系统里建的示例数据。
<b>操作顺序与配置点可以照搬，编号与名称请换成你自己系统里的值</b>；报错消息也可能因版本/语言/客户化而不同。</div>
<div class="box info"><b class="t">本站不做的一件事</b>
本站不臆造原文档没有的内容：标准值、表名、字段名、SAP Note 编号若原文档未给出，这里也不会补。
需要精确的字段清单时，请在系统里用 F1（字段帮助）/ F4（可能值）与 SPRO 的「文档」按钮确认。</div>''')

    body.append('<h2 id="sisters">8. 同目录的姊妹站</h2>')
    body.append('''<p>本机 <code>~/Desktop/work/training/</code> 下还有一套<b>日文语境的专题实训站</b>（MTO / ETO / MTS / VC / 受注形態比較 / SD 受注処理），
它们各自聚焦一个业务形态、带完整配置手顺与练习；本站是<b>中文版的全模块手册站</b>，覆盖面更广、画面全部来自真实系统。</p>
<ul>
<li><a href="../index.html">训练站总览（hub，日文语境）</a> — 各专题站的入口与学习路线。</li>
<li>若只想练「一笔受注怎么从报价走到开票」，专题站更聚焦；若要先具备「有哪些配置点、在哪里配」的全貌，从本站开始。</li>
</ul>''')

    return page('index.html', '总览 · SAP S/4HANA 中文实训站（全模块手顺 + 实机画面）', '\n'.join(body),
                desc='SAP S/4HANA 中文实训站：依据 425 页教材文档 S4.docx 整理的 6 大模块 222 个任务手顺，'
                     '含 IMG 路径、T-code、逐步操作与 1385 张实机画面截图；附讲师版、学员版、自测与排错页。',
                active='index.html', hero=hero)


# ------------------------------------------------------------------ tasks
def build_tasks():
    body = [breadcrumb([('index.html', '首页'), (None, '任务索引')])]
    body.append('<h1>任务索引（全部 %d 个任务）</h1>' % len(ALL_TASKS))
    body.append('''<p>按住关键词过滤：任务名、T-code、模块名都可以。点「任务」列直接跳到该任务的完整手顺
（含 IMG 路径、每一步的实机画面）。带 <code>#</code> 的是该任务在模块页内的锚点。</p>''')
    chips = ['<span class="chip on" data-mod="all">全部</span>']
    for m in MODULES:
        chips.append(f'<span class="chip" data-mod="{m["code"]}">{esc(m["nav"])}（{len(tasks_of(m["code"]))}）</span>')
    body.append('<div class="filterbar">'
                '<input type="search" id="taskfilter" placeholder="输入任务名 / T-code / 关键词，例如 MIRO、容差、字段状态…">'
                + ''.join(chips) + '</div>')
    body.append(f'<p class="hitcount" id="hitcount">显示 {len(ALL_TASKS)} / {len(ALL_TASKS)} 个任务</p>')
    rows = []
    for m in MODULES:
        for t in tasks_of(m['code']):
            key = ' '.join([m['title'], m['nav'], t['title']] + t['tcodes'] + [t['path'] or ''])
            rows.append(
                f'<tr data-mod="{m["code"]}" data-key="{esc(key)}">'
                f'<td>{esc(m["nav"])}</td>'
                f'<td><a href="{m["file"]}#{t["anchor"]}">任务 {t["no"]:02d}</a></td>'
                f'<td><a href="{m["file"]}#{t["anchor"]}">{esc(t["title"])}</a></td>'
                f'<td>{esc(t["fb"] or "—")}</td>'
                f'<td>' + (' '.join(f'<code>{esc(c)}</code>' for c in t['tcodes'][:6]) or '—') + '</td>'
                f'<td>{t["nimg"]}</td>'
                f'<td>{len(t["steps"])}</td></tr>')
    body.append('<div class="tblwrap"><table class="tbl idx" id="idxtable"><thead><tr>'
                '<th>模块</th><th>序号</th><th>任务</th><th>前后台</th><th>T-code</th>'
                '<th>画面</th><th>手顺步</th></tr></thead><tbody>' + ''.join(rows) + '</tbody></table></div>')
    return page('tasks.html', f'任务索引 · 全部 {len(ALL_TASKS)} 个任务 · S/4HANA 中文实训站', '\n'.join(body),
                desc=f'S/4HANA 中文实训站任务索引：{len(ALL_TASKS)} 个任务可过滤检索，直达模块页内的手顺与实机画面。',
                active=None)


# ------------------------------------------------------------------ tcode
def collect_tcodes():
    tc = OrderedDict()
    for m in MODULES:
        for t in tasks_of(m['code']):
            for c in t['tcodes']:
                rec = tc.setdefault(c, {'mods': [], 'tasks': []})
                if m['nav'] not in rec['mods']:
                    rec['mods'].append(m['nav'])
                rec['tasks'].append((m, t))
    return tc


def build_tcode():
    tc = collect_tcodes()
    body = [breadcrumb([('index.html', '首页'), (None, 'T-code / IMG 路径速查')])]
    body.append('<h1>T-code 与 IMG 后台路径速查</h1>')
    body.append(f'''<p>下面两张表都<b>只从原文档正文里抽取</b>，不补充文档没写的内容：
第一张是文档中出现过的事务代码（共 {len(tc)} 个），第二张是文档给出的 IMG 后台菜单路径（{stats()['paths']} 条）。
「原文档中用它做的事」一列直接引用该 T-code 所在任务的标题，因此可以和模块页逐条对上。</p>
<div class="box info"><b class="t">怎么用</b>
拿到一个任务但不知道从哪儿进 → 先看模块页该任务的「IMG 路径」；想反查某个 T-code 在本教材里的用途 → 用下面的表。
路径行在模块页上可以点击复制。</div>''')
    body.append('<h2 id="tcodes">1. 事务代码（T-code）</h2>')
    rows = []
    for c, rec in sorted(tc.items(), key=lambda kv: (-len(kv[1]['tasks']), kv[0])):
        uses = '；'.join(f'<a href="{m["file"]}#{t["anchor"]}">{esc(t["title"])}</a>'
                        for m, t in rec['tasks'][:3])
        if len(rec['tasks']) > 3:
            uses += f' …等 {len(rec["tasks"])} 处'
        rows.append(f'<tr id="{esc(c)}"><td>{esc(c)}</td><td>{len(rec["tasks"])}</td>'
                    f'<td>{" / ".join(esc(x) for x in rec["mods"])}</td><td>{uses}</td></tr>')
    body.append('<div class="tblwrap"><table class="tbl"><thead><tr><th>T-code</th><th>出现任务数</th>'
                '<th>模块</th><th>原文档中用它做的事（任务名）</th></tr></thead><tbody>'
                + ''.join(rows) + '</tbody></table></div>')

    body.append('<h2 id="imgpaths">2. IMG 后台菜单路径</h2>')
    body.append('<p>按模块与任务顺序排列。分隔符统一为 <code>→</code>（原文混用 <code>－</code> 与 <code>-&gt;</code>）。</p>')
    prows = []
    for m in MODULES:
        for t in tasks_of(m['code']):
            if not t['path']:
                continue
            prows.append(f'<tr><td>{esc(m["nav"])}</td>'
                         f'<td><a href="{m["file"]}#{t["anchor"]}">任务 {t["no"]:02d} {esc(t["title"])}</a></td>'
                         f'<td><code>{esc(t["path"])}</code></td></tr>')
    body.append('<div class="tblwrap"><table class="tbl"><thead><tr><th>模块</th><th>任务</th>'
                '<th>IMG 路径（后台菜单）</th></tr></thead><tbody>' + ''.join(prows) + '</tbody></table></div>')
    body.append('<div class="box warn"><b class="t">路径写法会随版本/语言不同</b>'
                '同一配置点在 SPRO 里的中文/英文/日文菜单名可能不同，某些版本还会移动节点。'
                '按路径找不到时，用 SPRO 的搜索框按路径关键字搜，或直接用表 1 里的 T-code 进对应的定制视图。</div>')
    return page('tcode.html', 'T-code 与 IMG 路径速查 · S/4HANA 中文实训站', '\n'.join(body),
                desc='S/4HANA 中文实训站：从教材文档中抽取的全部 T-code 与 IMG 后台菜单路径速查表。',
                active='tcode.html')


# ------------------------------------------------------------------ issues
ISSUES = [
    dict(sym='税码 <code>J1</code> 无效（消息号 <code>FS217</code>）；不允许对公司代码 <code>C999</code> 科目 <code>12010101</code> 进行销项/进项税相关操作',
         cause='总账科目的「税务类型」没有放开对应的销项/进项税操作',
         fix='执行 <code>FS00</code> → 输入总账科目 <code>12010101</code> → 在「控制数据」里设置税务类型：'
             '「<code>-</code>」= 只允许进项税、「<code>+</code>」= 只允许销项税、「<code>*</code>」= 允许所有税类型 → '
             '之后即可正常录入客户发票/付款；<b>注意需要退出 <code>MIRO</code> 后重新进入</b>（原文档原文如此）',
         links=[('fi', 12, '新建材料采购科目'), ('fi', 13, '新建损益科目'), ('mm', 39, '输入采购发票')]),
    dict(sym='物料 <code>R999-100</code>「的强制帐户设置（输入帐户设置类别）」/ 不可能为条目 <code>A999 BSX CN01</code> 确立帐户',
         cause='物料的会计视图里「评估类」与自动记账（<code>OBYC</code> / 事务码 BSX）的科目确定对不上',
         fix='把已经创建的采购订单全部删掉 → 修改物料会计视图 1 里的「评估类」（原文档示例：原材料用 <code>3000</code>）→ '
             '<b>同时要维护本期、上期和上一年度的评估类</b>；原文档建议在创建物料（<code>MM01</code>）时就把评估类一次做对',
         links=[('mm', 21, '定义评估类'), ('mm', 22, '新建原材料主数据'), ('mm', 28, '维护物料管理的自动记帐')]),
    dict(sym='自动记账相关的报错（收货/发票时的科目确定失败）',
         cause='自动记账规则（<code>OBYC</code>）中对应事务码/评估类的科目未维护',
         fix='原文档原文：「通过 T-CODE <code>OBYC</code>，按照如下方式维护，可以解决此问题」（并附有画面）',
         links=[('mm', 28, '维护物料管理的自动记帐'), ('mm', 29, '将存货科目设置为只能自动记帐')]),
    dict(sym='物料 <code>F999-100</code> 不存在于存储地点 <code>P999</code> 003',
         cause='物料的「库存地点」视图没有该库存地点（或该库存地点主数据缺失）',
         fix='用 <code>MMSC</code> 维护（原文档原文：「<code>MMSC</code> 维护」），并确认 <code>MM01</code>/<code>MM02</code> 中已为该物料展开对应库存地点视图',
         links=[('mm', 2, '创建库存地点'), ('mm', 24, '新建产成品主数据')]),
    dict(sym='<code>VL01N</code> 报「对于直到所选日期的交货没有到期的计划行」',
         cause='交货创建时使用的选择日期与销售订单的计划行（需求日期）不在同一区间',
         fix='原文档原文：「解决方案将选择日期与订单保持一致」——把 <code>VL01N</code> 的选择日期改成与订单里的一致',
         links=[('sd', 42, '创建外向交货')]),
    dict(sym='无法创建 <code>VL01N</code> 外向交货单',
         cause='没有库存可发（教材场景里库存为 0）',
         fix='原文档原文：「<code>MB1C</code> 501 录入期初库存，可以解决无法创建 <code>VL01N</code> 外向交货单的问题」',
         links=[('sd', 42, '创建外向交货'), ('mm', 38, '创建采购收货')]),
    dict(sym='没有内部作业 <code>LAB 1001</code> 的价格可被确定（成本估算取不到作业价格）',
         cause='该作业类型在当期没有维护作业输出价格',
         fix='原文档原文：「通过 <code>CK11N</code> 要，按照如下方式维护价格，即可」→ 维护价格后<b>退出 <code>CK11N</code>，'
             '然后重新执行 <code>CK24</code></b>',
         links=[('pp', 12, '设置作业输出价格'), ('pp', 22, '新建产品成本估算'), ('pp', 23, '标记价格')]),
    dict(sym='「不要分配到成本中心，会计年度没有激活」',
         cause='公司代码的会计年度/记账期间未激活（成本中心不能过账）',
         fix='原文档以该标题记录此问题并附画面（未写出处理文字）。按 FI 侧的做法：检查记账期间变式与期间开关（见相关任务），确认公司代码的会计年度已激活后再做过账',
         links=[('fi', 18, '设置记帐期间(前台)'), ('co', 1, '创建成本控制范围'), ('co', 2, '将公司代码分配给成本控制范围')]),
    dict(sym='「客户化错误：非当前业务交易组」',
         cause='原文档在 SD 模块末尾以该标题记录了客户化报错（附画面）',
         fix='原文档未写出处理文字，只保留了画面。遇到时请对照本页第 3 节的前提检查清单逐项确认，并在 SPRO 中用「非当前业务交易组」作为关键字定位',
         links=[('sd', 48, '运行资产负债表（原文档末尾章）')]),
    dict(sym='生产订单/内部订单结算时「无错误，运行已经完成」但看不到结果',
         cause='这不是报错：结算运行本身成功，结果要到结算结果/报表里看',
         fix='按原文档顺序：先运行结算（<code>KO88</code>），再到「显示内部订单的结算结果」/「生产订单成本报表显示」里查看',
         links=[('co', 33, '内部订单的结算'), ('co', 34, '显示内部订单的结算结果'), ('pp', 48, '生产订单差异结算')]),
]

PRECHECK = [
    '会计期间是否已开启、会计年度是否已激活（<code>OB52</code> 类期间开关的配置见 FI 任务 16〜18）。',
    '组织结构是否已经分配到位：公司代码 ↔ 成本控制范围、工厂 ↔ 公司代码、采购组织 ↔ 公司代码/工厂、销售组织 ↔ 公司代码。',
    '物料主数据的会计视图是否维护了正确的<b>评估类</b>（本期/上期/上一年度），以及自动记账 <code>OBYC</code> 的科目确定是否完整。',
    '产成品的标准价格是否已经估算并<b>标记/发布</b>（<code>CK11N</code> → <code>CK24</code>），否则生产订单收货取不到价格。',
    '库存是否存在（原文档在多个环节用 <code>MB1C</code> 501 录入期初库存、或先做采购收货来补库存）。',
    '主数据是否齐全：客户（销售视图 + 合作伙伴）、物料（销售视图 + 销售价格/条件记录）、供应商（采购数据/信息记录）。',
]


def build_issues():
    body = [breadcrumb([('index.html', '首页'), (None, '排错与踩坑')])]
    body.append('<h1>排错与踩坑（原文档记录的问题与处理）</h1>')
    body.append('''<p>本页把原文档 <code>S4.docx</code> 中记录的报错现象与处理办法集中起来。
「现象」与「处理」两列尽量引用原文档原文（引用部分用引号标出）；原文档只留下画面、没有写出文字的情形也如实标注，
不做推断性补写。</p>''')
    body.append('<h2 id="table">1. 现象 → 处理一览</h2>')
    rows = []
    for i, it in enumerate(ISSUES, 1):
        links = '、'.join(
            f'<a href="{mod_of(c)["file"]}#t{n:02d}">{esc(mod_of(c)["nav"])} 任务 {n:02d} {esc(lbl)}</a>'
            for c, n, lbl in it['links'])
        rows.append(f'<tr><td>{i}</td><td>{it["sym"]}</td><td>{it["cause"]}</td><td>{it["fix"]}</td>'
                    f'<td>{links}</td></tr>')
    body.append('<div class="tblwrap"><table class="tbl"><thead><tr><th>#</th><th>现象 / 报错</th>'
                '<th>原因</th><th>原文档给出的处理</th><th>相关手顺</th></tr></thead><tbody>'
                + ''.join(rows) + '</tbody></table></div>')

    body.append('<h2 id="precheck">2. 出问题前先查这 6 件事（按原文档的报错归纳）</h2>')
    body.append('<ul class="check">' + ''.join(f'<li>{x}</li>' for x in PRECHECK) + '</ul>')

    body.append('<h2 id="notes">3. 全站「踩坑提醒」索引</h2>')
    body.append('<p>下面是从 222 个任务里筛出的、正文含报错/限制/解决字样的笔记（原文照录），'
                '按模块顺序排列，点任务名可回到手顺上下文。</p>')
    warn_rows = []
    for m in MODULES:
        for t in tasks_of(m['code']):
            for n in t['notes']:
                if n['kind'] != 'warn':
                    continue
                warn_rows.append(
                    f'<tr><td>{esc(m["nav"])}</td>'
                    f'<td><a href="{m["file"]}#{t["anchor"]}">任务 {t["no"]:02d} {esc(t["title"])}</a></td>'
                    f'<td>{txt(n["text"])}</td></tr>')
    body.append('<div class="tblwrap"><table class="tbl"><thead><tr><th>模块</th><th>任务</th>'
                '<th>原文笔记</th></tr></thead><tbody>' + ''.join(warn_rows) + '</tbody></table></div>')
    body.append('<div class="box info"><b class="t">找不到对应报错？</b>'
                '① 先用 <a href="tasks.html">任务索引</a> 找到相关任务，看它的「教材笔记 / 原理说明」；'
                '② 再用 <a href="tcode.html">T-code 速查</a> 确认自己进的是同一个定制视图；'
                '③ 最后用系统自身的 F1（字段帮助）/ F4（可能值）确认字段含义 —— 本站不臆造原文档没有的字段与表名。</div>')
    return page('issues.html', '排错与踩坑 · S/4HANA 中文实训站', '\n'.join(body),
                desc='教材文档记录的报错现象与处理：税码 J1/FS217、评估类与 BSX 自动记账、OBYC、MMSC、VL01N 日期、CK11N/CK24 等。',
                active='issues.html')
