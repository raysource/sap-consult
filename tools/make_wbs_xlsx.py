#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
学習WBS（受講者版）Excel 生成器 — SAP 培训站系列共通

每个站生成一个「打勾式进度表」：WBS 行 = 该站实际页面上的 STEP / 验收清单条目
（从 HTML 抽取，保证与站点内容一致，不凭记忆编造），加上手写的 実機記録 / 修了判定。

用法:
    python3 tools/make_wbs_xlsx.py            # 全站（存在的站点だけ）
    python3 tools/make_wbs_xlsx.py sapmto     # 単站

出力: <site>/<SITE>_学習WBS_受講者版.xlsx  （5 シート）
  0_進め方 / 1_学習WBS / 2_進捗サマリ / 3_実機記録 / 4_修了判定
"""
import os
import re
import sys
import glob
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

BLUE, GREY, INK = "0A6ED1", "F2F4F7", "1D2D3E"
GREEN = "E8F5E9"
F_TITLE = Font(name="微软雅黑", size=15, bold=True, color="FFFFFF")
F_SMALL = Font(name="微软雅黑", size=9, color="6B7A8D")
F_HEAD = Font(name="微软雅黑", size=10, bold=True, color="FFFFFF")
F_BODY = Font(name="微软雅黑", size=10, color=INK)
F_BOLD = Font(name="微软雅黑", size=10, bold=True, color=INK)
FILL_TITLE = PatternFill("solid", fgColor=BLUE)
FILL_HEAD = PatternFill("solid", fgColor=BLUE)
FILL_ALT = PatternFill("solid", fgColor=GREY)
FILL_IN = PatternFill("solid", fgColor=GREEN)
THIN = Side(style="thin", color="C9D6E0")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP = Alignment(wrap_text=True, vertical="top")
CENTER = Alignment(wrap_text=True, vertical="center", horizontal="center")

# ----------------------------------------------------------------------------
# サイト定義（フェーズの手書き部分 + 抽出の対象ページ）
# ----------------------------------------------------------------------------
SITES = {
    "sapmto": dict(
        label="SD 受注生産（MTO）",
        code="MTO",
        intro=[
            ("本ワークブックの使い方",
             "左の「1_学習WBS」を上から順に実施し、各タスクの「完成基準」を満たしたら自己判定に ○ を入れてください。"
             "○ が付いた行数は「2_進捗サマリ」に自動集計されます。詰まった行は必ず「メモ」に症状を残し、講師と共有してください。"),
            ("目安時間",
             "配置（C0〜C16）と練習①〜⑤の目安は各行に記載しています。全体は「講義 1 日 ＋ 実機 2 日」程度を想定しています。"),
            ("記入のルール",
             "自己判定は ○（できた）/ △（一部できた・要確認）/ ×（できなかった）の 3 段階。△ と × は「4_修了判定」の再受講分野に転記します。"),
        ],
        overview_checks=[
            ("本站の環境と前提を説明できる", "得意先 1000 / プラント / 品目が利用可能で、SD・PP・MM の基本設定が生きていることを確認した"),
            ("端到端 10 ステップの流れを白紙に書ける", "受注 → 需要 → MRP → 指図 → 入庫 → 出荷 → 請求 → 月末 の順序を、在庫区分（特在 E）と併せて説明できる"),
            ("設定対象 17 項（C1〜C17）を一覧できる", "どの設定が何を決めるかを、決定链（品目 → VOV4 → 明細カテゴリ → VOV5 → 納入日程行カテゴリ → 所要量タイプ → 所要量クラス → 個別在庫 E）の上で位置づけられる"),
        ],
        concept_checks=[
            ("受注生産の決定链を白紙に書ける", "品目 → VOV4 → 明細カテゴリ → VOV5 → 納入日程行カテゴリ → 所要量タイプ → 所要量クラス → 個別在庫 E を、キー（販売組織・明細カテゴリグループなど）付きで言える"),
            ("個別在庫 E と特在テーブルを説明できる", "特在 E が受注明細に帰属し、数量が MSKA（および MMBE の特別在庫欄）に出ることを説明できる"),
            ("戦略 20 と 82（組立処理）の違いを説明できる", "82 は受注保存と同時に指図が 1:1 で作られる（所要量タイプ KMFA・所要量クラス 201・指図タイプ PP04）と説明できる"),
            ("受注在庫と財務の関係を説明できる", "出荷（PGI）時点で在庫が落ち、売上原価が計上されること、指図の差異が決済でどこへ行くかを説明できる"),
            ("主要テーブルの役割を言える", "VBAK / VBAP / VBEP / VBBS / MSKA / PLAF / AFPO / MATDOC のうち 5 つ以上を、どの情報を持つかで説明できる"),
        ],
        config_check_texts={},   # HTML から抽出（各ステップの確認欄）
        hands_on_extra=[
            ("発展①：戦略 82 で受注組立を試す", "受注を保存した瞬間に指図が作られることを、COOIS / CO03 で確認した"),
            ("発展②：明細カテゴリを ZTAK から標準に切り替えて挙動を比べる", "切替後に MD04 / MMBE の見え方がどう変わるかを記録した"),
        ],
        records=[
            ("受注番号（VA01）", "練習①で 1 件"),
            ("MD04 の得意先所要量", "受注数量と一致（受注番号付き）"),
            ("受注在庫 E の数量（MMBE / MSKA）", "受注数量（入庫前は 0、入庫後は受注数量）"),
            ("CO09 の可用量 / 不足", "不足が受注数量と一致（在庫 0 の場合）"),
            ("計画手配番号（MD04）", "MRP 実行後に生成される"),
            ("製造指図番号（CO08 / CO40）", "計画手配から変換 or 作成"),
            ("部品出庫（261）の数量", "BOM 所要量どおり"),
            ("完成品入庫（101）の数量", "受注数量"),
            ("出荷伝票番号（VL01N）", "数量 = 入庫数量"),
            ("請求書番号（VF01）", "金額 = 受注金額"),
            ("指図の差異額（KKS1 / KO88）", "標準原価との差異（±を記録）"),
            ("伝票フロー（VA03）に揃った伝票", "受注 → 指図 → 入庫 → 出庫 → 出荷 → 請求 の 6 種"),
        ],
        finish_checks=[
            "設定（C0〜C16）を、講師の指示なしで 1 人でやり切った",
            "練習①〜④ を通して、伝票フローが受注から請求まで一本に繋がった",
            "MD04 の「得意先所要量」と「受注在庫（MMBE）」の関係を、人に説明できた",
            "入庫が自由在庫ではなく受注在庫（特在 E）に入る理由を説明できた",
            "つまずいた点を「症状 → 根因 → 証拠 → 処置 → 再発防止」で 1 件以上記録できた",
            "能力测试（quiz.html）で 75% 以上（28 題中 21 問以上）",
        ],
    ),
    "sapeto": dict(
        label="受注設計生産（ETO）",
        code="ETO",
        intro=[
            ("本ワークブックの使い方",
             "MTO（sapmto）を先に終えてから着手してください。ETO は「案件の器（WBS）」を先に作り、受注・需要・原価・収益をそこへ集める設計です。"
             "各タスクの「完成基準」を満たしたら自己判定に ○ を入れ、○ の数は「2_進捗サマリ」に自動集計されます。"),
            ("目安時間",
             "配置（C0〜C16）＋練習①〜⑤で「講義 1 日 ＋ 実機 2〜3 日」程度。月末処理（進捗 → 結果分析 → 決済）は特に時間がかかります。"),
            ("特に注意",
             "プロジェクト在庫 Q が成立していないと、以降のすべて（入庫先・評価・決済・帳票）が崩れます。"
             "まず「4 点セット」——① 評価付プロジェクト在庫 ② MRP4 個別所要量 ③ 戦略グループ（評価区分 M）④ 受注明細の WBS ——を揃えてください。"),
        ],
        overview_checks=[
            ("本站の環境と前提を説明できる", "プロジェクトプロファイル・WBS の勘定設定・PS の権限が利用可能であることを確認した"),
            ("受注設計生産の流れを白紙に書ける", "プロジェクト（WBS）→ 受注（WBS 割当）→ 計画・予算 → MRP → 指図・ネットワーク → 入庫（Q）→ 出荷 → 請求 → 進捗 → 結果分析 → 決済 を順に説明できる"),
            ("E（受注在庫）と Q（プロジェクト在庫）の違いを 4 点で言える", "需要の帰属 / 在庫テーブル（MSKA vs MSPR）/ 成本の対象（指図 vs WBS）/ 請求と月末処理"),
        ],
        concept_checks=[
            ("E と Q の 4 点セットを、それぞれ資料を見ずに言える", "E: MRP4 個別所要量・所要量クラス・明細カテゴリの特別在庫 E・戦略グループ / Q: 評価付プロジェクト在庫・MRP4 個別所要量・戦略グループ（評価区分 M）・受注明細の WBS"),
            ("WBS の 3 つの役割を説明できる", "構造要素（入れ子）/ 勘定設定要素（原価を受け取る）/ 請求要素（収益を立てる）を、違いを踏まえて説明できる"),
            ("プロジェクト在庫 Q の成立条件を説明できる", "SAP Help の「評価付プロジェクト在庫」3 前提と、所要量クラスの評価区分 M の役割を説明できる"),
            ("請求方式の選択肢を比較できる", "出荷ベース / 請求計画（日付・出来高）/ マイルストーン請求 / RRB（DP90・DP91）を、契約との対応で説明できる"),
            ("月末処理の順序を言える", "進捗 → 結果分析（KKA2/KKAJ）→ WIP（KKAX）→ 決済（CJ88/CJ8G）の順序と、各ステップで何が変わるかを説明できる"),
            ("主要テーブルと T-code を対応付けられる", "PROJ / PRPS / AUFK / AFPO / MSPR / COEP / VBFA と、CJ20N / CJI3 / CJ31 / CJIC / KKA2 の対応"),
        ],
        config_check_texts={},
        hands_on_extra=[
            ("発展①：進捗を入力して結果分析を回す", "CNE1 で進捗率を入れ、KKA2 で認識収益・WIP が動いたことを KKAX で確認した"),
            ("発展②：出来高（マイルストーン）で 30%/70% を請求する", "請求計画の 2 行から VF01 で 2 枚の請求書を作り、収益が請求要素の WBS に立つことを CJI3 で確認した"),
            ("発展③：決済を実行して WBS の実績を締める", "CJ88 / KO88 / VA88 のうち該当するものを実行し、決済明細（CJIC）で振替先を確認した"),
            ("発展④：予算超過時の可用性管理の挙動を確かめる", "CJBV で警告/エラーが出ることを確認し、許容範囲の設定箇所を記録した"),
        ],
        records=[
            ("プロジェクト定義 ID（CJ20N）", "例 ZETO-1000"),
            ("WBS 要素（請求要素 / 勘定設定要素）", "3 件（.1 請求要素、.2/.3 勘定設定要素）"),
            ("ネットワーク番号（CN21）", "活動 2 件以上"),
            ("受注番号（VA01 ＋ 明細 WBS）", "明細に WBS が入っていること"),
            ("計画手配の勘定設定 / 在庫区分（MD04）", "勘定設定 = WBS、在庫区分 = Q"),
            ("製造指図番号（CO40 / CO08）", "勘定設定 = WBS（AUFK-PS_PSP_PNR）"),
            ("プロジェクト在庫 Q の数量（MMBE / MSPR）", "入庫で受注数量、出荷で 0"),
            ("出荷伝票番号（VL01N）＋ PGI", "在庫区分 Q、移動タイプ 601"),
            ("請求書番号（VF01 / 請求計画）", "30% / 70% の 2 枚（または出荷ベース 1 枚）"),
            ("CJI3 の収益（請求要素へ）", "請求金額と一致"),
            ("CJI3 の原価（勘定設定要素へ）", "材料費・労務費など"),
            ("予算と実績（CJ31 / CJI3）", "元予算・予算・実績・可用残"),
            ("進捗率と結果分析（CNE1 / KKA2 / KKAX）", "認識収益 / WIP の金額"),
            ("決済（CJ88 / KO88 / VA88）と CJIC", "振替先（差異・WIP・原価）を記録"),
            ("伝票フロー（VA03）に揃った伝票", "受注 → 指図 → 入庫 → 出庫 → 出荷 → 請求 → 会計 の連鎖"),
        ],
        finish_checks=[
            "4 点セットを自分で揃え、Q の在庫が MSPR に出ることを確認した",
            "受注明細に WBS を割り当て、収益が請求要素に立つことを CJI3 で確認した",
            "月末処理（進捗 → 結果分析 → WIP → 決済）を 1 回通した",
            "E と Q の対照表（scenario-eq）を見ずに、相違点を 5 点説明できた",
            "予算と可用性管理の挙動（警告 / エラー）を実際に見た",
            "つまずいた点を「症状 → 根因 → 証拠 → 処置 → 再発防止」で 1 件以上記録できた",
            "能力测试（quiz.html）で 75% 以上（28 題中 21 問以上）",
        ],
    ),
    "saporderflow": dict(
        label="受注形態の横断比較（講義）",
        code="CMP",
        intro=[
            ("本ワークブックの使い方",
             "本站は実機の手顺ではなく「比較と判断」の講義教材です。WBS は各ページの見出し単位で並んでいます。"
             "読むだけでなく、各項目を「自分の言葉で説明できるか」で判定してください（説明できない項目は △ か ×）。"),
            ("目安時間",
             "講義 90 分（速習）〜 180 分（デモ付き）。4〜5 時間版は sapmto と sapeto の実機を挟みます。"),
            ("到達点",
             "5 形態を「計画起点・库存区分・成本対象・請求方式」で言い分けられること、そして E と Q の 4 点セットを暗唱できること。"),
        ],
        overview_checks=[
            ("5 形態を 1 行ずつ説明できる", "MTS / MTO / ETO / ATO / VC を、計画起点と库存区分で説明できる"),
            ("選型判断の 3 つの問いを使える", "①受注の前に作るか ②案件単位で原価・収益を管理するか ③顧客が仕様を選ぶか、の順で形態を絞れる"),
            ("両实训站との関係を説明できる", "本サイトで判断し、実機は ../sapmto/（E）と ../sapeto/（Q）で通す、という役割分担を説明できる"),
        ],
        concept_checks=[],
        pages=[
            ("B 横断比較", "compare", [
                ("9 维度 × 5 形態マトリクスを上から読める",
                 "計画起点 → 库存区分 → 需要の単位 → 調達/製造 → 成本の対象 → 請求方式 → 収益認識 の因果を、1 本の線で説明できる"),
                ("戦略グループ早見表を使える",
                 "10 / 20 / 25 / 82 / E2 と、所要量タイプ（KE / KEK / KMFA / E21）・所要量クラス（040 系 / 046 / 201）を対応付けられる"),
                ("在庫テーブル早見表を使える",
                 "MARD（自由）/ MSKA（E）/ MSPR（Q）/ MSKU（預託）を即答できる"),
                ("明細カテゴリグループの用途を言える",
                 "0001 / 0002 / 0004 / ERLA / DIEN を、業務との結び付きで説明できる"),
                ("E と Q の 4 点セットを暗唱できる",
                 "E: MRP4 個別所要量・所要量クラス・明細カテゴリの特別在庫 E・戦略グループ / Q: 評価付プロジェクト在庫・MRP4 個別所要量・戦略グループ（評価区分 M）・受注明細の WBS"),
                ("設定を取り違えたときの症状を言える",
                 "明細カテゴリの設定ミス / 評価付フラグ漏れ / 戦略グループの不一致 の 3 症状を、確認手顺付きで説明できる"),
            ]),
            ("C E vs Q 対照実習", "scenario-eq", [
                ("STEP 対照表（0〜12）を通読した",
                 "計画手配・101 の入庫先・月末処理・帳票の 4 点で差が出る、と自分の言葉でまとめた"),
                ("一致点を 6 つ挙げられる",
                 "操作系（VA01 / MD04 / VL01N / VF01 / 261・101・601）はほぼ同一、と説明できる"),
                ("判別演習 8 問を解いた",
                 "解答と根拠（なぜそう判断したか）を講師の前で言えた"),
                ("30 分×2 の最小実機を 1 回ずつ走らせた",
                 "E と Q の両方で、入庫先の在庫テーブルが違うことを画面で確認した（任意だが強く推奨）"),
            ]),
            ("D VC 概観", "vc", [
                ("VC が「生産形態ではなく構成エンジン」であると説明できる",
                 "在庫区分と戦略は別途決める（VC × 25 / 82 / ETO）と説明できる"),
                ("VC の構成要素 6 つを言える",
                 "特徴 / クラス / KMAT / 依存関係 / 設定プロファイル / シミュレーション と、その T-code"),
                ("典型故障 7 項を、症状から原因を引ける",
                 "構成が出ない / BOM が切り替わらない / 変種価格が出ない などを、確認 T-code 付きで説明できる"),
            ]),
        ],
        records=[
            ("MTO を走らせた証跡（受注番号）", "在庫区分 E・MSKA に行があること"),
            ("ETO を走らせた証跡（プロジェクト定義）", "在庫区分 Q・MSPR に行があること"),
            ("両方の入庫（101）の比較メモ", "101 の後、在庫がどこに入ったか（MSKA と MSPR）"),
            ("判別演習 8 問のスコア", "8 問中 ___ 問"),
            ("能力测试 20 題のスコア", "20 題中 15 問以上（75%）"),
        ],
        finish_checks=[
            "5 形態を「計画起点・库存区分・成本対象・請求方式」で言い分けられる",
            "E の 4 点セットと Q の 4 点セットを、資料を見ずに言える",
            "在庫テーブル（MARD / MSKA / MSPR）を即答できる",
            "「CJI3 に収益が出ない」「入庫が自由在庫に入る」を 2 分で切り分けられる",
            "VC が「生産形態ではなく構成エンジン」であることを説明できる",
            "能力测试（quiz.html）で 75% 以上（20 題中 15 問以上）",
        ],
    ),
    "sapmts": dict(
        label="SD 見込生産（MTS）",
        code="MTS",
        intro=[
            ("本ワークブックの使い方",
             "本站は「予測で作り、在庫から納める」見込生産です。MTO（sapmto）と対比しながら進めると、"
             "「自由在庫 vs 受注在庫」「PIR vs 受注」「差異計算 vs 案件の進捗」の違いが腹に落ちます。"),
            ("目安時間", "配置（C0〜C16）＋練習①〜⑤で「講義 1 日 ＋ 実機 1〜2 日」程度。"),
            ("特に注意", "PIR（MD61）と安全在庫の設定が需要を作ります。需要が無ければ MRP は何も作りません。まず MD04 で需要の正体（PIR か受注か）を読む習慣を付けてください。"),
        ],
        overview_checks=[
            ("本站の環境と前提を説明できる", "得意先 1000 / 品目 / プラント / MRP エリアが利用可能であることを確認した"),
            ("見込生産の流れを白紙に書ける", "需要予測（PIR）→ MRP → 計画手配 → 指図 → 入庫（自由在庫）→ 受注 → 引当（ATP）→ 出荷 → 請求 を順に説明できる"),
            ("見込生産の 3 方式を区別できる", "品目レベル / 最終組立レベル / 組立レベル（戦略 10 / 30 / 40 系）の違いを説明できる"),
        ],
        concept_checks=[
            ("自由在庫と受注在庫の違いを説明できる", "MARD（自由）と MSKA（特在 E）の違い、引当の起こり方を説明できる"),
            ("PIR の役割を説明できる", "MD61 で作る需要予測が MRP の入力になり、受注が入ると消費される（消費モード）ことを説明できる"),
            ("ネットチェンジを説明できる", "MRP 実行で計画手配の日付・数量がどう調整されるか、MD04 の行の見方を説明できる"),
            ("標準原価と差異の流れを説明できる", "指図の投入 vs 出来高の差が差異になり、KKS1 / KO88 / CO88 で計算・決済されることを説明できる"),
            ("欠品・安全在庫の考え方を説明できる", "安全在庫と ATP が欠品をどう防ぐか、不足時に何が起きるかを説明できる"),
        ],
        config_check_texts={},
        hands_on_extra=[
            ("発展①：PIR を削って MRP の挙動を比べる", "MD61 で数量を変え、MD01N 後に計画手配がどう変わったかを記録した"),
            ("発展②：受注が PIR を消費することを確認する", "MD04 で PIR 行の消費（残）が減ることを確認した"),
            ("発展③：欠品を意図的に起こして ATP を確認する", "在庫と PIR を操作し、CO09 の不足と受注時の警告を確認した"),
        ],
        records=[
            ("PIR 登録（MD61）の品目・数量・期間", "月次 500 PC など"),
            ("MD04 の需要行（PIR / 受注）", "消費後の残を記録"),
            ("計画手配番号（MD04）", "MRP 実行後に生成"),
            ("製造指図番号（CO01 / CO40）", "標準原価が入っていること"),
            ("部品出庫（261）・完成品入庫（101）の数量", "指図数量と一致"),
            ("自由在庫の数量（MMBE / MB52）", "入庫後に増加"),
            ("受注番号と引当結果（CO09）", "不足なし／不足数量"),
            ("出荷・請求の伝票番号（VL01N / VF01）", "数量・金額"),
            ("指図の差異額（KKS1 / KO88）", "標準原価との差（±）"),
            ("伝票フロー（VA03）に揃った伝票", "受注 → 引当 → 出荷 → 請求"),
        ],
        finish_checks=[
            "PIR → MRP → 指図 → 入庫 → 受注 → 出荷 → 請求 を 1 人で通した",
            "自由在庫（MARD）と受注在庫（MSKA）の違いを、実機の画面で説明できた",
            "受注が PIR を消費する挙動を MD04 で確認した",
            "差異計算と決済（KKS1 / KO88 / CO88）を 1 回実行した",
            "MTO 站（sapmto）との違いを 5 点で説明できた",
            "能力测试（quiz.html）で 75% 以上",
        ],
    ),
    "sapvc": dict(
        label="SD バリアント設定付き受注生産（VC）",
        code="VC",
        intro=[
            ("本ワークブックの使い方",
             "VC は「1 品目で無数のバリエーション」を表現する構成エンジンです。手顺の暗記ではなく、"
             "「どの特徴が何を決めるか（BOM・工程・価格）」を設計できるようになることが目的です。"
             "各タスクの完成基準を満たしたら ○ を入れてください。"),
            ("目安時間", "配置（C0〜C16）＋練習①〜⑤で「講義 2 日 ＋ 実機 2〜3 日」程度。依存関係の作り込みに時間がかかります。"),
            ("特に注意", "VC を入れる前に、① バージョンと AVC/LO-VC の選択 ② 特徴設計の粒度 ③ 価格モデル を業務と合意してください。設計を誤ると後戻りが高くつきます。"),
        ],
        overview_checks=[
            ("本站の環境と前提を説明できる", "特徴 / クラス / KMAT / 設定プロファイルを作成する権限と、AVC（PMEVC）の利用可否を確認した"),
            ("VC の位置づけを説明できる", "VC は生産形態ではなく構成エンジンであり、在庫区分と戦略は別途決めることを説明できる"),
            ("設定値の流れを白紙に書ける", "受注で構成 → BOM 選別 → MRP → 指図 → 入庫 → 出荷 → 請求 の各段階で、設定値が何を決めるかを説明できる"),
        ],
        concept_checks=[
            ("VC の構成要素 6 つを言える", "特徴 / クラス / KMAT / 依存関係 / 設定プロファイル / シミュレーション（＋ C 步の T-code）"),
            ("依存関係の 4 種類を区別できる", "前提条件 / 選択条件 / 手続き / アクションが、それぞれ何を制御し、どこで評価されるかを説明できる"),
            ("スーパー BOM と受注 BOM の違いを説明できる", "設計上の全候補（スーパー BOM）と、受注時に選ばれた結果（受注 BOM）の関係を説明できる"),
            ("VC × 生産形態の組合せを言える", "戦略 25（KEK / 046）・82（KMFA / 201 / PP04）・ETO（Q）を、在庫区分と併せて説明できる"),
            ("変種価格のしくみを説明できる", "条件タイプ VA00 と、特徴の追加データ（SDCOM-VKOND）・条件レコードの関係を説明できる"),
            ("LO-VC と AVC の違いを説明できる", "S/4HANA の AVC（PMEVC）と従来 LO-VC の関係、移行の判断ポイントを説明できる"),
        ],
        config_check_texts={},
        hands_on_extra=[
            ("発展①：戦略 82 で受注組立（VC × ATO）を試す", "受注保存で指図が 1:1 に作られ、設定値が指図へ伝搬することを確認した"),
            ("発展②：選択条件を逆にして BOM の切替を確認する", "CU50 で BOM 展開が切り替わることを、変更前後で記録した"),
            ("発展③：変種価格を加算して請求金額を変える", "条件レコードを追加し、VA03 の条件画面と請求金額が変わったことを確認した"),
        ],
        records=[
            ("特徴名（CT04）×4 と値の一覧", "容量 / 材質 / 塗装 / 付属品 など"),
            ("クラス名（CL02）とクラス型", "クラス型 300・特徴の割当数"),
            ("設定可能品目（KMAT）の品目コード", "品目カテゴリグループ 0002 / 戦略グループ 25"),
            ("設定プロファイル名（CU41 / PMEVC）", "必須チェックの設定"),
            ("依存関係の名前（CU01〜CU03）×種類", "選択条件 / 前提条件 / 手続き"),
            ("スーパー BOM の構成品目数（CS03）", "___ 件"),
            ("CU50 のシミュレーション結果", "設定値ごとの BOM 構成品目"),
            ("受注番号と設定値（VA01）", "選んだ特徴値"),
            ("受注 BOM の構成品目（VA03 構成品目）", "選択条件どおりに選別されたか"),
            ("指図番号と設定値の伝搬（CO03）", "構成品目と作業手順"),
            ("変種価格の加算額（VA03 条件）", "条件タイプ VA00"),
            ("出荷・請求の伝票番号（VL01N / VF01）", "請求金額に加算が入っているか"),
        ],
        finish_checks=[
            "特徴 → クラス → KMAT → 設定プロファイル → 依存関係 を 1 人で作り切った",
            "CU50 で「設定値によって BOM が切り替わる」ことを確認した",
            "受注で構成し、その設定値が指図へ伝搬することを CO03 で確認した",
            "変種価格が請求金額に反映されることを確認した",
            "VC と MTO（戦略 25）／ATO（戦略 82）の違いを説明できた",
            "つまずいた点を「症状 → 根因 → 証拠 → 処置 → 再発防止」で 1 件以上記録できた",
            "能力测试（quiz.html）で 75% 以上",
        ],
    ),
    "sap_sd": dict(
        label="SD 受注処理（Sales Order Processing）",
        code="SD",
        intro=[
            ("本ワークブックの使い方",
             "録画「录像45 Sales order processing.mp4」（SAP Education Unit 14）の配套教材です。"
             "「1_学習WBS」を上から順に実施し、各タスクの「完成基準」を満たしたら自己判定に ○ を入れてください。"
             "○ の数は「2_進捗サマリ」に自動集計されます。詰まった行は「メモ」に症状を残し、講師と共有してください。"),
            ("目安時間",
             "配置（C0〜C16）と練習①〜⑤で「講義 1 日 ＋ 実機 1 日」程度（計 14〜16 時間）。"
             "動画（57 分）は各ページの該当時刻を再生しながら進めると理解が速くなります。"),
            ("特に注意",
             "本教材の主题は「操作」ではなく「値がどこから来るか」です。"
             "受注（VA01）を作ったら、必ず SE16N で VBAP（明細カテゴリ・出荷プラント）と主データ（MVKE / KNVV / KNMT）を"
             "並べて見る習慣を付けてください。標準の OR / TAN は書き換えず、ZOR1 / ZTAN を作って練習します。"),
        ],
        overview_checks=[
            ("本站の教材の出所と到達目標を説明できる",
             "同ディレクトリの録画（Unit 14: Sales Order Processing）が教材であり、目標は ① 伝票データの出所を判断できる ② 道具とヘルプを使える の 2 点だと説明した"),
            ("伝票データの 4 つの源泉を言える",
             "主データ／既存伝票データ／Customizing／ハードコード（ABAP）を、それぞれ例つきで説明できる"),
            ("端到端の流れを白紙に書ける",
             "受注（VA01）→ 変更（VA02：再決定・ブロック）→ 照会（VC/2）→ 出荷（VL01N・PGI）→ 請求（VF01）→ 情報照会 の順を説明できる"),
        ],
        concept_checks=[
            ("出荷プラントの 3 段階の優先順位を実測で示せる",
             "① 客先品目情報（VD51）→ ② 得意先マスタ 出荷先（XD02 出荷タブ）→ ③ 品目マスタ 販売組織1（MM02）の順で採用されることを、受注と VBAP-WERKS で確認した"),
            ("明細カテゴリ決定の 4 つのキーを暗唱できる",
             "販売伝票タイプ × 品目カテゴリグループ × 品目使用目的 × 高レベル明細カテゴリ（決定テーブル VOV4）"),
            ("明細カテゴリ TAN の性質を説明できる",
             "所要量タイプが空＝所要量を作らず在庫を持たない（受注在庫 E は戦略グループと所要量クラスの設計）と説明できる"),
            ("得意先変更の再決定ルールを 7 項目・4 項目で言える",
             "再決定：得意先マスタ・客先品目情報・テキスト・無償品・与力価格・出力・出荷プラントと出荷ポイント／不変：販売エリア・販売事務所と販売グループ・可用性と製品割当・バッチ"),
            ("ブロックの 3 階層と由来 3 通りを説明できる",
             "ヘッダ（納入・請求）・明細（請求）・納入日程行（納入）と、由来（手動／Customizing／チェック）を区別できる"),
            ("Sales Summary の画面構成がどこで決まるか言える",
             "SIS の Customizing 4 画面（Report Views／Views for an Evaluation／Report Views for a User／Last Documents for a Customer）"),
        ],
        config_check_texts={},   # HTML から抽出（各ステップの確認欄）
        hands_on_extra=[
            ("発展①：伝票タイプにブロックを仕込む",
             "ZOR1 に出荷ブロックを設定し、新規受注に自動で付くこと・既存受注は変わらないことを確認した"),
            ("発展②：出荷プラントの優先順位を実測する",
             "3 か所に違うプラントを入れ、上から順に採用されることを受注で確認した"),
            ("発展③：Sales Summary のビューを自作して適用する",
             "ビュー Z01 を定義し、情報ブロックを割り当て、自分のユーザに適用して VC/2 で表示を確認した"),
            ("発展④：不完全性の必須項目を追加し V.02 で管理する",
             "OVA2 で項目を追加し、警告で保存 → V.02 に表示 → 修正で消えることを確認した"),
        ],
        records=[
            ("受注番号（VA01）", "練習①で 1 件"),
            ("明細カテゴリ（VA03 明細詳細）", "TAN（動画のデモ値）"),
            ("出荷プラント（VA03 / VBAP-WERKS）", "1200（動画のデモ値。自システムの実測値を記録）"),
            ("正味価額（Net value）", "動画は 22,990.00 EUR。自システムの金額"),
            ("与力条件（VA03 条件画面）", "PR00 / MWST と金額・与力日付"),
            ("納入日程行カテゴリ / 納入日（VBEP）", "カテゴリと日付"),
            ("変更後の出荷プラント（VA02 → VBAP）", "変更前後の値"),
            ("ブロック 3 階層の設定と解除（VA02）", "納入ブロック・請求ブロックの値"),
            ("Sales Summary の与信値（VC/2）", "Credit Limit / Usage / Delta / Consumption %"),
            ("出荷伝票番号と PGI の実行（VL01N / VL02N）", "番号・数量・移動タイプ 601"),
            ("請求書番号と金額（VF01 / VF03）", "受注金額との一致"),
            ("伝票フロー（VA03）に揃った伝票", "受注 → 出荷 → 請求 の 3 種"),
            ("不完全な受注（V.02）", "わざと作った不完全伝票と、修正後に消えたこと"),
        ],
        finish_checks=[
            "伝票データの 4 つの源泉を、受注の実例で説明できた",
            "出荷プラントの 3 段階の優先順位を実測で示せた",
            "受注 → 変更 → 照会 → 出荷 → 請求 を 1 人で通した",
            "得意先変更の再決定／不変を、実際の受注で確認した",
            "ブロックの 3 階層を設定・解除し、由来を区別できた",
            "故障対照表から 2 件以上を再現し、症状→根因→証拠→処置を記録した",
            "つまずいた点を「症状 → 根因 → 証拠 → 処置 → 再発防止」で 1 件以上記録できた",
            "能力测试（quiz.html）で 75% 以上（28 題中 21 問以上）",
        ],
    ),
}

PAGE_ORDER = ["index", "concept", "config", "handson-1", "handson-2", "handson-3", "handson-4", "handson-5"]
PHASE_LABEL = {
    "index": "A 総覧",
    "concept": "B 概念と設計",
    "config": "C 配置（SPRO / マスタ）",
    "handson-1": "D 練習①",
    "handson-2": "E 練習②",
    "handson-3": "F 練習③",
    "handson-4": "G 練習④",
    "handson-5": "H 練習⑤（発展・故障）",
}
MIN_BY_KIND = {"index": 10, "concept": 10, "config": 15, "handson": 20, "check": 5, "extra": 20}


def strip_html(t):
    t = re.sub(r"<[^>]+>", "", t)
    t = t.replace("&nbsp;", " ").replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"')
    return re.sub(r"\s+", " ", t).strip()


def first_sentence(t, limit=110):
    t = strip_html(t)
    m = re.split(r"(?<=[。．\.])", t)
    s = (m[0] if m else t).strip()
    return s[:limit]


def read(site, page):
    p = os.path.join(ROOT, site, page + ".html")
    return open(p, encoding="utf-8").read() if os.path.exists(p) else None


def cfg_steps(html):
    """config.html の C ステップ（id と見出し、確認欄の文言）を抽出"""
    out = []
    marks = [(m.start(), m.group(1)) for m in re.finditer(r'<div class="steph" id="([^"]+)">', html)]
    for i, (pos, sid) in enumerate(marks):
        end = marks[i + 1][0] if i + 1 < len(marks) else len(html)
        block = html[pos:end]
        h = re.search(r"<h3[^>]*>(.*?)</h3>", block, re.S)
        title = strip_html(h.group(1)) if h else sid
        info = re.search(r'<div class="box info">(.*?)</div>', block, re.S)
        crit = first_sentence(info.group(1)) if info else ""
        out.append((sid, title, crit))
    return out


def h2_steps(html):
    """handson 系：h2 見出し（STEP）と、验收セクションのチェック項目を抽出"""
    steps, checks = [], []
    for m in re.finditer(r"<h2[^>]*>(.*?)</h2>", html, re.S):
        title = strip_html(m.group(1))
        if not title:
            continue
        if re.search(r"验收|完成基準|チェック", title):
            # 直後の ul.check を拾う
            tail = html[m.end(): m.end() + 4000]
            ul = re.search(r'<ul class="check">(.*?)</ul>', tail, re.S)
            if ul:
                for li in re.findall(r"<li[^>]*>(.*?)</li>", ul.group(1), re.S):
                    checks.append(strip_html(li))
            continue
        if re.search(r"期待結果|期待结果|つまずき|対照表|故障対照|完成基準|验收|チェックリスト|まとめ|問い合わせ|参考|出典", title):
            continue   # 参照表・完成基準・注意書きはタスクにしない（発展・故障対応は手順なので残す）
        if re.match(r"^\d+[-−–]\d", title):            # 1-1 / 2-3 形式の STEP
            steps.append(title)
        elif re.match(r"^(STEP|step)\s*\d", title):   # STEP 1 形式
            steps.append(title)
        elif re.match(r"^発展\s*\d", title):          # 発展 1：… 形式（選択課題だが手順）
            steps.append(title)
    return steps, checks


def build_rows(site, cfg, wb_rows, warn):
    site_dir = os.path.join(ROOT, site)
    # 明示的なページ構成を持つサイト（比較サイトなど、config/handson 構成を取らないもの）
    if cfg.get("pages"):
        for task, crit in cfg.get("overview_checks", []):
            wb_rows.append([PHASE_LABEL["index"], task, "index.html", crit, MIN_BY_KIND["index"]])
        for label, page, items in cfg["pages"]:
            if not os.path.exists(os.path.join(ROOT, site, page + ".html")):
                warn.append("%s/%s.html が見つかりません（WBS 行を生成できません）" % (site, page))
                continue
            for task, crit in items:
                wb_rows.append([label, task, page + ".html", crit, 15])
        return
    for page in PAGE_ORDER:
        html = read(site, page)
        if html is None:
            continue
        kind = "handson" if page.startswith("handson") else page
        if page == "config":
            steps = cfg_steps(html)
            if not steps:
                warn.append("%s/config.html: C ステップ（div.steph）を抽出できませんでした" % site)
            for sid, title, crit in steps:
                wb_rows.append([PHASE_LABEL[page], title, "config.html#%s" % sid,
                                crit or "当該設定を実施し、確認欄（自システムでの確認方法）で期待どおりの結果を確認した",
                                MIN_BY_KIND["config"]])
            continue
        if page.startswith("handson"):
            steps, checks = h2_steps(html)
            for t in steps:
                wb_rows.append([PHASE_LABEL[page], t, page + ".html",
                                "手順どおり操作し、「期待結果」の記載とシステムの状態が一致することを確認した",
                                MIN_BY_KIND["handson"]])
            for c in checks:
                wb_rows.append([PHASE_LABEL[page] + "（验收）", c, page + ".html",
                                c, MIN_BY_KIND["check"]])
            continue
        # index / concept：見出しを抽出し、完成基準は手書きリストで補う
        heads = [strip_html(m.group(1)) for m in re.finditer(r"<h2[^>]*>(.*?)</h2>", html, re.S)
                 if not re.search(r"出典|使い方|目次", strip_html(m.group(1)))]
        hand = cfg["overview_checks"] if page == "index" else cfg["concept_checks"]
        for i, (task, crit) in enumerate(hand):
            wb_rows.append([PHASE_LABEL[page], task, page + ".html", crit, MIN_BY_KIND[kind]])
        if not hand:
            warn.append("%s/%s.html: 完成基準が未定義" % (site, page))


def build_workbook(site, cfg):
    warn = []
    site_dir = os.path.join(ROOT, site)
    wb = Workbook()

    # ---- 1_学習WBS（先に組み立てて行数を確定させる） ----
    rows = []
    build_rows(site, cfg, rows, warn)
    # 講師版/受講者版/テスト（全站共通の締め）
    rows.append(["I 受講者版", "ワークシート（worksheet.html）を埋める", "worksheet.html",
                 "各シートを記入し、伝票番号・数値・故障記録が揃った", 60])
    rows.append(["J テスト", "能力测试（quiz.html）を受験する", "quiz.html",
                 "合格ライン（75%）以上を取得した", 30])
    rows.append(["J テスト", "修了チェック（到達点）を通す", "quiz.html",
                 "修了チェックリストの全項目にチェックが付いた", 30])

    ws = wb.active
    ws.title = "0_進め方"
    ws.merge_cells("A1:B1")
    c = ws.cell(1, 1, "学習WBS（受講者版）— %s" % cfg["label"]); c.font = F_TITLE; c.fill = FILL_TITLE
    ws.row_dimensions[1].height = 26
    ws.merge_cells("A2:B2")
    ws.cell(2, 1, "SAP S/4HANA 業務実践トレーニング / 記入式の進捗管理ワークブック（サイト版と同期）").font = F_SMALL
    r = 3
    for k, v in cfg["intro"]:
        ck = ws.cell(r, 1, k); ck.font = F_HEAD; ck.fill = FILL_HEAD; ck.alignment = WRAP; ck.border = BORDER
        cv = ws.cell(r, 2, v); cv.font = F_BODY; cv.alignment = WRAP; cv.border = BORDER
        ws.row_dimensions[r].height = max(17, 13 * (1 + len(v) // 55))
        r += 1
    r += 1
    ck = ws.cell(r, 1, "凡例"); ck.font = F_HEAD; ck.fill = FILL_HEAD; ck.alignment = WRAP; ck.border = BORDER
    cv = ws.cell(r, 2, "○ ＝ できた（完成基準を満たした）／△ ＝ 一部できた（要確認）／× ＝ できなかった。"
                       "「2_進捗サマリ」にフェーズ別の完了率が自動計算されます。"); cv.font = F_BODY; cv.alignment = WRAP; cv.border = BORDER
    ws.column_dimensions["A"].width = 26
    ws.column_dimensions["B"].width = 104

    ws = wb.create_sheet("1_学習WBS")
    heads = ["#", "フェーズ", "タスク", "参照ページ", "完成基準（ここを満たしたら ○）", "目安(分)", "実施日", "自己判定", "メモ"]
    widths = [5, 20, 40, 22, 62, 9, 12, 10, 30]
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(heads))
    c = ws.cell(1, 1, "学習WBS — %s（上から順に実施）" % cfg["label"]); c.font = F_TITLE; c.fill = FILL_TITLE
    ws.row_dimensions[1].height = 26
    for j, h in enumerate(heads, 1):
        cc = ws.cell(2, j, h); cc.font = F_HEAD; cc.fill = FILL_HEAD; cc.alignment = CENTER; cc.border = BORDER
    ws.row_dimensions[2].height = 24
    for i, row in enumerate(rows):
        r = 3 + i
        vals = [i + 1] + row + ["", "", ""]
        for j, v in enumerate(vals, 1):
            cc = ws.cell(r, j, v); cc.font = F_BODY; cc.border = BORDER
            cc.alignment = CENTER if j in (1, 4, 6, 7, 8) else WRAP
            if j == 8:
                cc.fill = FILL_IN
            elif i % 2 == 1:
                cc.fill = FILL_ALT
        ws.row_dimensions[r].height = max(18, 13 * (1 + len(str(row[3])) // 46))
    last = 2 + len(rows)
    dv = DataValidation(type="list", formula1='"○,△,×"', allow_blank=True, showDropDown=False)
    dv.error = "○ / △ / × のいずれかを入力してください"; dv.promptTitle = "自己判定"; dv.prompt = "○ = できた / △ = 一部 / × = できない"
    ws.add_data_validation(dv)
    dv.add("H3:H%d" % last)
    ws.auto_filter.ref = "A2:I%d" % last
    for j, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(j)].width = w
    ws.freeze_panes = ws.cell(3, 3)

    # ---- 2_進捗サマリ ----
    ws2 = wb.create_sheet("2_進捗サマリ")
    ws2.merge_cells("A1:E1")
    c = ws2.cell(1, 1, "進捗サマリ（1_学習WBS の自己判定から自動集計）"); c.font = F_TITLE; c.fill = FILL_TITLE
    ws2.row_dimensions[1].height = 26
    for j, h in enumerate(["フェーズ", "タスク数", "○", "△", "×", "完了率"], 1):
        cc = ws2.cell(2, j, h); cc.font = F_HEAD; cc.fill = FILL_HEAD; cc.alignment = CENTER; cc.border = BORDER
    phases = []
    for row in rows:
        if row[0] not in phases:
            phases.append(row[0])
    r0 = 3
    for i, ph in enumerate(phases):
        r = r0 + i
        ws2.cell(r, 1, ph).font = F_BODY
        ws2.cell(r, 2, '=COUNTIF(\'1_学習WBS\'!$B$3:$B$%d,$A%d)' % (last, r)).font = F_BODY
        ws2.cell(r, 3, '=COUNTIFS(\'1_学習WBS\'!$B$3:$B$%d,$A%d,\'1_学習WBS\'!$H$3:$H$%d,"○")' % (last, r, last)).font = F_BODY
        ws2.cell(r, 4, '=COUNTIFS(\'1_学習WBS\'!$B$3:$B$%d,$A%d,\'1_学習WBS\'!$H$3:$H$%d,"△")' % (last, r, last)).font = F_BODY
        ws2.cell(r, 5, '=COUNTIFS(\'1_学習WBS\'!$B$3:$B$%d,$A%d,\'1_学習WBS\'!$H$3:$H$%d,"×")' % (last, r, last)).font = F_BODY
        ws2.cell(r, 6, '=IF(B%d=0,"",ROUND(C%d/B%d*100,0)&" %%")' % (r, r, r)).font = F_BOLD
        for j in range(1, 7):
            ws2.cell(r, j).border = BORDER; ws2.cell(r, j).alignment = CENTER if j > 1 else WRAP
    rt = r0 + len(phases)
    ws2.cell(rt, 1, "合計 / 全体").font = F_BOLD
    ws2.cell(rt, 2, "=SUM(B%d:B%d)" % (r0, rt - 1)).font = F_BOLD
    ws2.cell(rt, 3, "=SUM(C%d:C%d)" % (r0, rt - 1)).font = F_BOLD
    ws2.cell(rt, 4, "=SUM(D%d:D%d)" % (r0, rt - 1)).font = F_BOLD
    ws2.cell(rt, 5, "=SUM(E%d:E%d)" % (r0, rt - 1)).font = F_BOLD
    ws2.cell(rt, 6, '=IF(B%d=0,"",ROUND(C%d/B%d*100,0)&" %%")' % (rt, rt, rt)).font = F_BOLD
    for j in range(1, 7):
        ws2.cell(rt, j).border = BORDER; ws2.cell(rt, j).fill = PatternFill("solid", fgColor="DCE9F5")
        ws2.cell(rt, j).alignment = CENTER if j > 1 else WRAP
    ws2.cell(rt + 2, 1, "実施合計時間（分）").font = F_BOLD
    ws2.cell(rt + 2, 2, "=SUM('1_学習WBS'!$F$3:$F$%d)" % last).font = F_BODY
    ws2.cell(rt + 3, 1, "○ のみの合計時間（分）").font = F_BOLD
    ws2.cell(rt + 3, 2, '=SUMIFS(\'1_学習WBS\'!$F$3:$F$%d,\'1_学習WBS\'!$H$3:$H$%d,"○")' % (last, last)).font = F_BODY
    for j, w in enumerate([26, 12, 8, 8, 8, 12], 1):
        ws2.column_dimensions[get_column_letter(j)].width = w

    # ---- 3_実機記録 ----
    ws3 = wb.create_sheet("3_実機記録")
    ws3.merge_cells("A1:E1")
    c = ws3.cell(1, 1, "実機記録（伝票番号・数値・証跡）— 講師の確認対象"); c.font = F_TITLE; c.fill = FILL_TITLE
    ws3.row_dimensions[1].height = 26
    for j, h in enumerate(["#", "記録項目", "期待値・見方", "実測値 / 伝票番号", "実施日", "証跡メモ"], 1):
        cc = ws3.cell(2, j, h); cc.font = F_HEAD; cc.fill = FILL_HEAD; cc.alignment = CENTER; cc.border = BORDER
    for i, (k, v) in enumerate(cfg["records"]):
        r = 3 + i
        ws3.cell(r, 1, i + 1).font = F_BODY
        ws3.cell(r, 2, k).font = F_BODY
        ws3.cell(r, 3, v).font = F_BODY
        for j in (4, 5, 6):
            ws3.cell(r, j).fill = FILL_IN
        for j in range(1, 7):
            ws3.cell(r, j).border = BORDER
            ws3.cell(r, j).alignment = CENTER if j in (1, 5) else WRAP
        ws3.row_dimensions[r].height = 22
    for j, w in enumerate([5, 38, 40, 30, 12, 34], 1):
        ws3.column_dimensions[get_column_letter(j)].width = w
    ws3.freeze_panes = ws3.cell(3, 1)

    # ---- 4_修了判定 ----
    ws4 = wb.create_sheet("4_修了判定")
    ws4.merge_cells("A1:C1")
    c = ws4.cell(1, 1, "修了判定（到達点チェックと講師確認）"); c.font = F_TITLE; c.fill = FILL_TITLE
    ws4.row_dimensions[1].height = 26
    for j, h in enumerate(["#", "到達点（これが言えたら本教材は修了）", "チェック"], 1):
        cc = ws4.cell(2, j, h); cc.font = F_HEAD; cc.fill = FILL_HEAD; cc.alignment = CENTER; cc.border = BORDER
    for i, t in enumerate(cfg["finish_checks"]):
        r = 3 + i
        ws4.cell(r, 1, i + 1).font = F_BODY
        ws4.cell(r, 2, t).font = F_BODY; ws4.cell(r, 2).alignment = WRAP
        ws4.cell(r, 3, "").fill = FILL_IN
        for j in range(1, 4):
            ws4.cell(r, j).border = BORDER
            ws4.cell(r, j).alignment = CENTER if j in (1, 3) else WRAP
        ws4.row_dimensions[r].height = max(20, 13 * (1 + len(t) // 52))
    dv2 = DataValidation(type="list", formula1='"✓,,—"', allow_blank=True, showDropDown=False)
    ws4.add_data_validation(dv2)
    dv2.add("C3:C%d" % (2 + len(cfg["finish_checks"])))
    r = 3 + len(cfg["finish_checks"]) + 1
    for k in ["再受講が必要な分野（△ × のあったフェーズ）", "講師所見", "実施日 / 講師署名"]:
        ck = ws4.cell(r, 1, k); ck.font = F_HEAD; ck.fill = FILL_HEAD; ck.alignment = WRAP; ck.border = BORDER
        ws4.merge_cells(start_row=r, start_column=2, end_row=r, end_column=3)
        cv = ws4.cell(r, 2, ""); cv.fill = FILL_IN; cv.border = BORDER
        ws4.row_dimensions[r].height = 34
        r += 1
    for j, w in enumerate([34, 78, 14], 1):
        ws4.column_dimensions[get_column_letter(j)].width = w

    out = os.path.join(site_dir, "%s_学習WBS_受講者版.xlsx" % cfg["code"])
    wb.save(out)
    return out, len(rows), warn


def main():
    targets = sys.argv[1:] or [s for s in SITES if os.path.isdir(os.path.join(ROOT, s))]
    bad = False
    for site in targets:
        if site not in SITES:
            print("unknown site:", site); continue
        if not os.path.isdir(os.path.join(ROOT, site)):
            print("skip (not found):", site); bad = True; continue
        out, n, warn = build_workbook(site, SITES[site])
        print("%-14s -> %s  (%d タスク)" % (site, os.path.basename(out), n))
        for w in warn:
            print("   WARN:", w); bad = True
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
