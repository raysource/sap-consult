# -*- coding: utf-8 -*-
"""页面: 首页 / Integration Suite"""
from sitegen.helpers import *


def _run_block():
    return (box("ok", "本机预览（无需任何安装）",
        p("站内所有页面、代码、数据都是<b>静态文件</b>，三种打开方式任选：") +
        pre("bash", """# 方式 A: Python 自带 HTTP 服务(推荐, 功能最全)
cd btp-dev-hub
python3 -m http.server 8000
# 浏览器打开 http://localhost:8000/

# 方式 B: 直接双击 index.html (file:// 打开也可浏览大部分内容,
#          但浏览器同源策略会限制部分 JS 交互, 代码复制不受影响)

# 方式 C: 已有 VS Code / 任意静态服务器, 指向 btp-dev-hub 目录即可""") +
        p("在“示例工程”页可拿到两个 CAP 工程（Node.js 版<b>已在本机实测运行</b>）、Fiori 应用、iFlow 建模手册与全套测试数据。")))


def page_index():
    inner = []

    inner.append('<div class="wrap"><article>')

    # ---- 三条路径 ----
    inner.append(h2("paths", "三条学习路径（新手建议按路径走）"))
    inner.append(cards_html([
        ("路径 A · 集成与 API",
         "isuite.html",
         "从 Integration Suite 全景开始 → 在 CPI 里亲手搭第一条 iFlow（含可照抄的建模手册与 Groovy 脚本）→ 掌握 MPL 排查。",
         ["Integration Suite", "iFlow", "Groovy"]),
        ("路径 B · 应用开发 (CAP)",
         "cap.html",
         "用 CAP 以“模型驱动”方式开发业务服务：先读模型与事件概念，再把本站的 Node.js / Java 示例工程跑起来，最后用 Fiori/UI5 消费。",
         ["CAP", "Node.js", "Java"]),
        ("路径 C · ABAP 平台 (RAP)",
         "rap.html",
         "在 ABAP 云/Steampunk 上做 Fiori 应用：CDS 数据模型 → 行为定义 → 服务暴露，全程代码样例，理解 Business Object 建模。",
         ["RAP", "CDS", "BDEF"]),
    ]))

    # ---- 六大专题 ----
    inner.append(h2("topics", "专题与案例"))
    inner.append(cards_html([
        ("开发全流程课件：图书受注管理",
         "dev-course.html",
         "用一个真实业务(受注登録/承認/変更)串起 要件定義書(Excel) → 設計 → 開発 → テスト → リリース 全流程，阶段产物全部可打开。",
         ["全流程", "要件定義書", "案例"]),
        ("SAP BTP Integration Suite",
         "isuite.html",
         "套件全家福：Cloud Integration(CPI) / API Management / Event Mesh / Open Connectors… 弄清谁是谁、什么时候用谁。",
         ["全景", "概念图"]),
        ("iFlow 实战 (Cloud Integration)",
         "iflow.html",
         "CPI 的核心姿势：Header vs Property、Content Modifier、Groovy 脚本、Request-Reply、MPL 排查；附可照抄的建模手册。",
         ["适配器", "Groovy", "手册"]),
        ("RAP (ABAP RESTful)",
         "rap.html",
         "Business Object 建模四件套：CDS 视图 + 行为定义 + 实现类 + 服务暴露；managed / draft / 校验动作全套样例。",
         ["ABAP Cloud", "BDEF"]),
        ("CAP (Cloud Application Programming)",
         "cap.html",
         "一套 CDS 模型打穿 DB/OData/UI：投影、关联、草稿、自定义 Action；Node.js 与 Java 两种运行时对比。",
         ["CDS", "OData V4"]),
        ("Fiori / UI5",
         "fiori.html",
         "Freestyle 与 Fiori elements 怎么选；附一个可本地运行的 UI5 演示应用；elements 注解样例。",
         ["UI5", "elements"]),
        ("示例工程与测试数据",
         "samples.html",
         "可下载/可运行的 4 组工程 + 全套测试数据（产品/客户/订单 CSV 与 JSON、iFlow 载荷）。",
         ["Node.js", "Java", "数据"]),
    ]))

    # ---- 上手 ----
    inner.append(h2("start", "两分钟上手"))
    inner.append(_run_block())

    # ---- 站点内容索引 ----
    inner.append(h2("map", "目录速览"))
    inner.append(pre("text", """btp-dev-hub/
├── index.html                  ← 你现在在这里
├── isuite.html / iflow.html / rap.html / cap.html / fiori.html  专题页
├── samples.html                示例工程与测试数据总入口
├── assets/                     样式与交互(无外部依赖, 可离线)
├── data/                       测试数据仓库
│   ├── catalog/   26 条产品 + 4 个分类  (products.csv / products.json 等)
│   ├── customers/ 5 个客户
│   └── orders/    8 张订单(19 条明细, 共 136 件), 含 OData 响应示例
├── projects/                   可运行工程
│   ├── node-cap/   CAP Node.js 示例(本机已验证) + 自带 CSV 种子
│   ├── java-cap/   CAP Java 示例(同模型, 另一套运行时)
│   ├── fiori/      UI5 Freestyle 演示应用(OpenUI5 CDN)
│   └── iflow/      iFlow 建模手册 + Groovy 脚本 + 样例载荷
└── tools/                      生成器(改数据/改页面后用)"""))
    inner.append(box("info", "怎么改这个站",
        p("页面由 <code>tools/sitegen/</code> 下的 Python 模板生成，改完重跑 <code>python3 tools/sitegen/generate.py</code> 即可；"
          "测试数据统一维护在 <code>tools/make_data.py</code>，重跑会同时刷新 CSV 与 JSON。")))

    inner.append('</article></div>')
    return {"title": "首页", "desc": "SAP BTP 开发者训练站：Integration Suite / iFlow / RAP / CAP / Fiori 学习与示例", "active": "index",
            "body": hero_html("免费 · 中文 · 可直接跑起来的样例", "SAP BTP 开发者训练站",
                              "把 Integration Suite / iFlow / RAP / CAP / Fiori 的学习曲线压平：<b>每讲一个概念，旁边就有代码；每个示例，背后都有测试数据</b>。从“这是什么”到“跑起来看效果”，一站走完。")
            + "".join(inner)}


