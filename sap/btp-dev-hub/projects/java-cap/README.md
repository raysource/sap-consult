# SAP CAP (Java) 训练示例：产品目录服务

与 `../node-cap` 共享**同一套 CDS 模型**（`db/schema.cds`、`srv/catalog-service.cds`、
`db/data/*.csv`），换一套 Java 运行时实现 —— 这正是 CAP 的“模型与运行时解耦”。

## 环境要求

- JDK 21+（SAP 官方推荐 21/25，可用 SapMachine）
- Maven 3.9.14+
- Node.js 18+（构建时需要；cds-maven-plugin 会自行下载，也可用全局 cds-dk 加速）

## 目录结构

```
java-cap/
├── pom.xml                     Maven: spring-boot parent + cds-services-bom
├── package.json                @sap/cds-dk (devDependency, 供 maven 插件 npm install)
├── db/
│   ├── schema.cds              领域模型(与 node-cap 完全一致)
│   └── data/*.csv              测试数据
└── srv/
    ├── catalog-service.cds     服务定义(投影 + draft + action)
    └── src/main/
        ├── java/com/training/catalog/
        │   ├── Application.java              Spring Boot 入口
        │   └── CatalogServiceHandler.java    Action 事件处理器
        └── resources/application.yaml        SQLite + mock 用户
```

## 运行步骤

```bash
cd projects/java-cap

# 1) 建库并灌入 CSV 测试数据 (cds-dk; 若未安装: npm i -g @sap/cds-dk)
npx cds deploy --to sqlite:db.sqlite

# 2) 首次构建: 下载依赖 + 编译 .cds -> 生成 cds.gen 类型 (较慢)
#    之后可直接 mvn spring-boot:run -o (离线)
mvn clean spring-boot:run
```

启动后:

- OData 服务: http://localhost:8080/odata/catalog/
- 元数据:   http://localhost:8080/odata/catalog/$metadata
- 测试数据(需要认证): 用 `admin/admin` 或 `alice/alice` 做 Basic Auth

```bash
# 查询(带 Basic Auth)
curl -u admin:admin "http://localhost:8080/odata/catalog/Products?\$top=5"

# 调用自定义 Action (alice 拥有 authenticated-user 角色即可)
curl -u alice:alice -X POST \
  "http://localhost:8080/odata/catalog/adjustPrice" \
  -H "Content-Type: application/json" \
  -d '{"productIDs": ["P-1003", "P-1008"], "deltaPercent": 10}'
```

> 注意：服务上标注了 `@requires: 'authenticated-user'`，匿名调用会得到 401。

## 常见问题

| 现象 | 处理 |
|---|---|
| `npm` 相关构建失败 | 确保网络可达 npm registry；或先 `npm install` 生成 package-lock 再 `mvn` |
| cds.gen 类报错 | 首次 `mvn compile` 后 target/generated-sources/cds4j 下会生成类型；类名/方法名以生成为准 |
| 端口 8080 被占 | `mvn spring-boot:run -Dspring-boot.run.arguments=--server.port=8081` |
| 没有数据 | 确认已执行第 1 步 `npx cds deploy`；SQLite 文件在项目根目录 db.sqlite |
| 想换内存库 | 把 application.yaml 的 url 改为 `jdbc:sqlite::memory:`，并在启动时自行灌数据 |

## 与 Node 版对照

| 关注点 | Node.js 版 | Java 版 |
|---|---|---|
| 模型文件 | 相同 | 相同(复制) |
| 自定义逻辑 | `srv/catalog-service.js` 事件处理器 | `@On/@Before` 注解 + 类型化上下文 |
| 事务 | `cds.tx(req)` | `PersistenceService` 自动路由事务 |
| Action 参数 | `req.data.productIDs` | 生成的 `AdjustPriceContext` getter |
| 本地开发 | `npm run deploy && npm start` | `npx cds deploy` + `mvn spring-boot:run` |
