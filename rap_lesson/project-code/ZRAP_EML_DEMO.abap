" ============================================================
" ZRAP_EML_DEMO — RAP BO 端到端测试程序（ADT/SE38 中执行）
" 验证: 创建（早编号）-> 明细 -> 状态机（draft 环境请先在 Fiori/EML 中 Activate）
" ============================================================
REPORT zrap_eml_demo.

" ---------- 1) 创建订单头（主键由 early numbering 自动生成） ----------
MODIFY ENTITIES OF zr_zpoheader
  ENTITY zr_zpoheader
  CREATE FIELDS ( po_date vendor_code status zz_memo )
  WITH VALUE #( ( %cid = 'H1'
                  po_date = cl_abap_context_info=>get_system_date( )
                  vendor_code = '0000000001'
                  status = 'NEW'
                  zz_memo = 'EML 测试订单' ) )
  ENTITY zr_zpoitem
  CREATE BY \_items FIELDS ( item_num matnr qty unit net_price currency )
  WITH VALUE #( ( %cid_ref = 'H1' %cid = 'I1'
                  item_num = '0010' matnr = 'MAT-100'
                  qty = 10 unit = 'EA' net_price = '1000.00' currency = 'JPY' )
                ( %cid_ref = 'H1' %cid = 'I2'
                  item_num = '0020' matnr = 'MAT-200'
                  qty = 5  unit = 'EA' net_price = '2500.00' currency = 'JPY' ) )
  MAPPED DATA(lt_mapped)
  FAILED DATA(lt_failed)
  REPORTED DATA(lt_reported).

IF lt_failed IS NOT INITIAL.
  LOOP AT lt_reported INTO DATA(ls_rep).
    WRITE: / '创建失败:', ls_rep-%msg->get_text( ).
  ENDLOOP.
  RETURN.
ENDIF.

" 读出框架自动分配的订单号（mapped 也可取）
READ ENTITIES OF zr_zpoheader
  ENTITY zr_zpoheader
  ALL FIELDS WITH VALUE #( ( %cid = 'H1' ) )
  RESULT DATA(lt_headers).

DATA(lv_po_num) = lt_headers[ 1 ]-po_num.
WRITE: / '已创建订单(草稿):', lv_po_num.

" ---------- 2) Activate（draft -> 正式表） ----------
MODIFY ENTITIES OF zr_zpoheader
  ENTITY zr_zpoheader
  EXECUTE activate
  WITH VALUE #( ( %key-po_num = lv_po_num ) )
  FAILED DATA(lt_fail_act)
  REPORTED DATA(lt_rep_act).
IF lt_fail_act IS NOT INITIAL.
  LOOP AT lt_rep_act INTO DATA(ls_rep_act).
    WRITE: / 'Activate 失败:', ls_rep_act-%msg->get_text( ).
  ENDLOOP.
  RETURN.
ENDIF.
WRITE: / '订单已激活（写入正式表）'.

" ---------- 3) 确定订单（Action: NEW -> CONFIRMED） ----------
MODIFY ENTITIES OF zr_zpoheader
  ENTITY zr_zpoheader
  EXECUTE confirmorder
  WITH VALUE #( ( %key-po_num = lv_po_num ) )
  RESULT DATA(lt_action)
  FAILED DATA(lt_fail2)
  REPORTED DATA(lt_rep2).

IF lt_fail2 IS NOT INITIAL.
  LOOP AT lt_rep2 INTO DATA(ls_rep2).
    WRITE: / 'Action 失败:', ls_rep2-%msg->get_text( ).
  ENDLOOP.
ELSE.
  WRITE: / '订单已确定，状态 =', lt_action[ 1 ]-%param-status.
ENDIF.

" ---------- 4) 再对同一订单执行（应报错：只有 NEW 可确定） ----------
MODIFY ENTITIES OF zr_zpoheader
  ENTITY zr_zpoheader
  EXECUTE confirmorder
  WITH VALUE #( ( %key-po_num = lv_po_num ) )
  FAILED DATA(lt_fail3)
  REPORTED DATA(lt_rep3).
IF lt_fail3 IS NOT INITIAL.
  WRITE: / '重复确定被拦截（符合状态机预期）'.
ENDIF.
