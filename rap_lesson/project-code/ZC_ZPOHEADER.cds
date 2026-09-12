# ZC_ZPOHEADER — 采购订单消费投影视图（CDS + UI 注解）
# 创建: ADT -> New -> Data Definition -> Define Projection View
# 说明: provider contract transactional_query = 可读写投影（行为来自下层 BO）
@EndUserText.label: '采购订单消费投影'
@AccessControl.authorizationCheck: #NOT_REQUIRED
@Metadata.ignorePropagatedAnnotations: true
@UI: {
  headerInfo: {
    typeName: '采购订单',
    typeNamePlural: '采购订单',
    title: { type: #FOR_KEY, value: 'PoNum' }
  },
  presentationVariant: [ { sortOrder: [ { by: 'PoDate', direction: #DESC } ] } ]
}
@Search.searchable: true
define root view entity ZC_ZPOHEADER
  provider contract transactional_query
  as projection on ZR_ZPOHEADER
{
  @UI: {
    lineItem:       [ { position: 10, label: '订单号' } ],
    selectionField: [ { position: 10 } ],
    identification: [ { position: 10 } ]
  }
  @Search.defaultSearchElement: true
  key PoNum,

  @UI: {
    lineItem:       [ { position: 20, label: '采购日期' } ],
    selectionField: [ { position: 20 } ],
    identification: [ { position: 20 } ]
  }
  PoDate,

  @UI: {
    lineItem:       [ { position: 30, label: '供应商' } ],
    selectionField: [ { position: 30 } ],
    identification: [ { position: 30 } ]
  }
  @Consumption.valueHelpDefinition: [ { entity: { name: 'ZR_VENDOR_TXT', element: 'VendorCode' } } ]
  VendorCode,

  @UI: {
    lineItem:       [ { position: 40, label: '状态' } ],
    selectionField: [ { position: 40 } ],
    identification: [ { position: 40 } ]
  }
  Status,

  @UI: { lineItem: [ { position: 50, label: '备注' } ] }
  ZzMemo,

  @UI.hidden: true
  CreatedBy
}
