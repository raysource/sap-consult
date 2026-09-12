#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S/4HANA 日本語実習サイトの生成ツールで共有する共通レイアウトと描画用ヘルパーです。"""
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SITE = os.path.basename(ROOT)

MODEL = json.load(open(os.path.join(ROOT, 'work/site_model_ja.json')))
MODEL_ZH = json.load(open(os.path.join(ROOT, 'work/site_model.json')))   # 原教材の中国語モデル（原文表示・対照表用）
IMAGES = json.load(open(os.path.join(ROOT, 'work/images.json')))
SEQ = {}
for rec in IMAGES:
    SEQ.setdefault(rec['path'], rec['seq'])
DIM = {rec['path']: (rec['w'], rec['h']) for rec in IMAGES}
ORIG = {rec['path']: rec['orig'] for rec in IMAGES}
TOTAL_SHOTS = len(IMAGES)

# ---------------------------------------------------------------- module meta
MODULES = [
    dict(code='prep', file='prep.html', nav='準備', short='準備',
         title='準備作業 — システムへのログオンと IMG 設定への移動',
         kicker='準備作業 · クライアントログオン · SPRO の IMG 設定入口',
         intro=[
             'サイト全体の最初のステップは、SAP GUI をシステムに接続し、設定用の IMG 設定（SPRO）を開くことです。以降の FI / CO / MM / PP / SD の 5 モジュールの設定はすべて、この IMG 設定の中で「IMG パス」をたどって階層ごとに行います。',
             '教材環境は中国語インターフェースの S/4HANA 一式です（会社コード <code>C999</code>、会社名 <code>頤寧機械有限公司</code>、プラント <code>F999</code>、品目は <code>T999-100</code> / <code>R999-100</code> / <code>F999-100</code> など）。これらは原教材ドキュメントの著者のシステムでの設定値であり、ご自身のシステムの番号範囲や組織構造と同じとは限りません —— 手順の「操作順序」はそのまま実行できますが、具体的な値はご自身のシステムに合わせて入力してください。',
         ],
         focus=['クライアントのアイコンとログオン画面（システム／クライアント／ユーザ／パスワード／言語）',
                'SPRO（IMG 設定）の入口：トランザクションコード <code>SPRO</code> → SAP リファレンス IMG → 各モジュールのメニューツリー',
                '当サイトでは「IMG 設定」と「業務処理」を分けて表記しています：<span class="fb">IMG 設定</span> ＝ IMG カスタマイジング、<span class="fb img">業務処理</span> ＝ 日常の業務トランザクション']),
    dict(code='fi', file='fi.html', nav='FI', short='FI',
         title='財務会計 FI（Financial Accounting）',
         kicker='財務会計 · 組織構造 · 勘定マスタ · 売掛金・買掛金 · 財務諸表',
         intro=[
             'FI のメインラインは「まず組織構造を構築し、次に勘定を登録し、最後に伝票とレポートを実行する」です：組織構造（会社コード / 勘定科目表 / 会計年度バリアント / 与信管理領域）→ グローバルパラメータ → 勘定グループと項目ステータスバリアント → 勘定マスタ（貸借対照表勘定、調整勘定の売掛金・買掛金、材料購買 GR/IR、損益）→ 伝票番号範囲と転記期間 → 転記の許容範囲グループ → 総勘定元帳伝票と残高 → 得意先／仕入先の勘定グループ、番号範囲とマスタデータ → 売掛金・買掛金（得意先請求書 / 入金 / 仕入先請求書 / 支払 / 残高）→ 財務諸表の構造（貸借対照表と損益計算書）とレポート実行。',
             '本サイトでは原教材ドキュメントの順序どおり 45 のタスクを保持し、各タスクに IMG パス、T-code（ドキュメントに登場するもの）と原教材ドキュメントの実機画面を掲載しています。教材のシナリオは「頤寧機械有限公司」がゼロから会社コード <code>C999</code> を構築し、貸借対照表と損益計算書を出力できるところまで進めるというものです。',
         ],
         focus=['組織構造の 4 点セット：会社コード / 勘定科目表 / 会計年度バリアント / 与信管理領域',
                '勘定マスタ：<code>FS00</code> で一般貸借対照表勘定、調整勘定（売掛／買掛）、材料購買勘定（GR/IR）、損益勘定を登録',
                '転記期間と伝票番号範囲：期間のオープン／クローズの仕組み（クローズした期間では伝票を変更できない）',
                '売掛金・買掛金のクローズドループ：得意先請求書 <code>FB70</code>、入金、仕入先請求書 <code>FB60</code>、支払、残高照会（<code>FD10N</code> / <code>FK10N</code>）']),
    dict(code='co', file='co.html', nav='CO', short='CO',
         title='管理会計 CO（Controlling）',
         kicker='管理会計 · 原価センタ · 原価要素 · 作業タイプ · 配賦・按分 · 内部指図',
         intro=[
             'CO のメインラインは「管理会計領域 → 原価センタ → 原価要素／作業タイプ → 期末按分 → 内部指図」です：管理会計領域を登録して会社コードを割り当てる → 原価センタグループと原価センタ（<code>OKEON</code>）→ 一次／二次原価要素（<code>KA01</code> / <code>KA06</code>）と原価要素グループ → 作業タイプ（<code>KL01</code>）と作業出力価格（<code>KP26</code>）→ 管理会計伝票の番号範囲 → 原価センタレポート、再転記（<code>KB61</code>）→ 統計キー数値（<code>KK01</code>）と統計キー数値の数量（<code>KB31N</code>）→ 配賦サイクル（賃料）と按分サイクル（電気料金）→ 内部指図：指図タイプと番号範囲、決済パラメータと割当構造、指図の登録（<code>KO04</code>）、費用請求書、決済（<code>KO88</code>）と決済結果。',
             '教材シナリオでは「管理部の賃料を面積に応じて各原価センタへ配賦する」「電気料金を統計キー数値で按分する」「内部指図で費用を集計してから決済する」という 3 つを一連の流れとして解説しており、CO の期末決算を理解するうえで最も分かりやすい道筋です。',
         ],
         focus=['管理会計領域と会社コードの割当（<code>OX19</code>。FI の会社コードとの整合に注意）',
                '原価要素（一次 = FI 勘定に対応、二次 = 按分／決済など CO 内部だけで流れる）',
                '配賦（<code>配賦サイクル</code>、統計キー数値／トレース要因を使用）と按分（<code>按分サイクル</code>）の違い',
                '内部指図：タイプ → 決済プロファイル → 配賦構造 → 登録 → 費用 → 決済 <code>KO88</code>']),
    dict(code='mm', file='mm.html', nav='MM', short='MM',
         title='品目管理 MM（Materials Management）',
         kicker='品目管理 · 組織構造 · 品目マスタ · 自動記帳 · MRP · 購買プロセス',
         intro=[
             'MM のメインラインは「組織構造とプラントパラメータ → 品目マスタ → 自動記帳 → MRP → 購買から請求書照合まで」です：プラント / 保管場所 / 購買組織 / 購買グループ / MRP 管理担当者 → 会社コードと購買組織への割当 → 品目グループ、計画マージンキー → プラントパラメータ（在庫引当、保管場所ビュー、税コードのデフォルト値、初期期間、MRP パラメータ）→ MRP の有効化、計画実行の番号範囲 → 品目タイプ属性、評価管理、評価クラス（勘定決定の前提）→ 品目マスタ（原材料（ROH）/ 商品（HAWA）/ 完成品（FERT）、<code>MM01</code>）→ 仕入先購買データ（<code>MK01</code>）と購買情報レコード（<code>ME11</code>）→ 自動記帳（<code>OBYC</code>）と在庫勘定は自動記帳のみ → 許容範囲（価格差異 / 入庫 / 請求書ブロック）→ MRP 実行（<code>MD03</code>）と在庫所要量一覧（<code>MD04</code>）→ 購買依頼（<code>ME51N</code>）→ 購買発注（<code>ME21N</code>）→ 入庫（<code>MIGO</code>）→ 請求書照合（<code>MIRO</code>）→ ブロック請求書の解除（<code>MRBR</code>）→ 請求書と会計伝票 → 在庫照会（<code>MMBE</code>）。',
             'このうち「評価クラス + 自動記帳（OBYC/BSX/WRX）」は MM と FI の接点であり、原教材ドキュメントで繰り返しトラブルシューティングが行われた箇所でもあります（「トラブルシューティングと注意点」ページを参照）。',
         ],
         focus=['組織構造の 4 点セット：プラント / 保管場所 / 購買組織 / 購買グループ、およびその割当関係',
                '品目マスタの 3 種類のビュー：基本データ、購買、MRP、会計（評価クラスが記帳勘定を決定）',
                '自動記帳 <code>OBYC</code>：BSX（在庫）、WRX（GR/IR）、GBB（費用／差異）などのトランザクションキーの勘定決定',
                '購買の全プロセス：<code>ME51N</code> → <code>ME21N</code> → <code>MIGO</code> → <code>MIRO</code> → <code>MRBR</code>']),
    dict(code='pp', file='pp.html', nav='PP', short='PP',
         title='生産計画 PP（Production Planning）',
         kicker='生産計画 · BOM · 作業区 · 工順 · 原価見積 · 製造指図',
         intro=[
             'PP のメインラインは「マスタデータ → 計画 → 実行 → 原価」です：生産計画パラメータファイル、生産スケジューラ、製造指図パラメータ（スケジューリング / 指図タイプ / 確認）→ 部品表（BOM）（<code>CS01</code>、使用箇所一覧 <code>CS15</code>）→ 作業区（責任者、制御コード、能力 <code>CR11</code>、作業時間タイプの作業区 <code>CR01</code>）→ 工順（<code>CA01</code>）と工程分割（<code>CA02</code>）→ 完成品の生産計画ビュー → 原価計算の基礎（原価構成構造、見積バリアント、日付制御、数量構造制御、原価計算バリアント <code>PC01</code>）→ 製品原価見積（<code>CK11N</code>）→ 価格のマーク / 価格のリリース（<code>CK24</code>）→ 実績原価計算の評価バリアントと仕掛品結果分析バージョン → 所要量チェック（チェックグループ、チェック範囲、チェックルール <code>PP01</code>/<code>PP02</code>）→ 計画戦略グループ（<code>MM02</code>）と独立所要量（<code>MD61</code>）→ MRP 実行（<code>MD02</code>）、MRP 一覧 <code>MD05</code>、在庫所要量一覧 <code>MD04</code> → 計画手配から製造指図へ → 購買依頼から購買発注へ → 入庫と請求書 → 製造指図の指図発行（<code>CO02</code>）/ 出庫 / 指図確認（<code>CO11N</code>）/ 入庫（<code>MIGO</code>）→ 原価照会（<code>CO03</code>）/ 技術的完了 / 差異決済（<code>KO88</code>）/ 原価レポート → 在庫一覧と在庫転送。',
             '教材のシナリオは、「鋳鋼ポンプ 170-230」1 台について、BOM、工順、標準原価見積から製造指図の完了、決済、原価分析までを一通り行うものです。',
         ],
         focus=['3 大マスタデータ：BOM（<code>CS01</code>）、作業区（<code>CR01</code>/<code>CR11</code>）、工順（<code>CA01</code>）',
                '標準原価見積と価格更新：<code>CK11N</code> で見積 → <code>CK24</code> でマーク → リリース',
                '計画戦略グループと独立所要量（<code>MD61</code>）→ MRP（<code>MD02</code>）→ 計画手配から製造指図への変換',
                '製造指図の実行チェーン：指図発行 <code>CO02</code> → 出庫 → 確認 <code>CO11N</code> → 入庫 <code>MIGO</code> → 決済 <code>KO88</code>']),
    dict(code='sd', file='sd.html', nav='SD', short='SD',
         title='販売管理 SD（Sales and Distribution）',
         kicker='販売管理 · 販売エリア · 価格設定 · パートナ · 販売プロセス · 請求',
         intro=[
             'SD のメインラインは「販売組織構造 → 出荷の基本データ → 価格設定と税 → 勘定と更新グループ → マスタデータ → 販売プロセス」です：販売組織 / 流通チャネル / 製品部門とその割当 → 販売エリア、販売事務所、販売グループ → 出荷（出発ポイント、積込ポイント、輸送条件、積載グループ、ピッキング用保管場所）→ 得意先勘定グループの販売データとパートナ決定 → 価格決定手順、得意先と伝票の価格決定手順、価格決定手順の決定 → 部品表（BOM）と排除、販売伝票の品目決定 → 税決定ルール、得意先と品目の税分類、売上税税率（<code>VK11</code>）→ 品目の勘定割当グループと売上高勘定 → ヘッダ／明細レベルの更新グループ → マスタデータ（品目の販売ビュー <code>MM01</code>、販売価格、受注先 <code>VD01</code>、納入先と割当 <code>VD02</code>）→ 販売プロセス（見積 <code>VA21</code> → 受注伝票 → 出荷伝票（外向納入）<code>VL01N</code> → 請求書 <code>VF01</code> / 転記 <code>VF02</code> → 元伝票 → 伝票一覧 <code>VA05</code> → 販売分析 <code>MCTA</code>）。',
             '教材のシナリオは、「遠東造船所」が「頤寧公司」の見積に基づいて受注伝票を登録し、その後、納入、請求、財務会計への転記まで一連の流れをたどるものです。',
         ],
         focus=['販売エリア（販売組織 + 流通チャネル + 製品部門）は SD で最も基本となる「業務区分」です',
                '価格決定手順（条件タイプ、手順の決定）と税決定ルール（得意先税分類 + 品目税分類）',
                'パートナ決定（受注先 / 請求先 / 支払先 / 納入先）と得意先勘定グループの機能割当',
                '販売プロセス：見積 <code>VA21</code> → 受注 → 納入 <code>VL01N</code> → 請求書 <code>VF01</code>/<code>VF02</code> → 会計伝票']),
]

