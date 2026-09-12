# 图书受注管理 (CAP Node.js) - 开发全流程课件的可运行实现

业务：**受注登録 → 承認 / 却下 → 変更(差戻し后可改) → 完了**
本工程对应课件《开发全流程课件》的“开发/测试”阶段产物：
要件定義書见 `course/要件定義書_图书受注管理.xlsx`。

## 状态机（服务端强制，客户端改不了状态）

```
            登録                    却下(reason 必填)
  [作成] --------> OPEN ----------------> REJECTED
                    ^  |                      |
                    |  | approve              | 修改(PATCH)后重新 submit
            sendBack|  |                      |
           (差戻し)  |  v                      |
                    | APPROVED <---------------+
                    +---(不可改/删; 仅差戻し)
```

| 状态 | 含义 | 可执行 |
|---|---|---|
| OPEN | 未承認(登録済) | 修改、删、追加行、approve / rejectOrder |
| APPROVED | 承認済 | 只读 + sendBack(差戻し) |
| REJECTED | 却下 | 修改、追加行(修正后再提交/重新登録) |

## 运行（Node 20/22；Node 26 暂缺 sqlite 原生库）

```bash
cd projects/book-order-app
npm install
npm run deploy     # 建 db.sqlite + 灌入 书籍/客户/2 笔示例受注
npm start          # http://localhost:4004/odata/order/
```

默认端口 4004（与其他示例一致）。若与 node-cap 同时跑，先停其一或改 package.json 端口。

## 资源

| 类型 | 路径 |
|---|---|
| OData 服务 | http://localhost:4004/odata/order/ ($metadata 可看结构) |
| 主数据(只读) | Books / Customers |
| 受注(CRUD) | Orders（明細以 items 展开，深创建） |
| 明細行 | OrderItems（单独增/改/删，行后自动重算合計） |
| 状态机 Action | approve / rejectOrder(orderNo, reason) / sendBack(orderNo) —— 需 Basic Auth(alice/alice) |

## 验收命令（第 1~7 步本机实测通过，见下方“实测输出”）

```bash
B="http://localhost:4004/odata/order"
# 1) 一覧(含状态与金额 + 明細展开)
curl -s "$B/Orders?\$expand=items&\$orderby=orderNo" | python3 -m json.tool

# 2) 受注登録(ヘッダ): 不传受注番号 -> 服务端採番; 状态自动 OPEN
curl -s -X POST "$B/Orders" -H "Content-Type: application/json" -d '{
  "orderDate":"2026-09-05","customer_code":"CUST-003","note":"演示登録"}'
#    → 記下返回的 orderNo(形如 SO20260905-HHMMSS), 用 $N 代替下面命令行中的订单号

# 3) 明細追加: 不传単価/书名 -> 从主数据补齐并自动行号/金额
curl -s -X POST "$B/OrderItems" -H "Content-Type: application/json" \
  -d '{"orderNo":"<N>","book_code":"B004","quantity":3}'
curl -s -X POST "$B/OrderItems" -H "Content-Type: application/json" \
  -d '{"orderNo":"<N>","book_code":"B007","quantity":2,"unitPrice":100}'
#    → 每次追加后ヘッダ totalAmount 自动更新

# 4) 非法明細: 书籍不存在 / 数量 0 -> 400
curl -s -X POST "$B/OrderItems" -H "Content-Type: application/json" \
  -d '{"orderNo":"<N>","book_code":"B999","quantity":1}'

# 5) 承認 (OPEN -> APPROVED; 需 alice)
curl -s -u alice:alice -X POST "$B/approve" -H "Content-Type: application/json" -d '{"orderNo":"SO20260904-001"}'
# 6) 已承認不可改: PATCH ヘッダ -> 400
curl -s -X PATCH "$B/Orders('SO20260903-001')" -H "Content-Type: application/json" -d '{"note":"想改"}'
# 7) 変更: OPEN 改備考 -> 200; 明細改数量 -> 合計自动重算
curl -s -X PATCH "$B/Orders('SO20260904-001')" -H "Content-Type: application/json" -d '{"note":"改为 9 月底到货"}'
curl -s -X PATCH "$B/OrderItems(orderNo='SO20260904-001',lineNo=1)" -H "Content-Type: application/json" -d '{"quantity":12}'
# 8) 却下(理由必填) -> REJECTED; 再承認(应 400)
curl -s -u alice:alice -X POST "$B/rejectOrder" -H "Content-Type: application/json" -d '{"orderNo":"SO20260904-001","reason":"客户预算未确认"}'
# 9) 差戻し -> OPEN, 修改后重新承認 (完整变更流)
curl -s -u alice:alice -X POST "$B/sendBack" -H "Content-Type: application/json" -d '{"orderNo":"SO20260903-001"}'
```

> 第 9 步之后 SO20260903-001 回到 OPEN 且 approvedBy 被清空 —— 这就是“承認後の変更”的完整路径。

## 本机实测输出（2026-09-05, macOS / Node 22 / SQLite）

| # | 操作 | 实测结果 |
|---|---|---|
| 登録 | POST /Orders(ヘッダのみ) | 201, `orderNo` 自动採番(如 SO20260905-35IQ), status=OPEN, total=0 |
| 明細追加 | POST /OrderItems(B004×3, 不传单价) | lineNo=1 自动, 书名・単価(168)从マスタ补齐, lineTotal=504 |
| 明細追加 | POST /OrderItems(B007×2, unitPrice=100) | lineNo=2, 折扣价生效 lineTotal=200 |
| 合計自動計算 | GET Orders(N) | totalAmount=704 (=504+200) |
| 明細不正 | B999 / quantity=0 | 400「書籍コード不存在: B999」「数量必须为大于 0 的整数」 |
| 承認 | POST approve (alice) | `{"ok":true,"status":"APPROVED"}`, approvedBy=alice, approvedAt 记录 |
| 未認証 | 匿名 approve | 401 |
| 二重承認 / REJECTED→approve | approve | 400「当前状态 …, 只有 OPEN 可承認」 |
| 承認後変更 | PATCH Orders / OrderItems | 400「已承認, 不可直接修改; 请先差戻し」/「明細不可变更」 |
| 変更 | OPEN ヘッダ PATCH note | 200, 状态・金额不变 |
| 却下 | rejectOrder 無理由 / 有理由 | 400「却下时必须填写理由」 / `{"ok":true,"status":"REJECTED"}` |
| 却下後修正 | PATCH 明細 quantity 3→5 | lineTotal 504→840, ヘッダ合計自動 1040 |
| 差戻し | sendBack(APPROVED) | `{"ok":true,"status":"OPEN"}`, approvedBy 清空 → 可再改・再承認 |
| 削除制御 | DELETE APPROVED / REJECTED / OPEN | APPROVED 400, REJECTED/OPEN 204 |
| 明細削除 | DELETE OrderItems | 204, ヘッダ合計自動再計算(例 1752→480→0) |
| 主データ | POST Books | 405「Entity … is read-only」 |
| 一覧 | GET + $filter=status eq 'APPROVED' | 只回 APPROVED 单 |

## 与课件/要件定義書的对应

| 要件(要件定義書) | 实现位置 |
|---|---|
| F-0100 受注登録(採番/默认状态/明細校验) | srv/order-service.js → before CREATE Orders |
| F-0200 承認(審批人/時間記録) | on approve |
| F-0300 変更(ヘッダ/明細/金额重算) | before UPDATE Orders·OrderItems + after 行 → recalcTotal |
| F-0400 却下・差戻し | on rejectOrder / on sendBack |
| マスタ連動(単価・书名快照) | bookMap() 补齐并快照 |
