#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成 SD見込生産MTS_要件定義・手順書.xlsx
-- SAP S/4HANA 見込生産（MTS / Make-to-Stock）实战训练站（sapmts/）の Excel 版成果物 --

用法: python3 tools/make_mts_xlsx.py
依赖: openpyxl (pip install openpyxl)

シート構成（11 枚）:
  0_概要 / 1_環境・前提 / 2_設定一覧(C1〜C17) / 3_配置手順(C0〜C16) / 4_練習手順(練習①〜⑤)
  5_期待結果・検証 / 6_故障対照表(12 項) / 7_用語集(日中) / 8_出典
  9_受講者チェックリスト / 10_講師用ガイド

視覚言語は btp-dev-hub/tools/make_requirements_xlsx.py と sapmto/tools/make_mto_xlsx.py を踏襲
（見出し行 = 青 0A6ED1 / 微软雅黑 / 罫線 / 交互行の淡灰 / シート別の列幅 / freeze panes）。
"""
import os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, "..", "SD見込生産MTS_要件定義・手順書.xlsx"))

BLUE, LIGHT, GREY, INK = "0A6ED1", "E3F0FA", "F2F4F7", "1D2D3E"
F_TITLE = Font(name="微软雅黑", size=15, bold=True, color="FFFFFF")
F_SMALL = Font(name="微软雅黑", size=9, color="6B7A8D")
F_HEAD = Font(name="微软雅黑", size=10, bold=True, color="FFFFFF")
F_BODY = Font(name="微软雅黑", size=10, color=INK)
FILL_TITLE = PatternFill("solid", fgColor=BLUE)
FILL_HEAD = PatternFill("solid", fgColor=BLUE)
FILL_ALT = PatternFill("solid", fgColor=GREY)
THIN = Side(style="thin", color="C9D6E0")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP = Alignment(wrap_text=True, vertical="top")
CENTER = Alignment(wrap_text=True, vertical="center", horizontal="center")


def table(ws, title, subtitle, headers, rows, widths):
    ncol = len(headers)
    last = get_column_letter(ncol)
    ws.merge_cells(f"A1:{last}1")
    c = ws.cell(1, 1, title); c.font = F_TITLE; c.fill = FILL_TITLE
    ws.row_dimensions[1].height = 26
    ws.merge_cells(f"A2:{last}2")
    ws.cell(2, 1, subtitle).font = F_SMALL
    ws.row_dimensions[2].height = 15
    for j, h in enumerate(headers, 1):
        c = ws.cell(3, j, h); c.font = F_HEAD; c.fill = FILL_HEAD
        c.alignment = CENTER; c.border = BORDER
    ws.row_dimensions[3].height = 22
    for i, row in enumerate(rows):
        r = 4 + i
        for j, v in enumerate(row, 1):
            c = ws.cell(r, j, v); c.font = F_BODY; c.alignment = WRAP; c.border = BORDER
            if i % 2 == 1:
                c.fill = FILL_ALT
        longest = max((len(str(x)) for x in row), default=0)
        ws.row_dimensions[r].height = max(17, 13 * (1 + longest // 30))
    for j, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(j)].width = w
    ws.freeze_panes = ws.cell(4, 1)
    return 4 + len(rows)


def kv(ws, title, subtitle, pairs, widths):
    ncol = len(widths)
    last = get_column_letter(ncol)
    ws.merge_cells(f"A1:{last}1")
    c = ws.cell(1, 1, title); c.font = F_TITLE; c.fill = FILL_TITLE
    ws.row_dimensions[1].height = 26
    ws.merge_cells(f"A2:{last}2")
    ws.cell(2, 1, subtitle).font = F_SMALL
    for i, (k, v) in enumerate(pairs):
        r = 3 + i
        ck = ws.cell(r, 1, k); cv = ws.cell(r, 2, v)
        ck.font = F_HEAD; ck.fill = FILL_HEAD; ck.alignment = WRAP; ck.border = BORDER
        cv.font = F_BODY; cv.alignment = WRAP; cv.border = BORDER
        ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=ncol)
        ws.row_dimensions[r].height = max(17, 13 * (1 + len(str(v)) // 60))
    for j, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(j)].width = w
    return 3 + len(pairs)


# ============================== データ ==============================

SUMMARY = [
    ("案件名称", "SAP S/4HANA 見込生産（Make-to-Stock / MTS）実習シナリオ"),
    ("案件ID", "TRN-SD-MTS-2026"),
    ("目的", "需要予測（PIR）→ MRP → 計画手配 → 製造指図 → 部品出庫 261 → 実績 → 完成品入庫 101（自由在庫）→ "
             "受注の引当（ATP）と PIR の消費 → 出荷 PGI 601 → 請求 → 差異計算・決済 を、"
             "①練習配置（SPRO 手順 C0〜C16）②練習流程（実機オペレーション ①〜⑤）の 2 本立てで学習する。"),
    ("対象範囲（本教材）", "見込生産の主線（戦略グループ 40 = 最終組立ありの計画）を主線とし、"
                      "対照として戦略 10（消費なし）・11（総所要量計画）・70（組立レベル）まで。"
                      "標準原価（CK11N/CK40N/CK24）・差異計算（KKS1/KKS2）・決済（KO88/CO88）・棚卸・欠品対応・"
                      "Cloud（スコープアイテム BJ5 / SSCUI）の差異対照を含む。"),
    ("対象外", "受注生産（MTO：戦略 20 / 受注在庫 E）と受注設計生産（ETO：WBS / プロジェクト在庫 Q）の詳細、"
             "バリアント設定（VC / 戦略 25）、繰返し生産（REM / 戦略 11 と組み合わせる場合）、"
             "aATP / PP-DS による能力制約付き計画、需要計画システム（IBP）の実装。"),
    ("システム前提", "SAP S/4HANA On-Premise 2020〜2024（画面パスは 2023/2024 基準）。"
                 "Public Cloud の差異は「3_配置手順」の C16 と「8_出典」を参照。"),
    ("練習用オブジェクト", "得意先 1000 / 販売組織 1000・チャネル 10・部門 00 / プラント 1000 / "
                    "完成品 ZMTS-FG01（FERT、標準価格 8,000 JPY、安全在庫 100 PC）/ "
                    "部品 ZMTS-RM01・ZMTS-RM02 / 作業区 ZMTS_WC01 / BOM RM01×2・RM02×4 / "
                    "対照用品目 ZMTS-FG10（戦略 10）。"),
    ("業務シナリオ", "月次見込 500 PC（PIR・版 00・3 か月分）。MRP で計画手配 → 製造指図 500 PC → "
                 "部品 RM01 1,000 PC / RM02 2,000 PC を 261 出庫 → 実績 500 → 101 で自由在庫 +500 PC。"
                 "得意先 1000 が 200 PC（8,000 JPY/PC = 1,600,000 JPY、希望納期 = 受注日 + 7 日）を受注 → "
                 "PIR を 200 消費（500 → 残 300）→ ATP 引当 → 出荷 PGI 601 → 請求 → 差異計算・決済。"),
    ("完成基準", "選択問題 28 題で 75% 以上（21/28）＋「9_受講者チェックリスト」の全項目が証跡つきで説明できること。"),
    ("本教材の立場（重要）", "SAP の標準値は版本・業界ソリューション・既有改造で異なる。本教材は「標準の通常情況」を示しつつ、"
                      "すべての STEP に『自システムでの確認方法（T-code / テーブル / 画面）』を添える。"
                      "例：戦略グループ 40 = 最終組立ありの計画（Planning with final assembly）、"
                      "70 = 組立レベルでの計画、30 = ロット生産、11 = 総所要量計画（受注は PIR を消費しない）。"
                      "ネット上の 40/30 の取り違えに注意し、OPPT の記述で必ず確認する。"),
    ("改訂", "v1.0（2026-09）初版。HTML サイト版（sapmts/ の 11 ページ）と内容同期。"),
]

ENV = [
    ("1", "販売組織 / 販売チャネル / 部門（販売エリア）", "1000 / 10 / 00",
     "SPRO の組織構造＋ VA01 の初期画面で選択可能か確認"),
    ("2", "プラント / 出荷プラント", "1000 / 1000", "VA01 の明細でプラント 1000 を入力できる"),
    ("3", "得意先 1000（受注先＝出荷先）", "得意先マスタに 販売エリアビュー＋出荷先（船積先）",
     "BP（または XD03）で得意先 1000 の販売エリア／出荷先を確認"),
    ("4", "品目マスタ（完成品）", "ZMTS-FG01 / FERT / PC / 販売組織1・2・MRP1〜4・会計1・原価計算1",
     "MM03 で全ビューが存在し、MRP3 の戦略グループが空でないこと（MARC-STRGR）"),
    ("5", "品目マスタ（部品）", "ZMTS-RM01（ROH）/ ZMTS-RM02（HAWA）/ 初期在庫 1,000・2,000 PC",
     "MB52 / MMBE で非制限使用在庫を確認（561 で投入）"),
    ("6", "標準原価", "標準価格 8,000 JPY/PC・価格管理 S（マーク・リリース済み）",
     "MM03 会計1（MBEW-STPRS・VPRSV）／CK13N の項目明細"),
    ("7", "原価計算の前提", "原価センタ・活動タイプ・レート（KP26）・原価計算バリアント（OKKN）・差異キー（OKV1/OKVW/OKVG）",
     "KP26 に当期レートがあること。無いと CK11N の作業費が 0 になる"),
    ("8", "BOM / 作業区 / 作業手順", "RM01×2・RM02×4 / ZMTS_WC01 / 工程 0010・1 H/PC、有効日が実習日を含む",
     "CS03 / CR03 / CA03（有効期間も確認）"),
    ("9", "条件レコード", "PR00 = 8,000 JPY（販売組織 1000・実習日を含む有効期間）", "VK13 で条件レコードを確認"),
    ("10", "SD 側の 3 つの決定", "VOV4（OR+0001+空+空→TAN）/ VOV5（TAN+PD→CP）/ VOV6（CP の所要量転送・在庫確認 ON）",
     "VOV7/VOV4/VOV5/VOV6 の画面と VBEP の実測値で確認"),
    ("11", "MRP 側の設定", "OPPT/OPPS（戦略 40）/ OMDU（MRP パラメータ）/ OPJH・OPL8（指図タイプ PP01）",
     "OPPT の説明文と MM03 MRP2 の伝票タイプ（PP01）"),
    ("12", "番号範囲", "受注（VN01）・出荷・請求・製造指図・棚卸伝票に空きがあること", "各伝票を 1 件ずつテスト登録"),
    ("13", "会計期間", "当期が FI/CO ともに開いている（差異計算と決済に必須）", "OB52（FI）と KKS2/KO88 のテスト実行"),
    ("14", "カスタマイジング依頼", "VOV4/VOV5 に自建行を入れる場合は書き込み可能な依頼が必要", "SPRO 起動時の依頼入力画面"),
    ("15", "権限", "SPRO 表示＋ MM01/02・MD61/MD62・MD01N・CO01/CO02/CO11N/CO40/CO41・MIGO・VA01・VL01N/VL02N・VF01・CK11N・KKS1/KKS2・KO88",
     "実習ユーザで 1 回ずつ実行して確認"),
]

SETTINGS = [
    ("C1", "品目カテゴリグループ（販売組織2）", "0001 NORM（標準品）。DIEN / LEIS / ERLA / LUMF 等は用途別。見込生産専用の標準キーは無い",
     "0001（発展で Z001 を追加）", "MM03 販売組織2（MVKE-MTPOS）"),
    ("C2", "品目 MRP1", "MRPタイプ PD / ロットサイズ EX / 手配タイプ E（内製）", "PD / EX / E", "MM02 MRP1（MARC-DISMM/DISPO）"),
    ("C3", "品目 MRP2 安全在庫・指図タイプ", "安全在庫は現場の欠品許容度で決める。指図タイプは PP01 が標準", "安全在庫 100 PC / PP01",
     "MM02 MRP2（MARC-EISBE）"),
    ("C4", "品目 MRP3 戦略グループ・消費モード <出典:OPPT/OPPS>", "見込生産 10/11/30/40/70。40 は受注が PIR を消費する。10/11 は消費しない",
     "戦略グループ 40 / 消費モード 2 / 逆 30 日・順 20 日", "MM02 MRP3（MARC-STRGR/VRMOD/VINT1/VINT2）"),
    ("C5", "品目 MRP3 在庫確認（チェックルール）", "見込生産は ATP 対象。値の意味は環境で異なるため F1 で確認", "例 02（F1 で説明を確認）",
     "MM02 MRP3（MARC-PRREG 系）・OVZ9"),
    ("C6", "品目 MRP4 個別/包括所要量", "見込生産は空（または包括所要量）。個別所要量のみにすると受注在庫 E（MTO）になる", "空",
     "MM02 MRP4（MARC-SOBSL 系）・MMBE の特在欄"),
    ("C7", "標準原価の計算・マーク・リリース", "CK11N（単品目）→ CK40N（一括）→ CK24（マーク/リリース）。会計1 の価格管理 S", "標準価格 8,000 JPY/PC",
     "CK11N・CK40N・CK24・MM03 会計1（MBEW-STPRS）"),
    ("C8", "BOM・作業区・作業手順", "計画手配の BOM 展開と標準工時の基礎。1 PC あたりの構成と標準時間", "RM01×2 / RM02×4、工程 0010、1 H/PC",
     "CS01・CR01・CA01（照会 CS03/CR03/CA03）"),
    ("C9", "計画方針／計画方針グループ", "OPPS（計画方針）/ OPPJ（方針グループ）/ OPPT（一覧）。10 LSF・11 BSF・40 VSF・70 VSFB", "40 を使用、対照で 10・11",
     "OPPS・OPPJ・OPPT"),
    ("C10", "需要管理（PIR の登録と消費）", "PIR は MD61/MD62/MD63/MD73、版 00 が有効版（T459U）。消費は戦略と消費モードに従う", "版 00、3 か月 × 500 PC",
     "MD61・MD62・MD73・SE16N: PBED/PBIM"),
    ("C11", "所要量タイプ／所要量クラス", "見込生産系：LSF（→100）/ BSF（→102）/ VSF。得意先：KSL（→030）/ KSV（→050）",
     "VSF / KSV（戦略 40 経由。実際の値は自システムで確認）", "OPPS・OVZH・OVZG・SE16N: T459K"),
    ("C12", "明細カテゴリグループの定義", "NORM / DIEN / LEIS / ERLA / LUMF 等。見込生産専用の標準キーは特に無い", "確認＋発展で Z001 を追加",
     "IMG：販売管理>販売伝票>販売伝票明細>定義: 明細カテゴリグループ"),
    ("C13", "明細カテゴリの定義", "TAN（標準明細）。特別在庫欄は空（= 自由在庫）が MTS の要点", "TAN を確認（発展で ZTAN 追加・特別在庫は空のまま）",
     "VOV7（TVAP-SOBKZ）"),
    ("C14", "明細カテゴリ／納入日程行カテゴリの割当", "VOV4 の 4 鍵 → TAN。VOV5 の 2 鍵（明細カテゴリ＋MRPタイプ）→ CP",
     "OR+0001→TAN、TAN+PD→CP", "VOV4・VOV5"),
    ("C15", "納入日程行カテゴリ（所要量転送・在庫確認）", "CP は所要量転送 ON・在庫確認 ON・移動タイプ 601（標準）。環境により値が異なる",
     "CP を確認（発展で ZCP）", "VOV6（TVEP-BEDSD/ATPPR/BWART/BDART）・VBEP"),
    ("C16", "在庫確認（ATP）の制御", "品目 MRP3 のチェックルール＋チェックグループ×チェックルール（OVZ2）＋スコープオブチェック（OVZ9）",
     "確認のみ（CO09 で動作確認）", "OVZ9・OVZ2・CO09・MDVP・V_V2"),
    ("C17", "出荷・請求・自動転記・棚卸", "LF / F2、VTFL コピー制御、OBYC（BSX/GBB）、棚卸は MI01/MI04/MI07", "標準のまま使用（確認のみ）",
     "VL01N・VF01・VTFL・OBYC・MI01・MATDOC"),
]

CONFIG_STEPS = [
    ("C0", "前提与环境确认", "VA01・BP/XD03・MMNR・VN01",
     "販売エリア 1000/10/00 / プラント 1000 / 得意先 1000（出荷先あり）/ 番号範囲に空き / 権限",
     "VA01 で販売エリアが選べる／BP/XD03 で得意先／MMNR で品目番号範囲／VN01 で受注明細範囲",
     "VA01 の初期画面で 1000/10/00 が選べること。受注はまだ保存しない（練習④ で作る）",
     "MD61 で品目/プラントが選べない → プラント在庫ビュー（MARC）未登録"),
    ("C1", "部品品目（ZMTS-RM01 / ZMTS-RM02）", "MM01・MM02・MIGO",
     "ROH/HAWA、MRPタイプ PD、ロットサイズ EX、手配タイプ F、会計1 価格管理 S、初期在庫 1,000 / 2,000 PC（561）",
     "MM01 でビュー選択（基本/購買/MRP1〜4/会計1/原価計算1/プラント在庫）→ 保存 → MIGO 561 で初期在庫",
     "MMBE で自由在庫 1,000 / 2,000 PC。MATDOC に 561 の在庫伝票",
     "部品に戦略グループを付けると部品にも PIR が必要になり MRP が空転する（付けない）"),
    ("C2", "完成品品目 ZMTS-FG01（最重要）", "MM01・MM02・MM03",
     "販売組織2 品目カテゴリグループ 0001 / MRP1 PD・EX・手配タイプ E / MRP2 安全在庫 100 / MRP3 戦略 40・消費モード 2・逆30 順20・在庫確認 / MRP4 個別包括所要量 空 / 会計1 価格管理 S",
     "MM01 で全ビュー選択 → 上記を入力 → 保存 → MM03 で再確認",
     "MM03 MRP1〜4 と SE16N: MARC（STRGR/VRMOD/VINT1/VINT2/DISMM/DISPO/BESKZ/EISBE）",
     "① MRP4 に 1 を入れると受注在庫 E になり MTO 化 ② 戦略グループ空だと受注が PIR を消費しない ③ 手配タイプ空だと計画手配ができない"),
    ("C3", "BOM・作業区・作業手順", "CS01・CR01・CA01・C223",
     "BOM：RM01×2・RM02×4（基本数量 1 PC）／作業区 ZMTS_WC01（活動タイプ・式）／工程 0010・標準時間 1 H/PC・割当",
     "CS01 → CR01 → CA01 の順に作成し、工程に割当（品目＋BOM 用途 1）を設定",
     "CS03 で明細 2 行、CA03 で工程 1 行。MD02 で部品に従属所要量が出る",
     "BOM の有効日切れ／工程の割当漏れ → CK11N で工数が拾えない・指図に工程が無い"),
    ("C4", "標準原価（CK11N → CK40N → CK24）", "CK11N・CK40N・CK24・OKKN・KP26",
     "価格管理 S／標準価格 8,000 JPY/PC／原価計算バリアント（例 PP01 系）／ロットサイズ EX／レート（KP26 例 3,000 JPY/H）",
     "KP26 でレート → CK11N → 結果保存 → CK24 でマーク → リリース（一括は CK40N）",
     "MM03 会計1 に標準価格 8,000 / 価格管理 S。MBEW-STPRS・CK13N の項目明細",
     "リリース忘れ（マークのみ）→ 標準価格が出ず差異計算ができない。レート無し → 作業費 0"),
    ("C5", "販売条件（PR00）と品目カテゴリグループ", "VK11・VK13・MM03",
     "条件レコード PR00 = 8,000 JPY（販売組織 1000・有効期間）／品目カテゴリグループ 0001",
     "VK11 で条件登録 → MM03 販売組織2 で品目カテゴリグループ確認（発展で Z001 を追加）",
     "VK13 で条件が見える。VA01 の条件画面に 8,000 JPY が出る",
     "有効期間切れ／販売組織不一致 → 請求額 0 の原因。品目カテゴリグループ空 → 明細カテゴリ決定不可"),
    ("C6", "明細カテゴリの定義（VOV7）", "VOV7",
     "TAN：明細カテゴリ標準／特別在庫 空／価格設定 有効／納入日程行許可 ON",
     "VOV7 で TAN を開いて各フラグを確認（発展で ZTAN をコピー作成・特別在庫は空のまま）",
     "VOV7 の画面／SE16N: TVAP（SOBKZ が空であること）",
     "特別在庫に E を入れると MTS が崩れる。納入日程行許可 OFF → 納入日程行が作られない"),
    ("C7", "明細カテゴリの割当（VOV4）", "VOV4",
     "OR ＋ 0001 ＋ 用途 空 ＋ 上位明細カテゴリ 空 → TAN（発展：OR + Z001 → ZTAN）",
     "VOV4 で OR を選択 → 4 鍵を確認／発展で Z001 の行を追加",
     "VA03 の明細カテゴリが TAN（発展では ZTAN）",
     "空値もキー。用途や上位明細を勝手に入れると決定がずれる。販売伝票タイプを間違えると効かない"),
    ("C8", "納入日程行カテゴリの定義（VOV6）", "VOV6",
     "CP：移動タイプ 601／納入関連 ON／所要量転送 ON／在庫確認 ON",
     "VOV6 で CP を開き、所要量転送・在庫確認・移動タイプを確認（発展で ZCP をコピー作成）",
     "VOV6 の画面／SE16N: TVEP（BEDSD/ATPPR/BWART/BDART）／VA03 納入日程行",
     "所要量転送 OFF → MD04 に受注が出ない。在庫確認 OFF → 確認済数量 0。移動タイプ ≠ 601 → PGI で在庫が落ちない"),
    ("C9", "納入日程行カテゴリの割当（VOV5）", "VOV5",
     "TAN ＋ PD（品目 MRPタイプ） → CP（発展：ZTAN + PD → ZCP）",
     "VOV5 で TAN の行を確認。「MRPタイプ空」の行の有無も確認 → 発展で ZTAN の行を追加",
     "VA03 の納入日程行カテゴリが CP（SE16N: VBEP-ETTYP）",
     "品目に MRP ビューが無い（MRPタイプ空）と別カテゴリになり、所要量転送や在庫確認の挙動が変わる"),
    ("C10", "所要量クラス（OVZG）", "OVZG・OVZH",
     "100（見込生産）/ 030（在庫からの販売）/ 050（消費付き受注）に個別在庫なし。040（MTO）に個別在庫あり",
     "OVZG で一覧を開き、各クラスの「個別在庫」「消費」フラグを確認。040 と対比する",
     "OVZG の各クラス。実測は VA03 の納入日程行の所要量タイプ → クラス。SE16N: T459K",
     "クラスに個別在庫があると 101 入庫が受注在庫 E に入る。消費フラグの意味を取り違えると PIR の動きを誤解する"),
    ("C11", "所要量タイプとその決定（OPPS/OVZH/OVZI）", "OPPS・OVZH・OVZI",
     "戦略 40：独立所要量タイプ VSF／得意先所要量タイプ KSV（→ クラス 050）。決定順は戦略グループ優先 → 明細カテゴリ＋MRPタイプ",
     "OPPS で計画方針 40 を開き、独立/得意先のタイプを確認 → OVZH でクラスを確認 → OVZI で決定順を確認",
     "OPPS の画面／VA03 の納入日程行（BDART）／MD04 の独立所要量明細",
     "品目に戦略グループがあると OVZI の自建決定は効かない。タイプ名は環境差があるので必ず自システムで確認する"),
    ("C12", "計画方針グループ（OPPT/OPPS/OPPJ）", "OPPT・OPPS・OPPJ",
     "10 = 見込生産（LSF/KSL、消費なし）／11 = 見込生産・総所要量計画（BSF/KSL、在庫を見ない）／30 = ロット生産（LSF/KL）／40 = 最終組立ありの計画（VSF/KSV、消費あり）／70 = 組立レベルでの計画（VSFB）",
     "OPPT で 10/11/30/40/70 の説明文と所要量タイプ割当を並べて確認（発展で Z040 を自建）",
     "OPPT の説明文（最も信頼できる「標準値」）／MM03 MRP3（MARC-STRGR）",
     "40 と 30 の説明を逆に覚えている教材が多い。30 = ロット生産（Production by lot size）が標準。必ず OPPT で確認する"),
    ("C13", "在庫確認（ATP）の設定", "OVZ9・OVZ2・CO09・MDVP・V_V2",
     "品目 MRP3 のチェックルール（例 02）／スコープオブチェック：在庫＋入庫予定＋出庫予定（個別所要量は通常 OFF）／得意先のチェックグループ",
     "MM02 MRP3 でチェックルール（F1 で意味を確認）→ OVZ9 でスコープを確認 → OVZ2 でチェックグループ×ルールの組合せを確認 → CO09 で動作確認",
     "CO09 の利用可能数量と要素一覧／VA03 の確認済数量／SE16N: VBEP・VBBS",
     "スコープに入庫予定が無いと、先造りした在庫が受注時に見えない。番号（01/02…）の意味は環境差 → F1 で確認"),
    ("C14", "MRP 側の設定と実行", "MD01N・MD02・MD04・OMDU・OPJH・OPL8・CO40・CO41",
     "処理キー（NEUPL 総再計画 / NETCH ネットチェンジ等）／指図タイプ PP01／計画手配の変換（CO40 単品目・CO41 一括）",
     "OMDU を確認 → MD01N 実行 → MD04 で計画手配を確認 → CO40/CO41 で指図に変換 → CO03 で確認",
     "MD04／SE16N: PLAF（計画手配）・AUFK/AFPO（指図）／MD01N の実行ログ",
     "MRP リスト（MD05/MD06）は MRP Live では作られない（KBA 2640393）。MD03 は提供されない"),
    ("C15", "出荷・請求・自動転記・棚卸", "VL01N・VL02N・VF01・VTFL・OBYC・MI01",
     "出荷タイプ LF／請求タイプ F2／PGI 移動タイプ 601／OBYC の BSX（在庫）・GBB（出庫相手）／棚卸 MI01→MI04→MI07",
     "VL01N → VL02N（引当・ピッキング）→ PGI 601 → VF01 → FB03。棚卸は 1 回通す",
     "VL03N の在庫/引当／MMBE／MATDOC（601）／FB03／OBYC の設定",
     "引当不足で PGI 不可、条件未設定で請求 0、勘定未設定で会計伝票が出ない"),
    ("C16", "Public Cloud 差异对照", "SSCUI・スコープアイテム・Fiori",
     "明細カテゴリ・販売伝票タイプの新規作成不可（What you see is what you get）。スコープアイテム BJ5（Make-to-Stock Production – Discrete Manufacturing）/ BJ8（Process）/ J44（MRP）。SSCUI 例 105120（明細カテゴリ別の所要量タイプ決定）",
     "「設定」アプリ（Manage Your Solution → Configuration）で名称検索し、自分の SSCUI ID とスコープアイテムを確認 → Fiori「Manage PIRs」で PIR を 1 行登録",
     "設定アプリの検索結果／スコープ（Scoping）画面／Road Map Viewer の Best Practices 一覧",
     "断言できるのは BJ5 と SSCUI 105120 まで。他の ID は版本で変わるため要確認。On-Premise の手順をそのまま適用すると詰まる"),
]

PRACTICE = [
    ("①", "需要予測と PIR（MD61 → MD62 → MD04）", "MD61・MD62・MD63・MD73・MM03・MMBE",
     "版 00、3 か月 × 500 PC（変更で 600）。戦略グループ 40・消費モード 2 を確認",
     "1) MM03 で戦略グループ確認 2) MD61 で PIR 登録 3) MD73 で一覧確認 4) MD04 で独立所要量（受注番号なし）を確認 5) MD62 で数量変更",
     "MD04 に「計画独立所要量」が 3 行（受注番号なし）／利用可能数量がマイナス／PBED に 3 行",
     "版が 00 以外だと MRP が見ない。納入日が表示期間外だと MD04 に出ない"),
    ("②", "MRP 実行と計画手配（MD01N → MD04 → CO40/CO41）", "MD01N・MD02・MD04・CO40・CO41・CO03",
     "プラント 1000・品目 ZMTS-FG01・処理キーは環境既定。安全在庫 100 を考慮した数量",
     "1) MD01N 実行 2) MD04 で計画手配確認 3) 純所要量を検算 4) 部品の従属所要量確認 5) CO40/CO41 で指図変換 6) CO03 で確認",
     "計画手配（例 600 PC/月、在庫区分 空・受注番号なし）／部品 RM01 1,000・RM02 2,000 PC／指図 PP01・状態 CRTD",
     "純所要量 = 総所要量 − 入庫予定 + 安全在庫 が合わない最大の原因は他の入庫予定。MRP リストは無い（MD04 を使う）"),
    ("③", "製造と入庫（CO02 → 261 → CO11N → 101 → 自由在庫）", "CO02・MIGO・CO11N・CO03・MMBE・MB52・FB03",
     "解放（REL）／部品 261：RM01 1,000・RM02 2,000／歩留 500 PC／101 で完成品 500 PC（保管場所 0001）",
     "1) CO02 で解放 2) MIGO 261 で部品出庫 3) CO11N で歩留 500 を実績 4) MIGO 101 で入庫 5) MMBE/MB52 で自由在庫確認 6) FB03 で会計伝票",
     "自由在庫（非制限利用）+500 PC・特別在庫は空／指図状態 DLV／会計伝票は標準価格ベース（8,000 × 500 = 4,000,000 JPY）",
     "入库が得意先別（受注在庫 E）に入ったら MTO 化（MRP4 の個別所要量／指図の受注参照を確認）"),
    ("④", "受注・引当・出荷・請求（VA01 → CO09 → VL01N → VF01）", "VA01・VA03・CO09・V_V2・VL01N・VL02N・VF01・VF03・FB03",
     "受注タイプ OR・得意先 1000・品目 ZMTS-FG01・200 PC・希望納期 受注日+7 日・単価 8,000 JPY（1,600,000 JPY）",
     "1) VA01 で受注 2) 明細カテゴリ TAN・納入日程行 CP を確認 3) CO09 で受注前後の可用量比較 4) MD04 で PIR 消費を確認 5) VL01N/VL02N で引当・PGI 601 6) VF01 で請求 7) VA03 の伝票フロー確認",
     "CO09 の可用量 500 → 300／MD04 の消費済 200（PBED は 500 のまま）／自由在庫 300／請求 1,600,000 JPY／伝票フロー閉合",
     "「PIR が減っていない＝消費されない」は誤解。消費は MD04 の消費済数量で確認する"),
    ("⑤", "月末処理と発展（KKS1/KKS2 → KO88/CO88・棚卸・故障）", "KKS2・KKS1・KKA1・KKAO・KO88・CO88・MI01・MI04・MI07・FB03",
     "差異計算（カテゴリ別）／決済（会計伝票）／棚卸差異（例 300 → 298 PC = 16,000 JPY）／故障対照表 12 項",
     "1) CO03 で実際原価確認 2) KKS2 → KKS1 で差異計算 3) KO88/CO88 で決済 4) FB03 で確認 5) 棚卸を 1 回通す 6) 故障対照表で 3 項以上を説明 7) 発展課題を 2 つ以上実行",
     "差異カテゴリ別の内訳／決済後の FI 伝票／棚卸更新後の在庫／発展（戦略 10 との比較・部品の購買化・ロットサイズ比較）",
     "差異は異常ではない（額と原因が問題）。差異カテゴリの番号は暗記せず KKS1 の出力で確認する"),
]

EXPECT = [
    ("1", "PIR", "版 00 に 3 か月 × 500 PC。MD04 に受注番号なしの独立所要量", "MD73・MD04・SE16N: PBED"),
    ("2", "MRP", "MD01N 後に計画手配（例 600 PC/月）が生成、在庫区分 空", "MD04・SE16N: PLAF"),
    ("3", "BOM 展開", "部品に従属所要量（RM01 1,000・RM02 2,000 PC）", "MD04（部品）・RESB"),
    ("4", "指図", "PP01 の製造指図、受注明細参照（AFPO-KDAUF/KDPOS）が空", "CO03・SE16N: AFPO"),
    ("5", "部品出庫", "261 で部品が減り、MATDOC に 261 の伝票", "MMBE・SE16N: MATDOC"),
    ("6", "実績", "CO11N で歩留 500、状態 CNF", "CO03・SE16N: AFRU"),
    ("7", "完成品入庫", "101 で自由在庫 +500 PC、特別在庫（得意先別）は空、状態 DLV", "MMBE・MB52・SE16N: MARD/MSKA"),
    ("8", "標準原価", "会計伝票の金額 = 標準価格 8,000 × 500 = 4,000,000 JPY", "FB03・MM03 会計1"),
    ("9", "受注", "明細カテゴリ TAN・納入日程行カテゴリ CP（所要量転送 ON・在庫確認 ON）", "VA03・VBAP・VBEP"),
    ("10", "ATP", "CO09 の可用量 500 → 300、確認済数量 200", "CO09・VA03"),
    ("11", "PIR 消費", "MD04 の消費済数量 200。PBED の数量（500）は不変", "MD04・SE16N: PBED"),
    ("12", "出荷", "引当は自由在庫（在庫区分 空）から 200 PC", "VL03N"),
    ("13", "PGI", "601 で自由在庫 500 → 300 PC", "MMBE・SE16N: MATDOC"),
    ("14", "請求", "請求 1,600,000 JPY（200 × 8,000）。会計伝票（売掛金/売上）", "VF03・FB03"),
    ("15", "伝票フロー", "受注 → 出荷 → 請求 → 会計伝票 が閉じている", "VA03 → 環境 → 伝票フロー"),
    ("16", "差異計算", "KKS2/KKS1 で差異と差異カテゴリ別内訳が出る", "KKS2・CO03"),
    ("17", "決済", "KO88/CO88 で差異が FI に転記される", "KO88 のログ・FB03"),
    ("18", "棚卸", "MI01→MI04→MI07 で実地数量に更新、差異の会計伝票", "MI03・MMBE・FB03"),
]

TROUBLE = [
    ("1", "MRP を実行しても計画手配が生成されない", "MRPタイプ ND（計画なし）／手配タイプ空／純所要量が 0",
     "MM03 MRP1〜2 → MD04 の利用可能数量 → MD01N の実行ログ"),
    ("2", "PIR を登録したのに MD04 に出ない", "版が 00 でない／納入日が表示期間外／プラント在庫ビュー無し",
     "SE16N: PBED（VERID/PDATU）・T459U・MM03 プラント在庫"),
    ("3", "受注が MD04 に出ない（需要が立たない）", "納入日程行カテゴリの所要量転送 OFF（VBEP-BEDSD 空）／品目に MRP ビュー無し",
     "VA03 納入日程行・VOV6・VOV5・SE16N: TVEP"),
    ("4", "受注の確認済数量が 0", "在庫確認 OFF（VBEP-ATPPR）／品目 MRP3 の在庫確認が空／スコープに在庫・入庫予定が無い",
     "CO09・OVZ9・MM03 MRP3・OVZ2"),
    ("5", "受注しても PIR が消費されない", "戦略グループ 10/11 系（消費しない）／消費期間外／戦略グループ空",
     "MM03 MRP3・MD04 の消費明細・OPPT"),
    ("6", "完成品の入庫が得意先別（受注在庫）になる", "MRP4 が個別所要量のみ／指図が受注に紐づいている",
     "MM03 MRP4・CO03・SE16N: AFPO-KDAUF/KDPOS・MMBE/MSKA"),
    ("7", "VOV4/VOV5 の自建行が効かない", "品目マスタの戦略グループが優先される／OVZI の決定順の理解不足",
     "MM03 MRP3・OVZI・VA03 の明細/納入日程行"),
    ("8", "MD05/MD06 に MRP リストが出ない", "MRP Live（MD01N）は MRP リストを作らない",
     "MD04 で確認（SAP KBA 2640393）"),
    ("9", "差異計算で「目標原価がありません」", "標準価格が未リリース（CK24 未完）／原価計算バリアント未設定／レート（KP26）無し",
     "MM03 会計1（MBEW-STPRS）・CK13N・KP26・OKKN"),
    ("10", "差異が大きいのに原因が分からない", "実績時間の入力ミス／部品の実際単価／スクラップ未記録／残差（設定漏れ）",
     "KKS2 のカテゴリ別内訳・AFRU・MATDOC・OKV1/OKVW/OKVG"),
    ("11", "決済しても FI に何も出ない", "差異計算未実施／決済ルール未設定（COBRB）／会計期間閉鎖",
     "KKS1 → KO88 のログ・FB03・決済プロファイル・OB52"),
    ("12", "在庫があるのに出荷（PGI）できない", "引当未実施（ピッキング数量 0）／在庫タイプ違い／別受注が先取り／保管場所違い",
     "VL03N の在庫/引当・MMBE の区分別在庫・CO09・MB52"),
]

GLOSSARY = [
    ("見込生産（MTS / Make-to-Stock）", "予測で作り、在庫から納める生産形態", "計画独立所要量（PIR）が需要源。完成品は自由在庫へ"),
    ("受注生産（MTO）", "受注ごとに作る生産形態", "戦略 20、受注在庫（特別在庫 E）、所要量クラス 040 系"),
    ("受注設計生産（ETO）", "受注ごとに設計から作る形態", "WBS・プロジェクト在庫 Q。姉妹站 sapeto を参照"),
    ("計画独立所要量（PIR）", "需要予測をシステムに登録した需求行", "MD61/MD62/MD63/MD73、表 PBIM/PBED/PBHI、有効版 00（T459U）"),
    ("消費（Consumption）", "受注が出荷/所要量として PIR を食べること", "MD04 上で起き、PBED の数量は変わらない"),
    ("消減（Reduction）", "PIR の数量そのものが減ること", "入庫（101）・生産/購買の完結時など"),
    ("戦略グループ", "需要の扱い方をまとめた品目項目（MRP3）", "10/11/30/40/70（標準）。OPPT/OPPS で確認"),
    ("消費モード", "消費の方向（逆/順）と期間の設定", "MARC-VRMOD（1 逆のみ/2 逆+順/3 順のみ/4 順+逆）、VINT1/VINT2"),
    ("自由在庫", "誰でも使える在庫（利用可能在庫）", "MARD/MCHB。MTS の完成品はここに入る（特在区分 空）"),
    ("受注在庫（特別在庫 E）", "特定の受注に紐づいた在庫", "MSKA。MTO の完成品が入る"),
    ("MRP タイプ / ロットサイズ / 手配タイプ", "MRP の基本制御（MRP1）", "PD（MRP 対象）/ EX（ロット単位）/ E（内製）が MTS の典型"),
    ("計画手配（Planned Order）", "MRP が作る補貨提案", "PLAF。在庫区分は空（MTS）、CO40/CO41 で製造指図に変換"),
    ("純所要量（正味所要量）", "MRP の計算結果", "総所要量 − 入庫予定（在庫＋入庫予定）＋ 安全在庫"),
    ("所要量転送", "受注を MRP の需求として渡すスイッチ", "納入日程行カテゴリ（TVEP-BEDSD / VOV6）"),
    ("在庫確認（ATP）", "利用可能在庫数量に対する確認", "CO09/MDVP/V_V2。品目 MRP3 のチェックルール＋スコープ（OVZ9）"),
    ("標準原価（標準価格）", "在庫評価の基準価格", "CK11N → CK40N → CK24（マーク/リリース）、MBEW-STPRS"),
    ("差異（Variance）", "目標原価（標準 × 出来高）と実際原価の差", "KKS1/KKS2 で計算。カテゴリ別（入力価格/入力数量/資源使用/混合価格/出力価格/スクラップ/残差）"),
    ("決済（Settlement）", "差異と WIP を FI に転記する処理", "KO88（単品目）/ CO88（一括）"),
    ("移動タイプ 261 / 101 / 601", "在庫の動きの種類", "261 = 指図への部品出庫 / 101 = 指図・発注への入庫 / 601 = 出荷の出庫確認（PGI）"),
    ("Public Cloud（S/4HANA Cloud）", "SaaS 版の SAP。設定は SSCUI、操作は Fiori", "明細カテゴリ/販売伝票タイプの新規作成不可。スコープアイテム BJ5 等"),
]

SOURCES = [
    ("戦略 10/11/30/40/70 の説明と所要量タイプ・所要量クラス",
     "SAP Tribal Knowledge「SAP Planning Strategies」（OPPT/OPPS/OVZH/OVZG の対応表）",
     "saptribalknowledge.wordpress.com/2017/06/13/sap-planning-strategies/"),
    ("戦略 10 は受注が消費しない／戦略 11 は在庫を見ない（混合MRP区分 2）",
     "SAP PRESS blog「4 Strategies for Make-to-Stock Production with SAP S/4HANA」",
     "blog.sap-press.com/4-strategies-for-make-to-stock-production-with-sap-s4hana"),
    ("MRP 方針一覧（10 見込生産／11 総所要量計画／30 ロット生産／40 最終組立ありの計画／70 組立品目レベル）",
     "SAP Help（Support Content）「MRP 方針 (PP-MRP)」",
     "help.sap.com/docs/SUPPORT_CONTENT/mrp/3138697884.html"),
    ("PIR の表（PBIM/PBED/PBHI・有効版 T459U）と消費/消減の違い",
     "SAP Help（Support Content）「Tables and programs of planned independent requirements」",
     "help.sap.com/docs/SUPPORT_CONTENT/erpman/3138697931.html"),
    ("関連表とカスタマイズ（MARA/MARC/MARD/MDTB/PLAF/PBED/RESB/AFKO/AFPO・OPPS/OPPT/OVZG/OVZH/OVZI/OMDU）",
     "SAP Help（Support Content）「Frequently used database tables and customizing in MRP」",
     "help.sap.com/docs/SUPPORT_CONTENT/mrp/3138698280.html"),
    ("MRP Live（MD01N）と古典 MRP の差異：MRP リストを作らない・MD03 は提供されない",
     "SAP KBA 2640393 / SAP Note 1914010", "me.sap.com/notes/2640393"),
    ("納入日程行カテゴリ CP の内容（所要量転送・在庫確認・移動タイプ 601）と VOV5 の決定キー",
     "SAP Community「Schedule line category CP」「Link between MRP type and schedule line category」",
     "community.sap.com（qaq のスレッド）"),
    ("差異カテゴリ（入力価格/入力数量/資源使用/混合価格/出力価格/スクラップ/残差）",
     "SAP Help「Variance Categories」（S/4HANA On-Premise CO-PC）・SAP Learning「Performing Variance Calculation」",
     "help.sap.com/docs/SAP_S4HANA_ON-PREMISE/5e23dc8fe9be4fd496f8ab556667ea05/c4324152fe4eaa1ae10000000a445394.html"),
    ("差異キー/差異計算バリアント（OKV1/OKVW/OKVG）と期末処理の順序（KKS1/KKAO/CO88）",
     "SAP Community「Variance calculation_PP」「CO Product Costing – Period End Closing」",
     "community.sap.com（qaq / blog のスレッド）"),
    ("在庫区分と数量表（自由在庫 MARD/MCHB・受注在庫 MSKA・プロジェクト在庫 MSPR）",
     "SAP Help「Stock Tables and Stock Types」", "help.sap.com/docs/SUPPORT_CONTENT/…/Stock Tables and Stock Types"),
    ("ATP（利用可能在庫数量）と在庫確認の制御（品目 MRP3 のチェックルール・OVZ9 のスコープ）",
     "SAP Help「Availability Check」「Availability Check According to ATP Logic」・tokulog「ATP利用可能在庫確認について徹底解説！」",
     "help.sap.com/docs/SAP_S4HANA_ON-PREMISE/…/Availability Check ・ tokulog.org/blog/atp/"),
    ("消費モードの値（1 逆のみ/2 逆+順/3 順のみ/4 順+逆）と期間フィールド（VINT1/VINT2）",
     "SAP Datasheet（T438M）・LeanX（LES_SHP_ATP_MAT の VRMOD/VINT1/VINT2）",
     "sapdatasheet.org/abap/tabl/t438m.html ・ leanx.eu/sap/table/les_shp_atp_mat"),
    ("Cloud：スコープアイテム BJ5（Make-to-Stock Production – Discrete Manufacturing）",
     "SAP Best Practices for SAP S/4HANA Cloud Public Edition",
     "help.sap.com/docs/s4hana-cloud-best-practices/make-to-stock-production-discrete-manufacturing-bj5-ae/purpose"),
    ("Cloud：SSCUI 105120（明細カテゴリ別の所要量タイプ決定）・スコープアイテム BJ8/J44",
     "SAP Help / 製造スコープアイテム一覧（Best Practices）",
     "help.sap.com（SSCUI 一覧は SAP for Me の Configuration ライブラリ）"),
    ("納入日程行カテゴリ・明細カテゴリの IMG パス（VOV7/VOV4/VOV6/VOV5）",
     "SAP SD IMG（Sales and Distribution > Sales > Sales Documents > …）・各チュートリアル",
     "IMG: 販売管理 > 販売伝票 > 販売伝票明細 / 納入日程行"),
    ("指図タイプと指図タイプ依存パラメータ（OPJH / OPL8）",
     "SAP PP IMG（Production > Shop Floor Control > Master Data > Order）",
     "IMG: 生産 > ショップフロア制御 > マスタデータ > 指図"),
]

CHECKS = [
    ("P1", "概念", "MTS と MTO の分水嶺（需要の起点・在庫の帰属）を一言で説明できる", "□", ""),
    ("P1", "概念", "戦略 10/11/30/40/70 の違いを、自分のシステムの OPPT の記述を根拠に説明できる", "□", ""),
    ("P1", "概念", "消費と消減の違いを、MD04 と PBED の観察で説明できる", "□", ""),
    ("P2", "配置 C0〜C16", "C0 C0 の前提（販売エリア・得意先・番号範囲・権限）を確認した", "□", ""),
    ("P2", "配置 C0〜C16", "C2 品目 ZMTS-FG01 の MRP1〜4（特に戦略 40・個別/包括所要量 空）を確認した", "□", ""),
    ("P2", "配置 C0〜C16", "C4 標準価格 8,000 JPY が MM03 会計1 に出る（マーク・リリース済み）", "□", ""),
    ("P2", "配置 C0〜C16", "C6〜C9 TAN/CP と VOV4/VOV5/VOV6 の設定値を確認した", "□", ""),
    ("P2", "配置 C0〜C16", "C10/C11 所要量クラス（個別在庫なし）と所要量タイプ（VSF/KSV）を確認した", "□", ""),
    ("P2", "配置 C0〜C16", "C13 ATP のスコープ（在庫・入庫予定・出庫予定）を CO09 で確認した", "□", ""),
    ("P2", "配置 C0〜C16", "C16 Cloud の場合、スコープアイテムと作れないオブジェクトを確認した", "□", ""),
    ("P3", "練習①〜⑤", "① 版 00 の PIR を登録し、MD04 の独立所要量（受注番号なし）を確認した", "□", ""),
    ("P3", "練習①〜⑤", "② MD01N 後に計画手配が出て、純所要量を検算できた", "□", ""),
    ("P3", "練習①〜⑤", "② CO40/CO41 で指図（PP01）に変換し、AFPO-KDAUF/KDPOS が空であることを確認した", "□", ""),
    ("P3", "練習①〜⑤", "③ 261 → CO11N → 101 を通し、自由在庫 +500 PC・特在空を確認した", "□", ""),
    ("P3", "練習①〜⑤", "④ 受注 200 PC で CO09 の可用量が 500 → 300 に変わった", "□", ""),
    ("P3", "練習①〜⑤", "④ MD04 の消費済 200 と PBED の数量不変を確認した", "□", ""),
    ("P3", "練習①〜⑤", "④ PGI 601 で自由在庫 300、請求 1,600,000 JPY、伝票フロー閉合を確認した", "□", ""),
    ("P3", "練習①〜⑤", "⑤ KKS2/KKS1 で差異（カテゴリ別）を計算し、KO88/CO88 で決済した", "□", ""),
    ("P3", "練習①〜⑤", "⑤ 棚卸（MI01→MI04→MI07）を 1 回通した", "□", ""),
    ("P4", "故障対応", "故障対照表 12 項のうち 3 項以上を、症状→根因→確認手順で説明できる", "□", ""),
    ("P4", "故障対応", "「3 層モデル（品目マスタ／SD の 3 決定／実行結果）」で切り分けられる", "□", ""),
    ("P5", "テスト", "能力测试で 21/28（75%）以上を取った", "□", ""),
    ("P5", "テスト", "発展課題（handson-5 5-8）を 2 つ以上実行した", "□", ""),
]

GUIDE = [
    ("時間割（2 日）", "Day1 午前：概念（150 分）／Day1 午後：配置 C0〜C16（150 分）／Day2 午前：練習①②（120 分）／"
                  "Day2 午後：練習③④（180 分）／Day2 最後：練習⑤＋テスト（60 分）"),
    ("時間割（1 日）", "午前：概念（90 分）＋配置（120 分、確認中心）／午後：練習①②（90 分）・練習③（60 分）・練習④（60 分）・⑤とテスト（45 分）"),
    ("時間割（半日）", "概念（45 分）＋練習①（30 分）＋練習③（45 分）＋練習④（45 分）＋解説（15 分）。配置は講師デモのみ"),
    ("削ってよい順", "配置詳細 → 練習⑤ → 練習①。削ってはいけないのは練習③（自由在庫への入庫）と練習④（PIR の消費）"),
    ("必ず実機で", "講師が画面を写して説明するだけの研修は、版本差・業界ソリューション差で必ず破綻する。受講者に必ず T-code を打たせる"),
    ("採点の原則", "「自システムで確認できたか」を評価し、「教科書の値を暗記したか」は評価しない。値が違う場合は理由を説明できれば満点"),
    ("配点例（100 点）", "C2 品目主数据 20／C6〜C9 SD 側 3 決定 20／C10〜C12 所要量クラス・タイプ・戦略 20／C13〜C15 ATP・MRP・出荷請求 20／"
                    "C0・C1・C3・C4・C16 前提・原価・Cloud 20"),
    ("減点ポイント", "値の丸暗記（根拠が言えない）／確認手順の省略／エラーを「なんとなく直した」"),
    ("必出 Q&A（抜粋）", "① MTS と MTO の違い ② なぜ MRP4 は空か ③ 戦略 40 と 10 の違い ④ 30 と 40 の違い ⑤ 消費と消減 ⑥ PIR を入れたのに MRP が動かない "
                    "⑦ 受注が MD04 に出ない ⑧ 在庫があるのに出荷できない ⑨ 差異は誰の責任か ⑩ MRP リストはどこ ⑪ Cloud でも同じ手順か ⑫ 安全在庫の意味 "
                    "（模範回答は instructor.html の #qa を参照）"),
    ("故障の教え方", "症状を読み上げ→「品目マスタ／SD の 3 決定／実行結果」のどの層かを当てさせる→層の中で T-code を挙げさせる。"
                 "講師が先に答えの T-code を言ってはいけない"),
    ("評価基準", "① 機制の理解（概念）40% ② 実機の操作 35% ③ 故障対応（切り分け）25%。"
             "テスト 75% 以上＋練習①〜⑤ の验收全項目＋ワークシート全欄記入で「自走できる」判定"),
    ("発展の導線", "形態比較（sapmto/sapeto）→ PP/DS・aATP → 需要計画（IBP/S&OP）→ Material Ledger・実際原価計算 → Cloud 実装（BJ5/SSCUI）"),
    ("講師の心得", "受講者が「自分のシステムでは値が違う」と言ったら最高の瞬間。標準値の暗記より、自分の環境で確認する方法を持ち帰らせる"),
]


def main():
    wb = Workbook()
    wb.remove(wb.active)

    ws = wb.create_sheet("0_概要")
    kv(ws, "SD 見込生産（MTS）要件定義・手順書", "SAP S/4HANA 見込生産（Make-to-Stock）实战训练站 / sapmts の Excel 版成果物",
       SUMMARY, [22, 150])

    ws = wb.create_sheet("1_環境・前提")
    table(ws, "環境・前提", "実習前に 30 分で確認する項目（自システムでの確認方法つき）",
          ["#", "項目", "本教材の値", "確認方法"], ENV, [6, 30, 52, 60])

    ws = wb.create_sheet("2_設定一覧")
    table(ws, "設定一覧（C1〜C17）", "標準値の「通常の情況」＋本教材の練習値＋確認場所。標準値は版本・業界ソリューション・既有改造で異なる",
          ["#", "設定項目", "標準値の通常情況", "本教材の練習値", "設定／確認處"], SETTINGS, [7, 30, 62, 40, 46])

    ws = wb.create_sheet("3_配置手順")
    table(ws, "配置手順（C0〜C16）", "各 STEP = 目的 / T-code / 入力値 / 手順 / 確認（自システムでの確認方法）/ つまずき",
          ["STEP", "目的", "T-code", "入力値", "手順", "確認（自システム）", "つまずき"],
          CONFIG_STEPS, [8, 26, 26, 60, 60, 52, 48])

    ws = wb.create_sheet("4_練習手順")
    table(ws, "練習手順（練習①〜⑤）", "実機オペレーション。各練習に期待結果とつまずきを添付",
          ["練習", "テーマ", "T-code", "入力値", "手順", "期待結果", "つまずき"],
          PRACTICE, [7, 30, 30, 54, 62, 56, 46])

    ws = wb.create_sheet("5_期待結果・検証")
    table(ws, "期待結果・検証", "「証跡で」確認する 18 項目。実機验收清单の Excel 版",
          ["#", "対象", "期待結果", "確認方法"], EXPECT, [5, 16, 78, 48])

    ws = wb.create_sheet("6_故障対照表")
    table(ws, "故障対照表（12 項）", "症状から引く。覚えるのではなく、確認手順を実行できることが目標",
          ["#", "症状", "根因の候補", "確認手順（T-code / 表）"], TROUBLE, [5, 40, 56, 56])

    ws = wb.create_sheet("7_用語集")
    table(ws, "用語集（日中対照）", "本教材で使う用語。日本語／英語の SAP 用語と中国語の説明",
          ["用語（日／英）", "中国語の説明", "補足（T-code・表・要点）"], GLOSSARY, [34, 38, 56])

    ws = wb.create_sheet("8_出典")
    table(ws, "出典", "本教材の数値・記述の根拠。SAP Help / SAP Note・KBA / SAP Community / SAP Learning / 第三者ブログ",
          ["主題", "出典", "参照先"], SOURCES, [52, 62, 60])

    ws = wb.create_sheet("9_受講者チェックリスト")
    table(ws, "受講者チェックリスト", "修了判定：全項目に□が付き、証跡（T-code・伝票番号・表の行）を記入できること",
          ["フェーズ", "区分", "確認項目", "□", "証跡（記入欄）"], CHECKS, [8, 16, 76, 5, 40])

    ws = wb.create_sheet("10_講師用ガイド")
    table(ws, "講師用ガイド", "進め方・採点・教え方。受講者には配布しない（或は最後に解答編として配布）",
          ["項目", "內容"], GUIDE, [22, 130])

    wb.save(OUT)
    print("saved:", OUT)
    print("sheets:", wb.sheetnames)


if __name__ == "__main__":
    main()
