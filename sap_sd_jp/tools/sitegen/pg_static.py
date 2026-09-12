#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Static pages: index / tasks (index+filter) / tcode / issues."""
import json
import os
import re
from collections import OrderedDict, Counter

from common import (MODULES, MODEL, ROOT, esc, txt, page, breadcrumb, IMAGES,
                    TOTAL_SHOTS, mod_of, tasks_of, FB_IMG, FB_FRONT, fb_label)

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
  <div class="kicker">SAP S/4HANA · 全モジュールの設定と操作 · <b>日本語版</b> · 教材ドキュメント <code>S4.docx</code> に基づく（{st['docx_media']} 枚の埋め込み画像 / 425 ページ）</div>
  <h1>SAP S/4HANA 日本語実習サイト</h1>
  <p class="lead">本サイトは、425 ページの中国語 S/4HANA 教材ドキュメント（<code>S4.docx</code>）を<b>日本語に翻訳・再構成</b>した、オフラインで閲覧できる研修サイトです：
  <b>{st['modules']} 大モジュール · {st['tasks']} タスク · {st['steps']} 手順ステップ · {st['shots']} 枚の実機操作画面</b>。
  各タスクには<b>原教材の IMG 設定メニューパス（日本語訳 + 中国語原文）</b>、<b>教材に出てくる T-code</b>、<b>ステップごとの手順</b>、
  そして<b>原教材の著者が実際のシステムでキャプチャした画面</b>（中国語インターフェース。赤い枠は著者が入力・選択すべき位置を示したものです）を掲載しています。</p>
  <p class="lead"><b>画面は中国語のまま収録しています</b>（原教材の実機画面のため描き直していません）。日本語の手順と画面の中国語表示を結びつけるため、
  各ステップに「原文（中国語）」の折りたたみ、各タスクの入力値表に「画面の中国語」列、
  そして <a href="glossary.html">用語対照表（日本語 ⇔ 中国語画面）</a> を用意しました。</p>
  <p class="lead">対象範囲：<b>準備作業（ログオン / SPRO の IMG 設定）→ 財務会計 FI → 管理会計 CO → 品目管理 MM →
 生産計画 PP → 販売管理 SD</b>。また、原教材ドキュメントの順序に従い、組織構造・マスタデータ・設定パラメータから業務処理・レポートに至るまで一連の流れをそのまま保持しています。</p>
  <div class="toc">
    <a href="#what">1. このサイトは何か</a>
    <a href="#scale">2. 規模と構成</a>
    <a href="#route">3. 学習ルート</a>
    <a href="#cards">4. 6 つのモジュール</a>
    <a href="#howto">5. ページの使い方</a>
    <a href="#tools">6. 関連ページ（講師用／受講者用／自習テスト）</a>
    <a href="#truth">7. 画面と設定値についての説明</a>
    <a href="#sisters">8. 同じディレクトリの姉妹サイト</a>
  </div></div></div>'''


    body.append('<h2 id="what">1. このサイトとは</h2>')
    body.append('''<p>これは「概念の講義資料」ではなく、<b>そのまま真似して作れる操作マニュアル</b>です。原教材ドキュメント <code>S4.docx</code> の形態は
