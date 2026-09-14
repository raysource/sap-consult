# 培训站系列 共通工具（~/Desktop/work/training/tools/）

6 个 SAP 培训站（`sap_sd` / `sapmto` / `sapeto` / `sapmts` / `sapvc` / `saporderflow`）で共用するスクリプト群。
各站は**静的 HTML（外部依存なし・オフライン可）＋ Excel**で、この tools/ から生成・検証します。

```
training/
├── tools/                     ← このフォルダ（共通ツール）
├── sap_sd/      SD 受注処理（Sales Order Processing）… 動画 Unit 14 準拠 / 受注・変更・照会・出荷/請求
├── sapmto/      SD 受注生産（MTO）    … 手順 C0〜C16＋練習①〜⑤＋配図 72 枚
├── sapeto/      SD 受注設計生産（ETO）… WBS / プロジェクト在庫 Q / 配図 86 枚
├── sapmts/      SD 見込生産（MTS）    … PIR / 標準原価 / 配図 66 枚
├── sapvc/       SD バリアント設定（VC）… KMAT / 特徴・依存関係 / 配図 68 枚
└── saporderflow/ 受注形態の横断比較（講義）… E vs Q 対照 / 配図 20 枚（6 対は 2 カラム）
```

## 一括検証（まずはこれ）

```bash
cd ~/Desktop/work/training
python3 tools/verify_all_sites.py              # 6 站を 1 表で棚卸し（構造＋GUI カバレッジ＋コンテナ健全性）
python3 tools/verify_all_sites.py --render     # GUI のラスタライズ検証まで（遅い）
python3 tools/verify_all_sites.py sapmto       # 単站
```

## SAP GUI 画面イメージ（モックアップ）

| スクリプト | 用途 |
|---|---|
| `make_gui_mockups.py <site>` | `tools/gui_spec.json` → `assets/gui/*.svg` を生成し、手顺ページの各 STEP に `<figure class="gui">` を挿入（冪等）。仕様は `GUI_SPEC_FORMAT.md` |
| `verify_gui_figures.py <site>` | spec に宣言した全ステップに図があるか／参照切れ／alt・figcaption・「画面イメージ」表記／SVG 妥当性 → `RESULT: PASS\|FAIL` |
| `check_gui_render.py <site>` | Chrome ヘッドレスで SVG→PNG→（stdlib zlib で）領域ピクセル統計。**画像を見られない環境でも「本当に描けているか」を証明**する |
| `check_gui_overlap.py <site>` | 赤い注記バッジ／吹き出しが表のセルや入力欄の文字に重なっていないか（`--fix` は spec 座標の調整案） |
| `pair_gui_figures.py <site>` | キャプションが `【E】…` / `【Q】…` の連続 figure を `<div class="gui-pair">` で包んで 2 カラム化（比較サイト用） |
| `add_gui_note.py <site>` | 図があるページの `<h1>` 直後に「実機スクリーンショットではありません」の注意書きを挿入（`--remove` で撤去） |
| `swap_gui_images.py <site>` | 実機スクリーンショットへの差し替え。`--status` 進行状況 / 引数なしで dry-run / `--apply` で `.svg`→画像に一括書換 / `--revert` で戻す。`.png .jpg .jpeg .webp`（大文字可）対応、PNG/JPEG は寸法を読んで小さすぎ・縦横比違いを警告 |
| `add_gui_note.py <site> --sync` | ページごとに「実機画像に全部置き換わったか」を判定して、注意書き（画面イメージ≠実機）を自動で入れる／外す |
| `export_gui_png.py <site> [--scale 2] [--zip] [--pdf-only]` | 画面イメージを **PNG（既定 2 倍解像度）** に書き出し（`assets/gui_png/`）、`--zip` で一括 ZIP、あわせて **`<CODE>_講義用画面集.pdf`**（手顺ごとに 1 セクション・画面＋キャプション＋注記＋確認 T-code）を生成。**実機写真が無くても講義資料が完結する**ようにするための出力 |
| `test_swap_workflow.sh` | 差し替えワークフローの自己テスト（生成 SVG をラスタライズして「撮影済み」に見立て、apply → note --sync → 検証 → revert まで通す。**実行結果: RESULT: PASS**）|
| `export_gui_capture_list.py [site…]` | 撮影リスト（`<CODE>_画面撮影リスト.xlsx / .csv`）を出力。画面ごとの T-code・見るべき点・差し替え後のファイル名つき |
| `GUI_SPEC_FORMAT.md` | 画面仕様 JSON の書き方（レイアウト種別・座標・内容の品質ルール） |

