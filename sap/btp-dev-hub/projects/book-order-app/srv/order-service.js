// ============================================================
// 受注管理 服务处理器 - 状态机 / 校验 / 自动计算
//
// 状态: OPEN(未承認) -> APPROVED(承認済); OPEN -> REJECTED(却下)
//        APPROVED --差戻し(sendBack)--> OPEN  (承認後の変更は差戻してから)
// 变更规则: ヘッダ/明細 的修改仅允许 OPEN / REJECTED; APPROVED 一律 400
// ============================================================
const cds = require('@sap/cds');

const DB_ORDERS = 'sap.training.bookorder.BookOrders';
const DB_ITEMS  = 'sap.training.bookorder.BookOrderItems';
const DB_BOOKS  = 'sap.training.bookorder.Books';

const STATUS = { OPEN: 'OPEN', APPROVED: 'APPROVED', REJECTED: 'REJECTED' };

module.exports = cds.service.impl(async function () {

  const { Orders, OrderItems } = this.entities;

  // ---------- 小工具 ----------
  const fmtDate = (v) => {
    if (v instanceof Date) {
      const p = (n) => String(n).padStart(2, '0');
      return `${v.getFullYear()}-${p(v.getMonth() + 1)}-${p(v.getDate())}`;
    }
    const s = String(v || '');
    return /^\d{4}-\d{2}-\d{2}/.test(s) ? s.slice(0, 10) : undefined;
  };
  const round2 = (n) => Number(Number(n).toFixed(2));

  async function getOrder(orderNo) {
    // 事件处理器内直接执行 CQN = 自动加入请求事务(ambient), 不要手动开新事务
    return (await SELECT.from(DB_ORDERS).where({ orderNo }))[0];
  }
  async function bookMap() {
    const rows = await SELECT.from(DB_BOOKS);
    const m = new Map();
    for (const b of rows) m.set(b.code, b);
    return m;
  }
  const noOrder = (orderNo) => `受注 ${orderNo} 不存在`;

  // 校验并加工行(用主数据补齐单价/书名快照; 计算行金额)
  function buildLines(items, books) {
    const lines = [];
    let no = 0;
    for (const it of items || []) {
      const book = books.get(it.book_code);
      if (!book) throw new Error(`書籍コード不存在: ${it.book_code}`);
      const qty = Number(it.quantity);
      if (!Number.isInteger(qty) || qty <= 0)
        throw new Error(`数量必须为大于 0 的整数(行: ${it.book_code})`);
      const unitPrice = it.unitPrice != null ? Number(it.unitPrice) : Number(book.price);
      if (!(unitPrice > 0)) throw new Error(`単価必须大于 0(行: ${it.book_code})`);
      no += 1;
      lines.push({
        lineNo: no,
        book_code: book.code,
        bookTitle: book.title,          // 快照: 以主数据为准
        quantity: qty,
        unitPrice: round2(unitPrice),
        lineTotal: round2(qty * unitPrice),
      });
    }
    if (lines.length === 0) throw new Error('受注至少需要一行明細');
    return lines;
  }

  // 重新合计订单金额(明細行增删改后调用)。注: 主键非 ID, 用 where 形式 UPDATE
  async function recalcTotal(orderNo) {
    const [{ total }] = await SELECT.from(DB_ITEMS)
      .columns('sum(lineTotal) as total').where({ orderNo });
    await UPDATE(DB_ORDERS).set({ totalAmount: round2(total || 0) }).where({ orderNo });
  }

  // ---------- 受注登録 (F-0100): 先登ヘッダ, 明細经 OrderItems 追加 ----------
  this.before('CREATE', Orders, async (req) => {
    const rows = Array.isArray(req.data) ? req.data : [req.data];
    for (const row of rows) {
      // 无托管组合, 不接受嵌套 items; 提示两段式登録
      if (row.items && row.items.length)
        return req.reject(400, '请先登録受注ヘッダ, 再通过 OrderItems 追加明細(金额自动计算)');

      // 採番 / 默认值(忽略客户端传入的受注番号与状态) —— SO+yyyyMMdd-4位码, ≤16 字符
      const d = new Date();
      const ymd = d.toISOString().slice(0, 10).replace(/-/g, '');
      const rand = Math.random().toString(36).slice(2, 6).toUpperCase().padEnd(4, '0');
      row.orderNo = 'SO' + ymd + '-' + rand;
      row.status = STATUS.OPEN;
      row.rejectReason = null; row.rejectedBy = null; row.rejectedAt = null;
      row.approvedBy = null;   row.approvedAt = null;
      row.orderDate = fmtDate(row.orderDate) || fmtDate(d);
      row.totalAmount = 0;                       // 行登録后由 recalcTotal 汇总
      delete row.items;
    }
  });

  // ---------- 変更 (F-0300): ヘッダ字段 ----------
  this.before('UPDATE', Orders, async (req) => {
    const orderNo = req.data.orderNo;
    const existing = await getOrder(orderNo);
    if (!existing) return req.reject(404, noOrder(orderNo));
    if (existing.status === STATUS.APPROVED)
      return req.reject(400, `受注 ${orderNo} 已承認, 不可直接修改; 请先差戻し(sendBack)`);

    // 状态与审计字段一律以服务端为准, 忽略客户端篡改
    req.data.status = existing.status;
    req.data.approvedBy = existing.approvedBy; req.data.approvedAt = existing.approvedAt;
    req.data.rejectedBy = existing.rejectedBy; req.data.rejectedAt = existing.rejectedAt;
    req.data.rejectReason = existing.rejectReason;
    req.data.totalAmount = existing.totalAmount;   // 金额只能由行变化重算
    if (req.data.orderDate) req.data.orderDate = fmtDate(req.data.orderDate);
  });

  // ---------- 取消(削除): 仅 未承認/却下 ----------
  this.before('DELETE', Orders, async (req) => {
    const orderNo = req.data.orderNo;
    const existing = await getOrder(orderNo);
    if (!existing) return req.reject(404, noOrder(orderNo));
    if (existing.status === STATUS.APPROVED)
      return req.reject(400, `受注 ${orderNo} 已承認, 不可删除; 请先差戻し`);
  });

  // ---------- 明細行增删改 (F-0300 的一部分) ----------
  this.before('CREATE', OrderItems, async (req) => {
    const row = req.data;
    const parent = await getOrder(row.orderNo);
    if (!parent) return req.reject(404, noOrder(row.orderNo));
    if (parent.status === STATUS.APPROVED)
      return req.reject(400, `受注 ${row.orderNo} 已承認, 明細不可变更`);

    const books = await bookMap();
    let line;
    try {
      [line] = buildLines(
        [{ book_code: row.book_code, quantity: row.quantity, unitPrice: row.unitPrice }],
        books
      );
    } catch (e) {
      return req.reject(400, e.message);
    }
    // 自动行号: 现有最大行号 + 1
    const max = await SELECT.from(DB_ITEMS)
      .columns('max(lineNo) as m').where({ orderNo: row.orderNo });
    row.lineNo = (max[0]?.m || 0) + 1;
    row.bookTitle = line.bookTitle; row.quantity = line.quantity;
    row.unitPrice = line.unitPrice; row.lineTotal = line.lineTotal;
  });

  this.before('UPDATE', OrderItems, async (req) => {
    const { orderNo, lineNo } = req.data;
    const parent = await getOrder(orderNo);
    if (!parent) return req.reject(404, noOrder(orderNo));
    if (parent.status === STATUS.APPROVED)
      return req.reject(400, `受注 ${orderNo} 已承認, 明細不可变更`);

    const [cur] = await SELECT.from(DB_ITEMS).where({ orderNo, lineNo });
    if (!cur) return req.reject(404, `行 ${lineNo} 不存在`);

    // 数量/単価: 传了就校验, 没传就保留现值; 行金额由服务端重算
    const qty = req.data.quantity != null ? Number(req.data.quantity) : Number(cur.quantity);
    if (!Number.isInteger(qty) || qty <= 0) return req.reject(400, '数量必须为大于 0 的整数');
    const unit = req.data.unitPrice != null ? Number(req.data.unitPrice) : Number(cur.unitPrice);
    if (!(unit > 0)) return req.reject(400, '単価必须大于 0');

    req.data.quantity = qty;
    req.data.unitPrice = unit;
    req.data.lineTotal = round2(qty * unit);
    req.data.lineNo = lineNo;            // 键不可改
    req.data.book_code = cur.book_code;  // 主数据引用不可改(换书=删行重加)
    req.data.bookTitle = cur.bookTitle;  // 快照列不可改
  });

  this.before('DELETE', OrderItems, async (req) => {
    const parent = await getOrder(req.data.orderNo);
    if (!parent) return req.reject(404, noOrder(req.data.orderNo));
    if (parent.status === STATUS.APPROVED)
      return req.reject(400, `受注 ${req.data.orderNo} 已承認, 明細不可变更`);
  });

  // 行变化后: 重算ヘッダ合計 (DELETE 的 each 不包含行数据, 从 req.data 取订单号)
  for (const ev of ['CREATE', 'UPDATE', 'DELETE']) {
    this.after(ev, OrderItems, async (each, req) => {
      const orderNo = (req && req.data && req.data.orderNo) || (each && each.orderNo);
      if (orderNo) await recalcTotal(orderNo);
    });
  }

  // ---------- 承認 (F-0200): OPEN -> APPROVED ----------
  this.on('approve', async (req) => {
    const { orderNo } = req.data;
    const existing = await getOrder(orderNo);
    if (!existing) return req.reject(404, noOrder(orderNo));
    if (existing.status !== STATUS.OPEN)
      return req.reject(400, `受注 ${orderNo} 当前状态 ${existing.status}, 只有 OPEN 可承認`);

    await UPDATE(DB_ORDERS).set({
      status: STATUS.APPROVED,
      approvedBy: req.user?.id || 'anonymous',
      approvedAt: new Date().toISOString(),
    }).where({ orderNo });
    return { ok: true, status: STATUS.APPROVED };
  });

  // ---------- 却下 (F-0400): OPEN -> REJECTED(必须写理由) ----------
  // 注意: 命名为 rejectOrder(reject 与框架基类方法冲突, 无法注册)
  this.on('rejectOrder', async (req) => {
    const { orderNo, reason } = req.data;
    if (!reason || !String(reason).trim())
      return req.reject(400, '却下时必须填写理由(reason)');
    const existing = await getOrder(orderNo);
    if (!existing) return req.reject(404, noOrder(orderNo));
    if (existing.status !== STATUS.OPEN)
      return req.reject(400, `受注 ${orderNo} 当前状态 ${existing.status}, 只有 OPEN 可却下`);

    await UPDATE(DB_ORDERS).set({
      status: STATUS.REJECTED,
      rejectReason: String(reason).trim(),
      rejectedBy: req.user?.id || 'anonymous',
      rejectedAt: new Date().toISOString(),
    }).where({ orderNo });
    return { ok: true, status: STATUS.REJECTED };
  });

  // ---------- 差戻し (F-0400): APPROVED -> OPEN(解除冻结) ----------
  this.on('sendBack', async (req) => {
    const { orderNo } = req.data;
    const existing = await getOrder(orderNo);
    if (!existing) return req.reject(404, noOrder(orderNo));
    if (existing.status !== STATUS.APPROVED)
      return req.reject(400, `受注 ${orderNo} 当前状态 ${existing.status}, 只有 APPROVED 可差戻し`);

    await UPDATE(DB_ORDERS).set({
      status: STATUS.OPEN,
      approvedBy: null, approvedAt: null,
      rejectReason: null, rejectedBy: null, rejectedAt: null,
    }).where({ orderNo });
    return { ok: true, status: STATUS.OPEN };
  });
});
