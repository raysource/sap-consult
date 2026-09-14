# -*- coding: utf-8 -*-
"""SVG 图元与通用图表构建器（纯 Python → SVG，无外部依赖、离线可用）。

为什么手写 SVG：站点要求 file:// 直接可开、不联网、不依赖 CDN 字体；同时文字宽度必须
按 CJK 全角 1.0em 估算，否则中文会溢出方框（这条在别的站踩过）。

模块包只提供「图的数据」（dict），排版全部由这里的 7 个构建器负责：
  mindmap  心智地图：中心 + 左右分支卡
  layers   分层结构图：一层一条带，带内若干方框（组织/主数据/字段状态…）
  flow     流程链：一行一步，自动折行
  tree     组织树：多层节点 + 父子连线
  swimlane 泳道图：行 = 角色/系统，列 = 步骤
  star     集成关系图：中心模块 + 四周邻居，双向箭头各带标签
  chains   决定链/规则卡：标题 + 横向链 + 说明行
校验：build() 会检查每段文字是否超出它所在的方框（CLAIMS 登记），并做 XML 合法性检查。
"""
import math
import re
import unicodedata
import xml.etree.ElementTree as ET

# ---------------------------------------------------------------- 调色板
BLUE, BLUE_D, BLUE_L = "#0a6ed1", "#0854a0", "#e3f0fa"
TEAL, TEAL_B = "#007272", "#e6f2f2"
AMBER, AMBER_B = "#8d6e00", "#fdf3d7"
GREEN, GREEN_B = "#177245", "#e6f2ec"
RED, RED_B = "#b3261e", "#fdeae9"
PURPLE, PURPLE_B = "#5b3fa8", "#efeaf9"
INK, INK2, MUTED, LINE = "#1d2d3e", "#354a5f", "#6b7a8d", "#d9e1e8"
FONT = "'PingFang SC','Hiragino Sans GB','Noto Sans CJK SC','Microsoft YaHei',sans-serif"
MONO = "'SF Mono',Menlo,Consolas,monospace"

NAMES = {"blue": (BLUE, BLUE_L), "teal": (TEAL, TEAL_B), "amber": (AMBER, AMBER_B),
         "green": (GREEN, GREEN_B), "red": (RED, RED_B), "purple": (PURPLE, PURPLE_B),
         "gray": (MUTED, "#f2f5f8")}


def color(name):
    return NAMES.get(name or "blue", (BLUE, BLUE_L))


# ---------------------------------------------------------------- 文本度量
def char_w(ch):
    if unicodedata.east_asian_width(ch) in ("W", "F"):
        return 1.0
    if ch in "iljI.,:;'|! ":
        return 0.32
    if ch in "mMW@":
        return 0.9
    return 0.575


def text_w(s, size):
    return sum(char_w(c) for c in s) * size


def wrap(s, size, maxw, max_lines=None):
    s = str(s)
    if "\n" in s:
        out = []
        for part in s.split("\n"):
            out.extend(wrap(part, size, maxw))
        if max_lines and len(out) > max_lines:
            out = out[:max_lines]
            out[-1] = out[-1][: max(1, len(out[-1]) - 1)] + "…"
        return out
    words, cur, lines = [], "", []
    for ch in s:
        if ch == " ":
            words.append(cur)
            words.append(" ")
            cur = ""
        else:
            cur += ch
    words.append(cur)
    line = ""
    for w in words:
        if text_w(line + w, size) <= maxw:
            line += w
        else:
            if line:
                lines.append(line.rstrip())
            while text_w(w, size) > maxw and len(w) > 1:
                k = 1
                while k < len(w) and text_w(w[: k + 1], size) <= maxw:
                    k += 1
                lines.append(w[:k])
                w = w[k:]
            line = w
    if line.strip():
        lines.append(line.rstrip())
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1][: max(1, len(lines[-1]) - 1)] + "…"
    return lines


