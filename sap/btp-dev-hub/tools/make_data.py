#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
训练站测试数据生成器
  - 单点维护 products / categories / orders / customers
  - 产出 data/catalog、data/orders、data/customers 下的 .csv 与 .json (完全一致)
用法: python3 make_data.py   (在 tools/ 目录内执行)
"""
import csv, io, json, os, random
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.abspath(os.path.join(HERE, "..", "data"))

CATEGORIES = [
    ("C-ELEC", "电子设备", "笔记本 / 显示器 / 会议设备"),
    ("C-ACC",  "配件外设", "键鼠 / 扩展坞 / 线材"),
    ("C-FURN", "办公家具", "桌椅 / 照明"),
    ("C-NET",  "网络设备", "AP / 交换机 / 存储"),
]

CAT_NAME = {c[0]: c[1] for c in CATEGORIES}

# (id, name, desc, price, currency, category, stock, reorder)
PRODUCTS = [
    ("P-1001", "SAP 培训笔记本电脑 (ThinkPad X1)", "16G/512G 企业办公本", 8999.00, "CNY", "C-ELEC", 32, 10),
    ("P-1002", "27 寸 4K 显示器", "IPS 广色域, USB-C 反向供电", 2599.00, "CNY", "C-ELEC", 18, 5),
    ("P-1003", "无线机械键盘", "青轴, 蓝牙 5.0 双模", 459.00, "CNY", "C-ACC", 120, 20),
    ("P-1004", "人体工学椅", "全网布, 4D 扶手", 1899.00, "CNY", "C-FURN", 9, 5),
    ("P-1005", "升降办公桌", "140x70, 双电机", 3299.00, "CNY", "C-FURN", 6, 5),
    ("P-1006", "企业级无线 AP", "Wi-Fi 6E, 支持 128 终端", 1299.00, "CNY", "C-NET", 25, 8),
    ("P-1007", "千兆企业交换机", "24 口 PoE+, 网管型", 2380.00, "CNY", "C-NET", 14, 5),
    ("P-1008", "USB-C 扩展坞", "双 4K@60Hz, 千兆网口", 699.00, "CNY", "C-ACC", 60, 15),
    ("P-1009", "会议全向麦", "拾音半径 5 米, USB/蓝牙", 1599.00, "CNY", "C-ELEC", 11, 5),
    ("P-1010", "NAS 网络存储", "4 盘位, 支持 RAID5", 4599.00, "CNY", "C-NET", 4, 3),
    ("P-1011", "移动工作站 (P16)", "64G/2T, RTX 专业显卡", 21999.00, "CNY", "C-ELEC", 7, 3),
    ("P-1012", "便携投影仪", "1080P, 3000 流明", 3199.00, "CNY", "C-ELEC", 5, 3),
    ("P-1013", "防蓝光护眼灯", "色温可调, 自动感应", 349.00, "CNY", "C-FURN", 88, 20),
    ("P-1014", "白板套装 (磁性)", "90x150cm, 含支架", 899.00, "CNY", "C-FURN", 22, 8),
    ("P-1015", "视频会议终端", "一体机, 4K 摄像头", 6499.00, "CNY", "C-ELEC", 3, 2),
    ("P-1016", "USB 摄像头 4K", "自动对焦, 隐私盖", 799.00, "CNY", "C-ACC", 34, 10),
    ("P-1017", "企业固态硬盘 1TB", "NVMe, 加密型号", 1299.00, "CNY", "C-NET", 41, 10),
    ("P-1018", "网络配线架 24口", "六类非屏蔽", 219.00, "CNY", "C-NET", 17, 6),
    ("P-1019", "显示器支架臂", "气弹簧, 双屏可扩展", 429.00, "CNY", "C-FURN", 55, 12),
    ("P-1020", "会议预约屏", "10.1 寸触控, PoE 供电", 1899.00, "CNY", "C-ELEC", 12, 4),
    ("P-1021", "培训白板笔套装", "可擦, 12 支装", 59.00, "CNY", "C-ACC", 200, 40),
    ("P-1022", "UPS 不间断电源", "1500VA, 纯正弦波", 1799.00, "CNY", "C-NET", 8, 3),
    ("P-1023", "无线投屏器", "4K, HDMI 即插即用", 899.00, "CNY", "C-ACC", 26, 6),
    ("P-1024", "培训室音响套装", "2.1 声道, 含麦克风", 3599.00, "CNY", "C-ELEC", 6, 3),
    ("P-1025", "桌面收纳套件", "理线盒/集线槽", 129.00, "CNY", "C-FURN", 150, 30),
    ("P-1026", "签字板 (电子)", "用于培训签到", 749.00, "CNY", "C-ACC", 19, 5),
]

# 客户 (id, name, company, city, email)
CUSTOMERS = [
    ("CUST-01", "张伟", "上海华悦信息科技", "上海", "zhangwei@huayue.example.cn"),
    ("CUST-02", "李娜", "深圳蓝海软件", "深圳", "lina@blueocean.example.cn"),
    ("CUST-03", "王强", "北京中科数联", "北京", "wangqiang@zkd.example.cn"),
    ("CUST-04", "陈静", "杭州云帆数据", "杭州", "chenjing@yunfan.example.cn"),
    ("CUST-05", "刘洋", "广州星河网络", "广州", "liuyang@xinghe.example.cn"),
]

# 订单 (id, customer, date, 明细: product, qty)
ORDERS = [
    ("O-20260001", "CUST-01", "2026-08-03", [("P-1001", 2), ("P-1008", 5)]),
    ("O-20260002", "CUST-03", "2026-08-05", [("P-1006", 8), ("P-1007", 3), ("P-1017", 10)]),
    ("O-20260003", "CUST-02", "2026-08-08", [("P-1003", 20), ("P-1013", 15)]),
    ("O-20260004", "CUST-05", "2026-08-11", [("P-1004", 4), ("P-1005", 2), ("P-1014", 3)]),
    ("O-20260005", "CUST-04", "2026-08-14", [("P-1002", 6), ("P-1019", 10)]),
    ("O-20260006", "CUST-01", "2026-08-16", [("P-1009", 3), ("P-1015", 1), ("P-1024", 2)]),
    ("O-20260007", "CUST-03", "2026-08-19", [("P-1022", 4), ("P-1023", 6)]),
    ("O-20260008", "CUST-02", "2026-08-22", [("P-1012", 2), ("P-1021", 30)]),
]

def write_csv(folder, filename, header, rows):
    os.makedirs(os.path.join(DATA, folder), exist_ok=True)
    path = os.path.join(DATA, folder, filename)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(header)
        for r in rows:
            w.writerow(r)
    print("csv :", path)

def write_json(folder, filename, obj):
    os.makedirs(os.path.join(DATA, folder), exist_ok=True)
    path = os.path.join(DATA, folder, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    print("json:", path)

# ---------- catalog ----------
cat_rows = [(c[0], c[1], c[2]) for c in CATEGORIES]
write_csv("catalog", "categories.csv", ["ID", "name", "description"], cat_rows)
write_json("catalog", "categories.json",
           [OrderedDict(ID=c[0], name=c[1], description=c[2]) for c in CATEGORIES])

prod_rows = []
for pid, name, desc, price, cur, cat, stock, reorder in PRODUCTS:
    prod_rows.append([pid, name, desc, price, cur, cat, CAT_NAME[cat], stock, reorder,
                      "true" if stock > reorder else "false"])
write_csv("catalog", "products.csv",
          ["ID", "name", "description", "price", "currency", "category_ID",
           "categoryName", "stock", "reorderLevel", "isActive"],
          prod_rows)
products_json = []
for pid, name, desc, price, cur, cat, stock, reorder in PRODUCTS:
    products_json.append(OrderedDict([
        ("ID", pid), ("name", name), ("description", desc),
        ("price", price), ("currency", cur),
        ("category", OrderedDict([("ID", cat), ("name", CAT_NAME[cat])])),
        ("stock", stock), ("reorderLevel", reorder),
        ("isActive", stock > reorder),
        ("stockValue", round(price * stock, 2)),
    ]))
write_json("catalog", "products.json", products_json)

# ---------- customers ----------
cust_rows = [[c[0], c[1], c[2], c[3], c[4]] for c in CUSTOMERS]
write_csv("customers", "customers.csv", ["ID", "name", "company", "city", "email"], cust_rows)
write_json("customers", "customers.json",
           [OrderedDict(ID=c[0], name=c[1], company=c[2], city=c[3], email=c[4]) for c in CUSTOMERS])

# ---------- orders (含嵌套明细) ----------
price_of = {p[0]: p[3] for p in PRODUCTS}
orders_json = []
header_rows = []
item_rows = []
for oid, cid, date, items in ORDERS:
    details = []
    total = 0.0
    for pid, qty in items:
        unit = price_of[pid]
        line_total = round(unit * qty, 2)
        total += line_total
        details.append(OrderedDict([("product_ID", pid), ("productName", dict((p[0], p[1]) for p in PRODUCTS)[pid]),
                                    ("quantity", qty), ("unitPrice", unit), ("lineTotal", line_total)]))
        item_rows.append([oid, pid, dict((p[0], p[1]) for p in PRODUCTS)[pid], qty, unit, line_total])
    cust = dict((c[0], c[1]) for c in CUSTOMERS)[cid]
    header_rows.append([oid, cid, cust, date, round(total, 2)])
    orders_json.append(OrderedDict([
        ("ID", oid), ("customer_ID", cid), ("customerName", cust),
        ("orderDate", date), ("totalAmount", round(total, 2)),
        ("items", details),
    ]))
write_csv("orders", "orders.csv", ["ID", "customer_ID", "customerName", "orderDate", "totalAmount"], header_rows)
write_csv("orders", "order_items.csv",
          ["order_ID", "product_ID", "productName", "quantity", "unitPrice", "lineTotal"], item_rows)
write_json("orders", "orders.json", orders_json)
# OData V4 风格的集合响应示例
write_json("orders", "orders-odata-response.json",
           OrderedDict([("@odata.context", "https://example.com/odata/catalog/$metadata#Orders"),
                        ("value", orders_json)]))

print("\n生成完成 ->", DATA)
