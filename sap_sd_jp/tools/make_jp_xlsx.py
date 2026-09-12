#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""S4JP_手順書.xlsx を生成します — S/4HANA 日本語実習サイトの併用ワークブックです。

Sheets: 0_説明 / 1_モジュール概要 / 2_手順一覧 / 3_画面索引 / 4_T-code早見表 /
 5_IMGパス一覧 / 6_つまずきとエラー / 7_学習WBS / 8_進捗サマリ

All rows come from work/site_model.json + work/images.json (the same data the HTML is
built from), so the workbook cannot drift from the site. Run after build_pages.py:
    python3 tools/make_cn_xlsx.py
"""
import json
import os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

MODEL = json.load(open('work/site_model_ja.json'))
IMAGES = json.load(open('work/images.json'))
SUMMARY = json.load(open('work/images_summary.json'))

import sys
sys.path.insert(0, os.path.join(ROOT, 'tools/sitegen'))
from common import MODULES, mod_of            # noqa: E402
from pg_static import ISSUES, PRECHECK        # noqa: E402
import pg_static                              # noqa: E402

ORANGE = '0A6ED1'
GREY = 'F0F3F6'
FONT = 'Microsoft YaHei'
thin = Side(style='thin', color='D9E1E8')
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)


def head(ws, cols, row=1):
    for i, (title, width) in enumerate(cols, 1):
        c = ws.cell(row=row, column=i, value=title)
        c.font = Font(name=FONT, size=10, bold=True, color='FFFFFF')
        c.fill = PatternFill('solid', fgColor=ORANGE)
        c.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        c.border = BORDER
        ws.column_dimensions[get_column_letter(i)].width = width
    ws.row_dimensions[row].height = 30


def row(ws, r, values, zebra=False, wrap_cols=()):
    for i, v in enumerate(values, 1):
        c = ws.cell(row=r, column=i, value=v)
        c.font = Font(name=FONT, size=9.5)
        c.border = BORDER
        c.alignment = Alignment(vertical='top', wrap_text=(i in wrap_cols))
        if zebra:
            c.fill = PatternFill('solid', fgColor=GREY)


def title_row(ws, text, ncol):
    ws.cell(row=1, column=1, value=text).font = Font(name=FONT, size=13, bold=True, color=ORANGE)
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=ncol)
    ws.row_dimensions[1].height = 26


def paras(ws, r, lines, ncol, size=10):
    for line in lines:
        c = ws.cell(row=r, column=1, value=line)
        c.font = Font(name=FONT, size=size)
        c.alignment = Alignment(vertical='top', wrap_text=False)
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=ncol)
        r += 1
    return r


wb = Workbook()

# ------------------------------------------------------------------ 0_説明
ws = wb.active
ws.title = '0_説明'
title_row(ws, 'SAP S/4HANA 日本語実習サイト — 付属の手順書（教材ドキュメント S4.docx に準拠）', 6)
r = paras(ws, 3, [
    '本ワークブックはツールで自動生成しています（tools/make_cn_xlsx.py）。データはウェブサイトの HTML と同じソースから生成しているため、サイトと Excel の内容が食い違うことはありません。',
    '',
    '【出典】教材ドキュメント S4.docx：425 ページ、6 大モジュール、222 タスク、埋め込み画像 %d 枚。' % SUMMARY['media_files_in_docx'],
    '【サイト収録】画面参照 %d 件（重複除去後 %d 個の画像ファイル、%.1f MB）。サイズ 90×14 以下のアイコン/装飾画像 %d 枚は除外しています。'
    % (SUMMARY['refs_kept'], SUMMARY['unique_files'], SUMMARY['asset_bytes'] / 1e6, SUMMARY['dropped_icons']),
    '【サイトのページ数】13 ページ：ホーム / 準備 / FI / CO / MM / PP / SD / T-code 早見表 / トラブルシューティング / タスク索引 / 講師用 / 受講者用 / 自習テスト',
    '',
    '【重要説明 1｜画面】すべての画面は、原教材ドキュメントで著者が実際のシステムからキャプチャした中国語インターフェースのスクリーンショットであり、模式図ではなく、描き直しもしていません。',
    ' 画面索引の各行には、原教材ドキュメントのファイル名（imageNNN.png）とサイト内パスを記載しているので、Word の原文と 1 枚ずつ照合できます。',
    '【重要説明 2｜設定値】ドキュメント内のサンプル値（会社コード C999 / プラント F999 / 品目 R999-100 / 得意先 K001 など）は、原作者の教材環境に属します。',
    ' 操作順序と設定ポイントはそのまま真似して構いませんが、番号と名称はご自分のシステムの値に置き換えてください。エラーメッセージもバージョン／言語／カスタマイズによって異なる場合があります。',
    '【重要説明 3｜推測で補わない】標準値、項目一覧、テーブル名、SAP Note 番号が原教材ドキュメントに記載されていない場合、本ワークブックとサイトでは補いません。',
    '',
    '【表ページの説明】',
    ' 1_モジュール概要 ：6 モジュールのタスク数／ステップ数／画面数と主要 T-code',
    ' 2_手順一覧 ：222 個のタスク × IMG パス / T-code / 画面数 / サイトリンク（モジュールとタスク番号順に並べ替え）',
    ' 3_画面索引 ：各画面の明細（画面番号、所属タスク、手順ステップ、元のファイル名、サイズ、サイト内パス）',
    ' 4_T-code早見表 ：原教材ドキュメントに登場するすべてのトランザクションコードとそのタスク',
    ' 5_IMGパス一覧 ：原教材ドキュメントが示している 203 件の IMG 設定メニューパス',
    ' 6_つまずきとエラー ：原教材ドキュメントに記録されたエラー現象と対処方法 + 問題発生前の 6 項目の前提チェック',
    ' 7_学習WBS ：受講者用の進捗表（自己判定 ○/△/×）、完成基準は手順と画面から取得',
    ' 8_進捗サマリ ：モジュール別に完了率を集計（数式で自動計算。7_学習WBS の判定を変更すると自動更新）',
], 6)
ws.column_dimensions['A'].width = 150

# ------------------------------------------------------------------ 1_モジュール概要
ws = wb.create_sheet('1_モジュール概要')
head(ws, [('モジュール', 26), ('ページファイル', 14), ('タスク数', 8), ('手順ステップ', 9), ('画面数', 9),
          ('IMG 設定／業務処理', 11), ('主要 T-code', 60), ('サイトのページ', 46)])
r = 2
for m in MODULES:
    ts = mod_of(m['code'])['tasks'] if False else [x for x in MODEL if x['code'] == m['code']][0]['tasks']
    tcs = []
    for t in ts:
        for c in t['tcodes']:
            if c not in tcs:
                tcs.append(c)
    row(ws, r, [m['title'], m['file'], len(ts), sum(len(t['steps']) for t in ts),
                sum(t['nimg'] for t in ts),
                '%d / %d' % (sum(1 for t in ts if t['fb'] == '后台'), sum(1 for t in ts if t['fb'] == '前台')),
                '、'.join(tcs[:18]), m['file']], zebra=(r % 2 == 0))
    r += 1
row(ws, r, ['合計', '13 ページ', sum(len(m['tasks']) for m in MODEL),
            sum(len(t['steps']) for m in MODEL for t in m['tasks']),
            sum(t['nimg'] for m in MODEL for t in m['tasks']), '',
            'T-code の早見表は 4_T-code速查 をご覧ください', 'index.html'], zebra=False)

# ------------------------------------------------------------------ 2_手順一覧
ws = wb.create_sheet('2_手順一覧')
head(ws, [('モジュール', 20), ('No.', 6), ('タスク', 40), ('IMG/業務', 8), ('T-code', 24),
          ('IMG パス（IMG 設定メニュー）', 70), ('画面', 6), ('手順ステップ', 7), ('サイトリンク', 26)],
     row=1)
ws.freeze_panes = 'A2'
ws.auto_filter.ref = 'A1:I223'
r = 2
for m in MODULES:
    for t in [x for x in MODEL if x['code'] == m['code']][0]['tasks']:
        link = '%s#%s' % (m['file'], t['anchor'])
        row(ws, r, [m['nav'], 'タスク %02d' % t['no'], t['title'], (t.get('fb_ja') or t['fb'] or ''),
                    ' '.join(t['tcodes']), t['path'] or '', t['nimg'], len(t['steps']), link],
            zebra=(r % 2 == 0))
        r += 1

# ------------------------------------------------------------------ 3_画面索引
ws = wb.create_sheet('3_画面索引')
head(ws, [('画面#', 7), ('モジュール', 16), ('No.', 6), ('タスク', 38), ('手順ステップ', 7),
          ('原教材ドキュメントのファイル名', 18), ('幅', 6), ('高', 6), ('KB', 8), ('サイト内パス', 40)])
ws.freeze_panes = 'A2'
ws.auto_filter.ref = 'A1:J%d' % (len(IMAGES) + 1)
r = 2
for rec in sorted(IMAGES, key=lambda x: x['seq']):
    row(ws, r, [rec['seq'], mod_of(rec['modcode'])['nav'], 'タスク %02d' % rec['taskno'],
                rec['task'], rec['step'], rec['orig'], rec['w'], rec['h'],
                round(rec['bytes'] / 1024, 1), 'assets/img/' + rec['path']],
        zebra=(r % 2 == 0))
    r += 1

# ------------------------------------------------------------------ 4_T-code速查
ws = wb.create_sheet('4_T-code早見表')
head(ws, [('T-code', 12), ('出題タスク数', 10), ('モジュール', 22), ('関連タスク', 90)])
r = 2
tc = pg_static.collect_tcodes()
for c, rec in sorted(tc.items(), key=lambda kv: (-len(kv[1]['tasks']), kv[0])):
    tasks = '；'.join('%s#%s（%s タスク %02d %s）' % (mod_of(m['code'])['file'], t['anchor'],
                                                   mod_of(m['code'])['nav'], t['no'], t['title'])
                      for m, t in rec['tasks'][:4])
    if len(rec['tasks']) > 4:
        tasks += '；…など %d か所' % len(rec['tasks'])
    row(ws, r, [c, len(rec['tasks']), ' / '.join(rec['mods']), tasks], zebra=(r % 2 == 0))
    r += 1

# ------------------------------------------------------------------ 5_IMGパス一覧
ws = wb.create_sheet('5_IMGパス一覧')
head(ws, [('モジュール', 20), ('No.', 6), ('タスク', 42), ('IMG パス（IMG 設定メニュー）', 90)])
r = 2
for m in MODULES:
    for t in [x for x in MODEL if x['code'] == m['code']][0]['tasks']:
        if not t['path']:
            continue
        row(ws, r, [m['nav'], 'タスク %02d' % t['no'], t['title'], t['path']], zebra=(r % 2 == 0))
        r += 1

# ------------------------------------------------------------------ 6_踩坑与报错
ws = wb.create_sheet('6_つまずきとエラー')
head(ws, [('#', 5), ('現象 / エラー', 46), ('原因', 40), ('原教材ドキュメントが示す処理', 60), ('関連手順', 50)])
r = 2
for i, it in enumerate(ISSUES, 1):
    links = '；'.join('%s#t%02d（%s タスク %02d %s）' % (mod_of(c)['file'], n, mod_of(c)['nav'], n, lbl)
                      for c, n, lbl in it['links'])
    clean = lambda s: s.replace('<code>', '').replace('</code>', '').replace('<b>', '').replace('</b>', '')
    row(ws, r, [i, clean(it['sym']), clean(it['cause']), clean(it['fix']), links], zebra=(r % 2 == 0))
    r += 1
r += 1
ws.cell(row=r, column=1, value='問題が起きる前に確認する 6 項目（原教材ドキュメントのエラーから整理）').font = Font(name=FONT, size=11, bold=True, color=ORANGE)
r += 1
for x in PRECHECK:
    c = ws.cell(row=r, column=1, value='• ' + x.replace('<code>', '').replace('</code>', '').replace('<b>', '').replace('</b>', ''))
    c.font = Font(name=FONT, size=9.5)
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=5)
    r += 1

# ------------------------------------------------------------------ 7_学習WBS
ws = wb.create_sheet('7_学習WBS')
head(ws, [('フェーズ', 16), ('No.', 6), ('タスク', 44), ('完成基準（手順と画面）', 62),
          ('画面数', 8), ('自己判定', 10), ('自分のシステムでの設定値 / 問題', 34), ('サイトリンク', 24)])
ws.freeze_panes = 'A2'
r = 2
first_row_of = {}
for m in MODULES:
    first_row_of[m['nav']] = r
    for t in [x for x in MODEL if x['code'] == m['code']][0]['tasks']:
        caps = [s['caption'].replace('\n', ' ') for s in t['steps'] if s['caption']]
        crit = (caps[0][:110] + '…') if caps and len(caps[0]) > 110 else (caps[0] if caps else '')
        if not crit:
            crit = '原教材ドキュメントの画面に沿ってこのタスクを実施します（%d 画面）' % t['nimg']
        row(ws, r, [m['nav'], 'タスク %02d' % t['no'], t['title'], crit, t['nimg'], '', '',
                    '%s#%s' % (m['file'], t['anchor'])], zebra=(r % 2 == 0))
        r += 1
last = r - 1
dv = DataValidation(type='list', formula1='"○,△,×"', allow_blank=True, showDropDown=False)
ws.add_data_validation(dv)
dv.add('F2:F%d' % last)

# ------------------------------------------------------------------ 8_進捗サマリ
ws = wb.create_sheet('8_進捗サマリ')
head(ws, [('モジュール', 22), ('タスク数', 9), ('○ 完了', 9), ('△ 進行中', 9), ('× 未実施', 9),
          ('空白', 8), ('完成率', 10), ('画面数', 9), ('見積所要時間（分）', 13)])
r = 2
for m in MODULES:
    ts = [x for x in MODEL if x['code'] == m['code']][0]['tasks']
    rows_ = [i for i, t in enumerate(ts)]
    a = first_row_of[m['nav']]
    b = a + len(ts) - 1
    ws.cell(row=r, column=1, value=m['title']).font = Font(name=FONT, size=9.5)
    ws.cell(row=r, column=2, value=len(ts)).font = Font(name=FONT, size=9.5)
    ws.cell(row=r, column=3, value='=COUNTIF(\'7_学習WBS\'!F%d:F%d,"○")' % (a, b)).font = Font(name=FONT, size=9.5)
    ws.cell(row=r, column=4, value='=COUNTIF(\'7_学習WBS\'!F%d:F%d,"△")' % (a, b)).font = Font(name=FONT, size=9.5)
    ws.cell(row=r, column=5, value='=COUNTIF(\'7_学習WBS\'!F%d:F%d,"×")' % (a, b)).font = Font(name=FONT, size=9.5)
    ws.cell(row=r, column=6, value='=COUNTIF(\'7_学習WBS\'!F%d:F%d,"")' % (a, b)).font = Font(name=FONT, size=9.5)
    ws.cell(row=r, column=7, value='=IF(B%d=0,0,C%d/B%d)' % (r, r, r)).font = Font(name=FONT, size=9.5)
    ws.cell(row=r, column=7).number_format = '0%'
    ws.cell(row=r, column=8, value=sum(t['nimg'] for t in ts)).font = Font(name=FONT, size=9.5)
    ws.cell(row=r, column=9, value=len(ts) * 25).font = Font(name=FONT, size=9.5)
    for col in range(1, 10):
        ws.cell(row=r, column=col).border = BORDER
        if r % 2 == 0:
            ws.cell(row=r, column=col).fill = PatternFill('solid', fgColor=GREY)
    r += 1
ws.cell(row=r, column=1, value='合計').font = Font(name=FONT, size=10, bold=True)
ws.cell(row=r, column=2, value='=SUM(B2:B%d)' % (r - 1)).font = Font(name=FONT, size=10, bold=True)
ws.cell(row=r, column=3, value='=SUM(C2:C%d)' % (r - 1)).font = Font(name=FONT, size=10, bold=True)
ws.cell(row=r, column=7, value='=IF(B%d=0,0,C%d/B%d)' % (r, r, r)).font = Font(name=FONT, size=10, bold=True)
ws.cell(row=r, column=7).number_format = '0%'
ws.cell(row=r + 2, column=1, value='説明：7_学習WBS の「自己判定」列で ○ / △ / × を選ぶと、本ページが自動集計します；'
                                   '所要時間の目安は 1 タスクあたり 25 分です（画面の確認と操作を含みます）。').font = Font(name=FONT, size=9.5)
ws.merge_cells(start_row=r + 2, start_column=1, end_row=r + 2, end_column=9)

out = 'S4JP_手順書_学習WBS.xlsx'
wb.save(out)
print('wrote', out, round(os.path.getsize(out) / 1024, 1), 'KB')
print('sheets:', wb.sheetnames)
for s in wb.sheetnames:
    print('  %-16s rows=%d' % (s, wb[s].max_row))