# ---------------------------------------------------------------- 溢出登记
CLAIMS = []


def claim(x_left, x_right, s, size, where=""):
    w = text_w(s, size)
    if x_left + w > x_right + 0.5:
        CLAIMS.append((where, s, round(x_left + w - x_right, 1)))


def wclaim(x, xmax, s, size, max_lines=None, where=""):
    """折行 + 登记：返回所有行（每行都已核对不会超出 xmax）。"""
    lines = wrap(s, size, xmax - x)
    for ln in lines:
        claim(x, xmax, ln, size, where)
    return lines


# ---------------------------------------------------------------- SVG 原语
def svg_open(w, h, title):
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" '
        'role="img" aria-label="%s" font-family="%s">\n'
        '<title>%s</title>\n'
        '<defs>'
        '<marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        '<path d="M0,0 L10,5 L0,10 z" fill="%s"/></marker>'
        '<marker id="ar2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        '<path d="M0,0 L10,5 L0,10 z" fill="%s"/></marker>'
        '<marker id="arw" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        '<path d="M0,0 L10,5 L0,10 z" fill="#ffffff"/></marker>'
        '<marker id="arback" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        '<path d="M10,0 L0,5 L10,10 z" fill="%s"/></marker>'
        '</defs>\n<rect width="%d" height="%d" fill="#ffffff"/>\n'
    ) % (w, h, w, h, title, FONT, title, BLUE, TEAL, RED, w, h)


def t(x, y, s, size=13.0, fill=INK, anchor="start", weight="400", family=None, opacity=None):
    s = str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    fam = ' font-family="%s"' % family if family else ""
    op = ' opacity="%s"' % opacity if opacity else ""
    return ('<text x="%.1f" y="%.1f" font-size="%s" fill="%s" text-anchor="%s" '
            'font-weight="%s"%s%s>%s</text>\n') % (x, y, size, fill, anchor, weight, fam, op, s)


def rect(x, y, w, h, fill="#ffffff", stroke=LINE, rx=8, sw=1.4, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    return ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" fill="%s" '
            'stroke="%s" stroke-width="%s"%s/>\n') % (x, y, w, h, rx, fill, stroke, sw, d)


def line(x1, y1, x2, y2, stroke=MUTED, sw=1.4, dash=None, marker=None, marker_back=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    m = ' marker-end="url(#%s)"' % marker if marker else ""
    mb = ' marker-start="url(#%s)"' % marker_back if marker_back else ""
    return ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s%s%s/>\n'
            ) % (x1, y1, x2, y2, stroke, sw, d, m, mb)


def path(d, stroke=MUTED, sw=1.6, fill="none", dash=None, marker=None):
    da = ' stroke-dasharray="%s"' % dash if dash else ""
    m = ' marker-end="url(#%s)"' % marker if marker else ""
    return '<path d="%s" fill="%s" stroke="%s" stroke-width="%s"%s%s/>\n' % (d, fill, stroke, sw, da, m)


def badge(cx, cy, label, fill=BLUE, r=11, size=12, tcolor="#ffffff"):
    return ('<circle cx="%.1f" cy="%.1f" r="%s" fill="%s"/>' % (cx, cy, r, fill)
            + t(cx, cy + 4.3, label, size, tcolor, "middle", "700"))


def title_bar(x, y, w, main, sub=None, size=22):
    out = [t(x, y, main, size, INK, weight="700")]
    if sub:
        for i, ln in enumerate(wclaim(x, x + w, sub, 13, where="header:" + sub)):
            out.append(t(x, y + 24 + i * 18, ln, 13, MUTED))
    return "".join(out), y + 24 + (24 * (1 + len(wrap(sub or "", 13, w)) - 1) if sub else 0)


