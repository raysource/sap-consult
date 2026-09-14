# 進捗メモ — SAP 培训站系列（全モジュール手順 日本語版/中文版 + SD 受注処理 / MTO / ETO / MTS / VC / 受注形態比較
                      + SD 培训课程 + **全モジュール培训课件（MM / PP / FI / CO）**）

最終更新: 2026-09-14 08:40 JST（**`sap_modules_cn`（SAP 全模块培训课件・中文・MM/PP/FI/CO 各 14 ページ + 総覽 = 57 ページ / 教材 172 タスク・695 手順 / 実機截图 1411 処引用（940 枚） / 自绘 SVG 32 図 / 自測 120 題 / Excel 5 冊。`verify_site.py` PASS）を追加**（§14） ／ 作業ディレクトリ: `/Users/jason/Desktop/work/training/`）
このファイルは**中断・再開用のハンドオフ**です（セッションが切れても、ここから再開できるように書いています）。

---

## 1. 何ができているか（このディレクトリで作ったもの）

SAP の業務実践トレーニング教材を **10 サイト**分（`sap_sd_jp` = 中国語教材 `S4.docx` の<b>日本語版・全モジュール手順</b>、`sap_sd_cn` = その中国語原文版。この 2 站は**画面が生成図ではなく教材 Word 文档の実機スクリーンショット（中国語インターフェースの SAP GUI）**、`sap_cn` = その SD 部分を使った<b>中国語 SD 専項コース</b>（実機截图 + 自绘の図）、残りは sap_sd の R/3 録画を除き生成した画面イメージ）。各サイトは
**静的 HTML（外部依存なし・オフライン可）＋ Excel＋ SAP GUI 画面イメージ（生成 SVG）**で構成。

| ディレクトリ | 内容 | ページ | 手順ステップ | 画面イメージ | Excel |
|---|---|---|---|---|---|
| **`sap_sd_jp/`** | **SAP S/4HANA 日本語実習サイト（全モジュール手順の日本語版）** — `sap_sd_cn` と同一教材 `S4.docx` 準拠。FI/CO/MM/PP/SD の 6 大モジュール・222 タスク・879 手順ステップ。**本文は日本語、画面は中国語のまま収録**し、各ステップに「原文（中国語）」折りたたみ／入力値表に「画面の中国語」列／用語対照表（`glossary.html`）を用意。講師用・受講者用・自習テスト・トラブルシューティング付き。翻訳は `work/i18n.py`（⟦n⟧ マーカー方式） | 14 | 879 | 1369（実機截图・去重 1209） | 手順書+学習WBS(9 sheet) |
| **`sap_sd_cn/`** | **SAP S/4HANA 中文实训站（全模块手册）** — 同ディレクトリの教材 Word 文档 `S4.docx`（425 页・内嵌画像 1385 枚）準拠。準備/FI/CO/MM/PP/SD の 6 大模块・222 任務。**画面は原文档の実機スクリーンショット（中文界面 SAP GUI）**、T-code 速查・排錯・任務索引・讲师版/学员版/自测 付き | 13 | 879 | 1369（実機截图・去重 1209 ファイル） | 手順書+学習WBS(9 sheet) |
| **`sap_cn/`** | **SAP SD 培训课程（中文・从概念到流程 / 总体到局部）** — `sap_sd_cn` と同じ教材 `S4.docx` の SD 48 タスク + 準備章の**実機スクリーンショット 269 枚を再利用**し、概念 → 组织结构 → 主数据 → 定价 → 端到端流程（O2C）→ 配置 → 分析 → 实训 の 16 ページに再構成。**自绘の思维导图/流程图/结构图 7 種 10 図**（純 Python → SVG）＋ 讲师版/学员版/自测 30 題/术语表。`tools/verify_course.py` は站専用検証器 | 16 | 179 | 155（実機截图引用・去重 120） | 課程大綱+学習WBS(8 sheet) |
| **`sap_modules_cn/`** | **SAP 全模块培训课件（MM / PP / FI / CO）** — 同じ教材 `S4.docx` の MM/PP/FI/CO 4 モジュールを中文课程化。総覽页 + モジュール別 14 ページ（概念→组织→主数据→流程→操作手顺3篇→配置→实训→讲师/学员/自测/术语）。実機截图 1411 処引用（940 枚 = 素材を使い切った）+ 自绘 SVG 32 図 | 57 | 695 | 1411 处引用（去重 940 枚実機截图） | 4 モジュール分 + 総覽（各 8 sheet） | 2026-09-14 |
| **`sap_sd/`** | **SD 受注処理（Sales Order Processing）** — 同ディレクトリの録画 `录像45 Sales order processing.mp4`（SAP Education Unit 14・57 分）準拠。伝票データの 4 つの源泉・販売エリア導出・**出荷プラントの優先順位**・明細カテゴリ決定の 4 キー・変更時の再決定・Sales Summary（`VC/2`） | 11 | 45 | 65 | 要件定義・手順書(11 sheet) + 学習WBS(111 タスク) + 撮影リスト |
| `sapmto/` | SD 受注生産（MTO / 受注在庫 E） | 11 | 44 | 82 | 要件定義・手順書(11 sheet) + 学習WBS(85 タスク) + 撮影リスト |
| `sapeto/` | 受注設計生産（ETO / プロジェクト在庫 Q・WBS・PS） | 11 | 46 | 97 | 要件定義・手順書(11) + 学習WBS(87) + 撮影リスト |
| `sapmts/` | SD 見込生産（MTS / PIR・自由在庫・標準原価） | 11 | 44 | 69 | 要件定義・手順書(11) + 学習WBS(94) + 撮影リスト |
| `sapvc/` | バリアント設定付き受注生産（VC / AVC・KMAT・依存関係） | 11 | 40 | 74 | 要件定義・手順書(11) + 学習WBS(95) + 撮影リスト |
| `saporderflow/` | 受注形態の横断比較（講義・E vs Q 対照／VC 概観） | 6 | 9 | 20（6 対は 2 カラム） | 講義テキスト(6) + 学習WBS(19) + 撮影リスト |
| `index.html` | **索引页（ハブ）**：10 站への入口・学習路線（⓪ 全モジュール手順（日本語版 / 中国語原文版）→ ① 受注処理 → ② MTO → ③ ETO → ④ 横断比較 → ⑤ MTS → ⑥ VC）・規模一覧・ツール説明 | 1 | — | — | `tools/make_hub_page.py` で自動生成 |
| `tools/` | 共通ツール群（12 スクリプト + 2 ドキュメント。`sap_sd` を SITES に追加済み） | — | — | — | 生成・検証のすべてはここ |

各 11 ページサイトの中身: `index` / `concept` / `config`（C0〜C16 の SPRO 手顺）/
`handson-1..5`（練習①〜⑤）/ `instructor`（讲师版＝解答・采分点・必出 Q&A）/ `worksheet`（学员版＝記入用）/
`quiz`（28 題・合格 75%）。`assets/` は 4 つの共有 CSS/JS（`style.css` `main.js` `quiz.js` ＋ サイト固有の `mto.css` 等）。

**`sap_sd`（新規・11 ページ / 45 手順ステップ / 65 画面 / 3 Excel）の要点** — 教材は動画そのもの（同ディレクトリの `录像45 Sales order processing.mp4`＝SAP Education Unit 14・57 分）。
`index.html` に「視頻章節対応表（動画の時刻 → 站内ページ）」を置き、**動画の範囲と本站が補った範囲（出荷・請求の作成側）を明記**（動画は `VL03N` の照会まで）。
デモ値: 得意先 `1000` Becker Berlin / 品目 `T-ATA30`・`T-ATA29` / 受注タイプ `OR` / 明細カテゴリ `TAN` / 出荷プラント `1200` / 支払条件 `ZB01` / ステータスバー `trn03`・`OVR`。
**同じ項目が動画内で 2 通りに出る例**（インコタームズ：スライドは `FOB`、実機デモは `CIF Berlin`。`VOV8` の詳細は `OR` ではなく `CR`）を明示し、「値は主データ由来なので自システムで確認」の方針を徹底。
生成: ページ `tools/pg_*.py` → `tools/build_pages.py` ／ 画面 `tools/gui_spec.d/*.json` → `tools/gui_spec_build.py` → `gui_spec.json` → `tools/make_gui_mockups.py` ／
Excel `tools/make_sd_xlsx.py`（2_設定一覧・3_配置手順は `pg_config.py` から生成＝HTML とずれない）＋ `tools/make_wbs_xlsx.py sap_sd`。
素材の証跡は `sap_sd/work/`（代表画面 220 枚・`curriculum.md`・`inv_0..9.json`。動画音声 wav は容量のため未同梱）。

**⚠ 動画のナレーション転写は試行済み・使用不可**（再実行しないこと）: 音声は全体 −42 dBFS と極小で、
AAC 169 kbps mono（WebEx/NetMeeting の再エンコード）。`mlx-whisper` large-v3-turbo で 29 分 49 秒かけて 3,003 セグメントを
生成したが内容は反復ハルシネーション（"the one, the one…" 等）。+24 dB 増幅して 1 区間のみ再試行しても回復せず。
→ **本站は「画面」を根拠に作成**（220 枚の代表画面＋`curriculum.md`）。ナレーション由来の記述は無い。

## 1.5 本次セッションの変更点（2026-09-12 夕方・引き継ぎ用）

**新規**: `sap_sd/`（動画 `录像45 Sales order processing.mp4` 準拠の SD 受注処理站。11 ページ / 45 手順ステップ / 65 画面 / 3 Excel / 学習WBS 111 タスク）。

**共有ツールの変更（他 5 站に影響しうる箇所）**
- `make_hub_page.py`: SITES/ORDER に `sap_sd` を追加（**先頭 = 学習路線 ①**）。フッターの站リンクと学習路線・職種別ショート路線の文言も更新。
- `make_wbs_xlsx.py`: SITES に `sap_sd` エントリを追加（label/code/SD、overview_checks・concept_checks・records・finish_checks）。
- `verify_all_sites.py`: SITES に `sap_sd` を追加。
- `export_gui_capture_list.py`: SITES に `sap_sd` を追加し、`code` マッピングに `"sap_sd": "SD"`（出力名 `SD_画面撮影リスト.*` にするため）。
- `tools/README.md`: 「6 个 SAP 培训站」に更新し `sap_sd/` を追記。
- いずれも実行済み: `verify_all_sites.py` → **6 站すべて OK**、`index.html`（ハブ）再生成済み。

**内容の修正（動画の画面記録に合わせた）**
- インコタームズ: スライドは `FOB`／実機デモは `CIF Berlin`。**同一項目が動画内で 2 通り**であることを明示（index・concept・handson-1・handson-2 の alt）。
- `VOV8` の詳細は `OR` ではなく **`CR`（Credit Memo Request）** を実演している旨を C1 に注記。
- 得意先変更時に **「Information: New pricing carried out.」** が出ることを handson-2 の手順に追加。
- `Last Documents for a Customer` のチェックは **Quotation / Order / Delivery / Credit memo request** に修正（C5 ④）。
- つまずき: 共有 WBS 抽出器は h2 に「チェック」を含む節を验收扱いにして**行を落とす**ため、`1-4 保存と伝票フロー（不完全性チェック）` → `（不完全性の検証）` に改名（5→4 行の欠落を修正）。

