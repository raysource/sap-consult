# SAP CPI iFlow 训练示例

> 场景：**OData 拉取 → 低库存预警 → CSV 输出**
> 本目录提供：建模手册（照做即可在租户里画出来）、可复用的 Groovy 脚本、输入/输出样例载荷。
> 所有材料均为**学习用途**，非官方交付物；版本以你租户中实际的 Integration Suite 版本为准。

## 目录结构

```
projects/iflow/
├── README.md                    本文件
├── manual/
│   └── 01-build-low-stock-alert.md   端到端建模手册（建议先读）
└── resources/
    ├── script/                  Groovy 脚本（拖入 Script 步骤即可用）
    │   ├── 01-read-and-log.groovy      脚本基础：读 body / header / property
    │   ├── 02-xml-to-csv.groovy        核心：把 OData XML 响应转成 CSV
    │   └── 03-json-transform.groovy    JSON 过滤 + 重组（备用场景）
    ├── payload/
    │   ├── in-odata-products.xml       入站：OData 服务响应（模拟）
    │   └── out-low-stock-products.csv  出站：脚本转换后的 CSV
    └── config/
        └── content-modifier-values.md  三个 Content Modifier 的精确配置值
```

## 一句话流程

```
外部调用(HTTPS) → Content Modifier(注入查询属性)
  → Request Reply(OData: $filter=UnitsInStock le 15, JSON 出参)
  → Script(02-xml-to-csv.groovy: XML→CSV)
  → Content Modifier(写 CSV 头部/时间戳属性)
  → 收件方(HTTP 或 File, 用于演示)
```

想跳过建模直接体验？在 CPI **设计**页手工搭建约 15 分钟，见 `manual/01-build-low-stock-alert.md`。
脚本与载荷都可脱离 iFlow 单独阅读/测试（Groovy 语法与 Java 相近）。
