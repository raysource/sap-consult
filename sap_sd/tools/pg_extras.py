# -*- coding: utf-8 -*-
"""instructor.html / worksheet.html / quiz.html"""
from pg_common import (page, h2, h3, toc, flow, tbl, box, vals, steps, task, checklist,
                       quiz_q, cards, esc)


# ============================================================ 講師版
def _instructor():
    b = []
    a = b.append
    a('<h1>讲师版 —— 指導案・解答・採点基準</h1>')
    a(box("warn", "この頁は講師用です（受講者は読まないでください）",
          '受講者に渡す前に <b><a href="worksheet.html">学员版（記入用）</a></b> と <b><a href="quiz.html">能力测试（28 題）</a></b> を印刷してください。'
          '本頁には<b>発展課題の解答例・症例判別の答え・必出 Q&A</b> が載っています。'))

    a(h2("1. 全体設計（この站で到達させたい 2 点）", "design"))
    a('''<p>動画（SAP Education <b>Unit 14: Sales Order Processing</b>）の到達目標は 2 つだけです。
本站はその 2 点を、<b>自分の環境で再現できる形</b>に分解しました。</p>''')
    a(tbl(["動画の目標", "本站での分解", "到達判定（受講者の言動）"],
          [['<b>① 伝票データの出所を言える</b>（material master・customer master・Customizing）',
            '概念 1〜6 節 ＋ 练习①の「値の出所表」＋ 练习⑤の故障切り分け 4 画面',
            '受注の任意の項目について「値・出所テーブル・決まった理由」を 3 つセットで言える'],
           ['<b>② ツールとヘルプを使える</b>（tools and help）',
            '练习⑤ の <code>SU3</code>／F1／与力分析／<code>VA05</code>／<code>V.02</code>／<code>SE16N</code>',
            '初見の異常に対して、自力で 3 つ以上の画面を開いて切り分けを進められる']]))

    a(h2("2. 時間割（推奨 2 日間）", "schedule"))
    a(tbl(["時間", "内容", "使う頁", "講師の作業"],
          [['Day1 09:00–09:30', 'オリエン：動画の位置づけとゴール', '総覧', '動画 <code>00:00</code>〜<code>06:45</code> を再生（概念スライド）'],
           ['Day1 09:30–11:00', '概念 1〜6 節＋板書（決定链）', '概念与设计', '<b>決定链を黒板に書き、受講者に写させる</b>'],
           ['Day1 11:00–12:00', '環境確認（C0）と前提の穴埋め', '配置手顺 C0', '受講者ごとの得意先・品目を確定させる（ここが遅れると以降が全部止まる）'],
           ['Day1 13:00–15:00', '练习① 受注登録（VA01）', '练习①', '動画 <code>06:48</code>〜<code>21:35</code> を流しながら、受講者の画面を巡回'],
           ['Day1 15:00–16:30', '概念 7〜13 節（変更・ブロック・チェック・SIS）', '概念与设计', '動画 <code>32:52</code>〜<code>51:22</code> を抜粋再生'],
           ['Day1 16:30–17:30', '练习② 伝票の変更と再決定', '练习②', '<b>「変わる／変わらない」を必ず口頭で確認</b>'],
           ['Day2 09:00–10:30', '练习③ Sales Summary（<code>VC/2</code>）', '练习③', '動画 <code>22:45</code>〜<code>32:29</code> の Customizing 4 画面を一緒に開く'],
           ['Day2 10:30–12:00', '配置手顺 C1〜C5（動画の Customizing）', '配置手顺', '<code>VOV8</code>／<code>OVT0</code>／<code>OVS9</code>／SIS レポートビューを実演'],
           ['Day2 13:00–14:30', '配置手顺 C6〜C16（決定テーブルと優先順位）', '配置手顺', '決定テーブルは<b>1 行ずつ追加</b>して効果を見せる'],
           ['Day2 14:30–16:00', '练习④ 出荷と請求', '练习④', 'PGI の前後を必ず記録させる（取消が難しいため）'],
           ['Day2 16:00–17:00', '练习⑤ 発展＋故障対照表', '练习⑤', '<b>症状だけ見せて答えを言わせない</b>'],
           ['Day2 17:00–17:45', '能力测试（28 題）＋振り返り', '能力测试', '75% 未満は該当節へ戻す']]))

    a(h2("3. 板書用の図（そのまま写す）", "board"))
    a('''<p>黒板／ホワイトボードに書く図は <b>2 枚だけ</b>に絞ります。これ以上書くと受講者が写しきれません。</p>''')
    a(h3("板書 1：受注伝票の決定链"))
    a(vals("""受注タイプ OR ─┐
品目カテゴリグループ ─┼→ 明細カテゴリ TAN ─┬→（与力関連）→ 価格決定手順 → 条件 PR00 → Net value
品目使用目的 ─┘                          └→ 納入日程行カテゴリ → 所要量タイプ → 在庫確認(ATP)

得意先 1000 → 販売エリア 1000/10/00 → パートナー SP/SH/BP/PY ─┬→ 支払条件 ZB01（Payer）
                                                          └→ インコタームズ FOB

出荷プラント ← ① 客先品目情報(VD51) ＞ ② 得意先マスタ出荷先(XD02) ＞ ③ 品目マスタ販売組織1(MM02)
             └→ 出荷ポイント → 出荷タイプ（VL01N）"""))
    a(h3("板書 2：データの出所 4 分類（異常時の探索順）"))
    a(vals("""① 主データ（得意先/品目/条件）  → XD03 / MM03 / VK13
② 既存伝票（先行受注・参照コピー） → VA03 / 伝票フロー
③ Customizing（伝票タイプ・決定テーブル） → VOV8 / VOV4 / VOV5 / OVA2
④ ハードコード（ABAP/拡張）        → ①②③が正しいときだけ疑う

≪切り分けの順序≫ ①受注を見る → ②主データを見る → ③設定を見る → ④拡張を疑う"""))

    a(h2("4. 発展課題の解答例（练习⑤）", "answers"))
    a(tbl(["課題", "解答の要点", "よくある誤答"],
          [['発展① 伝票タイプにブロックを仕込む',
            '<code>VOV8</code> の <code>ZOR1</code> に納入ブロックを設定 → そのタイプで作る受注は<b>最初からブロック付き</b>。設定を戻しても<b>既存受注はブロックのまま</b>（伝票に焼き付く）',
            '「設定を戻せば既存受注も解除される」→ ✗（新規受注のみに効く）'],
           ['発展② 出荷プラントの優先順位',
            '<code>MM02</code>（販売組織1）→ <code>XD02</code>（出荷先）→ <code>VD51</code>（客先品目情報）の順に値を入れ、<b>後から入れた上位が勝つ</b>。上位を空にすると下位に戻る',
            '「品目マスタを直せば必ず反映される」→ ✗（上位があると負ける）'],
           ['発展③ Sales Summary のビュー自作',
            '① でビュー <code>Z01</code> を定義 → ② で情報ブロックを 3〜5 個割当 → ③ で自分を <code>Z01</code> に割当 → <code>VC/2</code> の View に出る',
            '①だけ作って②を忘れる → ビューは出るが<b>中身が空</b>'],
           ['発展④ 不完全性の必須項目追加',
            '<code>OVA2</code> で手順に項目追加 → <code>VUA2</code> で<b>警告</b>にすると保存はでき、<code>V.02</code> に載る。項目を埋めると一覧から消える',
            '「エラーにしないと意味がない」→ ✗（業務では警告＋一覧管理が一般的）']]))

    a(h2("5. 症例判別（8 問）—— 症状だけを見せて答えさせる", "cases"))
    a('''<p>受講者に<b>症状だけ</b>を読み上げ、① 根因 ② 証拠の取り方 ③ 処置 を答えさせます。<b>答えを先に言わないこと。</b></p>''')
    a(tbl(["#", "症状", "答え（根因／証拠／処置）"],
          [['1', '受注の Net value が 0.00 EUR',
            '条件レコードが無い or 有効期間外 or 与力日付ずれ → <code>VA03</code> 条件画面＋<code>VK13</code> → <code>VK11</code> で正しいキー・期間で登録'],
           ['2', '明細の出荷プラントが空',
            '3 か所すべてに値が無い → <code>VD53</code>／<code>XD03</code>／<code>MM03</code> → どこに入れるか決めて保守'],
           ['3', '品目マスタを直したのに出荷プラントが変わらない',
            '上位（客先品目情報 or 得意先マスタ）に値がある → <code>KNMT</code>／<code>KNVV</code>／<code>VBAP-WERKS</code> を並べる → 上位を修正'],
           ['4', '明細カテゴリが <code>TAN</code> にならない',
            '決定テーブル（<code>VOV4</code>）の 4 キー不一致／品目カテゴリグループ違い → <code>MM03</code>（販売組織2）＋<code>VOV4</code> → 行を整備'],
           ['5', '保存時に「PO Number を入力してください」',
            '不完全性手順の必須項目（動画の環境で発生）→ <code>OVA2</code>／<code>V.02</code> → 埋める or 警告に変更'],
           ['6', '受注は保存できたが出荷できない',
            '納入／請求／与信ブロックのどれか → <code>VA03</code> ヘッダ 3 ブロック＋与信ステータス → 由来を特定して解除'],
           ['7', '得意先を変えたのに価格が古い',
            '再決定されない項目 or 手動条件 or 後続伝票ありで無変更 → 条件画面（手動表示）＋伝票フロー → 入れ直す／後続伝票を処理'],
           ['8', '<code>VC/2</code> に情報ビューが出ない',
            '「Report Views for a User」に未割当 or ビュー未定義 → <code>VC/2</code> の View＋SPRO → C5 の ①③ を整備']]))

    a(h2("6. 必出 Q&A（12 問）", "qa"))
    a(tbl(["質問", "答え"],
          [['伝票データの源泉 4 つは？', '主データ／既存伝票／Customizing／ハードコード（ABAP）'],
           ['販売エリアは何から導出される？', '得意先マスタ（販売エリアビュー）。複数あれば選択ダイアログ「Sales area for customer」'],
           ['出荷プラントの優先順位は？', '① 客先品目情報（<code>VD51</code>）→ ② 得意先マスタの出荷先（<code>XD02</code> 出荷タブ）→ ③ 品目マスタ 販売組織1（<code>MM02</code>）'],
           ['明細カテゴリの 4 つのキーは？', '販売伝票タイプ × 品目カテゴリグループ × 品目使用目的 × 高レベル明細カテゴリ'],
           ['<code>TAN</code> は在庫を持つ？', '持たない（所要量タイプが空＝所要量を作らない）。受注在庫 E とは別（戦略グループ・所要量クラスの設計）'],
           ['支払条件と与信を決めるパートナーは？', '<b>Payer</b>。納入先住所と出荷プラントは Ship-to 側'],
           ['得意先変更で再決定されるものは？', '得意先マスタ・客先品目情報・テキスト・無償品・<b>与力価格</b>・出力・<b>出荷プラントと出荷ポイント</b>'],
           ['得意先変更で変わらないものは？', '販売エリア・販売事務所／販売グループ・可用性／製品割当・バッチ'],
           ['後続伝票がある受注で得意先を変えると？', '<b>何も変更されない</b>（ステータス関連の先行／後続伝票がある場合の仕様）'],
           ['ブロックの 3 階層は？', 'ヘッダ（納入／請求）・明細（請求）・納入日程行（納入）。由来は ①手動 ②Customizing ③チェック（与信）'],
           ['Sales Summary の画面はどこで決まる？', 'SIS の Customizing 4 画面（Report Views／Views for an Evaluation／Report Views for a User／Last Documents for a Customer）'],
           ['不完全性の設定と一覧は？', '定義 <code>OVA2</code>（挙動 <code>VUA2</code>、適用 <code>VUP2</code>／<code>VUE2</code>）、一覧 <code>V.02</code>／<code>V.00</code>']]))

    a(h2("7. 採点基準と合否", "grading"))
    a(tbl(["項目", "配点", "合格ライン", "見方"],
          [['能力测试（28 題）', '100', '<b>75%（21 問）以上</b>', '概念 10／設定 7／実務 6／故障 5 の配分。故障問題を落とした場合は該当節を再実習'],
           ['练习①〜④ の验收清单', '必須', '<b>全項目 ✓</b>', '特に「値の出所表」と「変更前後比較表」は<b>実物の画面で確認させる</b>'],
           ['练习⑤ の故障対照表', '必須', '<b>2 件以上の再現記録</b>', '「症状 → 根因 → 証拠 → 処置 → 再発防止」が書けているか。証拠が画面名・T-code で具体的か'],
           ['発展課題 4 本', '加点', '2 本以上', '①〜④ のうち 2 本できれば実務即応レベル']]))
    a(box("danger", "指導上の禁止事項",
          '① <b>標準の <code>OR</code>／<code>TAN</code> を直接書き換えさせない</b>（<code>Z</code> コピーで練習させる）。<br>'
          '② <b>後続伝票がある受注で変更練習をさせない</b>（意図しない差異や実データ汚染の原因）。<br>'
          '③ <b>PGI を実施させたら必ず記録させる</b>（取消には専用処理が必要）。<br>'
          '④ 故障問題で<b>答えを先に言わない</b>（症状 → 自力で証拠、の順を守らせる）。'))
    return page("instructor.html", "讲师版",
                "SAP SD 受注処理トレーニングの指導案：時間割、板書用の決定链図、発展課題の解答例、症例判別 8 問の答え、"
                "必出 Q&A 12 問、採点基準（75% 合格）。動画 Unit 14 準拠。",
                "\n".join(b), crumb="讲师版", has_figures=False,
                foot='講師用：この站の指導案・解答・採点基準。受講者には学员版・能力测试を配布してください。')