「ひとまとまりの説明文 ＋ 一連の実機スクリーンショット」という形で、著者（原教材ドキュメントの署名は「馬老師学習ノート」）が各設定ポイントと各業務を画面で記録しています。
当サイトはこの形態をそのまま残し、原教材では探しにくい 3 つの情報を追加しました：</p>
<ul>
<li><b>IMG 設定のパスを個別に抽出</b>（原教材ドキュメントでは {paths} 個のタスクでメニューパスが示されています）。クリックでコピーできるので、そのまま SPRO でたどれます。</li>
<li><b>T-code を個別に抽出</b>（{tc} 個のタスクの本文にトランザクションコードが登場します）、<a href="tcode.html">T-code / IMG パス早見表</a>にまとめています。</li>
<li><b>タスク索引 + フィルタ</b>（<a href="tasks.html">{tasks} 個のタスク</a>）。モジュールまたはキーワード（タスク名、T-code）で絞り込めます。</li>
</ul>
<div class="box info"><b class="t">元の素材の形</b>
原教材ドキュメントは「設定マニュアルの形式」で、説明は短めで重点は画面にあります。そのため本サイトの各手順ステップ = <b>原文の説明 + そのステップに対応する画面</b> としています。
原文に文字がなく画面だけが掲載されているステップは、当サイトでは「前の画面のとおりに続けて操作（画面 N）」と表記し、推測で補うことはしません。</div>'''.format(
        paths=st['paths'], tc=st['tcode_tasks'], tasks=st['tasks']))

    body.append('<h2 id="scale">2. 規模と構成</h2>')
    rows = []
    for m in MODULES:
        ts = tasks_of(m['code'])
        shots = sum(t['nimg'] for t in ts)
        steps = sum(len(t['steps']) for t in ts)
        back = sum(1 for t in ts if t['fb'] == FB_IMG)
        front = sum(1 for t in ts if t['fb'] == FB_FRONT)
        rows.append(f'<tr><td><a href="{m["file"]}">{esc(m["title"])}</a></td><td>{len(ts)}</td>'
                    f'<td>{steps}</td><td>{shots}</td><td>{back} / {front}</td></tr>')
    body.append('<div class="tblwrap"><table class="tbl"><thead><tr><th>モジュール</th><th>タスク</th>'
                '<th>手順ステップ</th><th>実機画面</th><th>IMG／業務（原教材ドキュメントの表記）</th></tr></thead><tbody>'
                + ''.join(rows) +
                f'</tbody><tfoot><tr><th>合計</th><th>{st["tasks"]}</th><th>{st["steps"]}</th>'
                f'<th>{st["shots"]}</th><th>—</th></tr></tfoot></table></div>')
    body.append(f'''<div class="grid cards">
  <div class="card"><b>{st['docx_media']}</b><span>原教材ドキュメントに埋め込まれた画像の総数</span></div>
  <div class="card"><b>{st['kept']}</b><span>当サイトに収録した画面の参照</span></div>
  <div class="card"><b>{st['files']}</b><span>重複を除いた画像ファイル</span></div>
  <div class="card"><b>{st['size_mb']} MB</b><span>画像サイズ（オフラインで利用可）</span></div>
</div>''')
    body.append(f'<p>原教材ドキュメントに埋め込まれた {st["docx_media"]} 枚の画像のうち、{st["dropped"]} 枚はアイコン／装飾（サイズ 90×14 以下）で、'
                f'操作画面を構成しないため、当サイトでは除外しています。残りの {st["kept"]} か所の引用はすべて保持しています（同じ図を複数のステップで再利用する場合も、ファイルは 1 つだけ保存）。'
                '各画像の下には<b>原教材ドキュメントのファイル名</b>（例：<code>image1301.png</code>）とピクセルサイズが表示されているので、Word の原文と 1 枚ずつ照合できます。</p>')

    body.append('<h2 id="route">3. 学習ロードマップ</h2>')
    body.append('''<p>原教材ドキュメントの順序そのものが、実行可能な一つのロードマップです —— 「会社の登録」から始めて、財務、原価、品目、生産、販売の
エンタープライズ構造とマスタデータを設定してから業務を実行します。以下の順序どおりに進めることをお勧めします。飛ばさないでください：</p>''')
    route = [
        ('prep', 'まずクライアントに接続し、SPRO の IMG 設定に入れるようにします', '以降の設定はすべて SPRO で操作します。まずこの入口に慣れておきましょう。'),
        ('fi', '財務会計 FI（組織構造 → 勘定 → 伝票 → 売掛・買掛 → レポート）', 'FI の組織構造（会社コード／勘定科目表／会計年度）は CO・MM・SD に共通する前提です。'),
        ('co', '管理会計 CO（管理会計領域 → 原価センタ → 原価要素／作業タイプ → 配賦・按分 → 内部指図）', 'CO は FI の勘定と会社コードに依存するため、FI の後に置くのがいちばん自然です。'),
        ('mm', '品目管理 MM（プラント／購買組織 → 品目マスタ → 自動記帳 → MRP → 購買プロセス）', 'MM は PP と SD のデータソースです：品目マスタ、プラント、保管場所。'),
        ('pp', '生産計画 PP（BOM／作業区／工順 → 原価見積 → MRP → 製造指図 → 決済）', 'PP では MM の品目と購買を使い、CO の原価要素と作業タイプも使います。'),
        ('sd', '販売管理 SD（販売エリア → 価格設定／税 → マスタデータ → 見積→受注→納入→請求）', 'SD は最後に位置します。前の段階で整えた品目、得意先、勘定、更新グループを消費するためです。'),
    ]
    body.append('<div class="grid cards">' + ''.join(
        f'<div class="card"><b>{i + 1}　{esc(mod_of(c)["nav"])}</b><span>{esc(t1)}</span>'
        f'<span class="dim">{esc(t2)}</span><a href="{mod_of(c)["file"]}">{esc(mod_of(c)["nav"])} へ進む →</a></div>'
        for i, (c, t1, t2) in enumerate(route)) + '</div>')

    body.append('<h2 id="cards">4. 6 つのモジュール</h2>')
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
            f'<span class="dim">{len(ts)} タスク · {sum(len(t["steps"]) for t in ts)} ステップ · {shots} 画面</span>'
            f'<span class="tags">' + ' '.join(f'<span class="tag gray">{esc(c)}</span>' for c in tcs[:8]) + '</span>'
            f'<a href="{m["file"]}">モジュールの手順を開く →</a></div>')
    body.append('<div class="grid cards">' + ''.join(cards) + '</div>')

    body.append('<h2 id="howto">5. ページの使用説明</h2>')
    body.append('''<div class="tblwrap"><table class="tbl"><thead><tr><th>ページ上で見えるもの</th><th>意味</th></tr></thead><tbody>