**画面イメージ**: `tools/gui_spec.d/*.json`（ページ単位の分片）→ `tools/gui_spec_build.py` → `gui_spec.json` → `make_gui_mockups.py`。65 画面・45/45 ステップ。
`check_gui_overlap.py` を再実行したところ **3 箇所の実重なり**（handson-3 の表の日付セル上に注記）を検出 → 注記を表の下へ移動して **0 箇所**に。

**転写（ASR）は断念・記録済み**: 音声は全体 −42 dBFS・AAC 169 kbps mono の再エンコード。`mlx-whisper` large-v3-turbo で 29 分 49 秒／3 003 セグメント生成したが反復ハルシネーション。+24 dB 増幅の 1 区間再試行でも回復せず。**再実行しないこと**（詳細は `sap_sd/README.md`）。

**スナップショット**: `_snapshots/sap_sd_YYYYMMDD_HHMM.tar.gz`（站単体・`*.mp4` と `work/audio` を除外）、`_snapshots/sap_training_sites_*.tar.gz`（全站・`*.mp4` と `_snapshots` を除外）。

## 1.6 本次セッションの変更点（2026-09-12 夜）— `sap_sd_cn`（中国語・全模块手册站）

**新規**: `sap_sd_cn/`（13 ページ / 6 模块 / 222 任務 / 879 手順ステップ / 画面引用 1369・去重 1209 ファイル 20.7 MB / Excel 9 sheet）。

**この站だけ性格が違う**: 素材は Excel でも録画でもなく **Word 文档 `S4.docx`**（425 页・md5 `8d52c85f6957b001dc078a8e3ff75e5b`。`sap_sd/100H_S4_中国語_拆分文件_合并文件.docx` と同一ファイル）。
内嵌画像 1385 枚のうち操作画面にあたる 1369 処を抽出して使う。**生成 SVG ではなく実機スクリーンショット**なので、
他の 6 站にある `tools/gui_spec.json` / `assets/gui/*.svg` / 「画面イメージ」注意書き / 撮影差し替えの仕組みは**持たない**。

**パイプライン（すべて站内の `work/` と `tools/` に閉じている）**
```
S4.docx → work/parse_docx.py → work/build_model.py（模块→任務→テキストブロック）
        → work/extract_images.py（assets/img/<mod>/tNN/ へ语义命名 + 内容去重 + アイコン除外）
        → work/build_site_model.py（手順ステップ化 / IMG 路径 / T-code / 入力値 / 笔记分類）
        → tools/build_pages.py（13 页）+ tools/make_cn_xlsx.py（9 sheet）
検証: tools/verify_site_cn.py（站专用）＋ 共有の skill scripts/verify_site.py
```

**資料の性質から来る処理（他站では不要だったもの）**
- 原文は「短い説明 + スクリーンショット」型で、画面だけの手順も多い → その場合は
  「按上一屏继续操作（画面 N）」と明示し、**推測で文を足さない**。
- 文末の 1 セクションは**スキャン頁**（OCR 化け）→ 「連続して中文が出てこない行」を塊で除去し、
  読める「问题 / 思路 / 解决方法」と画面だけ残した。
- T-code 抽出は正規表現 + ストップリスト（`CODE` `COPY` `CLIENT` `UI114` `WJ14` `FS217` 等の
  化け由来トークンを除外）→ **64 個**が残る（速查表と自测の選択肢に使う）。

**共有ツールへの登録（他站に影響しない形で）**
- `tools/make_hub_page.py`: SITES/ORDER に `sap_sd_cn` を**先頭**で追加（学習路線 ⓪）、
  站数表記を可変化、hero に「うち 1369 张は実機スクリーンショット」を追記、
  スタンス欄に「sap_sd_cn だけは実機截图」の box を追加。
  **SVG を作らない站のための上書き**として `<site>/tools/hub_stats.json`（build_pages.py が生成）を読む
  ようにした（無い站は従来どおり実ファイルから数える＝6 站の表示は不変。`diff` で確認済み）。
- `tools/verify_all_sites.py` / `verify_gui_figures.py` には**入れていない**（この 2 つの契約は
  「各手順ステップに生成 `figure.gui` + 画面イメージ表記」で、実機截图 + `figure.shot` の本站には合わない）。
  代わりに站専用の `tools/verify_site_cn.py` が同等以上（画像実在 / 锚点 / nav / 计数 / quiz 整合）を検査する。
- `training/index.html`（ハブ）: この時点では 7 站 74 页 / 1107 步 / 1776 画面。
  **その後、並行セッションが `sap_sd_jp`（同じ `S4.docx` の日本語版・14 页）を追加**（→ §11）ので、
  現在のハブは **8 站 88 页 / 1986 手順ステップ / 3145 画面**（うち 2738 が `sap_sd_cn` + `sap_sd_jp` の実機截图）。
  ハブを再生成しても両站とも掲載される（両站が自分で `tools/hub_stats.json` を書くため）。

**検証（本セッションで実行したもの）**
```
cd ~/Desktop/work/training/sap_sd_cn
python3 tools/verify_site_cn.py            # → RESULT: PASS（img 1369 / 锚点 / nav 13 页一致 / quiz 30 题）
python3 ~/.hermes/skills/.../verify_site.py .   # → PASS: 13 pages, nav identical, 1 active each, tags balanced
cd .. && python3 tools/verify_all_sites.py      # → 6 站すべて OK（既存站は不変）
python3 tools/make_hub_page.py                  # → index.html 再生成
```

**スナップショット**: `_snapshots/sap_training_sites_8sites_<TS>.tar.gz`
（共有の `tools/make_snapshot.sh` が 8 站ぶんを 1 本にまとめる。`TS` を渡せば同名で再作成できる。
除外: `*.docx`（素材）・`*.mp4`・`<site>/work/*`（sap_sd_cn は docx_extract と render のみ）・
`assets/gui_png/*`・`*_画面PNG.zip`・`*_講義用画面集.pdf`・`*_学员用記入シート.pdf`）。

### 中断・再開用メモ（`sap_sd_cn` の現在の状態）

- **完成している**（このセッションで検証済み・2026-09-12 22:0x 以降 `sap_sd_cn/` は誰も触っていない）:
  13 页の HTML＋ `S4CN_手順書_学習WBS.xlsx`（9 sheet）＋ `README.md`。素材層（`work/*.py` → `work/site_model.json`）と
  生成器（`tools/build_pages.py` / `tools/make_cn_xlsx.py`）と専用検証器（`tools/verify_site_cn.py`）が揃っている。
- **再開時にまず叩くコマンド**:
  ```bash
  cd ~/Desktop/work/training/sap_sd_cn
  python3 tools/build_pages.py && python3 tools/make_cn_xlsx.py     # 再生成（冪等）
  python3 tools/verify_site_cn.py                                    # → RESULT: PASS が期待値
  cd .. && python3 tools/verify_all_sites.py                         # → 既存 6 站すべて OK
  ```
  `work/docx_extract/` を消しても `work/parse_docx.py` から再生成できる（`S4.docx` は站内に残してある）。
- **未着手（次にやると良い順）**:
  1. モジュール別の「講義用画面集 PDF」（1 画面 1 页・原文件名入り）— Chrome 印刷は直列実行が必要。
  2. モジュール別の配布シート（讲师版＝画面＋解説／学员版＝画面＋記入欄）。
  3. 実機で新しく撮ったスクリーンショットへの差し替えリスト（`3_画面索引` の原文件名が対応表になる）。
- **触ってはいけない前提**: `sap_sd_cn/assets/{style.css,main.js,quiz.js}` は共有デザインシステムのコピー。
  見た目の追加は `assets/s4cn.css` / `assets/s4cn.js` にだけ書く（他站と共有しているファイルは書き換えない）。

### `training/` ルートは **公開リポジトリ `sap-consult` に push 済み**（2026-09-12 23:1x）

- `git init -b main` + `origin = https://github.com/raysource/sap-consult.git`（**PUBLIC**）。
  push 済み HEAD = `982f38374ae381015e6512e50234b27ec2c75fe9`（`ls-remote` と `gh api commits/main` の両方で一致を確認）。
- 内容: **3669 blobs / 約 189 MB**（API 実測）。内訳の抜粋: `sap_sd_jp` 1310・`sap_sd_cn` 13 页 + 実機截图 1209・
  `*.svg` 画面イメージ 410・`*.xlsx` 26。**除外が効いている**ことも確認済み
  （リポジトリ内に `*.docx` / `*.mp4` / `*.zip` / `work/docx_extract` / 配布 PDF は **無し**）。
- `.gitignore`（ルート）: `*.mp4`（録画 114 MB）・`*.docx`（S4.docx 等）・`*.zip`・`_snapshots/`・
  `*/work/docx_extract/`・`*/work/render/`・`*/assets/gui_png/`・`*/画面PNG.zip`・`*/講義用画面集.pdf`・
  `*/学员用記入シート.pdf`・`node_modules/`・`.DS_Store`。
  つまり「生成すれば戻る派生物」と「配布物 PDF」は公開リポジトリに入れていない（必要なら `git add -f` で追加可能）。
- **入れ子リポジトリの扱い（重要）**: `git add` は**入れ子リポジトリ内のパスに対して静かに何もしない**
  （git 2.39 で実測: `git add -f sap_sd_cn/README.md` → exit 0 だが `git ls-files` は空）。
  そこで plumbing で普通のファイルとして取り込んだ:
  `git hash-object -w --stdin-paths` → `git update-index --add --index-info`。
  親リポジトリ側で計算した blob SHA が**入れ子リポジトリの索引の SHA と一致**することをアサートしている（内容一致の証明）。
  この手順は再利用できるよう `tools/include_nested_repo_files.sh` として残した
  （`sap_sd_cn/`＝プライベートリポジトリ、`nihong/`＝リポジトリ、はそれぞれの .git を保持したまま、
   親の `sap-consult` にも実ファイルとして入っている）。
- **注意**: `sap-consult` は **public** なので、`PROGRESS.md` を含む作業メモも公開されている
  （トークン等の秘密は含めていない）。教材の実機スクリーンショットも公開状態になった（ユーザー承認済み）。
  非公開に戻す場合は `gh repo edit raysource/sap-consult --visibility private`。

### 保存（2026-09-12 23:2x）— 「保存进度」の内容

この時点の保存物は 3 つ。どれも**自分で読んで確認した**結果をここに書いている（人の報告を転記していない）。

1. **git（ローカル + GitHub）**
   - `training/` ルート: `main` = `69f83cb`（`f367e81` → `982f383` → `69f83cb` の 3 コミット）、
     ワーキングツリーはクリーン（未コミット 0 行）。
   - 公開リポジトリ `raysource/sap-consult` の HEAD は `69f83cb`（`git ls-remote` と `gh api commits/main` で一致確認）。
   - `sap_sd_cn/` は別リポジトリで private `raysource/sap-s4hana-cn-training` に `a3b428e` まで push 済み（`ahead=0`）。
