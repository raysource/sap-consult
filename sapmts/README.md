# SAP S/4HANA 見込生産（MTS / Make-to-Stock）实战训练站

PP（需要予測・MRP・指図）× MM（在庫・入出庫）× SD（受注・出荷・請求）× CO（標準原価・差異）クロスモジュールの
**見込生産（MTS）** を、「練習配置（SPRO 手顺 C0〜C16）」と「練習流程（実機オペレーション ①〜⑤）」の 2 本立てで学習するための静的サイト。
ブラウザで `index.html` を開くだけで動きます（外部依存なし・オフライン可）。

姉妹站：**sapmto**（受注生産 / MTO・受注在庫 E）・**sapeto**（受注設計生産 / ETO・WBS）。本站は **見込生産（PIR 起点 + 自由在庫）** を担当します。

## ファイル構成

```
sapmts/
├── index.html        総覧：场景设定・端到端流程（10 步）・练习安排・设定对象一览（C1〜C17）・前提・出典
├── concept.html      概念与设计：見込生産の 3 方式对照（10/30・40/70）・PIR と消費/消減・自由在庫と ATP・
│                     MRP のネットチェンジ・計画手配→指図→101・標準原価と差異計算・関連表・S/4HANA 変更点・10 の誤解
├── config.html       練習配置手顺 C0〜C16（各 STEP = 目的/IMG パス/T-code/入力値/手順/確認/つまずき/練習課題）
│                     ＋ C16 Public Cloud 差異対照 ＋ 配置完了チェックリスト
├── handson-1.html    練習① 需要予測と PIR（MD61 / MD62 / MD73 / MD04 / PBED / 消費モード）
├── handson-2.html    練習② MRP 実行と計画手配（MD01N / MD04 / 純所要量の検算 / 従属所要量 / CO40・CO41 / ネットチェンジ）
├── handson-3.html    練習③ 製造と入庫（CO02 解放 / MIGO 261 / CO11N / MIGO 101 → 自由在庫 / 標準原価との差異の入口）
├── handson-4.html    練習④ 受注・引当・出荷・請求（VA01 / CO09・V_V2 / PIR の消費 / VL01N・VL02N PGI 601 / VF01 / 伝票フロー）
├── handson-5.html    練習⑤ 月末処理と発展（KKS1・KKS2 差異計算 / KO88・CO88 決済 / 棚卸 / 安全在庫切れ・欠品対応 /
│                     見込在庫と受注の取り合い / 故障対照表 12 項 / MD04 の読み方表 / 発展課題 8 項）
├── instructor.html   讲师版：時間割（2 日/1 日/半日）・事前準備・板書用の決定链・C0〜C16 の解答と採点ポイント・
│                     練習①〜⑤ の期待値・必出 Q&A 14 件・故障の教え方・評価基準・発展の導線
├── worksheet.html    学员版ワークシート（記入用／印刷可）：配置 C0〜C16・練習記録 24 項・MD04/MB52 読解・
│                     故障記録（症状→根因→証跡→対処→再発防止）・用語 10 語・修了判定
├── quiz.html         能力测试 28 問（概念 10 / 配置 9 / 流程 6 / 故障 3。自動採点＋解説）＋ 実機验收清单（合格 75%）
├── tools/make_mts_xlsx.py  Excel 版（要件定義・手順書）を生成。python3 tools/make_mts_xlsx.py
├── SD見込生産MTS_要件定義・手順書.xlsx  11 シート（概要/環境前提/設定一覧/配置手順/練習手順/期待結果/故障対照表/用語集/出典/受講者チェック/講師用ガイド）
└── assets/
    ├── style.css     デザインシステム（sapmto と同じ dev-hub 版。無改変）
    ├── mts.css       本サイト追加分のみ（steph / vals / task / check / strat チップなど）
    ├── main.js       nav ハイライト・コードコピー・to-top（複製。無改変）
    └── quiz.js       能力测试の採点スクリプト（複製。無改変）
```

## 学習の進め方（推奨）

1. `concept.html`（60 分）— 見込生産の 3 方式（10/30・40/70）と決定链
   （PIR → 戦略グループ → 消費モード → MRP → 計画手配 → 指図 → 自由在庫 → ATP 引当 → 差異）を理解する
2. `config.html` C0〜C16（150 分）— 自システムで確認しながら、品目 `ZMTS-FG01` の MRP1〜4 と標準原価（8,000 JPY）を整える
3. `handson-1〜4`（240 分）— PIR → MRP → 指図 → 261/101 → 受注 → PIR 消費 → 出荷 → 請求 を通しで実施
4. `handson-5`（90 分〜）— 差異計算・決済・棚卸・故障対照表、発展課題から 2 つ以上
5. `quiz.html` — 28 問（合格 75% = 21/28）＋ 実機验收清单が全部説明できれば完了

