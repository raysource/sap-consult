#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Teaching pages: instructor / worksheet / quiz."""
import os
import random

from common import (MODULES, MODEL, ROOT, esc, txt, page, breadcrumb, mod_of,
                    tasks_of, SEQ, FB_IMG, FB_FRONT, fb_label)

ALL_TASKS = [(m, t) for m in MODEL for t in m['tasks']]


# ------------------------------------------------------------ instructor
QA = [
    ('この教材の設定作業はどこから始めますか？',
     '「準備作業」の <code>SPRO</code> から IMG 設定に入り、その後は FI → CO → MM → PP → SD の順に進めます。'
     'FI のタスク 01〜05（会社コード / 勘定科目表 / 会計年度バリアント / 与信管理領域 / グローバルパラメータ）は全モジュール共通の前提なので、必ず最初に実施してください。'),
    ('FI の最初のタスクが「勘定の登録」ではなく「会社コードの登録」なのはなぜですか？',
     '会社コードは「1 つの完全な会計実体」です（原教材ドキュメントの表現）。以降のすべての勘定、伝票、期間、レポートはこの会社コードに紐づきます。'
     '教材で登録するのは <code>C999</code>「頤寧機械有限公司」です。'),
    ('勘定を登録したのに、伝票である項目が見えない（または項目がグレーになる）のはなぜですか？',
     '「勘定グループ + 項目ステータスバリアント」で決まります：タスク 06 で勘定グループと入力制御を定義し、タスク 07 で項目ステータスバリアントを定義し、タスク 08 でバリアントを会社コードに割り当てます。'
     'そのため、勘定を説明する前に、まずこの 2 つを説明する必要があります。'),
    ('「材料購買勘定」は何のためにあるのですか？なぜ GR/IR とも呼ばれるのですか？',
     '原教材ドキュメントの説明：入庫時は「在庫」を借方・「材料購買」を貸方に記帳し、請求書受領時は「材料購買」を借方・「買掛金」を貸方に記帳し、'
     '勘定は「1 件ずつ消し込む」必要があり、入庫と請求書受領の間をつなぐ中間勘定（GR/IR）です。貸方残高は <code>WRX</code> トランザクションキーに計上されます。'),
    ('MM で最も間違いやすい接点はどこですか？',
     '品目マスタの「評価クラス」と自動記帳 <code>OBYC</code>：評価クラスが勘定決定を左右し、評価クラスを誤って入力するとエラーになります'
     '「明細 A999 BSX CN01 に対して勘定を決定できません」。原教材ドキュメントでの対応は、作成済みの購買発注を削除し、品目の会計ビュー 1 の評価クラスを変更するというものです'
     '（当期／前期／前年度のすべてを変更する必要があります）。品目を登録する時点で正しく設定しておくことをおすすめします。'),
    ('税コードのエラー FS217 はどう対処しますか？',
     '<code>FS00</code> でその総勘定元帳勘定を開き、「制御データ」で税分類を緩めます：<code>-</code> は仕入税のみ許可、'
     '<code>+</code> は売上税のみ許可、<code>*</code> はすべて許可。変更後は <code>MIRO</code> を終了して入り直します。'),
    ('PP の標準原価見積は、どの T-code をどの順で使いますか？',
     '<code>CK11N</code> で見積 → <code>CK24</code> でマーク → <code>CK24</code> でリリース。'
     '作業価格が欠落している場合（例：「内部作業 LAB 1001 の価格を確定できません」）は、まず <code>KP26</code> で作業の出力価格をメンテナンスし、'
     '再び <code>CK11N</code> に戻ります——原教材ドキュメントが特に注意を促しているのは、メンテナンス後に<b>CK11N を終了して CK24 を再実行する</b>という点です。'),
    ('製造指図を指図発行から決済まで実演するとき、正しい順序はどれですか？',
     '指図発行 <code>CO02</code> → 出庫（製造指図への出庫）→ 確認 <code>CO11N</code> → 入庫 <code>MIGO</code> → '
     '原価照会 <code>CO03</code> → 技術的完了 <code>CO02</code> → 差異決済 <code>KO88</code> → 原価レポート。'
     '（PP のタスク 42〜49 に対応）'),
    ('SD の「販売エリア」とは何ですか？なぜ受注伝票の最初に必ず入力するのですか？',
     '販売エリア = 販売組織 + 流通チャネル + 製品部門 で、SD の業務区分です（タスク 01〜07）。'
     '受注伝票の価格決定手順、納入、税の決定、供給可能量はいずれもこれで特定するため、販売エリアを入力しないと何もできません。'),
    ('得意先マスタのパートナはなぜ 4 つあるのですか？',
     '原教材ドキュメントに記載されているのは：<code>SP</code> 受注先、<code>BP</code> 請求先、<code>PY</code> 支払先、<code>SH</code> 納入先。'
     '同じ得意先でも、役割ごとに別の相手を設定できます（例えば受領先 <code>K002</code> を納入先にするなど）。受注伝票ではこれらの役割が自動的に反映されます。'),
    ('1 件の取引が見積から会計伝票に至るまで、どの T-code を実演しますか？',
     '見積 <code>VA21</code> → 受注伝票（見積を参照して登録）→ 納入 <code>VL01N</code> → 請求書 <code>VF01</code> → '
     '転記 <code>VF02</code> → 会計伝票（元伝票をクリック）→ 伝票一覧 <code>VA05</code> / 販売分析 <code>MCTA</code>。'),
    ('受講者のシステムで出るエラーが教材と違うときはどうしますか？',
     'まず「トラブルシューティングと注意点」ページの 6 つの前提チェック（期間のオープン／クローズ、組織構造の割当、評価クラスと OBYC、価格のマークとリリース、在庫、マスタデータ）を行い、'
     '教材に出てくるエラーのほとんどは、この 6 つの分類に当てはまります。それでも解決しない場合は、F1/F4 と SPRO のドキュメントボタンで項目を確認してください —— 他人の標準値をそのまま写さないでください。'),
]


