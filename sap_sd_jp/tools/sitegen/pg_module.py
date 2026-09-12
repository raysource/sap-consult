#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Module pages: prep / fi / co / mm / pp / sd."""
from common import (MODULES, tasks_of, mod_of, esc, txt, render_task, page,
                    breadcrumb, SEQ, DIM, FB_IMG, FB_FRONT, fb_label)

ORDER = ['prep', 'fi', 'co', 'mm', 'pp', 'sd']


def module_stats(code):
    ts = tasks_of(code)
    shots = sum(t['nimg'] for t in ts)
    back = sum(1 for t in ts if t['fb'] == FB_IMG)
    front = sum(1 for t in ts if t['fb'] == FB_FRONT)
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
        fb = esc(fb_label(t)) if t['fb'] else '—'
        tc = ' '.join(f'<code>{esc(c)}</code>' for c in t['tcodes'][:5]) or '—'
        rows.append(f'<tr><td><a href="#{t["anchor"]}">タスク {t["no"]:02d}</a></td>'
                    f'<td><a href="#{t["anchor"]}">{esc(t["title"])}</a></td>'
                    f'<td>{fb}</td><td>{tc}</td><td>{t["nimg"]}</td><td>{len(t["steps"])}</td></tr>')
    return ('<div class="tblwrap"><table class="tbl idx"><thead><tr><th>No.</th><th>タスク</th>'
            '<th>IMG/業務</th><th>ドキュメント内の T-code</th><th>画面</th><th>手順ステップ</th></tr></thead>'
            '<tbody>' + ''.join(rows) + '</tbody></table></div>')


def build(code):
    m = mod_of(code)
    st = module_stats(code)
    ts = tasks_of(code)
    others = [c for c in ORDER if c != code]
    i = ORDER.index(code)
    prev = mod_of(ORDER[i - 1]) if i > 0 else None
    nxt = mod_of(ORDER[i + 1]) if i < len(ORDER) - 1 else None

    body = [breadcrumb([('index.html', 'ホーム'), (None, m['title'])])]
    body.append(f'<h1>{esc(m["title"])}</h1>')
    body.append(f'<p class="kicker">{esc(m["kicker"])}</p>')
    body.append('<div class="toc">'
                '<a href="#guide">1. 本モジュールのガイド</a>'
                '<a href="#toc">2. タスク一覧</a>'
                '<a href="#steps">3. 手順（タスクごと）</a>'
                '<a href="#sources">4. スクリーンショットと設定値について</a></div>')
    body.append('<div class="grid cards">'
                f'<div class="card"><b>{st["tasks"]}</b><span>タスク</span></div>'
                f'<div class="card"><b>{st["shots"]}</b><span>実機画面</span></div>'
                f'<div class="card"><b>{st["steps"]}</b><span>手順ステップ</span></div>'
                f'<div class="card"><b>{st["back"]}/{st["front"]}</b><span>IMG/業務のタスク</span></div>'
                '</div>')

    body.append('<h2 id="guide">1. 本モジュールのガイド</h2>')
    for p in m['intro']:
        body.append(f'<p>{p}</p>')
    body.append('<div class="panel"><b>このモジュールのポイント</b><ul>' +
                ''.join(f'<li>{x}</li>' for x in m['focus']) + '</ul>')
    if st['tcodes']:
        body.append('<p style="margin-top:10px">ドキュメントに出てくる T-code：' +
                    ' '.join(f'<a class="tag gray" href="tcode.html#{esc(c)}">{esc(c)}</a>'
                             for c in st['tcodes']) +
                    '（詳細は <a href="tcode.html">T-code / IMG パス早見表</a> を参照）</p>')
    body.append('</div>')

    body.append(f'<h2 id="toc">2. タスク目次（{st["tasks"]} 件）</h2>')
    body.append(f'<p>そのうち {st["paths"]} 件のタスクで、原教材ドキュメントの IMG 設定メニューパスが示されています；'
                '<span class="fb">IMG 設定</span> のマークが付いているのはカスタマイジング（設定）タスク、'
                '<span class="fb img">業務処理</span> と付いているのは日常業務の操作タスクです。表示がないタスクは原文でも明示されておらず、'
                'タスク名からご自身で判断してください（一般に「～の定義／～パラメータのメンテナンス」＝ IMG 設定、「伝票・指図・請求書の登録／入力／照会」＝業務処理）。</p>')
    body.append(toc_table(code))

    body.append('<h2 id="steps">3. 手順（タスクごと）</h2>')
    body.append('<div class="box info"><b class="t">このページの使い方</b>'
                '各タスクは原教材ドキュメントの順序どおりに掲載しています。まず「説明」を読み、次に「IMG パス」に従って設定ポイントへ進み、'
                'その後は番号付きのステップに沿って（各ステップに原教材ドキュメントの実機画面が付いています）、画面ごとに操作していきます。'
                '画面の赤い四角や矢印は、原教材ドキュメントの著者が「入力・選択すべき箇所」として付けたものです。'
                '画面をクリックすると拡大できます（1×/2×/3×、ESC で閉じる）。</div>')
    first = 0
    for t in ts:
        body.append(render_task(code, t))
        first += 1

    body.append('<h2 id="sources">4. スクリーンショットと設定値について</h2>')
    body.append('<div class="box warn"><b class="t">画面は原教材ドキュメントのものです</b>'
                '本モジュールのスクリーンショットはすべて <code>S4.docx</code> の著者が実システムでキャプチャした中国語インターフェースの画面です'
                '（元のファイル名 <code>imageNNN.png</code> は各図の図注に残しているので、Word の原文と 1 枚ずつ照合できます）。'
                '当サイトはこれらの画面を一切描き直したり、シミュレーションで再現したりしていません。</div>')
    body.append('<div class="box info"><b class="t">設定値はご自身のシステムの値を基準にしてください</b>'
                'ドキュメント内の組織構造とマスタデータの番号（会社コード <code>C999</code>、会社名「頤寧機械有限公司」、'
                'プラント <code>F999</code>、品目 <code>R999-100</code>/<code>T999-100</code>/<code>F999-100</code>、'
                '得意先 <code>K001</code>/<code>K002</code> など）はすべて原作者の教材環境のものです。'
                '手順どおりに作業するときは、<b>操作の順序と設定ポイントはそのまま流用できますが、具体的な番号や名称はご自身のシステムの値に置き換えてください</b>；'
                'ドキュメントと異なるメッセージが出た場合は、まず「<a href="issues.html">トラブルシューティングと注意点</a>」ページで原教材ドキュメントに記録された同種の問題を確認してください。</div>')

    navlink = []
    if prev:
        navlink.append(f'<a href="{prev["file"]}">← 前のモジュール：{esc(prev["nav"])} {esc(prev["title"])}</a>')
    if nxt:
        navlink.append(f'<a href="{nxt["file"]}">次のモジュール：{esc(nxt["nav"])} {esc(nxt["title"])} →</a>')
    navlink.append('<a href="tasks.html">全 222 タスクの索引 →</a>')
    body.append('<div class="panel" style="margin-top:22px">' + '<br>'.join(navlink) + '</div>')

    return page(m['file'], f'{m["title"]} · 手順と実機画面',
                '\n'.join(body),
                desc=f'{m["title"]}：{st["tasks"]} 件のタスクの手順、IMG パス、T-code と {st["shots"]} 枚の実機画面スクリーンショット。'
                     f'内容は教材ドキュメント S4.docx をもとに整理しています。',
                active=m['file'])


if __name__ == '__main__':
    print(build('fi')[:2000])
