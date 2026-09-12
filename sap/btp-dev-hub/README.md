# SAP BTP 开发者训练站 (btp-dev-hub)

面向 SAP BTP 开发者的中文自学资料站：Integration Suite / iFlow / RAP / CAP / Fiori，
每个专题都有**代码样例 + 可运行工程 + 测试数据**。

## 打开方式

```bash
cd btp-dev-hub
python3 -m http.server 8000
# 浏览器打开 http://localhost:8000/
# (或直接双击 index.html)
```

## 站点地图

| 页面 | 内容 |
|---|---|
| index.html | 学习路径 + 专题导航 |
| dev-course.html | 全流程课件：图书受注管理(要件定義書 Excel → 設計 → 開発 → テスト → リリース) |
| isuite.html | Integration Suite 服务地图与核心概念 |
| iflow.html | CPI iFlow 实战：Header/Property、表达式、Groovy、MPL |
| rap.html | ABAP RESTful 建模：CDS + BDEF + 行为实现 + 服务暴露 |
| cap.html | CAP：CDS 模型 / 服务 / 事件，Node 与 Java 对照 |
| fiori.html | UI5 / Fiori elements 选择、注解与演示应用 |
| samples.html | 工程与测试数据总入口（运行命令 + 验证状态） |

## 可运行工程（projects/）

- `book-order-app/` — 全流程课件案例：图书受注管理(受注登録/承認/却下/差戻し/変更)，要件定義書见 `course/`（本机实测通过）
- `node-cap/` — CAP Node.js 示例：OData CRUD + 校验 + Action + 报表函数 + CSV 种子
  （**本机 macOS / Node 22 实测通过**；注意 Node 26 暂缺 sqlite 原生库支持，建议 Node 20/22）
- `java-cap/` — CAP Java 示例（同一套 CDS 模型；需 JDK 21 + Maven，未在本机编译）
- `fiori/webapp/` — SAPUI5 Freestyle 演示应用（OpenUI5 CDN，需联网加载）
- `iflow/` — CPI iFlow 建模手册 + Groovy 脚本 + 样例载荷（需 BTP 试用租户实操）

## 测试数据（data/）

产品(26) / 分类(4) / 客户(5) / 订单(8 张、19 条明细) 的 CSV 与 JSON 同源产出，
另有 OData 响应样例与 iFlow 载荷。统一维护在 `tools/make_data.py`。

## 维护命令

```bash
python3 tools/make_data.py          # 刷新 data/ 下 csv + json
python3 tools/sitegen/generate.py   # 重新生成全部 html
```

## 声明

学习用途的非官方资料站，与 SAP 无隶属关系。代码与数据仅供参考；
落地生产前请以 help.sap.com / cap.cloud.sap 及你实际租户/系统版本为准。
