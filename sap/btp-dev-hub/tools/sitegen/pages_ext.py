# -*- coding: utf-8 -*-
"""页面: RAP / CAP / 示例工程与测试数据"""
from sitegen.helpers import *


def _toc(anchors):
    links = "".join('<a href="#%s">%s</a>' % (a, t) for t, a in anchors)
    return '<div class="toc">%s</div>' % links


# =====================================================================
# RAP
# =====================================================================
def page_rap():
    chunks = []
    chunks.append('<main class="page"><div class="wrap"><article>')
    chunks.append(_toc([("RAP 是什么", "what"), ("开发对象地图", "objects"),
                        ("演示: 三步建 Fiori 应用", "demo"), ("行为与校验实现", "impl"),
                        ("EML 速写", "eml"), ("概念对照表", "terms"), ("下一步", "next")]))

    chunks.append(h2("what", "RAP 是什么"))
    chunks.append(p("<b>ABAP RESTful Application Programming Model (RAP)</b> 是 ABAP Cloud / S/4HANA 扩展栈的"
                    "官方编程模型：把业务建模成 <b>Business Object (BO)</b>，框架自动为你处理持久化、事务、授权、草稿、ETag，"
                    "再以 <b>OData V4</b> 暴露给 Fiori。对比老式 <code>SE80 对话编程 + RFC + Gateway</code>，RAP 的样板代码少一个数量级。"))
    chunks.append(flow_html([("CDS 数据模型", 0), ("行为定义 BDEF", 0), ("行为实现 ABAP 类", 0),
                             ("投影 + 服务定义", 0), ("服务绑定 (OData V4)", 0), ("Fiori elements", 0)]))

    chunks.append(h2("objects", "一张图认清 6 类开发对象"))
    chunks.append("""<table class="tbl"><tr><th>对象(ADT 里的类型)</th><th>作用</th></tr>
<tr><td><b>DDIC 表</b>(如 ztrainingproduct)</td><td>持久化存储(BDEF 的 persistent table)</td></tr>
<tr><td><b>CDS 视图实体</b>(ZI_...)</td><td>接口视图: 定义 BO 的字段与关联、语义注解、访问控制</td></tr>
<tr><td><b>行为定义</b>(BDEF)</td><td>声明 BO 的“行为面”: 允许哪些操作/动作/校验/确定、是否 draft</td></tr>
<tr><td><b>行为实现类</b>(zbp_... / 局部类)</td><td>写动作、校验、确定的 ABAP 实现(EML 与 RAP 回调)</td></tr>
<tr><td><b>投影视图 + 服务定义</b></td><td>为每个消费方“裁剪”BO：只暴露该角色能看的字段/行为</td></tr>
<tr><td><b>服务绑定 + IAM 业务角色</b></td><td>把服务定义绑成 OData V4(UI) 端点并授权</td></tr>
</table>""")
    chunks.append(box("info", "命名约定（云/Steampunk 通用）",
                      "<ul><li>接口视图/行为对象: <code>ZI_*</code>；投影/消费视图: <code>ZC_*</code>；行为实现: <code>zbp_zi_*</code></li>"
                      "<li>表用 <code>z</code> 前缀；全部小写(新语法)；ADT 里用向导生成比手写稳</li></ul>"))

    chunks.append(h2("demo", "演示：一个“培训产品”BO（managed，带草稿）"))
    chunks.append(h3("① 接口视图（数据模型）"))
    chunks.append(pre("abap", """@AccessControl.authorizationCheck: #CHECK
@EndUserText.label: 'Training Product'
define root view entity ZI_TrainingProduct
  as select from ztrainingproduct
{
  key uuid      as Uuid,        // 语义键/技术键(建议 UUID)
      productid as ProductId,
      name      as Name,
      category  as Category,
      price     as Price,
      currency  as Currency,
      stock     as Stock,
      onsale    as OnSale,
      @Semantics.systemDateTime.createdAt: true
      createdat as CreatedAt
}"""))
    chunks.append(h3("② 行为定义 BDEF（managed + draft + 动作/校验/确定）"))
    chunks.append(pre("abap", """managed implementation in class zbp_zi_trainingproduct unique;
strict ( 2 );

define behavior for ZI_TrainingProduct alias Product
persistent table ztrainingproduct
lock master
authorization master ( instance )
etag master LastChangedAt
{
  create; update; delete;

  field ( readonly ) CreatedAt CreatedBy;   // 框架维护字段
  field ( mandatory ) Name Price;           // 必填

  action ( features : instance ) SetOnSale result [1] $self;   // 自定义动作
  validation validatePrice on save { field price; }            // 保存前校验
  determination setDefaults on modify { field category; }      // 创建时自动填充

  draft action Activate; Edit; Resume; Discard;                // draft 生命周期
}"""))
    chunks.append(p("BDEF 一行 <code>managed</code>，等于替你写好了 CREATE/UPDATE/DELETE 的数据库操作与事务——"
                    "这是 RAP 相比 ABAP 传统编程最大的节省。"))

    chunks.append(h3("③ 行为实现（动作 / 校验）"))
    chunks.append(pre("abap", """CLASS zcl_btp_tp_actions DEFINITION PUBLIC FINAL CREATE PUBLIC.
  PUBLIC SECTION.
    INTERFACES if_abap_behv.
ENDCLASS.

CLASS zcl_btp_tp_actions IMPLEMENTATION.
  METHOD if_abap_behv~setonsale.
    MODIFY ENTITIES OF zi_trainingproduct          " 自动套用事务与授权
      ENTITY product
        UPDATE FIELDS ( onsale )
        WITH VALUE #( FOR key IN keys ( %tky  = key-%tky
                                        onsale = abap_true ) )
      FAILED failed
      REPORTED reported.
  ENDMETHOD.

  METHOD if_abap_behv~validateprice.
    READ ENTITIES OF zi_trainingproduct IN LOCAL MODE
      ENTITY product FIELDS ( price currency )
        WITH CORRESPONDING #( keys )
      RESULT DATA(products).

    LOOP AT products INTO DATA(product).
      IF product-price <= 0.
        APPEND VALUE #( %tky = product-%tky ) TO failed-product;
        APPEND VALUE #( %tky = product-%tky
                        %msg = new_message_with_text(
                                 severity = if_abap_behv_message=>severity-error
                                 text     = '价格必须大于 0' ) ) TO reported-product.
      ENDIF.
    ENDLOOP.
  ENDMETHOD.
ENDCLASS.""", "abap"))
    chunks.append(p("（行为实现类在 ADT 里从 BDEF 右键 <b>Generate Behavior Implementation</b> 生成骨架，方法签名由框架决定，"
                    "上方为示意结构。）"))

    chunks.append(h2("impl", "投影 + 服务暴露（每个前端一套视图）"))
    chunks.append(pre("abap", """// 消费投影: 只留 UI 需要的字段, 并写 UI 注解(elements 直接消费)
@AccessControl.authorizationCheck: #CHECK
@UI: { headerInfo: { typeName: '产品', typeNamePlural: '产品',
                     title: { value: 'Name' } } }
define root view entity ZC_TrainingProduct
  provider contract transactional_query
  as projection on ZI_TrainingProduct
{
  key Uuid   as Uuid,
      Name   as Name,
      @UI.lineItem: [ { position: 10, label: '单价' } ]
      Price  as Price,
      @UI.lineItem: [ { position: 20, label: '库存' } ]
      Stock  as Stock
}

// 服务定义: 只暴露这一个投影
define service ZUI_TRAININGPRODUCT_S {
  expose ZC_TrainingProduct as TrainingProduct;
}"""))
    chunks.append(p("最后在 ADT：右键服务定义 → <b>New Service Binding</b> → 类型 <code>OData V4</code>、绑定类型 "
                    "<code>UI</code> → 生成 URL。在 Fiori 里用 <code>/sap/opu/odata4/.../TrainingProduct</code> 即可被 "
                    "Fiori elements List Report 直接消费。"))

    chunks.append(h2("eml", "EML 速写（在任意 ABAP 里操作 BO）"))
    chunks.append(pre("abap", """" 读
READ ENTITIES OF zi_trainingproduct
  ENTITY product FIELDS ( name price )
  WITH VALUE #( ( uuid = '...' ) )
  RESULT DATA(products).

" 改(动作/字段混合, 自动触发校验与确定)
MODIFY ENTITIES OF zi_trainingproduct
  ENTITY product
    UPDATE FIELDS ( price ) WITH VALUE #( ( %tky = products[ 1 ]-%tky
                                            price = 999 ) )
  FAILED failed REPORTED reported.

" 动作
MODIFY ENTITIES OF zi_trainingproduct
  ENTITY product
    EXECUTE setonsale WITH VALUE #( ( %tky = products[ 1 ]-%tky ) )."""))

    chunks.append(h2("terms", "概念对照：RAP ↔ CAP（方便两栈同学互译）"))
    chunks.append("""<table class="tbl"><tr><th>维度</th><th>RAP (ABAP 云)</th><th>CAP (Node/Java)</th></tr>
<tr><td>数据模型</td><td>CDS 视图实体 + DDIC 表</td><td>CDS 实体(自动建表)</td></tr>
<tr><td>行为声明</td><td>BDEF(managed/unmanaged)</td><td>服务定义 + 注解(如 @odata.draft.enabled)</td></tr>
<tr><td>自定义逻辑</td><td>行为实现类(EML)</td><td>事件处理器 (js/@On Java)</td></tr>
<tr><td>多消费方裁剪</td><td>投影视图 + 服务定义</td><td>服务投影 (projection on)</td></tr>
<tr><td>授权</td><td>IAM 角色 + @AccessControl</td><td>@requires / @restrict</td></tr>
<tr><td>运行位置</td><td>S/4HANA 或 ABAP 云 Steampunk</td><td>BTP Cloud Foundry/Kyma</td></tr>
</table>""")

    chunks.append(h2("next", "下一步"))
    chunks.append(cards_html([
        ("CAP：开源侧的“同类产品”", "cap.html", "模型驱动、双运行时(Node/Java)，有可本地跑的完整工程。", ["CAP"]),
        ("Fiori elements 消费", "fiori.html", "注解如何变成 List Report，以及 elements 模板用法。", ["UI5"]),
        ("示例工程", "samples.html", "可直接运行的工程与测试数据。", ["下载"]),
    ]))
    chunks.append('</article></div></main>')
    return {"title": "RAP 开发", "desc": "ABAP RESTful Application Programming Model：CDS+BDEF+行为实现+服务暴露全套样例", "active": "rap",
            "body": hero_html("ABAP Cloud 编程模型", "RAP：把业务对象建模成服务",
                              "CDS 视图 → 行为定义 → 行为实现 → 投影暴露，四步讲完一个现代 ABAP Fiori 应用的诞生。")
            + "".join(chunks)}


