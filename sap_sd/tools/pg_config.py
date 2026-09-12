# -*- coding: utf-8 -*-
"""config.html — 配置手顺 C0〜C16（练习配置）"""
from pg_common import page, h2, h3, toc, tbl, box, steph, kv, steps, vals, task, esc

# 各 STEP は dict で持ち、末尾で共通レンダリングする（構造を揃えるため）
CONFIG = [
 dict(
  id="c0", no="C0", title="前提与环境确认（受注が成立する 5 条件）",
  tc="VA01・VA03・XD03・MM03・VK13・SU3",
  purpose="動画のデモを自分の環境で再現できるかを、最初に確認します。<b>受注は「得意先・品目・条件・組織」の 4 つが揃わないと 1 件も作れません</b>。"
          "ここを飛ばすと、以降の練習で「なぜか保存できない」で止まります。",
  img="SPRO → 販売と流通（Sales and Distribution）／権限は <code>SU3</code> のプロファイルで確認。"
      "<b>動画の環境は SAP Training System / クライアント <code>800</code> / ユーザ <code>S000</code>・<code>tscm6-00</code></b> です（自システムの値に読み替えてください）。",
  tcode="<code>VA01</code>（初期画面）・<code>VA03</code>（照会）・<code>XD03</code>（得意先）・<code>MM03</code>（品目）・<code>VK13</code>（条件レコード）・<code>SU3</code>（ユーザプロファイル）・<code>SE16N</code>（テーブル照会）",
  input="""販売組織 1000 / 販売チャネル 10 / 部門 00      （＝販売エリア。動画のデモ値）
得意先     1000（Becker Berlin）または T-S62130（Teleko Textilien）
品目       T-ATA30（明細カテゴリ TAN になること）/ T-ATA29
受注タイプ OR（Standard Order）
支払条件   ZB01（14 Days 3%, 30/2%）  インコタームズ FOB
出荷プラント（品目マスタ 販売組織1 の値。動画では 1200）
与力条件   PR00（および税 MWST）が受注日を含む有効期間で存在すること""",
  items=[
   "<b>販売エリア</b>：<code>VA01</code> の初期画面で <code>1000</code>／<code>10</code>／<code>00</code> が F4 で選べること（選べない＝組織構造の割当未了）。",
   "<b>得意先</b>：<code>XD03</code> → 得意先 <code>1000</code> → <b>販売エリアビュー</b>があり、パートナー機能（<code>SP</code>／<code>BP</code>／<code>PY</code>／<code>SH</code>）と支払条件・インコタームズが入っていること。",
   "<b>品目</b>：<code>MM03</code> → 品目 <code>T-ATA30</code> → <b>販売組織 1</b>（出荷プラント・品目カテゴリグループ）、<b>販売組織 2</b>、<b>プラント在庫</b>ビューがあること。",
   "<b>与力条件</b>：<code>VK13</code> で <code>PR00</code>（価格）を照会。得意先×品目の組み合わせで有効な条件レコードがあること（<b>無いと Net value が 0 のままになります</b>）。",
   "<b>権限とユーザ設定</b>：<code>SU3</code> で自分のユーザ（動画では <code>tscm6-00</code>）の <b>住所・既定値（Defaults）・パラメータ（Parameters）</b>を確認。ここで受注の既定値を仕込んでおくと入力が減ります。",
  ],
  confirm="① <code>VA01</code> で <code>OR</code> ＋ 得意先 <code>1000</code> まで入れて Enter し、<b>概況画面（Create Standard Order: Overview）が開く</b>こと。<br>"
          "② 得意先が複数の販売エリアを持つ場合、動画と同じく「<b>Sales area for customer</b>」ダイアログが出ます（<code>09:02</code> 付近）。ここで選んだ販売エリアが以降のすべての基準になります。<br>"
          "③ 保存は<b>しない</b>で構いません（C0 は「入口が開くか」の確認だけ）。",
  trap="① 得意先を入れても販売エリアが選べない → 得意先マスタにその販売エリアビューが無い（<code>XD03</code>）。<br>"
       "② 与力条件が無く Net value が <code>0.00</code> → 受注の問題ではなく条件レコードの問題（<code>VK13</code> で有効期間を確認）。<br>"
       "③ 動画では<b>PO 番号が必須</b>になっています（保存時に「Enter PO number」のエラーが出る場面があります）。自システムの必須項目は <code>V.02</code>（不完全な受注一覧）で確認するのが早道です。",
  work="C0 の 5 項目を一覧にし、<b>自分の環境の実測値</b>（得意先番号・品目番号・販売エリア・出荷プラント・与力条件の有無）を書いてください。この一覧は練習⑤の故障切り分けで最初に見る資料になります。",
 ),
 dict(
  id="c1", no="C1", title="伝票タイプ（Sales Document Types）— 動画の Customizing ①",
  tc="VOV8・SE16N（TVAK）",
  purpose="受注タイプは<b>受注処理の「性格」を決める 1 番の設定</b>です。動画（<code>51:35</code> 付近）では <code>VOV8</code> の詳細画面が実演され、"
          "出荷・請求まわりの項目（納入タイプ・納入ブロック・出荷条件・即時出荷・請求タイプ・請求ブロック）が示されます。"
          "<b>動画が見ているのは一覧（238 エントリ）と、その中の <code>CR</code>（Credit Memo Request）の詳細</b>です。"
          "<code>OR</code> の詳細は値が違うので、<b>自分の環境で <code>OR</code> の詳細を開いて読み替えてください</b>"
          "（所要量タイプ・ブロックの有無・請求タイプは伝票タイプごとに違います）。",
  img="SPRO → 販売と流通 → 販売 → 販売伝票 → 販売伝票ヘッダ → <b>販売伝票タイプを定義</b>（呼称はリリースで異なる。SPRO の検索窓に「販売伝票タイプ」で探すのが確実）",
  tcode="<code>VOV8</code>（伝票タイプの定義＝動画で実演）／<code>SE16N</code> でテーブル <code>TVAK</code>（伝票タイプ）・<code>TVAKT</code>（名称）を確認",
  input="""伝票タイプ：OR（Standard Order）  ← 標準。練習では ZOR1 を作る
今回の練習で作るもの（推奨）：
  伝票タイプ ZOR1   名称 Z受注（練習用）  ← OR をコピーして作成
  作成時に確認する主な項目：
    与力関連／明細カテゴリ決定／価格決定手順／与信・納入・請求ブロック
    出荷：納入タイプ（LF）・出荷条件・即時出荷
    請求：出荷関連請求タイプ・受注関連請求タイプ（例 G2 Credit Memo）・請求ブロック（例 08）
    テキスト・出力決定手順・不完全性手順（→ C14）""",
  items=[
   "<code>VOV8</code> を起動 → 一覧（動画では <b>238 エントリ</b>）で <code>OR</code> を確認 →「照会」→「コピー（<code>新しいエントリを作成</code>／Copy As）」で <b><code>ZOR1</code></b> を作る。",
   "<b>明細カテゴリ決定</b>・<b>価格決定手順</b>・<b>不完全性手順</b>・テキスト決定手順を、<code>OR</code> と同じ値で引き継がせる（練習では変えない）。",
   "<b>出荷ブロック</b>を確認：標準 <code>OR</code> は空。ここに値を入れると、その伝票タイプで作った受注が<b>最初から出荷ブロック付き</b>になります（練習②で実験）。",
   "<b>請求ブロック</b>を確認：動画の <code>VOV8</code> 詳細画面では <code>08 Check credit memo</code> のような値が出ています（<code>CR</code> の受注関連請求タイプ <code>G2</code> = Credit Memo）。<b>これは CR の値なので、OR では別の値になります</b>。",
   "<b>照会だけなら <code>VOV8</code> は表示モードでも安全</b>です。変更は必ずカスタマイジング依頼（Transport）に入れてください。",
  ],
  confirm="① <code>VOV8</code> の一覧に <code>OR</code> と作成した <code>ZOR1</code> が並んでいる。<br>"
          "② 詳細画面で<b>出荷・請求・与信・不完全性の各グループ</b>の値を読み上げられること（動画と同じ項目を指せること）。<br>"
          "③ <code>SE16N</code> で <code>TVAK</code> を見て、同じ伝票タイプが 1 行になっていること（画面とテーブルが一致することを確認）。",
  trap="① <b>標準 <code>OR</code> を直接変更してしまう</b> → 以降の標準動作が変わります。<b>必ず Z コピー</b>。<br>"
       "② 伝票タイプを変えたのに受注の挙動が変わらない → 既存受注は<b>作ったときの設定を保持</b>します（新規受注で確認）。<br>"
       "③ 出荷タイプ・請求タイプの<b>決定は伝票タイプ側と品目側の両方</b>が絡みます（出荷タイプは出荷タイプ決定テーブル）。「設定したのに反映されない」は決定テーブルを確認。",
  work="<code>VOV8</code> で <code>OR</code> の詳細を開き、<b>出荷／請求グループの項目名を 6 つ書き出して</b>、それぞれ「受注の何を決めるか」を 1 行で説明してください。",
 ),
 dict(
  id="c2", no="C2", title="明細カテゴリ（Item Categories）— 明細の性格を決める",
  tc="VOV7・SE16N（TVAP・TSTL）",
  purpose="明細カテゴリは<b>「その明細が何をするか」</b>を決めます。動画のデモでは明細カテゴリは <code>TAN</code>（Standard Item）です。"
          "ここが変わると、所要量が作られるか（受注在庫になるか）、在庫確認（ATP）をするか、価格を探すか、が変わります。",
  img="SPRO → 販売と流通 → 販売 → 販売伝票 → 販売伝票明細 → <b>販売伝票明細カテゴリを定義</b>",
  tcode="<code>VOV7</code>／<code>SE16N</code>（<code>TVAP</code>＝明細カテゴリ、<code>TVAPT</code>＝名称）",
  input="""明細カテゴリ：TAN（Standard Item）  ← ドイツ語 „Standard“ 由来。動画のデモの値
確認する主な項目：
  一般：明細カテゴリグループ／高レベル明細カテゴリ（構造）
  与力：与力関連（Pricing relevant）
  所要量：所要量タイプ（TAN は空＝所要量を作らない）
  在庫：在庫管理（在庫を持つか）
  請求：請求関連、請求タイプの決定
  納入日程：納入日程行カテゴリの決定（→ VOV5）""",
  items=[
   "<code>VOV7</code> で <code>TAN</code> の詳細を開き、<b>「所要量タイプ」が空</b>であることを自分で確認する（＝<code>TAN</code> は在庫を持たない標準明細）。",
   "同じ画面で <b>「与力関連」が ON</b>であることを確認（＝与力価格が決定される）。",
   "明細カテゴリの一覧で <code>TAE</code>／<code>TAB</code>（見積・照会など）や <code>TANN</code> などの違いを見て、<b>受注（<code>TAN</code>）と見積の明細カテゴリが別物</b>であることを確認。",
   "練習用を作る場合は <code>ZTAN</code>（<code>TAN</code> のコピー）を作り、以降の決定テーブルは <code>ZTAN</code> で試す。",
  ],
  confirm="① <code>VOV7</code> で <code>TAN</code> の「所要量タイプ」が空／「与力関連」が ON であること。<br>"
          "② <code>VA03</code> で動画と同じ受注（明細カテゴリ <code>TAN</code>、品目 <code>T-ATA30</code>）を開き、<b>画面の明細カテゴリと設定画面が一致</b>すること。<br>"
          "③ <code>MD04</code> で <code>T-ATA30</code> を見て<b>所要量が作られていない</b>こと（＝<code>TAN</code> は所要量作成をしない）を確認。",
  trap="① 「受注したのに MRP で何も起きない」→ <b><code>TAN</code> では正常</b>です。受注在庫・所要量は戦略グループと所要量クラスを持つ品目（→ <code>../sapmto/</code>）の話。<br>"
       "② 明細カテゴリを変えると<b>既存の納入日程行・請求関連の挙動も変わる</b>ため、後続伝票がある受注では変更しない。<br>"
       "③ <code>TAN</code> と <code>TAE</code>（見積）を混同しない。<b>照会・見積・受注で明細カテゴリが違うのは正常</b>です。",
  work="<code>VOV7</code> で <code>TAN</code>／<code>TAE</code>／<code>TAB</code> の 3 つを比較し、<b>所要量タイプ・与力関連・在庫管理</b>の 3 項目の違いを表にしてください。",
 ),
 dict(
  id="c3", no="C3", title="得意先勘定グループ（Customer Account Groups）— 動画の Customizing ②",
  tc="OVT0・XD02",
  purpose="動画（<code>52:54</code>〜<code>54:09</code>）は <code>OVT0</code> で<b>得意先勘定グループ</b>の詳細画面を実演します。"
          "勘定グループは<b>得意先の番号範囲・項目ステータス（必須/表示のみ）・パートナー決定手順・出力決定手順</b>を決める、"
          "得意先マスタの「型」です。動画では <code>0001 Sold-to party</code>／<code>0002 Goods recipient</code>／<code>0003 Payer</code>／<code>0004 Bill-to party</code> が一覧で示されます。",
  img="SPRO → 財務会計／販売と流通 → 基本機能 → <b>取引先 → 得意先 → 得意先勘定グループを定義</b>（<code>OVT0</code>）",
  tcode="<code>OVT0</code>（動画で実演）／<code>XD02</code>（得意先マスタで使用中の勘定グループを確認）",
  input="""動画で確認できる勘定グループ（標準）：
  0001 Sold-to party     0002 Goods recipient    0003 Payer
  0004 Bill-to party     0005 Prospective customer
  0006 Competitor        0007 Sales partner
勘定グループ 0001 の詳細（動画の画面）：
  番号範囲 01 ／ One-time acct（未チェック）
  項目ステータス：General data／Company code data／<b>Sales data</b>
  （動画では Competitors／Sales partner／Prospect／Default SP／Consumer の各チェックが外れている）""",
  items=[
   "<code>OVT0</code> を起動 → 一覧で <code>0001</code>〜<code>0007</code> を確認（動画と同じ並び）。",
   "詳細画面で <b>「Expand field status」</b>を押し、<b>項目ステータス（必須／任意／表示のみ）</b>を確認する（＝どの項目が受注登録時に必須になるかの源流）。",
   "<b>番号範囲</b>を確認（動画は <code>01</code>）。<code>XD01</code> で得意先を新規作成するとき、この番号範囲が採番に使われます。",
   "<b>パートナー決定手順</b>・<b>出力決定手順</b>の欄を確認（動画の画面にも <code>PartnDet.Proc.</code>／<code>OutputDet.Proc.</code> が出ています）。受注のパートナーがどう決まるかはここが起点。",
   "<code>XD02</code> で得意先 <code>1000</code> を開き、上部の<b>勘定グループ</b>が何になっているかを確認（この得意先がどの「型」かが分かります）。",
  ],
  confirm="① <code>OVT0</code> の一覧に <code>0001</code>〜<code>0007</code> があること。<br>② 得意先 <code>1000</code> の勘定グループが分かること（<code>XD02</code>）。<br>"
          "③ 「勘定グループを変えると何が変わるか」を 3 つ言えること（<b>番号範囲・項目ステータス・パートナー/出力決定手順</b>）。",
  trap="① <b>使用中の得意先の勘定グループを変える</b> → 番号範囲・項目ステータスが変わり、既存データと矛盾することがあります（業務では原則変更しない）。<br>"
       "② 「受注で住所が必須にならない」→ 勘定グループの項目ステータスが原因（<code>OVT0</code>）。<b>受注側の設定だと思い込むと迷子になります</b>。",
  work="<code>OVT0</code> で <code>0001</code> と <code>0002</code> の項目ステータスを比べ、<b>違いが業務上何を意味するか</b>を 3 行で書いてください。",
 ),
 dict(
  id="c4", no="C4", title="得意先グループ（Customer Groups）— 動画の Customizing ③",
  tc="OVS9・XD02",
  purpose="動画（<code>52:22</code> 付近）は <code>OVS9</code> で<b>得意先グループ</b>の一覧（47 エントリ）を実演します。"
          "得意先グループは得意先の<b>分類（統計・分析のキー）</b>で、受注処理そのものを制御する設定ではありません。"
          "「制御する設定」と「分析用の属性」を区別できることが、この節の目的です。",
  img="SPRO → 販売と流通 → 販売 → マスタデータ → 得意先 → <b>得意先グループを定義</b>",
  tcode="<code>OVS9</code>（動画で実演）／<code>XD02</code> の販売エリアデータ → 販売タブ（得意先の得意先グループ欄）",
  input="""動画で確認できる得意先グループ：
  01 Industrial customers      02 Trading companies
  03 Development partners      04 Wholly-owned subsid.
  05 Part-owned subsidi.       06 Competition
  07 Public sector             10 Private customer
  20 CP Mass                    （ほか、計 47 エントリ）""",
  items=[
   "<code>OVS9</code> を起動し、一覧が動画と同じ並び（<code>01</code>〜）であることを確認する。",
   "<code>XD02</code> → 得意先 <code>1000</code> → <b>販売エリアデータ → 販売タブ</b>で「得意先グループ」欄を確認（動画 <code>51:22</code> 付近の画面にも出ています）。",
   "自分の環境で使う予定のグループ（例 <code>01</code> Industrial customers）を 1 つメモする。",
  ],
  confirm="① <code>OVS9</code> の一覧が読めること。<br>② <code>XD02</code> で得意先の得意先グループが確認できること。<br>"
          "③ <b>得意先グループは「分析・統計の分類」であり、与力価格や明細カテゴリを直接決める設定ではない</b>と言えること。",
  trap="① <code>OVS9</code> が「得意先グループ（Customer groups）」で、<b>勘定グループ（Account groups, <code>OVT0</code>）とは別物</b>です。名前が似ているので混同注意。<br>"
       "② 得意先グループを変えただけで受注の挙動（ブロック・価格）が変わると思い込む → 変わりません（分析属性です）。",
  work="「得意先グループ」と「得意先勘定グループ」の違いを、<b>① 決めるもの ② T-code ③ 変更したときに起こること</b>の 3 観点で表にしてください。",
 ),
 dict(
  id="c5", no="C5", title="SIS レポートビュー（Sales Summary <code>VC/2</code> の画面設計）— 動画の Customizing ④",
  tc="SPRO（4 画面）・VC/2",
  purpose="動画（<code>27:06</code>〜<code>28:29</code>）が最も長く割いている Customizing です。<b><code>VC/2</code>（Sales Summary）に何が出るかは、"
          "ここで決まります</b>。受注処理の「ツールとヘルプ」の後半を担う内容で、動画では 4 つの表が実演されます。",
  img="SPRO → 販売と流通 → 販売サポート（CAS）／情報システム（SIS）→ <b>リスト（Lists）</b> → レポートビュー関連の 4 アクティビティ",
  tcode="<code>SPRO</code>（IMG）／<code>VC/2</code>（Sales Summary 本体）／<code>SM30</code>・<code>SM31</code>（同じ表を直接保守する場合）",
  input="""動画の 4 画面（この順に実演されます）：

① Maintain Report Views（情報ビューの定義）
   001 Complete information（Standard＝チェック済み / Form SD-SALES-SUMMARY）
   002 Address/partner info   003 Statistical info   005 Telesales
   100 Credit Information     101 Last SD Documents 102 Backorders
   103 Quick Info             900 New Internet cust.

② Maintain Views for an Evaluation（ビューへ情報ブロックを順番つきで割当）
   例：Info view 001 Complete information
       Seq 001 Address / 002 Customer Classific. / 003 Performance Measures /
           004 Contact persons / 005 Sales Order Info / 006 Customer Pricing /
           007 Cust Delivery Info / 008 Partial Deliv. Info / 009 Cust Transport Info …
      （動画では 51 ブロック。詳細画面で Form / Window / Element まで持ちます）

③ Maintain the Report Views for a User（ユーザ別の既定ビュー）
   例：ユーザ BAPMS → ビュー ZPD（Precision Drilling V）
       ユーザ WF-SD-2 → ビュー 900（New Internet cust.）

④ Last Documents for a Customer（既存伝票の統計更新）
   文書カテゴリごとの「Statistics update desired」：
     1 Sales activities(CAS) 2 External transaction 3 Invoice list 4 Credit memo list
     5 Intercompany invoice  6 Intercompany credit me. A Inquiry B Quotation(チェック)
     C Order(チェック) D Item proposal …（動画では <b>B Quotation・C Order・Delivery・Credit memo request</b> にチェックが入っています）""",
  items=[
   "<code>SPRO</code> →「SAP Reference IMG」→ 販売と流通（Sales and Distribution）配下で<b>「リスト（Lists）」</b>を開き、動画と同じ 4 つのアクティビティを見つける（<b>Set Updating Of Partner Index／Item Index／Define Selection Criteria／Define List Layout Of Expected Customer Price</b> が並ぶ画面が動画に出ます）。",
   "<b>① Maintain Report Views</b>：情報ビューの一覧を確認。動画では <code>001</code> にだけ Standard チェックが入っています（＝既定で完全情報が出る理由）。",
   "<b>② Maintain Views for an Evaluation</b>：行を選んで詳細を開き、<b>Form / Window / Element</b>（例 Form <code>SD-SALES-SUMMARY</code> / Window <code>MAIN</code> / Element <code>LIST1_001</code>）まで確認する。",
   "<b>③ Maintain the Report Views for a User</b>：自分のユーザが入っていなければ、<b>動画と同じように 1 行追加して既定ビューを割り当てる</b>（練習では <code>001</code> か <code>101</code> を推奨）。",
   "<b>④ Last Documents for a Customer</b>：文書カテゴリ <b><code>C Order</code></b> の Statistics update が ON であることを確認（OFF だと <code>VC/2</code> の Last SD documents に受注が出ません）。",
   "<code>VC/2</code> を起動し、得意先 <code>1000</code> を入れて「<b>View</b>」ボタンで<b>動画と同じ情報ビュー一覧（<code>001</code>〜<code>900</code>）</b>が出ることを確認する。",
  ],
  confirm="① <code>VC/2</code> の「View」で、<code>001</code>／<code>002</code>／<code>003</code>／<code>005</code>／<code>100</code>／<code>101</code>／<code>102</code>／<code>103</code>／<code>900</code> が並ぶこと（動画と同じ）。<br>"
          "② ビュー <code>101</code>（Last SD Documents）を選ぶと、<b>受注と請求書の一覧（番号・日付・正味価額・ステータス）</b>が出ること。<br>"
          "③ 自分を「Report Views for a User」に割り当てた場合、<code>VC/2</code> の初期表示がそのビューになること。",
  trap="① <b>情報ビューが 1 つも出ない／少ない</b> → <code>001</code> の定義が無い、またはユーザ別割当がおかしい（①②③のどれか）。<br>"
       "② <b>Last SD documents が空</b> → 「Last Documents for a Customer」で <code>C Order</code> の統計更新が OFF、またはその得意先に伝票が無い。<br>"
       "③ SIS のフレキシブル分析は<b>統計ファイルの初期構築</b>が必要な環境があります。動画の環境（IDES/教育用）では既に構築済みなので、疑うのは最後にしてください。<br>"
       "④ 動画の概念スライドに出てくる得意先 <code>5264</code>（FA IDES, Walldorf）は<b>スライド用の例</b>です。実演は得意先 <code>1000</code> です。",
  work="<code>VC/2</code> を得意先 <code>1000</code> ・ビュー <code>001</code> とビュー <code>101</code> で表示し、<b>出てくる情報ブロックの違いを一覧</b>にしてください。そのうえで「③ Report Views for a User に行を足すと何が変わるか」を予想してから実際に試してください。",
 ),
 dict(
  id="c6", no="C6", title="納入日程行カテゴリ（Schedule Line Categories）",
  tc="VOV6",
  purpose="納入日程行（Schedule line）は<b>「いつ、いくつ納入するか」</b>を持ち、<b>所要量タイプと在庫確認（ATP）</b>がここに付きます。"
          "「受注したのに在庫確認が走らない／所要量が出ない」は、ほとんどの場合この設定です。",
  img="SPRO → 販売と流通 → 販売 → 販売伝票 → 販売伝票明細 → <b>納入日程行カテゴリを定義</b>",
  tcode="<code>VOV6</code>／<code>SE16N</code>（<code>TVEP</code>＝納入日程行カテゴリ）／<code>VA03</code>（明細 → 納入日程行）",
  input="""納入日程行カテゴリの例（環境により異なる。動画のデモは 明細 TAN の標準）：
  項目：所要量タイプ（Requirement type）／在庫確認（Availability check）／
        納入日付タイプ（Delivery date type）／納入数量提案／与力関連 など
確認の手順：
  1) VA03 で受注を開く → 明細 → 納入日程行 → カテゴリを読む
  2) VOV6 でそのカテゴリを開き、所要量タイプと在庫確認を読む
  3) 品目マスタ（MM03 → MRP3）の<b>戦略グループ</b>と突き合わせる""",
  items=[
   "<code>VA03</code> で動画と同じ受注を開き、明細の<b>納入日程行</b>を展開して<b>カテゴリ</b>を確認する（例：明細 <code>TAN</code> に対する標準の納入日程行カテゴリ）。",
   "<code>VOV6</code> でそのカテゴリを開き、<b>所要量タイプ</b>と<b>在庫確認</b>の値を確認する。",
   "<b>品目マスタ（<code>MM03</code> → MRP3）</b>で <b>戦略グループ</b>を確認し、納入日程行カテゴリの所要量タイプと<b>整合</b>しているかを見る。",
   "在庫確認の 3 階層（<b>伝票タイプ → 納入日程行カテゴリ → 品目マスタ</b>）を、<code>OVZ2</code>（伝票タイプ側）と <code>MM03</code> で突き合わせる（詳細は C13）。",
  ],
  confirm="① <code>VA03</code> の納入日程行カテゴリが読めること。<br>② そのカテゴリの<b>所要量タイプ</b>と、品目マスタ MRP3 の<b>戦略グループ</b>が対応して説明できること。<br>"
          "③ <code>MD04</code> で、<b>所要量タイプが空の場合は何も出ない</b>ことを確認（<code>TAN</code> の標準挙動）。",
  trap="① <b>標準値は環境・リリースで異なります</b>（動画のデモは 2007 年頃の R/3）。<b>暗記せず、<code>VA03</code> と <code>VOV6</code> で確認する習慣</b>を付けてください。<br>"
       "② 納入日程行カテゴリを変えると<b>所要量・ATP・納入日の決まり方が同時に変わります</b>。1 項目ずつ変えて差分を見る。",
  work="受注 1 件について「明細カテゴリ → 納入日程行カテゴリ → 所要量タイプ → 品目マスタの戦略グループ」を 1 本の線で書き出してください。",
 ),
 dict(
  id="c7", no="C7", title="伝票タイプ × 明細カテゴリの割当（許可テーブル）",
  tc="VOV4",
  purpose="<b>明細カテゴリ決定の前段</b>です。伝票タイプごとに「使ってよい明細カテゴリ」を許可します。ここに無いカテゴリは<b>受注に投入できません</b>"
          "（画面には入るが、Enter でエラーや別カテゴリに変わる）。",
  img="SPRO → 販売と流通 → 販売 → 販売伝票 → 販売伝票明細 → <b>伝票タイプごとに明細カテゴリを割当</b>",
  tcode="<code>VOV4</code>（割当と決定の両方がある。練習では「割当」側）／<code>SE16N</code>（<code>TVAK</code>・<code>TVAP</code> と割当の関係）",
  input="""例（動画のデモに倣う）：
  伝票タイプ OR に許可する明細カテゴリ：TAN（標準）／TAX 系（無償）／TANN ほか
  練習で作る場合：ZOR1 → ZTAN を追加し、OR の標準は変えない
注意：品目使用目的（Usage）や高レベル明細カテゴリの組み合わせで
      「使う／使わない」が更に分かれる場合があります（返品・無償など）""",
  items=[
   "<code>VOV4</code> の該当ビューで、伝票タイプ <code>OR</code> に許可されている明細カテゴリの一覧を確認する。",
   "<b>明細カテゴリを 1 つ追加して試す</b>（例：練習用に <code>ZTAN</code> を作り、<code>ZOR1</code> に割り当てる）→ <code>VA01</code> で <code>ZOR1</code> を使い、品目を入れて<b>明細カテゴリが <code>ZTAN</code> になる</b>ことを確認。",
   "逆に、許可していない明細カテゴリを指定しようとしたときの<b>挙動（エラー／代替）を記録する</b>（故障対照表の材料になります）。",
  ],
  confirm="① <code>OR</code>（または <code>ZOR1</code>）で <code>TAN</code> が使えること。<br>② 追加したカテゴリが新規受注で実際に使われること（<code>VA01</code> → 明細詳細で確認）。<br>"
          "③ 「割当（許可）」と「決定（自動でどれになるか）」は<b>別の仕組み</b>だと説明できること（決定は C8）。",
  trap="① <b>割当だけ足して決定テーブルを足し忘れる</b> → 自動では選ばれず、手で入れてもエラーになることがあります（C8 とセットで）。<br>"
       "② 標準の <code>OR</code> の割当を削ると、既存の標準業務が止まります。<b>Z 伝票タイプで練習</b>。",
  work="<code>VOV4</code> で「割当」と「決定」の 2 画面を開き、<b>それぞれ何を決めているか</b>を 1 行ずつで書き分けてください。",
 ),
 dict(
  id="c8", no="C8", title="明細カテゴリ決定（決定テーブル）— 受注処理の心臓",
  tc="VOV4・VOV7・SE16N",
  purpose="<b>「なぜこの明細カテゴリになるのか」の答えがここにあります。</b>"
          "販売伝票タイプ × 品目カテゴリグループ × 品目使用目的 × 高レベル明細カテゴリ の 4 キーで明細カテゴリが決まります。",
  img="SPRO → 販売と流通 → 販売 → 販売伝票 → 販売伝票明細 → <b>明細カテゴリ決定</b>",
  tcode="<code>VOV4</code>（決定テーブル）／<code>VOV7</code>（カテゴリ定義）／<code>MM03</code>（品目カテゴリグループ）／<code>VA03</code>（結果の確認）",
  input="""決定テーブルのキー（動画のデモで実際に使われている値）：
  販売伝票タイプ        OR
  品目カテゴリグループ  （品目 T-ATA30 の値。品目マスタ 販売組織2 の「品目カテゴリグループ」）
  品目使用目的          （空。返品・無償などで値が入る）
  高レベル明細カテゴリ  （空。BOM 親明細などの構造で使う）
  → 明細カテゴリ        TAN（Standard Item）

確認の順序：
  1) VA03 で明細カテゴリ（TAN）を読む
  2) MM03 の販売組織2 で品目カテゴリグループを読む
  3) VOV4 の決定テーブルで 4 キー → TAN の行を探す""",
  items=[
   "<code>MM03</code> → 品目 <code>T-ATA30</code> → <b>販売組織 2</b> ビューで<b>品目カテゴリグループ</b>を読む。",
   "<code>VOV4</code> の明細カテゴリ決定テーブルで、<b><code>OR</code> × その品目カテゴリグループ × 空 × 空</b>の行を探し、結果が <code>TAN</code> であることを確認する。",
   "<b>品目カテゴリグループを別の値にした品目</b>（例：<code>T-ATA29</code> や別の品目）で受注を作り、<b>明細カテゴリが変わるか</b>を観察する（変わらなければ決定テーブルの別行が効いています）。",
   "練習として、<b>決定テーブルに 1 行追加</b>して（<code>ZOR1</code> × 品目カテゴリグループ × 空 × 空 → <code>ZTAN</code>）、新規受注で反映されることを確認する。",
  ],
  confirm="① <code>VA03</code> の明細カテゴリと、<code>VOV4</code> の決定テーブルの結果が<b>一致</b>すること。<br>"
          "② 4 つのキーの名前を、資料を見ずに言えること（<b>伝票タイプ・品目カテゴリグループ・品目使用目的・高レベル明細カテゴリ</b>）。<br>"
          "③ 追加した行が新規受注で効くこと（既存受注には効かないことを確認）。",
  trap="① <b>決定テーブルに行が無い</b> → 受注に品目を入れた時点でエラー、または別のカテゴリにフォールバック。必ずキー 4 つを確認。<br>"
       "② <b>品目使用目的（Usage）や高レベル明細カテゴリが意図せず入る</b> → 参照コピーした受注・BOM 品目で起こりやすい。<code>VA03</code> の明細詳細で確認。<br>"
       "③ 伝票タイプを変えても既存受注の明細カテゴリは変わりません（<b>新規受注で確認</b>）。",
  work="品目カテゴリグループの<b>違う品目を 2 つ</b>選び、それぞれの受注で明細カテゴリがどうなるかを実測して表にしてください（キー 4 つと結果の組で）。",
 ),
 dict(
  id="c9", no="C9", title="納入日程行カテゴリの決定",
  tc="VOV5・VOV6",
  purpose="明細カテゴリと所要量タイプから<b>納入日程行カテゴリ</b>を決めるテーブルです。"
          "ここが <b>在庫確認（ATP）と所要量作成の入口</b>になります。",
  img="SPRO → 販売と流通 → 販売 → 販売伝票 → 販売伝票明細 → <b>納入日程行カテゴリの決定</b>",
  tcode="<code>VOV5</code>（決定）／<code>VOV6</code>（定義）／<code>VA03</code>（結果確認）",
  input="""キー：明細カテゴリ × 所要量タイプ（品目マスタ MRP3 由来）
  → 納入日程行カテゴリ（所要量タイプ／在庫確認／納入日付タイプを持つ）

確認の順序：
  1) VA03 の明細 → 納入日程行 → カテゴリを読む
  2) VOV5 でそのカテゴリに至るキーを特定する
  3) VOV6 でカテゴリの中身（在庫確認の有無）を読む""",
  items=[
   "<code>VA03</code> で受注の納入日程行カテゴリを確認する。",
   "<code>VOV5</code> の決定テーブルで、<b>明細カテゴリ × 所要量タイプ</b>の組み合わせを確認する。",
   "<code>VOV6</code> でそのカテゴリの<b>在庫確認</b>の値を確認し、C13 の 3 階層（伝票タイプ／納入日程行カテゴリ／品目マスタ）と突き合わせる。",
  ],
  confirm="① <code>VA03</code> → <code>VOV5</code> → <code>VOV6</code> の順で、<b>同じカテゴリに行き着く</b>こと。<br>② 在庫確認の ON/OFF がどこで決まっているかを言えること。",
  trap="① 所要量タイプが空だと<b>決定に至らない</b>ことがあります（<code>TAN</code> の標準はこのケース）。エラーではなく仕様です。<br>"
       "② <b>在庫確認の 3 階層の優先順位</b>を混同しやすい（C13 で整理）。",
  work="「明細カテゴリ → 所要量タイプ → 納入日程行カテゴリ → 在庫確認」の 4 段を、自システムの実値で 1 本の線にしてください。",
 ),
 dict(
  id="c10", no="C10", title="出荷プラントの自動提案（3 つの優先順位）",
  tc="VD51/VD52/VD53・XD02・MM02・VBAP",
  purpose="動画が独立したスライドを割いた論点（<code>19:51</code> 付近）です。"
          "<b>受注明細の出荷プラントは、3 つの主データから優先順位つきで提案されます</b>。"
          "「品目マスタを直したのに反映されない」を防ぐのがこの STEP の目的です。",
  img="SPRO → 販売と流通 → 基本機能 → マスタデータ → <b>客先品目情報</b>／得意先マスタ・品目マスタ側は各マスタの保守画面",
  tcode="<code>VD51</code>（客先品目情報の登録／<code>VD52</code>・<code>VD53</code>）／<code>XD02</code>（得意先：販売エリアデータ → 出荷タブ）／<code>MM02</code>（品目：販売組織 1）／<code>SE16N</code>（<code>KNMT</code>・<code>KNVV</code>・<code>MVKE</code>）",
  input="""優先順位（上が強い。動画のスライドと同じ）：

  1. 客先品目情報（Customer-Material Info Record）  VD51/VD52/VD53
     動画スライド：C1 × M1 × 客先品目コード PC-100 → 出荷プラント 1400

  2. 得意先マスタ（出荷先の販売エリアデータ）      XD02 → 出荷タブ
     動画スライド：得意先マスタ S1 → 出荷プラント 1100

  3. 品目マスタ（販売組織 1 ビュー）               MM02 → 販売組織 1
     動画スライド：品目マスタ M1 → 1000 / M2 → 1200
     （本編デモの品目 T-ATA30 は 1200 ＝ Change Plant で 1000 Dresden を選ぶ場面もあり）""",
  items=[
   "<b>3 か所を順に開いて、動画のデモ品目の実値を書き出す</b>：<code>VD53</code>（得意先×品目）→ <code>XD03</code>（出荷先の販売エリアデータ → 出荷タブ）→ <code>MM03</code>（販売組織 1 の出荷プラント）。",
   "<b>わざと 3 か所に違う値を入れて、受注でどれが勝つかを実測する</b>（練習では <code>XD02</code> と <code>MM02</code> の 2 か所から開始し、最後に <code>VD51</code> を追加）。",
   "受注（<code>VA01</code>）で明細を入れ、<b>Deliver.Plant に何が入ったか</b>を記録する。",
   "<code>SE16N</code> で <code>VBAP</code>（受注明細）の <code>WERKS</code> と、<code>MVKE</code>／<code>KNVV</code>／<code>KNMT</code> の該当項目を並べて見る（<b>どの源泉が効いたかを証拠で示す</b>）。",
  ],
  confirm="① <b>3 か所すべての値</b>を書き出し、受注に入った値が<b>優先順位どおり</b>であること。<br>"
          "② 「品目マスタを変えても受注が変わらない」場合、<b>上位 2 か所（客先品目情報・得意先マスタ）に値が入っている</b>ことを証拠として示せること。<br>"
          "③ <code>VBAP-WERKS</code> で受注明細の出荷プラントを直接確認できること。",
  trap="① <b>品目マスタだけ見て終わる</b>のが最頻出の誤り。<b>3 か所を見る</b>癖を付けてください。<br>"
       "② 動画のスライドには <b>“Weighting the different sources of information during plant determination”</b> とあり、"
       "標準の順序は <b>ABAP（USEREXIT 等）で上書き</b>され得ます（SAP Note <b>2787562</b>）。"
       "3 か所すべて空／矛盾しているのに想定外のプラントが入る場合は、拡張を疑って講師に確認してください。<br>"
       "③ 出荷プラントが変わると<b>出荷ポイントと出荷タイプも再決定</b>されます（後続伝票があると影響大。練習では後続伝票の無い受注で）。",
  work="3 か所の値を 1 枚の表にし、<b>「どこを消せばどの値が採用されるか」</b>を予想してから実測してください（予想と結果の差が学習効果になります）。",
 ),
 dict(
  id="c11", no="C11", title="パートナー機能と決定（得意先マスタ側）",
  tc="XD02・OVT0・VBPA",
  purpose="受注の 4 役割（<code>SP</code>／<code>SH</code>／<code>BP</code>／<code>PY</code>）は、"
          "<b>得意先マスタのパートナー機能</b>と<b>勘定グループ／伝票タイプのパートナー決定手順</b>から自動提案されます。"
          "動画の <code>XD02</code> 実演（<code>51:10</code> 付近）がまさにこの画面です。",
  img="SPRO → 販売と流通 → 基本機能 → パートナー → <b>パートナー決定手順を設定</b>／得意先側は <code>XD02</code>",
  tcode="<code>XD02</code>（販売エリアデータ → パートナー機能タブ）／<code>OVT0</code>（勘定グループのパートナー決定手順）／<code>SE16N</code>（<code>VBPA</code>＝受注のパートナー、<code>KNVP</code>＝得意先のパートナー）",
  input="""動画の XD02（得意先 1000）で確認できるもの：
  パートナー機能一覧：SP Sold-to party 1000 / BP Bill-to party 1000（＋ SH・PY など）
  その近くのブロック：Delivery and payment terms（Incoterms／Terms of payment／
                       Paym.guar.proc.／Credit ctrl area）
  販売タブ：Sales district／Sales Office／Sales Group／Customer group／
           ABC class／Currency／Order probab.  ← 動画 51:22 付近
受注側の対応：VA03 のヘッダ → パートナー（SP/SH/BP/PY と相手先）""",
  items=[
   "<code>XD02</code> → 得意先 <code>1000</code> → 販売エリア <code>1000/10/00</code> → <b>パートナー機能</b>タブで <code>SP</code>／<code>BP</code>／<code>PY</code>／<code>SH</code> の登録を確認する。",
   "同じ画面の <b>Delivery and payment terms</b>（インコタームズ・支払条件・与信管理エリア）を確認する（<b>受注の支払条件 <code>ZB01</code> の出所</b>）。",
   "<b>販売タブ</b>で Sales Office／Sales Group／得意先グループ／Order probability を確認する（動画 <code>51:22</code> の画面）。",
   "<code>VA01</code> で新規受注を作り、<b>パートナーが自動提案される</b>ことを確認する。出荷先だけ手で変えて、<b>何が再決定されるか</b>を見る（練習②の予習）。",
   "<code>SE16N</code> で <code>KNVP</code>（得意先のパートナー）と <code>VBPA</code>（受注のパートナー）を並べて見る。",
  ],
  confirm="① 得意先マスタの <code>SP</code>／<code>BP</code>／<code>PY</code>／<code>SH</code> が受注のパートナーに<b>そのまま提案される</b>こと。<br>"
          "② 支払条件 <code>ZB01</code> が<b>得意先マスタ由来</b>であることを、両画面で示せること。<br>"
          "③ <code>KNVP</code> と <code>VBPA</code> の対応が読めること。",
  trap="① <b>パートナーが出ない</b> → 得意先マスタのパートナー機能が未保守、またはパートナー決定手順（勘定グループ／伝票タイプ）の設定漏れ。<br>"
       "② 出荷先（<code>SH</code>）を変えたときの<b>再決定の範囲</b>を誤解しやすい（→ 概念 8 節）。<b>与力価格・出荷プラントは再決定、販売エリア・販売事務所は不変</b>。",
  work="得意先マスタのパートナー機能を 1 つ追加（例：別の出荷先）し、新規受注で<b>自動提案されるか／されないか</b>を確認して、理由を書いてください。",
 ),
 dict(
  id="c12", no="C12", title="与力価格決定（条件技術の入口）",
  tc="OVKK・V/06・V/07・V/08・VK11/VK13",
  purpose="受注の <b>Net value</b>（動画では <code>22,990.00 EUR</code>）がどこから来るのかを追えるようにします。"
          "価格は「条件レコード」から来ますが、<b>どの条件タイプを探すかは価格決定手順が決める</b>という 2 段構造が要点です。",
  img="SPRO → 販売と流通 → 基本機能 → 与力（Pricing）→ <b>与力手順を定義</b>／<b>条件タイプを定義</b>／<b>アクセス順序を定義</b>",
  tcode="<code>OVKK</code>（価格決定手順の割当＝販売伝票タイプ側）／<code>V/06</code>（条件タイプ）／<code>V/07</code>（アクセス順序）／<code>V/08</code>（条件テーブル）／<code>VK11</code>・<code>VK13</code>（条件レコード）",
  input="""動画のデモで確認できるもの：
  受注の Net value：22,990.00 EUR（明細 10 PC 投入後。動画 19:27 付近）
  条件タイプ：PR00（価格）／MWST（税）／VPRS（在庫評価額）ほか
  確認の順序：
   1) VA03 の条件画面で、実際に決定された条件タイプと金額を読む
   2) その条件タイプの条件レコードを VK13 で照会（得意先×品目の有効期間）
   3) VOV8 で伝票タイプ OR の「価格決定手順」を確認 → OVKK で手順の中身
   4) V/07 でアクセス順序（どの条件テーブルをどの順で探すか）""",
  items=[
   "<code>VA03</code> で受注を開き、<b>条件画面（与力分析）</b>を表示して、決定された条件タイプと金額を書き出す。",
   "<code>VK13</code> でその条件タイプ（<code>PR00</code>）を照会し、<b>有効期間と金額</b>を確認する（受注日が期間内かどうかが肝）。",
   "<code>VOV8</code> → 伝票タイプ <code>OR</code> の詳細で<b>価格決定手順</b>を確認し、<code>OVKK</code> でその手順に含まれる条件タイプの順序を見る。",
   "<b>わざと条件を無効化</b>（または期間外にして）受注を作り、<b>Net value が 0 になる／警告が出る</b>ことを観察する（故障対照表の材料）。",
  ],
  confirm="① 受注の Net value が<b>条件レコードの合計から説明できる</b>こと。<br>"
          "② 「どの条件タイプを探すかは価格決定手順が決める」と言えること（<b>手順 → 条件タイプ → 条件レコード</b>の 3 段）。<br>"
          "③ 条件を無効にしたときの症状（Net value 0／与力日付のエラー等）を記録したこと。",
  trap="① <b>条件レコードが無い／期間外</b> → Net value が 0。受注ではなく条件の問題（<code>VK13</code> で有効期間を確認）。<br>"
       "② 明細ごとに<b>与力日付（Pricing date）</b>が使われます。動画のデモでは与力日付 <code>02.06.2007</code> が出ています。<b>日付がずれると条件が拾われません</b>。<br>"
       "③ 手で条件を変更（手動条件）すると、後で<b>再決定で消える</b>ことがあります（練習②の再決定と関連）。",
  work="受注 1 件について、<b>条件画面の各行が「どの条件レコードのどの期間」から来たか</b>を 3 行分書き出してください。",
 ),
 dict(
  id="c13", no="C13", title="在庫確認（ATP）の 3 階層",
  tc="OVZ2・MM02（MRP3）・VOV6",
  purpose="「在庫があるのに受注で警告が出る／出ない」を切り分けられるようにします。"
          "<b>在庫確認は 伝票タイプ・納入日程行カテゴリ・品目マスタ の 3 か所で決まり、上位は下位を上書きできます</b>。",
  img="SPRO → 販売と流通 → 基本機能 → <b>在庫確認（Availability check）</b>／品目側は <code>MM02</code> → MRP3 → 在庫確認",
  tcode="<code>OVZ2</code>（伝票タイプ別の在庫確認）／<code>VOV6</code>（納入日程行カテゴリ側）／<code>MM02</code>・<code>MM03</code>（MRP3 の在庫確認）／<code>CO09</code>（与力可能数量の照会）／<code>MD04</code>",
  input="""3 つの階層（上位が優先。品目マスタが最下位）：
  1) 伝票タイプの在庫確認              OVZ2（例：OR は 在庫確認を実行しない、が既定のことが多い）
  2) 納入日程行カテゴリの在庫確認      VOV6（在庫確認の可否）
  3) 品目マスタ MRP3 の在庫確認        MM02/MM03（例 02 = 個別所要量ベース）
確認の道具：CO09（与力可能数量と不足）／MD04（所要量と在庫の流れ）""",
  items=[
   "<code>MM03</code> → 品目 → <b>MRP3</b> で「在庫確認」の値を確認する。",
   "<code>VOV6</code> で納入日程行カテゴリの在庫確認を確認し、<code>OVZ2</code> で伝票タイプ側を確認する。<b>3 か所の値を並べて書く</b>。",
   "<code>CO09</code> で品目とプラントを入れ、<b>与力可能数量</b>を確認する。",
   "<code>VA01</code> で在庫を超える数量を受注し、<b>警告が出るか／ブロックされるか</b>を記録する（伝票タイプ・品目の設定で挙動が変わることを体感する）。",
  ],
  confirm="① 3 階層のどこで在庫確認が ON になっているかを<b>実値で説明</b>できること。<br>"
          "② <code>CO09</code> の数量と、受注時の警告が<b>整合</b>していること。<br>"
          "③ 在庫確認が「されない」設定（動画の <code>TAN</code> は所要量タイプが空）では、<b>警告が出ないのが正常</b>であること。",
  trap="① <b>階層の優先順位を逆に覚える</b>と迷います。<b>伝票タイプ＞納入日程行カテゴリ＞品目マスタ</b>（品目側は最下位＝既定値）と整理してください。<br>"
       "② 所要量タイプが空の明細では在庫確認が走らないため、「ATP が効かない」のではなく「受注在庫を持たない明細だから」が答えです（→ <code>../sapmto/</code> で受注在庫の実習）。",
  work="同じ品目で「在庫確認 02」と「空」の 2 通りを作り、受注時の挙動を<b>症状つき</b>で記録してください（故障対照表に追記）。",
 ),
 dict(
  id="c14", no="C14", title="不完全性チェック（Incompletion）—「不完全な受注」はこう作られる",
  tc="OVA2・VUA2・VUP2・VUE2・V.02・SE16N",
  purpose="動画では <code>VA01</code> のデモ中に<b>「Enter PO number」の必須エラー</b>が出ます（<code>09:28</code> 付近）。"
          "これが不完全性チェックです。<b>どの項目が必須かを定義する側</b>を設定します。",
  img="SPRO → 販売と流通 → 基本機能 → <b>不完全項目のログ（Log of Incomplete Items）</b> → 不完全性手順を定義",
  tcode="<code>OVA2</code>（不完全性手順の定義）／<code>VUA2</code>（警告かエラーか）／<code>VUP2</code>（明細カテゴリへの割当）／<code>VUE2</code>（納入日程行カテゴリへの割当）／<code>V.02</code>（不完全な受注の一覧）／<code>V.00</code>（不完全な伝票の一覧）",
  input="""動画の環境で確認できる症状：
  PO 番号が必須（保存時に「Enter PO number」）
  → 受注の PO Number 欄に dddd / test 等のダミーを入れて保存している

定義の階層：
  不完全性手順（Procedure）     OVA2：手順に「グループ」を割り当てる
  グループ（Groups）            例：ヘッダ／明細／納入日程行／パートナー
  項目（Fields）                例：VBAP-POSEX（PO 番号）など
  挙動（Warning / Error）       VUA2
  適用先                        伝票タイプ（VOV8 の不完全性手順）／明細カテゴリ（VUP2）／
                                納入日程行カテゴリ（VUE2）
主要テーブル：TVUV（手順）・TVUVG（グループ）・TVUVF（項目）・
             VBUV（明細）・VBUP（明細ステータス）・VBUK（ヘッダステータス）""",
  items=[
   "<code>OVA2</code> を起動し、動画のデモ伝票タイプ <code>OR</code> に割り当てられている<b>不完全性手順</b>を確認する。",
   "その手順に含まれる<b>グループと項目</b>を開き、<b>PO 番号系の項目</b>が入っているかを探す（<b>動画の症状と設定を結びつける</b>）。",
   "<code>VUA2</code> で<b>警告／エラー</b>の設定を確認する（エラー＝保存不可、警告＝保存可）。",
   "<b>自分の練習用に 1 項目追加</b>して効果を見る（例：納入希望日を必須にする）→ <code>VA01</code> で空にして保存し、<b>症状を記録</b>。",
   "<code>V.02</code>（不完全な受注の一覧）を実行し、<b>わざと作った不完全な受注が一覧に出る</b>ことを確認する。<code>SE16N</code> で <code>VBUV</code>／<code>VBUK</code> も見る。",
  ],
  confirm="① 動画の「Enter PO number」が<b>どの設定に由来するか</b>を、<code>OVA2</code> を指して説明できること。<br>"
          "② 自分で追加した必須項目で、保存時にエラーが出ることを確認したこと。<br>"
          "③ 不完全な受注が <code>V.02</code> に表示されること（＝不完全なまま放置されない仕組み）。",
  trap="① 「PO 番号が必須なのは標準」と思い込む → <b>環境設定</b>です（動画の環境がそうなっているだけ）。<br>"
       "② エラーにしたまま<b>保存できない伝票を作る</b>と業務が止まります。運用的には<b>警告</b>にして <code>V.02</code> で管理するのが一般的。<br>"
       "③ 変更は<b>伝票タイプ・明細カテゴリ・納入日程行カテゴリの 3 か所</b>に分かれます。「設定したのに効かない」は適用先を確認。",
  work="不完全性チェックの<b>3 階層（手順／グループ／項目）</b>を図にし、<b>動画の PO 番号</b>がどこに入るかを書き込んでください。",
 ),
 dict(
  id="c15", no="C15", title="コピー管理（受注 → 出荷 → 請求）",
  tc="VTAA・VTFL・VTFA・VTFA（請求）",
  purpose="参照コピーしたときに<b>どの値を引き継ぎ、何を再決定するか</b>を決めるのがコピー管理です。"
          "動画の <b>Business Data スライド</b>（支払条件 <code>ZB01</code>／インコタームズ <code>FOB</code> の上書き）は、この設定と対で理解します。",
  img="SPRO → 販売と流通 → 販売 → 販売伝票 → <b>伝票のコピー管理を設定</b>",
  tcode="<code>VTAA</code>（受注 → 受注）／<code>VTFL</code>（受注 → 出荷）／<code>VTFA</code>（受注 → 請求）／<code>VA01</code>（「Create with Reference」で参照コピー）／<code>VL01N</code>・<code>VF01</code>",
  input="""コピー管理の要点（画面で確認する項目）：
  要求伝票タイプ → ターゲット伝票タイプ（例：OR → LF、OR → F2）
  コピーグループ（Header / Item / Schedule line）
  データ転送（Data transfer）
    − ヘッダ／明細のどちらの値を使うか
    − 価格（与力タイプ）を再決定するか、コピーするか
    − 支払条件・インコタームズはヘッダからコピーか、明細から再決定か
  数量／日付のルール（部分数量でのコピー等）""",
  items=[
   "<code>VTFL</code>（受注 → 出荷）を開き、<b>OR → LF</b> のエントリで<b>データ転送の設定</b>（与力の再決定など）を確認する。",
   "<code>VA01</code> の初期画面で「<b>Create with Reference</b>」を使い、<b>既存受注を参照して新しい受注を作る</b>（動画の Business Data スライドの状況を再現）。",
   "参照元と新しい受注で<b>支払条件・インコタームズがどうなったか</b>を比べる（動画のスライドでは明細 20 で <code>ZB01→ZB02</code>／<code>FOB→EXW</code> の上書き例が示されています）。",
   "<code>VA03</code> の<b>伝票フロー</b>で、受注 → 出荷 → 請求の連鎖を確認する（どの伝票からコピーされたかが分かります）。",
  ],
  confirm="① 参照コピーで「何が引き継がれ、何が再決定されたか」を<b>値の差分</b>で示せること。<br>"
          "② 出荷・請求が受注からコピーされる流れを、伝票フローで説明できること。<br>"
          "③ 与力を再決定する設定／コピーする設定の違いを、<code>VTFL</code> の画面で指せること。",
  trap="① <b>参照コピーは「コピー」ではなく「一部再決定」</b>です。古い受注を参照すると<b>古い価格・古い与力日付</b>が入り、想定と違う金額になることがあります。<br>"
       "② 後続伝票がある受注を参照コピーすると、<b>数量の二重計上</b>になり得ます（部分コピーの設定を確認）。",
  work="参照コピーで作った受注と元の受注を並べ、<b>一致した項目／変わった項目</b>を表にしてください（最低 5 項目）。",
 ),
 dict(
  id="c16", no="C16", title="出荷・請求・自動転記（受注の先）",
  tc="VL01N・VL02N・VF01・OBYC・VBFA",
  purpose="受注は<b>出荷と請求に繋がって初めて業務になります</b>。動画は出荷伝票 <code>80007832</code> の<b>照会</b>までを示しています。"
          "ここでは作成側の入口と、在庫・会計への自動転記の所在を押さえます。",
  img="SPRO → 販売と流通 → 出荷（Shipping）／請求（Billing）／自動転記は 財務会計 → <b>自動転記（OBYC）</b>",
  tcode="<code>VL01N</code>／<code>VL02N</code>／<code>VL03N</code>（出荷）・<code>VF01</code>／<code>VF03</code>（請求）・<code>OBYC</code>（自動転記）・<code>VA03</code>（伝票フロー）・<code>MB51</code>／<code>MM03</code>（在庫への影響確認）",
  input="""動画で確認できる値（出荷伝票の照会画面）：
  出荷伝票 80007832  ドキュメント日付 22.11.2000
  出荷先 1000（Becker Berlin）  計画出庫 21.11.2000 / 実出庫 23.11.2000
  明細：10 P-102 26 PC / 20 P-104 39 PC（いずれも ItCa TAN）
  タブ：Item Overview / Picking / Loading / Transport / Status Overview / Goods Movement Data
自システムで作る場合の入口：
  VL01N（受注参照で出荷を作成）→ VL02N（ピッキング数量入力 → 出庫過帳 PGI）→ VF01（請求）""",
  items=[
   "<code>VA03</code> で受注を開き、<b>伝票フロー</b>を確認する（動画では受注から出荷 <code>80007832</code> へ飛べることが示されます）。",
   "<b>出荷を作る</b>：<code>VL01N</code> → 出荷ポイントと納入日を指定 → 受注番号を参照 → 明細と数量を確認 → 保存。",
   "<code>VL02N</code> で<b>ピッキング数量</b>を入れ、<b>出庫過帳（PGI）</b>を実行する。実行後、<b>在庫が減り、売上原価が計上される</b>ことを <code>MB51</code>／<code>MM03</code>／<code>FB03</code> で確認する（自動転記 <code>OBYC</code> の設定による）。",
   "<code>VF01</code> で<b>請求</b>を作成する（受注または出荷を参照）。請求書の<b>正味価額が受注と一致</b>するか確認する。",
   "再度 <code>VA03</code> の伝票フローで<b>受注 → 出荷 → 請求</b>が 1 本に繋がっていることを確認する。",
   "<code>VC/2</code>（Sales Summary）で<b>得意先 <code>1000</code> の Open Sales Order Val／Open Delivery Value／Open Bill. Doc. Val</b> が変化することを見る（動画 <code>25:25</code> 付近と同じ見方）。",
  ],
  confirm="① 伝票フローに<b>受注・出荷・請求の 3 種</b>が並び、数量・金額が整合していること。<br>"
          "② PGI 後に<b>在庫が減る</b>ことを確認したこと（<code>MB51</code> または <code>MM03</code> のプラント在庫）。<br>"
          "③ <code>VC/2</code> の与信・受注残の値が動いたこと（＝情報照会が受注処理と連動していることを実感）。",
  trap="① <b>PGI は戻せません</b>（取消の専用処理 <code>VL09</code> 等が必要）。練習環境でも、まずは<b>照会と作成の分離</b>を意識してください。<br>"
       "② 在庫が無い／与信ブロックが付いていると出荷が作れません。<b>C13（在庫確認）と C14（不完全性）／与信設定</b>を先に確認。<br>"
       "③ 動画は<b>照会まで</b>です。「作成手順は本站が補った内容」であることを意識して読み、必ず自システムの画面で確かめてください。",
  work="受注 1 件を出荷・請求まで流し、<b>伝票フローの番号・数量・金額</b>を記録してください。そのうえで「PGI で何が起きたか」を 3 行で説明してください。",
 ),
]


