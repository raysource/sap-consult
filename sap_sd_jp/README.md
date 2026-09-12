# SAP S/4HANA 日本語実習サイト（sap_sd_jp）

同ディレクトリの **`S4.docx`（425 ページ・中国語の S/4HANA 教材ドキュメント）** を
**日本語に翻訳・再構成**した、オフラインで閲覧できる研修サイトです（姉妹サイト `../sap_sd_cn/` の日本語版）。

各タスクに **IMG 設定パス（日本語訳＋中国語原文）/ T-code / ステップごとの手順 / 実機画面** を並べています。

| 项目 | 数値（コードで自動集計。手書きではない） |
|---|---|
| モジュール | 6（準備作業 / 財務会計 FI / 管理会計 CO / 品目管理 MM / 生産計画 PP / 販売管理 SD） |
| タスク | 222 |
| 手順ステップ | 879 |
| 実機画面 | 1369 か所の参照（重複除去後 1209 ファイル / 20.7 MB） |
| ページ | 14 |
| 付属 Excel | `S4JP_手順書_学習WBS.xlsx`（9 シート） |
| 自習テスト | 30 問（自動採点・75% 合格） |

> **画面はすべて原教材ドキュメントの実機スクリーンショット（中国語インターフェースの SAP GUI）です。**
> 本站は抽出とレイアウトのみを行い、描き直し・生成・シミュレーションはしていません。
> 図注には原ドキュメントのファイル名（`imageNNN.png`）とピクセルサイズを残しており、Word 原文と 1 枚ずつ照合できます。

## ページ一覧

| ファイル | 内容 |
|---|---|
| `index.html` | 概要：出典と規模、学習ロードマップ、6 モジュール、ページの使い方、画面と設定値の説明、姉妹サイト |
| `prep.html` | 準備作業（システムへのログオン / SPRO の IMG 設定入口） |
| `fi.html` `co.html` `mm.html` `pp.html` `sd.html` | 5 モジュールの手順ページ：各タスク = 説明 → IMG パス → 入力値（日本語 / 画面の中国語 / 設定値）→ 手順ステップ（各ステップに画面＋「原文（中国語）」折りたたみ）→ 教材ノート |
| `tcode.html` | T-code 早見表（64 個）＋ IMG 設定メニューパス（203 件） |
| `glossary.html` | **用語対照表（日本語 ⇔ 中国語画面）** — 基本操作・SAP 用語・IMG パスの対照（本站独自） |
| `issues.html` | トラブルシューティング：原教材記録の現象 → 原因 → 対処 ＋ 6 項の前提チェック ＋ 全站の「つまずき注意」索引 |
| `tasks.html` | タスク索引：222 タスクをモジュール / キーワード（タスク名・T-code）で絞り込み |
| `instructor.html` | 講師用：5 日間の時間割、各モジュールの必演示タスク、必出 12 問答、採点の提案 |
| `worksheet.html` | 受講者用：222 行の進捗チェック表 ＋ 自分のシステムの設定値記入欄 ＋ 修了判定（印刷可） |
| `quiz.html` | 自習テスト 30 問（自動採点・75% 合格）＋ 実機での受入確認リスト |
| `S4JP_手順書_学習WBS.xlsx` | `0_説明` / `1_モジュール概要` / `2_手順一覧` / `3_画面索引` / `4_T-code早見表` / `5_IMGパス一覧` / `6_つまずきとエラー` / `7_学習WBS` / `8_進捗サマリ` |

サイトスクリプト：`assets/s4jp.js` = スクリーンショットのライトボックス（1×/2×/3×/4×、ESC で閉じる）
＋ 画面表示サイズ切替（投屏用、localStorage）＋ タスク索引の絞り込み ＋ 用語対照表の絞り込み ＋ パスのワンクリックコピー。
デザインは共有の `assets/style.css` / `main.js` / `quiz.js` をそのまま使い、本站は `assets/s4jp.css` に追加分だけを書いています。

## 日本語版としての作り方（本站の性格）

1. **本文は日本語**（原教材の中国語を訳出）。訳語は原教材の表記に合わせ、`work/ja/glossary.json` を唯一の用語基準にしています。
2. **画面は中国語のまま**（実機画面を描き直さない方針のため）。日本語の指示と画面表示を突き合わせるため、次の 3 つを実装：
   - 各手順ステップの **「原文（中国語）」折りたたみ**（`<details class="orig">`）= 原教材の一文そのまま
   - 各タスクの入力値表の **「画面の中国語」列**（日本語ラベル / 中国語ラベル / 設定値 の 3 列）
   - **`glossary.html` 用語対照表**（基本操作 21 項目・SAP 用語・IMG パス 203 件の日本語訳 ⇔ 中国語原文）
3. **原教材にない内容は補いません**。標準値・テーブル名・項目名・SAP Note 番号が原教材に無ければ、ここにも書きません。

## データフロー（再生成方法）