# =====================================================================
# CAP
# =====================================================================
def page_cap():
    chunks = []
    chunks.append('<main class="page"><div class="wrap"><article>')
    chunks.append(_toc([("CAP 是什么", "what"), ("Node 还是 Java", "runtime"),
                        ("第一个模型", "model"), ("服务与事件", "service"),
                        ("跑起来(样例工程)", "run"), ("上生产", "prod"), ("下一步", "next")]))

    chunks.append(h2("what", "CAP 是什么"))
    chunks.append(p("<b>Cloud Application Programming Model</b>：SAP 开源(CDS)的应用开发框架，一套声明式 <b>CDS 模型</b>"
                    "同时驱动数据库结构、OData V4 服务、输入校验与 Fiori 注解；Node.js 与 Java 双运行时。"
                    "对开发者：写模型 → 声明服务 → 补业务事件，通用 CRUD 一行代码不用写。"))
    chunks.append(flow_html([("CDS 模型", 0), ("服务投影", 0), ("OData V4 / REST", 0), ("Fiori elements", 0)]))
    chunks.append(p("与 RAP 的关系：RAP 是 ABAP 云侧的同思路实现；CAP 跑在 BTP 应用运行时(CF/Kyma)，模型语言同源(CDS)。"))

    chunks.append(h2("runtime", "Node.js 还是 Java？"))
    chunks.append("""<table class="tbl"><tr><th>维度</th><th>Node.js (@sap/cds)</th><th>Java (CAP Java / Spring)</th></tr>
<tr><td>上手速度</td><td>快：npm 装好即跑</td><td>稍重：Maven/编译/类型生成</td></tr>
<tr><td>类型安全</td><td>JS 弱类型(可配 TS)</td><td>强类型：cds 编译生成 Java 类型(cds.gen)</td></tr>
<tr><td>生态亲和</td><td>前端团队友好</td><td>企业 Java/Spring 团队友好</td></tr>
<tr><td>性能/规模</td><td>足够绝大多数场景</td><td>高并发/重计算更稳</td></tr>
<tr><td>本站示例</td><td>node-cap(已本机实测)</td><td>java-cap(同模型脚手架)</td></tr>
</table>""")

    chunks.append(h2("model", "第一个模型：实体 / 关联 / 通用方面"))
    chunks.append(pre("cds", """namespace sap.training.catalog;
using { cuid, managed, Currency, sap.common.CodeList } from '@sap/cds/common';

// 基础数据: CodeList 提供 name/descr 多语言字段
entity Categories : CodeList {
  key ID      : String(10);
  description : String(200);
}

// 根实体: cuid = UUID 主键; managed = 自动维护 createdAt/createdBy/... 
entity Products : cuid, managed {
  name         : String(120) @title: '产品名称';
  price        : Decimal(9, 2) @title: '单价';
  currency     : Currency default 'CNY';
  stock        : Integer @title: '库存';
  reorderLevel : Integer default 10;
  isActive     : Boolean default true;
  category     : Association to Categories @title: '分类';   // 关联
}"""))
    chunks.append(box("info", "读模型的三条铁律",
                      "<ul><li><b>类型即契约</b>：<code>String(120)</code> 同时约束 DB 列、OData 长度与 UI 输入</li>"
                      "<li><b>关联不落库</b>：Association 是逻辑关系，展开/过滤交给框架生成 JOIN</li>"
                      "<li><b>方面(aspect)复用</b>：<code>cuid / managed / CodeList</code> 是官方预制方面</li></ul>"))

    chunks.append(h2("service", "服务：投影 + 草稿 + 自定义 Action"))
    chunks.append(pre("cds", """using sap.training.catalog as db from '../db/schema';

service CatalogService @(path: '/odata/catalog') {

  // 自定义 Action(服务级 unbound; 带入参/出参 + 授权注解)
  @requires: 'authenticated-user'
  action adjustPrice(productIDs: array of String, deltaPercent: Decimal(5,2))
    returns { updated: Integer };

  @readonly entity Categories as projection on db.Categories;

  entity Products as projection on db.Products;
  // 想要 Fiori 草稿编辑? 给 Products 投影加 @odata.draft.enabled 即可(本示例未开)
}"""))
    chunks.append(p("服务层的<b>投影(projection)</b> = 只把模型的某个“切面”暴露给该消费方——字段裁剪、行为控制都在这一层做。"))
    chunks.append(pre("js", """// 事件处理器: 通用 CRUD 之外才写代码
const cds = require('@sap/cds');
module.exports = cds.service.impl(async function () {

  const { Products } = this.entities;

  // before: 校验(创建/更新前, 返回 400 + 中文错误)
  this.before(['CREATE', 'UPDATE'], Products, async (req) => {
    const rows = Array.isArray(req.data) ? req.data : [req.data];
    for (const row of rows) {
      if (row.price != null && row.price < 0)
        req.reject(400, `价格不能为负数: ${row.name || row.ID}`);
    }
  });

  // after: 读增强(给结果附加字段)
  this.after('READ', Products, (each) => {
    if (each.price != null && each.stock != null)
      each.stockValue = Number((each.price * each.stock).toFixed(2));
  });

  // on: 自定义 Action(事务内批量更新)
  this.on('adjustPrice', async (req) => {
    const tx = cds.tx(req);
    const { productIDs, deltaPercent } = req.data;
    const factor = 1 + deltaPercent / 100;
    const list = await tx.run(SELECT.from(Products).where({ ID: { in: productIDs } }));
    for (const p of list) {
      await tx.run(UPDATE(Products, p.ID).with({ price: Number((p.price * factor).toFixed(2)) }));
    }
    return { updated: list.length };
  });
});"""))

    chunks.append(h2("run", "跑起来（配套工程，10 秒出结果）"))
    chunks.append(pre("bash", """# 工程位置: projects/node-cap  (Node 版) / projects/java-cap (Java 版)
cd projects/node-cap
npm install
npm run deploy       # 建 SQLite 库并灌入 CSV 测试数据
npm start            # http://localhost:4004/odata/catalog/Products

# 立刻验证
curl -s "http://localhost:4004/odata/catalog/Products?\\$top=3&\\$orderby=price%20desc"
curl -s -u alice:alice -X POST "http://localhost:4004/odata/catalog/adjustPrice" \\
  -H "Content-Type: application/json" \\
  -d '{"productIDs":["P-1003","P-1008"],"deltaPercent":10}'   # -> {"updated":2}"""))
    chunks.append(box("ok", "验证状态",
                      "Node.js 版在本机完整跑通：<code>npm install → deploy → start</code> 后 OData 查询 / 创建校验 / 自定义 Action 均返回预期结果（本页所用代码即取自该工程）。"))

    chunks.append(h2("prod", "上生产的换装清单"))
    chunks.append("""<table class="tbl"><tr><th>开发期</th><th>生产(BTP Cloud Foundry)</th></tr>
<tr><td>@cap-js/sqlite(本地)</td><td>@cap-js/hana + SAP HANA Cloud 实例(模型零改动)</td></tr>
<tr><td>mock 用户 / 无认证</td><td>XSUAA + xs-security.json 的角色(对应 @requires)</td></tr>
<tr><td>localhost 直连</td><td>Destination / connectivity 访问后端 S/4</td></tr>
<tr><td>本地 npm start</td><td>cf push / MTA 打包 (cds build --production)</td></tr>
</table>""")
    chunks.append(p("官方脚手架：<code>npx cds init demo --add sample,multitenancy</code> 等模板；文档见 cap.cloud.sap。"))

    chunks.append(h2("next", "下一步"))
    chunks.append(cards_html([
        ("示例工程总入口", "samples.html", "node-cap / java-cap 全部文件、命令与验收清单。", ["工程"]),
        ("Fiori 消费 CAP 服务", "fiori.html", "把 UI5/Fiori elements 接到你刚跑起来的 /odata/catalog。", ["UI5"]),
        ("Integration Suite 集成 CAP", "isuite.html", "用 CPI/Event Mesh 把 CAP 应用接进企业集成。", ["集成"]),
    ]))
    chunks.append('</article></div></main>')
    return {"title": "CAP 开发", "desc": "SAP CAP 开发：CDS 模型/服务/事件处理器，Node.js 与 Java 双运行时与可运行工程", "active": "cap",
            "body": hero_html("Cloud Application Programming Model", "CAP：模型即一切",
                              "一份 CDS 模型同时产出数据库、OData 服务与 UI 注解。看懂四段代码，就能把两个配套工程跑起来。")
            + "".join(chunks)}