def build_instructor():
    st = {m['code']: dict(tasks=len(m['tasks']), shots=sum(t['nimg'] for t in m['tasks']),
                          steps=sum(len(t['steps']) for t in m['tasks'])) for m in MODEL}
    total_tasks = len(ALL_TASKS)
    total_shots = sum(x['shots'] for x in st.values())

    body = [breadcrumb([('index.html', 'ホーム'), (None, '講師用')])]
    body.append('<h1>講師用 — 授業設計、デモスクリプトと採点の提案</h1>')
    body.append(f'''<p>この教材を使って講習を担当する講師向けのページです。当サイトの素材は教材ドキュメント <code>S4.docx</code> に基づいています：
<b>{total_tasks} タスク／{total_shots} 枚の実機画面</b>。すべての画面は原作者が実際のシステムでキャプチャした中国語インターフェースです。</p>
<div class="box info"><b class="t">当サイトの立場（講義の際は同じ説明をしてください）</b>
① 画面は原教材ドキュメントの実機スクリーンショットであり、模式図ではありません。② ドキュメント内の組織構造とマスタデータの番号（<code>C999</code> / <code>F999</code> /
<code>R999-100</code> / <code>K001</code> …）は原作者の教材環境に属します。<b>操作の順序はそのまま行い、設定値は受講者ご自身のシステムのものに置き換えてください</b>。
③ 当サイトは原教材ドキュメントにない標準値、項目一覧、SAP Note を補足しません。</div>''')

    body.append('<h2 id="plan">1. 授業時間割の提案（5 日 / 30 時間）</h2>')
    body.append('''<p>タスク数も画面数も非常に多く、講義しきれないのは当然です。そこで「<b>設定は主要な流れだけ、業務はすべて実演</b>」をお勧めします：
各モジュールの IMG 設定から重要なタスクを 1〜2 件選んでデモし、業務処理のタスク（伝票の登録、入庫、請求）はすべて一通り実施します。</p>''')
    plan = [
        ('Day 1', '準備作業 + 財務会計 FI（前半）', 'prep + fi タスク 01〜21',
         'ログオンと SPRO；会社コード／勘定科目表／会計年度バリアント／与信管理領域；勘定グループと項目ステータスバリアント（重点的にデモ）；'
         '4 種類の勘定（貸借対照表／調整勘定／材料購買 GR-IR／損益）を登録。伝票番号範囲と転記期間。'),
        ('Day 2', '財務会計 FI（後半）+ 管理会計 CO', 'fi タスク 22〜45 + co タスク 01〜34',
         '得意先／仕入先の勘定グループとマスタデータ；売掛（請求書、全額／一部入金、残高）と買掛（請求書、支払、残高）；'
         ' CO 管理会計領域 → 原価センタ → 原価要素／作業タイプ → 配賦（賃料）と按分（電気料金）→ 内部指図と決済。'),
        ('Day 3', '品目管理（MM）', 'mm タスク 01〜42',
         'プラント／保管場所／購買組織／購買グループ → 品目タイプと評価クラス（重要：OBYC との関係）→ 3 種類の品目マスタ →'
         ' 自動記帳 OBYC → 許容範囲 → MRP 実行 → 購買依頼→購買発注→入庫→請求書照合→ブロック請求書の解除。'),
        ('Day 4', '生産計画（PP）', 'pp タスク 01〜51',
         'BOM／作業区／工順 → 原価計算バリアントと原価構成 → CK11N で見積、CK24 でマーク・リリース →'
         ' 所要量チェックと計画戦略グループ → 独立所要量 MD61 → MRP MD02 → 計画手配から製造指図への変換 →'
         ' 指図発行／出庫／確認／入庫 → 原価表示、技術的完了、差異決済 KO88。'),
        ('Day 5', '販売管理 SD + 総合トラブルシューティングとテスト', 'sd タスク 01〜48 + 自習テスト 30 問',
         '販売エリアと出荷マスタデータ → 価格決定手順と税の決定 → パートナ決定 → 品目／得意先の販売ビュー →'
         ' 見積 VA21 → 受注伝票 → 納入 VL01N → 請求書 VF01/VF02 → 元伝票 → 伝票一覧と販売分析；'
         '最後に「トラブルシューティングと注意点」と、本ページ第 4 節の必ず出る質問を実施します。'),
    ]
    body.append('<div class="tblwrap"><table class="tbl"><thead><tr><th>日程</th><th>内容</th>'
                '<th>対応するタスク</th><th>何を説明／実演するか</th></tr></thead><tbody>' +
                ''.join(f'<tr><td>{esc(a)}</td><td>{esc(b)}</td><td><code>{esc(c)}</code></td><td>{d}</td></tr>'
                        for a, b, c, d in plan) + '</tbody></table></div>')

    body.append('<h2 id="pick">2. 各モジュールで「必ず実演する」タスク</h2>')
    body.append('<p>以下のタスクは各モジュールの骨格です。一度実際にデモするほうが、10 回説明するより分かります。残りのタスクは、受講者が当サイトの手順に沿って自習できます。</p>')
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
            f'<li><a href="{m["file"]}#{t["anchor"]}">タスク {t["no"]:02d} {esc(t["title"])}</a>'
            + (f'　<span class="dim">IMG：<code>{esc(t["path"][:90])}</code></span>' if t['path'] else '')
            + f'　<span class="dim">{t["nimg"]} 画面</span></li>' for t in plist) + '</ul>')

    body.append('<h2 id="qa">3. 必ず出る質問（12 問、標準回答付き）</h2>')
    body.append('<div class="tblwrap"><table class="tbl"><thead><tr><th>#</th><th>受講者が必ず聞くこと</th>'
                '<th>このように答えるとよい</th></tr></thead><tbody>' +
                ''.join(f'<tr><td>{i}</td><td>{q}</td><td>{a}</td></tr>'
                        for i, (q, a) in enumerate(QA, 1)) + '</tbody></table></div>')

    body.append('<h2 id="grading">4. 採点と受入確認の提案</h2>')
    body.append('''<div class="tblwrap"><table class="tbl"><thead><tr><th>項目</th><th>配点</th><th>判定基準</th></tr></thead><tbody>
<tr><td>自習テスト（<a href="quiz.html">quiz.html</a> 30 題）</td><td>30%</td><td>75% 以上で合格（23 題以上）。誤答した問題は該当のタスクに戻って復習してください。</td></tr>
<tr><td>手順の完成度（<a href="worksheet.html">受講者用の記入表</a>）</td><td>40%</td><td>FI 01〜21 + MM 21〜28 + PP 22〜25 + SD 34〜44 の「重要チェーンのタスク」はすべてチェックが必要です。</td></tr>
<tr><td>トラブルシューティング問題（<a href="issues.html">トラブルシューティングページ</a> の 10 現象）</td><td>20%</td><td>「現象 → 原因 → 対処 T-code」の 3 要素を言えること。5 題を抽出し、全問正解で満点です。</td></tr>
<tr><td>口頭で流れを復唱</td><td>10%</td><td>購買チェーン（ME51N→ME21N→MIGO→MIRO→MRBR）と販売チェーン（VA21→受注伝票→VL01N→VF01→VF02）の 2 つの T-code の流れを自力で言えること。</td></tr>
</tbody></table></div>''')
    body.append('<div class="box ok"><b class="t">1 回の授業の最後の 20 分はこう締めくくります</b>'
                '① 受講者に受講者用の記入表で「遭遇した問題」欄を記入してもらう；② トラブルシューティングページの現象表を一緒に確認する；'
                '③ 自習テストページを一通り解き、その場で間違いを確認する。④「自分のシステムに戻って、会社コード／プラント／販売エリアを自分の値に置き換える」という課題を出す。</div>')
    return page('instructor.html', '講師用 · S/4HANA 日本語実習サイト', '\n'.join(body),
                desc='S/4HANA 日本語実習サイトの講師用：5 日間の時間割、各モジュールで必ず実演するタスク、必出の 12 問と採点の提案。',
                active='instructor.html')


