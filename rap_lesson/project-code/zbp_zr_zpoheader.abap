" ============================================================
" zbp_zr_zpoheader — Behavior Implementation（BIL / behavior pool）
" 生成: BDEF 光标置于方法上 -> Ctrl+1 -> Add all missing methods
" 本文件 = 全局类骨架 + 本地 handler 类（LHC 头实体 / LHC 明细实体）
" ============================================================
CLASS zbp_zr_zpoheader DEFINITION PUBLIC ABSTRACT FINAL
  FOR BEHAVIOR OF zr_zpoheader.
ENDCLASS.

CLASS zbp_zr_zpoheader IMPLEMENTATION.
ENDCLASS.

" ============================================================
" 本地类 1: 头实体 handler（编号 / 默认值 / 校验 / Action）
" ============================================================
CLASS lhc_zpoheader DEFINITION INHERITING FROM cl_abap_behavior_handler.
  PRIVATE SECTION.
    " --- 编号（早编号：CREATE 时从番号范围 ZNPO 取号） ---
    METHODS earlynumbering_create FOR NUMBERING
      IMPORTING entities FOR CREATE zr_zpoheader.

    " --- 默认值 Determination（modify 时触发） ---
    METHODS setdefaultvalues FOR DETERMINE ON MODIFY
      IMPORTING keys FOR zr_zpoheader.

    " --- 校验 Validation（save 时触发：供应商必须存在） ---
    METHODS validatevendor FOR VALIDATE ON SAVE
      IMPORTING keys FOR zr_zpoheader.

    " --- Action：確定订单（NEW -> CONFIRMED） ---
    METHODS confirmorder FOR MODIFY
      IMPORTING keys FOR ACTION zr_zpoheader~confirmorder
                RESULT result.
ENDCLASS.