def page_isuite():
    chunks = []
    chunks.append('<main class="page"><div class="wrap"><article>')
    chunks.append(h2("what", "Integration Suite 是什么"))
    chunks.append(p("SAP BTP Integration Suite（前身 SAP Cloud Platform Integration 与 API 产品线的整合）是 SAP 的"
                    "<b>集成平台即服务 (iPaaS)</b>。它不是单个工具，而是围绕“把 SAP 与 SAP / 非 SAP 系统连起来”的一组云服务。"
                    "对开发者，最重要的一条主线是：<b>Cloud Integration（CPI）里画的每一条 iFlow，本质是一条消息处理管线</b>。"))
    chunks.append(flow_html([("应用/系统 A", 0), "协议适配器", "消息管线 (iFlow)", "协议适配器", ("目标系统 B", 0)]))
    chunks.append(p("与本地 PI/PO 的最大区别：<b>免运维、多租户、纯 Web 设计器</b>，集成内容以“包(Package)”为单位做 CI/CD。"))

    chunks.append(h2("services", "套件里的服务（先认识名字，别急着全学）"))
    chunks.append("""<table class="tbl"><tr><th>服务</th><th>一句话</th><th>什么时候用</th></tr>
<tr><td><b>Cloud Integration (CPI)</b></td><td>iFlow 的设计与运行环境，套件的心脏</td><td>文件/API/事件类点对点集成、编排、转换</td></tr>
<tr><td><b>API Management</b></td><td>给 API 加代理、限流、密钥、分析</td><td>把后端(含 CPI 自己)包装成受管 API 对外发布</td></tr>
<tr><td><b>Event Mesh</b></td><td>云上消息总线(兼容 CloudEvents / AMQP)</td><td>系统间异步解耦、事件驱动架构</td></tr>
<tr><td><b>Open Connectors</b></td><td>200+ SaaS 的连接器(Stripe/Salesforce/…)</td><td>快速对接第三方 SaaS，少写代码</td></tr>
<tr><td><b>Trading Partner Management</b></td><td>B2B 伙伴与文档协议管理</td><td>EDI(如 X12/EDIFACT) 场景</td></tr>
<tr><td><b>Integration Advisor</b></td><td>基于 AI/语义的接口与映射推荐</td><td>从遗留接口资产生成映射，省建模时间</td></tr>
</table>""")

    chunks.append(h2("deploy", "落地形态：一套平台，两种“运行图”"))
    chunks.append(p("从部署视角，租户里同时存在两类东西："))
    chunks.append("""<table class="tbl"><tr><th>名称</th><th>是什么</th><th>开发者关心什么</th></tr>
<tr><td><b>Cloud Integration runtime</b></td><td>CPI 自己的运行节点</td><td>iFlow 部署/监控(MPL)、证书与安全物料(Keystore)、连接测试</td></tr>
<tr><td><b>BTP 子账户/空间</b></td><td>云平台本身(CF/Kyma)</td><td>业务应用(CAP/Java/Node)跑在这里，通过 Destination 连回 CPI 或后端</td></tr>
</table>""")
    chunks.append(box("warn", "试用版提醒",
                      p("BTP 试用版(Trial)可免费开通 Integration Suite。试用租户通常<b>无法直接访问公网目标系统</b>"
                        "（需要配置 <code>Cloud Connector</code> 或允许列表），本站 iFlow 样例以公开 OData 为演示目标，如被网络策略拦截，"
                        "按手册提示改用租户可达的端点即可。")))

    chunks.append(h2("concepts", "必须提前搞懂的四组概念"))
    chunks.append("""<table class="tbl"><tr><th>概念</th><th>说明</th></tr>
<tr><td>包 / 工件</td><td>Package 是版本化容器；Artifact = 一条 iFlow、脚本集、值映射等。导出/导入、CI/CD 都以包为单位</td></tr>
<tr><td>适配器 (Adapter)</td><td>Sender/Receiver 与外部世界的“插头”：HTTPS、SFTP、OData、SOAP、Mail、ProcessDirect、JMS…</td></tr>
<tr><td>集成流 (iFlow)</td><td>处理管线的可视化编排：一个发件方 + 若干步骤 + 一个/多个收件方</td></tr>
<tr><td>消息上下文</td><td>一次处理中流动的 body + header + property；<b>header 会出站、property 不出站</b>（详见 iFlow 页）</td></tr>
</table>""")

    chunks.append(h2("next", "下一步：去 iFlow 实战页"))
    chunks.append(cards_html([
        ("iFlow 实战：第一条低库存预警流", "iflow.html",
         "15 分钟手工建模手册 + Groovy 脚本 + 样例载荷，照抄即可在租户里跑通。", ["实战"]),
        ("示例工程与测试数据", "samples.html",
         "4 组工程可直接浏览/运行；测试数据覆盖产品/客户/订单与 iFlow 载荷。", ["下载", "数据"]),
    ]))
    chunks.append('</article></div></main>')

    return {"title": "SAP BTP Integration Suite", "desc": "Integration Suite 全景：CPI/API Management/Event Mesh 服务地图与核心概念", "active": "isuite",
            "body": hero_html("平台全景", "SAP BTP Integration Suite", "认识套件全家福：谁是核心、谁管 API、谁做事件；再落到“我该先学哪条”。")
            + "".join(chunks)}
