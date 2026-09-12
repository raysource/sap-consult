# SAP S/4HANA 受注設計生産（ETO）实战训练站

PS（WBS・ネットワーク）× SD（受注・出荷・請求）× PP（製造）× CO（予算・原価・収益）をまたぐ **受注設計生産（Engineer-to-Order / ETO）** を、
「練習配置（PS/SD の SPRO 手顺）」と「練習流程（実機オペレーション）」の 2 本立てで学習する静的サイト。
ブラウザで `index.html` を開くだけで動きます（外部依存なし・オフライン可）。MTO 站（`../sapmto/`）の姉妹サイトです。

## ファイル構成

```
sapeto/
├── index.html        総覧：场景设定・端到端流程・练习安排・设定对象一览（C1〜C17）・出典
├── concept.html      概念与设计：E（受注在庫）と Q（プロジェクト在庫）の違い・4 点セット・WBS の 3 役割・関連表・誤解 10
├── config.html       練習配置手顺 C0〜C16（PS プロファイル・評価付在庫・WBS 割当・予算・決済・結果分析）＋ Cloud（6GD）対照
├── handson-1.html    練習① 項目（CJ20N・WBS・請求要素）と受注（VA01 に WBS 割当・請求計画）
├── handson-2.html    練習② 計画（CJ40/CJ42）と MRP（MD51/MD50）・製造指図（CO40/CO08）
├── handson-3.html    練習③ 実行と入庫（CO02・261・CO11N/CN25・101 → プロジェクト在庫 Q）
├── handson-4.html    練習④ 出荷と請求（VL01N・VL02N 601・VF01・CJI3 で WBS に収益/原価）
├── handson-5.html    練習⑤ 発展（進捗 CNE1・結果分析 KKA2/KKAX・決済 CJ88/CJ8G・予算 CJBV・出来高請求）＋故障対照表 18 項
├── instructor.html   讲师版（解答・采分点・必出 Q&A 12・故障の教え方・評価基準）
├── worksheet.html    学员版ワークシート（挖空・記入用／印刷可）
├── quiz.html         能力测试 28 問（自動採点＋解説）＋実機验收清单
├── tools/make_eto_xlsx.py  Excel 版を生成（python3 tools/make_eto_xlsx.py）
├── SD受注設計生産ETO_要件定義・手順書.xlsx  11 シート（概要/環境前提/設定一覧/配置手順/練習手順/期待結果/故障対照表/用語集/出典/受講者チェック/講師用ガイド）
└── assets/           style.css・main.js（btp-dev-hub/sapmto から複製、無改変）／quiz.js（複製）／eto.css（本サイト追加分のみ）
```

## 学習の進め方（推奨）

1. `concept.html`（75 分）— **プロジェクト在庫 Q の 4 点セット**と E との違いを理解する
2. `config.html` C0〜C16（180 分）— 自システムで確認しながら、WBS を割り当てられる明細カテゴリと戦略グループを**実測**する
3. `handson-1〜4`（300 分）— 項目 → 受注 → 計画 → MRP → 指図 → 出庫/入庫 → 出荷 → 請求 を通しで実施
4. `handson-5`（120 分〜）— 進捗・結果分析・決済・予算管理から 2 つ以上
5. `quiz.html` — 28 問（合格 75%）＋ 実機验收清单が全部説明できれば完了

講師は `instructor.html` と Excel、受講者には `worksheet.html` を配布する運用を想定しています。

## 教材としての方針（重要）

- **ETO は環境差が最大のシナリオ**です。戦略グループ（S/4HANA Cloud の ETO は `E2`、所要量タイプ `E21`＝特別在庫 Q、6GD 活性後に利用可能）、
  WBS を割り当てられる明細カテゴリ（Cloud 例：`CBAO`）、評価付プロジェクト在庫の扱いは、版本・スコープ・既有改造で異なります。
  本站は「標準の通常情況」＋ **各所に『自システムでの確認手順』** を併記し、値の暗記ではなく検証を評価します。
