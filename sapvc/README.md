# SAP S/4HANA バリアント設定付き受注生産（VC / AVC）实战训练站

VC（バリアント設定 / S/4HANA では AVC）を **「構成エンジン」** として理解し、
「練習配置（SPRO 手順 C0〜C16）」と「練習流程（実機オペレーション 練習①〜⑤）」の 2 本立てで学ぶための静的サイト。
ブラウザで `index.html` を開くだけで動きます（外部依存なし・オフライン可）。

シナリオ：**産業用ポンプのバリアント設定付き受注生産** — 得意先 1000 が設定可能品目 `ZVC-PUMP01`（`KMAT`・品目カテゴリグループ `0002`・戦略グループ `25`）を 10 台（@850,000 JPY）発注し、
**容量・材質・塗装・付属品の 4 特徴**を選択 → 受注 BOM・作業手順・変種価格が依存関係で統制される → MRP（`KEK`・受注在庫 E）→ 製造指図（設定値伝搬）→ 出荷（601）→ 請求（`VA00` の加算込み）。

## ファイル構成

```
sapvc/
├── index.html        総覧：场景设定（ポンプ）・端到端流程・练习安排・設定対象一覧 C0〜C16・前提・標準値の立場・出典
├── concept.html      概念与设计：決定链（ASCII）・構成要素 6 つ・依存関係 4 種と適用先・クラス型 300・スーパー BOM と受注 BOM・
│                     設定値の流れ・VC × 生産形態（25/82/ETO）・変種価格・LO-VC と AVC・関連テーブル・S/4HANA 変更点・10 の誤解
├── config.html       練習配置手顺 C0〜C16（17 STEP、各 目的/IMGパス/T-code/入力値/手順/確認/つまずき/練習課題）＋配置完了チェックリスト
├── handson-1.html    練習① 特徴とクラスの設計（CT04 ×4 → CL02）
├── handson-2.html    練習② 設定可能品目と設定プロファイル（MM01 KMAT・クラス割当・CU41/PMEVC・CU50）
├── handson-3.html    練習③ 依存関係とスーパー BOM（CU01・CS01・CA01・CU50 で BOM 展開の切替）
├── handson-4.html    練習④ 受注で構成し製造・出荷・請求まで通す（VA01/MD04/CO40/CO03/MIGO/VL01N/VF01・伝票フロー）
├── handson-5.html    練習⑤ 発展と故障対応（変更統制・戦略 82 の 1:1・CU50/CU03/CU02 の読み方・故障対照表 14 項・発展課題 8 件）
├── instructor.html   讲师版：時間割（3/2/1 日）・事前準備・板書用図・C0〜C16 の解答と採点・練習①〜⑤の期待値・必出 Q&A 12 件・故障の教え方・評価基準
├── worksheet.html    学员版ワークシート（シート A 配置記録/B 練習記録 24 項/C CU50 結果表/D 故障記録/E 用語 10 語/F 質問メモと修了判定・印刷可）
├── quiz.html         能力测试 28 題（自動採点＋解説）＋ 実機验收清单 15 項
├── tools/make_vc_xlsx.py   Excel 版（要件定義・手順書）を生成。python3 tools/make_vc_xlsx.py
├── tools/check_site.py     追加の静的検証（アンカー/id 重複/クイズ構造/表のタイポ）。python3 tools/check_site.py .
├── SDバリアント設定VC_要件定義・手順書.xlsx  11 シート（概要/環境前提/設定一覧 C0〜C16/配置手順/練習手順/期待結果/故障対照表/用語集/出典/受講者チェック/講師用ガイド）
└── assets/
    ├── style.css     デザインシステム（btp-dev-hub から複製。無改変）
    ├── vc.css        本サイト追加分のみ（steph / vals / chips / dep / kv / check など。原型は sapmto/assets/mto.css）
    ├── main.js       nav ハイライト・コードコピー（複製。無改変）
    └── quiz.js       能力测试の採点スクリプト（複製。無改変）
```

## 学習の進め方（推奨・標準 3 日）