```
S4.docx
  └─ work/parse_docx.py         → work/doc_stream.json     （段落・表・画像参照を文書順に）
      └─ work/build_model.py    → work/curriculum.json     （モジュール → タスク → テキストブロック）
          └─ work/extract_images.py → assets/img/<mod>/tNN/…（意味的な命名 + 内容ハッシュで重複除去 + アイコン除外）
                                       work/images.json / work/images_summary.json
              └─ work/build_site_model.py → work/site_model.json（中国語モデル：ステップ化・IMG パス・T-code・入力値・ノート分類）
                  │
                  ├─ work/i18n.py collect all      → work/ja/{src,model}_atoms.json + _refs.json
                  ├─ work/i18n.py batches 5000     → work/ja/batches/*.json（15 バッチ）
                  │     （翻訳は work/ja/BRIEF.md の規約 + work/ja/glossary.json の用語で実施し、結果を work/ja/out/*.json に置く）
                  ├─ work/i18n.py merge            → work/ja/{src,model}_map.json（missing 0 を確認）
                  ├─ work/i18n.py check            → マーカー整合（668 リテラル）
                  ├─ work/i18n.py apply all        → 生成コードを日本語化（原本は work/ja/orig/ に退避）
                  │                                  + work/site_model_ja.json（日本語モデル。fb/fb_ja はコード側の比較用に中国語のまま保持）
                  ├─ work/jp_finalize.py           → lang=ja / assets/s4jp.* / MODEL_ZH 追加 / NAV に用語 / build_pages に glossary
                  ├─ work/jp_finalize2.py          → 前后台（IMG 設定 / 業務処理）の比較と表示を fb_ja 経由に統一
                  ├─ tools/build_pages.py          → 14 個の HTML（+ tools/hub_stats.json）
                  └─ tools/make_jp_xlsx.py         → S4JP_手順書_学習WBS.xlsx
```

```bash
cd ~/Desktop/work/training/sap_sd_jp

# 1) docx から素材層を作り直す（原稿が変わったときだけ）
python3 work/parse_docx.py && python3 work/resolve_media.py
python3 work/build_model.py && python3 work/extract_images.py && python3 work/build_site_model.py

# 2) 日本語化（翻訳の取り込み → 検証 → 適用 → 構造パッチ）
python3 work/i18n.py collect all && python3 work/i18n.py batches 5000
#   → work/ja/batches/*.json を翻訳して work/ja/out/*.json に置く
python3 work/i18n.py merge && python3 work/i18n.py check && python3 work/i18n.py apply all
python3 work/jp_finalize.py && python3 work/jp_finalize2.py

# 3) ページと Excel
python3 tools/build_pages.py
python3 tools/make_jp_xlsx.py

# 4) 検証
python3 tools/verify_site_jp.py                 # 本站專用（画像・アンカー・nav・タグ・クイズ・件数）
python3 ~/.hermes/skills/productivity/sap-training-sites/scripts/verify_site.py .
python3 work/qa_ja.py                           # 中国語（簡体字）の残りを検出（意図的な併記は除外）
```

### 翻訳パイプラインの仕組み（あとから訳を直すとき）

- **アトム** = 「1 行の自然言語」1 つ。`work/ja/{src,model}_atoms.json` は `{id: 中国語1行}`、`_map.json` は `{id: 日本語1行}`。
- **`apply` の再実行は条件付き**。`i18n.py apply src` は collect 時のオフセットに文字列を差し戻すため、
  **collect 後に手で編集したファイルには実行できません**。collect 時点のハッシュを各 ref に記録してあり、
  変わっていたらそのファイルを**スキップして警告**します（実測: 現在の 10 ファイルすべてスキップ＝安全）。
  - モデル側（`work/site_model_ja.json`）は無条件に再生成でき、`apply model` は冪等です（元の `site_model.json` を書き換えないため）。
  - 生成コードの訳語を直したい場合は、**日本語化済みのファイルを直接編集**してください（`work/ja/orig/` の中国語原本に戻して
    `apply` → `jp_finalize.py` → `jp_finalize2.py` をやり直す方法もありますが、構造パッチも再適用が必要です）。
- **マーカー**：HTML タグ・Python の `{...}` プレースホルダ・実体参照は `⟦0⟧⟦1⟧…` に置き換えて翻訳に出し、
  戻すときに「各マーカーがちょうど 1 回」であることを検証します（`i18n.py check`）。訳文がマークアップを壊せない仕組みです。
- **前后台の扱い**：データ側（モデル）は原教材の表記 `后台` / `前台` のまま保持し、表示は `fb_ja`（IMG 設定 / 業務処理）を使います。
  `pg_module.py` などの件数カウントが中国語定数と比較しているのはこのためです。
- 原本は `work/ja/orig/` に退避されています（差分確認用）。

## 注意（原教材の環境依存）

- 会社コード `C999`、会社名「頤寧機械有限公司」、プラント `F999`、保管場所 `P999`、
  品目 `R999-100` / `T999-100` / `F999-100`、得意先 `K001` / `K002`、原価センタ「管理部／製造部」など、
  **サンプル値は原教材の著者のシステムのもの**です。手順の順序と設定ポイントはそのまま使えますが、
  番号と名称は自分のシステムの値に置き換えてください。
- 画面は中国語インターフェースです。日本語版 SAP の標準訳語と異なる場合があるため、
  `glossary.html` の対照表（例：中国語「工厂」= 日本語では**プラント**）を併用してください。
- 原教材には OCR 由来の崩れた箇所が 1 か所あり、文字にならない行は除外しています（訳文にも残していません）。
