# Content Modifier 精确配置值（配合 manual/01 使用）

> 约定：`Constant` = 直接填值；`XPath` / `Expression` = 从输入消息里取。
> Header/Property 占位符语法在**同一 iFlow 后续步骤的任意表达式**中可用：
> `${header.名字}` `${property.名字}` `${in.body}` `${in.header.名字}`
> 注意：Content Modifier 的 *Message Body* 页签里写 `${in.body}` 表示“引用上一个消息体”。

## CM #1（请求前：注入查询参数属性）

| 区域 | 名称 | 类型 | 来源 | 值 |
|---|---|---|---|---|
| Message Properties | maxStock | String | Constant | 15 |
| Message Properties | dateTime | String | Constant | `${date:now:yyyyMMdd_HHmmss}` |
| Message Header | X-Source | String | Constant | training |

## Request Reply（OData / HTTPS GET）

- Resource Path:
  `/Products?$filter=UnitsInStock le ${property.maxStock}&$select=ProductID,ProductName,UnitPrice,UnitsInStock&$format=xml`
- 说明：`${property.maxStock}` 在**适配器连接配置**里也能解析（连接配置属于“表达式可解析”的位置）。

## CM #2（输出前：补 CSV 表头）

| 区域 | 名称 | 值 |
|---|---|---|
| Message Body (Type: Text) | - | `ProductID,ProductName,UnitPrice,UnitsInStock\n${in.body}` |

## 常用占位符速查

| 表达式 | 含义 |
|---|---|
| `${in.body}` | 上一步产出的消息体（文本） |
| `${header.X}` | Header X 的值 |
| `${property.X}` | 消息属性 X 的值 |
| `${exchangeProperty.X}` | Camel exchange 属性（跨子流程较稳定） |
| `${date:now:yyyyMMdd_HHmmss}` | 当前时间，格式自定 |
| `${header.originalMessageId}` | CPI 自动生成的 MPL ID 相关值 |
| `${property.camelError...}` | 异常上下文属性（配合错误处理） |

## Groovy 里读取对应值

```groovy
message.getBody(String.class)      // body
message.getHeader('X-Source')      // header (可能为 null)
message.getProperty('maxStock')    // property
message.setProperty('k', 'v')      // 写 property
message.setHeader('X-Out', 'v')    // 写 header
```