# ------------------------------------------------------------ worksheet
def build_worksheet():
    body = [breadcrumb([('index.html', 'ホーム'), (None, '受講者用（記入表）')])]
    body.append('<h1>受講者用 — タスク進捗と設定値の記入表</h1>')
    body.append('''<p>使い方：本ページを印刷します（または画面上に直接記入します）。タスクを 1 つ終えるごとに「✓」欄にチェックを入れ、
ご自分のシステムでの実際の設定値を「自分のシステムの設定値」欄に記入し、エラーが出たら「問題記録」欄に記入してください —— この表を提出すれば、それが学習の軌跡になります。</p>
<div class="box info"><b class="t">印刷のヒント</b>
ブラウザから印刷する場合は A4 横向き・縮小 90% を推奨します。ヘッダーとフッターは当サイトの印刷用スタイルで自動的に非表示になります。
「ドキュメントに記載された T-code / IMG パス」の列は原教材の参考値です。<b>システムにそのまま写さないでください</b>。あくまで「どの設定ポイントを見ればよいか」のヒントです。</div>''')
    body.append('<div class="tblwrap"><table class="tbl"><thead><tr>'
                '<th>モジュール</th><th>全体の達成状況</th><th>備考</th></tr></thead><tbody>' + ''.join(
                    f'<tr><td>{esc(m["nav"])} · {esc(m["title"].split("（")[0])}（{len(tasks_of(m["code"]))} タスク）</td>'
                    '<td>＿＿＿ / ' + str(len(tasks_of(m['code']))) + '</td><td></td></tr>'
                    for m in MODULES) + '</tbody></table></div>')

    for m in MODULES:
        mtasks = tasks_of(m['code'])
        body.append(f'<h2 id="w-{m["code"]}">{esc(m["nav"])} · {esc(m["title"])}'
                    f'　<span class="dim">（{len(mtasks)} 件のタスク / '
                    f'{sum(t["nimg"] for t in mtasks)} 枚の画面）</span></h2>')
        rows = []
        for t in mtasks:
            tc = ' '.join(f'<code>{esc(c)}</code>' for c in t['tcodes'][:4]) or '—'
            path = esc((t['path'] or '')[:70]) + ('…' if t['path'] and len(t['path']) > 70 else '')
            fb = esc(fb_label(t) or '—')
            rows.append(f'<tr><td>{t["no"]:02d}</td>'
                        f'<td><a href="{m["file"]}#{t["anchor"]}">{esc(t["title"])}</a></td>'
                        f'<td>{fb}</td><td>{tc}</td><td><span class="dim">{path or "—"}</span></td>'
                        f'<td class="wblank"></td><td class="wblank"></td><td class="wblank"></td></tr>')
        body.append('<div class="tblwrap"><table class="tbl ws"><thead><tr><th>#</th><th>タスク（クリックで手順を表示）</th>'
                    '<th>IMG/業務</th><th>ドキュメント記載の T-code</th><th>ドキュメント記載の IMG パス</th>'
                    '<th>自分のシステムの設定値</th><th>問題記録</th><th>✓</th></tr></thead><tbody>'
                    + ''.join(rows) + '</tbody></table></div>')

    body.append('<h2 id="finish">修了判定（自分でチェック）</h2>')
    checks = [
        '自分のシステムで <code>SPRO</code> から IMG 設定を開き、FI の「会社コード」設定ポイントを見つけられる。',
        '「勘定グループ + 項目ステータスバリアント」によって、伝票画面でどの項目が表示／必須入力になるかを説明できる。',
        '<code>FS00</code> で総勘定元帳勘定を登録でき、「税分類 <code>-</code>／<code>+</code>／<code>*</code>」の違いを説明できる。',
        '入庫時と請求書受領時に「材料購買（GR/IR）」勘定がそれぞれどんな伝票を自動生成するか説明できる。',
        '品目の「評価クラス」と <code>OBYC</code>（BSX/WRX）の関係を説明でき、評価クラスを誤ったときのリカバリ方法も分かっている。',
        '購買依頼 → 購買発注 → 入庫 → 請求書照合 の 4 ステップを自力で完了できる（4 つの T-code も言える）。',
        '独立所要量 → MRP → 計画手配から製造指図への変換 → 指図発行 → 出庫 → 確認 → 入庫 という PP の主要チェーンを完遂できます。',
        '<code>CK11N</code>/<code>CK24</code> を使って標準原価見積、マーク、リリースを一通り実行できる。',
        '見積 → 受注伝票 → 出荷伝票（外向納入）→ 請求書 → 転記 という SD の主要チェーンを完遂できます（あわせて 5 つの T-code を言える）。',
        'エラーが出たときは、「トラブルシューティングと注意点」ページの 6 つの前提チェックで一つずつ確認できます。',
    ]
    body.append('<ul class="check">' + ''.join(f'<li>{x}</li>' for x in checks) + '</ul>')
    body.append('''<div class="grid cards">
<div class="card"><b>自習テストの成績</b><span>＿＿＿ / 30 問（合格 75% = 23 問）</span></div>
<div class="card"><b>完了したモジュール</b><span>＿＿＿ / 6</span></div>
<div class="card"><b>未解決の問題</b><span>＿＿＿ 件（下表に記入）</span></div>
</div>
<div class="tblwrap"><table class="tbl ws"><thead><tr><th>#</th><th>自分が遭遇した問題（現象 / エラー番号）</th><th>解決方法（T-code）</th><th>講師に確認したい点</th></tr></thead><tbody>'''
                + ''.join('<tr><td>%d</td><td class="wblank"></td><td class="wblank"></td><td class="wblank"></td></tr>' % i
                          for i in range(1, 11)) + '</tbody></table></div>')
    return page('worksheet.html', '受講者用（記入表）· S/4HANA 日本語実習サイト', '\n'.join(body),
                desc='S/4HANA 日本語実習サイト受講者用：222 タスクの進捗チェック表、自分のシステムの設定値の記録欄、修了判定チェックリスト（印刷可能）。',
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
                       q=f'教材ドキュメント《S4.docx》では、「<a href="{mod_of(m["code"])["file"]}#{t["anchor"]}">{esc(t["title"])}</a>」'
                         f'このステップで出てくるのはどの T-code ですか？',
                       opts=[(k, f'<code>{esc(v)}</code>') for k, v in zip(keys, items)],
                       ans=ans,
                       exp=f'原教材ドキュメントでは、このタスクの本文に <code>{esc(correct)}</code> が登場します'
                           f'（このタスクの所属モジュール：{esc(mod_of(m["code"])["nav"])}、実機画面は計 {t["nimg"]} 枚）。'
                           f'残りの 3 項目は他のモジュールのタスクに登場するので、<a href="tcode.html">T-code 早見表</a> から逆引きできます。'))
        seen.add(m['code'])
    return qs


