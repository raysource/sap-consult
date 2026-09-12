#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate S4CN_手順書.xlsx — the workbook companion of the S/4HANA 中文实训站.

Sheets: 0_説明 / 1_模块总览 / 2_手順一覧 / 3_画面索引 / 4_T-code速查 /
        5_IMG路径一覧 / 6_踩坑与报错 / 7_学習WBS / 8_進捗サマリ

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

MODEL = json.load(open('work/site_model.json'))
IMAGES = json.load(open('work/images.json'))
SUMMARY = json.load(open('work/images_summary.json'))

import sys
sys.path.insert(0, os.path.join(ROOT, 'tools/sitegen'))
from common import MODULES, mod_of            # noqa: E402
from pg_static import ISSUES, PRECHECK        # noqa: E402
import pg_static                              # noqa: E402

ORANGE = '0A6ED1'
GREY = 'F0F3F6'
FONT = '微软雅黑'
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
title_row(ws, 'SAP S/4HANA 中文实训站 — 配套手順書（依据教材文档 S4.docx）', 6)
r = paras(ws, 3, [
    '本工作簿由工具自动生成（tools/make_cn_xlsx.py），数据与网站 HTML 同源，不会出现网站与 Excel 不一致。',
    '',
    '【来源】教材文档 S4.docx：425 页，6 大模块，222 个任务，内嵌 %d 张图片。' % SUMMARY['media_files_in_docx'],
    '【网站收录】%d 处画面引用（去重后 %d 个图片文件，%.1f MB）；排除 %d 张图标/装饰图（尺寸 90×14 以下）。'
    % (SUMMARY['refs_kept'], SUMMARY['unique_files'], SUMMARY['asset_bytes'] / 1e6, SUMMARY['dropped_icons']),
    '【网站页数】13 页：首页 / 准备 / FI / CO / MM / PP / SD / T-code速查 / 排错 / 任务索引 / 讲师版 / 学员版 / 自测',
    '',
    '【重要说明 1｜画面】全部画面是原教材文档中作者在真实系统里截取的中文界面截图，不是示意图、未重绘。',
    '   每行画面索引都给出原文档文件名（imageNNN.png）与站内路径，可与 Word 原文逐张对照。',
    '【重要说明 2｜取值】文档中的示例值（公司代码 C999 / 工厂 F999 / 物料 R999-100 / 客户 K001 等）属于原作者的教材环境。',
    '   操作顺序与配置点可以照搬，编号与名称请换成自己系统里的值；报错消息也可能因版本/语言/客户化而不同。',
    '【重要说明 3｜不臆造】标准值、字段清单、表名、SAP Note 编号若原文档未给出，本工作簿与网站都不补。',
    '',
    '【表页说明】',
    '   1_模块总览    ：6 个模块的任务/步骤/画面数与主要 T-code',
    '   2_手順一覧    ：222 个任务 × IMG 路径 / T-code / 画面数 / 网站链接（按模块与任务序号排序）',
    '   3_画面索引    ：每一处画面的明细（画面序号、所在任务、手順步、原文件名、尺寸、站内路径）',
    '   4_T-code速查  ：文档中出现的全部事务代码及其所在任务',
    '   5_IMG路径一覧 ：原文档给出的 203 条后台菜单路径',
    '   6_踩坑与报错  ：原文档记录的报错现象与处理办法 + 出问题前的 6 项前提检查',
    '   7_学習WBS      ：受讲者用进度表（自己判定 ○/△/×），完成基準取自手顺与画面',
    '   8_進捗サマリ  ：按模块统计完成率（公式自动计算，改动 7_学習WBS 的判定后自动更新）',
], 6)
ws.column_dimensions['A'].width = 150