def note_bar(x, y, w, text, fill=BLUE_L, stroke=BLUE, size=12.5):
    lines = wclaim(x + 12, x + w - 12, text, size, where="note")
    h = 16 + len(lines) * (size + 6)
    out = [rect(x, y, w, h, fill, stroke, 8, 1.2)]
    cy = y + 22
    for ln in lines:
        out.append(t(x + 12, cy, ln, size, BLUE_D if stroke == BLUE else INK2))
        cy += size + 6
    return "".join(out), y + h


def panel(x, y, w, title, lines, accent=BLUE, bg="#ffffff", title_size=15, size=12):
    """标题 + 多行说明的圆角卡，高度自适应。返回 (svg, y_bottom)。"""
    pad = 14
    ls = []
    for ln in lines:
        ls.extend(wclaim(x + pad, x + w - pad, ln, size, where="panel:" + title))
    h = 30 + len(ls) * (size + 6) + 12
    out = [rect(x, y, w, h, bg, accent, 9)]
    out.append(rect(x, y, 4.5, h, accent, accent, rx=2))
    claim(x + pad, x + w - pad, title, title_size, where="panel-title")
    out.append(t(x + pad, y + 24, title, title_size, accent, weight="700"))
    cy = y + 24 + 20
    for ln in ls:
        out.append(t(x + pad, cy, ln, size, INK2))
        cy += size + 6
    return "".join(out), y + h


def chip_rows(x, y, w, items, accent=BLUE, size=11.5, per_row=None, gap=8, h=30):
    """一排小胶囊（比如一条流程链）。自动折行，返回 (svg, y_bottom)。"""
    out = []
    cw = x
    row_y = y
    for it in items:
        tw = text_w(it, size) + 22
        if cw + tw > x + w and cw > x:
            cw, row_y = x, row_y + h + gap
        claim(cw + 10, cw + tw - 10, it, size, where="chip")
        out.append(rect(cw, row_y, tw, h - 8, "#ffffff", accent, 8, 1.2))
        out.append(t(cw + 11, row_y + 15.5, it, size, INK2))
        nx = cw + tw + 16
        if nx < x + w:
            out.append(path("M %.0f %.0f h 12" % (cw + tw + 1, row_y + 11), stroke=accent, sw=1.3, marker="ar"))
        cw = nx
    return "".join(out), row_y + h