HAND_QUESTIONS = [
    dict(mod='準備', tag='IMG 設定の入口', q='教材で「IMG 設定」に入るための入口は何ですか？',
         opts=[('A', '<code>SPRO</code>（SAP リファレンス IMG）'), ('B', '<code>SE38</code>'),
               ('C', '<code>SM30</code>'), ('D', '<code>SU01</code>')], ans='A',
         exp='原教材ドキュメント：「トランザクションコード欄に <code>spro</code> を入力し、IMG 設定画面へ進みます」。SE38/SU01 は ABAP エディタとユーザメンテナンス、SM30 はテーブルメンテナンスです。'),
    dict(mod='FI', tag='組織構造', q='教材で最初の「会社の登録」はどのタスクで行いますか？',
         opts=[('A', '勘定科目表を登録する'), ('B', '会社コードを登録する'), ('C', '会社コードのグローバルパラメータをメンテナンスする'),
               ('D', '会社コードの項目ステータスバリアントを定義する')], ans='B',
         exp='FI タスク 01「会社コードの登録」、IMG パスは「エンタープライズ構造 → 定義 → 財務会計 → 会社コードの編集/コピー/削除/チェック」、'
             '教材で登録するのは会社コード <code>C999</code>「頤寧機械有限公司」です。'),
    dict(mod='FI', tag='項目制御', q='伝票画面である項目に入力できるかどうかは、次のうちどの 2 つの設定で決まりますか？',
         opts=[('A', '勘定グループ + 項目ステータスバリアント'), ('B', '転記期間 + 伝票タイプ'),
               ('C', '許容範囲グループ + 税コード'), ('D', '評価クラス + 更新グループ')], ans='A',
         exp='FI タスク 06「勘定グループと入力コントロールの定義」とタスク 07「項目ステータスバリアントの定義」は一組です。勘定グループによって、どの項目ステータスバリアントを選ぶかが決まり、'
             'バリアントの各項目は、必須／任意／非表示に設定できます。'),
    dict(mod='FI', tag='勘定マスタ', q='《S4.docx》で「材料購買勘定」はなぜ「1 件ずつ消し込む」必要があるのですか？',
         opts=[('A', '入庫と請求書受領の間をつなぐ過渡勘定です（GR/IR）'),
               ('B', 'これは得意先の調整勘定です'), ('C', 'これは損益区分の勘定であり、年次決算では必ずゼロにする必要があります'),
               ('D', 'これは銀行勘定です')], ans='A',
         exp='原教材ドキュメントの説明：入庫時は在庫を借方・材料購買を貸方に記帳し、請求書受領時は材料購買を借方・買掛金を貸方に記帳するため、両者がこの勘定で相殺され、'
             'そのため 1 件ずつ消し込む必要があります。いわゆる GR/IR の過渡勘定です。'),
    dict(mod='FI', tag='転記期間', q='「クローズ済みの会計期間では伝票を変更できません」——これはどの仕組みですか？',
         opts=[('A', '転記期間バリアントと期間のオープン／クローズ（転記期間の設定）'), ('B', '伝票のアーカイブ'),
               ('C', '許容範囲グループ'), ('D', '勘定グループの入力制御')], ans='A',
         exp='原教材ドキュメント：「これは伝票のオープン／クローズのスイッチです。すでにクローズした転記期間では、伝票を変更できません。複数の会社コードの期間のオープンとクローズをまとめて制御できます。」'
             '対応するタスクは 16〜18（バリアントの定義 → 会社コードへの割当 → 転記期間の設定。最後のステップは業務処理での操作です）。'),
    dict(mod='MM', tag='評価と自動記帳', q='「エントリ <code>A999 BSX CN01</code> に対して勘定を決定できません」とエラーが出ます。原教材ドキュメントが示す対処法は？',
         opts=[('A', '登録済みの購買発注を削除し、品目の会計ビュー 1 の評価クラスを修正する（当期／前期／前年度のすべてを変更）'),
               ('B', '会社コードを再作成する'), ('C', '得意先勘定グループを変更する'), ('D', '為替レートを変更する')], ans='A',
         exp='原教材ドキュメントにはこの対応が明記されており、品目の登録時に評価クラスを一度で正しく設定することを推奨しています。<code>BSX</code> は自動記帳における在庫勘定のトランザクションキーです。'),
    dict(mod='MM', tag='自動記帳', q='自動記帳（勘定決定）はどの T-code でメンテナンスしますか？',
         opts=[('A', '<code>OBYC</code>'), ('B', '<code>FS00</code>'), ('C', '<code>MMSC</code>'), ('D', '<code>MPR1</code>')],
         ans='A',
         exp='原教材ドキュメントの随所で <code>OBYC</code> が示されています（タスク 28「品目管理の自動記帳のメンテナンス」。原文にも「T-CODE OBYC で、次のようにメンテナンスします」とあります）。'
             '<code>FS00</code> は総勘定元帳勘定のメンテナンス、<code>MMSC</code> は保管場所マスタに使用します。'),
    dict(mod='MM', tag='購買チェーン', q='購買から請求書照合までの主な流れで、正しい順序はどれですか？',
         opts=[('A', '購買依頼 <code>ME51N</code> → 購買発注 <code>ME21N</code> → 入庫 <code>MIGO</code> → 請求書照合 <code>MIRO</code> → ブロック請求書の解除 <code>MRBR</code>'),
               ('B', '購買発注 → 購買依頼 → 請求書照合 → 入庫'),
               ('C', '入庫 → 購買依頼 → 購買発注 → 請求書照合'),
               ('D', '請求書照合 → 入庫 → 購買発注 → 購買依頼')], ans='A',
         exp='これは MM タスク 36〜40 の順序であり、当サイトの「タスク索引」で番号順に並べた順序でもあります。ブロック請求書は解除の後でなければ買掛金に計上されません。'),
    dict(mod='MM', tag='MRP', q='教材で資材所要量計画を実行するときは何を使いますか？',
         opts=[('A', '<code>MD03</code> 単一階層計画（MM モジュール）/ <code>MD02</code>（PP モジュール）'),
               ('B', '<code>MB1C</code>'), ('C', '<code>MMBE</code>'), ('D', '<code>COOIS</code>')], ans='A',
         exp='原教材ドキュメントの MM タスク 34 の説明：「BOM は生産計画モジュールでメンテナンスするまでは展開できないため、現時点では BOM 展開ができず、単層計画になります」→ <code>MD03</code>。'
             'PP モジュールでは BOM を登録した後に <code>MD02</code> を使います。在庫/所要量一覧は <code>MD04</code>、在庫概要は <code>MMBE</code>。'),
    dict(mod='PP', tag='標準原価', q='標準原価見積の「見積 → マーク → リリース」はそれぞれ何を使いますか？',
         opts=[('A', '<code>CK11N</code> → <code>CK24</code> → <code>CK24</code>'),
               ('B', '<code>CK24</code> → <code>CK11N</code> → <code>MM03</code>'),
               ('C', '<code>KP26</code> → <code>CK11N</code> → <code>CK40N</code>'),
               ('D', '<code>MM02</code> → <code>CK11N</code> → <code>CK24</code>')], ans='A',
         exp='PP タスク 22（製品原価見積の新規作成 <code>CK11N</code>）→ タスク 23（価格のマーク <code>CK24</code>）→ タスク 25（価格のリリース <code>CK24</code>）；'
             '<code>MM03</code> は照会のみです（タスク 24/26 では将来／リリース済みの計画価格を確認）。'),
    dict(mod='PP', tag='トラブルシューティング', q='原価見積で「内部作業 <code>LAB 1001</code> の価格を決定できません」とエラーが出ます。原教材ドキュメントではどう対処している？',
         opts=[('A', '<code>CK11N</code> で価格をメンテナンスし、<b>CK11N を終了してから <code>CK24</code> を再実行します</b>'),
               ('B', '品目マスタを再作成する'), ('C', '工順を削除してやり直す'), ('D', '会社コードを変更する')], ans='A',
         exp='原教材の原文：「CK11N で、次のように価格をメンテナンスすればよい」「CK11N を終了し、その後 CK24 を再実行する」。'
             '作業価格そのものは <code>KP26</code> でメンテナンスします（タスク 12 で作業の出力価格を設定）。'),
    dict(mod='PP', tag='製造指図', q='製造指図を指図発行した後、決済までの正しい順序はどれですか？',
         opts=[('A', '指図発行 <code>CO02</code> → 出庫 → 確認 <code>CO11N</code> → 入庫 <code>MIGO</code> → 差異決済 <code>KO88</code>'),
               ('B', '確認 → 指図発行 → 決済 → 入庫 → 出庫'),
               ('C', '入庫 → 出庫 → 指図発行 → 確認 → 決済'),
               ('D', '決済 → 入庫 → 確認 → 出庫 → 指図発行')], ans='A',
         exp='PP タスク 42〜48 の順序：<code>CO02</code> で指図発行 → 製造指図への出庫 → <code>CO11N</code> で指図確認 → '
             '<code>MIGO</code> 入庫 → <code>CO03</code> 原価を確認 → <code>CO02</code> 技術的完了 → <code>KO88</code> 差異決済。'),
    dict(mod='CO', tag='配賦と按分', q='教材の「管理部の賃料を各原価センタの占有面積で配賦する」では、どの方式を使っていますか？',
         opts=[('A', '配賦サイクル（統計キー数値の実績値で追跡ファクタを決める）'), ('B', '按分サイクル'),
               ('C', '原価センタの再転記 <code>KB61</code>'), ('D', '作業タイプの価格 <code>KP26</code>')], ans='A',
         exp='CO タスク 20「配賦サイクルの定義」（原教材ドキュメント：受信側の追跡ファクタ = 物件賃料の面積統計キー数値の実際統計値）→ タスク 21「配賦」。'
             '電気料金はタスク 23「按分サイクルの定義」とタスク 24「按分」で処理します。'),
    dict(mod='CO', tag='原価要素', q='一次原価要素と二次原価要素の違いは何ですか？',
         opts=[('A', '一次は財務会計の勘定に対応し、二次は CO 内部（按分・決済など）だけで流れます'),
               ('B', '一次は原価センタにのみ使用でき、二次は内部指図にのみ使用できます'),
               ('C', '一次は収益区分、二次は費用区分です'),
               ('D', '両者に違いはなく、呼び方だけが異なります')], ans='A',
         exp='教材タスク 05「一次原価要素の登録」（<code>KA01</code>）とタスク 06「二次原価要素の登録」（<code>KA06</code>）：'
             '二次原価要素は FI 伝票を生成せず、CO 内部の按分／決済などの再配賦に使います。'),
    dict(mod='CO', tag='内部指図', q='内部指図の費用を集計し終えた後、何で決済しますか？',
         opts=[('A', '<code>KO88</code>'), ('B', '<code>FB50</code>'), ('C', '<code>KK01</code>'), ('D', '<code>KB31N</code>')],
         ans='A',
         exp='CO タスク 33「内部指図の決済」＝<code>KO88</code>（PP の差異決済も同じ）；'
             '<code>KK01</code> で統計キー数値を登録し、<code>KB31N</code> で統計キー数値の数量を入力、<code>FB50</code> で総勘定元帳伝票を入力します。'),
    dict(mod='SD', tag='販売エリア', q='「販売エリア」はどの 3 つの要素で構成されますか？',
         opts=[('A', '販売組織 + 流通チャネル + 製品部門'), ('B', '販売組織 + プラント + 保管場所'),
               ('C', '得意先 + 品目 + 価格決定手順'), ('D', '会社コード + 購買組織 + 販売事務所')], ans='A',
         exp='SD タスク 01〜07 の順序は、まずこの 3 つの要素（販売組織／流通チャネル／製品部門）を登録し、次に「販売エリアの設定」を行うというものです。'
             '受注、価格設定、納入、税の決定は、いずれも販売エリアで特定します。'),
    dict(mod='SD', tag='パートナ', q='原教材ドキュメントの表では、<code>BP</code> はどのパートナ機能に対応しますか？',
         opts=[('A', '請求先'), ('B', '受注先'), ('C', '支払先'), ('D', '納入先')], ans='A',
         exp='原教材ドキュメントのタスク 33 の表には次のように示されています：<code>SP</code> 受注先、<code>BP</code> 請求先、<code>PY</code> 支払先、<code>SH</code> 納入先。'),
    dict(mod='SD', tag='販売チェーン', q='見積から請求書の転記までの、正しい T-code の順序はどれですか？',
         opts=[('A', '見積 <code>VA21</code> → 受注伝票 → 納入 <code>VL01N</code> → 請求書 <code>VF01</code> → 転記 <code>VF02</code>'),
               ('B', '受注伝票 → 見積 → 請求書 → 納入'),
               ('C', '納入 → 見積 → 受注伝票 → 請求書'),
               ('D', '見積 → 納入 → 受注伝票 → 請求書')], ans='A',
         exp='SD タスク 40〜44：<code>VA21</code> で見積を登録 → 見積を参照して受注伝票を登録 → <code>VL01N</code> で出荷伝票（外向納入）を登録 → '
             '<code>VF01</code> で請求書を登録 → <code>VF02</code> で財務会計へ転記。'),
    dict(mod='SD', tag='トラブルシューティング', q='<code>VL01N</code> で「選択した日付までの納入に対して期限の来た計画行がありません」とエラーが出ます。原教材ドキュメントの解決方法は？',
         opts=[('A', '選択日付を伝票と一致するように変更する'), ('B', '<code>VF01</code> に切り替えて納入伝票を登録します'),
               ('C', '受注伝票を削除して再作成する'), ('D', '得意先マスタを変更する')], ans='A',
         exp='原教材の原文：「VL01N 時【選択日付までの納入について期限が到来していない計画行があります】解決策は、選択日付を伝票と一致させること」。'
             '関連する記述がもう 1 件あります。<code>VL01N</code> を作成できない場合は <code>MB1C</code> 501 で期首在庫を入力すると解決できます（在庫が 0）。'),
    dict(mod='総合', tag='環境差異', q='教材の会社コード・プラント・品目番号（<code>C999</code> / <code>F999</code> / <code>R999-100</code>）は何を意味するのでしょうか？',
         opts=[('A', '原教材ドキュメントの著者の教材環境での設定値です。操作の順序はそのまま真似できますが、番号は自分のシステムのものに置き換えてください'),
               ('B', 'SAP の標準初期値で、すべてのシステムで同じです'),
               ('C', '完全にそのまま写さないと、設定は通りません'),
               ('D', 'ランダムに生成された例示で、意味はありません')], ans='A',
         exp='これらの値は原作者のシステムのものです（当サイトでは各画面の元のファイル名を保持しているため、Word 原本と対照できます）。'
             '新しいバージョンや業種別ソリューションでは標準値が異なることがあるため、当サイトではいずれの設定値も「暗記すべき標準解」とは位置づけていません。'),
]


