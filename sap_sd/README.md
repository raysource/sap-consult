# SAP SD 受注処理（Sales Order Processing）实战训练站

**同ディレクトリの録画 `录像45 Sales order processing.mp4`（57 分 39 秒＝SAP Education 標準コース
Unit 14: Sales Order Processing）の配套教材**です。スライド講義と SAP GUI 実機デモで構成された動画を、
「自分の環境で再現し、値の出所を説明できる」状態まで持っていくための静的サイト。
ブラウザで `index.html` を開くだけで動きます（外部依存なし・オフライン可）。

動画の到達目標（冒頭スライド）は 2 点だけです ——
**① 伝票データの出所（material master / customer master / Customizing 等）を判断できる
② 受注を入力・処理するための道具とヘルプを使える**。本站はこの 2 点を 11 ページに分解しています。

シナリオは動画のデモをそのまま使います：**得意先 1000（Becker Berlin）から受注タイプ `OR` で品目 `T-ATA30` を 10 PC 受注**
（納入希望日 09.06.2007、支払条件 `ZB01`、インコタームズ `FOB`、与力価格日付 02.06.2007、正味価額 22,990.00 EUR、
出荷プラント `1200`、明細カテゴリ `TAN`）。デモ環境は SAP Training System / クライアント 800 / ユーザ `S000`・`tscm6-00` /
状態バー `trn03`・`OVR`（2007 年頃の R/3 GUI）。

## ファイル構成

```
sap_sd/
├── index.html        总览：教材の出所（動画 Unit 14）・**視頻章節対応表（時刻→ページ）**・场景设定・端到端流程・
│                     练习安排・設定対象一覧 C0〜C16・前提与环境・標準値の立場・出典
├── concept.html      概念与设计：伝票データの 4 つの源泉（ASCII 決定链）・販売エリアの導出・主データからの提案・
│                     パートナー 4 役割と提案元・**出荷プラントの優先順位**・明細カテゴリ決定の 4 キー・
│                     ヘッダ vs 明細・**変更時の再決定（Redetermined / Unchanged）**・ブロックの階層・
│                     不完全性と与信・Sales Summary・主要テーブル・10 の誤解
├── config.html       練習配置手顺 C0〜C16（17 STEP、各 目的/IMGパス/T-code/入力値/手順/確認（自系统）/つまずき/練習課題）
│                     ＋ 配置前的准备 / 配置完了チェックリスト
│                     ※動画が実演する Customizing は C1 VOV8・C3 OVT0・C4 OVS9・C5 SIS レポートビュー
├── handson-1.html    練習① 受注登録（VA01）：初期画面と販売エリア導出 → 主データからの提案 → 明細 T-ATA30 →
│                     出荷プラント自動提案 → 与力価格 → 保存と伝票フロー → 証拠を取る（SE16N で VBAK/VBAP/VBEP/VBPA）
├── handson-2.html    練習② 伝票の変更と再決定（VA02）：変更の 3 方式 → プラント変更 → 得意先変更（Redetermined/Unchanged）
│                     → ブロック 3 階層 → 変更前後の証拠（XD02 で得意先マスタとも突き合わせ）
├── handson-3.html    練習③ 販売情報システム（VC/2 Sales Summary）：照会の作法（3 経路）→ 情報ビュー/情報ブロック →
│                     与信情報（Credit Limit/Usage/Delta/Consumption %）→ Last SD documents と統計情報 →
│                     出荷伝票へのドリルダウン（動画の 80007832）→ 出ないときの切り分け（SIS Customizing 4 画面）
├── handson-4.html    練習④ 出荷と請求（VL01N → VL02N/PGI → VL03N → VF01）：動画は照会までのため、作成側は本站の補足
├── handson-5.html    練習⑤ ツール・発展・故障対応：SU3 と F1・与力分析 → 発展課題 4 本 → 故障対応の 4 画面 →
│                     故障対照表 15 項（症状 → 根因 → 証拠 → 処置）
├── instructor.html   讲师版：時間割（2 日/1 日）・板書用の決定链と 4 分類・発展課題の解答例・症例判別 8 問の答え・
│                     必出 Q&A 12 問・採点基準（75% 合格）
├── worksheet.html    学员版ワークシート：環境基本情報／受注 1 件の記録／**値の出所表**／出荷プラント 3 か所／
│                     変更前後比較／ブロック 3 階層／Sales Summary の記録／出荷・請求の記録／故障記録／自己判定（印刷可）
├── quiz.html         能力测试 28 題（概念 10 / 設定 7 / 実務 6 / 故障 5・自動採点＋解説）＋ 実機验收清单 8 項
├── tools/build_pages.py     11 ページの生成器（tools/pg_*.py を読み込んで HTML を書き出す）
├── tools/pg_common.py       nav/head/footer と组件（steph/kv/steps/box/quiz_q…）の一元管理
├── tools/pg_index.py      総覧（視頻章節対応表つき）／pg_concept.py／pg_config.py（C0〜C16）／
├── tools/pg_handson.py    練習①〜⑤／pg_extras.py 讲师版・学员版・能力测试
├── tools/gui_spec_build.py  SAP GUI 画面イメージ仕様の組立（tools/gui_spec.d/*.json → tools/gui_spec.json）
├── tools/gui_spec.d/        画面仕様の断片（ページ単位。並行作業しても衝突しない）
├── tools/make_sd_xlsx.py    Excel（要件定義・手順書）の生成。python3 tools/make_sd_xlsx.py
├── SD受注処理_要件定義・手順書.xlsx  11 シート（2_設定一覧・3_配置手順は pg_config.py から自動生成＝HTML とずれない）
├── SD_学習WBS_受講者版.xlsx          5 シート（学習WBS は本サイトの HTML から抽出）
├── SD_画面撮影リスト.xlsx / .csv     画面ごとの撮影リスト（実機差し替え用）
├── work/                   教材作成の証跡（動画解析）
│   ├── shots/              動画から抽出した代表画面 220 枚（タイムスタンプ付きファイル名）
│   ├── curriculum.md       画面単位の内容インベントリ（時刻・見出し・転記テキスト）＝本站の内容の根拠
│   ├── inv_0..9.json        10 分割で読み取った画面インベントリ（生データ）
│   ├── pick_frames.py      動画 → 1fps グレー指紋 → 代表画面の抽出（使い方: ファイル冒頭の docstring）
│   ├── digest.py           inv_*.json → curriculum.md の要約生成
│   ├── transcribe.py       ナレーションの文字起こし（mlx-whisper + PATH に ffmpeg が必要）
│   └── slice_probe.py      1 区間だけを増幅して転写する検証用（下記の断念理由の再確認用）
│
│   ※ ナレーションの文字起こしは**実施済みだが使用不可**（2026-09-12）:
│     音声は全体に −42 dBFS 程度と極端に小さく、2007 年頃の WebEx/NetMeeting 録音を
│     AAC 169 kbps mono に再エンコードしたもの。mlx-whisper（large-v3-turbo）は
│     29 分 49 秒かけて 3,003 セグメントを出したが内容は反復ハルシネーションで、
│     +24 dB 増幅して 1 区間だけ再試行しても回復しなかった（slice_probe.py）。
│     → **本站の内容は「画面」を根拠にしている**（work/shots の 220 枚と curriculum.md）。
│       ナレーション由来の記述は行っていないので、この欠落は内容の欠落を意味しない。
└── assets/
    ├── style.css     デザインシステム（btp-dev-hub から複製。無改変）
    ├── sd.css        本サイト追加分のみ（steph / vals / task / check / two-col / gui-* など。原型は sapmto/assets/mto.css）
    ├── main.js       nav ハイライト・コードコピー（複製。無改変）
    ├── quiz.js       能力测试の採点スクリプト（複製。無改変）
    └── gui/*.svg     SAP GUI 画面イメージ（生成物。実機スクリーンショットではない）
```

