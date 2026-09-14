# -*- coding: utf-8 -*-
"""生成课程 Excel（每个模块一份 + 一份全模块总览）。

    python3 tools/make_xlsx.py              # 全部（已生成的模块）
    python3 tools/make_xlsx.py mm           # 只生成 MM

每模块工作簿：<CODE>_课程大纲_学习WBS.xlsx
  0_说明      这份 Excel 是什么、怎么用、数据来源
  1_课程大纲  14 页 × 这页讲什么（小节标题从生成好的 HTML 里读）× 截图数
  2_学习WBS   配置篇的每个任务一行（组 / 任务号 / 标题 / IMG 路径 / 手顺步骤 / 要点 / 进度）
  3_实训记录  五个实训要交的号码与分录（打印后可手写）
  4_截图索引  页面里引用的每一张真实截图（页面 / 任务 / 原文件名）
  5_术语表    中英对照
  6_Tcode速查 教材出现的事务码 + 常用补充
  7_自绘图    本模块的 SVG 清单

总览工作簿：SAP全模块_课程总览_学习WBS.xlsx
  0_说明 / 1_模块总览 / 2_课程结构对照 / 3_全部任务索引

内容全部从「生成好的 HTML」与 sitegen 数据里读，不手抄 —— 改页面后重跑即可同步。
"""
import importlib
import io
import os
import re
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(HERE, "sitegen"))

import common  # noqa: E402
from common import MODULES, SLOTS  # noqa: E402

HEAD_FILL = PatternFill("solid", fgColor="0A6ED1")
SUB_FILL = PatternFill("solid", fgColor="E3F0FA")
HEAD_FONT = Font(name="微软雅黑", size=10, bold=True, color="FFFFFF")
SUB_FONT = Font(name="微软雅黑", size=10, bold=True, color="0854A0")
CELL_FONT = Font(name="微软雅黑", size=10)
MONO_FONT = Font(name="Consolas", size=9.5)
TITLE_FONT = Font(name="微软雅黑", size=13, bold=True, color="0854A0")
THIN = Side(style="thin", color="D9E1E8")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP = Alignment(vertical="top", wrap_text=True)
TOP = Alignment(vertical="top")


def ws_new(wb, title, widths, first=False):
    ws = wb.active if first else wb.create_sheet()
    ws.title = title
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.sheet_view.showGridLines = False
    return ws


def head(ws, row, cols):
    for i, c in enumerate(cols, 1):
        cell = ws.cell(row=row, column=i, value=c)
        cell.fill = HEAD_FILL
        cell.font = HEAD_FONT
        cell.alignment = Alignment(vertical="center", wrap_text=True)
        cell.border = BORDER
    ws.row_dimensions[row].height = 22
    return row + 1


def put(ws, row, values, mono_cols=(), wrap_cols=()):
    for i, v in enumerate(values, 1):
        cell = ws.cell(row=row, column=i, value=v)
        cell.font = MONO_FONT if i in mono_cols else CELL_FONT
        cell.alignment = WRAP if i in wrap_cols else TOP
        cell.border = BORDER
    return row + 1


def sub(ws, row, text, span):
    cell = ws.cell(row=row, column=1, value=text)
    cell.fill = SUB_FILL
    cell.font = SUB_FONT
    for i in range(2, span + 1):
        ws.cell(row=row, column=i).fill = SUB_FILL
    row += 1
    return row


def title_block(ws, lines, span):
    row = 1
    for i, (txt, font) in enumerate(lines):
        cell = ws.cell(row=row, column=1, value=txt)
        cell.font = font
        row += 1
    return row + 1


# --------------------------------------------------------------------------
def parse_page(path):
    """从生成的 HTML 里读小节标题与截图数（Excel 与页面因此不会脱节）。"""
    raw = io.open(path, encoding="utf-8").read()
    raw = raw.split("<article>", 1)[-1]
    heads = [(m.group(1), re.sub(r"<[^>]+>", "", m.group(2)).strip())
             for m in re.finditer(r'<h([23])[^>]*>(.*?)</h\1>', raw, re.S)]
    shots = len(re.findall(r'<figure class="shot', raw))
    dias = len(re.findall(r'<figure class="dia', raw))
    return heads, shots, dias


def shots_on_page(path):
    raw = io.open(path, encoding="utf-8").read()
    return re.findall(r'src="\.\./assets/img/([^"]+)"', raw)