def build_quiz():
    autos = auto_questions(12)
    qs = []
    for q in autos:
        qs.append(q)
    qs.extend(HAND_QUESTIONS[:18])
    body = [breadcrumb([('index.html', 'ホーム'), (None, '自習テスト')])]
    body.append('<h1>自習テスト 30 問（自動採点、75% で合格）</h1>')
    body.append(f'''<p>最初の 12 問は教材ドキュメント <code>S4.docx</code> の「タスク ↔ T-code」の実際の対応から出題しています（問題番号内のタスク名をクリックすると、そのタスクの手順と画面を確認できます）、
後半の 18 問は、組織構造、項目コントロール、自動記帳、配賦／按分、生産と販売のチェーン、そして原教材ドキュメントに記録されたトラブル対応を扱います。
選択肢をクリックするとすぐに採点して解説を表示します。1 問につき解答は 1 回だけで、「すべてやり直す」で最初からやり直せます。</p>
<div class="box info"><b class="t">採点</b>
30 問：75%（23 問）で合格、90%（27 問）以上で優秀です。間違えた問題は該当モジュールの手順ページに戻ってやり直し、「トラブルシューティングと注意点」ページでエラー時の対処を確認してください。</div>''')
    for i, q in enumerate(qs, 1):
        opts = ''.join(f'<div class="opt" data-key="{k}">{v}</div>' for k, v in q['opts'])
        body.append(f'''<div class="quiz-q" data-answer="{q['ans']}">
  <div class="q-meta"><span class="tag gray">{esc(q['mod'])}</span><span class="tag">{esc(q['tag'])}</span></div>
  <h4>{i}. {q['q']}</h4>
  <div class="opts">{opts}</div>
  <div class="explain">{q['exp']}</div>
</div>''')
    body.append('''<h2 id="checklist">実機での受入確認リスト（自習テストの後に 1 項目ずつチェック）</h2>
<ul class="check">
<li>自分のシステムで <code>SPRO</code> から IMG 設定を開き、本教材で扱う任意の設定ポイントを見つけられる。</li>
<li><code>FS00</code> で総勘定元帳勘定を登録し、「税分類」の 3 つの記号の意味を説明できる。</li>
<li>購買チェーンと販売チェーンについてそれぞれ 5 つの T-code を挙げ、各ステップで生じる伝票／書類を説明できる。</li>
<li>品目の「評価クラス」と自動記帳 <code>OBYC</code> の関係、および評価クラスを誤ったときのリカバリ手順を説明できる。</li>
<li><code>CK11N</code>/<code>CK24</code> を使って見積もり・マーク・リリースを実行でき、「マーク」と「リリース」の違いを説明できます。</li>
<li>教材に出てくる 10 件のエラー現象について、「現象 → 原因 → 対処 T-code」を説明できる。</li>
</ul>
<div class="box ok"><b class="t">合格判定</b>自習テストの正答率 ≥75% <b>かつ</b> 実機チェックリスト 6 項目すべてにチェック = 本教材の設定と操作を独力で再現できる能力を備えていると判断します。</div>''')
    return page('quiz.html', '自習テスト 30 問 · S/4HANA 日本語実習サイト', '\n'.join(body),
                desc='S/4HANA 日本語実習サイトの自習テスト：30 問の自動採点テストで、T-code、IMG 設定のパス、組織構造、自動記帳、生産と販売の流れ、トラブルシューティングを網羅しています。',
                active='quiz.html')
