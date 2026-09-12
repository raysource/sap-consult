# -*- coding: utf-8 -*-
"""index.html — 总览"""
from pg_common import (page, h2, h3, toc, flow, tbl, box, steph, vals, checklist, cards, esc)

HERO = '''
  <div class="kicker">SAP SD · 受注処理（Sales Order Processing）· 動画教材「Unit 14」準拠 · 中文 + 日本語/英語术语对照</div>
  <h1>SAP SD 受注処理 实战训练站</h1>
  <p class="lead">本站是 <b>同目录下录像「录像45 Sales order processing.mp4」（57 分 39 秒）</b> 的配套训练网页。
  原视频是 SAP Education 标准课程 <b>Unit 14: Sales Order Processing</b>（SAP Training System / 客户机 800 / 用户 <code>S000</code>、<code>tscm6-00</code>、状态栏 <code>trn03</code>・<code>OVR</code>），
  由「幻灯片讲义 + SAP GUI 实机演示」交替构成。</p>
  <p class="lead">本站把那段视频拆成 <b>2 条主线</b>：
  <b>① 受注伝票のデータはどこから来るのか</b>（主データ／既存伝票／Customizing／ハードコード）——
  <b>② そのデータを使って受注を登録し、変更し、照会し、出荷・請求へ流す</b>。
  全 11 页：<b>总览 / 概念与设计 / 配置手顺（C0〜C16）/ 练习①〜⑤ / 讲师版 / 学员版 / 能力测试（28 题）</b>。</p>
  <div class="toc">
    <a href="#scope">1. 这个站教什么</a>
    <a href="#video">2. 视频章节对应表</a>
    <a href="#story">3. 训练场景设定</a>
    <a href="#flow">4. 端到端流程</a>
    <a href="#plan">5. 练习安排</a>
    <a href="#objects">6. 设定对象一览 C0〜C16</a>
    <a href="#env">7. 前提与环境</a>
    <a href="#caveat">8. 关于标准值的立场</a>
    <a href="#sources">9. 出典</a>
  </div>'''