<tr><td><span class="fb">IMG 設定</span> / <span class="fb img">業務処理</span></td><td>原教材ドキュメントが示す設定／操作の性質です：IMG 設定 = IMG カスタマイズ（SPRO）、業務処理 = 日常の業務トランザクション。表示のないタスクは原教材に説明がないため、タスク名から判断してください。</td></tr>
<tr><td><b>IMG パス（IMG 設定のメニュー）</b></td><td>原教材ドキュメントに示されたメニュー階層を、<code>→</code> で統一して区切っています。クリックするとコピーできます。</td></tr>
<tr><td><span class="tc">T-code</span></td><td>そのタスクの本文に登場するトランザクションコード（原教材ドキュメントで著者が直接示したもの）。</td></tr>
<tr><td><b>手順ステップ（番号の丸印）</b></td><td>原教材の順序に沿った抜粋です：1 ステップ = 1 つの説明 + そのステップの画面。意味が不明な「前の画面のとおり続行」= 原教材に画面だけがあり文字がない箇所です。</td></tr>
<tr><td><b>画面 N</b></td><td>この画面が原教材ドキュメントに登場する順番（1 から）。Word の原文と照合するのに使えます。</td></tr>
<tr><td><b>教材ノート / 原理の説明 / つまずき注意</b></td><td>原教材ドキュメントの「馬老師学習ノート」や「解説：…」といった記述を、本サイトでは性質ごとに色分けして表示しています。エラーを含むものは<a href="issues.html">トラブルシューティングと注意点</a>も参照してください。</td></tr>
<tr><td>画面をクリック</td><td>ライトボックスで拡大：1× / 2× / 3×、ESC で閉じます。画像を保存すればそのまま講義資料に使えます。</td></tr>
</tbody></table></div>''')

    body.append('<h2 id="tools">6. 関連ページ（講師用 / 受講者用 / 自習テスト）</h2>')
    body.append('''<div class="grid cards">
<div class="card"><b>タスク索引（222 タスク）</b><span><a href="tasks.html">tasks.html</a> — モジュールまたはキーワード（タスク名 / T-code）で絞り込み、任意のタスクの手順に進めます。</span></div>
<div class="card"><b>T-code と IMG パス早見表</b><span><a href="tcode.html">tcode.html</a> — ドキュメントに登場するすべてのトランザクションコード + 203 件の IMG メニューパス。</span></div>
<div class="card"><b>トラブルシューティングと注意点</b><span><a href="issues.html">issues.html</a> — 原教材ドキュメントに記録されたエラー現象と対処方法（税コード J1/FS217、評価クラスと BSX、OBYC、VL01N の日付、CK11N/CK24 など）。</span></div>
<div class="card"><b>用語対照表（日本語 ⇔ 中国語画面）</b><span><a href="glossary.html">glossary.html</a> — 日本語の手順と中国語画面の表示を結びつける対照表。基本操作・SAP 用語・IMG パスの対照を収録。</span></div>
<div class="card"><b>講師用</b><span><a href="instructor.html">instructor.html</a> — 講義の進め方、時間配分、解説の順序、必ず出題する問答と採点の推奨事項です。</span></div>
<div class="card"><b>受講者用（記入表）</b><span><a href="worksheet.html">worksheet.html</a> — 222 タスクのチェック進捗表 + 自分のシステムでの設定値を記録する欄。そのまま印刷できます。</span></div>
<div class="card"><b>自習テスト（30 題）</b><span><a href="quiz.html">quiz.html</a> — T-code、IMG パス、IMG／業務の判断、トラブルシューティングを網羅する自動採点テストです（合格ラインは 75%）。</span></div>
</div>''')

    body.append('<h2 id="truth">7. 画面と設定値についての説明</h2>')
    body.append('''<div class="box ok"><b class="t">画面は実機スクリーンショットであり、イメージ図ではありません</b>