def build_module_xlsx(code):
    pack = importlib.import_module("pack_%s" % code)
    ctx = common.Ctx(code)
    meta = common.BY_CODE[code]
    mdir = os.path.join(ROOT, code)
    wb = Workbook()

    # 0_说明 -----------------------------------------------------------------
    ws = ws_new(wb, "0_说明", [22, 100], first=True)
    row = title_block(ws, [("%s 培训课程 —— 课程大纲与学习 WBS" % meta["site_title"], TITLE_FONT),
                           ("本工作簿由 tools/make_xlsx.py 从生成好的 HTML 与课程包数据自动导出，"
                            "页面改了重跑即可同步。", CELL_FONT)], 2)
    rows = [
        ("这是什么", "SAP %s 培训课程（%d 页静态站点，离线可开）的配套 Excel："
                     "课程大纲、配置任务 WBS、实训记录表、截图索引、术语与 T-code。" % (meta["brand"], 14)),
        ("怎么用", "① 备课：看 1_课程大纲 与 2_学习WBS，按任务号排课；"
                   "② 上课：学员用 3_实训记录 记单据号与分录（可打印）；"
                   "③ 查证：4_截图索引 里的每张图都能回教材《S4.docx》原稿核对。"),
        ("素材来源", "教材文档《S4.docx》（425 页、内嵌 1385 张图）的 %s 模块："
                     "%d 个任务 / %d 个手顺步骤 / %d 张真实截图（中文界面 SAP GUI）。"
                     % (meta["name_en"], len(ctx.tasks), sum(len(t["steps"]) for t in ctx.tasks),
                        len(set(k for k in common.MANIFEST if k.startswith(code + "/"))))),
        ("场景值", "公司代码 C999 / 工厂 P999 / 采购组织 Y999 等教材环境值；"
                   "换环境请按页面标注的方法（F1 字段帮助、F4 取值列表、IMG 路径、表名）核对。"),
        ("页面清单", "、".join(p["file"] for p in pack.PAGES)),
        ("重新生成", "cd sap_modules_cn && python3 tools/build_pages.py %s && python3 tools/make_xlsx.py %s"
                     % (code, code)),
    ]
    for k, v in rows:
        c1 = ws.cell(row=row, column=1, value=k)
        c1.font = SUB_FONT
        c1.alignment = TOP
        c1.border = BORDER
        c2 = ws.cell(row=row, column=2, value=v)
        c2.font = CELL_FONT
        c2.alignment = WRAP
        c2.border = BORDER
        ws.row_dimensions[row].height = 34
        row += 1

    # 1_课程大纲 -------------------------------------------------------------
    ws = ws_new(wb, "1_课程大纲", [6, 16, 26, 34, 60, 10, 8])
    row = head(ws, 1, ["#", "导航", "页面标题", "这页的定位（kicker）", "页内小节", "截图", "自绘图"])
    for i, pg in enumerate(pack.PAGES, 1):
        p = os.path.join(mdir, pg["file"])
        heads, shots, dias = parse_page(p)
        secs = " ／ ".join(("H%s %s" % (h, t)) for h, t in heads)
        row = put(ws, row, [i, common.SLOT_LABEL.get(pg["slot"], ""), pg["title"], pg["kicker"],
                            secs, shots, dias], wrap_cols=(4, 5))

    # 2_学习WBS --------------------------------------------------------------
    ws = ws_new(wb, "2_学习WBS", [4, 8, 26, 54, 8, 12, 46, 8])
    notes = getattr(pack, "CONFIG_NOTES", {})
    row = title_block(ws, [("学习 WBS —— 配置篇 %d 个任务（按组）" % len(ctx.tasks), TITLE_FONT)], 8)
    head_row = row
    row = head(ws, row, ["#", "组", "任务", "教材 IMG 路径 / 前台路径", "步骤", "事务码",
                         "一句话要点", "进度"])
    r = 0
    gidx = 0
    for gtitle, nos, blurb in getattr(pack, "CONFIG_GROUPS", []):
        gidx += 1
        row = sub(ws, row, "%s —— %s（%d 个任务）" % (gtitle, blurb, len(nos)), 8)
        for no in nos:
            t = ctx.task(no)
            r += 1
            gcode = gtitle.split(" ")[0] if re.match(r"^[A-Z][ .、]?", gtitle) else str(gidx)
            row = put(ws, row, [r, gcode,
                                "%02d %s" % (no, t["title"]), t.get("path") or "（前台操作，无 IMG 路径）",
                                len(t["steps"]), ", ".join(t.get("tcodes") or []) or "—",
                                notes.get(no, ""), ""],
                      mono_cols=(4,), wrap_cols=(4, 7))
    ws.cell(row=row + 1, column=3, value="合计").font = SUB_FONT
    ws.cell(row=row + 1, column=4, value="%d 个任务 / %d 个手顺步骤"
            % (len(ctx.tasks), sum(len(t["steps"]) for t in ctx.tasks))).font = SUB_FONT
    ws.cell(row=row + 2, column=4,
            value='已完成数（在「进度」列打 √ 后自动统计）：=COUNTIF(H%d:H%d,"√")'
                  % (head_row + 1, row - 1)).font = SUB_FONT
    ws.freeze_panes = "A%d" % (head_row + 1)

    # 3_实训记录 -------------------------------------------------------------
    ws = ws_new(wb, "3_实训记录", [26, 30, 30, 40])
    row = title_block(ws, [("实训记录表（打印后手写；单据号是「真的跑过」的证据）", TITLE_FONT)], 4)
    row = head(ws, row, ["记录项", "教材场景值", "你的系统", "说明 / 检查点"])
    items = [
        ("公司代码 / 工厂 / 库存地点", "C999 / P999 / 0001·0002·0003", "", "组织数据决定后面一切"),
        ("采购组织 / 采购组 / MRP 控制者", "Y999 / PG1·PG2 / 001·002", "", "决定订单归属与计划责任"),
        ("评估分组代码 / 评估类", "CN01 / 3000·3100·7920", "", "决定存货科目（BSX）"),
        ("物料号（原材料 / 产成品）", "R999-100 罩壳… / FERT", "", "关键字段：物料组、MRP 类型、评估类、价格控制"),
        ("供应商号 + 采购组织数据", "10000000 红星轴承厂", "", "MK01 维护"),
        ("采购信息记录（净价 / 数量 / 交期）", "管轴 50 件 / 1700 元 / 3 天", "", "ME11；订单价格从这里来"),
        ("采购申请号（ME51N）", "", "", "记下号码；ME5A 可查"),
        ("采购订单号（ME21N）", "", "", "参照请购创建；看订单历史"),
        ("物料凭证号（MIGO 101 收货）", "", "", "库存增加；库位要选对"),
        ("会计凭证号（收货）", "", "", "借：存货 / 贷：GR-IR"),
        ("发票号（MIRO）", "", "", "余额归零即匹配"),
        ("差异 / 容差码（如触发冻结）", "", "", "MRBR 看冻结原因"),
        ("发票校验的会计凭证借贷方", "借 GR-IR / 贷 应付账款", "", "抄下科目号与金额"),
        ("库存总览结果（MMBE）", "", "", "非限制库存是 MRP 用的那一列"),
    ]
    for it in items:
        row = put(ws, row, list(it), wrap_cols=(4,))

    # 4_截图索引 -------------------------------------------------------------
    ws = ws_new(wb, "4_截图索引", [6, 18, 10, 44, 10, 52])
    row = head(ws, 1, ["#", "页面", "任务", "assets/img 下的路径", "尺寸", "教材原图文件名"])
    n = 0
    for pg in pack.PAGES:
        p = os.path.join(mdir, pg["file"])
        for key in shots_on_page(p):
            m = common.MANIFEST.get(key)
            if not m:
                continue
            n += 1
            row = put(ws, row, [n, pg["file"], m.get("task") or "—", key,
                                "%sx%s" % (m["w"], m["h"]), m["orig"]], mono_cols=(4,))

    # 5_术语表 ---------------------------------------------------------------
    gl = getattr(pack, "GLOSSARY", [])
    ws = ws_new(wb, "5_术语表", [6, 22, 34, 60])
    row = head(ws, 1, ["#", "中文", "English / SAP 名称", "说明"])
    for i, (cn, en, note) in enumerate(gl, 1):
        row = put(ws, row, [i, cn, en, note], wrap_cols=(4,))

    # 6_Tcode速查 ------------------------------------------------------------
    ws = ws_new(wb, "6_Tcode速查", [8, 20, 40, 16])
    row = head(ws, 1, ["#", "T-code", "用途 / 教材任务", "类型"])
    i = 0
    seen = set()
    for t in ctx.tasks:
        for c in (t.get("tcodes") or []):
            i += 1
            seen.add(c)
            row = put(ws, row, [i, c, "教材任务 %02d %s" % (t["no"], t["title"]), "教材"],
                      mono_cols=(2,))
    for c, desc in getattr(pack, "TCODES_EXTRA", []):
        if c.split("/")[0] in seen:
            continue
        i += 1
        row = put(ws, row, [i, c, desc, "补充（项目常用）"], mono_cols=(2,))

    # 7_自绘图 ---------------------------------------------------------------
    ws = ws_new(wb, "7_自绘图", [6, 26, 12, 70])
    row = head(ws, 1, ["#", "文件", "类型", "标题 / 用途"])
    for i, d in enumerate(getattr(pack, "DIAGRAMS", []), 1):
        row = put(ws, row, [i, "assets/diagrams/%s/%s" % (code, d["file"]), d["kind"], d["title"]],
                  mono_cols=(2,), wrap_cols=(4,))

    out = os.path.join(ROOT, "%s_课程大纲_学习WBS.xlsx" % code.upper())
    wb.save(out)
    return out


