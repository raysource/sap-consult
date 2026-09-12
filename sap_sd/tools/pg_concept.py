# -*- coding: utf-8 -*-
"""concept.html — 概念与设计"""
from pg_common import page, h2, h3, toc, flow, tbl, box, vals, checklist, esc

TOC = [
    ("sources", "1. 伝票データの 4 つの源泉"),
    ("area", "2. 販売エリアの導出"),
    ("propose", "3. 主データから何が提案されるか"),
    ("partner", "4. パートナー 4 役割と提案元"),
    ("plant", "5. 出荷プラントの自動提案"),
    ("chain", "6. 受注処理の決定链（明細カテゴリまで）"),
    ("header", "7. ヘッダ vs 明細（Business Data）"),
    ("change", "8. 変更と再決定"),
    ("block", "9. ブロックの階層"),
    ("check", "10. 保存時のチェック（不完全性・与信）"),
    ("sis", "11. 販売情報システム（Sales Summary）"),
    ("tables", "12. 主要テーブルと T-code"),
    ("myths", "13. よくある誤解"),
]

CHAIN = """【受注伝票の決定链】—— VA01 で値を入れた瞬間に、裏でこの順に決まる

 ① 組織・エリア
   得意先 (1000) ────────────→ 販売エリア 1000 / 10 / 00
   └ 得意先マスタの販売エリアビュー（複数あれば選択ダイアログ）

 ② パートナー
   得意先マスタ(販売エリア) ──→ パートナー機能 SP / BP / PY / SH
   └ 出荷先（Ship-to）は受注ヘッダで変更可。与力先は与力データの基準

 ③ 明細カテゴリ（ここが受注処理の心臓）
   伝票タイプ (OR) ─────┐
   品目カテゴリグループ ─┼─→ 明細カテゴリ (TAN)
   品目使用目的 ────────┤
   高レベル明細カテゴリ ─┘
   └ 決定テーブル: VOV4（伝票タイプ×明細カテゴリの許可）→ 決定（VOV4/VOV7）

 ④ 納入日程行カテゴリ → 所要量タイプ → 在庫確認（ATP）
   明細カテゴリ ×（品目マスタの）所要量タイプ ─→ 納入日程行カテゴリ
   └ 決定テーブル VOV5。所要量タイプが空＝所要量を作らない（在庫を持たない明細）

 ⑤ 出荷プラント（優先順位あり）
   客先品目情報 (VD51) → 得意先マスタ 出荷先の出荷プラント → 品目マスタ 販売組織1
   └ 決定された出荷プラント → 出荷ポイント → 出荷タイプ（VL01N）

 ⑥ 与力価格・税
   価格決定手順（伝票タイプ×得意先/伝票の価格手順）→ 条件タイプ（PR00 / MWST / K007…）
   └ 条件テーブル + アクセス順序 → 条件レコード（VK11/VK13）

 ⑦ 保存時のチェック
   不完全性チェック（Incompletion: 伝票タイプの手順 → グループ → 項目）
   与信チェック（与信管理が有効な場合。与信区分・与信限度額と比較）
"""


