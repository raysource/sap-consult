#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SAP GUI 画面イメージ（モックアップ）生成 + 手顺ページへの挿入

- 仕様（JSON）から SAP GUI Classic 風の SVG を生成し、<site>/assets/gui/ に書き出す
- 手顺ページ（config.html の C ステップ / handson-*.html の STEP）へ <figure class="gui"> を挿入
- 挿入は冪等：既存の <figure class="gui">…</figure> を全部消してから入れ直す

重要：生成物は **実機のスクリーンショットではなく、標準レイアウトに基づくイメージ図**。
      実機で撮った画像に差し替えるときは、同じファイル名で .png を置いて
      `python3 tools/swap_gui_images.py <site> --apply` を実行する（src の拡張子を書き換える）。

用法:
    python3 tools/make_gui_mockups.py <site>            # 生成 + 挿入 + 検証
    python3 tools/make_gui_mockups.py <site> --no-insert
    python3 tools/make_gui_mockups.py <site> --check     # 挿入せず検証のみ

仕様ファイル: <site>/tools/gui_spec.json   （形式は tools/GUI_SPEC_FORMAT.md）
"""
import argparse
import html
import json
import os
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

W, H = 1180, 760
TITLE_H, MENU_H, TOOL_H, TAB_H, STATUS_H = 32, 24, 28, 26, 34

# SAP GUI Classic 風の配色
C_TITLE_A, C_TITLE_B = "#21456e", "#37699b"
C_CHROME, C_CHROME_LINE = "#e9e9e9", "#bdbdbd"
C_BODY = "#f4f4f2"
C_FIELD, C_FIELD_LINE = "#ffffff", "#8f9aa6"
C_TBL_HEAD = "#b7c7dd"
C_TBL_ALT = "#f3f6fa"
C_TBL_SEL = "#fff3a6"
C_TEXT = "#1d2d3e"
C_LINK = "#0a4f9e"
C_OK, C_WARN, C_ERR = "#2e7d32", "#b26a00", "#c62828"

FONT = "font-family='-apple-system,BlinkMacSystemFont,\"Noto Sans CJK JP\",\"Hiragino Sans\",\"Microsoft YaHei\",Meiryo,sans-serif'"
MONO = "font-family='SFMono-Regular,Menlo,Consolas,\"Courier New\",monospace'"

MENU_ITEMS = ["メニュー", "編集", "お気に入り", "ジャンプ", "システム", "ヘルプ"]
TOOLBAR = [
    ("↩", "Enter"), ("⌕", "検索"), ("⌫", "F3"), ("⇦", "戻る"), ("✖", "取消"),
    ("⇩", "次頁"), ("⇧", "前頁"), ("▣", "保存"), ("⎙", "印刷"), ("✎", "変更"), ("▤", "全体"),
]


def esc(t):
    return html.escape(str(t), quote=True)


def fmt(v, limit=0):
    if v is None:
        return ""
    v = str(v)
    return v if not limit else (v[:limit] + ("…" if len(v) > limit else ""))


_TEXT_BOXES = []          # 描画済みテキストのbbox（注記の重なり回避に使う）
_CALLOUT_BOXES = []       # 配置済み注記のbbox



def _wide(ch):
    return unicodedata.east_asian_width(ch) in ("W", "F")


def text_w(s, size, mono=False):
    """CJK（全角）を 1.0em、半角を 0.52/0.60em として幅を見積もる（重なり判定の精度が上がる）"""
    s = str(s)
    w = sum(1.0 if _wide(c) else (0.60 if mono else 0.52) for c in s)
    return w * size + 2

def _note_box(x, y, s, size, anchor, mono):
    w = text_w(s, size, mono)
    x0 = x if anchor == "start" else (x - w / 2 if anchor == "middle" else x - w)
    return [x0, y - size * 0.82, x0 + w, y + size * 0.26]


def _hit(b, boxes):
    for o in boxes:
        if not (b[2] <= o[0] or o[2] <= b[0] or b[3] <= o[1] or o[3] <= b[1]):
            return True
    return False


def text(x, y, s, size=13, fill=C_TEXT, bold=False, anchor="start", mono=False, italic=False):
    if str(s).strip():
        _TEXT_BOXES.append(_note_box(x, y, s, size, anchor, mono))
    fam = MONO if mono else FONT
    b = ' font-weight="700"' if bold else ""
    i = ' font-style="italic"' if italic else ""
    return ("<text x=\"%s\" y=\"%s\" font-size=\"%s\"%s %s fill=\"%s\" text-anchor=\"%s\"%s%s>%s</text>"
            % (x, y, size, b, fam, fill, anchor, "", i, esc(s)))


def rect(x, y, w, h, fill="none", stroke="none", rx=0, sw=1, opacity=None):
    o = ' opacity="%s"' % opacity if opacity is not None else ""
    return ('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>'
            % (x, y, w, h, rx, fill, stroke, sw, o))


def line(x1, y1, x2, y2, stroke=C_FIELD_LINE, sw=1, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    return '<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"%s/>' % (x1, y1, x2, y2, stroke, sw, d)


def glyph_box(x, y, g, cap="", size=18):
    """ツールバーのアイコンボックス"""
    out = [rect(x, y, 24, 22, fill="#fdfdfd", stroke="#c3ccd6", rx=3)]
    out.append(text(x + 12, y + 16, g, size=13, fill="#3c5a78", anchor="middle"))
    if cap:
        out.append(text(x + 12, y + 34, cap, size=8, fill="#6b7a8d", anchor="middle", mono=True))
    return "".join(out)


def render(spec):
    """spec（1 画面）→ SVG 文字列"""
    del _TEXT_BOXES[:]
    del _CALLOUT_BOXES[:]
    out = ['<?xml version="1.0" encoding="UTF-8"?>']
    out.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" role="img" '
               'aria-label="%s">' % (W, H, W, H, esc(spec.get("aria") or spec.get("title", "SAP GUI 画面イメージ"))))
    out.append('<defs><linearGradient id="tb" x1="0" y1="0" x2="0" y2="1">'
               '<stop offset="0%%" stop-color="%s"/><stop offset="100%%" stop-color="%s"/></linearGradient></defs>'
               % (C_TITLE_B, C_TITLE_A))
    out.append(rect(0, 0, W, H, fill=C_BODY))

    # ---- タイトルバー ----
    out.append(rect(0, 0, W, TITLE_H, fill="url(#tb)"))
    out.append(text(12, 21, spec.get("window_title") or ("%s   %s" % (spec.get("tx", ""), spec.get("title", ""))),
                    size=13, fill="#ffffff", bold=True))
    out.append(text(W - 66, 21, "─", size=13, fill="#dce8f5"))
    out.append(text(W - 44, 21, "▢", size=13, fill="#dce8f5"))
    out.append(text(W - 22, 21, "✕", size=13, fill="#dce8f5"))

    # ---- メニューバー ----
    y = TITLE_H
    out.append(rect(0, y, W, MENU_H, fill=C_CHROME))
    out.append(line(0, y + MENU_H, W, y + MENU_H))
    mx = 12
    for it in (spec.get("menu") or MENU_ITEMS):
        out.append(text(mx, y + 16, it, size=12, fill="#333a42"))
        mx += 14 + len(it) * 13
    if spec.get("tx"):
        out.append(text(W - 14, y + 16, "取引コード: %s" % spec["tx"], size=12, fill="#5b6b7c", anchor="end", bold=True))

    # ---- ツールバー ----
    y += MENU_H
    out.append(rect(0, y, W, TOOL_H, fill=C_CHROME))
    out.append(line(0, y + TOOL_H, W, y + TOOL_H))
    tb = spec.get("toolbar") or []
    x = 10
    for g, cap in (tb if tb else []):
        out.append(glyph_box(x, y + 3, g, cap))
        x += 30
    if spec.get("std_toolbar"):
        out.append(text(W - 14, y + 17, spec["std_toolbar"], size=10, fill="#5b6b7c", anchor="end", mono=True))

    # ---- タブ ----
    y += TOOL_H
    bx = 12
    if spec.get("tabs"):
        out.append(line(0, y + TAB_H, W, y + TAB_H, stroke=C_CHROME_LINE))
        act = spec.get("active_tab", 0)
        for i, t in enumerate(spec["tabs"]):
            wpx = 24 + len(t) * 12
            if i == act:
                out.append(rect(bx, y + 2, wpx, TAB_H, fill=C_BODY, stroke=C_CHROME_LINE, rx=6))
                out.append(rect(bx, y + TAB_H - 2, wpx, 3, fill=C_BODY))
                out.append(text(bx + wpx / 2, y + 18, t, size=12, fill=C_TEXT, bold=True, anchor="middle"))
            else:
                out.append(rect(bx, y + 4, wpx, TAB_H - 4, fill="#dfe3e8", stroke=C_CHROME_LINE, rx=6))
                out.append(text(bx + wpx / 2, y + 18, t, size=12, fill="#5b6b7c", anchor="middle"))
            bx += wpx + 4
        y += TAB_H
    else:
        out.append(line(0, y + TAB_H, W, y + TAB_H, stroke=C_CHROME_LINE))
        y += TAB_H

    body_top = y
    body_bot = H - STATUS_H
    out.append(rect(0, body_top, W, body_bot - body_top, fill=C_BODY))

    # ---- 本文 ----
    kind = spec.get("kind", "form")
    if kind == "form":
        render_form(out, spec, body_top, body_bot)
    elif kind == "table":
        render_table(out, spec, body_top, body_bot)
    elif kind == "tree":
        render_tree(out, spec, body_top, body_bot)
    elif kind == "split":
        mid = intra(body_top, body_bot, spec)
        render_form(out, spec, body_top, mid)
        render_table(out, spec, mid, body_bot, first=True)
    elif kind == "blank":
        out.append(text(W / 2, (body_top + body_bot) / 2, spec.get("placeholder", ""), size=14, fill="#8a94a0", anchor="middle"))
    else:
        raise ValueError("unknown kind: %s" % kind)

    # ---- ステータスバー ----
    sy = body_bot
    out.append(rect(0, sy, W, STATUS_H, fill="#eef1f4"))
    out.append(line(0, sy, W, sy, stroke=C_CHROME_LINE))
    st = spec.get("status")
    if st:
        lvl, msg = (st[0], st[1]) if isinstance(st, (list, tuple)) else ("success", st)
        col = {"success": C_OK, "warning": C_WARN, "error": C_ERR, "info": C_LINK}.get(lvl, C_OK)
        gi = {"success": "✓", "warning": "⚠", "error": "✕", "info": "ℹ"}.get(lvl, "✓")
        out.append(text(14, sy + 22, gi, size=14, fill=col, bold=True))
        out.append(text(34, sy + 22, msg, size=12.5, fill=col))
    out.append(line(W - 300, sy + 4, W - 300, sy + STATUS_H - 4, stroke=C_CHROME_LINE))
    out.append(text(W - 290, sy + 22, spec.get("status_right") or "S4H / 100 / TRAIN-01", size=11.5, fill="#5b6b7c", mono=True))

    # ---- 注記（キャプション内の凡例は HTML 側。SVG 内の見出し番号バッジは下で描画） ----
    for i, co in enumerate(spec.get("callouts") or [], 1):
        if len(co) < 3:                      # 座標省略時は既定位置に置く
            co = [co[0], 900, 190 + (i - 1) * 52] + list(co[1:])
        label, cx, cy0 = co[0], co[1], co[2]
        tw = co[3] if len(co) > 3 else None
        bw = (len(tw) * 12.5 + 16 + 22) if tw else 0   # 実際に描く吹き出し矩形に合わせる
        # バッジ / 吹き出しが他のテキストや注記に重ならない y を探す（±8px 刻み、上下 88px まで）
        cy, cx2 = cy0, cx
        for dy in [0, -26, 26, -52, 52, -78, 78, -104, 104, -130, 130]:
            placed = False
            for dx in [0, 70, -70, 140]:
                cand, candx = cy0 + dy, cx + dx
                b = [candx - 14, cand - 14, candx + 14, cand + 14]
                if tw:
                    b[2] = max(b[2], candx + 20 + bw)      # 吹き出し本体
                    b[1] = min(b[1], cand - 34)            # 吹き出しの上端
                if (40 < cand < H - 40 and 16 < candx < W - 60
                        and not _hit(b, _TEXT_BOXES) and not _hit(b, _CALLOUT_BOXES)):
                    cy, cx2, placed = cand, candx, True
                    break
            if placed:
                break
        cx = cx2
        _CALLOUT_BOXES.append([cx - 14, cy - 32 if tw else cy - 14, cx + 14 + bw, cy + 14])
        out.append('<circle cx="%s" cy="%s" r="13" fill="#ffffff" stroke="#d32f2f" stroke-width="2"/>' % (cx, cy))
        out.append(text(cx, cy + 5, str(i), size=13, fill="#d32f2f", bold=True, anchor="middle"))
        if tw:
            out.append(line(cx + 14, cy, cx + 14 + len(tw) * 7 + 16, cy, stroke="#d32f2f", sw=1.5, dash="4 3"))
            out.append(rect(cx + 20, cy - 30, len(tw) * 12.5 + 16, 24, fill="#fff5f5", stroke="#d32f2f", rx=4, sw=1))
            out.append(text(cx + 28, cy - 13, tw, size=12, fill="#b71c1c"))
    out.append("</svg>")
    return "\n".join(out)


def intra(top, bot, spec):
    """split レイアウトの分割位置"""
    return int(top + (bot - top) * (spec.get("split_ratio", 0.45)))


def render_form(out, spec, top, bot, first=False):
    y = top + (18 if not first else 6)
    x0 = 26
    if spec.get("section") and not first:
        out.append(text(x0, y + 4, spec["section"], size=13, fill=C_LINK, bold=True))
        y += 24
    cols = 2
    flds = spec.get("fields") or []
    # 2 列（左ラベル・入力欄）を cols 分並べる
    colw = (W - 2 * x0 - 20) // cols
    i = 0
    rows = []
    while i < len(flds):
        rows.append(flds[i:i + cols])
        i += cols
    for r in rows:
        maxh = 0
        for j, f in enumerate(r):
            label, value = f[0], (f[1] if len(f) > 1 else "")
            req = f[2] if len(f) > 2 else False
            wide = f[3] if len(f) > 3 else False
            fw = (f[4] if len(f) > 4 else None) or (colw * 0.55)
            fx = x0 + j * colw
            if wide:
                fw = colw - 20
            out.append(text(fx, y + 14, label, size=12.5, fill="#38424e", bold=bool(req)))
            out.append(rect(fx, y + 20, fw, 22, fill=C_FIELD, stroke=C_FIELD_LINE, rx=2))
            out.append(text(fx + 6, y + 35, fmt(value, 44), size=12.5, fill="#101820", mono=True))
            if req:
                out.append(rect(fx + fw + 5, y + 26, 10, 10, fill="#ffffff", stroke="#8f9aa6", rx=1))
                out.append(text(fx + fw + 6, y + 35, "✓", size=10, fill=C_OK))
            maxh = max(maxh, 50)
        y += maxh + 4
    if spec.get("note"):
        out.append(text(x0, min(y + 16, bot - 12), spec["note"], size=11.5, fill="#6b7a8d", italic=True))


def render_table(out, spec, top, bot, first=False):
    t = spec.get("table") or {}
    x0, x1 = 22, W - 22
    y = top + (10 if not first else 8)
    if t.get("title") and not first:
        out.append(text(x0, y + 6, t["title"], size=13, fill=C_LINK, bold=True))
        y += 22
    cols = t.get("columns") or []
    rows = t.get("rows") or []
    if not cols:
        return
    weights = t.get("widths") or [1] * len(cols)
    tot = sum(weights)
    avail = (x1 - x0) - 34
    xs, cx = [], x0 + 34
    for w in weights:
        xs.append((cx, avail * w / tot))
        cx += avail * w / tot
    rh = t.get("row_height", 26)
    # ヘッダー
    out.append(rect(x0, y, x1 - x0, 24, fill=C_TBL_HEAD, stroke="#8f9aa6"))
    out.append(rect(x0, y, 34, 24, fill="#a9bad0", stroke="#8f9aa6"))
    out.append(text(x0 + 17, y + 17, "", size=12, anchor="middle"))
    for (cx0, cw), name in zip(xs, cols):
        out.append(text(cx0 + 6, y + 17, fmt(name, 22), size=12, fill="#17263a", bold=True))
        out.append(line(cx0, y, cx0, bot - 4, stroke="#c3ccd6"))
    yh = y + 24
    for i, row in enumerate(rows):
        sel = (t.get("selected") == i)
        bg = C_TBL_SEL if sel else (C_TBL_ALT if i % 2 else "#ffffff")
        out.append(rect(x0, yh, x1 - x0, rh, fill=bg, stroke="#d7dee6"))
        out.append(text(x0 + 17, yh + rh * 0.68, str(i + 1), size=11.5, fill="#6b7a8d", anchor="middle", mono=True))
        for (cx0, cw), v in zip(xs, row):
            if v is None:
                continue
            bold = str(v).startswith("*")
            s = fmt(str(v).lstrip("*"), int(cw / 7.2))
            out.append(text(cx0 + 6, yh + rh * 0.68, s, size=12, fill=("#101820" if not sel else "#5c4b00"), mono=True, bold=bold))
        yh += rh
    if t.get("footer"):
        out.append(text(x0, min(yh + 18, bot - 20), t["footer"], size=11.5, fill="#6b7a8d", italic=True))
    if not first and spec.get("note"):
        out.append(text(x0, min(yh + 40, bot - 6), spec["note"], size=11.5, fill="#6b7a8d", italic=True))


def render_tree(out, spec, top, bot):
    tr = spec.get("tree") or {}
    x0 = 26
    y = top + 18
    if tr.get("title"):
        out.append(text(x0, y, tr["title"], size=13, fill=C_LINK, bold=True))
        y += 22
    rh = tr.get("row_height", 26)
    for i, node in enumerate(tr.get("rows") or []):
        label = node[0]
        depth = node[1] if len(node) > 1 else 0
        sel = (tr.get("selected") == i)
        xx = x0 + depth * 26
        out.append(rect(x0 - 6, y - 16, W - 2 * (x0 - 6) - 10, rh - 4,
                        fill=(C_TBL_SEL if sel else ("#ffffff" if i % 2 == 0 else C_TBL_ALT)), stroke="#d7dee6"))
        icon = "⊟" if depth == 0 else ("⊞" if depth == 1 else "•")
        out.append(text(xx, y + 2, icon, size=13, fill="#3c5a78"))
        out.append(text(xx + 22, y + 2, fmt(label, 90), size=12.5,
                        fill=("#101820" if not sel else "#5c4b00"), mono=True, bold=(depth == 0)))
        if len(node) > 2 and node[2]:
            out.append(text(W - 40, y + 2, node[2], size=12, fill="#37424e", anchor="end", mono=True))
        y += rh
    if spec.get("note"):
        out.append(text(x0, min(y + 18, bot - 12), spec["note"], size=11.5, fill="#6b7a8d", italic=True))


# ---------------------------------------------------------------------------
# 挿入（HTML）
# ---------------------------------------------------------------------------
FIG_START = '<figure class="gui"'
FIG_END = "</figure>"


PAIR_EMPTY_RE = re.compile(r'\n?<div class="gui-pair">\s*</div>')


def strip_figures(s):
    out, i = [], 0
    while True:
        j = s.find(FIG_START, i)
        if j < 0:
            out.append(s[i:])
            break
        out.append(s[i:j])
        k = s.find(FIG_END, j)
        if k < 0:
            break
        k += len(FIG_END)
        # 直前の改行・空白も落とす
        while out and out[-1].endswith("\n"):
            out[-1] = out[-1][:-1]
        i = k
    s2 = "".join(out)
    return PAIR_EMPTY_RE.sub("", s2)


def figure_html(spec, site_dir, rel_dir="assets/gui"):
    f = spec["file"]
    cap = spec.get("caption") or spec.get("title", "")
    leg = []
    for i, co in enumerate(spec.get("callouts") or [], 1):
        leg.append("<li><b>%d</b> %s</li>" % (i, esc(co[0])))
    h = ['<figure class="gui">']
    h.append('<img src="%s/%s" alt="%s" loading="lazy">' % (rel_dir, f, esc(spec.get("aria") or cap)))
    h.append('<figcaption><b class="t">%s</b>' % esc(cap))
    if spec.get("tx"):
        h.append('<span class="tx">%s</span>' % esc(spec["tx"]))
    if spec.get("title"):
        h.append('<span class="scr">%s</span>' % esc(spec["title"]))
    h.append('<span class="kind">画面イメージ</span></figcaption>')
    if leg:
        h.append('<ol class="gui-legend">' + "".join(leg) + "</ol>")
    if spec.get("tip"):
        h.append('<p class="gui-tip">%s</p>' % esc(spec["tip"]))
    h.append("</figure>")
    return "".join(h)


def bounds_config(html_src, cid):
    """C ステップの範囲：次の steph か次の h2 のどちらか早い方まで"""
    m = re.search(r'<div class="steph" id="%s">' % re.escape(cid), html_src)
    if not m:
        return None
    tail = html_src[m.end():]
    cands = [m.end() + x.start() for x in re.finditer(r'<div class="steph" id=|<h2', tail)]
    return m.start(), (min(cands) if cands else len(html_src))


def plain(t):
    t = re.sub(r"<[^>]+>", "", t)
    t = t.replace("&nbsp;", " ").replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"')
    return re.sub(r"\s+", " ", t).strip()


def bounds_h2_stop(html_src, key):
    """config.html 内の h2 節：次の h2 か次の div.steph のどちらか早い方まで"""
    ks = [m for m in re.finditer(r"<h2[^>]*>(.*?)</h2>", html_src, re.S)]
    for m in ks:
        if plain(m.group(1)) == key.strip() or plain(m.group(1)).startswith(key.strip()):
            tail = html_src[m.end():]
            cands = [m.end() + x.start() for x in re.finditer(r"<h2|<div class=\"steph\"", tail)]
            return m.start(), min(cands) if cands else len(html_src)
    return None


def bounds_h2(html_src, key):
    """h2 のプレーンテキストが key と一致するセクションの範囲を返す（インラインタグ許容）"""
    ks = [m for m in re.finditer(r"<h2[^>]*>(.*?)</h2>", html_src, re.S)]
    for i, m in enumerate(ks):
        if plain(m.group(1)) == key.strip() or plain(m.group(1)).startswith(key.strip()):
            s0 = m.start()
            e0 = ks[i + 1].start() if i + 1 < len(ks) else len(html_src)
            return s0, e0
    return None


VOID_TAGS = {"br", "hr", "img", "input", "meta", "link", "area", "base", "col", "embed", "source", "track", "wbr"}
TAG_RE = re.compile(r"<(/?)([a-zA-Z][a-zA-Z0-9]*)([^>]*?)(/?)>")


def balanced_prefix(block, pos):
    """block[:pos] のタグが過不足なく閉じているか（＝その位置は要素の外側か）"""
    st = []
    for m in TAG_RE.finditer(block, 0, pos):
        closing, name, _attrs, selfclose = m.group(1), m.group(2).lower(), m.group(3), m.group(4)
        if name in VOID_TAGS or selfclose:
            continue
        if closing:
            if not st:
                return False
            st.pop()
        else:
            st.append(name)
    return not st


def insert_point(html_src, s, e):
    """セクション [s,e) 内で、要素の外側にある安全な挿入位置を後ろから探す。
    （表のセルや <b> の中に図が入り込んで HTML が壊れるのを防ぐ）"""
    block = html_src[s:e]
    # 記事本文の外（</article> 以降）には絶対に入れない
    lim = re.search(r"</article>|</main>|</body>|</html>", block)
    limit = lim.start() if lim else len(block)
    cands = sorted({m.end() for m in re.finditer(r"</ol>|</table>|</ul>|</div>|</p>", block[:limit])})
    for pos in reversed(cands):
        if not balanced_prefix(block[:limit], pos):
            continue
        if re.match(r"\s*</", block[pos:]):      # 閉じタグの直前（＝要素の中）は避ける
            continue
        return s + pos
    return s + limit


def insert_site(site_dir, spec_pages, dry=False):
    """spec_pages: {page_file: [(step_key, [spec, ...]), ...]}"""
    report = []
    for page, steps in spec_pages.items():
        p = os.path.join(site_dir, page)
        s = open(p, encoding="utf-8").read()
        s = strip_figures(s)
        # 位置の浅いキーから挿入すると後続のオフセットがずれるので、後ろ（文書の後方）から処理する
        items = []
        for key, specs in steps.items():
            if page == "config.html":
                b = bounds_config(s, key) or bounds_h2_stop(s, key)   # steph が無い節（準備等）は h2 で拾う
            else:
                b = bounds_h2(s, key)
            if not b:
                report.append(("MISS", page, key))
                continue
            items.append((b[0], b[1], key, specs))
        for s0, e0, key, specs in sorted(items, key=lambda t: -t[0]):
            at = insert_point(s, s0, e0)
            figs = "\n".join(figure_html(sp, site_dir) for sp in specs)
            s = s[:at] + "\n" + figs + "\n" + s[at:]
            report.append(("OK", page, key, len(specs)))
        if not dry:
            open(p, "w", encoding="utf-8").write(s)
    return report


CSS = """
/* === SAP GUI 画面イメージ（モックアップ） =============================== */
figure.gui { margin: 18px 0 22px; padding: 0; }
figure.gui img { display: block; width: 100%; max-width: 1180px; height: auto;
  border: 1px solid #c9d6e0; border-radius: 8px; box-shadow: 0 6px 18px rgba(16,36,58,.12); background: #fff; }
figure.gui figcaption { display: flex; flex-wrap: wrap; align-items: center; gap: 8px;
  margin-top: 8px; font-size: 12.5px; color: #6b7a8d; }
figure.gui figcaption .t { color: #1d2d3e; font-size: 13px; font-weight: 600; }
figure.gui figcaption .tx { font-family: ui-monospace, Menlo, Consolas, monospace; font-weight: 700;
  color: #0a4f9e; background: #eef4fb; border: 1px solid #cddff2; border-radius: 4px; padding: 1px 6px; }
figure.gui figcaption .kind { margin-left: auto; font-size: 11px; color: #8a94a0;
  border: 1px dashed #c9d6e0; border-radius: 10px; padding: 1px 8px; }
figure.gui .gui-legend { margin: 8px 0 0; padding: 0 0 0 2px; list-style: none; display: grid; gap: 4px; }
figure.gui .gui-legend li { font-size: 12.5px; color: #38424e; }
figure.gui .gui-legend b { display: inline-block; min-width: 18px; height: 18px; line-height: 18px; text-align: center;
  margin-right: 6px; border-radius: 9px; background: #fff; border: 1.5px solid #d32f2f; color: #d32f2f; font-size: 11px; }
figure.gui .gui-tip { margin: 8px 0 0; font-size: 12.5px; color: #5b6b7c; }
.gui-note { background: #fff8e6; border: 1px solid #f0d9a0; border-left: 4px solid #d9a431;
  border-radius: 6px; padding: 10px 14px; margin: 14px 0; font-size: 12.5px; color: #6b5426; }
.gui-note b { color: #8a6a1f; }
"""


def add_css(site_dir):
    css = None
    for cand in ("mto.css", "eto.css", "cmp.css", "mts.css", "vc.css"):
        p = os.path.join(site_dir, "assets", cand)
        if os.path.exists(p):
            css = p
            break
    if not css:
        return None
    s = open(css, encoding="utf-8").read()
    marker = "/* === SAP GUI 画面イメージ（モックアップ）"
    if marker in s:
        s = s[:s.index(marker)].rstrip() + "\n"
    open(css, "w", encoding="utf-8").write(s.rstrip() + "\n" + CSS)
    return css


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("site")
    ap.add_argument("--no-insert", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    site_dir = os.path.join(ROOT, a.site)
    spec_path = os.path.join(site_dir, "tools", "gui_spec.json")
    if not os.path.exists(spec_path):
        sys.exit("spec not found: %s" % spec_path)
    spec = json.load(open(spec_path, encoding="utf-8"))
    outdir = os.path.join(site_dir, "assets", "gui")
    os.makedirs(outdir, exist_ok=True)
    for old in os.listdir(outdir):
        if old.endswith(".svg"):
            os.remove(os.path.join(outdir, old))

    pages, n = {}, 0
    for page, steps in spec["pages"].items():
        pages[page] = {}
        pbase = re.sub(r"[^0-9a-zA-Z-]", "", page.replace(".html", ""))
        for si, (key, screens) in enumerate(steps.items(), 1):
            pages[page][key] = []
            for sc in screens:
                fn = sc.get("file") or ("%s_s%02d_%d.svg" % (pbase, si, len(pages[page][key]) + 1))
                sc["file"] = fn
                svg = render(sc)
                try:
                    ET.fromstring(svg)
                except ET.ParseError as ex:
                    sys.exit("SVG parse error in %s/%s/%s: %s" % (page, key, fn, ex))
                open(os.path.join(outdir, fn), "w", encoding="utf-8").write(svg)
                pages[page][key].append(sc)
                n += 1
    print("generated %d SVG -> %s" % (n, os.path.relpath(outdir, ROOT)))
    if a.check:
        return
    rep = insert_site(site_dir, pages, dry=a.dry)
    ok = sum(1 for r in rep if r[0] == "OK")
    miss = [r for r in rep if r[0] == "MISS"]
    print("inserted into %d step(s)%s" % (ok, "" if not a.dry else " (dry)"))
    for m in miss:
        print("   MISS: %s / %s" % (m[1], m[2]))
    css = add_css(site_dir)
    if css:
        print("css updated:", os.path.relpath(css, ROOT))
    if miss:
        sys.exit(1)


if __name__ == "__main__":
    main()