# ============================================================ 学员版
def _worksheet():
    b = []
    a = b.append
    a('<h1>学员版 —— 記入用ワークシート</h1>')
    a(box("info", "使い方",
          '印刷して手元に置き、<b>実機の画面を見ながら記入</b>してください。'
          '空欄は自分の環境の値です（動画の値とは違って当然です）。記入が終わったら <a href="quiz.html">能力测试</a> へ。'))
    a('<p class="mini">記入欄は罫線になっています（印刷すると書きやすくなります）。</p>')

    a(h2("1. 環境基本情報（C0）", "env"))
    a('<table class="tbl wide fill">\n'
      '<tr><th>項目</th><th>自分の環境の値</th><th>確認 T-code / 確認した画面</th></tr>\n'
      + "\n".join('<tr><td>%s</td><td></td><td>%s</td></tr>' % (k, v) for k, v in [
          ('クライアント / ユーザ', 'ログオン情報'),
          ('販売組織 / チャネル / 部門', '<code>VA01</code> 初期画面の F4'),
          ('得意先（受注先）', '<code>XD03</code>'),
          ('品目（明細 10 用）', '<code>MM03</code>'),
          ('品目カテゴリグループ', '<code>MM03</code> → 販売組織 2'),
          ('出荷プラント（品目マスタ販売組織1）', '<code>MM03</code> → 販売組織 1'),
          ('支払条件 / インコタームズ', '<code>XD03</code> → 販売エリアデータ'),
          ('与力条件（<code>PR00</code>）の有無と期間', '<code>VK13</code>'),
          ('受注タイプ', '<code>VOV8</code>'),
          ('不完全性の必須項目（例：PO 番号）', '<code>V.02</code> / <code>OVA2</code>'),
      ]) + '\n</table>')

    a(h2("2. 受注 1 件の記録（练习①）", "order"))
    a('<table class="tbl wide fill">\n'
      '<tr><th>項目</th><th>記入</th><th>どこで見たか</th></tr>\n'
      + "\n".join('<tr><td>%s</td><td></td><td>%s</td></tr>' % (k, v) for k, v in [
          ('受注番号', '<code>VA03</code>'),
          ('販売エリア（実値）', '<code>VA03</code> ヘッダ'),
          ('Sold-to / Ship-to', '<code>VA03</code> ヘッダ'),
          ('明細 10：品目 / 数量', '<code>VA03</code> 明細'),
          ('明細カテゴリ（ItCa）', '<code>VA03</code> 明細詳細'),
          ('<b>出荷プラント</b>', '<code>VA03</code> 明細 ／ <code>VBAP-WERKS</code>'),
          ('納入日程行カテゴリ / 納入日', '<code>VA03</code> 明細 → 納入日程行'),
          ('正味価額（Net value）と通貨', '<code>VA03</code> ヘッダ'),
          ('支払条件 / インコタームズ', '<code>VA03</code> → Sales タブ'),
          ('与力価格日付', '<code>VA03</code> ヘッダ（日付）'),
          ('保存時のメッセージ（そのまま）', 'ステータスバー'),
      ]) + '\n</table>')

    a(h2("3. 値の出所表（3 列を埋める／最低 6 項目）", "source"))
    a('<table class="tbl wide fill">\n'
      '<tr><th>項目と値</th><th>出所（テーブル・項目）</th><th>源泉（主データ／既存伝票／Customizing／ABAP）</th></tr>\n'
      + "\n".join('<tr><td></td><td></td><td></td></tr>' for _ in range(8)) + '\n</table>')

    a(h2("4. 出荷プラントの 3 か所（练习①・発展②）", "plant"))
    a('<table class="tbl wide fill">\n'
      '<tr><th>優先度</th><th>保守箇所（T-code）</th><th>記入した値</th><th>受注で採用された？</th></tr>\n'
      '<tr><td>1（最優先）</td><td>客先品目情報 <code>VD51/VD53</code></td><td></td><td></td></tr>\n'
      '<tr><td>2</td><td>得意先マスタ 出荷先 <code>XD02</code> 出荷タブ</td><td></td><td></td></tr>\n'
      '<tr><td>3（最後）</td><td>品目マスタ 販売組織1 <code>MM02</code></td><td></td><td></td></tr>\n'
      '<tr><td colspan="3">受注に入った値（<code>VBAP-WERKS</code>）</td><td></td></tr>\n'
      '</table>')

    a(h2("5. 変更前後の比較（练习②）", "change"))
    a('<table class="tbl wide fill">\n'
      '<tr><th>項目</th><th>変更前</th><th>変更後</th><th>再決定された？<br>（Redetermined / Unchanged）</th></tr>\n'
      + "\n".join('<tr><td>%s</td><td></td><td></td><td></td></tr>' % k for k in [
          '与力価格（Net value）', '与力価格日付', '出荷プラント', '出荷ポイント', '支払条件',
          'インコタームズ', 'パートナー（SP/SH）', '販売エリア', '販売事務所／販売グループ', '納入日程行の日付'])
      + '\n</table>')

    a(h2("6. ブロックの 3 階層（练习②）", "block"))
    a('<table class="tbl wide fill">\n'
      '<tr><th>階層</th><th>設定したブロック</th><th>症状（何ができなくなったか）</th><th>解除した？</th></tr>\n'
      '<tr><td>ヘッダ</td><td></td><td></td><td></td></tr>\n'
      '<tr><td>明細</td><td></td><td></td><td></td></tr>\n'
      '<tr><td>納入日程行</td><td></td><td></td><td></td></tr>\n'
      '</table>')

    a(h2("7. Sales Summary の記録（练习③）", "sis"))
    a('<table class="tbl wide fill">\n'
      '<tr><th>項目</th><th>記入</th></tr>\n'
      + "\n".join('<tr><td>%s</td><td></td></tr>' % k for k in [
          '「View」に出た情報ビューの ID 一覧',
          'Credit Limit / Usage Level / Delta / Consumption %',
          'Open Sales Order Val / Open Delivery Value / Open Bill. Doc. Val',
          'Last SD documents に出た受注番号（上位 3 件）',
          'Last SD documents に出た請求書番号（上位 3 件）',
          '統計情報（年度比較）で見た指標と値',
          '出荷伝票番号と Status Overview の状態',
      ]) + '\n</table>')

    a(h2("8. 出荷・請求の記録（练习④）", "ship"))
    a('<table class="tbl wide fill">\n'
      '<tr><th>項目</th><th>記入</th></tr>\n'
      + "\n".join('<tr><td>%s</td><td></td></tr>' % k for k in [
          '出荷伝票番号 / 出荷数量',
          'ピッキング数量 / PGI 実行日時',
          'PGI 前後の在庫数量（プラント）',
          '移動タイプ <code>601</code> の明細（<code>MB51</code>）',
          '請求書番号 / 正味価額 / 税額',
          '伝票フローに並んだ伝票（受注・出荷・請求）',
      ]) + '\n</table>')

    a(h2("9. 故障記録（症状 → 根因 → 証拠 → 処置 → 再発防止）", "trouble"))
    a('<table class="tbl wide fill">\n'
      '<tr><th>症状</th><th>根因</th><th>証拠（画面・T-code）</th><th>処置</th><th>再発防止</th></tr>\n'
      + "\n".join('<tr><td></td><td></td><td></td><td></td><td></td></tr>' for _ in range(6)) + '\n</table>')

    a(h2("10. 到達度の自己判定", "self"))
    a('<table class="tbl wide fill">\n'
      '<tr><th>項目</th><th>○/△/×</th><th>根拠（証拠・画面）</th></tr>\n'
      + "\n".join('<tr><td>%s</td><td></td><td></td></tr>' % k for k in [
          '伝票データの 4 つの源泉を言える',
          '出荷プラントの 3 段階の優先順位を実測で示せる',
          '明細カテゴリ決定の 4 キーを暗唱できる',
          '変更時の再決定／不変を 7 項目・4 項目で言える',
          'ブロックの 3 階層と由来 3 通りを言える',
          'Sales Summary のビューとブロックの関係を説明できる',
          '不完全性チェックの 3 階層と <code>V.02</code> の運用を説明できる',
          '受注 → 出荷 → 請求を 1 本に繋げ、伝票フローで示せる',
          '異常時に 4 画面を順に開いて切り分けられる',
      ]) + '\n</table>')
    a(box("ok", "次の一歩",
          '記入が終わったら <a href="quiz.html">能力测试（28 題・75% 合格）</a> を受けてください。'
          '△／× の項目は、対応する頁（概念・配置手顺・练习番号）に戻って実機で確かめます。'))
    return page("worksheet.html", "学员版",
                "受講者用の記入ワークシート：環境基本情報、受注 1 件の記録、値の出所表（主データ/既存伝票/Customizing/ABAP）、"
                "出荷プラント 3 か所、変更前後比較、ブロック 3 階層、Sales Summary の記録、出荷・請求の記録、故障記録、自己判定。",
                "\n".join(b), crumb="学员版", has_figures=False,
                foot='受講者用：印刷して実機を見ながら記入するワークシート。記入後は能力测试（28 題）で確認。')