当サイトの操作画面はすべて、原教材ドキュメント <code>S4.docx</code> で著者が実際の S/4HANA システムでキャプチャした中国語インターフェースの画面です。
当サイトは抽出とレイアウトのみを行い、描き直しも生成もシミュレーションもしていません。元のファイル名（<code>imageNNN.png</code>）は図注に残しており、
Word の原文と 1 枚ずつ照合できます。</div>
<div class="box warn"><b class="t">サンプルの値は原作者の教材環境のもの</b>
会社コード <code>C999</code>、会社名「頤寧機械有限公司」、プラント <code>F999</code>、保管場所 <code>P999</code>、
品目 <code>R999-100</code> / <code>T999-100</code> / <code>F999-100</code>、得意先 <code>K001</code> / <code>K002</code>、
原価センタ「管理部／製造部」、財務諸表バージョン <code>F999</code> などは、いずれも原教材ドキュメントの著者が自分のシステムで作成したサンプルデータです。
<b>操作の順序と設定ポイントはそのまま参考にできますが、番号と名称はご自身のシステムの値に置き換えてください</b>。エラーメッセージもバージョン/言語/カスタマイジングによって異なることがあります。</div>
<div class="box info"><b class="t">当サイトがやらないこと</b>
当サイトは原教材ドキュメントにない内容を推測で補いません。標準値、テーブル名、項目名、SAP Note 番号が原教材ドキュメントに記載されていなければ、ここでも補いません。
正確な項目一覧が必要な場合は、システム上で F1（項目ヘルプ）／ F4（入力候補）と SPRO の「ドキュメント」ボタンで確認してください。</div>
<div class="box info"><b class="t">日本語版としての作り方（原文のたどり方）</b>
本文は日本語に翻訳していますが、<b>画面は中国語インターフェースのまま</b>収録しています（実機画面を描き直さないため）。
そこで、日本語の指示と画面の表示を突き合わせられるように、次の 3 つを用意しました：<br>
① 各手順ステップに <b>「原文（中国語）」</b> の折りたたみ（クリックで開きます）= 原教材ドキュメントのそのままの一文。<br>
② 各タスクの入力値表に <b>「画面の中国語」</b> 列 = その項目が中国語画面でなんと表示されるか。<br>
③ <a href="glossary.html">用語対照表（日本語 ⇔ 中国語画面）</a> = 基本操作・SAP 用語・IMG パスの対照表。<br>
訳語は原教材の表記に合わせています。たとえば中国語の「工厂」は直訳すると「工場」ですが SAP の日本語標準では<b>プラント</b>です。
自分のシステムが日本語インターフェースなら、日本語訳の語をそのまま画面で探してください。</div>''')

    body.append('<h2 id="sisters">8. 同じディレクトリの姉妹サイト</h2>')
    body.append('''<p>本機の <code>~/Desktop/work/training/</code> の下には、<b>各業務形態に特化した日本語の専門実習サイト</b>（MTO / ETO / MTS / VC / 受注形態比較 / SD 受注処理）もあります。
それぞれが 1 つの業務形態に焦点を当て、完全な設定手順と練習を備えています。本サイトは<b>全モジュールを横断する手順サイト（中国語教材の日本語版）</b>で、対象範囲がより広く、画面はすべて原教材の実システムから取得したものです。</p>
<ul>
<li><a href="../index.html">研修サイト一覧（ハブ）</a> — 各専門サイトへの入口と学習ルート。</li>
<li>「1 件の受注がどのように見積から請求まで進むか」だけを練習したい場合は、専門サイトのほうが焦点が絞られています。「どのような設定ポイントがあり、どこで設定するか」の全体像を先に把握したい場合は、本サイトから始めてください。</li>
<li>中国語の原文（<code>S4.docx</code>）と併読する場合は、本サイトの「原文（中国語）」折りたたみと画面番号（<b>画面 N</b>）が照合の手がかりになります。</li>
</ul>''')

    return page('index.html', '概要 · SAP S/4HANA 日本語実習サイト（全モジュールの手順 + 実機画面）', '\n'.join(body),
                desc='SAP S/4HANA 日本語実習サイト：425 ページの教材ドキュメント S4.docx を基に整理した 6 大モジュール 222 タスクの手順、'
                     'IMG パス、T-code、ステップごとの操作と 1385 枚の実機画面スクリーンショットを収録。講師用、受講者用、自習テスト、トラブルシューティングのページも付属します。',
                active='index.html', hero=hero)


# ------------------------------------------------------------------ tasks
def build_tasks():
    body = [breadcrumb([('index.html', 'ホーム'), (None, 'タスク索引')])]
    body.append('<h1>タスク索引（全 %d タスク）</h1>' % len(ALL_TASKS))
    body.append('''<p>キーワードを入力して絞り込めます。タスク名・T-code・モジュール名のいずれでも可能です。「タスク」列をクリックすると、そのタスクの完全な手順へジャンプします