CLASS lhc_zpoheader IMPLEMENTATION.

  METHOD earlynumbering_create.
    DATA: lv_number TYPE n LENGTH 10,
          lv_po_num TYPE z_po_hdr-po_num.

    LOOP AT entities INTO DATA(ls_entity).
      " 跳过已有主键的（防重入）
      IF ls_entity-po_num IS NOT INITIAL.
        APPEND VALUE #( %cid = ls_entity-%cid %key = ls_entity-%key
                        %is_draft = ls_entity-%is_draft po_num = ls_entity-po_num )
               TO mapped-zr_zpoheader.
        CONTINUE.
      ENDIF.

      CALL FUNCTION 'NUMBER_GET_NEXT'
        EXPORTING
          nr_range_nr = '01'
          object      = 'ZNPO'
        IMPORTING
          number      = lv_number.

      CONCATENATE 'Z' lv_number INTO lv_po_num.
      APPEND VALUE #( %cid = ls_entity-%cid %key = ls_entity-%key
                      %is_draft = ls_entity-%is_draft po_num = lv_po_num )
             TO mapped-zr_zpoheader.
    ENDLOOP.
  ENDMETHOD.

  METHOD setdefaultvalues.
    READ ENTITIES OF zr_zpoheader IN LOCAL MODE
      ENTITY zr_zpoheader
      FIELDS ( po_num po_date vendor_code status created_by )
      WITH CORRESPONDING #( keys )
      RESULT DATA(lt_headers).

    DATA(lv_date) = cl_abap_context_info=>get_system_date( ).
    DATA(lv_user) = cl_abap_context_info=>get_user_abap_64( ).

    MODIFY ENTITIES OF zr_zpoheader IN LOCAL MODE
      ENTITY zr_zpoheader
      UPDATE FIELDS ( po_date created_by status )
      WITH VALUE #( FOR ls_hdr IN lt_headers (
          %tky = ls_hdr-%tky
          po_date = COND #( WHEN ls_hdr-po_date IS INITIAL
                            THEN lv_date ELSE ls_hdr-po_date )
          created_by = COND #( WHEN ls_hdr-created_by IS INITIAL
                               THEN lv_user ELSE ls_hdr-created_by )
          status = COND #( WHEN ls_hdr-status IS INITIAL
                           THEN 'NEW' ELSE ls_hdr-status ) ) )
      REPORTED DATA(lt_rep)
      FAILED DATA(lt_fail).
  ENDMETHOD.

  METHOD validatevendor.
    READ ENTITIES OF zr_zpoheader IN LOCAL MODE
      ENTITY zr_zpoheader
      FIELDS ( vendor_code )
      WITH CORRESPONDING #( keys )
      RESULT DATA(lt_headers).

    DATA: lv_exists TYPE abap_bool.
    LOOP AT lt_headers INTO DATA(ls_hdr).
      CLEAR lv_exists.
      SELECT SINGLE @abap_true FROM z_vendor_txt
        WHERE vendor_code = @ls_hdr-vendor_code INTO @lv_exists.

      IF lv_exists <> abap_true.
        APPEND VALUE #( %tky = ls_hdr-%tky ) TO failed-zr_zpoheader.
        APPEND VALUE #( %tky = ls_hdr-%tky
                        %state_area = 'VALIDATE_VENDOR'
                        %msg = new_message_with_text(
                          severity = if_abap_behv_message=>severity-error
                          text = |供应商 { ls_hdr-vendor_code } 不存在| ) )
               TO reported-zr_zpoheader.
      ENDIF.
    ENDLOOP.
  ENDMETHOD.

  METHOD confirmorder.
    READ ENTITIES OF zr_zpoheader IN LOCAL MODE
      ENTITY zr_zpoheader
      FIELDS ( status )
      WITH CORRESPONDING #( keys )
      RESULT DATA(lt_headers).

    LOOP AT lt_headers INTO DATA(ls_hdr) WHERE status <> 'NEW'.
      APPEND VALUE #( %tky = ls_hdr-%tky ) TO failed-zr_zpoheader.
      APPEND VALUE #( %tky = ls_hdr-%tky
                      %state_area = 'CONFIRM_ORDER'
                      %msg = new_message_with_text(
                        severity = if_abap_behv_message=>severity-error
                        text = |只有 NEW 状态的订单可以确定| ) )
             TO reported-zr_zpoheader.
    ENDLOOP.

    MODIFY ENTITIES OF zr_zpoheader IN LOCAL MODE
      ENTITY zr_zpoheader
      UPDATE FIELDS ( status )
      WITH VALUE #( FOR ls IN lt_headers WHERE ( status = 'NEW' )
                    ( %tky = ls-%tky status = 'CONFIRMED' ) )
      FAILED DATA(lt_mod_fail)
      REPORTED DATA(lt_mod_rep).

    READ ENTITIES OF zr_zpoheader IN LOCAL MODE
      ENTITY zr_zpoheader
      ALL FIELDS WITH CORRESPONDING #( keys )
      RESULT DATA(lt_final).

    result = VALUE #( FOR ls_final IN lt_final
                      ( %tky = ls_final-%tky %param = ls_final ) ).
  ENDMETHOD.
ENDCLASS.

" ============================================================
" 本地类 2: 明细实体 handler（金额/数量 > 0 校验）
" ============================================================
CLASS lhc_zpoitem DEFINITION INHERITING FROM cl_abap_behavior_handler.
  PRIVATE SECTION.
    METHODS validateitemamount FOR VALIDATE ON SAVE
      IMPORTING keys FOR zr_zpoitem.
ENDCLASS.

CLASS lhc_zpoitem IMPLEMENTATION.
  METHOD validateitemamount.
    READ ENTITIES OF zr_zpoheader IN LOCAL MODE
      ENTITY zr_zpoitem
      FIELDS ( net_price qty )
      WITH CORRESPONDING #( keys )
      RESULT DATA(lt_items).

    LOOP AT lt_items INTO DATA(ls_item)
         WHERE net_price <= 0 OR qty <= 0.
      APPEND VALUE #( %tky = ls_item-%tky ) TO failed-zr_zpoitem.
      APPEND VALUE #( %tky = ls_item-%tky
                      %state_area = 'VALIDATE_ITEM_AMOUNT'
                      %msg = new_message_with_text(
                        severity = if_abap_behv_message=>severity-error
                        text = |行项目金额与数量必须大于 0| ) )
             TO reported-zr_zpoitem.
    ENDLOOP.
  ENDMETHOD.
ENDCLASS.
