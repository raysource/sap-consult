# テストケース / 测试用例（图书受注管理）

> 与要件定義書 Excel「テストケース」页同源(简版)。优先级: P1=必须 P2=重要 P3=可选。
> 本机实测输出见工程 README「本机实测输出」一节；回归可照此清单执行。

## 测试方针

- 单测: 状态机校验为主(命令行 curl 直接调用)
- 结合测试: 深创建(ヘッダ+明細) → 承認 → 変更 → 却下/差戻し 全链路
- 回归: 修改服务端校验逻辑后, 全量重跑本清单

## 功能用例

| No | 機能 | 操作 | 期待結果 | 优先级 |
|---|---|---|---|---|
| TC-01 | 受注登録(正常) | POST /Orders, 2 行明細, 不传受注番号/単価/书名 | 201; 服务端採番(SO+日期-序号); status=OPEN; 単価・书名从主数据补齐; 合計=Σ行金额 | P1 |
| TC-02 | 受注登録(数量不正) | 明細 quantity=0 | 400 中文错误, 不入库 | P1 |
| TC-03 | 受注登録(空明細) | items=[] | 400「至少需要一行明細」 | P1 |
| TC-04 | 受注登録(書籍不存在) | book_code 不存在 | 400「書籍コード不存在」 | P1 |
| TC-05 | 承認(正常) | POST approve(OPEN) | status=APPROVED; approvedBy/alice; approvedAt 写入 | P1 |
| TC-06 | 承認(重复/非法状态) | approve(APPROVED) / approve(REJECTED) | 400 提示当前状态不可承認 | P1 |
| TC-07 | 承認(匿名) | 不带 Basic Auth 调 approve | 401 | P2 |
| TC-08 | 変更(OPEN) | PATCH ヘッダ note | 200; 状态与金额不变 | P1 |
| TC-09 | 変更(APPROVED) | PATCH ヘッダ note | 400「已承認, 请先差戻し」 | P1 |
| TC-10 | 明細変更(OPEN) | PATCH OrderItems quantity | 200; lineTotal 与ヘッダ totalAmount 自动重算 | P1 |
| TC-11 | 明細追加/削除 | POST/DELETE OrderItems | 行号连续; 合計重算 | P2 |
| TC-12 | 却下(正常) | POST reject(reason 必填) | status=REJECTED; reason 记录 | P1 |
| TC-13 | 却下(无理由) | reject 不带 reason | 400「必须填写理由」 | P1 |
| TC-14 | 差戻し(完整变更流) | sendBack(APPROVED) → PATCH → 再 approve | APPROVED→OPEN(审计字段清空)→改→APPROVED | P1 |
| TC-15 | 删除 | DELETE OPEN 成功; DELETE APPROVED | OPEN/REJECTED 可删, APPROVED 400 | P2 |
| TC-16 | 主数据只读 | PATCH Books / Customers | 405 或 400(不可写) | P3 |
| TC-17 | 一覧 | GET Orders + $expand=items + $filter=status | 数据完整; 快照列 bookTitle 存在 | P2 |

## 状态机用例(矩阵)

| 現状態 | イベント | 次状態 | 許可 | 禁止理由 |
|---|---|---|---|---|
| OPEN | approve | APPROVED | 承認者 | — |
| OPEN | reject(reason) | REJECTED | 承認者 | 理由必須 |
| OPEN | PATCH / 行增改删 / DELETE | OPEN | 営業 | — |
| APPROVED | sendBack | OPEN | 管理者 | 承認後変更は差戻し経由 |
| APPROVED | PATCH / DELETE / reject | — | 禁止 | 400 |
| REJECTED | PATCH / 行增改删 / DELETE | REJECTED | 営業 | 修正后再提交 |
| REJECTED | approve | — | 禁止(需先修正) | 400 |
