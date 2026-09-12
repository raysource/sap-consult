# Fiori / UI5 演示应用（Freestyle）

一个最小但完整的 SAPUI5 **Freestyle** 应用：列表 + 搜索 + 排序 + 行点击交互，
数据来自本地 `webapp/data/products.json`（JSONModel）——无需任何后端即可跑。

```
projects/fiori/webapp/
├── index.html                启动页(引导 OpenUI5 从 CDN 加载)
├── Component.js              应用组件(manifest 驱动)
├── manifest.json             应用描述符: 模型/根视图/库依赖
├── view/Products.view.xml    视图 (XML, 声明式 UI)
├── controller/Products.controller.js   控制器(搜索/排序/点击)
├── model/formatter.js        格式化器示例
└── data/products.json        Mock 数据 (JSONModel)
```

## 本地运行（需要联网加载 OpenUI5 CDN）

```bash
cd projects/fiori/webapp
python3 -m http.server 8080
# 浏览器打开 http://localhost:8080/index.html
```

> 用 `file://` 直接双击 index.html 会因浏览器同源策略读不到 manifest/data，必须走 http 服务。

## 如何换成真实后端（进阶路线）

1. 本机先启动本站的 Node.js CAP 服务（见 `projects/node-cap/README.md`），拿到 OData 端点
   `http://localhost:4004/odata/catalog/`。
2. 安装 `@sap/ux-ui5-tooling` 或直接改用 **Fiori elements 模板**（List Report + Object Page），
   在 BAS / VS Code 用 Fiori Tools 向导：Service Catalog → 指向该 OData 服务 → 生成应用。
3. manifest 里把 `models.products` 换成 ODataModel + dataSource：
   ```json
   "dataSources": {
     "catalogService": {
       "type": "OData",
       "uri": "/odata/catalog/",
       "settings": { "odataVersion": "4.0" }
     }
   }
   ```

## 生产建议

- 用 **Fiori elements**（注解驱动）而非 Freestyle 做标准 CRUD/列表报表，开发量小一个数量级；
  注解在服务端（CAP `annotate` 或 RAP 元数据扩展）维护。
- 本地数据只是教学替身；真实项目一律通过 OData V4 服务 + CSRF/draft 处理。
