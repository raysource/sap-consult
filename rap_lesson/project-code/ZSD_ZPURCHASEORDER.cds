# ZSD_ZPURCHASEORDER — Service Definition（服务定义）
# 创建: ADT -> New -> Service Definition
# 说明: 暴露哪些实体给外部；VendorTxt 供 VendorCode 的 F4 值帮助取数
@EndUserText.label: '采购订单 RAP 服务'
define service ZSD_ZPURCHASEORDER {
  expose ZC_ZPOHEADER as ZpoHeader;
  expose ZC_ZPOITEM   as ZpoItem;
  expose ZR_VENDOR_TXT as VendorTxt;
}