# ============================================================ 能力测试
Q = [
 # ---- 概念 10
 ("概念", "gray", "動画（SAP Education Unit 14）が掲げる到達目標はどれ？",
  [("A", "受注伝票の作成手順を暗記し、1 分以内に登録できるようになること"),
   ("B", "<b>伝票データの出所（material master・customer master・Customizing 等）を判断でき、受注を入力・処理するための道具とヘルプを使えるようになること</b>"),
   ("C", "SD モジュールの全テーブル構造を暗記すること"),
   ("D", "ABAP で受注の拡張（USEREXIT）を書けるようになること")],
  "B", "動画冒頭の目標スライドは 2 点です —— ① Determine the origin of document data from various sources, like the material master, the customer master, or Customizing ② Find and use the tools and help for entering and processing sales orders。本站はこの 2 点をゴールにしています。→ <a href='concept.html#sources'>概念 1 節</a>"),

 ("概念", "gray", "伝票データの 4 つの源泉に<b>含まれない</b>ものはどれ？",
  [("A", "主データ（得意先マスタ・品目マスタ・条件）"),
   ("B", "既存伝票データ（先行受注など）"),
   ("C", "<b>ユーザの個人設定（<code>SU3</code> の住所・言語）</b>"),
   ("D", "Customizing（IMG）とハードコードされた ABAP 制御")],
  "C", "4 つの源泉は 主データ／既存伝票データ／Customizing／ハードコード（ABAP）です（動画のスライド「Overview: Sources for Document Data」）。<code>SU3</code> は道具とヘルプの話で、伝票データの源泉ではありません。→ <a href='concept.html#sources'>概念 1 節</a>"),

 ("概念", "gray", "受注の<b>販売エリア</b>が導出される主な根拠は？",
  [("A", "品目マスタの販売組織ビュー"),
   ("B", "<b>得意先マスタ（販売エリアビュー）。複数あれば選択ダイアログが出る</b>"),
   ("C", "伝票タイプ <code>OR</code> の固定値"),
   ("D", "出荷プラントから逆算される")],
  "B", "動画のスライド「Sales Order Entry - Deriving the Sales Area」は、受注の項目が得意先マスタから導出されることを図で示します。得意先 <code>1000</code> は複数の販売エリアを持ち、<code>09:02</code> 付近で「Sales area for customer」ダイアログが出る場面がその実例です。→ <a href='concept.html#area'>概念 2 節</a>"),

 ("概念", "gray", "受注明細の<b>出荷プラント</b>の提案優先順位（強い順）はどれ？",
  [("A", "品目マスタ → 得意先マスタ → 客先品目情報"),
   ("B", "<b>客先品目情報（VD51）→ 得意先マスタ（出荷先）→ 品目マスタ（販売組織1）</b>"),
   ("C", "得意先マスタ → 品目マスタ → 客先品目情報"),
   ("D", "優先順位はなく、常に最後に入力した値が使われる")],
  "B", "動画のスライド「Proposing Plants Automatically」は、客先品目情報（<code>PC-100</code> → <code>1400</code>）＞得意先マスタ（<code>1100</code>）＞品目マスタ（<code>1000</code>/<code>1200</code>）の順で決まることを示します。SAP の KBA 2787562 も同じ順序です。→ <a href='concept.html#plant'>概念 5 節</a> / <a href='config.html#c10'>C10</a>"),

 ("概念", "gray", "明細カテゴリを決定する 4 つのキーの組み合わせはどれ？",
  [("A", "販売伝票タイプ × 品目タイプ × プラント × 得意先"),
   ("B", "<b>販売伝票タイプ × 品目カテゴリグループ × 品目使用目的 × 高レベル明細カテゴリ</b>"),
   ("C", "得意先 × 品目 × 数量 × 納入日"),
   ("D", "販売エリア × 与力手順 × 出荷条件 × 納入日程行カテゴリ")],
  "B", "明細カテゴリ決定テーブル（<code>VOV4</code>）のキーは 4 つです。動画のデモでは「<code>OR</code> × 品目カテゴリグループ × 空 × 空 → <code>TAN</code>」になります。→ <a href='concept.html#chain'>概念 6 節</a> / <a href='config.html#c8'>C8</a>"),

 ("概念", "gray", "標準的な受注明細の明細カテゴリ <code>TAN</code> について正しい説明はどれ？",
  [("A", "<code>TAN</code> は受注在庫（特在 E）を作るので、MRP が計画手配を生成する"),
   ("B", "<b><code>TAN</code> は標準明細で、所要量タイプが空のため所要量を作らない（＝受注在庫にはならない）</b>"),
   ("C", "<code>TAN</code> は在庫を持つ明細で、品目は必ず <code>KMAT</code> でなければならない"),
   ("D", "<code>TAN</code> は無償出荷専用の明細カテゴリ")],
  "B", "<code>TAN</code>（Standard Item）は所要量タイプが空で、所要量を作りません。受注在庫（E）は戦略グループと所要量クラスの設計次第で、受注生産の実習（<code>../sapmto/</code>）の主题です。→ <a href='config.html#c2'>C2</a>"),

 ("概念", "gray", "<b>支払条件と与信チェック</b>の基準になるパートナー役割はどれ？",
  [("A", "Sold-to party（SP）"),
   ("B", "Ship-to party（SH）"),
   ("C", "<b>Payer（PY）</b>"),
   ("D", "Bill-to party（BP）")],
  "C", "動画のスライド「Proposing Order Data from the Customer Master」は、<code>R1</code>（Payer）から支払条件・与信限度額チェックが、<code>S1</code>（Ship-to）から納入先住所・GR 時間が提案されることを示します。→ <a href='concept.html#partner'>概念 4 節</a>"),

 ("概念", "gray", "受注の<b>得意先（Sold-to party）</b>を変更したとき、<b>再決定されない</b>ものはどれ？",
  [("A", "与力価格（Prices）"),
   ("B", "出荷プラントと出荷ポイント"),
   ("C", "<b>販売エリア、販売事務所と販売グループ</b>"),
   ("D", "出力（Output）とテキスト")],
  "C", "動画のスライドの 2 列がそのまま答えです —— <b>Redetermined</b>: 得意先マスタ／客先品目情報／テキスト／無償品／与力価格／出力／出荷プラントと出荷ポイント。<b>Unchanged</b>: 販売エリア／販売事務所と販売グループ／可用性と製品割当／バッチ。→ <a href='concept.html#change'>概念 8 節</a>"),

 ("概念", "gray", "既に<b>後続伝票（出荷・請求）がある受注</b>で得意先を変更すると、システムはどう動く？",
  [("A", "価格と出荷プラントだけが再決定され、それ以外はそのまま"),
   ("B", "<b>何も変更しない（ステータスに関係する先行／後続伝票があるため）</b>"),
   ("C", "後続伝票が自動で取り消され、最初から作り直される"),
   ("D", "エラーで処理が中断され、変更そのものが禁止される")],
  "B", "動画スライドの注記「No changes if there are: status relevant preceding documents / subsequent documents」が答えです。不具合ではなく仕様です。→ <a href='concept.html#change'>概念 8 節</a>"),

 ("概念", "gray", "Sales Summary（<code>VC/2</code>）の画面構成を決めているのは何？",
  [("A", "受注の伝票タイプ（<code>VOV8</code>）の設定"),
   ("B", "<b>SIS（販売情報システム）の Customizing —— 情報ビュー・情報ブロック・ユーザ別既定ビュー・統計更新</b>"),
   ("C", "得意先の勘定グループ（<code>OVT0</code>）"),
   ("D", "品目マスタの販売組織 2 ビュー")],
  "B", "動画（<code>27:06</code>〜<code>28:29</code>）が実演する 4 画面がこれです：Report Views／Views for an Evaluation／Report Views for a User／Last Documents for a Customer。→ <a href='concept.html#sis'>概念 11 節</a> / <a href='config.html#c5'>C5</a>"),

 # ---- 設定 7
 ("設定", "", "動画で <code>VOV8</code> を使って実演されていた設定はどれ？",
  [("A", "得意先勘定グループの定義"),
   ("B", "<b>販売伝票タイプ（Sales Order Types）の定義</b>"),
   ("C", "価格決定手順の定義"),
   ("D", "出荷ポイントの決定")],
  "B", "<code>VOV8</code> は販売伝票タイプの定義です。動画（<code>51:35</code> 付近）では詳細画面の出荷・請求グループ（納入タイプ・納入ブロック・出荷条件・即時出荷・受注関連請求タイプ <code>G2</code>・請求ブロックなど）が示されます。→ <a href='config.html#c1'>C1</a>"),

 ("設定", "", "得意先の<b>番号範囲・項目ステータス・パートナー決定手順</b>を決めるのはどれ？",
  [("A", "得意先グループ（<code>OVS9</code>）"),
   ("B", "<b>得意先勘定グループ（<code>OVT0</code>）</b>"),
   ("C", "伝票タイプ（<code>VOV8</code>）"),
   ("D", "不完全性手順（<code>OVA2</code>）")],
  "B", "<b>勘定グループ</b>が得意先マスタの「型」を決めます（番号範囲・項目ステータス・パートナー決定手順・出力決定手順）。動画（<code>52:54</code>〜）では <code>0001 Sold-to party</code> の詳細画面が実演されます。→ <a href='config.html#c3'>C3</a>"),

 ("設定", "", "<b>得意先グループ</b>（<code>OVS9</code>）の説明として正しいものはどれ？",
  [("A", "得意先の与信限度額を決める"),
   ("B", "<b>得意先の分類（統計・分析のキー）であり、受注の制御（価格・明細カテゴリ）を直接決めるものではない</b>"),
   ("C", "得意先の必須項目を決める"),
   ("D", "与力価格の条件タイプを決める")],
  "B", "得意先グループは分析用の属性です。<b>制御する設定（勘定グループ・伝票タイプ・決定テーブル）と、分析用の属性（得意先グループ）を区別する</b>のがこの問題の狙いです。動画では 47 エントリの一覧が示されます。→ <a href='config.html#c4'>C4</a>"),

 ("設定", "", "<code>VC/2</code> であるユーザに<b>既定の情報ビュー</b>を割り当てるのは、SIS Customizing のどの画面？",
  [("A", "Maintain Report Views"),
   ("B", "Maintain Views for an Evaluation"),
   ("C", "<b>Maintain the Report Views for a User</b>"),
   ("D", "Last Documents for a Customer")],
  "C", "4 画面の役割は ①ビューの定義 ②ビューへの情報ブロック割当 ③<b>ユーザ別の既定ビュー</b> ④既存伝票の統計更新 です。動画ではユーザ <code>BAPMS</code> → ビュー <code>ZPD</code>、<code>WF-SD-2</code> → <code>900</code> の例が示されます。→ <a href='config.html#c5'>C5</a>"),

 ("設定", "", "<code>VC/2</code> の「<b>Last SD documents</b>」に受注を出すために確認すべき設定はどれ？",
  [("A", "伝票タイプの不完全性手順"),
   ("B", "<b>「Last Documents for a Customer」で文書カテゴリ <code>C Order</code> の統計更新が有効かどうか</b>"),
   ("C", "品目マスタの所要量タイプ"),
   ("D", "出荷ポイントの決定テーブル")],
  "B", "動画の 4 画面のうち ④ がこれです。文書カテゴリ（<code>A Inquiry</code>／<code>B Quotation</code>／<code>C Order</code> 等）ごとに「Statistics update desired」のチェックが確認できます。→ <a href='config.html#c5'>C5</a>"),

 ("設定", "", "<b>不完全性手順</b>（どの項目を必須にするか）を定義する T-code はどれ？",
  [("A", "<code>VOV8</code>"),
   ("B", "<b><code>OVA2</code></b>"),
   ("C", "<code>VOV4</code>"),
   ("D", "<code>VD51</code>")],
  "B", "不完全性は IMG「基本機能 → 不完全項目のログ → 不完全性手順を定義」で、T-code は <code>OVA2</code> です。挙動（警告／エラー）は <code>VUA2</code>、適用先は <code>VUP2</code>（明細カテゴリ）／<code>VUE2</code>（納入日程行カテゴリ）。不完全な受注の一覧は <code>V.02</code>。→ <a href='config.html#c14'>C14</a>"),

 ("設定", "", "<b>客先品目情報</b>（得意先の品目コードや出荷プラントを保守するマスタ）の登録 T-code はどれ？",
  [("A", "<code>XD01</code>"),
   ("B", "<code>MM01</code>"),
   ("C", "<b><code>VD51</code></b>"),
   ("D", "<code>VK11</code>")],
  "C", "客先品目情報は <code>VD51</code>（登録）／<code>VD52</code>／<code>VD53</code> です。得意先マスタは <code>XD01</code>、品目マスタは <code>MM01</code>、条件レコードは <code>VK11</code>。出荷プラントの最優先の出所です。→ <a href='config.html#c10'>C10</a>"),

 # ---- 実務 6
 ("実務", "teal", "<code>VA01</code> で得意先を入力した後、その得意先が複数の販売エリアを持つときに表示されるダイアログは？",
  [("A", "Partner selection"),
   ("B", "<b>Sales area for customer</b>"),
   ("C", "Customer Change: Initial Screen"),
   ("D", "Info View Selection")],
  "B", "動画（<code>09:02</code> 付近）では <code>SOrg / DC / Dv</code> の一覧が出て、<code>1000 / 10 / 00</code> を選ぶ場面が映ります。Partner selection はパートナー（出荷先など）を選ぶダイアログで別物です。→ <a href='handson-1.html'>练习①</a>"),

 ("実務", "teal", "動画 <code>VA01</code> のデモで使われていた<b>受注タイプ・明細カテゴリ・品目</b>の組み合わせはどれ？",
  [("A", "受注タイプ <code>OR</code>／明細カテゴリ <code>TANN</code>／品目 <code>P-102</code>"),
   ("B", "<b>受注タイプ <code>OR</code>／明細カテゴリ <code>TAN</code>／品目 <code>T-ATA30</code></b>"),
   ("C", "受注タイプ <code>CR</code>／明細カテゴリ <code>TAN</code>／品目 <code>T-ATA29</code>"),
   ("D", "受注タイプ <code>OR</code>／明細カテゴリ <code>TAB</code>／品目 <code>PC-100</code>")],
  "B", "動画のデモは受注タイプ <code>OR</code>（Standard Order）、明細カテゴリ ItCa = <code>TAN</code>、品目 <code>T-ATA30</code>（数量 10 PC）です。明細 20 には <code>T-ATA29</code> も使われます。→ <a href='handson-1.html'>练习①</a>"),

 ("実務", "teal", "動画で <code>VA01</code> のデモ中に「<b>Enter PO number</b>」のエラーが出る理由は？",
  [("A", "標準では PO 番号が必ず必須だから"),
   ("B", "<b>その環境の設定（項目ステータス／不完全性手順）で必須になっているため</b>"),
   ("C", "得意先マスタに PO 番号が登録されていないため"),
   ("D", "受注タイプ <code>OR</code> では必ず PO 番号が要求されるため")],
  "B", "必須かどうかは環境の設定です。動画では PO Number 欄に <code>dddd</code> や <code>test</code> のようなダミーを入れて先へ進めています。自システムの必須項目は <code>V.02</code>（不完全な受注一覧）で確認するのが早道です。→ <a href='config.html#c14'>C14</a>"),

 ("実務", "teal", "動画のスライド「Overview: Changing of sales documents」が示す変更の 3 方式に<b>含まれない</b>ものはどれ？",
  [("A", "明細の一括変更（1 つの受注内で複数明細を同時変更）"),
   ("B", "複数の伝票の一括変更"),
   ("C", "<b>伝票タイプの変更（同じ受注の受注タイプを <code>OR</code> → <code>CR</code> に変更）</b>"),
   ("D", "文書一覧からの変更")],
  "C", "スライドの 3 方式は「明細の一括変更（Fast changes in document）」「複数伝票の一括変更」「文書一覧からの変更（Changes using document list）」です。→ <a href='concept.html#change'>概念 8 節</a> / <a href='handson-2.html'>练习②</a>"),

 ("実務", "teal", "<b>ブロック</b>を設定できる 3 つの階層の組み合わせとして正しいものは？",
  [("A", "伝票タイプ／得意先／品目"),
   ("B", "<b>ヘッダ／明細／納入日程行</b>"),
   ("C", "販売エリア／出荷ポイント／プラント"),
   ("D", "受注／出荷／請求")],
  "B", "動画の「Blocks」スライドは、ヘッダ（納入・請求ブロック）、明細（請求ブロック）、納入日程行（納入ブロック）の 3 階層を示します。→ <a href='concept.html#block'>概念 9 節</a>"),

 ("実務", "teal", "受注の <b>Net value が 0.00 EUR</b> のままだった。まず何を確認すべき？",
  [("A", "受注タイプの不完全性手順"),
   ("B", "<b>価格の条件レコード（有効期間・キー）。<code>VA03</code> の条件画面と <code>VK13</code></b>"),
   ("C", "品目マスタの MRP3 の在庫確認"),
   ("D", "納入日程行カテゴリの所要量タイプ")],
  "B", "価格は条件レコードから来ます。条件が無い／有効期間外／与力日付ずれで 0 になります。受注の設定を触る前に条件を確認するのが正しい順序です。→ <a href='config.html#c12'>C12</a>"),

 # ---- 故障 5
 ("故障", "red", "品目マスタ（販売組織 1）の出荷プラントを変更したのに、受注の出荷プラントが変わらない。最も可能性が高い原因は？",
  [("A", "<b>客先品目情報または得意先マスタ（出荷先）に出荷プラントが入っていて、そちらが優先されている</b>"),
   ("B", "受注を保存済みのため、明細の値は変更できない"),
   ("C", "品目マスタの変更が反映されるのは翌日だから"),
   ("D", "出荷プラントは手入力するしか方法がない")],
  "A", "優先順位は ①客先品目情報 → ②得意先マスタ（出荷先）→ ③品目マスタ です。上位に値があれば下位の変更は効きません。<b>3 か所すべてを見る</b>のが鉄則。→ <a href='concept.html#plant'>概念 5 節</a> / <a href='config.html#c10'>C10</a>"),

 ("故障", "red", "受注に品目を入れたが<b>明細カテゴリが <code>TAN</code> にならない</b>。確認する場所として最も適切なのは？",
  [("A", "<code>VK13</code>（条件レコード）"),
   ("B", "<b><code>MM03</code> の販売組織 2（品目カテゴリグループ）と <code>VOV4</code> の明細カテゴリ決定テーブル</b>"),
   ("C", "<code>OVA2</code>（不完全性手順）"),
   ("D", "<code>OVS9</code>（得意先グループ）")],
  "B", "明細カテゴリは 4 キーの決定テーブル（<code>VOV4</code>）で決まります。まず品目カテゴリグループ（<code>MM03</code> 販売組織 2）を読み、決定テーブルの該当行を探します。→ <a href='concept.html#chain'>概念 6 節</a> / <a href='config.html#c8'>C8</a>"),

 ("故障", "red", "<code>VC/2</code> を実行したら<b>情報ビューが <code>001</code> しか選べない</b>。疑うべき設定は？",
  [("A", "<code>OVA2</code> の不完全性手順"),
   ("B", "<b>「Maintain the Report Views for a User」に自分が割り当てられていない／追加ビューが未定義</b>"),
   ("C", "伝票タイプの与信ブロック"),
   ("D", "品目マスタの MTv 所要量タイプ")],
  "B", "表示できるビューが足りないときは ③ ユーザ別の既定ビュー割当と ① ビュー定義を確認します。情報ブロックが少なければ ② を疑います。→ <a href='config.html#c5'>C5</a> / <a href='handson-3.html'>练习③</a>"),

 ("故障", "red", "受注は正常に保存できたが<b>出荷伝票が作成できない</b>。「ブロックされています」と表示される。切り分けの順序として正しいものは？",
  [("A", "まず品目マスタを疑い、次に価格条件を見る"),
   ("B", "<b>受注ヘッダ／明細／納入日程行の 3 階層のブロックを確認し、次に与信ブロックと納入日程行の有無を確認する</b>"),
   ("C", "まず ABAP の USEREXIT を疑う"),
   ("D", "<code>VC/2</code> の統計情報を確認する")],
  "B", "ブロックは 3 階層にあり、由来も ① 手動 ② Customizing ③ チェック（与信）の 3 通りです。上から順に確認し、与信ブロックなら与信解除の処理が必要です。→ <a href='concept.html#block'>概念 9 節</a> / <a href='handson-4.html'>练习④</a>"),

 ("故障", "red", "得意先を変更したのに<b>与力価格が古いまま</b>だった。考えられる説明として<b>適切でない</b>ものはどれ？",
  [("A", "後続伝票（出荷・請求）があり、システムが何も変更しなかった"),
   ("B", "明細に手動で入れた条件が残っている"),
   ("C", "<b>販売エリアが変わったので、システムが自動で全条件を再決定するのが正常</b>"),
   ("D", "与力日付が変わらず、条件レコードが拾い直されていない")],
  "C", "再決定されないものに<b>販売エリアは含まれます</b>（Unchanged 側）。「販売エリアが変わったから再決定される」は誤りです。A・B・D はいずれも実際に起こり得ます。→ <a href='concept.html#change'>概念 8 節</a>"),
]


