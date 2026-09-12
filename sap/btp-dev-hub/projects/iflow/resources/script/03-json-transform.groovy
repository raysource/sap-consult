import groovy.json.JsonOutput
import groovy.json.JsonSlurper

// ============================================================
// 03 - 备用脚本: JSON 过滤 + 字段重组
// 适用: OData 以 $format=json 返回 / 对方直接发 JSON
// ============================================================

def Message processData(Message message) {

    String body = message.getBody(String.class)
    if (body == null || body.trim().isEmpty()) {
        message.setBody('[]', 'UTF-8')
        return message
    }

    def json = new JsonSlurper().parseText(body)

    // Northwind JSON: { "value": [ { ProductID, ProductName, UnitPrice, UnitsInStock } ] }
    def rows = json.value ?: json
    if (!(rows instanceof List)) rows = [rows]

    String maxStock = message.getProperty('maxStock') ?: '15'

    def filtered = rows.findAll { it.UnitsInStock != null && (it.UnitsInStock as int) <= (maxStock as int) }
                   .collect { row ->
        [
            productId: row.ProductID,
            name     : row.ProductName,
            price    : row.UnitPrice,
            stock    : row.UnitsInStock
        ]
    }

    // 覆盖消息体
    message.setBody(JsonOutput.prettyPrint(JsonOutput.toJson(filtered)), 'UTF-8')
    message.setProperty('filteredCount', filtered.size().toString())

    return message
}