NAV = [('index.html', 'ホーム')] + [(m['file'], m['nav']) for m in MODULES] + [
    ('tcode.html', 'T-code'),
    ('glossary.html', '用語'),
    ('issues.html', 'トラブルシューティング'),
    ('tasks.html', '索引'),
    ('instructor.html', '講師'),
    ('worksheet.html', '受講者'),
    ('quiz.html', '自習テスト'),
]
SITE_TITLE = 'SAP S/4HANA 日本語実習サイト'
SITE_SUB = '全モジュールの設定と操作手順 · 実機画面'


# ---------------------------------------------------------------- helpers
def esc(s):
    return html.escape(s or '', quote=True)


FB_IMG, FB_FRONT = '后台', '前台'   # 原教材ドキュメントの表記（データ側の値）


def fb_label(t):
    """表示用の日本語ラベル（IMG 設定 / 業務処理）。"""
    return t.get('fb_ja') or t.get('fb') or ''


def zh_of(code, no):
    """原教材（中国語）側の同じタスクを返す（構造は日本語モデルと同一）。"""
    for m in MODEL_ZH:
        if m['code'] == code:
            for tz in m['tasks']:
                if tz['no'] == no:
                    return tz
    return {}


def orig(text, label='原文（中国語）'):
    """原教材の中国語テキストを折りたたんで併記する（照合用）。"""
    if not (text or '').strip():
        return ''
    return (f'<details class="orig"><summary>{esc(label)}</summary>'
            f'<div class="zh">{txt(text)}</div></details>')


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
    """手順のキャプション → HTML。解説／説明の導入語にマークを付ける。"""
    c = c.strip()
    if not c:
        return ''
    m = re.match(r'^(解説|説明|注意)([：:])\s*(.*)$', c, re.S)
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