2. **スナップショット（オフライン復元用）**
   - `_snapshots/sap_training_sites_8sites_<TS>.tar.gz`（`TS` を渡して同名再作成可能）。
   - 検算: アーカイブ内 **3152 entries / 38 MB**・`sap_sd_cn/assets/img` **1209**・`sap_sd_jp/assets/img` **1209**・
     `.git` エントリ **0**・`*.docx` / `*.mp4` **0**（`tar -tzf` で実測）。
3. **サイト自体の検証状態**
   - `sap_sd_cn/tools/verify_site_cn.py` → `RESULT: PASS`（222 任务 / 1369 画面引用 / 索引 222 行 / quiz 30 题 / 锚点・nav 一致）
   - 技能 `verify_site.py` → `PASS: 13 pages, nav identical, 1 active each, tags balanced, quiz keys valid`
   - `tools/verify_all_sites.py` → 既存 6 站すべて OK（実機截图の 2 站は対象外・`hub_stats.json` で数を申告）

**再開時に最初に叩くもの**（コピペ用）:
```bash
cd ~/Desktop/work/training
git log --oneline -3 && git status --short          # どこまで保存したか
python3 tools/verify_all_sites.py                   # 既存 6 站の健全性
cd sap_sd_cn && python3 tools/verify_site_cn.py      # 中文站の健全性（PASS が期待値）
```

**未着手のまま残っていること**（次にやる候補・優先順）:
1. `sap_sd_cn` のモジュール別「講義用画面集 PDF」（1 画面 1 页）／配布シート（Chrome 印刷は直列実行）。
2. `sap-consult` に GitHub Pages（public なので可）＋ `index.html` ポータル。
3. 配布物 PDF / PNG ZIP（`.gitignore` で除外中）を公開リポジトリに載せるか判断。

### 保存（第 2 回・2026-09-12 23:38）— 併走セッションとの「同名スナップショット」衝突

- git: `training/` は `f7a8f10` まで push 済み（`git rev-parse HEAD` == `git ls-remote` == `gh api commits/main`）。
  `sap_sd_cn/` は別リポジトリで private に `a3b428e`（`ahead=0`）。
- スナップショットは 3 本ある（どれも `gzip -t` OK / 3153 entries / 38 MB で中身はほぼ同一）:
  | ファイル | 出自 | 備考 |
  |---|---|---|
  | `_snapshots/sap_training_sites_8sites_20260912_233856_cn.tar.gz` | **本セッション** | **詳細検算済み**（下記） |
  | `_snapshots/sap_training_sites_8sites_20260912_233859.tar.gz` | 併走セッション（1 秒後に作成） | `gzip -t` OK / 3153 entries |
  | `_snapshots/sap_training_sites_8sites_20260912_2338.tar.gz` | 分単位の既定名（両者が同時に書いた可能性） | 今は `gzip -t` OK / 3153 entries |
- 本セッションが作った 1 本の検算結果: `sap_sd_cn` 画像 **1209 == disk**、`sap_sd_jp` 画像 **1209 == disk**、
  `.svg` **407 == disk**、`.xlsx` **20**、`.git` **0**、`*.docx/*.mp4/*.zip` **0**、`PROGRESS.md`・`index.html` **あり**。
- **学び（重要）**: `tools/make_snapshot.sh` の既定の出力名は**分単位**（`..._8sites_YYYYMMDD_HHMM.tar.gz`）。
  同じディレクトリで 2 セッションが同時に「保存」すると**同名衝突**し、**書きかけの tar を読んで「壊れている」と誤判定**する
  （実際に起きた: `gzip: data stream error` → 直後に同じファイルが VALID になった。原因は書き込み中の読み取り＋二重書き）。
  対策:
  ```bash
  TS="$(date +%Y%m%d_%H%M%S)_cn" TS="$TS" bash tools/make_snapshot.sh   # 秒＋接尾辞で一意化（スクリプトは TS を尊重する）
  gzip -t <out> && tar -tzf <out> | wc -l                               # 検算は gzip -t → 件数 の順
  ```
  さらに「`ls -l` のサイズが秒ごとに変わる＝まだ書き込み中」なので、その間は読まない。
- 併走セッションが編集中の未コミット変更（`tools/README.md` +12 行、`tools/make_snapshot.sh` 1 行）は
  **あえて commit していない**（相手の作業中ファイルに触らない方針）。次の保存時に一緒に入れるか、相手の commit を待つ。

### 個別リポジトリの現状（git remote）

| ディレクトリ | remote | 可視性 | 状態 |
|---|---|---|---|
| `sap_sd_cn/` | `origin = https://github.com/raysource/sap-s4hana-cn-training.git` | **private** | 2 commit push 済み（`a3b428e`）、HEAD 一致を API / ls-remote で確認済み |
| `sap_cn/` | `origin = https://github.com/raysource/sap_cn_sd.git` | **public** | 3 commit push 済み、HEAD `f0bcc698`（`ls-remote` / `gh api` と一致、blobs 318 == tracked 318） |
| `training/`（ルート） | `origin = https://github.com/raysource/sap-consult.git` | **public** | remote のみ・未 push |

## 2. 検証（これが「できている」の根拠）

```bash
cd /Users/jason/Desktop/work/training

# 6 サイトを 1 表で棚卸し（構造＋GUI カバレッジ＋コンテナ健全性）
python3 tools/verify_all_sites.py            # → 「すべてのサイトで構造検証・GUI 図カバレッジとも OK」

# サイトごと
cd sapmto && python3 ~/.hermes/skills/productivity/sap-training-sites/scripts/verify_site.py .   # → PASS
cd .. && python3 tools/verify_gui_figures.py sapmto     # 手顺ステップの網羅（RESULT: PASS）
python3 tools/check_gui_render.py sapmto                # 実際に描画されるか（NG 0）
python3 tools/check_gui_overlap.py sapmto               # 注記が文字に重なっていないか（0 箇所）

# sap_sd（新規）も同じセットで検証済み: verify_site=PASS / verify_gui_figures=RESULT: PASS（45/45・65 図）/ overlap=0 箇所
# 注意: この環境では check_gui_render.py（Chrome headless）が起動待ちでタイムアウトする。
#       代替として `qlmanage -t -s 1180 -o <outdir> assets/gui/*.svg` でラスタライズし、目視で確認した（sap_sd は 6 枚抽查）。

# 再生成（冪等・何度でも）
python3 tools/make_gui_mockups.py sapmto      # spec → SVG → ページ挿入 + CSS
python3 tools/make_wbs_xlsx.py                # 全サイトの 学習WBS（受講者版）を再生成
python3 tools/export_gui_capture_list.py      # 画面撮影リスト（CSV/XLSX）
```

**直近の確認結果（13:00 時点、発展セクションの配図が入った後）**：5 サイトとも `verify_site` PASS、GUI カバレッジ 44/46/44/40/9 すべて一致（合計 183 ステップ / 342 画面）、
注記の重なり 0 箇所（CJK 幅を正しく見積もった検出器で再確認）、文字のはみ出し 0 件、
`sapmto`/`sapeto`/`saporderflow` は画素レベルの描画検証も NG 0（`sapmts`/`sapvc` は再生成後に再実行）。

## 3. 進行中／完了した作業

**4 エージェントすべて完了**（発展セクションの配図）。追加された画面と件数:

| エージェント | サイト | 追加内容 | 結果 |
|---|---|---|---|
| `sa-0-7b5f1328` | `sapmto/` | 発展 1〜5：VA01→自動指図（PP04）／品目カテゴリグループ切替（0001→Z001）／KKS1 と KO88／MD04 の購買依頼／VA02 変更と VL09 取消 | 39→44 步 / 73→82 图 |
| `sa-1-8c5be191` | `sapeto/` | 発展 1〜6：CNE1→KKA2／CJ88→CJIC／CJ31→CJBV／請求計画と VF01(70%)／CN25／ME51N（WBS 直手配） | 40→46 步 / 87→97 图 |
| `sa-2-d5631d37` | `sapmts/` | 5-8 発展課題：MD04 戦略 10（PIR 消費なし）と 手配タイプ F（購買依頼）。5-6 故障対照表は参照表なので**意図的に見送り** | 43→44 步 / 67→69 图 |
| `sa-3-d848d4d7` | `sapvc/` | 5-3 故障対応の 3 画面（CU50 / CU03 / CU02）＋ 5-5 の SET 処理（MM01 0004・CU42） | 38→40 步 / 69→74 图 |

エージェントが**見つけて直したこと**（重要）:
- `sapeto/tools/gui_spec_build.py` は再ビルド時に**手で足した「配置前的準備」キーを黙って落としていた**（86 vs 87 画面）→ `merge_existing()` ガードを追加して解決。生成器と実ファイルが二重管理になっているサイトは要注意。
- `check_gui_overlap.py` は **CJK の文字幅を過小評価**していた（全角を 0.58em と見積もり）→ 検出器と生成器が同じ推定式を共有していたため**両方が同じ嘘をつき、64 箇所の重なりが見えていなかった**。CJK 対応の `text_w()`（全角 1.0em・半角 0.52/0.60em）を両方に入れて再生成 → **5 サイトとも 0 箇所**。
- `sapmts` のエージェントは、シナリオに仕入先・購買組織が無いため **ME21N の項目名を発明せず**、MD04 の購買依頼行で表現するに留めた（正しい判断）。

**最終検証（完了）**：全 342 画面の画素レベル描画検証 → **5 サイトすべて `NG 0`**
（`sapmto 82 / sapeto 97 / sapmts 69 / sapvc 74 / saporderflow 20`）。途中で二重に走っていた検証プロセスを整理し、単プロセス直列で回した結果です。

## 4. 再開時にやること（チェックリスト）

1. 4 エージェントの結果を確認（`delegate_task action='list'`、または上記ライブログの末尾）— **残りは sapvc のみ**
2. `python3 tools/verify_all_sites.py` → 全 OK か（発展配図で**ステップ数が増える**ので、カバレッジ欄が増えているのが正常）
3. `python3 tools/check_gui_overlap.py --all` → 0 箇所か
4. `python3 tools/check_gui_render.py <site>` を 5 サイト分（遅いので background + notify 推奨）→ NG 0 か
5. `python3 tools/export_gui_capture_list.py` → 撮影リストを再出力（現在 316 行 → 発展配図で ~345 行見込み）
6. `python3 tools/add_gui_note.py --all` → 新しいページに「画面イメージ（実機ではない）」注意書きが入っているか
7. `python3 tools/make_hub_page.py` → 索引页の数字を最新化（ページ/ステップ/図数を自動統計）
8. もう一度スナップショットを取る（下記 §6）— 索引页と PROGRESS.md も含める

## 5. 既知の未達・注意

- **発展セクションの配図は進行中**（§3）。完了前は「すべての操作ステップに図がある」とは言えない。
- 画面イメージは **SAP GUI の標準レイアウトを再現した図**であり、**実機のスクリーンショットではない**。
  各サイトの README とページ内 `gui-note` に明記済み。実機画像に差し替える運用は
  `tools/swap_gui_images.py <site> --apply`（同名 `.png` を `assets/gui/` に置く）。
- 業務サイトは**コンパイル検証できない**ため、標準値は「出典つき」か「通常は〜（自システムで確認）」で記載。
  断定を避けたフィールド名は各エージェントが報告済み（例: `OVZI` の origin 値、`CO11N` の不良数量欄、`SDCOM-VKOND`）。
- `sapvc` の画素検証は一度 FileNotFoundError で落ちたが、これは**再生成と検証の並走によるファイル競合**（図の問題ではない）。再実行で解消。
- 同じサイトの HTML を**2 プロセスで同時に編集しない**（配図はファイル全体を書き換えるため後勝ちで壊れる）。

## 6. スナップショット（保存済み）

**最新**: `_snapshots/sap_training_sites_6sites_20260912_1714.tar.gz`（1.9MB / 585 ファイル: svg 407・html 62・xlsx 18・py 39）
生成は `bash tools/make_snapshot.sh`（`find` で対象を明示し、派生物＝`assets/gui_png/`・`*_画面PNG.zip`・
`*_講義用画面集.pdf`・`*_学员用記入シート.pdf`・`*.mp4`・`sap_sd/work/` を除外。これらは生成コマンド 1 本で再現可能）。
**注意**: tar の `--exclude='*/…'` はこの環境（bsdtar）で期待通りに効かず、193MB の巨大アーカイブを作った事故がある。必ず `make_snapshot.sh` を使うこと。