# ---------------------------------------------------------------- 构建器
def build_mindmap(spec):
    """心智地图：中心 + 左右分支卡（每张卡：标题 + 若干要点行）。"""
    W = spec.get("w", 1420)
    s = [svg_open(W, 100, spec["title"])]
    s.append(t(40, 46, spec["title"], 22, INK, weight="700"))
    s.append(t(40, 72, spec.get("sub", ""), 12.5, MUTED))

    branches = spec["branches"]
    left = [b for b in branches if b.get("side", "L") == "L"]
    right = [b for b in branches if b.get("side", "L") == "R"]
    CW = spec.get("card_w", 470)
    GAPY = 18
    top = 108

    def col(items, cx):
        out, y = [], top
        for b in items:
            acc, bg = color(b.get("color"))
            lines = []
            for ln in b["leaves"]:
                lines.append(ln)
            svg, yb = panel(cx, y, CW, b["title"], lines, acc, bg, title_size=15, size=12)
            out.append(svg)
            y = yb + GAPY
        return "".join(out), y

    lx, rx = 40, W - 40 - CW
    lsvg, ly = col(left, lx)
    rsvg, ry = col(right, rx)
    body_top = top
    body_bottom = max(ly, ry) - GAPY

    cw, ch = spec.get("center_w", 300), spec.get("center_h", 168)
    ccx = W / 2.0
    ccy = (body_top + body_bottom) / 2.0
    center = [
        rect(ccx - cw / 2.0, ccy - ch / 2.0, cw, ch, BLUE_D, BLUE_D, 16),
        t(ccx, ccy - ch / 2.0 + 42, spec["center_title"], 30, "#ffffff", "middle", "700"),
        t(ccx, ccy - ch / 2.0 + 74, spec.get("center_sub", ""), 17, "#dbeafd", "middle"),
        t(ccx, ccy - ch / 2.0 + 102, spec.get("center_en", ""), 12, "#a9cdf3", "middle", family=MONO),
        t(ccx, ccy - ch / 2.0 + 130, spec.get("center_note", ""), 11.5, "#a9cdf3", "middle"),
    ]
    # 连线：从中心到每张卡的左/右中心
    links = []
    y = top
    for b in left:
        h = 0
        for ln in b["leaves"]:
            h += len(wrap(ln, 12, CW - 28))
        cardh = 30 + h * 18 + 12
        lyc = y + cardh / 2.0
        links.append(path("M %.0f %.0f C %.0f %.0f, %.0f %.0f, %.0f %.0f"
                          % (ccx - cw / 2.0, ccy, ccx - cw / 2.0 - 60, ccy, lx + CW + 60, lyc, lx + CW + 2, lyc),
                          stroke=color(b.get("color"))[0], sw=2))
        y += cardh + GAPY
    y = top
    for b in right:
        h = 0
        for ln in b["leaves"]:
            h += len(wrap(ln, 12, CW - 28))
        cardh = 30 + h * 18 + 12
        lyc = y + cardh / 2.0
        links.append(path("M %.0f %.0f C %.0f %.0f, %.0f %.0f, %.0f %.0f"
                          % (ccx + cw / 2.0, ccy, ccx + cw / 2.0 + 60, ccy, rx - 60, lyc, rx - 2, lyc),
                          stroke=color(b.get("color"))[0], sw=2))
        y += cardh + GAPY

    s.append("".join(links))
    s.append(lsvg)
    s.append(rsvg)
    s.append("".join(center))
    H = int(max(ly, ry) + 26)
    s.append("</svg>\n")
    return H, "".join(s)


def build_layers(spec):
    """分层结构图：一层 = 一条带（标题 + 方框若干 + 可选说明）。"""
    W = spec.get("w", 1280)
    s = [svg_open(W, 100, spec["title"])]
    s.append(t(40, 46, spec["title"], 22, INK, weight="700"))
    s.append(t(40, 72, spec.get("sub", ""), 12.5, MUTED))
    y = 104
    band_pad = 18
    for band in spec["bands"]:
        acc, bg = color(band.get("color"))
        boxes = band["boxes"]
        per_row = band.get("per_row", len(boxes))
        bw = (W - 80 - 2 * band_pad - (per_row - 1) * 14) / float(per_row)
        rows = [boxes[i:i + per_row] for i in range(0, len(boxes), per_row)]
        row_h = []
        for row in rows:
            hmax = 0
            for b in row:
                item = b if isinstance(b, dict) else {"t": b}
                lines = item.get("lines") or []
                n = 0
                for ln in lines:
                    n += len(wrap(ln, 11.5, bw - 24))
                hmax = max(hmax, 30 + n * 17 + 12)
            row_h.append(hmax)
        band_h = 44 + sum(row_h) + (len(rows) - 1) * 12 + 14
        s.append(rect(40, y, W - 80, band_h, bg, acc, 12, 1.2))
        claim(40 + band_pad, W - 40 - band_pad, band["title"], 15.5, where="band")
        s.append(t(40 + band_pad, y + 28, band["title"], 15.5, acc, weight="700"))
        if band.get("note"):
            for i, ln in enumerate(wclaim(40 + band_pad + text_w(band["title"], 15.5) + 16,
                                          W - 40 - band_pad, band["note"], 12, where="bandnote")):
                s.append(t(40 + band_pad + text_w(band["title"], 15.5) + 16, y + 28 + i * 16, ln, 12, MUTED))
        cy = y + 46
        for r, row in enumerate(rows):
            for i, b in enumerate(row):
                item = b if isinstance(b, dict) else {"t": b}
                bx = 40 + band_pad + i * (bw + 14)
                bh = row_h[r]
                s.append(rect(bx, cy, bw, bh, "#ffffff", acc, 8, 1.2))
                claim(bx + 12, bx + bw - 12, item["t"], 13.5, where="box")
                s.append(t(bx + 12, cy + 21, item["t"], 13.5, acc, weight="700"))
                ly = cy + 38
                for ln in item.get("lines") or []:
                    for seg in wclaim(bx + 12, bx + bw - 12, ln, 11.5, where="boxline"):
                        s.append(t(bx + 12, ly, seg, 11.5, INK2))
                        ly += 17
            cy += row_h[r] + 12
        y += band_h + 16
    H = int(y + 8)
    s.append("</svg>\n")
    return H, "".join(s)


