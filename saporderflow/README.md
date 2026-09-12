# SAP 受注形態の横断比較（MTS / MTO / ETO / ATO / VC）

「どの生産形態を選ぶか」で後工程（库存区分・所要量タイプ・成本対象・請求方式・収益認識）が連鎖して決まる——
その全体像を 1 ヵ所で比較する**講義用サイト**。実機の手顺は持たず、姉妹サイトの実習站（`../sapmto/`＝MTO、`../sapeto/`＝ETO）へ繋ぐ役割を持ちます。
ブラウザで `index.html` を開くだけ（外部依存なし・オフライン可）。

## ファイル構成

```
saporderflow/
├── index.html        総覧：5 形態の地図・選型判断 6 問・両站との関係・授课方案・出典
├── compare.html      横断比較：9 维度マトリクス・戦略/所要量タイプ早見・在庫テーブル・明細カテゴリグループ・E vs Q 4 点セット・取違えの症状
├── scenario-eq.html  E vs Q 対照実習：同じ受注を 2 通りで走らせる STEP 対照表・一致点/相違点・期末の見え方・最小手顺・判別演習 8 問
├── vc.html           VC 概観：構成要素 6 つ・他形態との組合せ・設定値の流れ・LO-VC と AVC・典型故障 7 項・学習導線
├── instructor.html   讲师版：時間割（90/180/300 分）・板書用の 3 つの問い・演習解答（振り分け 5 件 / 判別 8 問）・討論テーマ・採点・必出 Q&A 7
├── quiz.html         能力测试 20 題（形態判別 / 主数据 / T-code / 故障 / VC）＋修了チェック
├── tools/make_cmp_xlsx.py   Excel 版を生成（python3 tools/make_cmp_xlsx.py）
├── SAP受注形態比較_講義テキスト.xlsx  6 シート（概要/比較マトリクス/早見表/E vs Q 対照/演習解答/出典）
└── assets/           style.css・main.js（複製）/ quiz.js（複製）/ cmp.css（本サイト追加分のみ）
```

## 使い方（推奨の流れ）

1. `index.html` → `compare.html` で「形態 × 9 维度」の地図を頭に入れる（90 分）
2. `scenario-eq.html` で E と Q の対照表を読み、判別演習 8 問を解く
3. 実機は `../sapmto/`（E）→ `../sapeto/`（Q）で 1 回ずつ通す
4. 最後に「需要の帰属・在庫の表・成本の対象・請求の仕方・月末処理」の 5 点を、資料なしで 5 分で説明できるようにする（＝到達点）
5. `quiz.html`（20 題・合格 75%）

## 方針

- 本サイトは**比較と判断**の教材です。設定値は「標準の通常情況」を記載し、**具体値は各実習站の『自システムでの確認手順』で実測**する前提です。
  特に ETO（戦略グループ・WBS 割当可能な明細カテゴリ）と VC（モデリング設計）は環境差・設計差が大きい領域です。
- T-code と表現は S/4HANA On-Premise 2020〜2024 基準。Cloud の場合は スコープアイテム（6GD / IYT / 7DM など）の Test Script を優先してください。

## 検証

```bash
python3 ~/.hermes/skills/productivity/sap-training-sites/scripts/verify_site.py .
# → PASS: 6 pages, nav identical, 1 active each, tags balanced, copy buttons present, quiz keys valid
```

## 学習WBS（受講者版）

講義用の打勾式シート（0_進め方 / 1_学習WBS（16 タスク = 各ページの到達項目）/ 2_進捗サマリ / 3_実機記録 / 4_修了判定）。
生成: `python3 ../tools/make_wbs_xlsx.py saporderflow`。

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
