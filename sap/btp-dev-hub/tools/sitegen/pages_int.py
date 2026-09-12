# -*- coding: utf-8 -*-
"""页面: iFlow 实战 / Fiori & UI5"""
from sitegen.helpers import *


def _toc(anchors):
    links = "".join('<a href="#%s">%s</a>' % (a, t) for t, a in anchors)
    return '<div class="toc">%s</div>' % links


# =====================================================================
# iFlow 实战
# =====================================================================
def page_iflow():
    chunks = []
    chunks.append('<main class="page"><div class="wrap"><article>')
    chunks.append(_toc([("管线长什么样", "pipeline"), ("Header vs Property", "hvsp"),
                        ("第 1 步 建包建模", "build"), ("常用表达式", "expr"),
                        ("Groovy 三板斧", "groovy"), ("异常与重试", "err"),
                        ("排查: MPL", "mpl"), ("常见坑", "pit"), ("配套文件", "files")]))

    chunks.append(h2("pipeline", "一条 iFlow 长什么样"))
    chunks.append(p("Cloud Integration(CPI)里，集成流 = <b>发件方 + 步骤链 + 收件方</b>。消息一路流过去，"
                    "每一步都能读改写 body，或读写 header / property。本站配套示例是一条“OData 拉取 → 低库存 → CSV”预警流："))
    chunks.append(flow_html(["HTTPS 调用(或 Timer)", "Content Modifier", "Request Reply(OData)",
                             "Script: XML→CSV", "Content Modifier: 补表头", "Receiver(HTTP/Mail)"]))
    chunks.append(p("完整建模手册（逐字段可抄）：<code>projects/iflow/manual/01-build-low-stock-alert.md</code>；"
                    "本页把其中最需要“讲原理”的部分展开。"))

    chunks.append(h2("hvsp", "第一个必须过关的概念：Header vs Property"))
    chunks.append("""<table class="tbl"><tr><th></th><th>Header(报文头)</th><th>Property(消息属性)</th></tr>
<tr><td>作用域</td><td>随消息<b>出站</b>发给外部系统</td><td>只在当前 iFlow 内部流转</td></tr>
<tr><td>典型用途</td><td>HTTP 头、认证信息、Content-Type</td><td>中间计算结果、路由标志、查询参数</td></tr>
<tr><td>表达式读取</td><td><code>${header.名字}</code></td><td><code>${property.名字}</code></td></tr>
<tr><td>Groovy 读取</td><td><code>message.getHeader('x')</code></td><td><code>message.getProperty('x')</code></td></tr>
<tr><td>设置</td><td>Content Modifier / <code>setHeader</code></td><td>Content Modifier / <code>setProperty</code></td></tr>
</table>""")
    chunks.append(box("warn", "新手最常踩的坑",
                      p("把业务中间量(如查询条件)放进 Header，导致它被无脑发给下游外部系统——"
                        "轻则报错，重则把内部字段泄给第三方。<b>内部中间量一律用 Property。</b>")))

    chunks.append(h2("build", "第 1 步：三个 Content Modifier 练手"))
    chunks.append(p("Content Modifier 是 CPI 里最常用的步骤：改 header、改 property、改 body，三种动作一个组件全包。"
                    "以本站样例为例（完整字段表见 <code>projects/iflow/resources/config/content-modifier-values.md</code>）："))
    chunks.append(pre("xml", """<!-- 场景1: 把常量变成 Property(稍后拼进 OData $filter) -->
Message Properties:
  Name: maxStock    Type: String   Source: Constant    Value: 15
  Name: dateTime    Type: String   Source: Constant    Value: ${date:now:yyyyMMdd_HHmmss}

Message Header:
  Name: X-Source    Type: String   Source: Constant    Value: training

<!-- 场景2: 用 XPath 从入站 XML 里抠一个值放进 Header(发给下游) -->
Message Header:
  Name: OrderNo     Source: XPath   Value: //OrderNumber

<!-- 场景3: 改写 body: 引用上一个消息体并补表头 -->
Message Body (Type: Text):
  ProductID,ProductName,UnitPrice,UnitsInStock
  ${in.body}""", "xml"))
    chunks.append(p("关键理解：CM 的 <code>Message Body</code> 页签里 <code>${in.body}</code> 表示<b>引用上一个步骤产出的消息体</b>"
                    "——这正是“补表头 / 套壳 / 拼装”的惯用法。"))

    chunks.append(h2("expr", "常用表达式速查（CM 与适配器配置里通用）"))
    chunks.append("""<table class="tbl"><tr><th>表达式</th><th>含义</th></tr>
<tr><td><code>${in.body}</code></td><td>上一步产出的消息体文本</td></tr>
<tr><td><code>${header.X}</code> / <code>${property.X}</code></td><td>取 header / property 值</td></tr>
<tr><td><code>${date:now:yyyyMMdd_HHmmss}</code></td><td>当前时间(格式 Java SimpleDateFormat)</td></tr>
<tr><td><code>${header.originalMessageId}</code></td><td>消息 ID(排查用)</td></tr>
<tr><td><code>${property.camelError...}</code></td><td>异常子流程里读取错误信息</td></tr>
</table>""")

    chunks.append(h2("groovy", "Groovy 脚本三板斧（Script 步骤直接粘贴）"))
    chunks.append(h3("① 读 body / header / property"))
    chunks.append(pre("groovy", """def Message processData(Message message) {
    // body 当文本读
    String body = message.getBody(String.class)

    // header 与 property(区别见上)
    String src = message.getHeader('X-Source')      // 可能为 null
    String max = message.getProperty('maxStock')

    // 写 property / header
    message.setProperty('trace.maxStock', max ?: 'NOT SET')
    message.setHeader('X-Source', src ?: 'unknown')

    // 打日志(在 MPL 的 Logs 页签可见)
    def log = message.getLog() ?: java.util.logging.Logger.getLogger('iflow')
    return message
}"""))
    chunks.append(h3("② 解析 XML 并转换（XmlSlurper，样例核心）"))
    chunks.append(pre("groovy", """import groovy.xml.XmlSlurper
import java.nio.charset.StandardCharsets

def Message processData(Message message) {
    String body = message.getBody(String.class)
    def xml = new XmlSlurper().parseText(body)

    // Atom/OData 命名空间别名
    def d = new groovy.xml.Namespace('http://schemas.microsoft.com/ado/2007/08/dataservices', 'd')

    StringBuilder csv = new StringBuilder()
    int count = 0
    String maxStock = message.getProperty('maxStock') ?: '15'

    xml.'**'.findAll { it.name() == 'entry' }.each { entry ->
        def p = entry.content.properties
        String stock = p.UnitsInStock.text()?.trim()
        if (stock && (stock as int) > (maxStock as int)) return   // 业务过滤
        csv.append(p.ProductID.text()).append(',').append(p.ProductName.text()).append('\\n')
        count++
    }

    message.setBody(csv.toString(), StandardCharsets.UTF_8.name())
    message.setProperty('csvLineCount', count.toString())
    return message
}"""))
    chunks.append(h3("③ JSON 版本（JsonSlurper，OData JSON / REST 入站用）"))
    chunks.append(pre("groovy", """import groovy.json.*

def Message processData(Message message) {
    def json = new JsonSlurper().parseText(message.getBody(String.class))
    def rows = json.value instanceof List ? json.value : [json.value]  // OData 集合
    def out  = rows.findAll { (it.UnitsInStock as int) <= 15 }
                 .collect { [id: it.ProductID, name: it.ProductName, stock: it.UnitsInStock] }
    message.setBody(JsonOutput.prettyPrint(JsonOutput.toJson(out)), 'UTF-8')
    message.setProperty('filteredCount', out.size().toString())
    return message
}"""))
    chunks.append(box("info", "脚本最佳实践",
                      "<ul><li>签名永远是 <code>def Message processData(Message message)</code></li>"
                      "<li>取到的外部值先判空再用；数字类先 <code>isNumber()</code> 再转型</li>"
                      "<li>日志不要打整包敏感信息；多打 property 少打 body</li>"
                      "<li>脚本里抛异常会直接让消息变 Failed，想优雅失败请看下一节</li></ul>"))

    chunks.append(h2("err", "异常与重试：让 iFlow 优雅地失败"))
    chunks.append("""<table class="tbl"><tr><th>机制</th><th>位置</th><th>用途</th></tr>
<tr><td>Exception Subprocess</td><td>步骤右键可包成子流程</td><td>把“正常流程”和“出错补救”分开画</td></tr>
<tr><td>Escalation / Error End</td><td>子流程边界</td><td>失败时走告警(发邮件/Webhook)或写错误存储</td></tr>
<tr><td>Groovy raise</td><td>脚本内</td><td>业务校验失败主动中断:<code>throw new Exception('价格不合法')</code></td></tr>
<tr><td>Retry(重试)</td><td>Request-Reply 属性</td><td>对瞬时故障(超时/5xx)按次数与间隔重试</td></tr>
</table>""")
    chunks.append(pre("groovy", """// 主动失败 + 带错误上下文(配合 Exception Subprocess 读取)
def Message processData(Message message) {
    String id = message.getProperty('orderId')
    if (id == null) {
        message.setProperty('errorStage', 'validate')
        throw new Exception('orderId 缺失, 终止处理')
    }
    return message
}"""))

    chunks.append(h2("mpl", "排查三板斧：MPL / Trace / 重放"))
    chunks.append("""<ol class="steps">
<li><b>看 MPL</b>：Monitor → Message Processing Log，选一条消息，逐步骤看状态(绿/黄/红)与耗时</li>
<li><b>开 Trace</b>：MPL 详情里对失败步骤看入/出站 payload——80% 的问题在这一步现行(字段名/编码/空值)</li>
<li><b>重放/重试</b>：排障修复后，对失败消息点 Retry 重放；正式环境再配 Alert 通知</li>
</ol>""")

    chunks.append(h2("pit", "常见坑速查"))
    chunks.append("""<table class="tbl"><tr><th>现象</th><th>原因</th><th>处理</th></tr>
<tr><td>端点 404</td><td>Sender Address 与部署后实际端点不一致</td><td>以 Monitor 展示的端点为唯一事实来源</td></tr>
<tr><td>变量 undefined</td><td>Header/Property 拼写或作用域错</td><td>先用日志脚本打印 getHeaders()/getProperties()</td></tr>
<tr><td>中文乱码</td><td>编码不一致</td><td>统一 UTF-8；Receiver 显式 Content-Type charset</td></tr>
<tr><td>OData 401</td><td>认证/证书没配</td><td>先 Postman 单独调通目标，再接 iFlow；生产用 OAuth2ClientCredentials</td></tr>
<tr><td>偶发超时</td><td>目标慢且没重试</td><td>Request-Reply 打开重试 + 增大超时</td></tr>
</table>""")

    chunks.append(h2("files", "配套文件（复制即用）"))
    chunks.append(pre("text", """projects/iflow/
├── manual/01-build-low-stock-alert.md      端到端建模手册(推荐先看)
├── resources/script/
│   ├── 01-read-and-log.groovy              调试三件套: 读/打日志
│   ├── 02-xml-to-csv.groovy                核心: XML feed → CSV
│   └── 03-json-transform.groovy            JSON 备用版
├── resources/payload/
│   ├── in-odata-products.xml               入站响应样例(可当 Mock)
│   └── out-low-stock-products.csv          期望输出
└── resources/config/content-modifier-values.md  三个 CM 的精确配置值"""))
    chunks.append(box("warn", "关于 .iflow 文件",
                      p("iFlow 在 Web UI 里是可视化对象，导出为 .iflow XML 依赖当前租户的 schema 版本；"
                        "与其给一份“大概率导入失败”的旧 XML，本站给出<b>可照抄的建模手册</b>——在租户里 15 分钟能画出等价流程，且一定与你的版本匹配。")))

    chunks.append('</article></div></main>')
    return {"title": "iFlow 实战", "desc": "SAP CPI iFlow 实战：Header/Property、Content Modifier、Groovy、MPL 排查与可抄手册", "active": "iflow",
            "body": hero_html("Cloud Integration 实战", "iFlow：从画布到会排查",
                              "概念 + 表达式 + Groovy + 手册四件套。看完本页，你能独立在 CPI 里搭一条能跑、能查、能改的集成流。")
            + "".join(chunks)}


