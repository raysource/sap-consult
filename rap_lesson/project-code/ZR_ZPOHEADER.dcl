# ZR_ZPOHEADER — Access Control（DCL，可选）
# 用途: 若把 CDS 的 @AccessControl.authorizationCheck 改为 #CHECK 时启用；
#       先在 SU21 创建授权对象 ZPURCHASE_AUTH（字段 VENDOR_CODE, ACTVT），再 PFCG 分配角色。
@EndUserText.label: '采购订单访问控制'
@MappingRole: true
define role ZR_ZPOHEADER {
  grant
    select
  on
    ZR_ZPOHEADER
  where
    ( vendor_code )
    = aspect pfcg_auth( ZPURCHASE_AUTH, VENDOR_CODE, ACTVT = '03' );

  grant select on ZR_ZPOITEM;
  grant select on ZR_VENDOR_TXT;
}