| ファイル | 取得時刻 | 内容 | 整合性 |
|---|---|---|---|
| `_snapshots/sap_training_sites_20260912_1257.tar.gz` | 12:57 JST | PROGRESS.md + tools + 5 サイト（493 エントリ / html 50・svg 342・xlsx 15・py 27、1.47MB） | `gzip -t` OK、svg 数が当時の実ファイル数と一致 |

| `_snapshots/sap_training_sites_20260912_1302.tar.gz` | 13:02 JST | 同上（PROGRESS.md を更新した版） | `gzip -t` OK |
| `_snapshots/sap_training_sites_final_20260912_1339.tar.gz` | 13:39 JST | **最終版**：PROGRESS.md ＋ 索引页（index.html, assets/）＋ tools ＋ 5 サイト（499 エントリ / html 51・svg 342・xlsx 15・py 28、1.49MB） | `gzip -t` OK ／ `/tmp` に展開して中身を実確認済み（PROGRESS.md・索引页・hub.css・tools・各サイト・Excel すべて存在） |

| `_snapshots/sap_sd_20260912_1633.tar.gz` | 16:33 JST | **sap_sd（新規站）単体**: 11 ページ HTML ＋ 65 画面 SVG ＋ 3 Excel ＋ `tools/`（ページ生成器・gui_spec.d 分片・make_sd_xlsx）＋ `work/`（代表画面 220 枚・curriculum.md・inv_0..9.json）。`*.mp4` と `work/audio` は除外（21MB） | `gzip -t` OK |
| `_snapshots/sap_training_sites_final_20260912_1645.tar.gz` | 16:45 JST | **全站・最終版**: `PROGRESS.md` ＋ 索引页（`index.html`/`assets/`）＋ `tools/` ＋ **6 サイト**（610 エントリ / html 62・svg 407・xlsx 18・py 37・csv 6、1.9MB）。`sap_sd/work`・`*.mp4`・`rap/`・`sapgui/`・`nihong/`・`sap/`・`_snapshots/` は除外 | `gzip -t` OK、件数を実ファイルと突き合わせ済み（svg 342+65 / xlsx 15+3） |

> 途中で 133MB（`sap_sd` 全体＝源動画を含んだ）と 235MB（`node_modules` を含んだ）の tarball を作ってしまったが、**どちらも削除済み**。上の 2 本が正。

取り出し: `tar -xzf _snapshots/sap_training_sites_20260912_1302.tar.gz -C <任意のディレクトリ>`
**最終スナップショットは取得済み**（上表の `..._final_20260912_1645.tar.gz`）。復元コマンド:

```bash
tar -xzf _snapshots/sap_training_sites_final_20260912_1645.tar.gz -C <任意のディレクトリ>
```

これ以降に内容を変えた場合は、`python3 tools/make_hub_page.py && python3 tools/make_wbs_xlsx.py && python3 tools/export_gui_capture_list.py`
を実行してから、同じコマンドで `_snapshots/sap_training_sites_final_<日時>.tar.gz` を撮り直してください。
- このディレクトリは **git 管理外**（`rap/` 438MB・`sap_sd/` 129MB など無関係の大物が同居しているため）。
  git で履歴管理したい場合は、成果物 5 ディレクトリ＋`tools/` だけを対象に
  `git init` + `.gitignore`（`rap/ sap_sd/ sapgui/ nihong/ sap/ _snapshots/`）するのが安全。

## 7. 参照ドキュメント

- `tools/README.md` … ツールの使い方（生成・検証・差し替え・撮影リスト）
- `tools/make_hub_page.py` … 索引页（`index.html`）を実ファイルの統計値で生成
- `tools/GUI_SPEC_FORMAT.md` … 画面仕様 JSON の書き方と品質ルール
- 各サイトの `README.md` … そのサイトの構成・手順・Excel・画面イメージの説明
- スキル `sap-training-sites`（`~/.hermes/skills/productivity/sap-training-sites/`）… 作り方の手順と
  落とし穴（配図の挿入事故 7 項目、発展セクションを除外しないこと、など）。参照資料:
  `references/sap-sd-pp-mto-facts.md`、`references/sap-eto-ps-facts.md`、`references/sap-order-forms-comparison.md`

## 8. 実機スクリーンショット差し替え（フロー実証済み）

現場の実機で撮った画像に置き換える手順。**ツール側は自己テストで通してあります**
（`tools/test_swap_workflow.sh` → `RESULT: PASS`）:

```bash
# ① 撮影リストを見ながら実機で撮る（<CODE>_画面撮影リスト.xlsx / .csv、342 行）
#    列: # / サイト / ページ / ステップ / 画像ファイル / 差し替え後(.png) / 画面タイトル / T-code / キャプション / callouts / 撮影メモ

# ② 撮った画像を「差し替え後」の名前で置く
<site>/assets/gui/config_s01_1.png        ← 形式は png / jpg / jpeg / webp、大文字拡張子も可

# ③ 一括差し替え
python3 tools/swap_gui_images.py sapmto --status    # 何枚置けたか（進行状況）
python3 tools/swap_gui_images.py sapmto             # dry-run（対応表を表示）
python3 tools/swap_gui_images.py sapmto --apply      # src を .svg → .png に書換
python3 tools/add_gui_note.py sapmto --sync          # 実機画像だけになったページの注意書きを自動で外す

# ④ 検証（構造・網羅）
cd sapmto && python3 ~/.hermes/skills/productivity/sap-training-sites/scripts/verify_site.py .
cd .. && python3 tools/verify_gui_figures.py sapmto

# ⑤ 元に戻す
python3 tools/swap_gui_images.py sapmto --revert && python3 tools/add_gui_note.py sapmto --sync
```

**実証テストの中身**（`tools/test_swap_workflow.sh`）: saporderflow で 8 枚を「撮影済み」に見立て、
`--status` 8 枚検出 → `--apply` 8 枚書換 → `--sync` が **全図が画像になったページ（vc.html）から注意書きだけを外す** →
`verify_site` PASS・`verify_gui_figures` PASS → `--revert` で 8 枚戻し・注意書きも復元 → **compare/scenario-eq は元とバイト一致**。
（テスト中に見つけて直した不具合: `--revert` 単独実行が dry-run で止まっていた／注意書きの用語が既存 26 ページと不統一だった）

注意: 画像サイズは幅合わせで表示されるため縦長でも崩れませんが、幅 800px 未満・縦横比が 1180:760 と大きく違う場合は
警告が出ます（拡大で粗くなる／縦長で見づらい）。実機の SAP GUI は概ね 1200×800 前後で撮ると揃います。

## 9. 写真が無くても講義で使える形にする（PNG / 画面集 PDF）

実機スクリーンショットが無い環境でも配布・投影できるよう、生成図から直接資料を作れるようにしました。

```bash
python3 tools/export_gui_png.py <site> --scale 2 --zip
#   → <site>/assets/gui_png/*.png（2 倍解像度・スライドや Word にそのまま貼れる）
#   → <site>/<CODE>_画面PNG.zip（一括）
#   → <site>/<CODE>_講義用画面集.pdf（手顺ごとに 1 セクション。画面＋キャプション＋赤番号注記＋確認 T-code）
python3 tools/export_gui_png.py <site> --pdf-only      # PDF だけ作り直す
```

- 例（実測）: `sapmto` = PNG 82 枚（失敗 0）／`MTO_画面PNG.zip` 9.6MB／`MTO_講義用画面集.pdf` 8.3MB（82 画面）
- 画面集 PDF は 2 倍 PNG を埋め込むので軽い（SVG 直埋めだと 20 画面で 32MB になったため切替）。A4 横向き・1 手顺セクションごとに改ページ。
- スライドに使うなら PNG、配布なら PDF、どちらも実機写真は不要です。

### 補足（ツールの対応範囲をそろえた）
このセッションで `check_gui_overlap.py` / `add_gui_note.py` / `export_gui_png.py` の SITES リストに
**`sap_sd` を追加**しました（`--all` で 6 サイト全部が対象になる）。`verify_all_sites.py` / `make_hub_page.py` /
`make_wbs_xlsx.py` / `export_gui_capture_list.py` は別セッションで既に追加済みです。

### 注意（Chrome の競合）
`check_gui_render.py` / `export_gui_png.py` は Chrome を 1 枚ずつ起動するため、**同時に走らせると起動待ちでタイムアウト**します
（別セッションでも発生）。直列実行が前提。並行させたい場合は `--limit` で分割してください。

## 10. 講義資料の仕上げ（画面集 PDF のページ割り）

- **1 画面 = 1 ページ（実測 1.01）に修正**。経緯と結論:
  1. 当初は `width:100%` のみ → 2 倍解像度（2360×1520）の画像が A4 横の印刷可能高さを超え、**図がページをまたいで切れた**
     （MTO 82 画面 → 177 ページ）。`max-height` を足しても 171 ページでほぼ改善せず。
  2. 制御実験（同じ CSS で figure を 5 枚だけ刷る）では **1.00 ページ/図**。つまり CSS 単体は正しいのに、実際の
     画面集では ~2 ページ/図になる → Chrome の自動ページ割りが、節見出しと図の組み合わせ・`break-inside: avoid` の
     押し出しで空白ページを混ぜていた（`page-break-after: always` と節の `page-break-before` の二重指定でも別の症状）。
  3. 決定的な方式に変更：**印刷可能領域と同じ固定高（188mm）の `.page` を作り、その中に 1 画面を入れて
     `page-break-after: always`**。節見出しはその節の最初のページに同居。これで 6 サイトとも **1.0 ページ/画面**
     （合計 413 ページ / 407 画面）になり、画像は絶対に分割されない。
  教訓: Chrome の print-to-pdf は「内容の高さ × 自動割り」に依存すると再現性が低い。
  **高さを固定した箱で割る**のが確実（`export_gui_png.py` / `make_handout_pdf.py` の両方に適用済み）。
