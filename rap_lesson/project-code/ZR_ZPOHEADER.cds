# ZR_ZPOHEADER — 采购订单头 BO Root View（CDS）
# Package: Z_WBS_DEV / 项目: ZPURORDER_APP
# 创建: ADT -> New -> Data Definition -> Define Root View Entity
# 依赖: 表 z_po_hdr, 视图 ZR_ZPOITEM / ZR_VENDOR_TXT
@EndUserText.label: '采购订单头 BO Root View'
@AccessControl.authorizationCheck: #NOT_REQUIRED
@Metadata.allowExtensions: true
@AbapCatalog.viewEnhancementCategory: [#NONE]
define root view entity ZR_ZPOHEADER
  as select from z_po_hdr
  composition [0..*] of ZR_ZPOITEM as _Items
  association [0..1] to ZR_VENDOR_TXT as _Vendor
    on $projection.VendorCode = _Vendor.VendorCode
{
  key po_num       as PoNum,
      po_date      as PoDate,
      vendor_code  as VendorCode,
      status       as Status,
      created_by   as CreatedBy,
      zz_memo      as ZzMemo,

      /* 关联：供应商主数据（只读），供 UI/服务导航与值帮助 */
      _Vendor
}
