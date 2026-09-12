// ---------- CDS 数据模型: 培训示例域 (产品目录) ----------
// 模型语言即规范: 一份 .cds 同时驱动 数据库结构 / OData 服务 / Fiori UI
namespace sap.training.catalog;
using { cuid, managed, sap.common.CodeList } from '@sap/cds/common';

// 分类 (CodeList 风格基础数据)
// sap.common.CodeList 提供 name/descr 多语言文本字段
entity Categories : CodeList {
  key ID        : String(10);
  description   : String(200);
  icon          : String(40);   // 仅演示普通字段
}

// 产品 (根实体)
// cuid: 自动 UUID 主键; managed: 自动维护 createdAt/createdBy/modifiedAt/modifiedBy
entity Products : cuid, managed {
  name         : String(120) @title: '产品名称';
  description  : String(500);
  price        : Decimal(9, 2) @title: '单价';
  currency     : String(3) default 'CNY' @title: '币种';   // 生产可用 Currency 类型(自动码表校验)
  stock        : Integer @title: '库存';
  reorderLevel : Integer default 10 @title: '补货阈值';
  isActive     : Boolean default true @title: '启用';
  category     : Association to Categories @title: '分类';
}

// 常用按分类统计的只读视图: 顺便演示 CDS View
view ProductsByCategory as
  select from Products {
    category.name  as categoryName,
    count(*)       as productCount,
    sum(price)     as totalValue,
    avg(price)     as avgPrice
  } group by category.name;