def build_flow(spec):
    """流程链：一行一步（每步 = 标签 + 小字），超出宽度自动折行并画折返箭头。"""
    W = spec.get("w", 1280)
    s = [svg_open(W, 100, spec["title"])]
    s.append(t(40, 46, spec["title"], 22, INK, weight="700"))
    if spec.get("sub"):
        s.append(t(40, 72, spec["sub"], 12.5, MUTED))
    x, y = 40, 104
    avail = W - 80
    steps = spec["steps"]
    size = 13.0
    widths = [max(text_w(st["t"], size) + (62 if st.get("no") else 42), 150) for st in steps]
    pos, cx_, cy_, rows = [], x, y, 1
    rowh = 96
    for i, wd in enumerate(widths):
        if cx_ + wd > x + avail and cx_ > x:
            cx_, cy_, rows = x, cy_ + rowh, rows + 1
        pos.append((cx_, cy_, wd))
        cx_ += wd + 30
    for i, (st, (px, py, wd)) in enumerate(zip(steps, pos)):
        acc, bg = color(st.get("color"))
        lines = [st.get("sub", "")] if st.get("sub") else []
        h = 34 + (17 * len(lines) if lines else 0) + (24 if st.get("note") else 0)
        s.append(rect(px, py, wd, h, bg, acc, 9, 1.5))
        if st.get("no"):
            s.append(badge(px + 18, py + 18, st["no"], acc, r=12, size=11.5))
            claim(px + 36, px + wd - 10, st["t"], 14, where="flow")
            s.append(t(px + 36, py + 23, st["t"], 14, acc, weight="700"))
        else:
            claim(px + 12, px + wd - 12, st["t"], 14, where="flow")
            s.append(t(px + 12, py + 22, st["t"], 14, acc, weight="700"))
        ly = py + 42
        for ln in lines:
            for seg in wclaim(px + 12, px + wd - 12, ln, 11.5, where="flowsub"):
                s.append(t(px + 12, ly, seg, 11.5, INK2))
                ly += 17
        if st.get("note"):
            for seg in wclaim(px + 12, px + wd - 12, st["note"], 11, MUTED, where="flownote"):
                s.append(t(px + 12, ly + 4, seg, 11, MUTED))
                ly += 16
        if i < len(steps) - 1:
            nx, ny, _ = pos[i + 1]
            if ny == py:
                s.append(path("M %.0f %.0f H %.0f" % (px + wd + 2, py + 26, nx - 4),
                              stroke=acc, sw=1.8, marker="ar"))
            else:
                sx = px + wd + 2
                d = "M %.0f %.0f h 14 V %.0f H %.0f V %.0f h -14" % (sx, py + 26, py + 60, x - 20,
                                                                     ny + 26)
                s.append(path(d, stroke=acc, sw=1.6, dash="5 4", marker="ar"))
    H = int(y + rows * rowh + 14)
    if spec.get("note"):
        col = color(spec.get("note_color", "blue"))
        svg, yb = note_bar(40, y + rows * rowh + 4, W - 80, spec["note"], col[1], col[0])
        s.append(svg)
        H = int(yb + 14)
    s.append("</svg>\n")
    return H, "".join(s)