- **讲师版 / 学员版**: `tools/make_handout_pdf.py <site> --both`（どちらも 1 画面 = 1 ページ）
  - `<CODE>_講義用画面集.pdf` … 画面＋キャプション＋赤番号注記＋確認 T-code（讲师が配る用）
  - `<CODE>_学员用記入シート.pdf` … 同じ画面だが注記は空欄（自分の言葉で埋める欄＋メモ罫線）
  両版とも `assets/gui_png/*.png` を使う（先に `export_gui_png.py <site>` を実行しておくこと）。
- **Chrome は直列で**: `check_gui_render.py` / `export_gui_png.py` / `make_handout_pdf.py` はそれぞれ Chrome を
  1 枚ずつ起動する。並行させると起動待ちでタイムアウトするため、キューを分けて順に回すこと（本セッションでは
  「渲染校验 → PNG 書き出し → PDF 生成」の順に直列で実行した）。

## 11. `sap_sd_jp`（SAP S/4HANA 日本語実習サイト・中国語教材の日本語版）— 2026-09-12 深夜

**新規**: `sap_sd_jp/`（14 ページ / 6 モジュール / 222 タスク / 879 手順ステップ / 画面参照 1369・実ファイル 1209 / 20.7 MB / Excel 9 シート）。
素材は `sap_sd_cn` と**同一ファイル**の Word 文档 `S4.docx`（425 页・md5 `8d52c85f6957b001dc078a8e3ff75e5b`。`sap_sd/100H_S4_中国語_拆分文件_合并文件.docx` とも同一）。
つまり **中国語站の日本語版**で、画面は同じ実機スクリーンショット（中国語インターフェース）をそのまま使い、本文だけを日本語にした。

### この站の設計（中国語画面を日本語で教えるための 3 点）

1. **各手順ステップに「原文（中国語）」の折りたたみ**（`<details class="orig">`）= 原教材の一文そのまま。画面と手順を突き合わせる根拠。
2. **入力値表を 3 列化**（項目（日本語）/ 画面の中国語 / 教材の設定値）。中国語画面のどの項目かがその場で分かる。
3. **`glossary.html` 用語対照表（日本語 ⇔ 中国語画面）** = 基本操作 21 項目（保存/回车/执行/新条目/选中/显示-更改/返回-退出…）＋ SAP 用語（`work/ja/glossary.json` の約 230 語）＋ **IMG パス 203 件の日本語訳 ⇔ 中国語原文**。
   パスは画面と同じく中国語で書かれているため、日本語システムでたどる時の実用品になる。
   加えて IMG パスの直下に「原教材の中国語パス」を小さく併記（タスク単位）。

### 翻訳パイプライン（すべて站内 `work/` に閉じている・再実行可能）

```
work/parse_docx.py …（sap_sd_cn と同一）→ work/site_model.json（中国語モデル）
work/i18n.py collect all    → work/ja/{src,model}_atoms.json + _refs.json     （2102 アトム / 69,707 字）
work/i18n.py batches 5000   → work/ja/batches/*.json（15 バッチ）
   （翻訳は work/ja/BRIEF.md の規約 + work/ja/glossary.json の用語表で実施 → work/ja/out/*.json）
work/i18n.py merge          → work/ja/{src,model}_map.json（missing 0）
work/i18n.py check          → 668 リテラルのマーカー整合 0 失敗
work/i18n.py apply all      → 生成コードを日本語化（原本は work/ja/orig/）+ work/site_model_ja.json
work/jp_finalize.py         → lang=ja / assets/s4jp.* / MODEL_ZH 読み込み / NAV に「用語」 / build_pages に glossary
work/jp_finalize2.py        → 前后台の比較は中国語定数（后台/前台）、表示は fb_ja に統一
tools/build_pages.py        → 14 HTML        tools/make_jp_xlsx.py → S4JP_手順書_学習WBS.xlsx
```

- **アトム = 1 行**。`{id: 中国語}` と `{id: 日本語}` の 2 つのマップだけが翻訳の実体なので、
  訳を直したいときは `work/ja/*_map.json` を編集して `apply` を再実行するだけでよい（冪等）。
- **マーカー方式が肝**: HTML タグ・Python の `{...}`・実体参照を `⟦0⟧⟦1⟧…` に置換して翻訳に出し、
  戻す時に「各マーカーちょうど 1 回」を検証する。**訳文がコードやマークアップを壊せない**（今回 0 失敗）。
  当初 `check()` が「翻訳された行だけを連結」して検証していたため 13 件の偽 FAIL が出た（タグだけの行が未訳のため）。
  apply と同じ手順（リテラル全体を組み直す）に直して 0 になった。
- **ハマりどころ**: 翻訳は「`后台`/`前台`」の**文字列リテラル**も日本語化するため、`t['fb'] == '后台'` の比較が壊れる
  （件数が 0 になる）。データ側は中国語のままにし、比較は `FB_IMG`/`FB_FRONT` 定数、表示は `fb_ja` に寄せて解決（`jp_finalize2.py`）。
- **CSS/JS の共通部品はサイト内コピー**を日本語化した（`assets/s4jp.js` / `main.js` / `quiz.js` / `s4jp.css`）。他站の `main.js` は触っていない。

### 検証（このセッションで実行した実測）

| コマンド | 結果 |
|---|---|
| `python3 tools/verify_site_jp.py` | **PASS** — img 1369 / zoom 1369 すべて実在、アンカー全解決、nav 14 リンク同一・active 1、`</article>` 1 個、タグ均衡、クイズ 30 問のキー一致、tasks 222・画面 1369・ワークシート空欄 696 |
| `python3 ~/.hermes/…/scripts/verify_site.py .` | **PASS**（14 pages, nav identical, copy buttons, quiz keys） |
| `python3 work/qa_ja.py` | 簡体字の残り **index/prep/tcode/tasks/instructor/worksheet/quiz = 0 字**。モジュールページの残りは**すべて意図的な「画面の中国語」列**（合計 36 字） |
| `python3 tools/make_hub_page.py` | ハブを **8 站**に更新（`sap_sd_jp` を ⓪ に、`sap_sd_cn` は「原文中文」として 1 つ後ろ）。他の 6 站のカードは差分なし、死リンク 0、`**` 残り 0 |
| `python3 tools/verify_all_sites.py` | 既存 6 站すべて OK（`sap_sd_jp`/`sap_sd_cn` は**登録しない**＝実機スクリーンショット站のため。代わりに `tools/hub_stats.json` で数を申告） |

- 画面の目視: Chrome headless で `index.html` と `fi.html` のタスク 01〜03 を切り出して確認
  （3 列の入力値表・「原文」折りたたみ・「原教材の中国語パス」・図注がすべて想定どおり。切り出しは `work/render/` に置き、站のルートには置かない）。
- **翻訳の当て方**: 15 バッチを 10+5 のサブエージェントで並列翻訳し、構造検証（キー集合・マーカー多重度・改行なし）を全件で自分で再実行した（problems 0）。

### 用語の統一（サブエージェント並列翻訳の副作用と、その直し方）

15 バッチを別々のエージェントに訳させたため、**同じ中国語が違う日本語になっていた**箇所が 3 つ出た（いずれも原教材の機械翻訳由来）:

| 中国語 | 出ていた訳 | 統一後（採用理由） |
|---|---|---|
| 商店底价控制 | ショップフロア制御 / ショップフロアコントロール / 製造指図管理 | **ショップフロアコントロール**（Shop Floor Control の直訳崩れ。日本語 SAP の IMG 名） |
| 结算参数文件 | 決済パラメータファイル / 決済プロファイル | **決済プロファイル**（日本語 SAP 標準の決済プロファイル） |
| 生产成本 | 生産原価 / 製造原価 | **製造原価**（日本語会計の標準語。勘定名も統一） |

- 直し方は **`work/ja/model_map.json` を正規表現で置換 → `python3 work/i18n.py apply model` → `build_pages.py` → `make_jp_xlsx.py`**。
  モデル側は冪等なので、これで 18 値が直り、全 14 ページで 変種 0 / 統一後 63・32・22 になった（検証済み）。
  **`src_map.json` 側は今回 0 件**だったのでコードの手編集は不要だった（chrome 側に変種が出たら、apply は使えないので直接編集する）。
- 併せて `work/ja/glossary.json` にこの 4 語を追加し、`glossary.html` の「混同しやすい語」表に 3 行
  （商店底价控制→ショップフロアコントロール / 结算参数文件→決済プロファイル / 生产成本→製造原価）を追記した。
- 一般則: **並列翻訳では必ず「用語の横断チェック」を後で 1 回やる**（同じ中国語の訳が何通りあるか機械的に数える）。
  用語集を先に作っても、子エージェントは未知語で揺れる。

### IMG パス表記の統一（同語多訳の機械監査 — 2026-09-12 深夜 追記）

並列翻訳の副作用をもう一段洗うため、**同語多訳の横断監査ツール**を追加した:
`python3 work/term_audit.py`（① IMG パスのセグメント整列 ② 用語集の訳語が本文に無い行 ③ 概念ごとの表記揺れ）。

- 初回実行: 整列できた中国語セグメント 645 種のうち **68 種が揺れ**ていた。
  例: `物料管理` → 品目管理（MM）×66 / 品目管理×9、`控制` → 管理会計（CO／Controlling）×43 / 管理会計×18、
  `期末结算` → 期末決算 / 期末決済、`业务伙伴` → 業務パートナ / ビジネスパートナ、`分配` → 配賦 / 割当。
- 修正は `work/normalize_paths.py`（**中国語セグメントをキーにした正規形テーブル**、パス内だけに適用）。
  1 回目で model 173 + src 1 値、2 回目で 18 値 → **揺れ 68 → 5 種**。残り 5 は意図的なもの
  （`订单` は文脈で 指図／受注伝票／購買発注 に分かれる／引用符付きメニュー名／文章中の「→」）。
- 重要な判断: **エンタープライズ構造・単一機能の `分配` は SPRO の "Assignment"＝日本語メニューは「割当」**（配賦ではない）。
  一方 CO の分配循環は配賦のまま。曖昧な語（`订单` など）はテーブルに入れず温存するのが原則。
- パス内では用語集の補足（`品目管理（MM）` 等）を外して**メニュー名そのまま**にする（学習者はその名前で画面を探すため）。
  本文（prose）側の補足は残す。

## 12. 全站の用語統一（表記揺れの監査と一括修正）— 2026-09-12 深夜