def build():
    b = []
    a = b.append

    # ---------------------------------------------------------------- 1
    a(h2("1. 这个站教什么", "scope"))
    a('''<p>受注処理（Sales Order Processing）の中核は <b>「伝票を作る」ことではなく「伝票に入る値を決める仕組みを知る」こと</b>です。
動画の冒頭スライドがこの点を明言しています —— 到達目標は
<b>① Determine the origin of document data from various sources, like the material master, the customer master, or Customizing</b>（伝票データの出所を言える）
と <b>② Find and use the tools and help for entering and processing sales orders</b>（道具とヘルプを使える）、この 2 つです。</p>
<p>したがって本站は、<code>VA01</code> のキー操作の暗記ではなく、次の 3 つを「自分の環境で確かめられる」状態をゴールにします。</p>
<div class="grid cards">
  <div class="card">
    <h3>① 値の出所を言える</h3>
    <p>受注伝票の各項目が <b>主データ（得意先マスタ・品目マスタ・条件）／既存伝票（先行受注）／Customizing（伝票タイプ・決定テーブル）／ハードコード（ABAP）</b>
    のどれから来るのか。とくに <b>出荷プラント</b> と <b>販売エリア</b> は出所が複数あり、優先順位で決まります。</p>
    <div class="tags"><span class="tag gray">概念</span><span class="tag teal">约 60 分</span></div>
  </div>
  <div class="card">
    <h3>② 決まり方を追える</h3>
    <p><b>販売エリアの導出</b>（得意先 → 販売エリア）、<b>明細カテゴリの決定</b>（伝票タイプ × 品目カテゴリグループ × 使用目的）、
    <b>出荷プラントの自動提案</b>（客先品目情報 → 得意先マスタ → 品目マスタ）、<b>与力価格の決定</b>（条件技術）、
    <b>変更時の再決定</b>（何が変わり、何が変わらないか）を、決定链として言えること。</p>
    <div class="tags"><span class="tag gray">概念</span><span class="tag teal">约 90 分</span></div>
  </div>
  <div class="card">
    <h3>③ 実機で証拠を取れる</h3>
    <p>動画のデモを自分の環境で再現し、<code>VA03</code>／<code>XD03</code>／<code>VC/2</code>／<code>SE16N</code> などで
    <b>「なぜその値になったのか」の証拠画面</b>を取れること。各手順には必ず「自系统での確認方法」を付けています。</p>
    <div class="tags"><span class="tag teal">实操</span><span class="tag amber">约 300 分</span></div>
  </div>
  <div class="card">
    <h3>④ 業務の前後ろに繋げられる</h3>
    <p>受注で終わらせず、<b>変更（再決定・ブロック・一括変更）→ 出荷（<code>VL01N</code>・PGI）→ 請求（<code>VF01</code>）→ 情報照会（<code>VC/2</code>）</b>
    まで一本に繋げます。動画が <code>VC/2</code>（Sales Summary）を厚く扱っているのはこのためです。</p>
    <div class="tags"><span class="tag teal">实操</span><span class="tag green">约 120 分</span></div>
  </div>
</div>
<div class="box info"><b class="t">本站与既存站的关系（役割分担）</b>
本站は <b>「受注伝票そのもの」（SD の受注処理）</b>を扱います。生産形態別の実習は既存站が担当します ——
受注生産 <code>../sapmto/</code>（E）／受注設計生産 <code>../sapeto/</code>（Q）／見込生産 <code>../sapmts/</code>／バリアント設定 <code>../sapvc/</code>、
形態の横断比較は <code>../saporderflow/</code>。<b>本站で受注の「読み方」を固めてから、各形態の站へ進む</b>のが最短です。</div>''')

    # ---------------------------------------------------------------- 2
    a(h2("2. 视频章节对应表（录像45 → 本站页面）", "video"))
    a('''<p>57 分の動画を、画面が切り替わった位置で 13 の区間に切り分けました。
<b>左端の時刻は動画内の経過時間</b>です（秒数の目安として使ってください）。
「種別」は <span class="pill op">スライド</span> と <span class="pill pc">GUI 実機</span> の区別で、実機パートには 取引コード を付けています。</p>''')
    a(tbl(["動画の時刻", "種別", "内容（動画の見出し・操作）", "T-code", "対応する本站页面"],
          [
              ['<b>00:00</b>–00:46', '<span class="pill op">スライド</span>', 'Unit 14: Sales Order Processing（本单元の到達目標 2 点）', '—',
               '<a href="index.html#scope">总览 1 節</a>'],
              ['<b>02:17</b>–06:02', '<span class="pill op">スライド</span>', 'Overview: Sources for Document Data（<b>伝票データの 4 つの源泉</b>）', '—',
               '<a href="concept.html#sources">概念 1 節</a>'],
              ['<b>06:03</b>–06:45', '<span class="pill op">スライド</span>', 'Sales Order Entry – Deriving the Sales Area（<b>販売エリアの導出</b>）', '—',
               '<a href="concept.html#area">概念 2 節</a>'],
              ['<b>06:48</b>–09:41', '<span class="pill pc">GUI</span>', 'ログオン（<code>800</code> / <code>S000</code>）→ SAP Easy Access → <code>VA01</code> 初期画面 → 得意先 <code>1000</code> 入力 →「Sales area for customer」選択 → <b>PO Number 必須エラー</b>',
               'VA01', '<a href="handson-1.html">练习①</a>'],
              ['<b>09:55</b>–12:37', '<span class="pill op">スライド</span>', 'Proposing Order Data from Master Data（主データから何が提案されるか：パートナー／与力価格／税／納入日程／支払／出力）', '—',
               '<a href="concept.html#propose">概念 3 節</a>'],
              ['<b>13:01</b>–14:42', '<span class="pill op">スライド</span>', 'Business Partners from the Customer Master（<b>Sold-to / Ship-to / Bill-to / Payer</b>）＋ Proposing Order Data from the Customer Master（役割ごとの提案元）', '—',
               '<a href="concept.html#partner">概念 4 節</a>'],
              ['<b>16:45</b>–19:47', '<span class="pill op">スライド</span>', 'Business Data（<b>ヘッダ vs 明細</b>の支払条件・インコタームズ、参照コピー時の上書き）＋ Item Data（明細 <code>10</code>／<code>TAN</code>／<code>T-ATA30</code>／10 PC）',
               'VA01', '<a href="handson-1.html">练习①</a>'],
              ['<b>19:51</b>–21:35', '<span class="pill op">スライド</span>', 'Proposing Plants Automatically（<b>出荷プラントの自動提案</b>：客先品目情報 → 得意先マスタ → 品目マスタ）', '—',
               '<a href="concept.html#plant">概念 5 節</a>'],
              ['<b>22:45</b>–25:54', '<span class="pill pc">GUI</span>', 'Sales Summary（<code>VC/2</code>）実演：情報ブロック／与信情報／Last SD documents／統計情報 ＋ 出荷伝票 <code>80007832</code> の照会',
               'VC/2, VL03N', '<a href="handson-3.html">练习③</a>'],
              ['<b>25:55</b>–28:29', '<span class="pill pc">GUI</span>', 'SIS レポートビューの Customizing：Maintain Report Views／Views for an Evaluation／Report Views for a User／Last Documents for a Customer',
               'SPRO', '<a href="config.html#c5">C5</a>'],
              ['<b>32:52</b>–38:49', '<span class="pill op">スライド</span>＋<span class="pill pc">GUI</span>', 'Overview: Changing of sales documents（明細一括変更・伝票一括変更・文書一覧からの変更）＋ Blocks（<b>ブロックの階層</b>）＋ Change Plant（プラント変更）',
               'VA02', '<a href="handson-2.html">练习②</a>'],
              ['<b>48:01</b>–51:22', '<span class="pill op">スライド</span>＋<span class="pill pc">GUI</span>', 'Changes to the Sold-to Party in the Sales Document（<b>再決定されるデータ／されないデータ</b>）＋ Customer Change 実演 → <code>XD02</code>（得意先マスタの販売エリアデータ・パートナー機能）',
               'VA02, XD02', '<a href="handson-2.html">练习②</a>'],
              ['<b>51:35</b>–55:12', '<span class="pill pc">GUI</span>', 'Customizing 実演：<code>VOV8</code>（伝票タイプ）／<code>OVS9</code>（得意先グループ）／<code>OVT0</code>（得意先勘定グループ）',
               'VOV8, OVS9, OVT0', '<a href="config.html#c1">C1</a>・<a href="config.html#c3">C3</a>'],
          ]))
    a(box("info", "動画を見る順番（推奨）",
          '① <b>00:00–06:45</b>（概念スライド）→ 本站 <a href="concept.html">概念与设计</a> を読む → '
          '② <b>06:48–21:35</b>（受注登録の実演）→ <a href="handson-1.html">练习①</a> を自分の環境で実施 → '
          '③ <b>22:45–28:29</b>（Sales Summary と Customizing）→ <a href="handson-3.html">练习③</a> → '
          '④ <b>32:52–51:22</b>（変更・ブロック・再決定）→ <a href="handson-2.html">练习②</a> → '
          '⑤ <b>51:35–57:39</b>（Customizing とツール）→ <a href="config.html">配置手顺</a>・<a href="handson-5.html">练习⑤</a>。<br>'
          '<b>注意</b>：動画の後半（38:06–38:48）は講師のパスワード変更画面が入るなど、教材外の操作が混ざります。飛ばして構いません。'))
    a(box("warn", "動画と自システムの違い（先に読む）",
          '動画は <b>2007 年頃の SAP R/3（SAP GUI for Windows・Internet Explorer 表示の Web 教材）</b> です。'
          '本站在此基础上做了三件事：<b>①</b> 画面名・項目名は当時のまま（<code>Create Standard Order: Overview</code> 等）を示しつつ、'
          '<b>S/4HANA では Fiori アプリに置き換わっている操作</b>には注記を付けました（例：<code>VA01</code> →「Sales Order」アプリ）。'
          '<b>②</b> 動画に出てくる T-code のうち、現在も同じ役割で使えるものだけを手順に採用し、'
          '<b>③</b> 数値（得意先 <code>1000</code>・品目 <code>T-ATA30</code>・プラント <code>1200</code> 等）は動画のデモ値をそのまま使っています。'
          '<b>自システムの値が違う場合は、その値で読み替えてください</b>（各手順の「自系统での確認方法」が読み替えの助けになります）。'))

    # ---------------------------------------------------------------- 3
    a(h2("3. 训练场景设定", "story"))
    a('''<p>場景は動画のデモをそのまま使います —— <b>得意先 <code>1000</code>（Becker Berlin）から標準受注（<code>OR</code>）で
品目 <code>T-ATA30</code> を 10 PC 受ける</b>、という一本です。動画の後半では練習用得意先 <code>T-S62130</code>／<code>T-S623A30</code>（Teleko Textilien 系）も登場しますが、
本編と同じ流れなので、<b>どちらか 1 つに統一して練習してください</b>。</p>''')
    a(h3("組織と主データ（本教程で使う値。動画のデモ値）"))
    a(tbl(["区分", "値", "説明"],
          [
              ['システム / クライアント', '<code>SAP Training System</code> / <code>800</code>', '動画のログオン画面。状態バーは <code>trn03</code>（システム）と <code>OVR</code>（ユーザ）'],
              ['ユーザ', '<code>S000</code>（デモ）・<code>tscm6-00</code>（受講者用）', '動画では両方が使われます。<code>SU3</code> で自分のプロファイルを確認'],
              ['販売組織 / 販売チャネル / 部門', '<code>1000</code> / <code>10</code> / <code>00</code>', '<b>販売エリア（Sales Area）</b>。<code>1000</code>=Germany Frankfurt、<code>10</code>=Final customer sales、<code>00</code>=Cross-division'],
              ['得意先（受注先）', '<code>1000</code> Becker Berlin', 'Calvinstrasse 36 / D-13467 Berlin-Hermsdorf（動画のデモ得意先）'],
              ['得意先（練習用）', '<code>T-S62130</code>・<code>T-S623A30</code>', 'Teleko Textilien / Hirschstr. 53 / 55124 Mainz（動画後半のデモ・SAP 教材用得意先）'],
              ['品目（明細 10 / 20）', '<code>T-ATA30</code> / <code>T-ATA29</code>', '説明は “Screen 1”。明細カテゴリ（ItCa）は <code>TAN</code>'],
              ['受注タイプ', '<code>OR</code>（Standard Order）', '動画の初期画面で <code>OR</code> → Standard Order を選択'],
              ['受注数量 / 納入希望日', '<code>10 PC</code> / <code>09.06.2007</code>', '明細画面の Order Quantity と First date'],
              ['与力価格日付 / 正味価額', '<code>02.06.2007</code> / <code>22,990.00 EUR</code>', '明細投入後の Net value（環境により金額は変わります）'],
              ['支払条件 / インコタームズ', '<code>ZB01</code>（14 Days 3%, 30/2%）/ <code>FOB</code>（スライド）・<code>CIF Berlin</code>（実機デモ）', 'Business Data スライドは <code>FOB</code>／<code>EXW</code> の上書き例。<b>実機デモの受注は CIF Berlin</b> で出ます。<b>値は得意先マスタ由来なので環境で必ず変わります</b>'],
              ['出荷プラント', '<code>1200</code>', '品目マスタ「販売組織1」ビューの出荷プラント。<b>自動提案の結果</b>として入ります'],
              ['登録した受注番号', '（各自の採番）', '保存後に <code>VA03</code> で伝票フローを確認します'],
          ]))
    a(box("info", "練習量（業務ストーリー）",
          '得意先 <code>1000</code> から受注タイプ <code>OR</code> で <b>品目 <code>T-ATA30</code> × 10 PC</b>、'
          '納入希望日 <code>09.06.2007</code>、支払条件 <code>ZB01</code>、インコタームズは<b>得意先マスタの値</b>（動画のスライドは <code>FOB</code>、実機デモは <code>CIF Berlin</code>）。<br>'
          'システムは <b>①</b> 得意先 <code>1000</code> から<b>販売エリアとパートナー（SP/BP/PY/SH）</b>を提案 → '
          '<b>②</b> 品目 <code>T-ATA30</code> から<b>明細カテゴリ <code>TAN</code> と出荷プラント <code>1200</code></b> を提案 → '
          '<b>③</b> 条件レコードから<b>与力価格（<code>PR00</code> 等）と税 <code>MWST</code></b> を決定 → '
          '<b>④</b> 保存時に <b>不完全性チェック（Incompletion log）</b>と<b>与信チェック</b>を実行。<br>'
          '後に <b>変更（<code>VA02</code>：プラント変更・得意先変更・一括変更・ブロック）</b>、'
          '<b>出荷（<code>VL01N</code> → ピッキング → PGI）</b>、<b>請求（<code>VF01</code>）</b>、'
          '<b>情報照会（<code>VC/2</code> Sales Summary）</b> へ進みます。'))

    # ---------------------------------------------------------------- 4
    a(h2("4. 端到端流程（练习要跑通的动作）", "flow"))
    a(flow([
        '0 値の出所<br><small>主データ / 既存伝票<br>Customizing</small>',
        '1 VA01 受注登録<br><small>販売エリア導出</small>',
        '2 主データ提案<br><small>パートナー・与力条件</small>',
        '3 明細入力<br><small>TAN / T-ATA30</small>',
        '4 出荷プラント<br><small>自動提案 1200</small>',
        '5 与力価格・ATP<br><small>条件技術</small>',
        '6 保存<br><small>不完全性チェック</small>',
        '7 VA02 変更<br><small>再決定・ブロック</small>',
        '8 VL01N 出荷<br><small>ピッキング → PGI</small>',
        '9 VF01 請求<br><small>伝票フロー</small>',
        '10 VC/2 照会<br><small>Sales Summary</small>',
    ]))
    a('''<p>各段階で<b>「どの値が・どこから・どの優先順位で」決まるか</b>が本站の主题です。
特に <b>段階 4（出荷プラント）</b>と <b>段階 7（変更時の再決定）</b>は、動画が独立したスライドを割いている論点なので、能力测试でも必ず出題します。</p>''')

    # ---------------------------------------------------------------- 5
    a(h2("5. 练习安排（5 个实操）", "plan"))
    a(cards([
        ('<a href="handson-1.html">练习① 受注登録（<code>VA01</code>）</a>',
         '販売エリアの導出 → 得意先からのパートナー／支払条件の提案 → 明細 <code>T-ATA30</code> の入力 → <b>出荷プラント <code>1200</code> の自動提案</b> → 与力価格と税の確認 → 保存。<code>VA03</code> の伝票フローで証拠を取ります。',
         [('实操', ''), ('约 90 分', 'amber')]),
        ('<a href="handson-2.html">练习② 伝票の変更と再決定（<code>VA02</code>）</a>',
         'プラント変更・得意先変更（Customer Change）・明細一括変更・ブロックの設定 → <b>「再決定されるデータ／されないデータ」を自分の目で確認</b>。<code>XD02</code> で得意先マスタとの対応も追います。',
         [('实操', ''), ('约 100 分', 'amber')]),
        ('<a href="handson-3.html">练习③ 販売情報システム（<code>VC/2</code> Sales Summary）</a>',
         '情報ビュー（<code>001</code>〜<code>900</code>）と情報ブロックの読み方、与信情報、Last SD documents、統計情報。<b>動画の Customizing（4 画面）</b>も再現して「レポートが出ない理由」を切り分けます。',
         [('实操', ''), ('约 80 分', 'amber')]),
        ('<a href="handson-4.html">练习④ 出荷と請求（<code>VL01N</code> → <code>VF01</code>）</a>',
         '受注 → 出荷伝票 → ピッキング → PGI → 請求 → 伝票フロー。動画は出荷伝票 <code>80007832</code> の<b>照会</b>までなので、作成側は本站が補います（どこが動画の範囲かを明記）。',
         [('实操', ''), ('约 90 分', 'amber')]),
        ('<a href="handson-5.html">练习⑤ ツール・発展・故障対応</a>',
         '<b>ツールとヘルプ</b>（<code>SU3</code> ユーザプロファイル・パラメータ・お気に入り・<code>VA05</code> 一覧）＋ 発展課題 ＋ <b>故障対照表</b>（価格が出ない／プラントが入らない／明細カテゴリが違う／与信ブロック…）。',
         [('实操', ''), ('约 70 分', 'amber')]),
    ]))

    # ---------------------------------------------------------------- 6
    a(h2("6. 设定对象一览 C0〜C16", "objects"))
    a('''<p>配置手顺页（<a href="config.html">配置手顺</a>）で扱う 17 個の STEP です。
<b>動画が実演している Customizing（<code>VOV8</code>／<code>OVS9</code>／<code>OVT0</code>／SIS レポートビュー）を中核に置き、</b>
受注処理が成立するための前提設定をその前後に並べました。各 STEP には
<b>目的／IMG パス／T-code／入力値／手順／確認（自系统）／つまずき／練習課題</b>を付けています。</p>''')
    a(tbl(["STEP", "内容", "主要 T-code", "ここで何が決まるか"],
          [
              ['C0', '前提与环境确认', '<code>VA01</code>・<code>XD03</code>・<code>MM03</code>', '販売エリア・得意先・品目・与力条件が使えることの確認（ここが崩れると以降が全部崩れます）'],
              ['C1', '<b>伝票タイプ（Sales Order Types）</b>', '<code>VOV8</code>', '受注タイプ <code>OR</code> の性格：明細カテゴリ決定・価格決定手順・与信/納入/請求ブロック・出荷タイプ・即時出荷'],
              ['C2', '明細カテゴリ（Item Categories）', '<code>VOV7</code>', '<code>TAN</code>＝標準明細の性質（価格関連・与力関連・所要量タイプなし＝在庫を持たない）'],
              ['C3', '<b>得意先勘定グループ（Customer Account Groups）</b>', '<code>OVT0</code>', '得意先 <code>0001</code>（Sold-to party）の番号範囲・項目ステータス・パートナー決定手順・出力決定手順'],
              ['C4', '<b>得意先グループ（Customer Groups）</b>', '<code>OVS9</code>', '得意先分類（<code>01</code> Industrial customers 等）＝統計・分析のキー'],
              ['C5', '<b>SIS レポートビュー（Sales Summary の画面設計）</b>', 'SPRO（4 画面）', '情報ビュー <code>001</code>〜<code>900</code> と情報ブロックの並び、ユーザ別の既定ビュー、既存伝票の統計更新'],
              ['C6', '納入日程行カテゴリ（Schedule Line Categories）', '<code>VOV6</code>', '納入日程行ごとの<b>所要量タイプと在庫確認（ATP）</b>の有無'],
              ['C7', '伝票タイプ×明細カテゴリの割当', '<code>VOV4</code>', '<code>OR</code> で使える明細カテゴリの許可（ここに無いカテゴリは受注に入りません）'],
              ['C8', '<b>明細カテゴリ決定</b>（決定テーブル）', '<code>VOV4</code>・<code>VOV7</code>', '伝票タイプ × 品目カテゴリグループ × 品目使用目的 × 高レベル明細カテゴリ → 明細カテゴリ'],
              ['C9', '納入日程行カテゴリ決定', '<code>VOV5</code>', '明細カテゴリ × 所要量タイプ → 納入日程行カテゴリ（AVC/ATP の入口）'],
              ['C10', '<b>出荷プラントの自動提案</b>', '<code>VD51</code>・<code>XD02</code>・<code>MM02</code>', '客先品目情報 → 得意先マスタ（出荷先）→ 品目マスタ（販売組織1）の優先順位で出荷プラントが決まる'],
              ['C11', 'パートナー機能（得意先マスタ側）', '<code>XD02</code>', '<code>SP</code>/<code>BP</code>/<code>PY</code>/<code>SH</code> と、受注へ自動提案されるパートナー'],
              ['C12', '与力価格決定（条件技術）', '<code>OVKK</code>・<code>V/06</code>・<code>V/07</code>・<code>VK11</code>', '条件テーブル・アクセス順序・条件タイプ <code>PR00</code>／税 <code>MWST</code> と価格決定手順'],
              ['C13', '在庫確認（ATP）の設定', '<code>OVZ2</code>・<code>MM02</code>（MRP3）', '伝票タイプ／納入日程行カテゴリ／品目マスタの 3 段で在庫確認の有無が決まる'],
              ['C14', '不完全性チェック（Incompletion）', '<code>OVA2</code>・<code>VUA2</code>・<code>V.02</code>', 'どの項目が必須か（手順・グループ・項目）と、警告かエラーかの挙動'],
              ['C15', 'コピー管理（Copy Control）', '<code>VTAA</code>・<code>VTFA</code>', '受注 → 出荷 → 請求へ値をどう引き継ぐか（流量・与力価格の再決定・データ転送）'],
              ['C16', '出荷・請求タイプと自動転記', '<code>VL01N</code>・<code>VF01</code>・<code>OBYC</code>', '出荷タイプの決定、PGI の在庫・売上原価、請求タイプ <code>F2</code>'],
          ]))
    a(box("warn", "C 番号の読み方",
          '本站の C0〜C16 は<b>本站が整理した学習順の番号</b>であり、動画にこの番号は出てきません。'
          '動画の Customizing 実演は <b>C1（<code>VOV8</code>）・C3（<code>OVT0</code>）・C4（<code>OVS9</code>）・C5（SIS レポートビュー）</b>の 4 つです。'
          '残りは「受注処理が動くために必要な設定」として、動画の概念スライド（データの出所）と対応させて並べたものです。'))

    # ---------------------------------------------------------------- 7
    a(h2("7. 前提与环境", "env"))
    a('''<ul>
<li><b>受注できる状態の得意先</b>：得意先 <code>1000</code>（または <code>T-S62130</code>）に<b>販売エリアビュー</b>（<code>1000/10/00</code>）があり、
<code>XD02</code> の「販売エリアデータ」で与力先・出荷先・支払条件・インコタームズが保守されていること。</li>
<li><b>受注できる状態の品目</b>：品目 <code>T-ATA30</code>（等）が品目タイプ <code>FERT</code> 等で、<b>販売組織1・販売組織2・プラント在庫</b>ビューを持ち、
品目カテゴリグループと<b>出荷プラント</b>が入っていること。</li>
<li><b>与力条件レコード</b>：<code>VK11</code>／<code>VK13</code> で <code>PR00</code>（および税 <code>MWST</code>）が有効日付内にあること。<b>無いと Net value が 0 になります</b>。</li>
<li><b>権限</b>：<code>VA01</code>〜<code>VA03</code>・<code>VL01N</code>・<code>VF01</code>・<code>XD02</code>・<code>VD51</code>・<code>VC/2</code>・<code>SPRO</code>（照会だけでも可）。</li>
<li><b>Customizing を触る場合</b>：カスタマイジング依頼（Transport Request）に入る権限。<b>本站の C 手順は「自分の Z オブジェクトを作る」方式</b>なので、標準を壊さずに練習できます。</li>
</ul>''')
    a(box("danger", "やってはいけないこと",
          '練習用クライアントとはいえ、<b>標準伝票タイプ <code>OR</code> や標準明細カテゴリ <code>TAN</code> を直接書き換えない</b>でください。'
          '設定の効き方を確かめたいときは、<b><code>Z</code> で始まる自分の伝票タイプ／明細カテゴリを作る</b>のが原則です（例：<code>ZOR1</code>、<code>ZTAN</code>）。'
          '本站の配置手顺もその方針で書いています。'))

    # ---------------------------------------------------------------- 8
    a(h2("8. 关于标准值的立场（重要）", "caveat"))
    a('''<p>本站の数値と T-code は、<b>① 動画で実際に画面に出ていた値</b>、<b>② SAP Help／SAP Note 等の一次情報で確認できた値</b>、
<b>③ どちらも取れない場合は「通常は〜。自システムで確認」と書いた記述</b>、の 3 段階で扱いを分けています。</p>
<p>とくに次の点は<b>你的系统里可能不同</b>ので、必ず自システムで確認してください。</p>''')
    a(tbl(["項目", "動画の値", "なぜ違い得るか／どこで確認するか"],
          [
              ['販売エリア', '<code>1000 / 10 / 00</code>', '組織構造は環境ごとに違う。<code>VA01</code> 初期画面の F4、または <code>XD03</code> の販売エリアビューで確認'],
              ['出荷プラント', '<code>1200</code>', '客先品目情報 → 得意先マスタ → 品目マスタの順で決まるため、<b>3 か所すべてを見る</b>（<code>VD53</code>／<code>XD03</code>／<code>MM03</code>）'],
              ['明細カテゴリ', '<code>TAN</code>', '品目カテゴリグループと伝票タイプの決定テーブル次第（<code>VOV4</code>／<code>VOV7</code>）。<code>VA03</code> の明細詳細で確認'],
              ['支払条件', '<code>ZB01</code>', '<b>自社定義</b>の条件です（標準は <code>0001</code> 等）。<code>OBB8</code> で一覧、<code>XD03</code> で得意先の既定値'],
              ['インコタームズ', 'スライド <code>FOB</code>／実機デモ <code>CIF Berlin</code>', '<b>得意先マスタの値が入る</b>ので環境で異なる。<code>XD03</code> で確認するが、この項目は「動画でも 2 通り出ている」典型例'],
              ['受注タイプ', '<code>OR</code>', '標準。<code>VOV8</code> で確認（本站は <code>ZOR1</code> を自作する練習を推奨）'],
              ['納入日程行カテゴリ・所要量タイプ', '（画面には出ない）', '<code>VA03</code> の明細 → 納入日程行、または <code>VOV5</code>／<code>VOV6</code>。<b>標準値は環境で異なるため暗記しない</b>'],
              ['SIS の情報ビュー', '<code>001</code>〜<code>900</code>', '得意先の Customizing。<code>SPRO</code> の 4 画面、または <code>VC/2</code> の「View」ボタンで実際に表示されるものを確認'],
          ]))
    a(box("ok", "本站の検証方針",
          'すべての手順に <b>「自系统での確認方法（T-code ＋ テーブル ＋ 見る画面）」</b> を付けています。'
          '値そのものを覚えるのではなく、<b>「どのテーブルを見れば決まり方が分かるか」</b>を持ち帰ってください。'
          '本站の推算値・画面レイアウトは動画と SAP 標準に基づく<b>再現イメージ</b>であり、実機のスクリーンショットではありません（各図に「画面イメージ」と表示）。'))

    # ---------------------------------------------------------------- 9
    a(h2("9. 出典", "sources"))
    a('''<table class="tbl wide">
<tr><th>種別</th><th>内容</th></tr>
<tr><td><b>主教材（動画）</b></td><td>同ディレクトリの <code>录像45 Sales order processing.mp4</code>（57 分 39 秒）＝ SAP Education <b>Unit 14: Sales Order Processing</b>。講義スライドと SAP GUI 実機デモで構成。<b>本站のシナリオ値・画面名・T-code はこの動画から採取</b>しました。</td></tr>
<tr><td>動画の環境</td><td>SAP Training System / クライアント <code>800</code> / ユーザ <code>S000</code>・<code>tscm6-00</code> / 状態バー <code>trn03</code>・<code>OVR</code> / 2007 年頃の SAP R/3 GUI（Web 教材は Internet Explorer 表示）</td></tr>
<tr><td>SAP 標準（一次情報）</td><td>出荷プラントの決定順序（客先品目情報 → 得意先マスタ → 品目マスタ）と決定場所は SAP Help「Delivering Plants」「Creating Customer-Material Information Records」および SAP Knowledge Base Article <b>2787562</b>（How is the delivering plant determined for sales order items）に基づく。不完全性チェックの T-code（<code>OVA2</code>／<code>VUA2</code>／<code>VUP2</code>／<code>VUE2</code>）と一覧 <code>V.02</code>、テーブル（<code>TVUV</code>・<code>TVUVF</code>・<code>VBUV</code>・<code>VBUP</code>・<code>VBUK</code>）は SAP Help「Log of Incomplete Items」と SD 標準ドキュメントに基づく。</td></tr>
<tr><td>関連サイト</td><td>受注生産 <code>../sapmto/</code>／受注設計生産 <code>../sapeto/</code>／見込生産 <code>../sapmts/</code>／バリアント設定 <code>../sapvc/</code>／形態比較 <code>../saporderflow/</code></td></tr>
</table>''')
    a(box("info", "本站の位置づけ",
          '本站は <b>動画の代替ではありません</b>。動画で「見た」内容を、<b>自分の環境で再現し、証拠を取り、言葉で説明できるようにする</b>ための補助教材です。'
          '動画の該当時刻は <a href="#video">2 節の対応表</a>にまとめてあります。'))

    return page("index.html", "总览",
                "SAP SD 受注処理（Sales Order Processing）实战训练站：以 SAP Education「Unit 14」录像为教材，"
                "讲解伝票データの源泉（主データ/既存伝票/Customizing/ABAP）、販売エリア導出、主データからの提案、"
                "出荷プラント自動決定、明細カテゴリ決定、変更時の再決定、Sales Summary（VC/2）、"
                "並提供 C0〜C16 配置手顺、练习①〜⑤、讲师版、学员版、28 题能力测试。",
                "\n".join(b), hero=HERO,
                foot='動画「录像45 Sales order processing.mp4」準拠。受注処理の「値がどこから来るか」から、変更・出荷・請求・情報照会まで。',
                foot_next='まず <a href="concept.html">概念与设计</a> で「伝票データの 4 つの源泉」を押さえてから、<a href="handson-1.html">练习① 受注登録</a> へ進んでください。')