def build_tree(spec):
    """组织树：levels = [[{t, sub}, …], …]，父节点按 order 均匀分布在上层之下。"""
    W = spec.get("w", 1280)
    s = [svg_open(W, 100, spec["title"])]
    s.append(t(40, 46, spec["title"], 22, INK, weight="700"))
    if spec.get("sub"):
        s.append(t(40, 72, spec["sub"], 12.5, MUTED))
    y = 108
    LEVEL_H = spec.get("level_h", 96)
    layers = []
    for li, lv in enumerate(spec["levels"]):
        n = len(lv["nodes"])
        bw = min(spec.get("box_w", 240), (W - 80 - (n - 1) * 16) / float(n))
        row = []
        for i, node in enumerate(lv["nodes"]):
            bx = 40 + i * ((W - 80 - bw) / float(max(1, n - 1))) if n > 1 else (W - bw) / 2.0
            acc, bg = color(node.get("color") or lv.get("color"))
            lines = []
            for ln in node.get("lines") or []:
                lines.extend(wrap(ln, 11.5, bw - 22))
            h = 30 + len(lines) * 16 + 10
            s.append(rect(bx, y, bw, h, bg, acc, 9, 1.4))
            claim(bx + 11, bx + bw - 11, node["t"], 13.5, where="tree")
            s.append(t(bx + 11, y + 21, node["t"], 13.5, acc, weight="700"))
            ly = y + 38
            for ln in lines:
                s.append(t(bx + 11, ly, ln, 11.5, INK2))
                ly += 16
            row.append((bx + bw / 2.0, y, y + h))
        layers.append(row)
        if li < len(spec["levels"]) - 1:
            y += LEVEL_H
    # 父子连线：按父索引均匀分配子节点
    for li in range(len(spec["levels"]) - 1):
        children = spec["levels"][li + 1]["nodes"]
        parents = layers[li]
        for i, ch in enumerate(children):
            pidx = ch.get("parent", int(i * len(parents) / max(1, len(children))))
            pidx = min(pidx, len(parents) - 1)
            px, _pt, pb = parents[pidx]
            cx, ct, _cb = layers[li + 1][i]
            midy = (pb + ct) / 2.0
            s.append(path("M %.0f %.0f V %.0f H %.0f V %.0f" % (px, pb + 2, midy, cx, ct - 2),
                          stroke=MUTED, sw=1.3))
    H = int(y + LEVEL_H + 8)
    s.append("</svg>\n")
    return H, "".join(s)


def build_swimlane(spec):
    """泳道图：列 = 步骤，行 = 角色/系统，单元格文字可为空。"""
    W = spec.get("w", 1400)
    s = [svg_open(W, 100, spec["title"])]
    s.append(t(40, 46, spec["title"], 22, INK, weight="700"))
    if spec.get("sub"):
        s.append(t(40, 72, spec["sub"], 12.5, MUTED))
    cols = spec["cols"]           # [{"t": 列标题, "sub": 小字}]
    rows = spec["rows"]           # [{"t": 行名, "color": c, "cells": [文字或 None]}]
    lane_w = 150.0
    colw = (W - 80 - lane_w) / float(len(cols))
    y = 106
    head_h = 46
    s.append(rect(40, y, W - 80, head_h, BLUE_L, BLUE, 8, 1.2))
    s.append(t(40 + 12, y + 28, spec.get("lane_head", "步骤 / 角色"), 13, BLUE_D, weight="700"))
    for ci, c in enumerate(cols):
        cx = 40 + lane_w + ci * colw
        claim(cx + 8, cx + colw - 8, c["t"], 12.5, where="swimcol")
        s.append(t(cx + colw / 2.0, y + 21, c["t"], 12.5, INK, "middle", "700"))
        if c.get("sub"):
            s.append(t(cx + colw / 2.0, y + 38, c["sub"], 11, MUTED, "middle"))
    y += head_h
    for row in rows:
        acc, bg = color(row.get("color"))
        cells = row["cells"]
        hmax = 40
        for cell in cells:
            if cell:
                hmax = max(hmax, 22 + 16 * len(wrap(cell, 11.5, colw - 18)))
        s.append(rect(40, y, W - 80, hmax, "#ffffff", acc, 6, 1.1))
        s.append(rect(40, y, lane_w, hmax, bg, acc, 6, 1.1))
        claim(40 + 12, 40 + lane_w - 10, row["t"], 13, where="swimrow")
        s.append(t(40 + 12, y + 24, row["t"], 13, acc, weight="700"))
        for ci, cell in enumerate(cells):
            cx = 40 + lane_w + ci * colw
            if ci:
                s.append(line(cx, y, cx, y + hmax, LINE, 1))
            if cell:
                ly = y + 22
                for seg in wclaim(cx + 10, cx + colw - 10, cell, 11.5, where="swimcell"):
                    s.append(t(cx + 10, ly, seg, 11.5, INK2))
                    ly += 16
        y += hmax
    H = int(y + 14)
    s.append("</svg>\n")
    return H, "".join(s)


