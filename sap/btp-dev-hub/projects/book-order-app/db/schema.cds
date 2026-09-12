// ============================================================
// 图书受注管理 - 数据模型 (要件定義書「DB項目定義」的落地形态)
// 业务: 受注登録 -> 承認(或却下) -> 変更(差戻し后可改) -> 完了
// ============================================================
namespace sap.training.bookorder;
using { managed } from '@sap/cds/common';

// 図書マスタ(书籍主数据)
entity Books {
  key code      : String(10)  @title: '書籍コード';
  title         : String(120) @title: '书名';
  author        : String(60)  @title: '作者';
  publisher     : String(60)  @title: '出版社';
  price         : Decimal(9, 2)  @title: '定价';
  stock         : Integer default 0 @title: '库存';
}

// 得意先マスタ(客户主数据)
entity Customers {
  key code      : String(10)  @title: '得意先コード';
  name          : String(80)  @title: '客户名称';
  city          : String(40);
  contact       : String(40);
}

// 受注ヘッダ(订单头)
entity BookOrders : managed {
  key orderNo    : String(16) @title: '受注番号';      // 例 SO20260904-001 (服务端自动採番)
  orderDate      : Date       @title: '受注日';
  customer       : Association to Customers @title: '得意先';
  status         : String(10) default 'OPEN' @title: '状态';  // OPEN=未承認 / APPROVED=承認済 / REJECTED=却下
  rejectReason   : String(200);
  rejectedBy     : String(40);
  rejectedAt     : DateTime;
  approvedBy     : String(40);
  approvedAt     : DateTime;
  note           : String(300) @title: '備考';
  totalAmount    : Decimal(12, 2) @title: '合計金額';  // 服务端由明細重算, 客户端不可写
  // 明細: 显式 to-many(子表持有 FK), $expand=items 可读; 行本身通过 OrderItems CRUD 维护
  items          : Association to many BookOrderItems on items.orderNo = $self.orderNo;
}

// 受注明細(订单行) —— orderNo 用普通 FK 字段(避免关联键名泄漏), 由服务端保证一致性
entity BookOrderItems {
  key orderNo    : String(16) @title: '受注番号';   // 父订单号(FK, 非关联型)
  key lineNo     : Integer @title: '行号';          // 1..n, 服务端自动赋值
  book           : Association to Books;
  bookTitle      : String(120);                     // 快照列: 保留受注当时的书名
  quantity       : Integer  @title: '数量';
  unitPrice      : Decimal(9, 2) @title: '単価';
  lineTotal      : Decimal(12, 2) @title: '行金額'; // 服务端计算
}
