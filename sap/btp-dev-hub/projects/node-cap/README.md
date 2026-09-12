# SAP CAP (Node.js) 训练示例：产品目录服务

一个“麻雀虽小五脏俱全”的 CAP 工程：OData V4 CRUD、自定义 Action、只读报表函数、
校验/读增强事件、CSV 测试数据。**本目录已在本机 (macOS) 验证可运行**。

> 想体验 Fiori 草稿编辑？在 Products 投影上加 `@odata.draft.enabled` 即可（见文末）。

## 目录结构

```
node-cap/
├── package.json               @sap/cds + express; devDeps: @cap-js/sqlite + @sap/cds-dk
├── db/
│   ├── schema.cds             领域模型: Categories / Products / 统计视图
│   └── data/                  CSV 测试数据 (部署时自动灌入)
│       ├── sap.training.catalog-Categories.csv
│       └── sap.training.catalog-Products.csv
└── srv/
    ├── catalog-service.cds    服务: 投影 + action adjustPrice + function productStats
    └── catalog-service.js     事件处理器: before 校验 / after 增强 / on action|function
```

## 运行

```bash
cd projects/node-cap
npm install            # 需要 Node 18+ (本项目验证于 Node 22; Node 26 暂缺原生依赖)
npm run deploy         # 建 db.sqlite 并灌入 CSV
npm start              # http://localhost:4004
```

浏览器打开 http://localhost:4004/ 看欢迎页；OData 服务在 /odata/catalog/。

## 验收命令（每一条都应得到预期结果）

```bash
# 1) 元数据
curl -s "http://localhost:4004/odata/catalog/\$metadata" | head -5

# 2) 列表 + $top/$orderby
curl -s "http://localhost:4004/odata/catalog/Products?\$top=3&\$orderby=price%20desc"

# 3) 关联展开: 每个产品的分类名
curl -s "http://localhost:4004/odata/catalog/Products?\$expand=category&\$top=2"

# 4) 创建(应通过 before 校验)
curl -s -X POST "http://localhost:4004/odata/catalog/Products" \
  -H "Content-Type: application/json" \
  -d '{"name":"测试新品","price":99.90,"currency":"CNY","stock":50,"category_ID":"C-ACC"}'

# 5) 非法创建(价格负数 -> 400 + 中文错误)
curl -s -X POST "http://localhost:4004/odata/catalog/Products" \
  -H "Content-Type: application/json" \
  -d '{"name":"坏数据","price":-1}'

# 6) 自定义 Action(标了 @requires: authenticated-user, 用 mock 用户 alice)
curl -s -u alice:alice -X POST "http://localhost:4004/odata/catalog/adjustPrice" \
  -H "Content-Type: application/json" \
  -d '{"productIDs":["P-1003","P-1008"],"deltaPercent":10}'
# -> {"updated":2} ; 之后查 P-1003 单价应约为 504.90
# 7) 报表函数(聚合视图以 function 暴露, 避免无主键实体上 OData)
curl -s "http://localhost:4004/odata/catalog/productStats()"
```

### 认证说明

本地开发时 cds 默认启用 mock 认证（basic-auth，预置用户 `alice/alice`、`bob/bob`）：
- 匿名请求可以读写 CRUD 实体（无 @requires 保护）；
- 标了 `@requires: 'authenticated-user'` 的 adjustPrice 需带 Basic Auth，匿名会得到 401。

### 想体验草稿(Fiori elements 编辑)？

在 `catalog-service.cds` 的 Products 投影上加一行 `@odata.draft.enabled` 并重新
`npm run deploy` 即可（CAP 会自动建草稿表与 DraftAdministrativeData）。
本地文件库场景下草稿请求会走独立的 draft 语义，建议在需要 Fiori 草稿编辑时再开启。

## 生产形态提示

- 数据库: 开发用 @cap-js/sqlite；上 BTP 换 `@cap-js/hana` + HANA Cloud 实例即可，模型零改动。
- 部署: Cloud Foundry (cf push / MTA) 或 Kyma；官方模板见 `cds init` + `npm run build`。
- 验证/CI: 事件处理器与模型测试可交给 `cds test`（本示例含 test 脚本占位）。
