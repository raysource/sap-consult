import com.sap.it.api.mapping.MappingContext
import groovy.xml.XmlSlurper
import java.nio.charset.StandardCharsets

// ============================================================
// 01 - 脚本基础: 读 body / header / property, 打印日志
// 用途: 放在任意步骤后, 在 MPL(Message Processing Log)里观察消息
// ============================================================

def Message processData(Message message) {

    // 1) 消息体 (body) —— 按文本读取
    String body = message.getBody(String.class)
    message.setProperty('bodyCharsetInfo', 'utf-8')
    if (body != null) {
        // 只打前 2000 字符, 避免日志爆炸
        def preview = body.length() > 2000 ? body.substring(0, 2000) : body
        message.setProperty('bodyPreview', preview)
    }

    // 2) Header 与 Property
    def headers = message.getHeaders()          // 随出站请求发送
    def props   = message.getProperties()       // 仅当前消息上下文
    message.setProperty('headerNames', headers.keySet().join(','))
    message.setProperty('propertyNames', props.keySet().join(','))

    // 3) 取单个值 (推荐逐个取, 避免整包打印泄密)
    String source = message.getHeader('X-Source')          // null 安全: getHeader 不存在时返回 null
    String maxStock = message.getProperty('maxStock')
    message.setProperty('trace.maxStock', maxStock ?: 'NOT SET')
    message.setProperty('trace.X-Source', source ?: 'NOT SET')

    // 4) 直接写日志(比 System.out 更适合排查)
    def log = message.getLog() ?: java.util.logging.Logger.getLogger('iflow')
    // 生产环境推荐: message.setProperty('log.level','DEBUG') 或使用审计日志服务

    return message
}
