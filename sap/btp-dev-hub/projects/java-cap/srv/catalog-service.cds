// ---------- 服务定义: 对外只暴露"投影", 隐藏底层模型细节 ----------
using sap.training.catalog as db from '../db/schema';

service CatalogService @(path: '/odata/catalog') {

  // 自定义 Action: 批量加价/降价 (服务级 unbound action)
  // 演示 action + 入参出参 + @requires 授权; POST /odata/catalog/adjustPrice
  @requires: 'authenticated-user'
  action adjustPrice(productIDs: array of String, deltaPercent: Decimal(5, 2))
    returns { updated: Integer };

  // 只读报表函数: 聚合视图无主键, 用 function 返回(不落 OData 实体)
  // 演示 unbound function; GET /odata/catalog/productStats()
  function productStats()
    returns array of {
      categoryName : String;
      productCount : Integer;
      totalValue   : Decimal(9, 2);
      avgPrice     : Decimal(9, 2);
    };

// 启用草稿可让 Fiori elements 获得草稿编辑能力 —— 本地示例先不加,
// 需要时在 Products 投影上标注 @odata.draft.enabled 即可
@readonly
entity Categories as projection on db.Categories;

entity Products as projection on db.Products;
}