1. `concept.html`（90 分）— **決定链**（特徴 → クラス → KMAT → プロファイル → 依存関係 → 受注 BOM・工程・価格）と **依存関係 4 種の適用先** を理解する
2. `handson-1` / `handson-2`（135 分）— 特徴 4 つ・クラス `ZVC_PUMP_CL`（型 `300`）・`KMAT` の **5 条件**・設定プロファイル → `CU50` が開く状態まで
3. `handson-3`（180 分）— 依存関係（前提条件・選択条件・手続き）＋スーパー BOM ＋作業手順 → `CU50` で **材質・付属品・塗装による取捨**を実演
4. `handson-4`（180 分）— 受注 → 受注 BOM → 変種価格 → MD04（E）→ 指図（設定値伝搬）→ 入出庫 → 出荷 601 → 請求 → 伝票フロー
5. `handson-5`（150 分）— 変更統制・戦略 `82`（1:1）・故障対照表 14 項・切り分け演習（故意に壊したモデル）・発展課題 2 つ以上
6. `config.html` C0〜C16（120 分）— 自システムの実測値を記入（`VOV4` / `OVZG` / `CU43` / `VK13`）
7. `quiz.html` — 28 題（合格 75%）＋ 実機验收清单 → 修了判定

講師は `instructor.html`（解答・採点ポイント・必出 Q&A・評価基準）と `SDバリアント設定VC_要件定義・手順書.xlsx`、
受講者には `worksheet.html`（記入用ワークシート）を配布する運用を想定しています。

## 教材としての方針（重要）

- **標準値は環境依存**（版本・業界ソリューション・既有改造）。本站は「標準の通常情況」を書きつつ、
  **各所に『自システムでの確認手順（T-code / 画面 / テーブル）』を必ず添えてあります**。暗記対象ではなく検証対象として扱ってください。
- VC 用の**明細カテゴリ**は「通常は `TAN` 系」という記載（varconf）と「`TAC` = Configurable material item」という記載（thesdvault）が**両方存在する**ため、
  本站では値を断定せず **`VOV4` ＋ `VA03` の実測を正**としています。
- **変種価格のキー**は LO-VC では `SDCOM-VKOND`、AVC では `MMCOM-VKOND` という記載があります。本站は構造の存在を断定せず、`CT04` の追加データと `SE11` での確認を手順にしています。
- 所要量クラス（`046` 系）・**受注在庫の評価**・戦略グループの値は環境差が大きい項目です（`OVZG` / `OPPS` / 品目の会計ビューで確認）。
- **依存関係の構文と標準時間の項目名**はリリース差が大きいため、本站は項目名を断定せず「`CU03` の使用箇所」「`CA03` の標準値欄」で確認する手順にしています。
- 出典は `index.html` の「8. 出典と参考」と Excel の `8_出典` に列挙（SAP Help / SAP Help Support Content / SAP KBA・SAP Note / SAP Community / SAP Learning / varconf.com / thesdvault / sapstack でのテーブル実在確認）。

## 動作確認（静的検証）

```bash
python3 ~/.hermes/skills/productivity/sap-training-sites/scripts/verify_site.py .
# → PASS: 11 pages, nav identical, 1 active each, tags balanced, copy buttons present, quiz keys valid

python3 tools/check_site.py .
# → PASS: 11 pages, anchors+ids+assets resolved, quiz 28 questions (4 options A-D each, answer in keys, 1 explain each), no stray '|' in <td>
```

追加で実施済みの検証：`file.html#anchor` を全件解決（同一ページ内アンカー含む）／`id` 重複なし／
quiz 28 問が「4 択・キー A〜D ちょうど 1 回ずつ・`data-answer` がキーに含まれる」／アセット参照の実在。

## 練習環境の前提

- SAP S/4HANA On-Premise（2020〜2024。画面パスは 2023/2024 基準）。Public Cloud は `config.html#c16` の差異表を参照（**AVC 前提・SSCUI で作れない領域あり**）。
- 販売組織 1000 / プラント 1000 / 得意先 1000、`CT04`・`CL02`・`CU01`・`CU41`・`CU50`（AVC は `PMEVC`）の実行権限。
- 品目タイプ `KMAT` の番号範囲に空き。カスタマイジング依頼に書き込める権限（練習後にロールバックできるように）。
- 本教材の数値（数量 10 台、基本価格 850,000 JPY、納期 +45 日、加算額）は**教学用の例**です。自分の環境に合わせて読み替えてください。

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
