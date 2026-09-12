// ============================================================
// 服务处理器: 演示 CAP Node.js 事件处理器 (CQN / 事务 / 授权上下文)
// 运行时自动装配: 未覆盖的事件走框架的通用实现
// ============================================================
const cds = require('@sap/cds');

module.exports = cds.service.impl(async function () {

  const { Products } = this.entities;

  // ---------- 只读报表: productStats (聚合视图查询, 返回数组) ----------
  this.on('productStats', async () => {
    // 视图没有主键, 不能作为实体暴露, 但可以直接查
    return SELECT.from('sap.training.catalog.ProductsByCategory');
  });

  // ---------- 校验: 创建/更新前 (before hook) ----------
  this.before(['CREATE', 'UPDATE'], Products, async (req) => {
    const rows = Array.isArray(req.data) ? req.data : [req.data];
    for (const row of rows) {
      if (row.price != null && row.price < 0) {
        req.reject(400, `价格不能为负数: ${row.name || row.ID}`);
      }
      if (row.currency === 'USD' && row.price != null && row.price > 100000) {
        req.reject(400, `USD 单价超过 100,000 需走审批流: ${row.name || row.ID}`);
      }
    }
  });

  // ---------- 读增强: 返回前附加字段 (after hook) ----------
  this.after('READ', Products, (each) => {
    if (each.price != null && each.stock != null) {
      each.stockValue = Number((each.price * each.stock).toFixed(2)); // 金额小计(演示)
      each.lowStock = each.stock <= (each.reorderLevel ?? 10);
    }
  });

  // ---------- 自定义 Action: adjustPrice (批量按百分比调价) ----------
  this.on('adjustPrice', async (req) => {
    const { productIDs, deltaPercent } = req.data;
    if (!Array.isArray(productIDs) || productIDs.length === 0) {
      return req.reject(400, 'productIDs 不能为空');
    }
    if (deltaPercent == null) return req.reject(400, 'deltaPercent 必填');

    const tx = cds.tx(req); // 复用请求事务
    const factor = 1 + deltaPercent / 100;

    // 逐行取出 -> 计算新价 -> 写回 (同事务内完成, 保证一致性)
    const list = await tx.run(SELECT.from(Products).where({ ID: { in: productIDs } }));
    for (const p of list) {
      const newPrice = Number((p.price * factor).toFixed(2));
      await tx.run(UPDATE(Products, p.ID).with({ price: newPrice }));
    }
    req.reply({ updated: list.length });
  });
});