講師は `instructor.html`（解答・採点ポイント・必出 Q&A・評価基準）と `SD見込生産MTS_要件定義・手順書.xlsx`、
受講者には `worksheet.html`（記入用ワークシート）を配布する運用を想定しています。

## 教材としての方針（重要）

- **标准値は環境依存**（版本・業界ソリューション・激活済み業務機能・既有改造）。本站は「標準の通常情況」を書きつつ、
  **各所に『自システムでの確認手順（T-code / テーブル / 画面）』を必ず添えてあります**。暗記対象ではなく検証対象として扱ってください。
- 本站が依拠した標準の対応（要確認事項つき）：
  - 戦略グループ **10 = 見込生産（Net requirements planning、受注は PIR を消費しない）**、
    **11 = 見込生産・総所要量計画（Gross requirements planning、在庫を見ない／MRP3 の混合MRP区分 = 2）**、
    **30 = ロット生産（Production by lot size）**、**40 = 最終組立ありの計画（Planning with final assembly、受注が PIR を消費）**、
    **70 = 組立レベルでの計画（Planning at assembly level）**。
    ネット上には 40 と 30 の説明を入れ替えた記述が多く見られます。**必ず `OPPT` の自分のシステムの記述で確認**してください。
  - 所要量タイプの対応（戦略 40：独立 `VSF` / 得意先 `KSV`→クラス `050`、戦略 10：`LSF`/`KSL`→`030`、戦略 11：`BSF`→`102`）は
    第三者資料（SAP Tribal Knowledge の OPPT/OPPS/OVZH/OVZG 対応表）に基づく「通常は〜」の値です。**番号は環境で確認**してください。
  - 納入日程行カテゴリ `CP` は標準では「所要量転送 ON・在庫確認 ON・移動タイプ 601」ですが、
    **値は環境で異なる**ため `VOV6` と `VBEP`（実測）で確認する手顺を各所に置いています。
  - 差異カテゴリ（入力価格/入力数量/資源使用/混合価格/出力価格/スクラップ/残差）は SAP Help「Variance Categories」に基づきますが、
    **番号（010/020…）や有効なカテゴリは版本・設定依存**なので、教材では番号を暗記対象にしていません。
- Public Cloud の差異は `config.html` の C16 に集約。**断言しているのは スコープアイテム `BJ5`（Make-to-Stock Production – Discrete Manufacturing）と
  SSCUI `105120`（明細カテゴリ別の所要量タイプ決定）まで**で、その他の ID は「版本で変わるため要確認」と明記しています。
- 出典は `index.html` の「8. 出典と参考」と `concept.html` / 各練習ページ末尾、Excel の `8_出典` シートに列挙
  （SAP Help / Support Content / SAP Note・KBA / SAP Community / SAP Learning / SAP PRESS blog / SAP Tribal Knowledge / SAP Datasheet・LeanX）。

## 動作確認（静的検証）

```bash
python3 ~/.hermes/skills/productivity/sap-training-sites/scripts/verify_site.py .
# → PASS: 11 pages, nav identical, 1 active each, tags balanced, copy buttons present, quiz keys valid
```

追加で実施済みの検証：全アンカー（`file.html#anchor` 含む）の解決、`id` 重複なし、内部 `href="#…"` の解決、
`<td>` 内の stray `|` なし、quiz 28 問すべて 4 択（キー A〜D）・正解キー整合、全アセット参照の解決、
ローカル HTTP サーバ（`python3 -m http.server 8784`）で全ページ・全アセットが HTTP 200 を返すこと。

## 練習環境の前提

- SAP S/4HANA On-Premise（2020〜2024。画面パスは 2023/2024 基準）。Public Cloud は `config.html#c16` の差異対照を参照。
- 販売組織 1000 / プラント 1000 / 得意先 1000、完成品 `ZMTS-FG01`（FERT・標準価格 8,000 JPY・安全在庫 100 PC）、
  部品 `ZMTS-RM01` / `ZMTS-RM02`、作業区 `ZMTS_WC01`、BOM RM01×2・RM02×4。
- **原価計算（CO-PC）が使えること**（`CK11N`・`CK24`・`KKS1`・`KO88`）——これが無いと練習⑤ が成立しません。
- カスタマイジング依頼に書き込める権限（練習後にロールバックできるように）。
- 本教材の数値（見込 500 PC/月、安全在庫 100 PC、受注 200 PC、単価 8,000 JPY、納期 +7 日）は教学用の例です。自分の環境に合わせて読み替えてください。

## 未収録（今後の拡張）

- `MTS_学習WBS_受講者版.xlsx`（打勾式の進捗表）は本サイトには未収録です。親ディレクトリの共通スクリプト
  `~/Desktop/work/training/tools/make_wbs_xlsx.py` の `SITES` に sapmts のエントリを追加すれば、
  `config.html` の `div.steph id="cN"` と各練習の `<ul class="check">` から自動生成できます（本站はそのマークアップ契約を満たしています）。

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