## 学習の進め方（推奨・標準 2 日）

1. 動画 `00:00`〜`06:45`（概念スライド）→ `concept.html` 1〜5 節（**4 つの源泉・販売エリア・主データからの提案・出荷プラントの優先順位**）
2. `config.html` C0（30〜60 分）— 自分の環境の実測値を記入（`VA01` / `XD03` / `MM03` / `VK13`）
3. 動画 `06:48`〜`21:35`（受注登録の実演）→ `handson-1.html`（90 分）— 受注を 1 件作り、**証拠（`VBAP-WERKS` と `MVKE`/`KNVV`/`KNMT`）を並べて取る**
4. `concept.html` 6〜13 節 → 動画 `32:52`〜`51:22`（変更・ブロック・再決定）→ `handson-2.html`（100 分）
5. 動画 `22:45`〜`32:29`（Sales Summary と Customizing）→ `handson-3.html`（80 分）＋ `config.html` C5
6. `config.html` C1〜C16（120 分）— `VOV8` / `OVT0` / `OVS9` / SIS レポートビューを実際に開き、決定テーブルは 1 行ずつ追加して検証
7. `handson-4.html`（90 分）— 受注 → 出荷（PGI）→ 請求 → 伝票フロー
8. `handson-5.html`（70 分）— `SU3`・`F1`・発展課題 4 本・故障対照表から 2 件以上を再現
9. `quiz.html`（28 題・75% 合格）＋ 実機验收清单 → 修了判定

講師は `instructor.html` と `SD受注処理_要件定義・手順書.xlsx`、受講者には `worksheet.html` を配布する運用を想定しています。

## 教材としての方針（重要）

- **主教材は動画そのもの**です。`index.html` 2 節に「視頻章節対応表（動画の時刻 → 本站ページ）」を置いています。
  動画で見た内容を、自分の環境で再現して確かめるのが本站の役割です。
