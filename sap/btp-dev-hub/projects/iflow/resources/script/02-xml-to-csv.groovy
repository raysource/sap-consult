import groovy.xml.XmlSlurper
import java.nio.charset.StandardCharsets

// ============================================================
// 02 - 核心脚本: OData XML feed -> CSV 文本
// 输入:  <feed> 内含多个 <entry><content><m:properties>
//        ProductID / ProductName / UnitPrice / UnitsInStock
// 输出:  CSV 数据行(不含表头, 表头由后面的 Content Modifier 补)
//        同时把行数写入 property: csvLineCount
// ============================================================

def Message processData(Message message) {

    // ---- 1. 取原始 body ----
    String body = message.getBody(String.class)
    if (body == null || body.trim().isEmpty()) {
        message.setProperty('csvLineCount', '0')
        message.setBody('', StandardCharsets.UTF_8.name())
        return message
    }

    // ---- 2. 解析 XML ----
    def xml = new XmlSlurper().parseText(body)
    def ns = new groovy.xml.Namespace('http://www.w3.org/2005/Atom', 'atom')
    def d  = new groovy.xml.Namespace('http://schemas.microsoft.com/ado/2007/08/dataservices', 'd')
    def m  = new groovy.xml.Namespace('http://schemas.microsoft.com/ado/2007/08/dataservices/metadata', 'm')

    StringBuilder csv = new StringBuilder()
    int count = 0

    xml.'**'.findAll { it.name() == 'entry' }.each { entry ->
        def props = entry.content.properties
        String pid  = props.ProductID.text()?.trim()
        String pname = props.ProductName.text()?.trim()?.replaceAll(',', ' ') // CSV 转义: 去掉逗号
        String price = props.UnitPrice.text()?.trim()
        String stock = props.UnitsInStock.text()?.trim()

        // 业务过滤: 只保留低库存 (<= 外部传入的 maxStock)
        String maxStock = message.getProperty('maxStock') ?: '15'
        if (stock && stock.isNumber() && (stock as int) > (maxStock as int)) {
            return // 跳过
        }

        csv.append("${pid},${pname},${price},${stock}\n")
        count++
    }

    // ---- 3. 设回 body + property ----
    message.setBody(csv.toString(), StandardCharsets.UTF_8.name())
    message.setProperty('csvLineCount', count.toString())

    return message
}