- 机制の要点は 2 つだけ：**① プロジェクト在庫 Q の 4 点セット（評価付フラグ／MRP4 個別所要量／戦略グループ／受注明細の WBS）**、
  **② 収益は請求要素・原価は勘定設定要素**。すべての故障はこの 2 つに帰着します。
- 数量テーブルは **`MSPR`（プロジェクト在庫 Q）** と `MSKA`（受注在庫 E）。混同しないこと。

## 動作確認（静的検証）

```bash
python3 ~/.hermes/skills/productivity/sap-training-sites/scripts/verify_site.py .
# → PASS: 11 pages, nav identical, 1 active each, tags balanced, copy buttons present, quiz keys valid
```

追加で実施済み：全アンカー（`file.html#anchor` 含む）の解決、`id` 重複なし、quiz 28 問すべて 4 択・正解キー整合、
Excel の `unzip -t` と openpyxl 回読、`python3 -m http.server` での 11 ページ配信確認。

## 練習環境の前提

- SAP S/4HANA On-Premise（PS 導入済み、2020〜2024。画面は 2023/2024 基準）。
- プロジェクト `ZETO-1000`（WBS `.1` 設計・調達＝請求要素 / `.2` 製造 / `.3` 据付）、品目 `ZETO-FG01`（個別所要量品目）/ `ZETO-RM01` / `ZETO-RM02`、作業区 `ZETO_WC01`。
- 予算（`CJ30`）・決済（`CJ88`）・結果分析（`KKA2`）まで練習するため、PS/CO の権限とプロファイルが必須。
- 数値（1 式・5,000,000 JPY・30%/70%）は教学用の例です。自分の環境に合わせて読み替えてください。

## 学習WBS（受講者版）

受講者が「完成基準」を満たしたら ○ を付けて進める**打勾式の進捗表**（5 シート: 0_進め方 / 1_学習WBS（80 タスク）/ 2_進捗サマリ（完了率を自動計算）/ 3_実機記録（Q の数量・CJI3 の収益・決済まで 15 項）/ 4_修了判定）。
生成: `python3 ../tools/make_wbs_xlsx.py sapeto`（ページを直したら再生成）。

## 画面イメージ（SAP GUI モックアップ）と撮影リスト

手顺（config の各 STEP と各練習）には、SAP GUI の標準レイアウトに基づく**画面イメージ（SVG）**を添付しています。
**実機のスクリーンショットではありません**（フィールド名・配置はリリースとカスタマイズで変わります）。各 STEP の「自システムでの確認」に確認用の T-code と表を書いています。

- 生成: `cd .. && python3 tools/make_gui_mockups.py <site>`（spec = `tools/gui_spec.json`。再実行は冪等）
- 検証: `python3 tools/verify_gui_figures.py <site>`（全 STEP に図があるか）/ `python3 tools/check_gui_render.py <site>`（実際に描画されているか）
- **実機のスクリーンショットに差し替える**:
  1. 撮影リスト（`<CODE>_画面撮影リスト.xlsx` / `.csv`）を開き、画面ごとに実機で撮影
  2. 撮った画像を `assets/gui/` に「差し替え後」のファイル名（＝同じベース名の `.png`）で保存
  3. `cd .. && python3 tools/swap_gui_images.py <site> --apply` → ページの `src` を一括で `.png` に書き換え（戻すときは `--revert`）
- 注意書きの文面を外す場合: `python3 tools/add_gui_note.py <site> --remove`

## ローカルツール（この站固有）

- この站には**ローカルの spec ビルダ**があります: `tools/gui_spec_build.py`（＋ `tools/spec_h5.py`）が
  `tools/gui_spec.json` を組み立てます。**手で JSON に足したキーは `merge_existing()` が元の位置のまま保持**します
  （過去に再ビルドで「配置前的準備」の画面が消えた事故があるため）。ビルダを使うときは、ビルド前後で
  `python3 ../tools/verify_gui_figures.py sapeto` のステップ数が変わらないことを確認してください。
