// ============================================================
// 受注管理服务 (OData V4): 投影 + 状态机 Action
// 参考 要件定義書: 機能要件 F-0100 受注登録 / F-0200 承認 / F-0300 変更 / F-0400 却下・差戻し
// ============================================================
using sap.training.bookorder as db from '../db/schema';

service OrderService @(path: '/odata/order') {

  // ---- 主数据: 只读 ----
  @readonly
  entity Books as projection on db.Books;

  @readonly
  entity Customers as projection on db.Customers;

  // ---- 受注: 全 CRUD(状态机在服务端把关) ----
  entity Orders as projection on db.BookOrders;

  // 受注明細: 允许直接行增删改(前提: 订单处于 OPEN / REJECTED)
  entity OrderItems as projection on db.BookOrderItems;

  // ---- 状态机 Action (服务级 unbound; 入参校验由实现完成) ----
  @requires: 'authenticated-user'
  action approve(orderNo: String)
    returns { ok: Boolean; status: String };

  @requires: 'authenticated-user'
  action rejectOrder(orderNo: String, reason: String)
    returns { ok: Boolean; status: String };

  @requires: 'authenticated-user'
  action sendBack(orderNo: String)
    returns { ok: Boolean; status: String };    // 差戻し: APPROVED -> OPEN, 之后可修改
}