**新しい共通道具**: `python3 tools/term_consistency_audit.py [site…]`（既定 = 7 站 + ハブ）
① 概念ごとの候補表記の出現数（サイト別） ② 長音符ゆれ（ユーザ/ユーザー 等） ③ 全角/半角の併存
④ 簡体字（中国語）の残り。**同じ語を 2 通り以上で書いている概念だけ**を「要確認」として出し、
「別概念なので直さない」ものは `KEEP_NOTES` に理由付きで表示する（次に触る人が同じ判断を繰り返さないため）。

### 直したもの（`tools/fix_term_drift.py` + `fix_term_drift2.py`、計 93 箇所）

| 直した表記 | → 統一後 | 主なサイト |
|---|---|---|
| 明細タイプ / 項目カテゴリ / 請求項目カテゴリ | **明細カテゴリ / 請求明細カテゴリ** | sapmts, sapmto |
| 受入予定 / 受入処理時間 / 受入数量 | **入庫予定 / 入庫処理時間 / 入庫数量** | sapmts, sapmto |
| ワークセンター | **作業区** | sapeto |
| 顧客（+顧客契約・顧客グループ） | **得意先** | sap_sd(42), saporderflow(15), sapvc, sapeto |
| 資材伝票 | **品目伝票**（MB03） | sapvc(16) |
| 科目（転記科目・借方/貸方の科目） | **勘定**（転記先の勘定） | sapmts |
| 払出（払出しになる・材料払出） | **出庫** | sapeto, sapvc |
| 組織構造の分配未了 / 分配済み | **割当未了 / 割当済み** | sapvc |
| ユーザー | **ユーザ**（36:1 の少数派を寄せた） | sap_sd |

- 反映は「生成器 → 再生成」の順: sap_sd は `tools/build_pages.py` → `gui_spec_build.py` → `make_gui_mockups.py` → `add_gui_note.py`、
  sapvc/sapeto は `gui_spec_build.py` → `make_gui_mockups.py`、他は `make_gui_mockups.py`。GUI モックアップ内の文字（gui_spec.json）も同時に直した。
- 全 6 站 + sap_sd_jp で `verify_site.py` / `verify_gui_figures.py` / `check_gui_overlap.py`（重なり 0）/ `verify_all_sites.py` が PASS。

### 直さないと決めたもの（`KEEP_NOTES` に 21 概念を記録）

`受入/払出`（MD04 の列名＝日本語 SAP の画面表記）、`評価区分`（所要量クラスの評価区分。評価クラスとは別）、
`記帳`（実績記帳）、`伝票/ドキュメント`、`納入先`、`請求伝票/請求書`、`マスタ/マスタデータ`、`完成品/製品`、
`オーダ`（バックオーダー）、`アカウント`（ログイン）、`倉庫`（物理的な倉庫） など。理由をツールに書いてある。

### 残っている論点（要判断）: 6 站の「中国語 UI 表記」

6 站は **ナビ・見出しに中国語表記を意図的に混ぜた作り**（`练习` `总览` `概念与设计` `实战训练站` `学员版` `讲师版` `验收` `期待结果` `对照` `早见表`）。
実測（簡体字の出現数）: sapmto 1614 / sapmts 1167 / sapvc 655 / sapeto 664 / sap_sd 413 / saporderflow 209。
各站の Excel（要件定義・手順書）のシート名も同じ語を使っている。
これは以前のセッションの作風（sap_sd_cn と対になる中文混じり）なので、**勝手に書き換えていない**。
全站を日本語 UI に揃えるなら、ナビ・見出し・Excel・ハブの文言まで含む別タスクになる（実測 4,722 箇所 + シート名）。


## 13. `sap_cn`（SAP SD 培训课程站・中文）— 2026-09-13 夜

**新規**: `sap_cn/`（16 ページ / 配置タスク 48 / 実機截图の引用 155（去重 121・元ファイル 269）/ 自绘 SVG 10（7 種）/ Excel 8 sheet）。
「**从概念到流程、从总体到局部**」の SD 専項コース。素材は既存の `sap_sd_cn`（同一教材 `S4.docx`）の
SD モジュール + 準備章の**実機スクリーンショット 269 枚をコピー**して使い、手順・IMG パス・T-code は
教材原文のまま（`work/sd_source.json` = `sap_sd_cn/work/site_model.json` の SD 48 タスクを書き出したもの）。

### 構成（16 ページ・ナビ順 = 教学順）

`index`（课程地图 = 思维导图 + 学習路线 + 六大板块）/ `concept`（概念：真实系统界面・三大概念层・五大单据・**12 个常见误解**）/
`org`（企业结构・销售结构・装运结构 + 12 タスク）/ `master`（客户三层・**四伙伴角色**・物料销售视图・条件记录）/
`pricing`（条件表 → 存取顺序 → 条件类型 → 定价过程 → 过程确定 → 账户确定）/ `flow`（O2C 泳道流程图 + 单据流 + 集成点）/
`order` / `delivery` / `billing`（局部详解、各页都有真实画面）/ `analysis`（单据流・VA05・MCTA・**教材踩坑集**）/
`config`（**48 タスクの完全索引**（A〜J の 10 群・教材原文の IMG パス・手顺要点・画面 96））/
`practice`（実訓 5 タスク・完成基准つき）/ `instructor`（讲师版：课时分配・板书路线・**必问 12 題と答案**・评分标准）/
`worksheet`（学员版 记入表・印刷可）/ `quiz`（30 題・合格 75%）/ `glossary`（术语 48 + T-code 33 + 常用表）。

### 自绘图（`tools/make_diagrams.py` → `assets/diagrams/*.svg`・純 Python で SVG）

`mindmap`（思维导图：中央 SD + 6 分岐（左右 3+3））/ `org-structure`（组织结构图 A〜D + 自动派生链条）/
`integration`（SD ⇄ FI/MM/PP/CO）/ `pricing-chain`（条件技术 4 層 + 过程确定 + 账户确定 + 算价例）/
`o2c-flow`（端到端 3 泳道流程图）/ `doc-flow`（单据流 + 参照 + 状态）/ `order-internal`（订单内部自动确定 + 3 决定链）。

**描画検証のやり方（次に図を描く人へ）**: `qlmanage -t` は **正方形に pad する**ため右端が切れて見え、
「切れている」と誤判定する（実際に誤判定した）。**Chrome headless で SVG を直接撮る**こと:
```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu \
  --window-size=1420,1240 --screenshot=/tmp/x.png "file://$PWD/assets/diagrams/<name>.svg"
```
（Chrome は 1 本ずつ直列で。自分で見て直す前提で、次の 3 つは実際に踏んだ罠）
1. 中心から分岐への**ベジェ曲線が葉ノードの箱を横切る** → 分岐ヘッダを葉の「上」に置き、曲線は中央の
   空隙（左右 70px のコリドー）だけを通す。放射レイアウトは最初これで崩れた。
2. **箱の幅を主テキストだけで計算**すると副ラベル（小さい文字）がはみ出す → `max(text_w(main), text_w(sub)) + pad`。
3. **横並びチェーンが可用幅を超える**と箱が枠外に出る → `chain()` で自動折返し（同行のみ直矢印、
   折返しは行末から下行頭へ肘状に戻す。矢印が空白を指さないように）。
4. `text_w()` は CJK 全角 1.0em / 半角 0.575em（他站と共通の教訓）。`\n` は強制改行として扱う
   （そうしないと英語フレーズが語中で折れて "Informa tion" になる）。

### 検証（本セッションで実行した実測）

| コマンド | 結果 |
|---|---|
| `python3 tools/verify_course.py` | **PASS** — pages=16 / figure.shot=155（去重 120 / 磁盘 269）/ figure.dia=10（去重 7）/ quiz=30 |
| `python3 ~/.hermes/…/scripts/verify_site.py .` | **PASS**（16 pages, nav identical, 1 active each, tags balanced, quiz keys valid） |
| `python3 tools/make_course_xlsx.py` | 8 sheet（1_课程大纲 16 行 / 4_截图索引 152 行 = 站内引用数 / 2_学习WBS 19 行 + COUNTIF） |
| `python3 tools/make_hub_page.py` | ハブを **9 站**（104 页 / 2165 步 / 3300 画面）に更新。`sap_sd_jp`・`sap_sd_cn` の行は差分なし |

`verify_course.py` が見るもの: 構造（DOCTYPE / 単一 `article` / `</article>` が `<footer>` より前 / タグ配平 /
重複 id なし）、ナビ（全頁 href 一致 + active ちょうど 1）、站内リンクと锚点、`assets/img`・`assets/diagrams` の実在、
図注（「画面」番号 + 出典）、30 題の答えが選択肢に含まれる、`hub_stats.json` との一致、残留 Markdown/占位符なし。

### 気をつけたこと（次に同種のコース站を作る人へ）

- **「実機截图」は既存站から再利用**。`sap_sd_cn/assets/img/{sd,prep}` をそのままコピーし、
  各图の説明行に**元ファイル名**（`01_1_image1297.png` 等）を残した → Word 原稿と突き合わせできる。
  ページのパス・截图は `work/sd_source.json` から取る（手でファイル名を書かない）。
- **画面の「实测值」は読図で確認してから書く**。`work/gui_screenshot_text.json` = 27 枚のキー画面を
  视觉で逐字抄録した結果（窗口标题 / 字段 / 表格列名と行データ。不明瞭な箇所は「不清楚」と明記）。
  ここから確定した値: 销售组织 `C999` 颐宁销售 / 渠道 `Z1` 直销・`Z2` 批发 / 产品组 `Z1` 铸钢泵・`Z2` 增压泵 /
  **4 つの销售范围**（C999×Z1×Z1 など）/ 工厂 `P999` 颐宁机械工厂 / 起运点 `Z999` / 拣配库位 `003` /
  客户 `10000000` 远东造船厂（送达方 = 同番号の第三分公司）/ 客户账户组 `K001` 订货方-颐宁 /
  报价类型 `QT` / 交货 `80000000`（拣配状态 A 尚未拣配・交货/拣配 120 PC・库位 003）/
  发票 `90000000` / 物料 `F999-100` 铸钢泵 170-230（`FERT`）/ PR00 = **8,000.00 RMB**/PC・有効期間 2021.01.01–9999.04.14 /
  统计组 `1 'A' 物资`・更新组 `1`。
  **この作業で実際に誤りを 1 つ発見した**: `prep/t01/04_1_image4.png` は SAP Easy Access のメニューツリー
  **ではなく** "System Entry Properties"（登录器の接続設定・英語 UI）だった。Easy Access のツリーは
  `sd/t41/01_1_image1297.png`。図注を根拠なく書くとこうなるので、**画面を読んでから書く**こと。
- **教材の数値は出典つきで断言**。**それ以外は「自システムで確認」（F1・F4・表名）** と書き、断定しない。
- **配置页（`config.html`）は教材 48 タスクをそのまま索引化**（IMG パスは教材原文＝ユーザーの中国語システムの
  実メニュー名なので、勝手に英訳・日本語化しない）。各タスクの画面は「第 1 步 + 最後の步」の 2 枚まで。
- 共有ファイルは触っていない（`assets/{style.css,main.js,quiz.js}` はコピー、`sd.css`/`sd.js` は
  `s4cn.css`/`s4cn.js` の站内コピーを改名しただけ）。