def build_star(spec):
    """集成关系图：中心模块 + 四周邻居（双向箭头，各带「我方给它 / 它给我」标签）。"""
    W = spec.get("w", 1280)
    cx, cy = W / 2.0, 400.0
    cw, ch = 300, 150
    satellites = spec["satellites"]
    s = [svg_open(W, 100, spec["title"])]
    s.append(t(40, 46, spec["title"], 22, INK, weight="700"))
    if spec.get("sub"):
        s.append(t(40, 72, spec["sub"], 12.5, MUTED))
    pos = []
    n = len(satellites)
    for i, sat in enumerate(satellites):
        ang = sat.get("ang")
        if ang is None:
            ang = -90 + i * (360.0 / n)
        rad = math.radians(ang)
        sx = cx + (W / 2.0 - 250) * math.cos(rad)
        sy = cy + 300 * math.sin(rad)
        pos.append((sx, sy))

    for (sx, sy), sat in zip(pos, satellites):
        acc, bg = color(sat.get("color"))
        bw, bh = 330, 120
        bx, by = sx - bw / 2.0, sy - bh / 2.0
        dirx = -1 if sx > cx else 1
        # 双向箭头：从中心边缘到卫星边缘
        cxx = cx + (cw / 2.0 + 4) * (1 if sx > cx else -1)
        sxx = bx + (0 if sx > cx else bw) + (4 if sx > cx else -4)
        s.append(line(cxx, cy, sxx, sy, acc, 1.8, marker="ar", marker_back="arback"))
        s.append(rect(bx, by, bw, bh, bg, acc, 9, 1.4))
        claim(bx + 12, bx + bw - 12, sat["t"], 14, where="sat")
        s.append(t(bx + 12, by + 24, sat["t"], 14, acc, weight="700"))
        ly = by + 44
        if sat.get("down"):
            for seg in wclaim(bx + 12, bx + bw - 12, "它给我们：" + sat["down"], 11.5, where="satdown"):
                s.append(t(bx + 12, ly, seg, 11.5, INK2))
                ly += 16
        if sat.get("up"):
            for seg in wclaim(bx + 12, bx + bw - 12, "我们给它：" + sat["up"], 11.5, where="satup"):
                s.append(t(bx + 12, ly, seg, 11.5, MUTED))
                ly += 16
    s.append(rect(cx - cw / 2.0, cy - ch / 2.0, cw, ch, BLUE_D, BLUE_D, 14))
    s.append(t(cx, cy - 18, spec["center_title"], 26, "#ffffff", "middle", "700"))
    s.append(t(cx, cy + 10, spec.get("center_sub", ""), 15, "#dbeafd", "middle"))
    s.append(t(cx, cy + 36, spec.get("center_en", ""), 12, "#a9cdf3", "middle", family=MONO))
    H = int(cy + 300 + 90)
    if spec.get("note"):
        svg, yb = note_bar(40, H - 60, W - 80, spec["note"], BLUE_L, BLUE)
        s.append(svg)
        H = int(yb + 16)
    s.append("</svg>\n")
    return H, "".join(s)