def build():
    b = []
    a = b.append
    a('<h1>配置手顺（C0〜C16）—— 練習配置</h1>')
    a('''<div class="box info"><b class="t">この頁の使い方と方針</b>
<b>動画が実演している Customizing は C1（<code>VOV8</code>）・C3（<code>OVT0</code>）・C4（<code>OVS9</code>）・C5（SIS レポートビュー）</b>です。それ以外は
「受注処理が成り立つために必要な設定」として、動画の概念スライド（伝票データの 4 つの源泉）と対応させて並べました。<br>
各 STEP は <b>目的 / IMG パス / T-code / 入力値 / 手順 / 確認（自系统） / つまずき / 練習課題</b> の固定構成です。
<b>標準値は環境で異なるので暗記せず</b>、必ず「自系统での確認方法」で自分の環境の値を確かめてください。
練習では <b><code>Z</code> で始まる自分のオブジェクト</b>を作る方針を推奨します（標準を壊さないため）。</div>''')
    a(toc([(c["id"], "%s %s" % (c["no"], _plain(c["title"])[:26])) for c in CONFIG]
          + [("done", "配置完了チェックリスト")]))

    a(h2("配置前的准备", "prep"))
    a('''<p>配置に入る前に 3 つ確認します。<b>① カスタマイジング依頼（Transport Request）を指定できるか</b>、
<b>② <code>SPRO</code> に入れる権限があるか</b>（照会だけでも学習は可能）、<b>③ 練習用の販売エリア・得意先・品目が使えるか</b>（C0）。</p>
<div class="box warn"><b class="t">SD 特有の前提（これを最初に確認する）</b>
① <b>伝票タイプを自分で作れるか</b>：<code>VOV8</code> でコピーすれば標準を壊さずに練習できます（推奨：<code>ZOR1</code>）。
② <b>明細カテゴリの決定を触る勇気</b>：決定テーブル（<code>VOV4</code>）は<b>受注が動かなくなる箇所</b>です。1 行ずつ追加して検証してください。
③ <b>SIS（<code>VC/2</code>）は統計ファイルに依存</b>します。C5 で情報ビューを足しても、統計が未構築なら数字は出ません（構造だけは見えます）。
④ <b>動画は 2007 年頃の R/3</b>です。S/4HANA では Fiori アプリに置き換わった操作があります（<code>VA01</code> →「Sales Order」アプリ等）。<b>画面は違っても、決まり方（決定テーブル・優先順位）は同じ</b>です。</div>''')

    for c in CONFIG:
        a(steph(c["id"], c["no"], c["title"], c["tc"]))
        a(kv([
            ("目的", c["purpose"]),
            ("IMG パス（環境によって呼称が異なる）", c["img"]),
            ("T-code", c["tcode"]),
        ]))
        a('<dl class="kv"><dt>入力値 / 確認対象</dt><dd>%s</dd></dl>' % vals(c["input"]))
        a(steps(c["items"]))
        a(box("info", "確認（自系统での確認方法）", c["confirm"]))
        a(box("warn", "つまずき", c["trap"]))
        a(task(c["work"]))

    a(h2("配置完了チェックリスト", "done"))
    a('''<p>以下がすべて「はい」になれば、受注処理の練習環境は整っています。</p>''')
    a('<ul class="check">\n' + "\n".join("  <li>%s</li>" % x for x in [
        "<code>VA01</code> で <code>OR</code> ＋ 得意先 1000 から概況画面まで進める（C0）",
        "<code>VOV8</code> で伝票タイプ <code>OR</code> の出荷・請求・与信・不完全性の各グループを説明できる（C1）",
        "<code>VOV7</code> で明細カテゴリ <code>TAN</code> の「所要量タイプが空」「与力関連 ON」を確認した（C2）",
        "<code>OVT0</code> で勘定グループの番号範囲・項目ステータス・パートナー決定手順を確認した（C3）",
        "<code>OVS9</code> と <code>OVT0</code> の違い（得意先グループ vs 得意先勘定グループ）を説明できる（C4）",
        "<code>VC/2</code> で情報ビューを切り替え、Last SD documents と与信情報を表示できた（C5）",
        "納入日程行カテゴリの所要量タイプと品目マスタの戦略グループを突き合わせた（C6）",
        "<code>VOV4</code> の「割当」と「決定」の違いを説明できる（C7・C8）",
        "明細カテゴリ決定の 4 キーを暗唱でき、<code>VA03</code> の結果と一致させた（C8）",
        "納入日程行カテゴリ決定から在庫確認まで 1 本の線で説明できる（C9・C13）",
        "出荷プラントの 3 つの優先順位を実測し、<code>VBAP-WERKS</code> で確認した（C10）",
        "得意先マスタのパートナー機能と受注のパートナーを対応づけた（C11）",
        "与力価格の 3 段（手順 → 条件タイプ → 条件レコード）を説明できる（C12）",
        "不完全性チェックの 3 階層を説明し、<code>V.02</code> に不完全な受注を出せた（C14）",
        "参照コピーで一致した項目／変わった項目を示せた（C15）",
        "受注 → 出荷 → 請求を 1 本に繋ぎ、伝票フローで示せた（C16）",
    ]) + '\n</ul>')
    a(box("ok", "次の一歩",
          '設定が終わったら <a href="handson-1.html">练习① 受注登録</a> へ。'
          '配置で分からなくなった箇所は、<a href="concept.html">概念与设计</a> の該当節（とくに 5 節の出荷プラント・6 節の決定链）に戻ると解決が早いです。'))

    return page("config.html", "配置手顺",
                "SAP SD 受注処理の練習配置 C0〜C16：前提確認、伝票タイプ（VOV8）、明細カテゴリ（VOV7）、得意先勘定グループ（OVT0）、"
                "得意先グループ（OVS9）、SIS レポートビュー（Sales Summary/VC/2 の 4 Customizing）、納入日程行カテゴリ（VOV6）、"
                "明細カテゴリ決定（VOV4）、出荷プラントの自動提案（VD51/XD02/MM02）、パートナー決定、与力価格決定（OVKK/VK11）、"
                "在庫確認（OVZ2）、不完全性チェック（OVA2/V.02）、コピー管理（VTAA/VTFL/VTFA）、出荷・請求（VL01N/VF01/OBYC）。",
                "\n".join(b), crumb="配置手顺",
                foot='動画の Customizing（VOV8・OVT0・OVS9・SIS レポートビュー）を中核に、受注処理が動くための設定を C0〜C16 に整理。各 STEP に「自系统での確認方法」つき。',
                foot_next='<a href="handson-1.html">练习① 受注登録（VA01）</a> から、動画と同じ流れを自分の環境で再現します。')


def _plain(s):
    import re
    return re.sub(r"<[^>]+>", "", s)
