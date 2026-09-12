#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Module pages: prep / fi / co / mm / pp / sd."""
from common import (MODULES, tasks_of, mod_of, esc, txt, render_task, page,
                    breadcrumb, SEQ, DIM)

ORDER = ['prep', 'fi', 'co', 'mm', 'pp', 'sd']


def module_stats(code):
    ts = tasks_of(code)
    shots = sum(t['nimg'] for t in ts)
    back = sum(1 for t in ts if t['fb'] == '后台')
    front = sum(1 for t in ts if t['fb'] == '前台')
    tcs = []
    for t in ts:
        for c in t['tcodes']:
            if c not in tcs:
                tcs.append(c)
    paths = sum(1 for t in ts if t['path'])
    return dict(tasks=len(ts), shots=shots, back=back, front=front, tcodes=tcs, paths=paths,
                steps=sum(len(t['steps']) for t in ts))


def toc_table(code):
    rows = []
    for t in tasks_of(code):
        fb = esc(t['fb']) if t['fb'] else '—'
        tc = ' '.join(f'<code>{esc(c)}</code>' for c in t['tcodes'][:5]) or '—'
        rows.append(f'<tr><td><a href="#{t["anchor"]}">任务 {t["no"]:02d}</a></td>'
                    f'<td><a href="#{t["anchor"]}">{esc(t["title"])}</a></td>'
                    f'<td>{fb}</td><td>{tc}</td><td>{t["nimg"]}</td><td>{len(t["steps"])}</td></tr>')
    return ('<div class="tblwrap"><table class="tbl idx"><thead><tr><th>序号</th><th>任务</th>'
            '<th>前后台</th><th>文档中的 T-code</th><th>画面</th><th>手顺步</th></tr></thead>'
            '<tbody>' + ''.join(rows) + '</tbody></table></div>')


def build(code):
    m = mod_of(code)
    st = module_stats(code)
    ts = tasks_of(code)
    others = [c for c in ORDER if c != code]
    i = ORDER.index(code)
    prev = mod_of(ORDER[i - 1]) if i > 0 else None
    nxt = mod_of(ORDER[i + 1]) if i < len(ORDER) - 1 else None

    body = [breadcrumb([('index.html', '首页'), (None, m['title'])])]
    body.append(f'<h1>{esc(m["title"])}</h1>')
    body.append(f'<p class="kicker">{esc(m["kicker"])}</p>')
    body.append('<div class="toc">'
                '<a href="#guide">1. 本模块导读</a>'
                '<a href="#toc">2. 任务目录</a>'
                '<a href="#steps">3. 手顺（逐个任务）</a>'
                '<a href="#sources">4. 关于截图与取值</a></div>')
    body.append('<div class="grid cards">'
                f'<div class="card"><b>{st["tasks"]}</b><span>个任务</span></div>'
                f'<div class="card"><b>{st["shots"]}</b><span>张实机画面</span></div>'
                f'<div class="card"><b>{st["steps"]}</b><span>个手顺步骤</span></div>'
                f'<div class="card"><b>{st["back"]}/{st["front"]}</b><span>后台 / 前台任务</span></div>'
                '</div>')

    body.append('<h2 id="guide">1. 本模块导读</h2>')
    for p in m['intro']:
        body.append(f'<p>{p}</p>')
    body.append('<div class="panel"><b>本模块重点</b><ul>' +
                ''.join(f'<li>{x}</li>' for x in m['focus']) + '</ul>')
    if st['tcodes']:
        body.append('<p style="margin-top:10px">文档中出现的 T-code：' +
                    ' '.join(f'<a class="tag gray" href="tcode.html#{esc(c)}">{esc(c)}</a>'
                             for c in st['tcodes']) +
                    '（完整说明见 <a href="tcode.html">T-code / IMG 路径速查</a>）</p>')
    body.append('</div>')

    body.append(f'<h2 id="toc">2. 任务目录（{st["tasks"]} 个）</h2>')
    body.append(f'<p>其中 {st["paths"]} 个任务给出了原文档中的 IMG 后台菜单路径；'
                '带 <span class="fb">后台</span> 标注的是定制（配置）任务，带 '
                '<span class="fb img">前台</span> 标注的是日常业务操作任务；没有标注的任务原文未指明，'
                '请按任务名自行判断（一般「定义/维护…参数」＝后台，「创建/输入/显示…凭证、订单、发票」＝前台）。</p>')
    body.append(toc_table(code))

    body.append('<h2 id="steps">3. 手顺（逐个任务）</h2>')
    body.append('<div class="box info"><b class="t">怎么用这一页</b>'
                '每个任务按原文档的顺序保留：先读「说明」，再照「IMG 路径」进入配置点，'
                '然后按编号步骤（每一步都配原文档的实机画面）逐屏操作。'
                '画面里的红色方框/箭头是原文档作者标注的「要填/要选的地方」。'
                '点击任意画面可放大（1×/2×/3×，ESC 关闭）。</div>')
    first = 0
    for t in ts:
        body.append(render_task(code, t))
        first += 1

    body.append('<h2 id="sources">4. 关于截图与取值</h2>')
    body.append('<div class="box warn"><b class="t">画面来自原教材文档</b>'
                '本模块的截图全部来自 <code>S4.docx</code> 中作者在真实系统里截取的中文界面画面'
                '（原始文件名 <code>imageNNN.png</code> 保留在每张图的图注里，可与 Word 原文逐张对照）。'
                '本站没有对这些画面做任何重绘或模拟。</div>')
    body.append('<div class="box info"><b class="t">取值请以自系统为准</b>'
                '文档中的组织结构与主数据编号（公司代码 <code>C999</code>、公司名「颐宁机械有限公司」、'
                '工厂 <code>F999</code>、物料 <code>R999-100</code>/<code>T999-100</code>/<code>F999-100</code>、'
                '客户 <code>K001</code>/<code>K002</code> 等）都来自原作者的教材环境。'
                '照着手顺做时，<b>操作顺序与配置点可以照搬，具体编号/名称请换成你自己系统里的值</b>；'
                '遇到与文档不同的提示消息，先看「<a href="issues.html">排错与踩坑</a>」页里原文档记录的同类问题。</div>')

    navlink = []
    if prev:
        navlink.append(f'<a href="{prev["file"]}">← 上一模块：{esc(prev["nav"])} {esc(prev["title"])}</a>')
    if nxt:
        navlink.append(f'<a href="{nxt["file"]}">下一模块：{esc(nxt["nav"])} {esc(nxt["title"])} →</a>')
    navlink.append('<a href="tasks.html">全部 222 个任务索引 →</a>')
    body.append('<div class="panel" style="margin-top:22px">' + '<br>'.join(navlink) + '</div>')

    return page(m['file'], f'{m["title"]} · 手顺与实机画面',
                '\n'.join(body),
                desc=f'{m["title"]}：{st["tasks"]} 个任务的手顺、IMG 路径、T-code 与 {st["shots"]} 张实机画面截图。'
                     f'内容依据教材文档 S4.docx 整理。',
                active=m['file'])


if __name__ == '__main__':
    print(build('fi')[:2000])
