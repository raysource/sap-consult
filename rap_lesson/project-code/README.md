# ============================================================
# ZPURORDER_APP（Z 购买订单管理）项目代码包说明
# 对应 WBS Sheet③「統合ミニプロジェクト」的 RAP 部分
# 使用前请先阅读同目录 site 的 手顺①〜④ / project.html
# ============================================================

## 创建顺序（建议严格按此顺序）
0) 包与 Transport ............................... 手顺①  (包 Z_WBS_DEV)
1) 数据字典（SE11 / ADT 建表，非代码）.......... z_po_hdr / z_po_itm / z_vendor_txt
2) 测试数据（造数程序）......................... ZRAP_SEED_DATA（见手顺①页面）
3) CDS BO 视图
   ZR_VENDOR_TXT.cds                    (供应商主数据视图)
   ZR_ZPOITEM.cds                       (明细视图)
   ZR_ZPOHEADER.cds                     (root BO 视图, 含 composition/association)
4) 行为层
   ZR_ZPOHEADER.bdef                    (BDEF: managed + draft + early numbering)
   zbp_zr_zpoheader.abap                (BIL: 全局类 + 本地 handler LHC)
5) 番号范围 ZNPO ............................... SNRO（见 README 字段说明或手顺③ STEP3-6）
6) 消费投影
   ZC_ZPOHEADER.cds                     (头投影 + UI 注解 + VH)
   ZC_ZPOITEM.cds                       (明细投影 + UI 注解)
   ZC_ZPOHEADER.bdef                    (Projection BDEF: use create/update/delete/action)
7) 服务
   ZSD_ZPURCHASEORDER.cds               (Service Definition)
   —— ADT 向导创建 Service Binding: ZUI_ZPURCHASEORDER_O4 (OData V4 UI)
8) 权限（可选）.................................. ZR_ZPOHEADER.dcl + SU21 授权对象
9) 测试 ......................................... ZRAP_EML_DEMO.abap 或 Fiori Preview

## 各文件创建方式
- *.cds   : ADT -> New -> Other ABAP Repository Object -> Core Data Services -> Data Definition
             （新建后把文件内容整体粘贴，再 Ctrl+S / Ctrl+F3 激活）
- *.bdef  : 右键 CDS 实体 -> New Behavior Definition（BDEF）粘贴内容
             投影 BDEF 在创建投影视图时勾选 transactional_query 自动生成，或手动 New。
- *.abap  : ADT -> New -> ABAP Class / Report（全局类名见文件内），本地类代码粘贴到 Include 区。
- *.dcl   : 右键 CDS 视图 -> New Access Control，粘贴内容。

## 注意
- 代码基于 S/4HANA 2021+ / BTP ABAP 环境 RAP 语法整理；请以实际系统 ADT 校验为准。
- draft 启用后，创建的数据先落草稿表，Activate 才写正式表（EML 示例已含 activate）。
- 若不用早编号而想直接手输订单号：删掉 BDEF 的 early numbering 与编号方法即可，
  并把 PoNum 字段控制改为 ( readonly : update )。