- **標準値の断定を避けた代表例**: 移動类型 601/501/101 は「教材が使った値」として提示、伙伴角色的
  コードは「システムによって WE/SH が異なるので F4 で確認」と注記、`F1` がキーと单据类型 `F2` の
  混同を避けるため语境を明示。

### GitHub へ公開（`raysource/sap_cn_sd`）— 2026-09-13 22:22

`sap_cn/` を**独立リポジトリ**として公開した: **https://github.com/raysource/sap_cn_sd**（`main` / **public**）。
HEAD = `f0bcc698fbb97a1e1447c978af3e1ff9bffd9d66`（3 commit: 站点本体 → 发布脚本 → 对账脚本）。

| コマンド | 結果 |
|---|---|
| `bash sap_cn/tools/publish_to_github.sh` | `git init -b main` + remote + commit + push（何度でも再実行可） |
| `bash sap_cn/tools/verify_publish.sh` | local HEAD == `git ls-remote` == `gh api commits/main` = `f0bcc698…`；**315 blobs**（当時の tracked と一致） |
| `bash sap_cn/tools/reconcile_remote.sh` | **remote blobs=318 == local tracked=318**、「只在远端 / 只在本地」両方空。CJK ファイル名（`SAPSD_课程大纲_学习WBS.xlsx` sha `ded2dcb9…` / 29207 B）も API で読めることを確認 |

- **教材スクリーンショットを含むので可視性は要判断**: 今回はユーザーが指定した既存リポジトリが **PUBLIC** だったためそのまま公開
  （同批の截图はすでに public な `raysource/sap-consult` にも入っている）。戻すなら
  `gh repo edit raysource/sap_cn_sd --visibility private`。
- **入れ子リポジトリになった**: `sap_cn/.git` ができたので、親の `sap-consult` から `git add sap_cn/...` は
  **黙って無効**（skill の既知の罠）。親に取り込むときは既存の `tools/include_nested_repo_files.sh`
  （`git hash-object -w --stdin-paths` → `git update-index --add --index-info`）を使う。
- **やらかしやすい罠（今回踏んだ）**: ① `gh api …/git/trees` の件数を「ファイル数」と数えると
  **ディレクトリ項目（`type=tree`）が混ざって 269 → 320 に見える**（`select(.type=="blob")` で絞る）。
  ② `comm` は**両側を sort しないと嘘の差分を出す**。③ `git ls-files` は既定で CJK を
  `"SAPSD_\350…"` とエスケープするので、API の生文件名と比較するなら `-c core.quotepath=false`。
  この 3 つは `reconcile_remote.sh` に正しい形で残した。

### 保存（第 3 回・2026-09-14 22:4x）— 「保存进度」の内容と、**保存していないもの**

併走セッション検知: `PROGRESS.md` / `index.html` の mtime は **2026-09-14 08:3x**（別セッションが
`sap_modules_cn/` を作り、§14 と hub を更新した）。45 秒あけた 2 回の md5 が同一なので**書き込みは終わっている**。
そのセッションの成果物には**触っていない**（下記の「保存していないもの」）。

1. **スナップショット（オフライン復元用）**

   `_snapshots/sap_training_sites_9sites_20260914_223904_sapcn.tar.gz`（**43,278,316 B / 41 MB**）
   `TS="…_sapcn"` を渡して作成（既定名は分単位なので、併走と衝突しないよう秒＋接尾辞）。

   | 検算（実測） | 結果 |
   |---|---|
   | `gzip -t` | OK |
   | entries | **3472** |
   | `sap_cn/` エントリ | **319**（16 页 + 269 图 + 7 自绘图 + tools/work/README/.gitignore） |
   | `sap_cn/assets/img` | list **269** == disk **269** |
   | `sap_cn/assets/diagrams` | list **7** == disk **7** |
   | `sap_sd_jp` / `sap_sd_cn` 画面 | 1209 / 1209（disk と一致） |
   | html / xlsx | list 105 / 21 == disk 105 / 21 |
   | `*/.git/` エントリ | **0**（新しくできた `sap_cn/.git` は除外されている） |
   | `*.docx` / `*.mp4` / `*.zip` / `gui_png` / 配布 PDF | 0 |
   | 主要ファイル | `PROGRESS.md`・`index.html`・`sap_cn/index.html`・`mindmap.svg`・`gui_screenshot_text.json`・`SAPSD_课程大纲_学习WBS.xlsx`・`tools/make_hub_page.py` 全部あり |

2. **站自体の検証状態（実測）**

   - `cd sap_cn && python3 tools/verify_course.py` → `pages=16 figure.shot=155（去重 120 / 磁盘 269） figure.dia=10（去重 7） quiz=30` / **RESULT: PASS**
   - `python3 ~/.hermes/…/scripts/verify_site.py .` → **PASS**（16 pages, nav identical, 1 active each, tags balanced, quiz keys valid）
   - Excel: **8 sheet**（`4_截图索引` 155 行 = 站内图引用数、`2_学习WBS` 23 行）
   - hub（`index.html`）: **カード 11 個（10 站 + tools/README.md）**、すべてローカルに実在、「10 个站」表記

3. **git（ローカル + GitHub）**

   | リポジトリ | HEAD | 確認方法 |
   |---|---|---|
   | `sap_cn/` → `raysource/sap_cn_sd`（public） | **`63604cba1c8e6fdd53c326ebe17229591fcf4935`** | `git rev-parse` == `git ls-remote origin main` == `gh api repos/raysource/sap_cn_sd/commits/main` |
   | `training/` → `raysource/sap-consult`（public） | **`177c549ab2d6ad680b94017c2178e73827f7ea27`** | 同上（`gh api repos/raysource/sap-consult/commits/main`） |

   親リポジトリの commit 直前の HEAD は `8c68da8c…` だったが、**その間に併走セッションが自分の成果物を
   自分で commit していた**（`cb2a6c7 sap_modules_cn: SAP 全模块培训课件（…57 页）`）。私の commit はその上に載っている。
   index を汚していないこと（私の commit に入ったのは `sap_cn/` 320 + `PROGRESS.md` + `tools/` のみ）は
   `git diff --cached --name-only` の出力で確認した（私の commit に他セッションのファイルは入っていない）。

   `sap_cn/` は `tools/include_nested_repo_files.sh` で**親リポジトリにも普通のファイルとして取り込んだ**
   （`.git` は保持したまま。script が「親で計算した blob SHA == 入れ子リポジトリの索引の SHA」を assert するので
   内容一致は証明済み）。`git ls-files sap_cn | wc -l` が `sap_cn` の tracked 数と一致することを確認。

4. **保存していないもの／保存したもの（要判断・実測）**

   - **`sap_modules_cn/`（別セッションの站・1099 ファイル / 27 MB・`.git` なし）**: 私の commit にも
     スナップショットにも**入れていない**。ただし**併走セッションが自分で commit していた**
     （`cb2a6c7 sap_modules_cn: …（57 页）`）ので、親リポジトリには彼らの手で入っており、
     hub の `sap_modules_cn` カードは親リポジトリ上でも解決する。
   - **スナップショットの範囲**: 私の `…_9sites_20260914_223904_sapcn.tar.gz` は
     「9 sites + hub + 共有 `tools/`」で、`sap_modules_cn` を含まない。ただし**19 秒後に併走セッションが
     自分の手で 10 sites 版を取っている**（`_snapshots/sap_training_sites_10sites_20260914_223923_modules.tar.gz` /
     58,997,334 B / 22:39:23）。つまり**全 10 sites の完全バックアップはそちらの名前で存在する**ので、
     復元するときは用途で選ぶ（`sap_cn` を確実に含むのは私の 9sites 版、`sap_modules_cn` まで含むのは 10sites 版）。
   - **`tools/make_snapshot.sh` は現在 10 sites 版**（併走セッションが `sap_modules_cn` を追加。私の `sap_cn` 行は
     そのまま残っている）。私の commit `177c549` はこの作業コピーの内容をそのまま入れた（= repo 上のツールと
     実際に使われたツールが一致している）。
   - **私の commit に入れたもの**: `sap_cn/`（320 files、入れ子リポジトリから plumbing で取り込み）、
     `PROGRESS.md`（§13 の保存節 + §1 の `sap_cn` 行の数字修正）、`tools/make_hub_page.py` と
     `index.html`（= 併走セッションが `sap_modules_cn` を hub に登録した分を含む。書き込みは 08:3x と
     22:39 のスナップショットで止まっていることを md5 の 2 回測定で確認し、差分を読んでから入れた）、
     `tools/make_snapshot.sh`、`tools/README.md`（追記）。
   - 併走セッションの**未 commit の作業ファイルには触っていない**。

5. **次にやるとよい順**（前節の続き）

   1. `sap_cn` の講義用 PDF（1 図 1 ページ）／実機で撮り直した画面への差し替え。
   2. 残り 242 枚の画面の読図（`work/gui_screenshot_text.json` と同じ手順）。
   3. `sap_modules_cn` の担当者が親リポジトリへの取り込み（`include_nested_repo_files.sh`）と
      `make_snapshot.sh` への登録を済ませると、hub のリンク切れが消える。

### スナップショット

**最新（この保存で取得）**: `_snapshots/sap_training_sites_9sites_20260914_223904_sapcn.tar.gz`
（3472 entries / 41 MB / `gzip -t` OK / `sap_cn` 319 entries / `*.git*` 0 / `sap_modules_cn` 0）。
検算は上の「保存（第 3 回）」§1 の表に実測値を書いてある。

ひとつ前の `_snapshots/sap_training_sites_9sites_20260913_221624_cn.tar.gz`
（3465 entries / 41 MB、`sap_cn` 312 entries）= 2026-09-13 夜の版。実機截图の 7 枚の図を直す前の状態なので、
復元するなら新しい方を使うこと。両方残してある（別セッションのものは消していない）。

### 未着手（次にやるとよい順）

1. `sap_cn` の講義用 PDF（`tools/export_gui_png.py` 相当を站内 PNG 用に作る／または Chrome 印刷 1 図 1 ページ）。
2. 実機で新しく撮ったスクリーンショットへの差し替え（`4_截图索引` の原文件名が対応表）。
3. **残り 242 枚の画面はまだ読図していない**（27 枚だけ逐字抄録済み）。手顺ページの図注は教材原文の
   手顺説明を使っているので誤りではないが、`config.html` の 96 図のように「教材の一句」がそのまま
   図注になっている箇所は、読図して具体的な値（画面に見えているコード・金額）に置き換えるとより良い。
   進め方は `work/gui_screenshot_text.json` と同じ（読図 → 値の表を作る → ページに反映）。
4. `sap_cn/tools/*` を共有 `tools/` に寄せるか（現状は站内に閉じている。他站に影響しない代わりに再利用は手作業）。

## 14. `sap_modules_cn`（SAP 全模块培训课件 MM / PP / FI / CO）— 2026-09-14 朝

