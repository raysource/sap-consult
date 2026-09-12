# ZR_ZPOITEM — 采购订单明细 BO View（CDS）
# 创建: ADT -> New -> Data Definition -> Define View Entity
# 依赖: 表 z_po_itm
@EndUserText.label: '采购订单明细 BO View'
@AccessControl.authorizationCheck: #NOT_REQUIRED
@Metadata.allowExtensions: true
@AbapCatalog.viewEnhancementCategory: [#NONE]
define view entity ZR_ZPOITEM
  as select from z_po_itm
{
  key po_num     as PoNum,
  key item_num   as ItemNum,
      matnr      as Matnr,
      qty        as Qty,
      unit       as Unit,
      net_price  as NetPrice,
      currency   as Currency
}