（IMG パスや各ステップの実機画面を含む）。<code>#</code> が付いているものは、そのタスクのモジュールページ内のアンカーです。</p>''')
    chips = ['<span class="chip on" data-mod="all">すべて</span>']
    for m in MODULES:
        chips.append(f'<span class="chip" data-mod="{m["code"]}">{esc(m["nav"])}（{len(tasks_of(m["code"]))}）</span>')
    body.append('<div class="filterbar">'
                '<input type="search" id="taskfilter" placeholder="输入任务名 / T-code / 关键词，例如 MIRO、容差、字段状态…">'
                + ''.join(chips) + '</div>')
    body.append(f'<p class="hitcount" id="hitcount">{len(ALL_TASKS)} / {len(ALL_TASKS)} タスクを表示</p>')
    rows = []
    for m in MODULES:
        for t in tasks_of(m['code']):
            key = ' '.join([m['title'], m['nav'], t['title']] + t['tcodes'] + [t['path'] or ''])
            rows.append(
                f'<tr data-mod="{m["code"]}" data-key="{esc(key)}">'
                f'<td>{esc(m["nav"])}</td>'
                f'<td><a href="{m["file"]}#{t["anchor"]}">タスク {t["no"]:02d}</a></td>'
                f'<td><a href="{m["file"]}#{t["anchor"]}">{esc(t["title"])}</a></td>'
                f'<td>{esc(fb_label(t) or "—")}</td>'
                f'<td>' + (' '.join(f'<code>{esc(c)}</code>' for c in t['tcodes'][:6]) or '—') + '</td>'
                f'<td>{t["nimg"]}</td>'
                f'<td>{len(t["steps"])}</td></tr>')
    body.append('<div class="tblwrap"><table class="tbl idx" id="idxtable"><thead><tr>'
                '<th>モジュール</th><th>No.</th><th>タスク</th><th>IMG/業務</th><th>T-code</th>'
                '<th>画面</th><th>手順ステップ</th></tr></thead><tbody>' + ''.join(rows) + '</tbody></table></div>')
    return page('tasks.html', f'タスク索引 · 全 {len(ALL_TASKS)} 件のタスク · S/4HANA 日本語実習サイト', '\n'.join(body),
                desc=f'S/4HANA 日本語実習サイトのタスク索引：{len(ALL_TASKS)} 件のタスクを絞り込み検索でき、モジュールページ内の手順と実機画面へ直接移動できます。',
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
    body = [breadcrumb([('index.html', 'ホーム'), (None, 'T-code / IMG パス早見表')])]
    body.append('<h1>T-code と IMG 設定パスの早見表</h1>')
    body.append(f'''<p>以下の 2 つの表はどちらも<b>原教材ドキュメントの本文からのみ抽出</b>したもので、書かれていない内容は補いません：
1 枚目はドキュメントに登場したトランザクションコード（計 {len(tc)} 個）、2 枚目はドキュメントに記載された IMG 設定のメニューパス（{stats()['paths']} 件）です。
「原教材ドキュメントでこれを使って行っていること」の列は、その T-code が登場するタスクのタイトルをそのまま引用しているので、モジュールページと 1 件ずつ突き合わせられます。</p>
<div class="box info"><b class="t">使い方</b>
タスクは分かっているけれど入口が分からない → まずモジュールページでそのタスクの「IMG パス」を見てください。ある T-code が本教材で何に使われているかを逆引きしたい → 下の表を使ってください。
パスの行はモジュールページでクリックしてコピーできます。</div>''')
    body.append('<h2 id="tcodes">1. トランザクションコード（T-code）</h2>')
    rows = []
    for c, rec in sorted(tc.items(), key=lambda kv: (-len(kv[1]['tasks']), kv[0])):
        uses = '；'.join(f'<a href="{m["file"]}#{t["anchor"]}">{esc(t["title"])}</a>'
                        for m, t in rec['tasks'][:3])
        if len(rec['tasks']) > 3:
            uses += f' …など {len(rec["tasks"])} か所'
        rows.append(f'<tr id="{esc(c)}"><td>{esc(c)}</td><td>{len(rec["tasks"])}</td>'
                    f'<td>{" / ".join(esc(x) for x in rec["mods"])}</td><td>{uses}</td></tr>')
    body.append('<div class="tblwrap"><table class="tbl"><thead><tr><th>T-code</th><th>出現タスク数</th>'
                '<th>モジュール</th><th>原教材ドキュメントでこれを使って行うこと（タスク名）</th></tr></thead><tbody>'
                + ''.join(rows) + '</tbody></table></div>')

    body.append('<h2 id="imgpaths">2. IMG 設定メニューのパス</h2>')
    body.append('<p>モジュールとタスクの順に並べています。区切り記号は <code>→</code> に統一しました（原文では <code>－</code> と <code>-&gt;</code> が混在）。</p>')
    prows = []
    for m in MODULES:
        for t in tasks_of(m['code']):
            if not t['path']:
                continue
            prows.append(f'<tr><td>{esc(m["nav"])}</td>'
                         f'<td><a href="{m["file"]}#{t["anchor"]}">タスク {t["no"]:02d} {esc(t["title"])}</a></td>'
                         f'<td><code>{esc(t["path"])}</code></td></tr>')
    body.append('<div class="tblwrap"><table class="tbl"><thead><tr><th>モジュール</th><th>タスク</th>'
                '<th>IMG パス（IMG 設定メニュー）</th></tr></thead><tbody>' + ''.join(prows) + '</tbody></table></div>')
    body.append('<div class="box warn"><b class="t">パスの表記はバージョンや言語によって異なります</b>'
                '同じ設定ポイントでも SPRO 上の中国語／英語／日本語のメニュー名は異なることがあり、バージョンによってはノードの位置が変わることもあります。'
                'パスで見つからない場合は、SPRO の検索ボックスでパスのキーワードを検索するか、表 1 の T-code から直接対応するカスタマイジングビューを開いてください。</div>')
    return page('tcode.html', 'T-code と IMG パス早見表 · S/4HANA 日本語実習サイト', '\n'.join(body),
                desc='S/4HANA 日本語実習サイト：教材ドキュメントから抽出したすべての T-code と IMG 設定メニューパスの早見表。',
                active='tcode.html')


# ------------------------------------------------------------------ issues
ISSUES = [
    dict(sym='税コード <code>J1</code> が無効です（メッセージ番号 <code>FS217</code>）。会社コード <code>C999</code> の勘定 <code>12010101</code> では売上税／仕入税に関する操作を実行できません',
         cause='総勘定元帳勘定の「税タイプ」で、対応する売上税／仕入税の処理が許可されていない',
         fix='<code>FS00</code> を実行 → 総勘定元帳勘定 <code>12010101</code> を入力 → 「制御データ」で税分類を設定：'
             '「<code>-</code>」＝仕入税のみ許可、「<code>+</code>」＝売上税のみ許可、「<code>*</code>」＝すべての税分類を許可 → '
             'その後は得意先請求書／支払を正常に入力できます。<b>なお、<code>MIRO</code> を終了してから入り直す必要があります</b>（原教材ドキュメントの原文どおり）',
         links=[('fi', 12, '材料購買勘定を新規登録する'), ('fi', 13, '損益勘定を新規登録する'), ('mm', 39, '購買請求書を入力する')]),
    dict(sym='品目 <code>R999-100</code>「の強制勘定設定（勘定設定カテゴリの入力）」/ エントリ <code>A999 BSX CN01</code> に対して勘定を決定できません',
         cause='品目の会計ビューで「評価クラス」と自動記帳（<code>OBYC</code> / トランザクションコード BSX）の勘定決定が一致しない',
         fix='登録済みの購買発注をすべて削除 → 品目の会計ビュー 1 の「評価クラス」を変更（原教材ドキュメントの例：原材料は <code>3000</code>）→ '
             '<b>当期・前期・前年度の評価クラスもあわせてメンテナンスします</b>。原教材ドキュメントでは、品目の登録（<code>MM01</code>）時に評価クラスを一度で正しく設定することを推奨しています',
         links=[('mm', 21, '評価クラスを定義する'), ('mm', 22, '原材料（ROH）のマスタデータを新規登録する'), ('mm', 28, '品目管理の自動記帳をメンテナンスする')]),
    dict(sym='自動記帳に関するエラー（入庫／請求書のときの勘定決定の失敗）',
         cause='自動記帳ルール（<code>OBYC</code>）で該当するトランザクションキー／評価クラスの勘定がメンテナンスされていない',
         fix='原教材の原文：「T-CODE <code>OBYC</code> で、次のようにメンテナンスするとこの問題を解決できます」（画面も添付）',
         links=[('mm', 28, '品目管理の自動記帳をメンテナンスする'), ('mm', 29, '在庫勘定を自動記帳専用に設定する')]),
    dict(sym='品目 <code>F999-100</code> は保管場所 <code>P999</code> 003 に存在しません',
         cause='品目の「保管場所」ビューにその保管場所がない（またはその保管場所のマスタデータが登録されていない）',
         fix='<code>MMSC</code> でメンテナンスし（原教材の原文：「<code>MMSC</code> 维护」）、<code>MM01</code>/<code>MM02</code> でその品目の該当する保管場所ビューが展開されていることを確認します',
         links=[('mm', 2, '保管場所を登録する'), ('mm', 24, '完成品（FERT）のマスタデータを新規登録する')]),
    dict(sym='<code>VL01N</code> で「選択した日付までの納入に対して期限の来た計画行がありません」とエラーが出る',
         cause='納入伝票の登録時に使用する選択日付が、受注伝票の計画行（所要日付）と同じ期間に入っていない',
         fix='原教材の原文：「解決策は、選択日付を伝票と一致させること」——<code>VL01N</code> の選択日付を伝票と同じに変更します',
         links=[('sd', 42, '出荷伝票（外向納入）を登録する')]),
    dict(sym='<code>VL01N</code> で出荷伝票（外向納入）を登録できない',
         cause='出庫できる在庫がない（教材のシナリオでは在庫が 0）',
         fix='原教材の原文：「<code>MB1C</code> 501 で期首在庫を入力すると、<code>VL01N</code> の出荷伝票（外向納入）を作成できない問題を解決できます」',
         links=[('sd', 42, '出荷伝票（外向納入）を登録する'), ('mm', 38, '購買の入庫を登録する')]),
    dict(sym='内部作業 <code>LAB 1001</code> の価格を決定できません（原価見積が作業価格を取得できない）',
         cause='その作業タイプには、当期の作業出力価格がメンテナンスされていない',
         fix='原教材の原文：「<code>CK11N</code> で、次のように価格をメンテナンスすればよい」→ 価格をメンテナンスした後<b><code>CK11N</code> を終了し、'
             'その後、<code>CK24</code> を再実行します</b>',
         links=[('pp', 12, '作業出力価格を設定する'), ('pp', 22, '製品原価見積を新規登録する'), ('pp', 23, '価格のマーク')]),
    dict(sym='「原価センタに配賦できません。会計年度が有効化されていません」',
         cause='会社コードの会計年度／転記期間が有効化されていない（原価センタに転記できない）',
         fix='原教材ドキュメントはこの見出しで本件の現象を記録し、画面を添付しています（対処方法の記述はありません）。FI 側のやり方に従うと：転記期間バリアントと期間のオープン/クローズ（関連タスクを参照）を確認し、会社コードの会計年度が有効化されていることを確かめてから転記します',
         links=[('fi', 18, '転記期間を設定（業務処理）'), ('co', 1, '管理会計領域を登録する'), ('co', 2, '会社コードを管理会計領域に割り当てる')]),
    dict(sym='「カスタマイジングエラー：現在の業務取引グループではありません」',
         cause='原教材ドキュメントでは、SD モジュールの末尾にこのタイトルでカスタマイジングのエラーが記録されています（画面付き）',
         fix='原教材ドキュメントには対処方法の記述がなく、画面のみが残されています。遭遇したときは、本ページ第 3 節の前提チェックリストと 1 項目ずつ照合して確認し、SPRO では「カスタマイジングエラー：現在の業務トランザクショングループではありません」をキーワードに特定してください',
         links=[('sd', 48, '貸借対照表を実行（原教材ドキュメントの最終章）')]),
    dict(sym='製造指図／内部指図の決済で「エラーはなく、処理が完了しました」と出るのに結果が見えない',
         cause='これはエラーではありません。決済処理自体は成功しており、結果は決済結果やレポートで確認します',
         fix='原教材ドキュメントの順序では、まず決済を実行し（<code>KO88</code>）、その後「内部指図の決済結果の照会」／「製造指図の原価レポートの照会」で確認します',
         links=[('co', 33, '内部指図の決済'), ('co', 34, '内部指図の決済結果を照会する'), ('pp', 48, '製造指図の差異決済')]),
]

PRECHECK = [
    '転記期間がオープンになっているか、会計年度がアクティブになっているか（<code>OB52</code> などの期間のオープン／クローズの設定は FI タスク 16〜18 を参照）。',
    '組織構造が正しく割り当てられているか：会社コード ↔ 管理会計領域、プラント ↔ 会社コード、購買組織 ↔ 会社コード/プラント、販売組織 ↔ 会社コード。',
    '品目マスタの会計ビューで正しい<b>評価クラス</b>（当期/前期/前年度）がメンテナンスされているか、また自動記帳 <code>OBYC</code> の勘定決定が完全かどうか。',
    '完成品の標準価格はすでに見積もられ、<b>マーク/リリース</b>されているか（<code>CK11N</code> → <code>CK24</code>）。そうでないと、製造指図の入庫時に価格を取得できません。',
    '在庫が存在するか（原教材ドキュメントでは複数の場面で <code>MB1C</code> 501 で期首在庫を入力したり、先に購買の入庫を行って在庫を補充したりしています）。',
    'マスタデータがそろっているか：得意先（販売ビュー + パートナ）、品目（販売ビュー + 販売価格/条件レコード）、仕入先（購買データ/購買情報レコード）。',
]


def build_issues():
    body = [breadcrumb([('index.html', 'ホーム'), (None, 'トラブルシューティングと注意点')])]
    body.append('<h1>トラブルシューティングと注意点（原教材ドキュメントに記録された問題と対処）</h1>')
    body.append('''<p>このページでは、原教材ドキュメント <code>S4.docx</code> に記録されたエラー現象と対処方法をまとめています。
「現象」と「対応」の 2 列は、できるだけ原教材の原文を引用しています（引用部分は引用符で示しています）。原教材ドキュメントに画面だけが残り文字が書かれていない場合も、そのまま明記し、
推測による補足はしません。</p>''')
    body.append('<h2 id="table">1. 現象 → 対処の一覧</h2>')
    rows = []
    for i, it in enumerate(ISSUES, 1):
        links = '、'.join(
            f'<a href="{mod_of(c)["file"]}#t{n:02d}">{esc(mod_of(c)["nav"])} タスク {n:02d} {esc(lbl)}</a>'
            for c, n, lbl in it['links'])
        rows.append(f'<tr><td>{i}</td><td>{it["sym"]}</td><td>{it["cause"]}</td><td>{it["fix"]}</td>'
                    f'<td>{links}</td></tr>')
    body.append('<div class="tblwrap"><table class="tbl"><thead><tr><th>#</th><th>現象 / エラー</th>'
                '<th>原因</th><th>原教材ドキュメントが示す対処</th><th>関連する手順</th></tr></thead><tbody>'
                + ''.join(rows) + '</tbody></table></div>')

    body.append('<h2 id="precheck">2. 問題が起きる前に確認する 6 項目（原教材ドキュメントのエラーから整理）</h2>')
    body.append('<ul class="check">' + ''.join(f'<li>{x}</li>' for x in PRECHECK) + '</ul>')

    body.append('<h2 id="notes">3. サイト全体の「つまずき注意」索引</h2>')
    body.append('<p>以下は 222 件のタスクから抽出した、本文にエラー／制限／解決の語を含むノートです（原文をそのまま引用）、'
                'モジュール順に並んでいます。タスク名をクリックすると、その手順の該当箇所に戻れます。</p>')
    warn_rows = []
    for m in MODULES:
        for t in tasks_of(m['code']):
            for n in t['notes']:
                if n['kind'] != 'warn':
                    continue
                warn_rows.append(
                    f'<tr><td>{esc(m["nav"])}</td>'
                    f'<td><a href="{m["file"]}#{t["anchor"]}">タスク {t["no"]:02d} {esc(t["title"])}</a></td>'
                    f'<td>{txt(n["text"])}</td></tr>')
    body.append('<div class="tblwrap"><table class="tbl"><thead><tr><th>モジュール</th><th>タスク</th>'
                '<th>原文ノート</th></tr></thead><tbody>' + ''.join(warn_rows) + '</tbody></table></div>')
    body.append('<div class="box info"><b class="t">該当するエラーが見つかりませんか？</b>'
                '① まず <a href="tasks.html">タスク索引</a> で該当するタスクを探し、その「教材ノート / 原理の説明」を確認します；'
                '② 次に <a href="tcode.html">T-code 早見表</a> で、自分が開いたのが同じカスタマイズビューであることを確認します；'
                '③ 最後にシステム自身の F1（項目ヘルプ）／ F4（入力候補）で項目の意味を確認してください —— 当サイトは原教材ドキュメントにない項目やテーブル名を勝手に補いません。</div>')
    return page('issues.html', 'トラブルシューティングと注意点 · S/4HANA 日本語実習サイト', '\n'.join(body),
                desc='教材ドキュメントに記録されたエラーの現象と対処：税コード J1/FS217、評価クラスと BSX の自動記帳、OBYC、MMSC、VL01N の日付、CK11N/CK24 など。',
                active='issues.html')