def build_chains(spec):
    """决定链 / 规则卡：一叠「标题 + 横向链 + 说明行」的面板。"""
    W = spec.get("w", 1280)
    s = [svg_open(W, 100, spec["title"])]
    s.append(t(40, 46, spec["title"], 22, INK, weight="700"))
    if spec.get("sub"):
        s.append(t(40, 72, spec["sub"], 12.5, MUTED))
    y = 106
    for item in spec["items"]:
        acc, bg = color(item.get("color"))
        lines = item.get("texts") or []
        svg, yb = panel(40, y, W - 80, item["title"], [], acc, bg, title_size=15.5, size=12)
        out = [svg]
        cy = y + 52
        if item.get("chain"):
            # 注意：chip_rows 返回的是「链底部的绝对 y」，不是高度 —— 早期把它当高度用，
            # 导致面板高度按 y 累积、图越画越长（4 个面板能拉到 4600px）。这里直接用返回值。
            csvg, cbottom = _chain(58, cy, W - 196, item["chain"], acc)
            out.append(csvg)
            cy = cbottom + 6
        for ln in lines:
            for seg in wclaim(58, W - 58, ln, 12, where="chaintext"):
                out.append(t(58, cy, seg, 12, INK2))
                cy += 18
        # 重画底板以覆盖自适应高度（先算后画）
        h = cy - y + 10
        out[0] = rect(40, y, W - 80, h, bg, acc, 9) + rect(40, y, 4.5, h, acc, acc, rx=2) + \
            t(58, y + 28, item["title"], 15.5, acc, weight="700")
        s.append("".join(out))
        y += h + 16
    H = int(y + 6)
    s.append("</svg>\n")
    return H, "".join(s)


def _chain(x, y, avail, items, accent=BLUE, size=11.5, rowh=42):
    """横向链（chips），超宽折行；返回 (svg, 高度)。"""
    return chip_rows(x, y, avail, items, accent, size, h=rowh)


BUILDERS = {
    "mindmap": build_mindmap,
    "layers": build_layers,
    "flow": build_flow,
    "tree": build_tree,
    "swimlane": build_swimlane,
    "star": build_star,
    "chains": build_chains,
}


def build(spec):
    """渲染一张图：返回 (svg_text)。spec 里必须有 kind / file / title。"""
    kind = spec["kind"]
    if kind not in BUILDERS:
        raise ValueError("未知图形类别：%s（可用：%s）" % (kind, ", ".join(sorted(BUILDERS))))
    del CLAIMS[:]
    h, svg = BUILDERS[kind](spec)
    # 各构建器先按「已知宽度 + 占位高度」开画布，算完全部内容才知道最终高度，这里回填。
    svg = re.sub(r'viewBox="0 0 (\d+) 100" width="(\d+)" height="100"',
                 lambda m: 'viewBox="0 0 %s %d" width="%s" height="%d"'
                           % (m.group(1), h, m.group(2), h), svg, count=1)
    svg = svg.replace('<rect width="%d" height="100" fill="#ffffff"/>' % spec.get("w", 1280),
                      '<rect width="%d" height="%d" fill="#ffffff"/>' % (spec.get("w", 1280), h))
    # XML 合法性
    try:
        ET.fromstring(svg)
    except ET.ParseError as e:
        raise ValueError("SVG XML 不合法（%s）：%s" % (spec["file"], e))
    return svg, list(CLAIMS)
