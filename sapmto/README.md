# SAP S/4HANA SD 受注生産（MTO）实战训练站

SD（受注・出荷・請求）× PP（所要量・指図）× MM（在庫）クロスモジュールの **受注生産（MTO）** を、
「練習配置（SPRO 手顺）」と「練習流程（実機オペレーション）」の 2 本立てで学習するための静的サイト。
ブラウザで `index.html` を開くだけで動きます（外部依存なし・オフライン可）。

## ファイル構成

```
sapmto/
├── index.html        総覧：场景设定・端到端流程・练习安排・设定对象一览・出典
├── concept.html      概念与设计：MTO の机制・決定链・関連テーブル・S/4HANA 変更点・10 の誤解
├── config.html       練習配置手顺 C0〜C16 + C17 Public Cloud 差異対照 + 配置完了チェックリスト
├── handson-1.html    練習① 受注登録と所要量転送（VA01 / VA03 / MD04 / MMBE / CO09）
├── handson-2.html    練習② MRP 実行と製造指図（MD01N / MD02 / MD13 / CO40 / CO08 / CO03）
├── handson-3.html    練習③ 部品出庫・製造実績・完成品入庫（CO02 / MIGO 261 / CO11N / MIGO 101）
├── handson-4.html    練習④ 出荷・出庫確認・請求（VL01N / VL02N / VF01 / 伝票フロー）
├── handson-5.html    練習⑤ 発展（戦略82 組立処理・ZTAK 切替・差異決算・購買連携・取消）＋故障対照表 12 項
├── instructor.html   讲师版：時間割・事前準備・配置/練習の解答と採点ポイント・必出 Q&A・評価基準
├── worksheet.html    学员版ワークシート（挖空・記入用／印刷可）
├── quiz.html         能力测试 28 問（自動採点＋解説）＋実機验收清单
├── tools/make_mto_xlsx.py  Excel 版（要件定義・手順書）を生成。python3 tools/make_mto_xlsx.py
├── SD受注生産MTO_要件定義・手順書.xlsx  11 シート（概要/環境前提/設定一覧/配置手順/練習手順/期待結果/故障対照表/用語集/出典/受講者チェック/講師用ガイド）
└── assets/
    ├── style.css     デザインシステム（btp-dev-hub から複製。無改変）
    ├── mto.css       本サイト追加分のみ（steph / checklist / vals など）
    ├── main.js       nav ハイライト・コードコピー・to-top（複製。無改変）
    └── quiz.js       能力测试の採点スクリプト（複製。無改変）
```

## 学習の進め方（推奨）

1. `concept.html`（60 分）— 決定链（品目マスタ → VOV4/VOV5 → 所要量タイプ → 所要量クラス → 個別在庫 E）を理解する
2. `config.html` C0〜C16（150 分）— 自システムで確認しながら、練習用に `Z001 / ZTAK / ZCP` を自建
3. `handson-1〜4`（240 分）— 受注 → MRP → 指図 → 出庫/入庫 → 出荷 → 請求 を通しで実施
4. `handson-5`（90 分〜）— 発展課題から 2 つ以上 + 故障対照表で復習
5. `quiz.html` — 28 問（合格 75%）＋ 実機验收清单が全部説明できれば完了

講師は `instructor.html`（解答・採点ポイント・必出 Q&A・評価基準）と `SD受注生産MTO_要件定義・手順書.xlsx`、
受講者には `worksheet.html`（記入用ワークシート）を配布する運用を想定しています。

## 教材としての方針（重要）

- **标准値は環境依存**（版本・業界ソリューション・既有改造）。本站は「標準の通常情況」を書きつつ、
  **各所に『自システムでの確認手順（T-code / テーブル / 画面）』を必ず添えてあります**。暗記対象ではなく検証対象として扱ってください。
- 例：明細カテゴリ `TAK` は SAP 標準に**存在しません**（SAP Note 2708455）。そのため本站は自建の `ZTAK` を使う練習にしています。
- 受注在庫の評価は環境差が大きい項目です（S/4HANA Cloud の MTO シナリオは評価付＝所要量クラス `046` が前提）。
  On-Premise で `040` 系を使っている場合、評価の有無は所要量クラスの「評価区分」と品目会計ビューで確認してください。
- 出典は `index.html` の「8. 出典と参考」に列挙（SAP Help / SAP Community / SAP Note・KBA / SAP Learning / 外部解説）。

## 動作確認（静的検証）

```bash
python3 ~/.hermes/skills/productivity/sap-training-sites/scripts/verify_site.py .
# → PASS: 11 pages, nav identical, 1 active each, tags balanced, copy buttons present, quiz keys valid
```

追加で実施済みの検証：全アンカー（`file.html#anchor` 含む）の解決、`id` 重複なし、
コードブロック内の HTML エスケープ（`&lt;`/`&gt;`）、quiz 28 問すべて 4 択・正解キー整合。

## 練習環境の前提

- SAP S/4HANA On-Premise（2020〜2024。画面パスは 2023/2024 基準）。Public Cloud は `config.html#cloud` の差異対照を参照。
- 販売組織 1000 / プラント 1000 / 得意先 1000、品目 `ZMTO-FG01`（FERT）/ `ZMTO-RM01` / `ZMTO-RM02`、作業区 `ZMTO_WC01`。
- カスタマイジング依頼に書き込める権限（練習後にロールバックできるように）。
- 本教材の数値（数量 10 PC、単価 12,000 JPY、納期 +30 日）は教学用の例です。自分の環境に合わせて読み替えてください。

## 学習WBS（受講者版）

受講者が「完成基準」を満たしたら ○ を付けて進める**打勾式の進捗表**（5 シート: 0_進め方 / 1_学習WBS（80 タスク、C ステップと各練習の验收項目を自動抽出）/ 2_進捗サマリ（フェーズ別の完了率を自動計算）/ 3_実機記録 / 4_修了判定）。
生成は親ディレクトリの共通スクリプト: `python3 ../tools/make_wbs_xlsx.py sapmto`（HTML から STEP と验收項目を抽出するので、ページを直したら再生成してください）。

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