# =====================================================================
# 示例工程与测试数据
# =====================================================================
def page_samples():
    chunks = []
    chunks.append('<main class="page"><div class="wrap"><article>')
    chunks.append(_toc([("四个工程", "projects"), ("Node.js CAP", "node"), ("Java CAP", "java"),
                        ("iFlow 素材包", "iflow"), ("Fiori 演示", "fiori"), ("测试数据仓库", "data"),
                        ("怎么改数据", "regenerate")]))

    chunks.append(h2("projects", "工程总览"))
    chunks.append(p("<b>想先看“一个业务怎么从要件定义做到上线”？</b> 请走《<a href='dev-course.html'>开发全流程课件：图书受注管理</a>》"
                    "——那里有 Excel 要件定義書和完整案例实现 <code>projects/book-order-app/</code>。下面按技术栈列出本站全部工程："))
    chunks.append(cards_html([
        ("CAP Node.js 示例", "#node", "OData CRUD + 校验/读增强 + Action + 报表函数 + CSV 种子；本机实测可运行。", ["Node.js", "已验证"]),
        ("CAP Java 示例", "#java", "同一套 CDS 模型的 Java 运行时版本(脚手架级)。", ["Java", "需 JDK21"]),
        ("iFlow 素材包", "#iflow", "端到端建模手册 + Groovy 脚本 + 样例载荷。", ["CPI", "Groovy"]),
        ("Fiori / UI5 演示", "#fiori", "Freestyle 应用: 列表/搜索/排序/交互。", ["UI5"]),
    ]))

    chunks.append(h2("node", "① CAP Node.js：sap-training-catalog（推荐先跑）"))
    chunks.append(pre("text", """projects/node-cap/
├── package.json
├── db/schema.cds              模型: Products / Categories / 统计视图
├── db/data/*.csv              种子数据(10 产品 + 4 分类)
└── srv/
    ├── catalog-service.cds    服务: draft + action adjustPrice
    └── catalog-service.js     事件: 校验 / 读增强 / action"""))
    chunks.append(pre("bash", """cd projects/node-cap
npm install          # Node 18+(本机验证于 Node 22)
npm run deploy       # 建 db.sqlite 并灌 CSV
npm start            # http://localhost:4004
# 验收: $metadata / CRUD / 校验(400 中文报错) / Action / $expand=category
# 详见 node-cap/README.md 的验收命令清单"""))
    chunks.append(box("ok", "本机实测通过",
                      "安装、建库、启动、OData 查询与 Action 调用均验证成功（测试环境 macOS / Node 22；Node 26 因底层 sqlite 原生库尚不支持未能本地跑，工程本身无影响）。"))

    chunks.append(h2("java", "② CAP Java：同一模型的另一种运行时"))
    chunks.append(pre("text", """projects/java-cap/
├── pom.xml                   Spring Boot parent + cds-services-bom
├── package.json              @sap/cds-dk(供 maven npm 目标使用)
├── db/                       与 node 版相同的 schema.cds / data.csv
└── srv/src/main/
    ├── java/com/training/catalog/
    │   ├── Application.java
    │   └── CatalogServiceHandler.java   @On Action(类型化上下文)
    └── resources/application.yaml       SQLite + mock 用户"""))
    chunks.append(pre("bash", """cd projects/java-cap
npx cds deploy --to sqlite:db.sqlite   # 建库+种子
mvn clean spring-boot:run              # http://localhost:8080/odata/catalog
# 带 Basic Auth 调用(admin/admin 或 alice/alice)"""))
    chunks.append(box("warn", "验证状态",
                      "本机无 JDK/Maven，工程<b>未编译验证</b>。结构与官方 cloud-cap-samples-java 一致；"
                      "首次 <code>mvn compile</code> 会生成 cds.gen 类型，若与处理器中的签名有出入，以生成代码为准（README 有对照表）。"))

    chunks.append(h2("iflow", "③ iFlow 素材包（在 CPI 租户里照抄）"))
    chunks.append(pre("text", """projects/iflow/
├── manual/01-build-low-stock-alert.md     9 步建模手册(字段级)
└── resources/
    ├── script/  01-read-and-log / 02-xml-to-csv / 03-json-transform
    ├── payload/ in-odata-products.xml / out-low-stock-products.csv
    └── config/  content-modifier-values.md(三个 CM 精确配置)"""))
    chunks.append(box("warn", "前提",
                      "需要一个可登录的 Integration Suite / CPI 租户(试用版即可)。手册目标 OData 用公开 Northwind V3，"
                      "若租户网络不可达，把 payload 样例当 Mock 响应即可。"))

    chunks.append(h2("fiori", "④ Fiori / UI5 演示（浏览器直开）"))
    chunks.append(pre("text", """projects/fiori/webapp/
├── index.html                 OpenUI5 CDN 引导
├── Component.js / manifest.json
├── view/Products.view.xml + controller/Products.controller.js
└── data/products.json         10 条本地 Mock"""))
    chunks.append(pre("bash", """cd projects/fiori/webapp
python3 -m http.server 8080
# 打开 http://localhost:8080/index.html (需联网拉取 OpenUI5)"""))

    chunks.append(h2("data", "测试数据仓库（data/，CSV 与 JSON 同源）"))
    chunks.append("""<table class="tbl"><tr><th>文件</th><th>内容</th><th>适用场景</th></tr>
<tr><td>data/catalog/products.csv / .json</td><td>26 条产品(中英文名称/价格/币种/库存/补货阈值/分类)</td><td>CAP 种子、OData 演示、报表联调</td></tr>
<tr><td>data/catalog/categories.csv / .json</td><td>4 个分类</td><td>关联/CodeList 演示</td></tr>
<tr><td>data/customers/*</td><td>5 个客户</td><td>主数据类接口演示</td></tr>
<tr><td>data/orders/orders.csv + order_items.csv</td><td>8 张订单 / 19 条明细(共 136 件)</td><td>订单主从、金额计算</td></tr>
<tr><td>data/orders/orders.json</td><td>同数据(嵌套明细)</td><td>JSON 载荷、Mock API</td></tr>
<tr><td>data/orders/orders-odata-response.json</td><td>OData V4 集合响应格式</td><td>前端 Mock 对齐 @odata.context</td></tr>
<tr><td>projects/iflow/resources/payload/*</td><td>OData XML feed / 期望 CSV</td><td>iFlow 脚本离线调试</td></tr>
<tr><td>projects/fiori/webapp/data/products.json</td><td>10 条(UI 友好字段)</td><td>UI5 JSONModel</td></tr>
</table>""")

    chunks.append(h2("regenerate", "数据从哪来 / 怎么改"))
    chunks.append(p("全部业务数据由 <code>tools/make_data.py</code> 单点维护：改里面的 Python 列表 → 重跑 → CSV/JSON 同步刷新，"
                    "保证两格式永远一致。页面由 <code>tools/sitegen/</code> 生成："))
    chunks.append(pre("bash", """cd btp-dev-hub
python3 tools/make_data.py          # 刷新 data/ 下的 csv+json
python3 tools/sitegen/generate.py   # 重新生成全部 html 页面"""))

    chunks.append(box("danger", "免责声明",
                      "本站为学习/培训用途的独立资料站，与 SAP 无隶属关系；示例代码与数据仅供参考，"
                      "不构成任何 SAP 官方支持范围。ABAP/CPI 侧语法随版本演进，落地前请以你的系统与官方文档为准。"))
    chunks.append('</article></div></main>')
    return {"title": "示例工程与测试数据", "desc": "SAP BTP 示例工程与测试数据总入口：CAP Node/Java、Fiori、iFlow 素材与数据集", "active": "samples",
            "body": hero_html("动手区", "示例工程与测试数据",
                              "四个可运行的工程 + 一套同源测试数据(CSV/JSON)。每个工程都标注了验证状态与运行命令。")
            + "".join(chunks)}
