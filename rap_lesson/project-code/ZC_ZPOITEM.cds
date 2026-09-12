# ZC_ZPOITEM — 采购订单明细消费投影视图（CDS + UI 注解）
# 说明: 对象页（Object Page）明细表由本视图的 lineItem 注解自动构成
@EndUserText.label: '采购订单明细消费投影'
@AccessControl.authorizationCheck: #NOT_REQUIRED
@Metadata.ignorePropagatedAnnotations: true
@UI: {
  headerInfo: { typeName: '采购订单明细', typeNamePlural: '采购订单明细' }
}
define view entity ZC_ZPOITEM
  provider contract transactional_query
  as projection on ZR_ZPOITEM
{
  @UI: { lineItem: [ { position: 10 } ], identification: [ { position: 10 } ] }
  key ItemNum,

  @UI: { lineItem: [ { position: 20, label: '物料' } ], identification: [ { position: 20 } ] }
  Matnr,

  @UI: { lineItem: [ { position: 30, label: '数量' } ], identification: [ { position: 30 } ] }
  Qty,

  @UI: { lineItem: [ { position: 40, label: '单位' } ], identification: [ { position: 40 } ] }
  Unit,

  @UI: { lineItem: [ { position: 50, label: '单价' } ], identification: [ { position: 50 } ] }
  NetPrice,

  @UI: { lineItem: [ { position: 60, label: '币种' } ], identification: [ { position: 60 } ] }
  Currency,

  @UI.hidden: true
  PoNum
}
