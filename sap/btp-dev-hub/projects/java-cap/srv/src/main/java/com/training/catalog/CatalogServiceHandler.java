package com.training.catalog;

// ---------------------------------------------------------------------
// 自定义业务逻辑 (与 node-cap 的 catalog-service.js 演示同一 Action)
//
// ⚠ 本文件使用了"类型化访问器" API: 首次执行 mvn compile 后, 插件会把
//    .cds 编译成 Java 类型, 位于 target/generated-sources/cds4j/cds/gen/
//    若签名与本文件有出入(不同 SDK 小版本生成略有差异), 以生成代码为准。
// 参照: SAP-samples/cloud-cap-samples-java 的 CatalogServiceHandler
// ---------------------------------------------------------------------

import static cds.gen.catalogservice.CatalogService_.PRODUCTS;

import cds.gen.catalogservice.AdjustPriceContext;
import cds.gen.catalogservice.Products;
import com.sap.cds.Result;
import com.sap.cds.ql.Select;
import com.sap.cds.ql.Update;
import com.sap.cds.services.handler.EventHandler;
import com.sap.cds.services.handler.annotations.On;
import com.sap.cds.services.handler.annotations.ServiceName;
import com.sap.cds.services.persistence.PersistenceService;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

/** CatalogService 的处理器: 演示 Action(adjustPrice) 在 Java 里的写法。 */
@Component
@ServiceName(CatalogService_.CDS_NAME)
public class CatalogServiceHandler implements EventHandler {

  private final PersistenceService db;

  // Spring 构造注入 CAP 持久化服务(自动路由到当前租户/事务)
  @Autowired
  public CatalogServiceHandler(PersistenceService db) {
    this.db = db;
  }

  /**
   * 自定义 Action: adjustPrice(按百分比批量调价)
   * 框架把 OData Action 请求映射为类型化上下文 AdjustPriceContext
   * (由 cds-maven-plugin 从 catalog-service.cds 生成)。
   */
  @On
  public AdjustPriceContext.ReturnType onAdjustPrice(AdjustPriceContext context) {
    List<String> productIDs = context.getProductIDs();
    BigDecimal delta = context.getDeltaPercent();
    BigDecimal factor = BigDecimal.ONE.add(delta.divide(BigDecimal.valueOf(100)));

    int updated = 0;
    for (String id : productIDs) {
      // 1) 类型化查询: 取当前单价
      Products product = db.run(Select.from(PRODUCTS).byId(id)).single();

      // 2) 计算新价(四舍五入到分)
      BigDecimal newPrice = product
          .getPrice()
          .multiply(factor)
          .setScale(2, RoundingMode.HALF_UP);

      // 3) 类型化更新: Update.entity(...).byId(...).data(字段, 值)
      db.run(Update.entity(PRODUCTS).byId(id).data(Products.PRICE, newPrice));
      updated++;
    }

    AdjustPriceContext.ReturnType result = AdjustPriceContext.ReturnType.create();
    result.setUpdated(updated);
    return result;
  }
}