# ------------------------------------------------------------------ 1_模块总览
ws = wb.create_sheet('1_模块总览')
head(ws, [('模块', 26), ('页文件', 14), ('任务数', 8), ('手顺步', 9), ('画面数', 9),
          ('后台/前台', 11), ('主要 T-code', 60), ('网站页面', 46)])
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
row(ws, r, ['合计', '13 页', sum(len(m['tasks']) for m in MODEL),
            sum(len(t['steps']) for m in MODEL for t in m['tasks']),
            sum(t['nimg'] for m in MODEL for t in m['tasks']), '',
            'T-code 速查见 4_T-code速查', 'index.html'], zebra=False)

# ------------------------------------------------------------------ 2_手順一覧
ws = wb.create_sheet('2_手順一覧')
head(ws, [('模块', 20), ('序号', 6), ('任务', 40), ('前后台', 8), ('T-code', 24),
          ('IMG 路径（后台菜单）', 70), ('画面', 6), ('手顺步', 7), ('网站链接', 26)],
     row=1)
ws.freeze_panes = 'A2'
ws.auto_filter.ref = 'A1:I223'
r = 2
for m in MODULES:
    for t in [x for x in MODEL if x['code'] == m['code']][0]['tasks']:
        link = '%s#%s' % (m['file'], t['anchor'])
        row(ws, r, [m['nav'], '任务 %02d' % t['no'], t['title'], t['fb'] or '',
                    ' '.join(t['tcodes']), t['path'] or '', t['nimg'], len(t['steps']), link],
            zebra=(r % 2 == 0))
        r += 1

# ------------------------------------------------------------------ 3_画面索引
ws = wb.create_sheet('3_画面索引')
head(ws, [('画面#', 7), ('模块', 16), ('序号', 6), ('任务', 38), ('手順步', 7),
          ('原文档文件名', 18), ('宽', 6), ('高', 6), ('KB', 8), ('站内路径', 40)])
ws.freeze_panes = 'A2'
ws.auto_filter.ref = 'A1:J%d' % (len(IMAGES) + 1)
r = 2
for rec in sorted(IMAGES, key=lambda x: x['seq']):
    row(ws, r, [rec['seq'], mod_of(rec['modcode'])['nav'], '任务 %02d' % rec['taskno'],
                rec['task'], rec['step'], rec['orig'], rec['w'], rec['h'],
                round(rec['bytes'] / 1024, 1), 'assets/img/' + rec['path']],
        zebra=(r % 2 == 0))
    r += 1

# ------------------------------------------------------------------ 4_T-code速查
ws = wb.create_sheet('4_T-code速查')
head(ws, [('T-code', 12), ('出现任务数', 10), ('模块', 22), ('相关任务', 90)])
r = 2
tc = pg_static.collect_tcodes()
for c, rec in sorted(tc.items(), key=lambda kv: (-len(kv[1]['tasks']), kv[0])):
    tasks = '；'.join('%s#%s（%s 任务 %02d %s）' % (mod_of(m['code'])['file'], t['anchor'],
                                                   mod_of(m['code'])['nav'], t['no'], t['title'])
                      for m, t in rec['tasks'][:4])
    if len(rec['tasks']) > 4:
        tasks += '；…等 %d 处' % len(rec['tasks'])
    row(ws, r, [c, len(rec['tasks']), ' / '.join(rec['mods']), tasks], zebra=(r % 2 == 0))
    r += 1

# ------------------------------------------------------------------ 5_IMG路径一覧
ws = wb.create_sheet('5_IMG路径一覧')
head(ws, [('模块', 20), ('序号', 6), ('任务', 42), ('IMG 路径（后台菜单）', 90)])
r = 2
for m in MODULES:
    for t in [x for x in MODEL if x['code'] == m['code']][0]['tasks']:
        if not t['path']:
            continue
        row(ws, r, [m['nav'], '任务 %02d' % t['no'], t['title'], t['path']], zebra=(r % 2 == 0))
        r += 1

