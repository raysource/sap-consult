#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成 要件定義書_图书受注管理.xlsx (开发全流程课件的要件阶段成果物)
用法: python3 tools/make_requirements_xlsx.py
依赖: openpyxl (pip install openpyxl)
"""
import os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, "..", "course", "要件定義書_图书受注管理.xlsx"))

BLUE = "0A6ED1"
LIGHT = "E3F0FA"
GREY = "F2F4F7"
INK = "1D2D3E"

F_TITLE = Font(name="微软雅黑", size=16, bold=True, color="FFFFFF")
F_SUB = Font(name="微软雅黑", size=9, color="6B7A8D")
F_HEAD = Font(name="微软雅黑", size=10, bold=True, color="FFFFFF")
F_BODY = Font(name="微软雅黑", size=10, color=INK)
F_SMALL = Font(name="微软雅黑", size=9, color="6B7A8D")
F_SEC = Font(name="微软雅黑", size=11, bold=True, color="0854A0")

FILL_TITLE = PatternFill("solid", fgColor=BLUE)
FILL_HEAD = PatternFill("solid", fgColor=BLUE)
FILL_SEC = PatternFill("solid", fgColor=LIGHT)
FILL_ALT = PatternFill("solid", fgColor=GREY)

THIN = Side(style="thin", color="C9D6E0")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP = Alignment(wrap_text=True, vertical="top")
CENTER = Alignment(wrap_text=True, vertical="center", horizontal="center")


def _table(ws, title, subtitle, headers, rows, widths, start=1):
    """标准表格布局: 标题行 / 副标题 / 表头 / 数据"""
    ncol = len(headers)
    last = get_column_letter(ncol)
    ws.merge_cells(f"A{start}:{last}{start}")
    c = ws.cell(start, 1, title)
    c.font = F_TITLE; c.fill = FILL_TITLE; c.alignment = Alignment(vertical="center")
    ws.row_dimensions[start].height = 26
    if subtitle:
        ws.merge_cells(f"A{start + 1}:{last}{start + 1}")
        c = ws.cell(start + 1, 1, subtitle)
        c.font = F_SMALL
        ws.row_dimensions[start + 1].height = 14
    hr = start + 2
    for j, h in enumerate(headers, 1):
        c = ws.cell(hr, j, h)
        c.font = F_HEAD; c.fill = FILL_HEAD; c.alignment = CENTER; c.border = BORDER
    ws.row_dimensions[hr].height = 20
    r = hr + 1
    for i, row in enumerate(rows):
        for j, v in enumerate(row, 1):
            c = ws.cell(r, j, v)
            c.font = F_BODY; c.alignment = WRAP; c.border = BORDER
            if i % 2 == 1:
                c.fill = FILL_ALT
        ws.row_dimensions[r].height = max(18, 13 * (1 + max((len(str(x)) for x in row), default=0) // 26))
        r += 1
    for j, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(j)].width = w
    ws.freeze_panes = ws.cell(hr + 1, 1)
    return r


def _kv(ws, title, subtitle, pairs, widths, start=1):
    """键值对布局(概要页)"""
    ncol = len(widths)
    last = get_column_letter(ncol)
    ws.merge_cells(f"A{start}:{last}{start}")
    c = ws.cell(start, 1, title); c.font = F_TITLE; c.fill = FILL_TITLE
    ws.row_dimensions[start].height = 26
    if subtitle:
        ws.merge_cells(f"A{start + 1}:{last}{start + 1}")
        ws.cell(start + 1, 1, subtitle).font = F_SMALL
    r = start + 2
    for k, v in pairs:
        ck = ws.cell(r, 1, k); cv = ws.cell(r, 2, v)
        ck.font = F_HEAD; ck.fill = FILL_HEAD; ck.alignment = WRAP; ck.border = BORDER
        cv.font = F_BODY; cv.alignment = WRAP; cv.border = BORDER
        ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=ncol)
        r += 1
    for j, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(j)].width = w
    return r


def _section(ws, row, text, ncol):
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=ncol)
    c = ws.cell(row, 1, text)
    c.font = F_SEC; c.fill = FILL_SEC; c.border = BORDER
    ws.row_dimensions[row].height = 18
    return row + 1


def main():
    wb = Workbook()

    # ============ S0 概要 ============
    ws = wb.active
    ws.title = "0_概要"
    pairs = [
        ("案件名称", "图书受注管理系统 (书商向け受注管理 / Book Order Management)"),
        ("案件ID", "TRN-BOOKORDER-2026"),
        ("目的", "面向 SAP BTP 培训的端到端案例: 以「图书受注」业务为载体, 走完 要件定義 → 設計 → 開発 → テスト → リリース 全流程, 并产出可运行的 CAP 应用与文档体系"),
        ("対象業務", "①受注登録(受注ヘッダ+明細, 主数据連動) ②承認/却下 ③変更(ヘッダ・明細) ④状態管理(OPEN/APPROVED/REJECTED) ⑤一覧照会"),
        ("対象外(v1)", "在庫引当/出荷、請求/売上計上、マスタ保守画面(直接DB/CSV更新)、モバイルUI、多言語(i18n)"),
        ("利用者ロール", "営業(受注登録/変更)・承認者(承認/却下)・管理者(差戻し/全件照会) —— 本実装は mock 認証(alice/alice)で再現"),
        ("技術スタック", "SAP BTP Cloud Foundry + CAP(Node.js) + SQLite(開発)/HANA(本番) + OData V4 + Fiori elements(UI方針)"),
        ("関連資料", "開発全流程课件: dev-course.html | 実装: projects/book-order-app/ (README・docs/test-cases.md) | 他ページ: cap.html / rap.html / fiori.html"),
        ("用語: 受注", "客户(書店/団体)向けの書籍注文。本システムでは注文そのものを指す(売上計上は対象外)"),
        ("用語: 承認(approve)", "営業が登録した受注を承認者が確認し確定すること。承認済み=APPROVED 以降は変更不可(差戻し除く)"),
        ("用語: 却下(reject)", "承認者が理由付きで差し戻すこと(REJECTED)。営業は修正後、再度承認依頼できる"),
        ("用語: 差戻し(sendBack)", "管理者が APPROVED を受注変更のために OPEN へ戻す操作。承認者・日時記録はクリア"),
        ("作成日 / 版", "2026-09-04 / v1.0 (培訓用テンプレート; 正式案件ではレビュー承認履歴を付すこと)"),
    ]
    _kv(ws, "要件定義書 图书受注管理系统", "目的外利用禁止 · 学習用資料(非SAP公式) · 記載内容は要件の雛形であり、実案件では顧客合意が必要",
        pairs, [22, 110])

    # ============ S1 機能要件 ============
    ws = wb.create_sheet("1_機能要件")
    rows = [
        ("F-0100", "受注登録", "営業が受注を登録する(ヘッダ登録→明細追加の2段階)", "営業", "状態=OPENで採番(SO+日付-連番)。明細は OrderItems 経由で追加: 数量>0、単価/書名は書籍マスタから自動取得(単価は上書き可)。合計金額は明細追加時に自動計算", "P1", "order-service.js → before CREATE Orders + OrderItems"),
        ("F-0200", "承認", "承認者が未承認(OPEN)の受注を承認する", "承認者", "OPEN→APPROVED。承認者ID・承認日時を記録。APPROVED以降はヘッダ/明細の変更・削除不可", "P1", "action approve (要認証)"),
        ("F-0300", "変更", "ヘッダ(受注日/得意先/備考)と明細(数量/単価/行追加削除)を変更する", "営業", "変更できるのは OPEN/REJECTED のみ。行変更後は合計金額を自動再計算。APPROVEDは差戻し後に変更", "P1", "before UPDATE Orders/OrderItems + 行後recalc"),
        ("F-0400", "却下・差戻し", "却下: OPEN→REJECTED(理由必須) / 差戻し: APPROVED→OPEN", "承認者/管理者", "却下理由・却下者・日時を記録。差戻し時は承認/却下の監査項目をクリア", "P1", "action rejectOrder / sendBack (要認証)"),
        ("F-0500", "一覧照会", "受注一覧を状態/日付/得意先で絞り込み照会", "全ロール", "OData $filter/$orderby/$top/$expand=items。状態別件数表示(別集計function可)", "P2", "GET /odata/order/Orders"),
        ("F-0600", "マスタ管理", "書籍マスタ/得意先マスタの参照", "全ロール", "v1は参照のみ(メンテナンスはCSV更新で実施)", "P2", "GET Books / Customers (@readonly)"),
        ("F-0700", "監査記録", "承認・却下・差戻しの操作者と日時を保持", "システム", "approvedBy/approvedAt, rejectedBy/rejectedAt/reason を自動記録し、変更APIではクライアントからの改変を拒否", "P1", "schema.cds 監査項目 + before フック"),
    ]
    _table(ws, "機能要件一覧", "区分: F=機能 / 優先度: P1必須 P2重要", 
        ["No", "機能区分", "要件名", "内容", "入力者", "状態・規則", "優先度", "実装位置(本講座コード)"], rows,
        [10, 12, 16, 34, 9, 40, 9, 34])

    # ============ S2 状態遷移・ロール ============
    ws = wb.create_sheet("2_状態遷移")
    r = _table(ws, "状態定義", None,
        ["状態コード", "状態名", "意味", "表示色(UI案)"], 
        [("OPEN", "未承認(登録済)", "登録されたが未承認。変更・削除・行操作が可能", "灰/黄"),
         ("APPROVED", "承認済", "承認確定。ヘッダ/明細の変更・削除不可(差戻しのみ)", "緑"),
         ("REJECTED", "却下", "理由付きで却下。修正して再依頼するか、破棄(削除)する", "赤")],
        [12, 16, 46, 16])
    r = _section(ws, r + 1, "状態遷移表", 4)
    for row in [
        ("現状態", "イベント", "次状態", "権限・条件"),
        ("(新規)", "登録(作成)", "OPEN", "営業。サービス側で採番・既定値設定"),
        ("OPEN", "承認 approve", "APPROVED", "承認者。要認証。承認者ID/日時記録"),
        ("OPEN", "却下 reject", "REJECTED", "承認者。理由(reason)必須"),
        ("OPEN", "変更(PATCH/行操作)/削除", "OPEN", "営業。金額はサーバ再計算"),
        ("APPROVED", "差戻し sendBack", "OPEN", "管理者。監査項目クリア → 以降変更可"),
        ("APPROVED", "変更・削除・却下", "—(禁止)", "400 エラーを返す"),
        ("REJECTED", "変更/行操作/削除", "REJECTED", "営業。修正後に再登録・再承認依頼"),
        ("REJECTED", "承認 approve", "—(禁止)", "400。修正して OPEN に戻す運用は「再登録」で実現"),
    ]:
        ws.append(row)
    for row in ws.iter_rows(min_row=r, max_row=r + 8, max_col=4):
        for c in row:
            c.font = F_BODY; c.border = BORDER; c.alignment = WRAP
            if c.row == r:
                c.font = F_HEAD; c.fill = FILL_HEAD; c.alignment = CENTER
    r = r + 9
    r = _section(ws, r, "ロール定義(本講座実装: mock ユーザ alice/bob)", 4)
    for row in [
        ("ロール", "責務", "機能範囲", "対応ユーザ(実装)"),
        ("営業", "受注登録・変更・削除(OPEN/REJECTED)", "F-0100 F-0300 F-0500", "匿名でも可(本実装方針)。要認証にする場合は alice"),
        ("承認者", "承認・却下", "F-0200 F-0400", "alice(alice) — approve/reject に必要"),
        ("管理者", "差戻し・全件照会", "F-0400(sendBack) F-0500", "alice (ロール分離の本格対応は XSUAA 導入時に実施)"),
    ]:
        ws.append(row)
    for row in ws.iter_rows(min_row=r, max_row=r + 3, max_col=4):
        for c in row:
            c.font = F_BODY; c.border = BORDER; c.alignment = WRAP
            if c.row == r:
                c.font = F_HEAD; c.fill = FILL_HEAD; c.alignment = CENTER
    for j, w in enumerate([12, 16, 46, 16, 16, 16], 1):
        pass
    ws.column_dimensions["A"].width = 12; ws.column_dimensions["B"].width = 24
    ws.column_dimensions["C"].width = 46; ws.column_dimensions["D"].width = 34

    # ============ S3 業務フロー ============
    ws = wb.create_sheet("3_業務フロー")
    rows = [
        (1, "受注情報の入力", "営業", "登録画面(またはAPI)", "得意先・受注日・書籍/数量(単価はマスタから)", "マスタより単価・書名を取得、明細行を組立て", "受注=OPEN / 合計金額計算"),
        (2, "内容確認", "営業", "一覧/詳細画面", "一覧 or 明細確認", "誤りがあれば 3a へ", "—"),
        (3, "承認依頼(默認: 登録=依頼)", "営業", "—", "状態 OPEN のまま", "承認者へ通知(本講座は対象外: Event Mesh で拡張可能)", "—"),
        (4, "承認", "承認者", "詳細画面「承認」", "金額・得意先・納期(備考)を確認", "approve 実行", "OPEN→APPROVED(承認者/日時記録)"),
        (5, "却下", "承認者", "詳細画面「却下」", "理由を入力(必須)", "reject 実行", "OPEN→REJECTED(理由記録)"),
        (6, "却下後の修正", "営業", "変更画面", "指摘事項を修正(ヘッダ/明細)", "PATCH / 行操作、合計再計算", "REJECTED のまま(修正後再依頼)"),
        (7, "承認後の変更", "管理者", "「差戻し」", "変更理由を連絡(備考欄)", "sendBack 実行", "APPROVED→OPEN(監査クリア)"),
        (8, "変更", "営業", "変更画面", "ヘッダ/明細を変更", "PATCH / 行操作、合計再計算", "OPEN のまま"),
        (9, "再承認", "承認者", "詳細画面「承認」", "変更内容を確認", "approve 実行", "OPEN→APPROVED"),
        (10, "受注完了・出荷", "システム(別領域)", "—", "—", "v1 対象外(在庫/出荷システムと連携する場合: 受注完了イベントを Event Mesh へ)", "APPROVED を確定データとして参照"),
    ]
    _table(ws, "業務フロー(受注ライフサイクル)", "受注登録 → 承認/却下 → 変更 → 再承認 の一連の流れ",
        ["No", "ステップ", "操作者", "画面/API", "入力・条件", "処理", "出力・状態遷移"], rows,
        [5, 18, 9, 20, 28, 34, 28])

    # ============ S4 DB項目定義 ============
    ws = wb.create_sheet("4_DB項目定義")
    def entity_block(title, cols_note, items):
        return [("ENTITY: " + title, "", "", "", "", "", "", "", cols_note)] + items
    rows = []
    rows += entity_block("Books 書籍マスタ (物理名: sap_training_bookorder_Books)", "KEY=● 必須=○",
        [("code", "書籍コード", "String", "10", "●", "○", "", "マスタキー"),
         ("title", "书名", "String", "120", "", "○", "", "一覧/明細へ表示"),
         ("author", "作者", "String", "60", "", "", "", ""),
         ("publisher", "出版社", "String", "60", "", "", "", ""),
         ("price", "定价", "Decimal", "9,2", "", "○", "", "受注時単価の既定値(上書き可)"),
         ("stock", "库存", "Integer", "", "", "", "0", "v1 は参照のみ")])
    rows += entity_block("Customers 得意先マスタ (物理名: sap_training_bookorder_Customers)", "", 
        [("code", "得意先コード", "String", "10", "●", "○", "", "マスタキー"),
         ("name", "客户名称", "String", "80", "", "○", "", ""),
         ("city", "都市", "String", "40", "", "", "", ""),
         ("contact", "联系人", "String", "40", "", "", "", "")])
    rows += entity_block("BookOrders 受注ヘッダ (物理名: sap_training_bookorder_BookOrders)", "managed により createdAt/createdBy/modifiedAt/modifiedBy を自動付与",
        [("orderNo", "受注番号", "String", "16", "●", "○", "SO+日付-連番", "サービス側採番(クライアント指定不可)"),
         ("orderDate", "受注日", "Date", "", "", "○", "当日", "受注日"),
         ("customer_code", "得意先(FK)", "String", "10", "", "○", "", "Customers への参照"),
         ("status", "状態", "String", "10", "", "○", "OPEN", "OPEN/APPROVED/REJECTED(クライアント変更不可)"),
         ("rejectReason", "却下理由", "String", "200", "", "", "", "reject 時必須"),
         ("rejectedBy / rejectedAt", "却下者/却下日時", "String / DateTime", "40/-", "", "", "", "監査"),
         ("approvedBy / approvedAt", "承認者/承認日時", "String / DateTime", "40/-", "", "", "", "監査。sendBack でクリア"),
         ("note", "備考", "String", "300", "", "", "", "納期希望等を記入"),
         ("totalAmount", "合計金額", "Decimal", "12,2", "", "○", "", "明細からサーバ計算。クライアント書込不可")])
    rows += entity_block("BookOrderItems 受注明細 (物理名: sap_training_bookorder_BookOrderItems)", "Composition of BookOrders: 親削除と同時に削除。FK: order_no",
        [("orderNo(lineNo組)", "受注番号(FK)", "String", "16", "●", "○", "", "親ヘッダのキー"),
         ("lineNo", "行番号", "Integer", "", "●", "○", "1..n", "サービス側自動採番"),
         ("book_code", "書籍(FK)", "String", "10", "", "○", "", "Books 参照。変更不可(変更=行削除+追加)"),
         ("bookTitle", "書名(スナップショット)", "String", "120", "", "○", "", "受注時点の書名を固定(マスタ改名の影響を受けない)"),
         ("quantity", "数量", "Integer", "", "", "○", "", ">0 の整数"),
         ("unitPrice", "単価", "Decimal", "9,2", "", "○", "マスタ価格", "登録時はマスタから。営業上書き可(>0)"),
         ("lineTotal", "行金額", "Decimal", "12,2", "", "○", "", "数量×単価(サーバ計算)")])
    _table(ws, "DB項目定義(CDS モデル = db/schema.cds と 1:1)", "命名: エンティティ=エンティティ名, 物理名=namespace を _ に置換したテーブル名(自動)",
        ["物理名(項目)", "論理名", "型", "桁/精度", "KEY", "必須", "既定値", "説明"], rows,
        [26, 22, 13, 9, 6, 6, 16, 44])

    # ============ S5 API定義 ============
    ws = wb.create_sheet("5_API定義")
    rows = [
        ("A-01", "GET", "/odata/order/Books", "エンティティ(読取)", "—", "OData コレクション", "—", "なし", "@readonly。主データ参照"),
        ("A-02", "GET", "/odata/order/Customers", "エンティティ(読取)", "—", "同上", "—", "なし", "@readonly"),
        ("A-03", "GET", "/odata/order/Orders", "エンティティ(読取)", "—", "一覧(JSON)。$top/$orderby/$filter/$expand=items 対応", "—", "なし", "F-0500 一覧照会"),
        ("A-04", "POST", "/odata/order/Orders", "エンティティ(作成: ヘッダ)", "ヘッダ項目(orderDate/customer_code/note 等。明細は含めない)", "201。採番後 orderNo/status=OPEN/合計=0 を返却", "—", "なし", "F-0100 受注登録(ヘッダ)。明細は A-08 で追加"),
        ("A-05", "PATCH", "/odata/order/Orders(orderNo='…')", "エンティティ(更新)", "note/orderDate/customer_code 等", "200。APPROVED は 400(差戻し要)", "—", "なし", "F-0300 変更"),
        ("A-06", "DELETE", "/odata/order/Orders(orderNo='…')", "エンティティ(削除)", "—", "204。APPROVED は 400", "—", "なし", "取消(OPEN/REJECTED のみ)"),
        ("A-07", "PATCH", "/odata/order/OrderItems(orderNo='…',lineNo=…)", "エンティティ(明細更新)", "quantity 等", "200。行金額・ヘッダ合計を自動再計算", "—", "なし", "F-0300 明細変更"),
        ("A-08", "DELETE/POST", "/odata/order/OrderItems", "明細行の追加・削除", "POST: book_code+quantity", "200/201。行番号自動。合計再計算", "—", "なし", "F-0300"),
        ("A-09", "POST", "/odata/order/approve", "Action(unbound)", "{orderNo}", "{ok,status:APPROVED}", "OPEN→APPROVED", "BasicAuth(alice)", "F-0200"),
        ("A-10", "POST", "/odata/order/rejectOrder", "Action(unbound)", "{orderNo, reason}", "{ok,status:REJECTED}", "OPEN→REJECTED(理由必須)", "BasicAuth", "F-0400 却下。※reject は框架予約語のため rejectOrder と命名"),
        ("A-11", "POST", "/odata/order/sendBack", "Action(unbound)", "{orderNo}", "{ok,status:OPEN}", "APPROVED→OPEN", "BasicAuth", "F-0400"),
    ]
    _table(ws, "API定義(OData V4)", "実装: srv/order-service.cds + order-service.js。エラーレスポンスは OData error 形式(メッセージは中国語)",
        ["No", "Method", "Path", "種別", "リクエスト", "レスポンス", "状態遷移", "認証", "備考"], rows,
        [7, 8, 40, 16, 34, 34, 18, 16, 26])

    # ============ S6 画面設計 ============
    ws = wb.create_sheet("6_画面設計")
    rows = [
        ("SC-01", "受注一覧", "List Report(Fiori elements)", "受注番号/得意先/受注日/状態/合計", "検索フィルタ(状態・期間・得意先)", "新規登録へ導線 / 行タップで詳細へ", "全ロール"),
        ("SC-02", "受注登録", "Object Page(新規)", "得意先(ValueHelp)/受注日/備考 + 明細テーブル(書籍 ValueHelp・数量・単価)", "保存=POST(深作成)", "登録後 OPEN。エラーは項目別表示", "営業"),
        ("SC-03", "受注詳細", "Object Page(表示+アクション)", "ヘッダ全項目 + items テーブル + 状態バッジ + 監査欄(承認者/日時/却下理由)", "承認 / 却下(理由ダイアログ) / 差戻し / 変更ボタン", "状態によりボタン活性制御(APPROVED は読取専用+差戻しのみ)", "営業/承認者/管理者"),
    ]
    r = _table(ws, "画面設計(方針: Fiori elements)", "実装は backend annotation(UI.LineItem/SelectionFields/HeaderInfo)を CDS に追加し Fiori tools で生成(本講座は v1 でAPI先行、UIは本表を要件として提示)",
        ["No", "画面名", "種別", "主要項目", "操作", "状態制御/備考", "対象ロール"], rows,
        [7, 14, 26, 36, 30, 34, 14])
    r = _section(ws, r + 1, "画面遷移", 7)
    for row in [
        ("起点", "イベント", "終点"),
        ("一覧", "「新規登録」", "登録画面"),
        ("登録画面", "保存(成功)", "一覧(新規受注 OPEN)"),
        ("一覧/登録", "行タップ", "詳細画面"),
        ("詳細(OPEN)", "承認ボタン", "詳細(APPROVED, 操作グレーアウト)"),
        ("詳細(OPEN)", "却下ボタン→理由入力", "詳細(REJECTED, 却下理由表示)"),
        ("詳細(APPROVED)", "差戻しボタン(管理者)", "詳細(OPEN, 変更可能に復帰)"),
        ("詳細(OPEN/REJECTED)", "変更→保存", "詳細(同状態, 合計更新)"),
    ]:
        ws.append(row)
    for row in ws.iter_rows(min_row=r, max_row=r + 7, max_col=3):
        for c in row:
            c.font = F_BODY; c.border = BORDER; c.alignment = WRAP
            if c.row == r:
                c.font = F_HEAD; c.fill = FILL_HEAD; c.alignment = CENTER
    ws.column_dimensions["A"].width = 7; ws.column_dimensions["B"].width = 26
    ws.column_dimensions["C"].width = 40; ws.column_dimensions["D"].width = 36
    ws.column_dimensions["E"].width = 30; ws.column_dimensions["F"].width = 34
    ws.column_dimensions["G"].width = 14

    # ============ S7 テストケース ============
    ws = wb.create_sheet("7_テストケース")
    rows = [
        ("TC-01", "受注登録(正常)", "POST /Orders(items×2, 不指定番号/単価/書名)", "201; 採番・OPEN・マスタ連動・合計=Σ", "P1"),
        ("TC-02", "数量不正", "quantity=0", "400 中文エラー", "P1"),
        ("TC-03", "空明細", "items=[]", "400「至少需要一行明細」", "P1"),
        ("TC-04", "書籍不在", "存在しない book_code", "400「書籍コード不存在」", "P1"),
        ("TC-05", "承認", "approve(OPEN)", "APPROVED; approvedBy/alice; approvedAt 記録", "P1"),
        ("TC-06", "二重承認/不正状態", "approve(APPROVED または REJECTED)", "400", "P1"),
        ("TC-07", "未認証Action", "approve を匿名で", "401", "P2"),
        ("TC-08", "変更(OPEN)", "PATCH note", "200; 状態・金額不変", "P1"),
        ("TC-09", "変更(APPROVED)", "PATCH note", "400「已承認…差戻し」", "P1"),
        ("TC-10", "明細変更", "PATCH quantity(OPEN)", "lineTotal・合計 自動再計算", "P1"),
        ("TC-11", "明細追加/削除", "POST/DELETE OrderItems", "行番号連番; 合計再計算", "P2"),
        ("TC-12", "却下", "reject(reason有)", "REJECTED; reason 記録", "P1"),
        ("TC-13", "却下(理由無)", "reject(reason無)", "400「必须填写理由」", "P1"),
        ("TC-14", "差戻しフロー", "sendBack→PATCH→再approve", "APPROVED→OPEN(監査クリア)→変更→APPROVED", "P1"),
        ("TC-15", "削除制御", "DELETE OPEN/APPROVED", "OPEN可 / APPROVED 400", "P2"),
        ("TC-16", "主データ書込", "PATCH Books/Customers", "405/400(読取専用)", "P3"),
        ("TC-17", "一覧", "GET + $expand=items + $filter", "明細・快照(bookTitle)が正しく返る", "P2"),
    ]
    _table(ws, "テストケース(機能・異常系)", "実施: 端末コマンド(curl)で本機実行。本講座の実測結果は README「本机实测输出」参照",
        ["No", "テスト項目", "手順", "期待結果", "優先度"], rows,
        [8, 20, 44, 40, 8])

    # ============ S8 非機能要件 ============
    ws = wb.create_sheet("8_非機能要件")
    rows = [
        ("性能", "NFR-01", "一覧応答", "データ100件程度で一覧表示 ≤2秒(ローカル目安)。$top 併用を推奨"),
        ("性能", "NFR-02", "登録/承認処理", "1操作 ≤1秒(ローカル目安)。トランザクションは自動管理"),
        ("可用性", "NFR-03", "稼働", "BTP Cloud Foundry 標準(99.9%目標は導入環境依存。v1 は単一インスタンス+ローカルDB)"),
        ("可用性", "NFR-04", "バックアップ", "本番は HANA Cloud の自動バックアップを利用(v1 開発は SQLite ファイル管理)"),
        ("セキュリティ", "NFR-05", "認証", "Action は要認証。本番は XSUAA + ロール(営業/承認者/管理者)へ移行。v1=mock(BasicAuth)"),
        ("セキュリティ", "NFR-06", "認可", "状態機会の権限はサーバ側で強制(クライアントからの状態改変不可)"),
        ("セキュリティ", "NFR-07", "監査", "承認/却下/差戻しの操作者・日時を保存(機能要件 F-0700)"),
        ("セキュリティ", "NFR-08", "通信", "HTTPS(TLS)。OData エンドポイントは BTP ルート経由"),
        ("運用", "NFR-09", "ログ", "CAP 標準ログ(cds ログ)。エラー時は 応答+ログ の trace を確保"),
        ("運用", "NFR-10", "初期データ", "マスタ(書籍/得意先)は CSV 投入手順を用意(プロジェクト db/data)"),
        ("制約", "NFR-11", "利用環境", "Chrome / Edge 最新版(PC)。モバイル最適化は v1 対象外"),
        ("制約", "NFR-12", "言語", "UI/メッセージ: 中国語(プロトタイプ)。i18n 対応は v2 で設計"),
        ("データ保持", "NFR-13", "保持期間", "受注・監査データは削除しない(却下理由含む)。削除は未承認/却下のみ可"),
    ]
    _table(ws, "非機能要件", "v1 の受入基準(ローカル実行)を明記。本番基準は導入時レビュー",
        ["分類", "No", "要件名", "内容・受入基準"], rows,
        [10, 10, 20, 74])

    # ============ S9 工程計画 ============
    ws = wb.create_sheet("9_工程計画")
    rows = [
        ("要件定義", "2-3日", "要件定義書(本ファイル: 0_概要〜8_非機能)", "ヒアリング → 機能/非機能/状態遷移の合意", "状態遷移・監査要件の抜け漏れ"),
        ("基本設計", "2-3日", "db/schema.cds, order-service.cds, 画面方針(6_画面設計)", "DB項目定義/API一覧を確定、UI 方式を選定(elements)", "キー設計・マスタ連動方針"),
        ("詳細設計", "2日", "order-service.js(状態機会/バリデーション設計), docs/test-cases.md", "状態機会・例外系・監査項目の実装仕様", "400系エラー設計・金額計算箇所"),
        ("開発実装", "3日", "プロジェクトコード一式(projects/book-order-app)", "CAP モデル→サービス→ハンドラ→CSV 初期データ", "レビュー: 状態機会がバイパス不能か"),
        ("結合テスト", "1-2日", "docs/test-cases.md + 実行ログ", "curl/Postman で TC-01〜TC-17 実施", "異常系・権限(401)含め全数実施"),
        ("総合テスト(UAT)", "1-2日", "UAT 結果記録(別紙)", "利用者ロールで業務フロー(3_業務フロー)を通し確認", "業務としての使い勝手・運用観点"),
        ("リリース", "1日", "mta.yaml(本番向け), 初期データ CSV", "BTP CF へデプロイ。HANA 切替・Destination 設定", "環境差分(HANA/SQLite)の動作確認"),
        ("運用手引", "0.5日", "プロジェクト README 運用手順", "起動/再デプロイ/データ再投入手順の文書化", "新人でも再現可能か"),
    ]
    _table(ws, "工程計画(WBS: 目安)", "個人学習想定の目安工数。チーム案件では各工程にレビューとサインオフを追加すること",
        ["工程", "期間", "成果物", "主な作業", "レビュー観点"], rows,
        [12, 10, 40, 40, 30])

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    wb.save(OUT)
    print("saved:", OUT)


if __name__ == "__main__":
    main()