NOTE_LABEL = {'tip': '教材ノート', 'info': '原理の説明', 'warn': 'つまずき注意', 'ref': '参考'}


def note_html(n):
    return (f'<div class="note {n["kind"]}"><b class="t">{NOTE_LABEL.get(n["kind"], "笔记")}</b>'
            f'{txt(n["text"])}</div>')


def render_task(code, t):
    """1 タスク = .steph ヘッダ + 説明 + IMG パス + 入力値 + 手順（ol.oplist） + ノート。"""
    mod = mod_of(code)
    tno = t['no']
    tz = zh_of(code, tno)
    tags = []
    if t['fb']:
        tags.append(f'<span class="fb{" img" if t["fb"] == FB_FRONT else ""}">{esc(fb_label(t))}</span>')
    for tc in t['tcodes'][:6]:
        tags.append(f'<span class="tc">{esc(tc)}</span>')
    tags.append(f'<span class="tc2">{t["nimg"]} 画面 / {len(t["steps"])} ステップ</span>')
    out = [f'<div class="steph" id="{t["anchor"]}">'
           f'<span class="no">タスク {tno:02d}</span><h3>{esc(t["title"])}</h3>'
           + ''.join(tags) + '</div>']
    if t['desc']:
        for d in t['desc']:
            out.append(f'<p>{txt(d)}</p>')
    if tz.get('title') and tz['title'] != t['title']:
        out.append(orig('【タスク名】%s\n%s' % (tz['title'], '\n'.join(tz.get('desc') or [])),
                        '原語（中国語）'))
    if t['path']:
        out.append(f'<div class="pathline" data-copy="{esc(t["path"])}">'
                   f'<b>IMG パス（IMG 設定メニュー）</b>{esc(t["path"])}</div>')
        if tz.get('path') and tz['path'] != t['path']:
            out.append('<div class="pathzh"><b>原教材の中国語パス</b>'
                       f'<code>{esc(tz["path"])}</code></div>')
    if t['values']:
        zvals = tz.get('values') or []
        rows = []
        for i, v in enumerate(t['values']):
            zk = zvals[i]['k'] if i < len(zvals) and isinstance(zvals[i], dict) else ''
            rows.append(f'<tr><td>{esc(v["k"])}</td><td><code>{esc(zk)}</code></td>'
                        f'<td>{esc(v["v"])}</td></tr>')
        out.append('<table class="tbl vals"><thead><tr><th>項目（日本語）</th>'
                   '<th>画面の中国語</th><th>教材の設定値</th></tr></thead>'
                   f'<tbody>{"".join(rows)}</tbody></table>')
    for n in t['notes']:
        if n['after'] == 0:
            out.append(note_html(n))
    if t['steps']:
        zsteps = tz.get('steps') or []
        out.append('<ol class="oplist">')
        for i, s in enumerate(t['steps'], 1):
            cls = ' class="is-note"' if s.get('note') else ''
            out.append(f'<li{cls}>')
            zcap = zsteps[i - 1]['caption'] if i <= len(zsteps) else ''
            if s['caption']:
                out.append(f'<p class="opcap">{cap_html(s["caption"])}</p>')
            elif not s.get('note'):
                out.append(f'<p class="opcap"><span class="sub">前の画面に続けて操作します（画面 {SEQ.get(s["imgs"][0], "")}）</span></p>')
            if zcap and zcap != s['caption']:
                out.append(orig(zcap, '原文'))
            out.append(figures(s['imgs'], s['caption'], f'{esc(t["title"])} · ステップ {i}' if t['nimg'] > 1 else esc(t['title'])))
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
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="stylesheet" href="assets/style.css">
<link rel="stylesheet" href="assets/s4jp.css">
</head>
<body>
<header class="site">
  <div class="nav-wrap">
    <a class="brand" href="index.html"><span class="logo">S4</span><span class="txt">日本語実習サイト</span></a>
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
  <p>内容は同ディレクトリの教材ドキュメント <code>S4.docx</code>（425 ページ · 6 大モジュール · 222 タスク · 1385 枚の実機スクリーンショット）に基づいて整理しています。すべてのページはオフラインで開くことができ、外部依存はありません。</p>
  <div><h5>画面について</h5><p>サイト内のすべてのスクリーンショットは<b>原教材ドキュメントの実機画面</b>（中国語インターフェースの SAP GUI）であり、イメージ図やシミュレーションによる生成画像ではありません。ファイル名は原教材ドキュメントの番号をそのまま保持しており、Word の原文と対照できます。ドキュメント内のサンプル値（会社コード <code>C999</code>、プラント <code>F999</code>、品目 <code>R999-100</code> など）は原作者の教材環境のものですので、ご自身のシステムの組織構造と番号範囲に合わせて読み替えてください。</p></div></div>
  <div class="cols">
    <div><h5>モジュール</h5>
{mods_links}    </div>
    <div><h5>サイト全体</h5>
{foot_links}    </div>
  </div>
</div></footer>
<script src="assets/main.js"></script>
<script src="assets/s4jp.js"></script>
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
