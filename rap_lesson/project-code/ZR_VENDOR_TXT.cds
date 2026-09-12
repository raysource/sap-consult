# ZR_VENDOR_TXT — 供应商主数据视图（CDS）
# 用途: 供应商 F4 值帮助 / 数据预览关联
@EndUserText.label: '供应商主数据视图'
@AccessControl.authorizationCheck: #NOT_REQUIRED
@AbapCatalog.viewEnhancementCategory: [#NONE]
define view entity ZR_VENDOR_TXT
  as select from z_vendor_txt
{
  key vendor_code as VendorCode,
      vendor_name as VendorName,
      country     as Country
}