- **動画の範囲を明示**しています：受注登録・変更・照会・Customizing の実演（`VA01` / `VA02` / `VC/2` / `VOV8` / `OVT0` / `OVS9` / SIS）は動画の内容、
  出荷・請求の**作成側**（`VL01N` / `VL02N` / `VF01`）は受注が業務として成立するために本站が補った内容（動画は `VL03N` の照会まで）。
- **標準値は環境依存**です。本站は「通常は〜」と書きつつ、**各 STEP に『自系统での確認方法（T-code ＋ テーブル ＋ 見る画面）』を必ず添えています**。
  暗記対象ではなく検証対象として扱ってください（明細カテゴリ・納入日程行カテゴリ・所要量タイプは特に差が出ます）。
- 出荷プラントの決定順序（客先品目情報 → 得意先マスタ → 品目マスタ）と、ABAP 拡張で重み付けされ得ることは
  SAP Help「Delivering Plants」および SAP KBA **2787562** に基づきます。不完全性チェックの T-code 群
  （`OVA2` / `VUA2` / `VUP2` / `VUE2` / `V.02`）とテーブル（`TVUV` / `TVUVF` / `VBUV` / `VBUP` / `VBUK`）は SAP Help
  「Log of Incomplete Items」に基づきます。
- 動画にない**数値・画面は作りません**。画面イメージは SAP GUI の標準レイアウトを再現した図で、実機のスクリーンショットではありません。

## 動作確認（静的検証）

```bash
cd /Users/jason/Desktop/work/training/sap_sd

python3 ~/.hermes/skills/productivity/sap-training-sites/scripts/verify_site.py .
# → PASS: 11 pages, nav identical, 1 active each, tags balanced, copy buttons present, quiz keys valid

cd .. && python3 tools/verify_all_sites.py sap_sd   # 站の棚卸し＋GUI カバレッジ＋コンテナ健全性
python3 tools/verify_gui_figures.py sap_sd          # 手顺ステップの画面イメージ網羅（RESULT: PASS）
python3 tools/check_gui_overlap.py sap_sd           # 注記が文字に重なっていないか（0 箇所）
python3 tools/add_gui_note.py sap_sd                # 「実機スクリーンショットではない」注意書き（冪等）
```

## 練習環境の前提

- SAP S/4HANA（On-Premise または練習用クライアント）。動画は R/3 ですが、**決定テーブルと優先順位の考え方は同じ**です。
- 販売エリア `1000/10/00`・得意先 `1000`（販売エリアビュー＋出荷先＋与力条件）・品目 `T-ATA30` 相当（販売組織 1・2・プラント在庫ビュー）が使えること。
- `VA01`〜`VA03`・`VL01N`・`VF01`・`XD02`・`VD51`・`VC/2`・`SE16N`・`V.02`・`SPRO` の権限。
- Customizing を触る場合はカスタマイジング依頼に入れる権限。**標準の `OR` / `TAN` は書き換えず、`ZOR1` / `ZTAN` を作って練習**します。

## 再生成の順序（ページを直したとき）

```bash
cd /Users/jason/Desktop/work/training/sap_sd
python3 tools/build_pages.py                 # HTML を生成（図は消える）
cd .. && python3 tools/make_gui_mockups.py sap_sd    # spec → SVG → 各 STEP へ挿入（冪等）
python3 tools/add_gui_note.py sap_sd                 # 注意書き（冪等）
python3 tools/export_gui_capture_list.py sap_sd      # 撮影リストを更新
python3 tools/make_wbs_xlsx.py sap_sd                # 学習WBS（HTML から抽出）
cd sap_sd && python3 tools/make_sd_xlsx.py           # 要件定義・手順書
cd .. && python3 tools/make_hub_page.py              # 索引页（数を実ファイルから数え直す）
```

## 画面イメージ（SAP GUI モックアップ）と撮影リスト

手顺（config の各 STEP と各練習）には、SAP GUI の標準レイアウトに基づく**画面イメージ（SVG）**を添付しています。
**実機のスクリーンショットではありません**（フィールド名・配置はリリースとカスタマイズで変わります）。各 STEP の「自系统での確認」に確認用の T-code と表を書いています。

- 仕様: `tools/gui_spec_build.py` が `tools/gui_spec.d/*.json` をマージして `tools/gui_spec.json` を生成（**JSON を直接編集しない**）
- 生成・挿入: `cd .. && python3 tools/make_gui_mockups.py sap_sd`（冪等）
- **実機のスクリーンショットに差し替える**:
  1. `SD_画面撮影リスト.xlsx` を見ながら実機で撮影
  2. 同じベース名の `.png` を `assets/gui/` に置く
  3. `cd .. && python3 tools/swap_gui_images.py sap_sd --apply`（戻すときは `--revert`）