**注意**：生成される図は標準レイアウトに基づく**再現イメージ**で、実機のスクリーンショットではありません。
実機で撮った画像に差し替える運用を前提に、ファイル名（＝差し替え後名）と注意書きを用意しています。

### 画面 1 枚の追加手順

```bash
# 1) <site>/tools/gui_spec.json にステップ（config.html は id、handson は h2 の見出し）を追記
# 2) 生成 → 検証
python3 tools/make_gui_mockups.py <site>
python3 tools/verify_gui_figures.py <site>
python3 tools/check_gui_render.py <site> --limit 3   # 数枚だけ確認
python3 tools/check_gui_overlap.py <site>
```

## Excel 成果物

| スクリプト | 用途 |
|---|---|
| `make_hub_page.py` | 索引页（`~/Desktop/work/training/index.html`）を生成。ページ数・手順ステップ数・画面数・Excel を**実ファイルから数えて**埋め込むので、追記したら再実行すれば最新になる（各サイトの `assets/style.css`・`main.js` をコピーして同じ見た目にする） |
| `make_wbs_xlsx.py [site…]` | 各站の `学習WBS（受講者版）`（5 シート：進め方／学習WBS／進捗サマリ／実機記録／修了判定）を生成。**WBS 行は站の HTML から抽出**（config の `div.steph` と各練習の `h2`＋`ul.check` の验收項目）するので、ページを直したら再実行するだけで追随する |
| 各站の `tools/make_*_xlsx.py` | 站ごとの『要件定義・手順書』（11 シート）を生成。例: `cd sapmto && python3 tools/make_mto_xlsx.py` |

## 用語の整合（同語多訳の監査と一括修正）

| スクリプト | 役割 |
|---|---|
| `term_consistency_audit.py [site…]` | 7 站（既定 = 6 特集站 + `sap_sd_jp`）の**用語の表記揺れ**を監査。①概念ごとの候補表記（同じ語を 2 通り以上で書いている概念だけ）②長音符ゆれ（ユーザ/ユーザー）③全角/半角の併存 ④**簡体字（中国語）の残り**。「別概念なので直さない」組は `KEEP_NOTES` に理由付きで表示 |
| `fix_term_drift.py` / `fix_term_drift2.py` | 監査で見つかった表記を日本語 SAP の標準表記へ寄せる（顧客→得意先、資材伝票→品目伝票、明細タイプ→明細カテゴリ、受入予定→入庫予定、ワークセンター→作業区 …）。**生成器（`pg_*.py` / `spec_*.py` / `gui_spec.d`）と生成物の両方**を直し、その後 `build_pages.py` → `gui_spec_build.py` → `make_gui_mockups.py <site>` → `add_gui_note.py <site>` → `make_*_xlsx.py` で再生成する |

- 実測（2026-09-12 の統一作業）: 93 箇所を修正 → 監査の「要確認」概念 0 /「意図的な使い分け」21 概念。
- 残っている論点: 6 特集站は**ナビ・見出しに中国語表記を意図的に混ぜている**（练习 / 总览 / 概念与设计 / 学员版 / 验收 …、約 4,700 箇所 + Excel シート名）。
  これは作風の判断なので監査は数を出すだけで、勝手に書き換えない。
- 中国語教材から作った `sap_sd_jp` の翻訳パイプラインは站内に閉じている（`sap_sd_jp/work/i18n.py`、詳細は同站 README）。