def build_overview_xlsx(codes):
    wb = Workbook()
    ws = ws_new(wb, "0_说明", [22, 100], first=True)
    title_block(ws, [("SAP 全模块培训课程 —— 总览", TITLE_FONT),
                     ("四个模块（MM / PP / FI / CO）共用一套教学结构：概念 → 组织 → 主数据 → 流程 → "
                      "分步操作手顺 → SPRO 配置 → 实训 → 自测。", CELL_FONT)], 2)
    row = 4
    for k, v in [("站点入口", "index.html（总览页）→ <模块>/index.html"),
                 ("每模块页数", "14 页（含三篇流程详解与配置篇）"),
                 ("素材", "教材文档《S4.docx》的真实 SAP GUI 截图（中文界面），保留原图文件名可回查"),
                 ("模块工作簿", "、".join("%s_课程大纲_学习WBS.xlsx" % c.upper() for c in codes))]:
        c1 = ws.cell(row=row, column=1, value=k)
        c1.font = SUB_FONT
        c2 = ws.cell(row=row, column=2, value=v)
        c2.font = CELL_FONT
        c2.alignment = WRAP
        row += 1

    ws = ws_new(wb, "1_模块总览", [10, 18, 22, 10, 10, 10, 12, 10, 10, 60])
    row = head(ws, 1, ["模块", "中文名", "English", "页数", "教材任务", "手顺步骤", "截图引用",
                       "自绘图", "自测", "这模块管什么"])
    for code in codes:
        pack = importlib.import_module("pack_%s" % code)
        ctx = common.Ctx(code)
        mdir = os.path.join(ROOT, code)
        shots = sum(len(shots_on_page(os.path.join(mdir, p["file"]))) for p in pack.PAGES)
        quiz = len(re.findall(r'class="quiz-q"',
                              io.open(os.path.join(mdir, "quiz.html"), encoding="utf-8").read()))
        row = put(ws, row, [code.upper(), common.BY_CODE[code]["name_cn"],
                            common.BY_CODE[code]["name_en"], len(pack.PAGES), len(ctx.tasks),
                            sum(len(t["steps"]) for t in ctx.tasks), shots,
                            len(getattr(pack, "DIAGRAMS", [])), quiz,
                            common.BY_CODE[code]["hub_line"]], wrap_cols=(10,))

    ws = ws_new(wb, "2_课程结构对照", [6, 16, 30, 90])
    row = head(ws, 1, ["#", "导航", "页面", "内容要求"])
    desc = {
        "index": "课程地图、学习路线、规模统计、教材场景值",
        "concept": "这个东西管什么、产出什么凭证、与邻居模块的分界、常见误解",
        "org": "组织结构与分配关系（先给数据定坐标）",
        "master": "主数据的分层、关键字段、填错的后果",
        "flow": "端到端流程、单据流、记账影响、顺序错误",
        "proc1": "流程①②③：局部操作详解（含教材任务逐屏走查）",
        "config": "SPRO 配置路线：教材全部任务（IMG 路径 + 手顺 + 原始画面）",
        "practice": "五个实训任务与完成基准",
        "instructor": "课时分配、板书路线、必问 12 题、评分标准",
        "worksheet": "学员记入表（可打印）",
        "quiz": "30 题自测（合格 75%）",
        "glossary": "术语中英对照、T-code 速查、常用表",
    }
    for i, slot in enumerate(SLOTS, 1):
        row = put(ws, row, [i, common.SLOT_LABEL.get(slot, slot), slot,
                            desc.get(slot, "")], wrap_cols=(4,))

    ws = ws_new(wb, "3_全部任务索引", [8, 8, 26, 60, 10, 14, 40])
    row = head(ws, 1, ["模块", "任务号", "任务标题", "IMG 路径 / 前台路径", "步骤数", "事务码", "一句话要点"])
    for code in codes:
        pack = importlib.import_module("pack_%s" % code)
        ctx = common.Ctx(code)
        notes = getattr(pack, "CONFIG_NOTES", {})
        for t in ctx.tasks:
            row = put(ws, row, [code.upper(), t["no"], t["title"],
                                t.get("path") or "（前台操作）", len(t["steps"]),
                                ", ".join(t.get("tcodes") or []) or "—", notes.get(t["no"], "")],
                      mono_cols=(4,), wrap_cols=(4, 7))
    out = os.path.join(ROOT, "SAP全模块_课程总览_学习WBS.xlsx")
    wb.save(out)
    return out


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("-")]
    codes = []
    for m in MODULES:
        path = os.path.join(HERE, "sitegen", "pack_%s.py" % m["code"])
        if os.path.exists(path) and (not args or m["code"] in args):
            codes.append(m["code"])
    if not codes:
        print("没有可导出的模块（先写 pack_<code>.py）")
        return 1
    for c in codes:
        print("OK", os.path.relpath(build_module_xlsx(c), ROOT))
    print("OK", os.path.relpath(build_overview_xlsx(codes), ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