**依頼**: 「参考 `https://sap-cn-sd.vercel.app/`（= `sap_cn/`）の内容で、**SAP の他モジュール**の培训课件を作る。
上から下へ、総体から細部へ。概念・流程・操作手顺を含み、SAP GUI の実機スクリーンショット入り。質問せず自分で生成」。

**成果物**: `sap_modules_cn/` — **MM / PP / FI / CO の 4 モジュール × 14 ページ ＋ 総覽ページ**。
既存の「一主題一站」ではなく**一つの站に 4 モジュール**（根 `index.html` = 総体、`mm/ pp/ fi/ co/` = 各 14 ページ）。

| 項目 | 実測（`tools/verify_site.py`） |
|---|---|
| ページ | 56 ＋ 総覽 1 = **57** |
| 教材タスク | MM 42 / PP 51 / FI 45 / CO 34 = **172**（教材の全タスクを配置篇で逐一走査） |
| 手順ステップ | **695** |
| 実機截图引用 | **1411 処（去重 940 枚 = `sap_sd_cn/assets/img/{mm,pp,fi,co}` の素材を全部使い切った）** |
| 自绘 SVG | **32**（各モジュール 8：mindmap / star 統合 / org tree / 主データ layers / フロー / 水泳線 / 決定鎖） |
| 自測 | 4 × 30 = **120 題**（全問 `data-answer` が選択肢にあり、解説付き） |
| Excel | `MM/PP/FI/CO_課程大綱_学習WBS.xlsx`（各 8 シート）＋ `SAP全模块_課程総覧_学習WBS.xlsx` |

**アーキテクチャ（データ / 版面 / 内容の三層分離）**

```
work/modules.json        モジュールメタ（名称・副題・3 つの流程ページのファイル名とナビ标签）
work/modules_model.json  教材 4 モジュールの全タスク（prep_data.py が sap_sd_cn/work/site_model.json から抽出）
work/img_manifest.json   截图の幅高 + 原図名（ページが width/height を書く根拠）
tools/sitegen/common.py  骨格と部品（Ctx がモジュール接頭辞を束ねる）+ ナビ（スロット → 标签）
tools/sitegen/walk.py    render_task / render_config：教材タスクを「手順＋截图」ブロックに描画
tools/sitegen/svgkit.py  7 種の自绘图の排版エンジン + 文字溢出登記（中文が箱を突き抜けたら検知）
tools/sitegen/pack_<code>.py + <code>_p2/p3/p4.py   モジュール内容パック（「どう教えるか」だけ書く）
tools/{build_pages,build_diagrams,build_hub,make_xlsx,make_readme,verify_site,shoot_pages}.py
tools/sitegen/PACK_SPEC.md   モジュールパックの契約（並行執筆のための仕様書）
```

**「手で写さない」を機械的に保証した点**（sap_cn の発想を強化）
- 14 ページのスロット順は固定（`index concept org master flow proc1..3 config practice instructor
  worksheet quiz glossary`）。順番/ファイル名が違えば `build_pages.py` が即エラー。
- **配置篇は 100% データから描画**：`render_config()` が「グループが教材の全タスクを重複なく覆うか」を検査し、
  漏れ・重複があれば例外。→ 「站の手顺 = 教材の手顺」が機械保証になる。
- 自測は `data-answer` が選択肢に無い / 解説が無い / 30 題でない、を検証器が個別に指摘。

**並行執筆のやり方（今回の肝）**
1. 私が「版面と規格」を先に凍結（`common/walk/svgkit` ＋ build/verify 群 ＋ `PACK_SPEC.md`）。
2. **MM を参考実装として自分で書き**（`pack_mm.py` + `mm_p2/p3/p4.py` 約 2000 行）、検証を通す。
3. PP / FI / CO を**3 つの子エージェントで並行執筆**。各エージェントは自分の 4 ファイルだけ変更可、
   `build_hub.py`（共有産物）とスクリーンショット（Chrome 並行で固まる）は禁止。
4. 各エージェントは `build_diagrams.py <code>` → `build_pages.py <code>` → `verify_site.py <code>` を
   `RESULT: PASS` まで自走。最後に**私が全モジュールを再構築して総検証**。

並行のために入れた変更（再利用価値あり）：
- 統計ファイルを `work/build_stats.json`（単一）→ **`work/stats/<code>.json`（モジュールごと）** に分割。
  両エージェントが同時に構築しても統計を潰し合わない。hub と検証器はディレクトリ全体を読む。
- 1 モジュールだけ構築したときのクロスモジュールリンク（`../pp/index.html`）は、
  **リンク先モジュールのディレクトリが未生成なら WARN**（FAIL にしない）。

**子エージェントの出力を信用しなかった検証（3 段）**
1. 自分で `build_pages.py` / `build_hub.py` / `verify_site.py` を再実行 → `pages=56 shot=1411 dia=38 quiz=120 RESULT: PASS`。
2. **自動「捏造検出」**：生 HTML から SAP コードらしいトークン（8 桁科目、`R999-x`、`P999` 等）を抽出し、
   `work/source_<mod>.txt`（教材原文ダンプ）に存在するか照合。ヒットしなかったのは
   「表示/変更系 T-code 変体（FD03/CS03/KA02）」「IMG T-code（OBYC/OMJJ/OX10）」など正当な標準知識のみ。
3. **截图の vision 抜き打ち照合**：CO の自測が言う「1001 Workshops / 1002 Warehouse は MFG 製造部」
   「分配循環 DRENT」「分配構造 A1 の決済成本要素 803010」を教材原図で逐字確認 → 3 件とも一致
   （子エージェントは本当に画像を読んでいた）。

**今回踏んだ罠（再発する）**
1. `svgkit` は**画布の高さを後から回填**する必要がある。占位 `height="100"` のまま出力すると
   ブラウザは 100px しか表示しない（図が空白に見える）。`build()` で `viewBox/width/height` と背景 `rect` を置換。
2. `chip_rows()` の戻り値は**「チェーンの底の絶対 y」であって高さではない**。高さとして足すと
   パネル高が y で累積し、4 パネルの図が **4642px** に伸びた（修復後 688px）。**生成後は viewBox の寸法を必ず見る**
   （`height > 2600` か `< 200` は疑う）。
3. **截图パスが別モジュールを指すことがある**（MM の发票校验タスクが `fi/t20/…png` を貼っている）。
   `assets/img/` のキーは「先頭がモジュール名か」で判定（`Ctx.key()`）。単純に接頭辞を足すと
   `assets/img/mm/mm/t22/…` になる。
4. 教材データの `imgs` は既にモジュール接頭辞付き。部品側は両方の書き方を冪等に扱う。
5. **同一ページで二種類のアンカーを使わない**：`render_task` が作る `id="tNN"` は配置篇のアンカー。
   流程ページで `<h2 id="t38">` を書くと id 重複（検証器が拾う）。流程ページは `id="secNN"`。
6. CSS は共有ツリーに**追記のみ**（`assets/mod.css` = sd.css を改名 + 追記：モジュール切替条 `.modsw`、
   タスク走査ブロック `.taskblk` / `ol.tasksteps` の番号丸、`.muted` / `.lead2` / `.cnt`、印刷規則）。
7. 統計カードを 1 行 4 枚にするには `.grid.cards.stats { grid-template-columns: repeat(auto-fit, minmax(150px,1fr)) }`。
8. README 生成器の `"  ".join("%s/" …)` が `co//` を生むなど、**生成物も読んで直す**（数字は自動・文字は手書きの所が崩れる）。
9. 図は「構造 + 色 + 中文ラベル」のデータ駆動（`DIAGRAMS` は dict のリスト）にすると、子エージェントが
   SVG の数学に触れずに済み、並行執筆が安全になる。

**再構築コマンド**
```bash
cd ~/Desktop/work/training/sap_modules_cn
python3 tools/prep_data.py        # 教材データ（冪等）
python3 tools/build_diagrams.py   # 32 枚の SVG（溢出 0 を確認）
python3 tools/build_pages.py      # 57 ページ
python3 tools/build_hub.py        # 総覽ページ
python3 tools/make_xlsx.py        # Excel 5 冊
python3 tools/make_readme.py      # README.md + tools/hub_stats.json（数字は自動）
python3 tools/verify_site.py      # RESULT: PASS
```

**生態系への接続**：`tools/make_hub_page.py` の `SITES` + `ORDER` に `sap_modules_cn` を追加し、
学習路線に「①' 全模块培训课件」を追記、「立場と注意」の実機スクリーンショット節も更新（本站は実機截图）。
`python3 tools/make_hub_page.py` 再実行 → ルート `index.html` は **10 站**、本站カードは
「57 页 / 695 手顺ステップ / 1411 画面 / 5 Excel」（数字は `sap_modules_cn/tools/hub_stats.json` の自己申告）。

**未了 / 次の人へ**
- GitHub へは**まだ push していない**。`tools/publish_to_github.sh`（既定 `raysource/sap_modules_cn`）と
  `tools/verify_publish.sh` を用意済み。截图は公開済みの `raysource/sap_cn_sd` と同源だが、
  public にするかはユーザー判断（private にするなら `gh repo edit … --visibility private`）。
- 本機に `vercel` CLI は無い（Vercel は GitHub 連携で発火）。push 後に Vercel 側でリポジトリを connect すれば
  `sap-cn-sd.vercel.app` と同じ形で公開できる。
- ルート `PROGRESS.md` / `tools/make_snapshot.sh` は**私の変更ではない差分**（前セッションの未コミット）。
  コミットするなら `git add PROGRESS.md index.html tools/make_hub_page.py sap_modules_cn` のように自分の分だけ。

## 15. 次に触る人へ（再開手順）

- `tools/hub_stats.json`（`n_pages: 14` / `n_steps: 879` / `figs: 1369`）は `tools/build_pages.py` が自動更新する。
- `work/i18n.py apply src` は **collect 時のオフセットに差し戻す**方式なので、`jp_finalize*.py` 以降に手を入れたファイルには
  実行してはいけない（壊れる）。collect 時のファイルハッシュを記録してあり、**変わっていたらスキップ＋警告**するようにしてある
  （実測: 現在は 10 ファイルすべてスキップ。訳語を直すなら日本語化済みファイルを直接編集する）。
  `apply model` は元の `site_model.json` を書き換えないので冪等。
  変更後は必ず `tools/build_pages.py` → `tools/make_jp_xlsx.py` → 3 つの検証、の順で回す。
- `tools/make_jp_xlsx.py` の `0_説明` は**実際のシート名**を列挙する必要がある（初回生成では中国語のままのシート名が 4 つ残っていた＝
  `1_模块总览` / `4_T-code速查` / `5_IMG路径一覧` / `6_踩坑与报错`）。生成後に
  「`0_説明` の文字列」と「`wb.sheetnames`」を突き合わせ、**数式のシート参照（`'7_学習WBS'!F…`）が実在シートを指しているか**も検証すること（今回は参照先が未改名だったため数式は無事）。
- 画面（実機スクリーンショット）は `assets/img/` にあり、これは**コンテンツそのもの**なのでスナップショットに含める。
  除外は `work/docx_extract/`（元画像の生展開）と `work/render/`（目視用の切り出し）のみ。
