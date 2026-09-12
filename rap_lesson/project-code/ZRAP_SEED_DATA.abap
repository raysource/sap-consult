" ============================================================
" ZRAP_SEED_DATA — 造数程序（开发/测试环境使用）
" 警告: 会 DELETE 三张表后重新插入；只可在练习系统执行！
" ============================================================
REPORT zrap_seed_data.

" 1) 供应商
DELETE FROM z_vendor_txt.
INSERT z_vendor_txt FROM TABLE @( VALUE #(
  ( vendor_code = '0000000001' vendor_name = 'ABC Trading'  country = 'JP' )
  ( vendor_code = '0000000002' vendor_name = 'XYZ Parts'    country = 'DE' )
  ( vendor_code = '0000000003' vendor_name = 'Global Foods' country = 'US' ) ) ).

" 2) 订单头 + 明细
DELETE FROM z_po_hdr.
DELETE FROM z_po_itm.
INSERT z_po_hdr FROM TABLE @( VALUE #(
  ( po_num = 'Z0000000001' po_date = '20260901' vendor_code = '0000000001' status = 'NEW'       created_by = sy-uname )
  ( po_num = 'Z0000000002' po_date = '20260902' vendor_code = '0000000002' status = 'CONFIRMED' created_by = sy-uname ) ) ).
INSERT z_po_itm FROM TABLE @( VALUE #(
  ( po_num = 'Z0000000001' item_num = '0010' matnr = 'MAT-100' qty = 10 unit = 'EA' net_price = '1000.00' currency = 'JPY' )
  ( po_num = 'Z0000000001' item_num = '0020' matnr = 'MAT-200' qty = 5  unit = 'EA' net_price = '2500.00' currency = 'JPY' )
  ( po_num = 'Z0000000002' item_num = '0010' matnr = 'MAT-300' qty = 2  unit = 'PC' net_price = '80.00'   currency = 'USD' ) ) ).

IF sy-subrc = 0.
  WRITE 'OK: vendor=3, header=2, item=3'.
ENDIF.