## HTML の構造検証（站ごと）

```bash
cd <site>
python3 ~/.hermes/skills/productivity/sap-training-sites/scripts/verify_site.py .
# PASS: 11 pages, nav identical, 1 active each, tags balanced, copy buttons present, quiz keys valid
```

`verify_all_sites.py` はこの結果に加えて **`</article>` が 1 回だけで `<footer>` より前にあるか**（コンテナ閉じ位置の異常）も見ます。
過去に、図の挿入位置がずれて記事コンテナが途中で閉じてしまう事故があったためです（詳細は skill `sap-training-sites` の "Figure-insertion pitfalls"）。

## 実機スクリーンショット系のコース站（站内ツール・共有 `tools/` とは別）

`sap_cn/`（SAP SD 培训课程）は**実機截图 + 自绘 SVG**のコース站で、生成・検証・公開の道具を
すべて**站内の `sap_cn/tools/`** に閉じている（共有 `tools/` を触らないので他站に影響しない）。

```bash
cd ~/Desktop/work/training/sap_cn
python3 tools/make_diagrams.py        # 7 種の自绘图 → assets/diagrams/*.svg（純 Python → SVG）
python3 tools/build_pages.py          # 16 ページ HTML（統計数字は生成物から数える）
python3 tools/make_course_xlsx.py     # 课程大纲_学习WBS.xlsx（8 sheet）
python3 tools/verify_course.py        # 站専用検証器（構造/ナビ/リンク/锚点/画像実在/図注/quiz/hub 一致）
bash   tools/save_check.sh            # 「保存进度」用：検証 + Excel + hub + snapshot + git を一括実測
bash   tools/publish_to_github.sh     # 独立リポジトリ raysource/sap_cn_sd へ init/commit/push
bash   tools/verify_publish.sh        # push の出力ではなく ls-remote / API / ファイル数で確認
bash   tools/reconcile_remote.sh      # 逐路径対账（core.quotePath=false / blob だけ数える）
bash   tools/check_snapshot_cn.sh     # スナップショット検証（gzip / 件数 / 归档内 SVG と磁盘 md5 一致）
```

**踏んだ罠（この種の站で再利用する価値あり）**

- `qlmanage -t` で SVG を確認すると**正方形に pad/クロップ**され、右端が切れて「図が壊れている」と誤判定する。
  → **Chrome headless で SVG を直接撮る**（`--window-size=1420,1240 --screenshot=… file://…/*.svg`）。Chrome は直列で。
- `gh api repos/…/git/trees?recursive=1` の件数を「ファイル数」と数えると**ディレクトリ（`type=tree`）が混ざる**
  （269 → 320 に見えた）。`select(.type=="blob")` で絞る。
- `comm` は**両側を sort しないと嘘の差分**を出す。`git ls-files` は既定で CJK をエスケープするので
  `-c core.quotepath=false` を付ける。
- 親リポジトリ（`sap-consult`）へ入れるときは `tools/include_nested_repo_files.sh` を使う
  （`sap_cn/` は `.git` を持つ入れ子リポジトリなので `git add sap_cn/...` は黙って無効）。
- 中国語教材から作った站（`sap_sd_cn` / `sap_sd_jp` / `sap_modules_cn`）の道具も站内に閉じている。
  それぞれの `tools/` と README を見ること（`sap_modules_cn` は 2026-09-14 朝に別セッションが作成中）。

## 運用メモ

- **同じ站の HTML を 2 つのプロセス／エージェントで同時に編集しない**（図の挿入はファイル全体を書き換えるため、後勝ちで壊れます）。
- 図の仕様（spec）は**站ごとに 1 ファイル**。生成は冪等なので、何度でも再実行して構いません。
- 検証は「存在」ではなく「中身」を見る：`verify_gui_figures`（網羅）＋`check_gui_render`（描画）＋`check_gui_overlap`（可読性）の 3 点セットを推奨。
