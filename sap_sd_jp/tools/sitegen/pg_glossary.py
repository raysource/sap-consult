#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""用語対照表（日本語 ⇔ 中国語画面）— 日本語サイト独自のページ。

画面は中国語インターフェースなので、日本語の手順に出てくる語と「画面に出ている中国語」を
結びつける表が必要になる。ここでは
  1. 画面の読み替え方（中国語画面の基本操作）
  2. 基本操作の対照表（日本語 → 中国語画面の表示）
  3. 用語対照表（本文で使う日本語 ↔ 中国語画面の語）
  4. IMG パス対照表（日本語訳 ⇔ 原教材の中国語パス）
をまとめる。用語は work/ja/glossary.json を唯一の出所にし、
「画面に出てくる中国語」は原教材 S4.docx のスクリーンショットに合わせている。
"""
import json
import os
import re
from collections import Counter

from common import (MODULES, MODEL, MODEL_ZH, ROOT, esc, txt, page, breadcrumb, tasks_of)

GLOSS = json.load(open(os.path.join(ROOT, 'work/ja/glossary.json'), encoding='utf-8'))['terms']

# 中国語画面で実際に使われている基本操作（原教材のスクリーンショットと本文から採取）
BASIC = [
    ('保存', '保存', 'Ctrl+S / ツールバーの💾。登録後は「伝票が保存されました」のメッセージを確認'),
    ('戻る', '返回', 'F3。前の画面に1段戻る'),
    ('終了', '退出', 'Shift+F3。トランザクションを抜ける'),
    ('取り消し', '取消', 'F12。入力中の画面をキャンセル'),
    ('Enter', '回车', 'Enter。確定して次の項目・次の画面へ'),
    ('実行', '执行', 'F8。レポートや更新処理を開始'),
    ('新規エントリ', '新条目', 'F5。ツールバーの「新条目」= 新しい行・新しいレコード'),
    ('選択（チェック）', '选中 / 勾选', '行頭のチェックボックスを選択（勾选 = チェックを入れる）'),
    ('ダブルクリック', '双击', '行やエントリを開く'),
    ('照会 / 表示', '显示', 'F7 相当。登録済みの内容を照会する'),
    ('変更', '更改', 'F6 相当。登録済みの内容を変更する'),
    ('登録（作成）', '创建', '新規にマスタ・伝票・設定を作る'),
    ('削除', '删除', '登録済みの内容を削除する'),
    ('コピー', '复制', '既存エントリを雛形として複製する'),
    ('項目', '字段', '画面の入力項目。F1 = 項目ヘルプ、F4 = 可能値'),
    ('画面', '屏幕', 'SAP GUI の画面（スクリーン）'),
    ('ボタン', '按钮', '画面下部・上部のボタン'),
    ('伝票ヘッダ', '抬头', '伝票のヘッダ部（共通項目）'),
    ('明細行', '行项目', '伝票・指図の明細行（アイテム）'),
    ('ウィザード', '向导', '対話形式で設定を進める画面。無向导 = ウィザードなし'),
    ('はい / いいえ', '是 / 否', '確認ダイアログの応答'),
]

EXTRA = [
    ('ショップフロアコントロール（SFC）', '商店底价控制', '原教材の「商店底价控制」は Shop Floor Control の<b>機械翻訳の崩れ</b>。日本語 SAP の IMG では「ショップフロアコントロール」（生産の指図実行・確認・所要量チェックの設定群）'),
    ('決済プロファイル', '结算参数文件', '内部指図・製造指図の決済で、配賦構造や決済方法を決めるプロファイル（原文は「结算参数文件」）。ここの「文件」は文書ではなく<b>設定ファイル＝プロファイル</b>の意味'),
    ('製造原価', '生产成本 / 生产原価', '原教材の「生产成本」は日本語会計の標準語では<b>製造原価</b>（勘定名の訳も統一）'),
    ('得意先（受注先/請求先/納入先/支払先）', '客户 / 售达方 / 收票方 / 送达方 / 付款方',
     'SD のパートナ機能。中国語画面では「售达方」などの役割名で表示される'),
    ('会社コード', '公司代码', 'FI の会計単位。教材の例は C999'),
    ('プラント', '工厂', '教材の例は F999。中国語の「工厂」は工場だが SAP ではプラント'),
    ('保管場所', '库存地点', '教材の例は P999 / 0001'),
    ('勘定科目', '科目 / 总帐科目', '総勘定元帳の勘定。中国語画面では「总帐科目」'),
    ('調整勘定', '统驭科目', '得意先・仕入先の元帳を総勘定元帳につなぐ科目'),
    ('転記', '过账', '会計伝票を作成して計上すること'),
    ('伝票', '凭证', '会計伝票・業務伝票'),
    ('受注伝票', '销售订单', 'SD の受注。T-code VA01'),
    ('購買発注', '采购订单', 'MM の発注。T-code ME21N'),
    ('製造指図', '生产订单', 'PP の指図。T-code CO01/CO02'),
    ('内部指図', '内部订单', 'CO の内部指図。T-code KO01/KO04'),
    ('出荷', '装运 / 交货', 'SD の出荷（装运 = 輸送・出荷業務全般）'),
    ('請求書', '发票', 'SD の請求書 / MM の仕入請求書'),
    ('入庫 / 出庫', '收货 / 发货', '在庫移動。T-code MIGO'),
    ('評価クラス', '评估类', '品目の会計ビューの項目。自動記帳の勘定決定に使う'),
    ('自動記帳', '自动记账', 'OBYC。在庫や GR/IR の勘定決定ルール'),
    ('原価センタ', '成本中心', 'CO。教材の例は「行政部」「制造部」'),
    ('管理会計領域', '成本控制范围', 'CO の最上位組織。T-code OX19'),
    ('作業区', '工作中心', 'PP の生産資源。T-code CR01/CR11'),
    ('工順', '工艺路线', 'PP の作業手順。T-code CA01'),
    ('部品表（BOM）', '物料清单', 'PP の構成品表。T-code CS01'),
    ('資材所要量計画（MRP）', '物料需求计划', 'T-code MD02/MD03。確認は MD04'),
    ('所要量チェック', '可用性检查', '受注や指図の所要量確認。設定は OVZ2/OPJJ 系'),
    ('販売エリア', '销售范围', '販売組織＋流通チャネル＋製品部門'),
    ('価格決定手順', '定价过程', 'SD の条件タイプの並び順。T-code V/08'),
    ('与信管理領域', '信贷控制范围', 'FI の与信管理の単位（T-code OVA6 で割当）'),
]


def corpus_count():
    """用語が本文にどのくらい出てくるか（並び順に使う）。"""
    atoms = json.load(open(os.path.join(ROOT, 'work/ja/model_atoms.json'), encoding='utf-8'))
    cnt = Counter()
    for t in atoms.values():
        for w in GLOSS:
            if w in t:
                cnt[w] += 1
    return cnt


def build():
    cnt = corpus_count()
    terms = sorted(GLOSS.items(), key=lambda kv: (-cnt.get(kv[0], 0), kv[0]))

    body = [breadcrumb([('index.html', 'ホーム'), (None, '用語対照表')])]
    body.append('<h1>用語対照表（日本語 ⇔ 中国語画面）</h1>')
    body.append('''<p>本站のスクリーンショットは<b>中国語インターフェースの SAP GUI</b>の実機画面です。
手順本文は日本語で書いていますが、画面に出ているボタン名・項目名は中国語のままなので、
「日本語の指示 → 画面のどこを見るか」を結びつける表をここに置きます。
<b>用語は原教材 <code>S4.docx</code> の表記に合わせています</b>（日本語版 SAP の標準訳と異なる場合があります）。</p>''')

    body.append('<h2 id="basic">1. 中国語画面の基本操作</h2>')
    body.append('<div class="box info"><b class="t">まずはこの 6 つ</b>'
                '<b>登録（作成）→ 保存</b>、<b>输入</b>（入力）→ <b>回车</b>（Enter）、'
                '<b>新条目</b>（F5, 新しい行）、<b>选中</b>（チェックを入れる）、'
                '<b>显示/更改</b>（照会 / 変更）、<b>返回 / 退出</b>（1 段戻る / 抜ける）。'
                '画面下のステータスバーに出る中国語メッセージは、同じ意味の日本語メッセージと読み替えてください。</div>')
    rows = ''.join('<tr><td><b>%s</b></td><td><code>%s</code></td><td>%s</td></tr>'
                   % (esc(a), esc(b), esc(c)) for a, b, c in BASIC)
    body.append('<div class="tblwrap"><table class="tbl"><thead><tr><th>日本語での呼び方</th>'
                '<th>中国語画面の表示</th><th>補足</th></tr></thead><tbody>'
                + rows + '</tbody></table></div>')

    body.append('<h2 id="terms">2. 用語対照表（SAP 用語）</h2>')
    body.append('''<p>下の表は本站の日本語本文で使う語と、中国語画面での表示の対応です。
「出典」列の数字は原教材の本文にその語が何回出てくるか（多い順に並べています）＝ 重要度の目安です。
上の検索欄で絞り込めます（日本語・中国語どちらでも引けます）。</p>''')
    body.append('<div class="filterbar"><input type="search" id="glossfilter" '
                'placeholder="用語で絞り込む（例: 伝票、成本中心、評価クラス、IMG）"></div>')
    body.append('<p class="hitcount" id="glosscount">%d 語を表示</p>' % len(terms))
    rows = []
    for zh, ja in terms:
        rows.append('<tr data-key="%s"><td><b>%s</b></td><td><code>%s</code></td><td>%d</td></tr>'
                    % (esc('%s %s' % (ja, zh)), esc(ja), esc(zh), cnt.get(zh, 0)))
    body.append('<div class="tblwrap"><table class="tbl" id="glosstable"><thead><tr>'
                '<th>日本語（本站の表記）</th><th>中国語画面の語</th><th>出典</th>'
                '</tr></thead><tbody>' + ''.join(rows) + '</tbody></table></div>')

    body.append('<h2 id="extra">3. 混同しやすい語（日本語訳と中国語画面が離れているもの）</h2>')
    rows = ''.join('<tr><td><b>%s</b></td><td><code>%s</code></td><td>%s</td></tr>'
                   % (esc(a), esc(b), esc(c)) for a, b, c in EXTRA)
    body.append('<div class="tblwrap"><table class="tbl"><thead><tr><th>日本語</th>'
                '<th>中国語画面</th><th>なぜ注意が必要か</th></tr></thead><tbody>'
                + rows + '</tbody></table></div>')

    body.append('<h2 id="paths">4. IMG パス対照表（日本語訳 ⇔ 原教材の中国語パス）</h2>')
    body.append('''<p>SPRO のメニューは<b>ログオン言語によって表示名が変わります</b>。原教材は中国語インターフェースで
操作しているため、パスも中国語で書かれています。左が本站の日本語訳、右が原教材の中国語パスです。
自分のシステムが日本語（または英語）インターフェースなら、<b>日本語訳の方をたどってください</b>。</p>''')
    prows = []
    for meta in MODULES:
        m = [x for x in MODEL if x['code'] == meta['code']][0]
        zh = [x for x in MODEL_ZH if x['code'] == meta['code']][0]
        for j, t in enumerate(m['tasks']):
            p_ja = t.get('path')
            p_zh = zh['tasks'][j].get('path') if j < len(zh['tasks']) else None
            if not p_ja:
                continue
            prows.append('<tr><td><a href="%s#%s">%s タスク %02d</a></td>'
                         '<td>%s</td><td><code>%s</code></td></tr>'
                         % (meta['file'], t['anchor'], esc(meta['nav']), t['no'],
                            esc(t['title']), esc(p_zh or '')))
    body.append('<div class="tblwrap"><table class="tbl" id="pathtable"><thead><tr>'
                '<th>タスク</th><th>日本語訳（本站の表記）</th><th>原教材の中国語パス</th>'
                '</tr></thead><tbody>' + ''.join(prows) + '</tbody></table></div>')

    body.append('<div class="box warn"><b class="t">版・言語によってメニュー名は異なります</b>'
                '同じ設定点でも、リリースや言語、アドオンによって SPRO のメニュー名・階層は変わります。'
                'パスで見つからないときは SPRO の検索欄でキーワード検索するか、'
                '<a href="tcode.html">T-code 早見表</a>から直接そのカスタマイズ画面に入ってください。</div>')
    body.append('<p class="dim">本站の用語は原教材の表記に合わせています。たとえば中国語の「工厂」は'
                '直訳すると「工場」ですが、SAP の日本語標準では<b>プラント</b>です。'
                '自分のシステムの表示言語に合わせて読み替えてください。</p>')

    return page('glossary.html', '用語対照表（日本語 ⇔ 中国語画面）',
                '\n'.join(body),
                desc='日本語の手順と中国語インターフェースの画面表示を結びつける用語対照表。'
                     '基本操作・SAP 用語・IMG パスの対照を収録。',
                active='glossary.html')
