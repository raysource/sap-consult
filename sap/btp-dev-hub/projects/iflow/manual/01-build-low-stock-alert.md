# 端到端建模手册：OData → 低库存预警 CSV

目标读者：第一次在 SAP BTP Integration Suite / Cloud Integration（CPI）里手工搭一个 iFlow。
全程在 **Web UI** 完成，不需要代码 IDE。照抄每一步，完成后用 curl 触发即可看到输出。

适用租户：SAP BTP 试用版（Integration Suite）或正式版 Cloud Integration 的 **Design → Integration Packages**。

---

## 第 1 步 建包 (Integration Package)

1. 登录 CPI Web UI → 左侧 **Design** → **Integrations**（或 Monitor 旁的设计区）。
2. **Create** → Integration Package，名称：`Training Low Stock Alert`，ID：`training.lowstock.alert`。
3. 打开包 → **Artifacts** 页签 → **Add** → **Integration Flow**。
   - 名称：`OData Low Stock to CSV`
   - ID：`odata_lowstock_to_csv`
   - 类型：**P2M (Process Directly)** 的 HTTPS 主动型即可；模板选 **SAP Help 里的 “HTTPS sender”** 也行。
4. 打开该 iFlow 进入画布（Integration Flow Editor）。

> 术语：**Integration Package（包）** 是资产容器；**Artifact（工件）** = 一条 iFlow / Value Mapping / 脚本集合；
> **Sender/Receiver** 通过**适配器(Adapter)** 与外部系统通信。iFlow 中圆角小图标是**步骤(Step)**。

## 第 2 步 发件方 Sender（HTTPS，手动触发）

画布左侧 **Sender** 拖入 → 点开齿轮：

| 页签 | 字段 | 值 |
|---|---|---|
| General | Address | `/trigger/lowstock` |
| Connection | Protocol | HTTPS |
| Connection | Authentication | No Authentication（学习用；生产必配 OAuth/证书） |
| Message | Message Type | XML |

> 这样部署后会得到形如
> `https://<tenant>.it-cpi001.cfapps.<region>.hana.ondemand.com/http/trigger/lowstock`
> 的端点，之后用 curl/Postman POST 触发（Payload 随意，流程不消费它）。

## 第 3 步 Content Modifier #1（把入参变成查询属性）

拖入 **Content Modifier**，双击 → 三个页签分别填：

- **Message Header**：不加（演示 Header 用法时再加：Name=`X-Source`，Source Type=`Constant`，Value=`training`）。
- **Message Properties**：

| Name | Type | Source Type | Value |
|---|---|---|---|
| `maxStock` | 常量 | Constant | `15` |
| `dateTime` | 常量 | Constant | `${date:now:yyyyMMdd_HHmmss}` |

> 提示：Property 只活在当前消息上下文（可用于后面脚本/表达式），**不会**发给外部收件方；
> Header 会随出站请求发送。这是 CPI 新手最容易混的两个概念。

## 第 4 步 Request Reply（OData 出站调用）

1. **External Call** → 拖入 **Request Reply**，拉到 Content Modifier 之后，连出 **Receiver**。
2. Receiver 适配器：选择 **HTTPS**（省事）或 **OData**（语义更完整，可导入 EDMX）。
   示例端点用公开的 Northwind **V3** OData（返回的 XML 是 `<feed><entry><m:properties>` wrapper 结构，
   与 `02-xml-to-csv.groovy` 的解析逻辑一致）：
   `https://services.odata.org/V3/OData/OData.svc/Products`
3. Request Reply 的 HTTP 配置：
   - Resource Path：`/Products?$filter=UnitsInStock le ${property.maxStock}&$select=ProductID,ProductName,UnitPrice,UnitsInStock&$format=xml`
   - Method：`GET`
   - 若想演示 **OData 适配器**：Connection 页填 Service URL（去掉末尾的 `/Products`），Resource Path 填相对路径同上。

> 若你的租户网络访问不了 `services.odata.org`，把 `resources/payload/in-odata-products.xml` 当响应体、
> 配一个本地 Mock 服务，或改用公司内部 OData；只要 XML 结构（feed/entry/m:properties）一致即可。
> 若目标返回 **JSON**，把 Resource Path 的 `$format=xml` 去掉，并把第 6 步脚本换成 `03-json-transform.groovy`。

## 第 5 步 写日志（可选但强烈建议）

放一个 **Script** 步骤，粘贴 `resources/script/01-read-and-log.groovy` 内容。
作用：把 body / header / property 打日志，方便看每一步的输入。调通后可删除。

## 第 6 步 Script：XML → CSV

再放一个 **Script** 步骤，粘贴 `resources/script/02-xml-to-csv.groovy`。
逻辑：`XmlSlurper` 解析 feed → 遍历 `<d:Product>` → 组 CSV 行 → 设成新 body，并把总行数写进 property `csvLineCount`。

## 第 7 步 Content Modifier #2（给 CSV 加“外壳”）

- **Message Header**：不加。
- **Message Properties**：不加。
- **Message Body**（Type=`Text`）：
  ```
  ProductID,ProductName,UnitPrice,UnitsInStock
  ${in.body}
  ```
> 上一步脚本输出的是“数据行”，这一步用 `${in.body}` 引用前一消息体并补表头。若脚本里已含表头可跳过本步。

## 第 8 步 收件方 Receiver

- 简单演示：Receiver 用 **HTTPS**，指向 Webhook.site 或本地测试端点 → 部署后触发，浏览器/Webhook 面板里直接看到 CSV。
- 或演示 **Mail** 收件：Receiver 选 Mail，把 `csvLineCount` 用进主题（如 `Low stock alert - ${property.csvLineCount} items`）。

## 第 9 步 保存、部署、触发

1. 右上角 **Save** → **Deploy**（等状态变 Started）。
2. 触发（地址见第 2 步）：
   ```bash
   curl -X POST "https://<你的端点>/http/trigger/lowstock" \
        -H "Content-Type: application/xml" -d "<order/>" -v
   ```
3. 观察结果：
   - **Monitor → Manage Integration Content**：iFlow Started 状态、`Message Processing Log`（MPL）看执行轨迹与每步耗时；
   - 脚本打的日志在 MPL 的 Logs 页签；
   - 收件方收到的 body 应与 `resources/payload/out-low-stock-products.csv` 结构一致。

## 常见坑（都在 MPL 里现形）

| 现象 | 原因 | 处理 |
|---|---|---|
| `Couldn't find the endpoint...` | Sender Address 与调用 URL 不一致 | 以部署后 Monitor 里展示的端点为准 |
| OData 401/404 | 认证或路径写错 | 先用 Postman 单独调通目标服务再接到 iFlow |
| 脚本报 `XmlSlurper` 找不到节点 | 命名空间前缀不同 | 用 payload 样例对照，调整遍历前缀/路径 |
| 输出乱码 | 编码不一致 | Content Modifier 里显式 `UTF-8`；Receiver 配 `Content-Type: text/csv; charset=utf-8` |
| 变量未定义 | Header/Property 拼写或作用域 | 日志脚本先打一遍 `message.getHeaders()/getProperties()` |

> 进阶：换 **Timer** 发件方即变定时任务；加 **Exception Subprocess + Escalation** 实现失败告警；
> 把 csv 输出改成 **Data Store** 落库再异步取走，就是“存储转发”模式。