# =====================================================================
# Fiori / UI5
# =====================================================================
def page_fiori():
    chunks = []
    chunks.append('<main class="page"><div class="wrap"><article>')
    chunks.append(_toc([("UI5/Fiori/elements 关系", "what"), ("怎么选", "choose"),
                        ("可运行示例", "demo"), ("对接真实服务", "odata"),
                        ("elements 注解长啥样", "annot"), ("从零建应用", "scaffold"), ("下一步", "next")]))

    chunks.append(h2("what", "先分清三个词"))
    chunks.append("""<table class="tbl"><tr><th>词</th><th>是什么</th></tr>
<tr><td><b>SAPUI5 / OpenUI5</b></td><td>UI 技术框架(控件库 + 数据绑定 + 路由)。SAPUI5 是 SAP 发行版，OpenUI5 是开源版</td></tr>
<tr><td><b>SAP Fiori</b></td><td>体验规范(设计语言 + 启动台 FLP + 应用类型)。Fiori 应用 = 符合规范的 UI5 应用</td></tr>
<tr><td><b>Fiori elements</b></td><td>“配置即应用”：只写注解，框架自动生成 List Report / Object Page 等页面模板</td></tr>
</table>""")
    chunks.append(flow_html([("浏览器 UI5 控件", 0), ("OData V4 模型", 0),
                             ("服务 (CAP / RAP / S4 网关)", 0), ("数据库", 0)]))
    chunks.append(p("现代 SAP 开发的默认姿势：<b>后端用 CAP 或 RAP 把业务建模成 OData V4 服务，前端用 Fiori elements 消费</b>"
                    "——两端都用“声明式”，UI 注解甚至可以写在服务端 CDS 里。"))

    chunks.append(h2("choose", "Freestyle 还是 Fiori elements？"))
    chunks.append("""<table class="tbl"><tr><th>场景</th><th>推荐</th><th>理由</th></tr>
<tr><td>标准 CRUD / 列表报表 / 主从</td><td><b>Fiori elements</b></td><td>写注解不写页面，模板自带搜索/过滤/分页/草稿</td></tr>
<tr><td>强定制交互/可视化大屏</td><td><b>Freestyle</b></td><td>页面自由，控件任选</td></tr>
<tr><td>混合</td><td>elements + 自定义扩展</td><td>用 element 模板做 80%，Controller 扩展做 20%</td></tr>
</table>""")

    chunks.append(h2("demo", "本站配套：一个能本地跑的 Freestyle 示例"))
    chunks.append(p("<code>projects/fiori/</code> 是一个完整 UI5 应用（manifest + XML 视图 + 控制器 + JSONModel 数据），"
                    "含列表/搜索/排序/行点击四个交互。运行："))
    chunks.append(pre("bash", """cd btp-dev-hub/projects/fiori/webapp
python3 -m http.server 8080
# 浏览器打开 http://localhost:8080/index.html  (需联网加载 OpenUI5 CDN)"""))
    chunks.append(pre("text", """projects/fiori/webapp/
├── index.html               引导: 加载 OpenUI5 + 指定 resourceroot
├── Component.js             UIComponent(manifest 驱动)
├── manifest.json            应用描述符: 根视图/模型/库依赖
├── view/Products.view.xml   XML 视图: 工具栏 + ObjectListItem 列表
├── controller/Products.controller.js   搜索/排序/点击
├── model/formatter.js       格式化器示例
└── data/products.json       JSONModel 测试数据"""))
    chunks.append(p("视图里“值随库存变红”的写法，是 UI5 表达式绑定的典型用法："))
    chunks.append(pre("xml", """<ObjectListItem
    type="Active"
    title="{products>name}"
    number="{parts: [{path: 'products>price'}, {path: 'products>currency'}],
            type: 'sap.ui.model.type.Currency'}"
    numberState="{= ${products>stock} &lt;= ${products>reorderLevel} ? 'Error' : 'Success' }">
    <firstStatus>
        <ObjectStatus text="库存 {products>stock}"
                      state="{= ${products>stock} &lt;= ${products>reorderLevel} ? 'Error' : 'None' }"/>
    </firstStatus>
</ObjectListItem>"""))
    chunks.append(p("搜索 = 给列表的 binding 加 Filter；排序 = 换 Sorter。完整实现见示例控制器。"))

    chunks.append(h2("odata", "从本地 JSON 换到真实 OData（生产形态）"))
    chunks.append(pre("json", """// manifest.json: 把 JSONModel 换成 ODataModel
"dataSources": {
  "catalogService": {
    "type": "OData",
    "uri": "/odata/catalog/",                  // 指向 CAP/RAP 服务
    "settings": { "odataVersion": "4.0" }
  }
},
"models": {
  "": { "dataSource": "catalogService" }       // 默认模型 = 该服务
}"""))
    chunks.append(box("ok", "零成本试真服务",
                      p("先跑本站 <code>projects/node-cap</code>（CAP Node.js 服务，本机已验证），就能拿到一个"
                        "OData V4 端点 <code>/odata/catalog/</code>；把下面 dataSource 指向它，再刷新 UI5 页面，"
                        "列表就会变成真后端数据。")))

    chunks.append(h2("annot", "Fiori elements：注解长什么样"))
    chunks.append(p("elements 消费的是服务 metadata 里的 <b>UI 注解</b>。CAP 里直接在 CDS 写注解即可，运行时自动进入 metadata："))
    chunks.append(pre("cds", """// 在服务定义处 annotate(推荐做法: 与模型同源)
annotate CatalogService.Products with {
  @title            : '产品'
  @UI.SelectionFields: [name, category_ID];   // 列表页顶部过滤字段
  @UI.LineItem       : [
    { $Type : 'UI.DataField', Value : name,        Label : '产品名称' },
    { $Type : 'UI.DataField', Value : category.name, Label : '分类' },
    { $Type : 'UI.DataField', Value : price,       Label : '单价' },
    { $Type : 'UI.DataField', Value : stock,       Label : '库存' }
  ];                                            // List Report 的列
  @UI.HeaderInfo      : { TypeName : '产品', TypeNamePlural : '产品' };
}"""))
    chunks.append(p("同一套注解数据流到 RAP 侧时，通常写在 ABAP 的<b>元数据扩展</b>或投影视图里（语法同为 CDS 注解，见 RAP 页）。"
                    "生成后的服务 metadata($metadata)里就是等效的 OData V4 注解 XML。"))

    chunks.append(h2("scaffold", "从零建一个 Fiori elements 应用"))
    chunks.append("""<ol class="steps">
<li>在 BAS / VS Code 打开 Fiori 项目：菜单 <b>Fiori: Open Application Generator</b></li>
<li>模板选 <b>List Report Object Page</b>；Data Source 指向你的 OData V4 服务(或本机 node-cap 的 /odata/catalog/)</li>
<li>指定主实体(Products)与导航实体(Categories) → 生成即得到一个可运行的 elements 应用</li>
<li>运行: 应用内 <b>Run Configurations → Start</b>(自动起 UI5 并代理服务)</li>
<li>缺列/缺字段? 别改前端, 回服务端补注解后刷新 metadata</li>
</ol>""")

    chunks.append(h2("next", "下一步"))
    chunks.append(cards_html([
        ("CAP：把后端建起来", "cap.html", "模型 → 服务 → 注解，CAP 页含两种运行时与全套样例。", ["后端"]),
        ("RAP：ABAP 侧的同类能力", "rap.html", "CDS 视图 + 行为定义 + 元数据扩展，ABAP 云上建模。", ["ABAP"]),
        ("示例工程与测试数据", "samples.html", "Fiori 应用文件、CAP 工程与数据集总入口。", ["下载"]),
    ]))
    chunks.append('</article></div></main>')
    return {"title": "Fiori / UI5", "desc": "Fiori / UI5 开发：elements vs Freestyle、可运行示例、OData 对接与注解", "active": "fiori",
            "body": hero_html("体验层开发", "Fiori / UI5：少写页面，多写注解",
                              "讲清 UI5 / Fiori / Fiori elements 的关系，给一个能本地跑的示例，再教你把页面接到 CAP / RAP 服务上。")
            + "".join(chunks)}