def _quiz():
    b = []
    a = b.append
    a('<h1>能力测试（28 題）—— 点击选项即时判分</h1>')
    a(box("info", "受け方",
          '① 先に設问だけを読み、<b>自信のない問題は印を付けて</b>進めます。② 選択肢をクリックすると<b>即時判分と解説</b>が出ます。'
          '③ 28 題のうち <b>21 問（75%）以上</b>が合格ライン。④ 間違えたら、解説のリンクから該当節へ戻って実機で確認してください。'))
    a(tbl(["分野", "出題数", "ねらい"],
          [['概念', '10 題', '伝票データの源泉・販売エリア・出荷プラント・明細カテゴリ・再決定・Sales Summary の考え方'],
           ['設定', '7 題', '動画の Customizing（<code>VOV8</code>／<code>OVT0</code>／<code>OVS9</code>／SIS）と決定テーブル・不完全性'],
           ['実務', '6 題', '動画のデモ（<code>VA01</code> の操作、ブロック、変更の 3 方式、Net value）'],
           ['故障', '5 題', '症状から根因と確認場所を引く力']]))
    a('<p class="mini">合格ライン：<b>75%（21 問 / 28 題）以上</b>。故障分野を落とした場合は、<a href="handson-5.html">练习⑤ の故障対照表</a> で再実習してください。</p>')
    for i, (tag, cls, q, opts, ans, exp) in enumerate(Q, 1):
        a(quiz_q(i, tag, cls, q, opts, ans, exp))

    a(h2("実機验收清单（テストと別に、必ず実機で確認する）", "accept"))
    a(checklist([
        "<code>VA01</code> で受注を 1 件作成し、<b>受注番号</b>を取得した",
        "<b>出荷プラント・明細カテゴリ・Net value</b> の 3 つを、根拠となる画面（主データ／決定テーブル／条件）と一緒に説明できる",
        "受注の得意先を変更し、<b>再決定されるもの／されないもの</b>を実測で示した",
        "ブロックを <b>3 階層</b>で設定し、解除した",
        "<code>VC/2</code> で<b>情報ビューを切り替え</b>、Last SD documents と与信情報を表示した",
        "出荷伝票を作成し、<b>PGI の前後で在庫が変化</b>することを確認した",
        "請求書を作成し、<b>伝票フロー</b>で受注 → 出荷 → 請求を 1 本に繋げた",
        "故障対照表のうち <b>2 件以上</b>を実際に再現し、証拠を記録した",
    ]))
    a(box("ok", "合格後の進路",
          '<b>本站は「受注伝票そのもの」の実習</b>です。ここから先は生産形態別の実習へ —— '
          '受注生産（E）<code>../sapmto/</code>／受注設計生産（Q）<code>../sapeto/</code>／見込生産 <code>../sapmts/</code>／'
          'バリアント設定 <code>../sapvc/</code>／形態の横断比較 <code>../saporderflow/</code>。<br>'
          '<b>本站で「値の出所を追う力」が付いていれば、どの站も読み解けます。</b>'))
    return page("quiz.html", "能力测试",
                "SAP SD 受注処理の能力测试 28 題（概念 10／設定 7／実務 6／故障 5）。クリックで即時判分・解説つき。"
                "75% 合格。実機验收清单つき。動画 Unit 14 準拠。",
                "\n".join(b), crumb="能力测试", has_figures=False,
                foot='28 題・75% 合格。概念と設定だけでなく「症状から根因を引く」故障問題を含みます。',
                foot_next='不合格の場合は <a href="handson-5.html">练习⑤ の故障対照表</a> と <a href="config.html">配置手顺</a> に戻って再実習してください。')


def build_all():
    return {
        "instructor.html": _instructor(),
        "worksheet.html": _worksheet(),
        "quiz.html": _quiz(),
    }