def build():
    b = []
    a = b.append
    a('<h1>概念与设计 —— 受注伝票のデータはどこから来るのか</h1>')
    a('<div class="box info"><b class="t">この頁の使い方</b>動画（<code>00:00</code>〜<code>21:35</code> と <code>32:52</code>〜<code>56:07</code>）のスライド内容を、'
      '全部 1 枚にまとめたものです。<b>13 節の見出しだけを先に読み、細部は練習中に戻って確認</b>してください。'
      '本站で最も重要な 2 つの暗記事項は <b>6 節の決定链</b>と <b>5 節の出荷プラントの優先順位</b>です。</div>')
    a(toc(TOC))
    b.append('<p style="font-size:14px;color:var(--muted)">全体像は以下の 1 本の図に集約されます。まずこれを眺めてから各節へ進んでください。</p>')
    a('<pre class="vals">%s</pre>' % esc(CHAIN))

    # 1
    a(h2("1. 伝票データの 4 つの源泉（Overview: Sources for Document Data）", "sources"))
    a('''<p>動画の最初のスライドは「受注伝票のデータは 4 種類の源泉から来る」と宣言します。これが Unit 14 全体の地図です。</p>''')
    a(tbl(["源泉", "動画の例", "本站での具体例（デモ値）", "どこで確認するか"],
          [
              ['<b>① 主データ（Master data）</b>', 'Customer master: plant, shipping condition<br>Material master: plant, loading group',
               '得意先 <code>1000</code> の支払条件 <code>ZB01</code>・インコタームズ <code>FOB</code>（<b>実機デモでは <code>CIF Berlin</code></b>。<b>同じ項目が動画内で 2 通りに出る＝主データ依存の代表例</b>）<br>品目 <code>T-ATA30</code> の品目カテゴリグループと<b>出荷プラント <code>1200</code></b>',
               '<code>XD03</code>（得意先）／<code>MM03</code>（品目）／<code>VK13</code>（条件）'],
              ['<b>② 既存伝票データ（Existing document data）</b>', 'The delivering plant at item level as the basis for determining the shipping point',
               '受注明細の<b>出荷プラント</b>が、後続の<b>出荷ポイント</b>と<b>出荷タイプ</b>を決める（<code>VL01N</code> の入口）',
               '<code>VA03</code> の明細 → 出荷タブ／伝票フロー'],
              ['<b>③ Customizing（IMG）</b>', 'Sales document type: delivery block, shipping condition<br>Determination of shipping point',
               '伝票タイプ <code>OR</code> の与信/納入/請求ブロック、明細カテゴリ決定、価格決定手順の割当',
               '<code>VOV8</code>／<code>VOV4</code>／<code>OVKK</code>／<code>SPRO</code>'],
              ['<b>④ ハードコード制御（Hard-coded controls / ABAP）</b>', '（例：出荷プラント決定時の優先度の重み付け）',
               'USEREXIT 等で標準の決定順序を上書きできる（SAP Note <b>2787562</b> が言及）',
               '原則として<b>見えない</b>。動きが標準と違うときは ABAP を疑う（講師に確認）'],
          ]))
    a(box("warn", "「値が入らない」ときの切り分けは、この 4 分類で行う",
          '受注の項目が空／想定と違うときは、<b>①主データを見る → ②既存伝票を見る → ③Customizing を見る → ④それでも合わなければ ABAP を疑う</b>の順で追います。'
          '逆順（いきなり Customizing を触る）は<b>一番やってはいけない順番</b>です。練習⑤の故障対照表はこの順序で書いてあります。'))

    # 2
    a(h2("2. 販売エリアの導出（Sales Order Entry – Deriving the Sales Area）", "area"))
    a('''<p>受注の最初の関門は <b>販売エリア（Sales Area ＝ 販売組織 / 販売チャネル / 部門）</b> を決めることです。
動画のスライドは「受注の項目 ← 得意先マスタ」という 1 本の矢印で説明しています。</p>''')
    a(tbl(["順序", "何が起きるか", "動画の画面", "自システムでの確認"],
          [
              ['1', '<code>VA01</code> の初期画面で<b>受注タイプ</b>（<code>OR</code>）と<b>販売エリア</b>を入れる。<b>販売組織だけ入れて Enter してもよい</b>',
               'Create Sales Order: Initial Screen', '初期画面の F4 に自分の販売組織が出るか（出ない＝組織構造の割当未了）'],
              ['2', '得意先（Sold-to party）を入れて Enter → 得意先が<b>複数の販売エリア</b>を持っていれば「Sales area for customer」ダイアログが出る',
               '「Sales area for customer」ポップアップ（<code>SOrg</code>/<code>DC</code>/<code>Dv</code> の一覧）', '<code>XD03</code> → 販売エリアビューで、その得意先が持つ販売エリアを確認'],
              ['3', '選んだ販売エリアが受注ヘッダに入り、以降<b>すべての項目がこの販売エリアで解釈される</b>（与力条件・出荷条件・パートナー・出力）',
               'Create Standard Order: Overview（<code>Sales area 1000 // Germany Frankfurt</code>）', '受注ヘッダの「販売エリア」欄。<b>後から変えると再決定が走ります</b>（8 節）'],
          ]))
    a(box("info", "「販売エリアが選べない」＝ 3 つのどれか",
          '① 得意先マスタにその販売エリアビューが無い（<code>XD03</code>）／② 品目マスタにその販売組織のビューが無い（<code>MM03</code>）／'
          '③ 組織構造の割当（販売組織↔プラント、販売組織↔会社コード）が未了。<b>動画のデモでは得意先 <code>1000</code> が複数の販売エリアを持ち、'
          '選択ダイアログが出る場面がそのまま教材になっています</b>（<code>09:02</code> 付近）。'))

    # 3
    a(h2("3. 主データから何が提案されるか（Proposing Order Data from Master Data）", "propose"))
    a('''<p>動画のスライドは、受注伝票のどの部分が得意先マスタ・客先品目情報・品目マスタから提案されるかを列挙します。
<b>「受注を登録する」とは、実は「提案された値を確認して、必要な所だけ直す」作業</b>だというのがこの節の要点です。</p>''')
    a(tbl(["受注の構成要素", "提案元（動画のスライド）", "動画のデモでの実際の値", "確認コマンド"],
          [
              ['ビジネスパートナー（Business Partners）', '得意先マスタ（Customer master）', '<code>SP</code>=<code>1000</code>（Becker Berlin）、<code>BP</code>=<code>1000</code>、出荷先 <code>SH</code>', '<code>VA03</code> ヘッダ → パートナー、<code>XD03</code> → パートナー機能'],
              ['与力価格（Pricing）', '得意先マスタ＋条件レコード', '<code>PR00</code> 等で Net value <code>22,990.00 EUR</code>（明細 10 PC 投入後）', '<code>VA03</code> → 条件画面、<code>VK13</code>'],
              ['税決定（Tax determination）', '得意先マスタ（税分類）＋品目マスタ（税分類）', '税条件タイプ <code>MWST</code>', '<code>VA03</code> 条件画面／<code>OVK1</code>（税決定）'],
              ['納入日程（Delivery scheduling）', '得意先マスタ（出荷条件）＋品目マスタ（リードタイム）', '納入希望日 <code>09.06.2007</code> → 納入日程行', '<code>VA03</code> 明細 → 納入日程行、<code>VOV6</code>'],
              ['支払（Payment）', '得意先マスタ（支払条件）', '<code>ZB01</code>（14 Days 3%, 30/2%）', '<code>VA03</code> ヘッダ → 支払条件、<code>XD03</code> → 販売エリアデータ'],
              ['出力（Output）', '得意先マスタ＋出力決定手順', '伝票タイプ <code>OR</code> の出力決定（<code>VOV8</code>／<code>OVT0</code> の出力決定手順）', '<code>VA03</code> → 出力、<code>VV11</code>〜'],
              ['客先品目情報（Customer-material info）', '客先品目情報レコード（<code>VD51</code>）', '得意先の品目コード・品目説明の置き換え、<b>出荷プラントの第 1 優先</b>', '<code>VD53</code>'],
              ['明細（Item）', '品目マスタ（品目カテゴリグループ等）', '品目 <code>T-ATA30</code> → 明細カテゴリ <code>TAN</code>、出荷プラント <code>1200</code>', '<code>VA03</code> 明細詳細、<code>MM03</code>'],
          ]))
    a(box("ok", "この節の合格ライン",
          '「受注を登録するとき、値は自分で全部入れるのではなく、<b>得意先マスタ・品目マスタ・条件レコードから提案され、自分は例外だけを直す</b>」'
          'と、口頭で言えること。逆に言えば、<b>提案がおかしいときは受注ではなく主データを直す</b>のが原則です。'))

    # 4
    a(h2("4. パートナー 4 役割と、役割ごとの提案元", "partner"))
    a('''<p><b>Business Partners from the Customer Master</b>（受注の 4 役割は全部「得意先マスタ」から来る）と、
<b>Proposing Order Data from the Customer Master</b>（役割ごとに見る場所が違う）という 2 枚のスライドが対になっています。</p>''')
    a(tbl(["役割", "略号", "動画の例", "この役割が決めるもの（＝どこを見るか）"],
          [
              ['Sold-to party（与力先／受注先）', '<code>SP</code>／<code>AG</code>', '<code>C1</code> / <code>1000</code> Becker Berlin',
               '受注の基準。ここから<b>販売エリア・与力価格・インコタームズ・出荷条件</b>が提案される'],
              ['Ship-to party（出荷先）', '<code>SH</code>／<code>WE</code>', '<code>S1</code> / <code>1000</code>',
               '<b>納入先住所・出荷プラント（得意先マスタ側の第 2 優先）</b>・Goods Receiving Hours・税の一部'],
              ['Bill-to party（請求先）', '<code>BP</code>／<code>RE</code>', '<code>1000</code>',
               '請求書の宛先。<b>請求書が別の法人に渡る</b>取引では与力先と分ける'],
              ['Payer（支払先）', '<code>PY</code>／<code>RG</code>', '<code>R1</code>',
               '<b>支払条件・与信限度額チェック</b>。Finance（FI）への債権の相手'],
          ]))
    a(box("info", "覚え方： 4 役割は「モノ / カネ」で分ける",
          '<b>モノの流れ</b>：Sold-to（誰が注文したか）→ Ship-to（誰に届けるか）。'
          '<b>カネの流れ</b>：Bill-to（誰に請求するか）→ Payer（誰が払うか）。<br>'
          'だから <b>支払条件と与信は Payer</b> から、<b>納入先住所と出荷プラントは Ship-to</b> から来る、と整理できます。'
          '動画の「Proposing Order Data from the Customer Master」スライドは、まさにこの対応表です（<code>C1</code>=与力条件、<code>R1</code>=支払条件と与信、<code>S1</code>=納入先住所）。'))

    # 5
    a(h2("5. 出荷プラントの自動提案（Proposing Plants Automatically）", "plant"))
    a('''<p>動画（<code>19:51</code> 付近）が独立したスライドを割いている、<b>本站で最も出題したい論点</b>です。
受注明細の「出荷プラント（Deliver.Plant）」は、<b>3 つの主データから優先順位つきで提案</b>されます。</p>''')
    a(tbl(["優先度", "提案元", "動画スライドでの値", "保守する T-code", "自システムでの確認"],
          [
              ['<b>1（最優先）</b>', '客先品目情報レコード（Customer-Material Info Record）の出荷プラント', 'C1 / M1 / 客先品目コード <code>PC-100</code> → 出荷プラント <code>1400</code>',
               '<code>VD51</code>（登録）／<code>VD52</code>／<code>VD53</code>', '<code>VD53</code> で得意先×品目を入力し、Shipping エリアのプラントを見る'],
              ['<b>2</b>', '得意先マスタ（<b>出荷先の販売エリアデータ</b>）の出荷プラント', '得意先マスタ S1 → 出荷プラント <code>1100</code>',
               '<code>XD02</code>（販売エリアデータ → 出荷タブ）', '<code>XD03</code> → 販売エリアデータ → 出荷タブ →「出荷プラント」'],
              ['<b>3（最後）</b>', '品目マスタ（<b>販売組織 1</b> ビュー）の出荷プラント', '品目マスタ M1 → <code>1000</code> / M2 → <code>1200</code>',
               '<code>MM02</code>（販売組織 1 ビュー）', '<code>MM03</code> → 販売組織 1 ビュー →「出荷プラント」'],
          ]))
    a('''<p>動画のスライドは、同じ得意先 <code>S1</code> でも受注先（K1 / K2 / C3）と品目（M1 / M2）の組み合わせによって
<b>プラントが <code>1400</code> / <code>1100</code> / <code>1000</code> / <code>1200</code> と変わる</b>ことを示しています。
つまり <b>「受注を見れば、どの主データが効いたか分かる」</b>——これが練習②の故障切り分けの土台になります。</p>''')
    a(box("warn", "つまずき（動画でも触れられている罠）",
          '① <b>3 か所のうち 2 か所に違うプラントが入っている</b>（例：客先品目情報に <code>1400</code>、品目マスタに <code>1200</code>）→ '
          '<b>優先度が高い方が勝つ</b>ので「品目マスタを直したのに変わらない」が起きます。<b>3 か所すべてを見る</b>のが鉄則。<br>'
          '② スライドに <b>“Weighting the different sources of information during plant determination”</b>（重み付け）とあるように、'
          '標準の優先順位は ABAP（USEREXIT 等）で上書きされていることがあります（SAP Note <b>2787562</b>）。'
          '自システムの挙動がスライドと違うときは、主データの誤りではなく<b>拡張</b>を疑ってください。'))

    # 6
    a(h2("6. 受注処理の決定链（明細カテゴリ・納入日程行カテゴリ）", "chain"))
    a('''<p>受注処理で最も質問が多いのが <b>「なぜこの明細カテゴリ（例 <code>TAN</code>）になるのか」</b>です。
答えは 4 つのキーの組み合わせで決まる<b>決定テーブル</b>です。本站の暗記事項その 1。</p>''')
    a('''<pre class="vals">明細カテゴリの決定（Sales Document Item Category Determination）

  キー 1  販売伝票タイプ         例: OR      （伝票タイプ側。VOV8）
  キー 2  品目カテゴリグループ   例: 0001    （品目マスタ 販売組織2 / または品目タイプ）
  キー 3  品目使用目的 (Usage)   例: 空      （標準の受注は空。返品・無償などで使う）
  キー 4  高レベル明細カテゴリ   例: 空      （BOM の親明細など。通常の単品受注は空）
        └──────────┬──────────┘
                   ↓  決定テーブル（T-code: VOV4 の「明細カテゴリ決定」）
            明細カテゴリ（Item Category） 例: TAN（Standard Item）
                   ↓
        ┌──────────┴───────────┐
        ↓                      ↓
  価格決定（与力）        納入日程行カテゴリ（VOV5）
  ├ 明細カテゴリが「与力関連」か   ├ 所要量タイプがあるか
  ├ 価格決定手順（伝票タイプ×得意先）  ├ 在庫確認（ATP）をするか
  └ 条件タイプ PR00 / MWST…       └ 納入日付タイプ（日付の決まり方）

  補足: TAN（標準明細）は「在庫を持たない明細」です。所要量タイプが空なので、
        MRP はここから所要量を作りません（＝受注在庫 E にはならない）。
        在庫を持つ／所要量を作るのは、受注生産（戦略グループ 20/25 等）や
        受注組立（82）のように「所要量クラス」が付くケースです。→ ../sapmto/ で実習</pre>''')
    a(tbl(["決まるもの", "キー（決定テーブル）", "T-code", "自システムでの確認"],
          [
              ['明細カテゴリ', '伝票タイプ × 品目カテゴリグループ × 品目使用目的 × 高レベル明細カテゴリ', '<code>VOV4</code>（割当・決定）／<code>VOV7</code>（カテゴリ定義）',
               '<code>VA03</code> 明細詳細の「明細カテゴリ」＋<code>VOV4</code> の決定テーブルを突き合わせる'],
              ['納入日程行カテゴリ', '明細カテゴリ × 所要量タイプ（品目マスタ MRP3 戦略グループ由来）', '<code>VOV5</code>／<code>VOV6</code>',
               '<code>VA03</code> 明細 → 納入日程行のカテゴリ、<code>MD04</code>（所要量が出るかどうか）'],
              ['与力価格決定', '伝票タイプ（＋得意先／伝票の価格手順）→ 価格決定手順 → 条件タイプ → アクセス順序', '<code>OVKK</code>／<code>V/06</code>／<code>V/07</code>／<code>V/08</code>／<code>VK11</code>',
               '<code>VA03</code> の条件画面（与力分析）、<code>VK13</code> で条件レコードの有効性'],
              ['パートナー決定', '得意先の勘定グループ／伝票タイプのパートナー決定手順 × 得意先マスタのパートナー機能', '<code>OVT0</code>（勘定グループ）／<code>VOPA</code> 系／<code>XD02</code>',
               '<code>XD03</code> のパートナー機能タブと、<code>VA03</code> のパートナーを比べる'],
          ]))
    a(box("warn", "「明細カテゴリが <code>TAN</code> にならない」とき",
          '① <b>品目カテゴリグループ</b>が想定と違う（品目マスタ 販売組織2、または品目タイプから提案）→ <code>MM03</code>／<code>VOV4</code>。<br>'
          '② その<b>組み合わせが決定テーブルに無い</b>→ <code>VOV4</code> の決定テーブルを見る（無ければシステムがエラーを出します）。<br>'
          '③ <b>伝票タイプ（<code>OR</code>）にその明細カテゴリが許可されていない</b>→ 割当テーブル（<code>VOV4</code>）を確認。<br>'
          '④ 品目使用目的や高レベル明細カテゴリが意図せず入っている（参照コピーした受注で起こりやすい）→ <code>VA03</code> の明細詳細。'))

    # 7
    a(h2("7. ヘッダ vs 明細（Business Data とコピーの挙動）", "header"))
    a('''<p>動画の <b>Business Data</b> スライドは、<b>支払条件とインコタームズがヘッダと明細の両方にある</b>ことを図で示しています。</p>''')
    a(tbl(["レベル", "動画の値", "意味と挙動"],
          [
              ['ヘッダ（HEADER）', '支払条件 <code>ZB01</code> ／ インコタームズ <code>FOB</code>',
               '伝票全体の既定値。<b>明細に入れると、その明細だけ上書きされる</b>（ヘッダより明細が優先）'],
              ['明細 10 / 20', '支払条件 <code>ZB01</code> ／ インコタームズ <code>FOB</code>',
               '得意先マスタから提案された値。動画では<b>明細レベルにも同じ値が入っている</b>状態が示されます'],
              ['（別の受注へコピーした場合）', '明細 20 で <code>ZB01→ZB02</code>、<code>FOB→EXW</code>（スライドでは赤で上書き表示）',
               '<b>参照コピーでは、コピー管理（<code>VTAA</code>）の「データ転送」設定に従って転送されるか再決定されるかが決まる</b>'],
          ]))
    a(box("info", "なぜ「ヘッダと明細の両方」なのか",
          '請求・与信・支払条件は<b>ヘッダでも明細でも持ち得る</b>設計です（明細ごとに支払条件を変えられるようにするため）。'
          '結果として <b>「ヘッダの支払条件を変えたのに、明細に値が入っているので請求書が変わらない」</b>という現象が起きます。'
          '切り分けは <code>VA03</code> で<b>ヘッダの支払条件と明細の支払条件を両方見る</b>こと（本站 能力测试でも出題します）。'))

    # 8
    a(h2("8. 変更と再決定（Changes to the Sold-to Party in the Sales Document）", "change"))
    a('''<p>動画の後半（<code>48:01</code>〜）で最も丁寧に扱われるスライドです。
<b>受注の得意先（Sold-to party）を変更すると、システムは何を決め直し、何をそのままにするのか</b>——これを知らないと、
「得意先を変えたのに価格が古いまま」という事故が起きます。</p>''')
    a('<div class="two-col">')
    a('<div class="panel"><h4>再決定されるデータ（Redetermined Data）</h4><ul>'
      '<li>得意先マスタ（Customer master）</li>'
      '<li>客先品目情報レコード（Customer-material info record）</li>'
      '<li>テキスト（Texts）</li>'
      '<li>無償品（Free goods）</li>'
      '<li>与力価格（Prices）</li>'
      '<li>出力（Output）</li>'
      '<li>出荷プラントと出荷ポイント（Plant and shipping point）</li></ul></div>')
    a('<div class="panel"><h4>変わらないデータ（Unchanged Data）</h4><ul>'
      '<li>販売エリア（Sales area）</li>'
      '<li>販売事務所と販売グループ（Sales office and sales group）</li>'
      '<li>可用性と製品割当（Availability and product allocation）</li>'
      '<li>バッチ（Batches）</li></ul></div>')
    a('</div>')
    a(box("warn", "「何も変わらない」条件（スライドの注記）",
          '<b>No changes if there are: status-relevant preceding documents / subsequent documents</b> —— '
          'つまり<b>ステータスに関係する先行伝票・後続伝票が既にある場合、システムは何も変更しません</b>。'
          '出荷伝票や請求書が既にできている受注で得意先を変えても反映されないのは、この仕様です。'
          '（動画の実演では、この再決定を確認するために <code>VA02</code> から得意先マスタへ飛ぶ流れが示されます）'))
    a(h3("変更の 3 つの方式（Overview: Changing of sales documents）"))
    a(tbl(["方式", "動画のスライド", "T-code", "使いどころ"],
          [
              ['<b>明細の一括変更（Fast changes in document）</b>', 'Item 10 / 20 の Plant を <code>1200</code> → <code>2000</code> に同時変更',
               '<code>VA02</code> の明細概況で複数明細を選択 → 一括変更', '同じ受注の中で、複数明細のプラント・納入日・数量をまとめて直す'],
              ['<b>複数伝票の一括変更</b>', '複数の受注の Plant 列をまとめて <code>2000</code> に',
               '<code>VA02</code> の一括変更（<code>MASS</code>／<code>VA05</code> からの変更）', '一定期間の受注をまとめて直す（障害時の一括対応）'],
              ['<b>文書一覧からの変更（Changes using document list）</b>', '受注リスト → 変更',
               '<code>VA05</code>（受注一覧）／<code>V.02</code>（不完全な受注一覧）', '条件で絞って変更対象を確定する（出荷ブロックの解除など）'],
          ]))
    a(box("danger", "実習での注意",
          '<b>既に後続伝票がある受注は変更しない</b>でください（業務でも同じです）。練習②では<b>保存済みで後続伝票の無い受注</b>を作り、'
          'そこに変更を加えて再決定を観察します。'))

    # 9
    a(h2("9. ブロックの階層（Blocks）", "block"))
    a('''<p>動画（<code>37:35</code> 付近）の <b>Blocks</b> スライドは、ブロックが<b>3 つの階層</b>に設定できることを示します。
「なぜこの受注が出荷できないのか」を追うときは、この 3 階層を上から見ます。</p>''')
    a(tbl(["階層", "設定できるブロック", "動画の記載", "解除の T-code"],
          [
              ['<b>ヘッダ（受注ヘッダ）</b>', '納入ブロック（Delivery block）／請求ブロック（Billing block）', 'Header → Delivery block / Billing block',
               '<code>VA02</code> ヘッダ → 各ブロック項目を空に／<code>V.23</code>・<code>V.24</code>（一覧）'],
              ['<b>明細（受注明細）</b>', '請求ブロック（Billing block）', 'Item 10 / 20 → Billing block',
               '<code>VA02</code> 明細 → 請求ブロック'],
              ['<b>納入日程行（Schedule line）</b>', '納入ブロック（Delivery block）', 'Schedule line 1 / 2 → Delivery block',
               '<code>VA02</code> 明細 → 納入日程行 → 納入ブロック'],
          ]))
    a(box("info", "スライドの読み方： “User sets and removes blocks / Defining”",
          'ブロックは <b>①ユーザが設定・解除できるもの</b>と、<b>②Customizing で標準的に付くもの</b>があります'
          '（例：伝票タイプ <code>OR</code> の与信/納入/請求ブロック、得意先マスタの与信区分）。'
          'つまり<b>「ブロックが付いている理由」は ①手で付けた ②マスタ／設定で付いた ③チェックで付いた（与信など）</b>の 3 通り。'
          '本站では練習②でこの 3 通りを作り分けます。'))

    # 10
    a(h2("10. 保存時のチェック（不完全性・与信）", "check"))
    a('''<p>受注を保存する瞬間に走るチェックです。動画では <code>VA01</code> のデモ中に
<b>「Enter PO number」の必須エラー</b>（<code>09:28</code> 付近）が出る場面があり、これもこの仕組みの一部です。</p>''')
    a(tbl(["チェック", "何を見るか", "設定（T-code）", "失敗したときの挙動"],
          [
              ['<b>不完全性チェック</b>（Incompletion）', '伝票タイプに割り当てた<b>不完全性手順</b> → グループ → 項目（例：PO 番号、出荷先、納入日）',
               '<code>OVA2</code>（手順）／<code>VUA2</code>（警告かエラーか）／<code>VUP2</code>（明細カテゴリ）／<code>VUE2</code>（納入日程行カテゴリ）',
               'エラー＝保存できない／警告＝保存はできるが不完全伝票として記録される。後から <code>V.02</code>（不完全な受注一覧）で拾える'],
              ['<b>与信チェック</b>（Credit check）', '与信区分・与信限度額と、与信使用額（売掛＋受注残＋出荷残）',
               '<code>OVA8</code>（伝票タイプの与信チェック）／<code>OB45</code>（与信管理エリア）／<code>FD32</code>（得意先の与信）',
               '与信ブロックが付く → 出荷できない → 与信解除（<code>VKM1</code>／<code>VKM3</code> 等）'],
              ['<b>必須項目チェック</b>（動画の「Enter PO number」）', '伝票タイプの項目ステータス／不完全性手順の必須設定',
               '<code>VOV8</code>（伝票タイプの項目ステータス）／<code>OVA2</code>', '赤いエラーが項目に出て保存できない。<b>動画では PO 番号が必須になっている例がそのまま映っています</b>'],
          ]))
    a(box("ok", "本站での扱い",
          '不完全性チェックは<b>「不完全な受注を放置しない仕組み」</b>です。'
          '動画のデモ環境では PO 番号が必須項目になっているため、<b>受注の PO Number 欄に何か入れてから保存</b>します'
          '（動画では <code>dddd</code> や <code>test</code> のようなダミー値が入っています）。'
          '自システムの必須項目は <code>V.02</code> にわざと不完全な受注を作って確認するのが最短です。'))

    # 11
    a(h2("11. 販売情報システム（SIS）と Sales Summary", "sis"))
    a('''<p>動画の前半（<code>22:45</code>〜<code>32:29</code>）は <b>Sales Summary（<code>VC/2</code>）</b>の実演と、その Customizing に費やされます。
これは「受注処理の道具とヘルプ」の後半を担う内容です。<b>Sales Summary は得意先マスタの情報と受注残・与信・既存伝票を 1 画面に集めた照会</b>です。</p>''')
    a(tbl(["要素", "動画で確認できるもの", "どこで決まるか"],
          [
              ['情報ビュー（Info view）', '<code>001</code> Complete information／<code>002</code> Address/partner info／<code>003</code> Statistical info／<code>005</code> Telesales／<code>100</code> Credit Information／<code>101</code> Last SD Documents／<code>102</code> Backorders／<code>103</code> Quick Info／<code>900</code> New Internet cust.',
               'SPRO の「Maintain Report Views」（本站 <a href="config.html#c5">C5</a>）'],
              ['情報ブロック（Info block）', 'Address（Firma / Calvinstrasse 36 / D-13467 Berlin-Hermsdorf）、Classification（Nielsen ID / Customer classif. / Industry sector）、Key figures、Contact person、Last SD documents、Document key figures、Pricing',
               'SPRO の「Maintain Views for an Evaluation」（ビューへブロックを順番つきで割当）'],
              ['ユーザ別の既定ビュー', '<code>BAPMS</code> → <code>ZPD</code>、<code>WF-SD-2</code> → <code>900</code> などの割当',
               'SPRO の「Maintain the Report Views for a User」'],
              ['既存伝票の統計更新', '文書カテゴリ（<code>A</code> Inquiry／<code>B</code> Quotation／<code>C</code> Order／<code>D</code> Item proposal／<code>3</code> Invoice list 等）ごとの「Statistics update desired」',
               'SPRO の「Last Documents for a Customer」'],
              ['与信情報', 'Credit Limit <code>511,291.88 EUR</code>／Usage Level <code>1,472,653.29 EUR</code>／Delta <code>-961,361.41</code>／Consumption in % <code>288</code>／Receivables／Open Delivery Value／Open Sales Order Val／Open Bill. Doc. Val',
               'FI/SD の与信管理（<code>OB45</code>・<code>OVA8</code>・<code>FD32</code>）＋ 得意先マスタの与信区分'],
              ['Last SD documents', '受注（<code>11076</code> 等・Open）と請求書（<code>90035240</code> 等・Completed / Being processed）の一覧',
               '上記の統計更新設定と、その得意先の既存伝票'],
              ['統計情報', 'Net value of incoming orders／Net sales／Open net value of orders 等の 2007 vs 2006 比較',
               'SIS の統計ファイル更新（受注・請求の更新時に自動）'],
          ]))
    a(box("info", "「Sales Summary が出ない／情報が空」の切り分け",
          '① 得意先が違う（<code>5264</code> は動画の概念スライド用の例。実際のデモは <code>1000</code>）→ 番号を確認。<br>'
          '② <b>情報ビューが割り当てられていない</b>→ <code>VC/2</code> の「View」ボタンで出る一覧と、SPRO のビュー割当を比べる（<a href="config.html#c5">C5</a>）。<br>'
          '③ <b>そのユーザに既定ビューが無い</b>→「Maintain the Report Views for a User」を確認。<br>'
          '④ <b>統計更新が OFF</b> の文書カテゴリ → 「Last Documents for a Customer」のチェック状況を確認。<br>'
          '⑤ そもそも統計ファイルが未構築（SIS のフレキシブル分析は初期構築が必要）→ 講師に確認。'))
    a('''<p>もう 1 つ、動画では <b>Sales Summary から出荷伝票 <code>80007832</code>（<code>VL03N</code>）へ飛ぶ</b>流れが示されます。
<b>「受注 → 出荷」が伝票フローで繋がっている</b>ことを、情報照会の側から確認する操作です。</p>''')

    # 12
    a(h2("12. 主要テーブルと T-code", "tables"))
    a(tbl(["目的", "テーブル", "主な T-code", "見方"],
          [
              ['受注ヘッダ', '<code>VBAK</code>', '<code>VA01</code>／<code>VA02</code>／<code>VA03</code>', '得意先 <code>VBAK-KUNNR</code>、販売エリア、正味価額 <code>VBAK-NETWR</code>、伝票タイプ <code>VBAK-AUART</code>'],
              ['受注明細', '<code>VBAP</code>', '同上', '品目 <code>VBAP-MATNR</code>、明細カテゴリ <code>VBAP-PSTYV</code>、<b>出荷プラント <code>VBAP-WERKS</code></b>'],
              ['納入日程行', '<code>VBEP</code>', '同上', '納入日 <code>VBEP-EDATU</code>、納入日程行カテゴリ <code>VBEP-ETTYP</code>'],
              ['パートナー', '<code>VBPA</code>', '同上', '役割 <code>VBPA-PARVW</code>（<code>SP</code>/<code>SH</code>/<code>BP</code>/<code>PY</code>）と相手先'],
              ['得意先マスタ（販売）', '<code>KNA1</code>／<code>KNVV</code>', '<code>XD01</code>／<code>XD02</code>／<code>XD03</code>', '販売エリア別の支払条件・出荷条件・<b>出荷プラント</b>（<code>KNVV</code>）'],
              ['品目マスタ（販売）', '<code>MARA</code>／<code>MVKE</code>', '<code>MM01</code>／<code>MM02</code>／<code>MM03</code>', '品目カテゴリグループ <code>MVKE-MTPOS</code>、<b>出荷プラント <code>MVKE-DWERK</code></b>'],
              ['客先品目情報', '<code>KNMT</code>', '<code>VD51</code>／<code>VD52</code>／<code>VD53</code>', '得意先品目コードと<b>出荷プラント</b>（第 1 優先）'],
              ['条件レコード', '<code>KONP</code>／<code>KONH</code>／<code>A*</code>', '<code>VK11</code>／<code>VK12</code>／<code>VK13</code>', '条件タイプ <code>PR00</code>・税 <code>MWST</code> の金額と有効期間'],
              ['不完全性ログ（受注）', '<code>VBUV</code>（明細）／<code>VBUK</code>（ヘッダ）／<code>VBUP</code>', '<code>V.02</code>／<code>V.00</code>', '不完全な項目の一覧。手順定義は <code>TVUV</code>／<code>TVUVF</code>（<code>OVA2</code>）'],
              ['伝票フロー', '<code>VBFA</code>', '<code>VA03</code> → 伝票フロー', '受注 → 出荷 → 請求 の連鎖と数量・金額'],
          ]))
    a(box("ok", "テーブルを見るコツ（本站の推奨）",
          '画面で「なぜこの値か」が分からないときは、<b>受注のテーブル（<code>VBAK</code>/<code>VBAP</code>）と主データのテーブル（<code>KNVV</code>/<code>MVKE</code>/<code>KNMT</code>）を並べて見る</b>と、'
          '<b>どの源泉が効いたか</b>が一目で分かります（<code>SE16N</code>／<code>SE16</code>）。'
          '本站の練習①〜②は、この「並べて見る」作業を課題に入れています。'))

    # 13
    a(h2("13. よくある誤解（10 項目）", "myths"))
    a(tbl(["#", "よくある誤解", "正しい理解"],
          [
              ['1', '受注の値は自分で全部入力するもの', '<b>主データから提案され、例外だけ直す</b>。提案がおかしいときは受注ではなく主データを直す'],
              ['2', '出荷プラントは品目マスタだけで決まる', '<b>客先品目情報 > 得意先マスタ（出荷先）> 品目マスタ（販売組織1）</b>の優先順位。3 か所すべてを見る'],
              ['3', '明細カテゴリは品目だけで決まる', '伝票タイプ × 品目カテゴリグループ × 品目使用目的 × 高レベル明細カテゴリの<b>決定テーブル</b>（<code>VOV4</code>）'],
              ['4', '<code>TAN</code> は受注在庫（E）になる', '<code>TAN</code> は<b>在庫を持たない標準明細</b>（所要量タイプが空）。受注在庫は戦略グループと所要量クラスの設計（→ <code>../sapmto/</code>）'],
              ['5', '支払条件はヘッダにだけある', '<b>ヘッダと明細の両方</b>にあり得る。明細に入ると明細が優先。請求額が変わらないときはここを疑う'],
              ['6', '得意先を変えれば価格も全部変わる', '再決定されるのは価格・プラント・出力など。<b>販売エリアや販売事務所は変わらない</b>'],
              ['7', '後続伝票があっても得意先は変えられる', 'ステータスに関係する先行・後続伝票があると<b>何も変更されない</b>（動画スライドの注記）'],
              ['8', 'ブロックは手で付けるものだけ', '手で付ける／Customizing で付く／チェックで付く（与信）の <b>3 通り</b>。階層はヘッダ・明細・納入日程行'],
              ['9', 'PO 番号が必須なのは標準仕様', '環境の設定（項目ステータス／不完全性手順）。動画の環境では必須になっているだけ。<code>V.02</code> で確認'],
              ['10', 'Sales Summary は受注と無関係な帳票', '受注の「環境」メニューからも <code>VC/2</code> を開ける。<b>受注・与信・既存伝票を 1 画面で見る照会</b>であり、SIS の Customizing と対で理解する'],
          ]))
    a(box("info", "次の一歩",
          '概念を読んだら、<a href="config.html">配置手顺（C0〜C16）</a>を眺めて「どこで何が決まるか」を確認し、'
          '<a href="handson-1.html">练习① 受注登録</a> で実際に動かしてください。'
          '用語の確認は <a href="worksheet.html">学员版</a>、理解度は <a href="quiz.html">能力测试（28 題）</a> で。'))

    return page("concept.html", "概念与设计",
                "受注処理の概念：伝票データの 4 つの源泉（主データ/既存伝票/Customizing/ABAP）、販売エリアの導出、"
                "主データからの提案、パートナー 4 役割、出荷プラントの自動提案（優先順位）、明細カテゴリ・納入日程行カテゴリの決定链、"
                "ヘッダと明細の関係、変更時の再決定（Redetermined/Unchanged）、ブロックの階層、不完全性・与信チェック、Sales Summary。",
                "\n".join(b), crumb="概念与设计",
                foot='受注伝票のデータは主データ・既存伝票・Customizing・ハードコードの 4 つから来る。決まり方を知れば、受注は「読める」ようになる。',
                foot_next='<a href="config.html">配置手顺（C0〜C16）</a> で、この決まり方を自分の環境で作り・確かめます。')