# ------------------------------------------------------------------ 6_踩坑与报错
ws = wb.create_sheet('6_踩坑与报错')
head(ws, [('#', 5), ('现象 / 报错', 46), ('原因', 40), ('原文档给出的处理', 60), ('相关手顺', 50)])
r = 2
for i, it in enumerate(ISSUES, 1):
    links = '；'.join('%s#t%02d（%s 任务 %02d %s）' % (mod_of(c)['file'], n, mod_of(c)['nav'], n, lbl)
                      for c, n, lbl in it['links'])
    clean = lambda s: s.replace('<code>', '').replace('</code>', '').replace('<b>', '').replace('</b>', '')
    row(ws, r, [i, clean(it['sym']), clean(it['cause']), clean(it['fix']), links], zebra=(r % 2 == 0))
    r += 1
r += 1
ws.cell(row=r, column=1, value='出问题前先查这 6 件事（按原文档的报错归纳）').font = Font(name=FONT, size=11, bold=True, color=ORANGE)
r += 1
for x in PRECHECK:
    c = ws.cell(row=r, column=1, value='• ' + x.replace('<code>', '').replace('</code>', '').replace('<b>', '').replace('</b>', ''))
    c.font = Font(name=FONT, size=9.5)
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=5)
    r += 1

# ------------------------------------------------------------------ 7_学習WBS
ws = wb.create_sheet('7_学習WBS')
head(ws, [('阶段', 16), ('序号', 6), ('任务', 44), ('完成基準（手顺与画面）', 62),
          ('画面数', 8), ('自己判定', 10), ('我的系统里的取值 / 问题', 34), ('网站链接', 24)])
ws.freeze_panes = 'A2'
r = 2
first_row_of = {}
for m in MODULES:
    first_row_of[m['nav']] = r
    for t in [x for x in MODEL if x['code'] == m['code']][0]['tasks']:
        caps = [s['caption'].replace('\n', ' ') for s in t['steps'] if s['caption']]
        crit = (caps[0][:110] + '…') if caps and len(caps[0]) > 110 else (caps[0] if caps else '')
        if not crit:
            crit = '按原文档画面完成该任务（%d 张画面）' % t['nimg']
        row(ws, r, [m['nav'], '任务 %02d' % t['no'], t['title'], crit, t['nimg'], '', '',
                    '%s#%s' % (m['file'], t['anchor'])], zebra=(r % 2 == 0))
        r += 1
last = r - 1
dv = DataValidation(type='list', formula1='"○,△,×"', allow_blank=True, showDropDown=False)
ws.add_data_validation(dv)
dv.add('F2:F%d' % last)

# ------------------------------------------------------------------ 8_進捗サマリ
ws = wb.create_sheet('8_進捗サマリ')
head(ws, [('模块', 22), ('任务数', 9), ('○ 完成', 9), ('△ 进行中', 9), ('× 未做', 9),
          ('空白', 8), ('完成率', 10), ('画面数', 9), ('预估用时(分)', 13)])
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
ws.cell(row=r, column=1, value='合计').font = Font(name=FONT, size=10, bold=True)
ws.cell(row=r, column=2, value='=SUM(B2:B%d)' % (r - 1)).font = Font(name=FONT, size=10, bold=True)
ws.cell(row=r, column=3, value='=SUM(C2:C%d)' % (r - 1)).font = Font(name=FONT, size=10, bold=True)
ws.cell(row=r, column=7, value='=IF(B%d=0,0,C%d/B%d)' % (r, r, r)).font = Font(name=FONT, size=10, bold=True)
ws.cell(row=r, column=7).number_format = '0%'
ws.cell(row=r + 2, column=1, value='说明：在 7_学習WBS 的「自己判定」列选择 ○ / △ / ×，本页自动统计；'
                                   '预估用时按每个任务 25 分钟估算（含看画面与操作）。').font = Font(name=FONT, size=9.5)
ws.merge_cells(start_row=r + 2, start_column=1, end_row=r + 2, end_column=9)

out = 'S4CN_手順書_学習WBS.xlsx'
wb.save(out)
print('wrote', out, round(os.path.getsize(out) / 1024, 1), 'KB')
print('sheets:', wb.sheetnames)
for s in wb.sheetnames:
    print('  %-16s rows=%d' % (s, wb[s].max_row))
