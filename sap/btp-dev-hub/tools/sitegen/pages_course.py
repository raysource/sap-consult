# -*- coding: utf-8 -*-
"""页面: 开发全流程课件(图书受注管理案例)"""
from sitegen.helpers import *


def _toc(anchors):
    links = "".join('<a href="#%s">%s</a>' % (a, t) for t, a in anchors)
    return '<div class="toc">%s</div>' % links


def page_devcourse():
    chunks = []
    chunks.append('<main class="page"><div class="wrap"><article>')
    chunks.append(_toc([
        ("案例定位", "case"), ("成果物体系", "deliverables"),
        ("① 要件定義", "req"), ("② 設計", "design"), ("③ 開発", "dev"),
        ("④ テスト", "test"), ("⑤ リリース", "release"), ("延伸阅读", "next")]))

    # ---------------- 案例定位 ----------------
    chunks.append(h2("case", "案例：图书受注管理系统（从要件定義書到可运行代码）"))
    chunks.append(p("本课件用一套 <b>图书受注管理</b> 业务，演示一个 BTP 应用开发项目的完整过程："
                    "<b>要件定義 → 設計 → 開発 → テスト → リリース</b>。业务本身很单纯，正好能看清流程与工程化："))
    chunks.append("""<table class="tbl"><tr><th>角色</th><th>业务职责</th><th>系统中的动作</th></tr>
<tr><td>営業(营业员)</td><td>接单、录入受注、改单</td><td>受注登録(ヘッダ+明細)、変更(OPEN/REJECTED 时)</td></tr>
<tr><td>承認者(审批人)</td><td>核对金额/客户后批准或退回</td><td>approve(承認) / rejectOrder(却下, 必填理由)</td></tr>
<tr><td>管理者</td><td>已承認订单的变更管理</td><td>sendBack(差戻し)→ 修改 → 再承認</td></tr>
</table>""")
    chunks.append(flow_html([("営業: 受注登録", 0), ("OPEN 未承認", 0), ("承認者 approve", 0),
                             ("APPROVED 承認済", 0), ("(変更需要) 管理者 sendBack", 0), ("回到 OPEN", 0)]))
    chunks.append(p("状态机由<b>服务端强制</b>：客户端传什么状态都无效——这正是“业务规则不依赖 UI”的工程实践。"))

    # ---------------- 成果物体系 ----------------
    chunks.append(h2("deliverables", "每个阶段的成果物（全部在本站，可直接打开）"))
    chunks.append("""<table class="tbl"><tr><th>工程阶段</th><th>成果物</th><th>位置</th><th>形态</th></tr>
<tr><td>① 要件定義</td><td>要件定義書（10 个 sheet: 概要/機能/状態遷移/業務フロー/DB項目/API/画面/テスト/非機能/WBS）</td>
<td><a href="course/要件定義書_图书受注管理.xlsx">course/要件定義書_图书受注管理.xlsx</a></td><td>Excel(可改)</td></tr>
<tr><td>② 設計</td><td>DB設計(=CDS 模型) / API設計(=サービス定義) / UI方針(Fiori elements)</td>
<td>projects/book-order-app/db/schema.cds<br>projects/book-order-app/srv/order-service.cds</td><td>CDS(可直接编译)</td></tr>
<tr><td>③ 開発</td><td>CAP Node.js 実装(状態機会/校验/金额计算) + CSV 初期数据</td>
<td>projects/book-order-app/（srv/order-service.js 等）</td><td>可运行</td></tr>
<tr><td>④ テスト</td><td>テストケース + 本机实测输出</td>
<td>projects/book-order-app/docs/test-cases.md<br>projects/book-order-app/README.md</td><td>MD/表格</td></tr>
<tr><td>⑤ リリース/運用</td><td>运行手册 / 部署指引 / 初期データ投入手順</td>
<td>projects/book-order-app/README.md</td><td>MD</td></tr>
</table>""")
    chunks.append(box("info", "怎么用这套课件",
                      p("按 ①→⑤ 顺序读；每一步都先在“成果物”里打开对应文件对照。<b>建议实操</b>：跑起 ③ 的工程，"
                        "然后用 ④ 的用例清单自己点一遍——本页引用的实测结果都是跑出来的真实输出，不是截图。")))

    # ---------------- ① 要件定義 ----------------
    chunks.append(h2("req", "① 要件定義（分析业务，别急着写码）"))
    chunks.append(p("这个阶段不写代码，产出的是<b>能跟业务方达成一致</b>的描述。核心三件事："))
    chunks.append("""<ol class="steps">
<li><b>业务范围与角色</b>：谁在什么情况下做什么（营业登録 / 承認者承認 / 管理者差戻し）——见要件定義書「0_概要」「2_状態遷移」</li>
<li><b>功能与非功能需求</b>：每条需求有编号(F-0100〜F-0700)、输入者、规则、优先级——见「1_機能要件」「8_非機能要件」</li>
<li><b>验收口径</b>：把“什么样算做完”写清楚（状态机矩阵 + 测试用例）——见「2_状態遷移」「7_テストケース」</li>
</ol>""")
    chunks.append(box("ok", "成果物",
                      p("点击下载：<a href='course/要件定義書_图书受注管理.xlsx'><b>要件定義書_图书受注管理.xlsx</b></a>"
                        "（10 个 sheet，已带样例数据，可直接当模板改成你自己的案件）。")))
    chunks.append("""<table class="tbl"><tr><th>sheet</th><th>内容</th><th>sheet</th><th>内容</th></tr>
<tr><td>0_概要</td><td>案件信息/用語/关联资料</td><td>5_API定義</td><td>OData 端点・参数・状态迁移</td></tr>
<tr><td>1_機能要件</td><td>F-0100〜F-0700 编号化需求</td><td>6_画面設計</td><td>Fiori elements 三画面方案</td></tr>
<tr><td>2_状態遷移</td><td>状態定义/迁移表/角色</td><td>7_テストケース</td><td>17 条用例(含异常系)</td></tr>
<tr><td>3_業務フロー</td><td>10 步业务流(登録→承認→変更)</td><td>8_非機能要件</td><td>性能/安全/审计/约束</td></tr>
<tr><td>4_DB項目定義</td><td>4 实体・字段级定义</td><td>9_工程計画</td><td>WBS(要件→リリース)</td></tr>
</table>""")
    chunks.append(box("warn", "要件定義的常见坑",
                      "<ul><li>只写“要什么功能”，不写“谁/什么状态下能用” → 状态机与角色要跟功能同步定</li>"
                      "<li>把 UI 需求写进功能需求 → 画面方案单独成 sheet(6_画面設計)，功能里只写业务规则</li>"
                      "<li>没有验收口径 → 开发完才发现理解不一致；测试用例在要件阶段就起草(7_テストケース)</li></ul>"))

    # ---------------- ② 設計 ----------------
    chunks.append(h2("design", "② 設計（CDS 就是设计文档）"))
    chunks.append(p("本案例选用 CAP。设计阶段把要件翻译成模型与接口：<b>DB項目定義 → db/schema.cds</b>、"
                    "<b>API定義 → srv/order-service.cds</b>。CDS 模型既定义了数据库结构，也定义了 OData 契约——设计稿就是可编译代码。"))
    chunks.append(h3("受注ヘッダ的模型设计（要点）"))
    chunks.append(pre("cds", """entity BookOrders : managed {
  key orderNo    : String(16);   // 业务主键, 服务端採番(SO+日期-4位码)
  orderDate      : Date;
  customer       : Association to Customers;
  status         : String(10) default 'OPEN';   // OPEN/APPROVED/REJECTED
  rejectReason   : String(200);                 // 却下理由(監査)
  approvedBy     : String(40); approvedAt : DateTime;   // 承認監査
  totalAmount    : Decimal(12, 2);              // 由明細重算, 客户端不可写
  items          : Association to many BookOrderItems on items.orderNo = $self.orderNo;
}"""))
    chunks.append(p("三个设计决策值得记住："))
    chunks.append("""<ul>
<li><b>状态与审计字段放在实体里</b>——状态机、审批人、理由都是业务数据，天然支持查询与审计(要件 F-0700)</li>
<li><b>金额一律服务端算</b>——totalAmount/lineTotal 客户端写了也会被服务端重算覆盖</li>
<li><b>書名用“快照列”</b>——明細里冗余保存受注当时的書名，避免マスタ改名后历史单据“变脸”</li>
</ul>""")
    chunks.append(h3("服务接口设计（OData V4）"))
    chunks.append(pre("cds", """service OrderService @(path: '/odata/order') {
  @readonly entity Books      as projection on db.Books;      // マスタ只读
  @readonly entity Customers  as projection on db.Customers;
  entity Orders     as projection on db.BookOrders;           // ヘッダ CRUD
  entity OrderItems as projection on db.BookOrderItems;       // 明細行 CRUD

  @requires: 'authenticated-user'
  action approve(orderNo: String) returns { ok: Boolean; status: String };
  @requires: 'authenticated-user'
  action rejectOrder(orderNo: String, reason: String) returns { ok: Boolean; status: String };
  @requires: 'authenticated-user'
  action sendBack(orderNo: String) returns { ok: Boolean; status: String };
}"""))
    chunks.append(p("对照要件：A-01〜A-11 与这里一一对应；Action 都标了 <code>@requires: 'authenticated-user'</code>"
                    "（要件 NFR-05，本地用 mock 用户 alice/alice 验证）。"))

    # ---------------- ③ 開発 ----------------
    chunks.append(h2("dev", "③ 開発（状态机怎么“焊死”在服务端）"))
    chunks.append(p("工程位置：<code>projects/book-order-app/</code>。文件树："))
    chunks.append(pre("text", """projects/book-order-app/
├── db/schema.cds                  模型(≈DB設計書)
├── db/data/*.csv                  初期データ(書籍10/客户4/示例受注2)
└── srv/
    ├── order-service.cds          服务契约(≈API設計書)
    └── order-service.js           状态机/校验/金额计算(业务规则核心)"""))
    chunks.append(h3("骨架：事件处理器里“只补默认值，规则全在服务端”"))
    chunks.append(pre("js", """// 登録: 服务端採番 + 强制初始状态(客户端传 status/orderNo 一律无效)
row.orderNo  = 'SO' + ymd + '-' + rand;   // ≤16 字符
row.status   = STATUS.OPEN;               // 忽略客户端
row.approvedBy = row.approvedAt = null;   // 审计字段防篡改
row.totalAmount = 0;                      // 明細登録后自动汇总"""))
    chunks.append(h3("承認/却下/差戻し：先查后改，状态不对就 400"))
    chunks.append(pre("js", """this.on('approve', async (req) => {
  const existing = await getOrder(req.data.orderNo);
  if (!existing) return req.reject(404, noOrder(orderNo));
  if (existing.status !== STATUS.OPEN)
    return req.reject(400, `当前状态 ${existing.status}, 只有 OPEN 可承認`);

  await UPDATE(DB_ORDERS).set({
    status: STATUS.APPROVED,
    approvedBy: req.user?.id || 'anonymous',   // 監査: 誰
    approvedAt: new Date().toISOString(),      // 監査: いつ
  }).where({ orderNo });
  return { ok: true, status: STATUS.APPROVED };
});"""))
    chunks.append(h3("修改防线：APPROVED 一律挡在 before 钩子里"))
    chunks.append(pre("js", """this.before('UPDATE', Orders, async (req) => {
  const existing = await getOrder(req.data.orderNo);
  if (!existing) return req.reject(404, noOrder(orderNo));
  if (existing.status === STATUS.APPROVED)
    return req.reject(400, `已承認, 不可直接修改; 请先差戻し(sendBack)`);
  // 客户端想顺带改状态/审计字段? 一律以数据库现值覆盖
  req.data.status = existing.status;
  req.data.approvedBy = existing.approvedBy; req.data.approvedAt = existing.approvedAt;
  req.data.totalAmount = existing.totalAmount;   // 金额只能由行变化重算
});"""))
    chunks.append(p("同一套 before/after 还管着：明細行增删改（自动行号、主数据补齐、行后 <code>recalcTotal</code> 汇总）"
                    "与删除规则（APPROVED 不可删）。完整实现见 <code>srv/order-service.js</code>（约 230 行，含注释）。"))

    chunks.append(h3("跑起来"))
    chunks.append(pre("bash", """cd projects/book-order-app
npm install            # Node 20/22 (Node 26 暂缺 sqlite 原生库)
npm run deploy         # 建 db.sqlite + 灌入 CSV 初期数据
npm start              # http://localhost:4004/odata/order/

# 最小闭环: 登録 → 加行 → 承認
curl -s -X POST "http://localhost:4004/odata/order/Orders" \\
  -H "Content-Type: application/json" -d '{"customer_code":"CUST-001"}'
curl -s -X POST "http://localhost:4004/odata/order/OrderItems" \\
  -H "Content-Type: application/json" -d '{"orderNo":"<上一步返回的orderNo>","book_code":"B001","quantity":5}'
curl -s -u alice:alice -X POST "http://localhost:4004/odata/order/approve" \\
  -H "Content-Type: application/json" -d '{"orderNo":"<orderNo>"}'"""))

    # ---------------- ④ テスト ----------------
    chunks.append(h2("test", "④ テスト（用例先行，跑通才算数）"))
    chunks.append(p("测试用例在要件阶段就起草（要件定義書「7_テストケース」17 条），开发完按 <code>docs/test-cases.md</code> 逐条执行。"
                    "关键结论（2026-09-05 本机实测）："))
    chunks.append("""<table class="tbl"><tr><th>用例</th><th>实测结果</th><th>用例</th><th>实测结果</th></tr>
<tr><td>登録+採番+默认状态</td><td>✓ 201, status=OPEN, 客户端指定状态无效</td><td>承認(审计记录)</td><td>✓ alice + 日時入库</td></tr>
<tr><td>明細マスタ連動</td><td>✓ 単価/書名自动补齐; 折扣単価可用</td><td>承認後改单</td><td>✓ ヘッダ/明細 均 400</td></tr>
<tr><td>合計自動計算</td><td>✓ 行增/改/删后 total 即时重算(704→1040→1280)</td><td>却下</td><td>✓ 无理由 400; 有理由 REJECTED</td></tr>
<tr><td>异常系 400</td><td>✓ 書籍不存在/数量0/空行/重复承認</td><td>差戻し变更流</td><td>✓ APPROVED→OPEN(审计清空)→改→再承認</td></tr>
<tr><td>权限</td><td>✓ 匿名 Action 401; 主数据只读 405</td><td>削除规则</td><td>✓ APPROVED 400, OPEN/REJECTED 204</td></tr>
</table>""")
    chunks.append(box("ok", "完整记录",
                      p("全部命令与逐条输出见 <code>projects/book-order-app/README.md</code>「本机实测输出」一节；"
                        "用例清单见 <code>docs/test-cases.md</code>。回归时照 README 重跑一遍即可。")))

    # ---------------- ⑤ リリース ----------------
    chunks.append(h2("release", "⑤ リリース / 運用（把“能跑”变成“能用”）"))
    chunks.append("""<ol class="steps">
<li><b>环境切换</b>：开发 SQLite → 本番 SAP HANA Cloud（模型零改动，换 @cap-js/hana + 服务绑定）</li>
<li><b>認証強化</b>：mock alice → XSUAA + 角色(営業/承認者/管理者)，Action 的 @requires 换成具体角色</li>
<li><b>デプロイ</b>：CAP 标准打包（cf push / MTA），OData 走 BTP 路由的 HTTPS 入口</li>
<li><b>初期データ</b>：マスタ CSV 按 db/data 的格式随部署导入（正式环境可用 HANA 导入或管理 API）</li>
<li><b>監査・運用</b>：承認/却下记录可查询（要件 F-0700）；日志用 CAP 标准日志；备份交给 HANA Cloud</li>
</ol>""")
    chunks.append(p("v2 候选：Fiori elements 三画面(要件「6_画面設計」，加 UI 注解即可)、Event Mesh 通知审批人、"
                    "在庫連動(受注確定時に引当)、却下通知邮件。"))

    # ---------------- 延伸 ----------------
    chunks.append(h2("next", "延伸阅读"))
    chunks.append(cards_html([
        ("CAP 技术详解", "cap.html", "模型/事件/运行时(Node vs Java)的通用知识，本案例的技术底座。", ["CAP"]),
        ("Fiori elements 消费", "fiori.html", "把要件「6_画面設計」的三画面用注解真正做出来。", ["UI5"]),
        ("RAP 同款案例", "rap.html", "同一套业务(受注/承認/変更)在 ABAP 云上如何建模。", ["RAP"]),
        ("示例工程汇总", "samples.html", "全部工程与测试数据总入口。", ["下载"]),
    ]))
    chunks.append(box("warn", "免责与版本",
                      p("本课件为学习用途：业务与文档是“示范模板”，落地正式案件请按客户环境裁剪；"
                        "状态机语义与 OData 行为随 CAP 版本演进，以你的实际依赖版本为准（本案例验证于 @sap/cds 8.x / Node 22）。")))
    chunks.append('</article></div></main>')
    return {"title": "开发全流程课件", "desc": "图书受注管理开发全过程课件：要件定義書(Excel)→設計→開発→テスト→リリース", "active": "devcourse",
            "body": hero_html("全流程实战案例", "从要件定義書到可运行代码：图书受注管理",
                              "一个业务(受注登録/承認/変更)走完 要件→設計→開発→テスト→リリース 五个阶段，每阶段都有真实成果物可打开、可运行、可验证。")
            + "".join(chunks)}
