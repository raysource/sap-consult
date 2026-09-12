# -*- coding: utf-8 -*-
"""
gui_spec.json を組み立てるビルダ（sapeto 用）。

tools/make_gui_mockups.py が読む `<site>/tools/gui_spec.json` を生成する。
画面は F/T/TR/SP のヘルパで作り、callouts は「行・列」で指定すると
make_gui_mockups.py の描画ジオメトリから座標を計算する（手で座標を書かない）。

    python3 tools/gui_spec_build.py [--check]

分割ファイル（spec_config_a.py など）を exec して PAGES に追記する。
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)

W, H = 1180, 760
BODY_TOP, BODY_BOT, STATUS_H = 110, H - 34, 34          # タイトル+メニュー+ツールバー+タブ = 110
FORM_DY, FORM_ROW_W = 18, 54                            # 1 行目 y=128、以降 54px 刻み
TBL_X0, TBL_X1, TBL_CURSOR = 22, 1158, 56               # 表の左端 / 右端 / 先頭列の開始 x
TBL_RH, TREE_RH = 26, 26

PAGES = {}
STEP_COUNT = [0]


def add(page, key, screens):
    PAGES.setdefault(page, {})[key] = screens
    STEP_COUNT[0] += 1


def _cols_geom(widths, n):
    ws = list(widths) if widths else [1] * n
    if len(ws) != n:
        ws = [1] * n
    tot = float(sum(ws))
    avail = (TBL_X1 - TBL_X0) - 34
    out, cx = [], TBL_X0 + 34
    for w in ws:
        out.append((cx, avail * w / tot))
        cx += avail * w / tot
    return out


def _table_top(spec, part):
    if spec.get("kind") == "split" and part == "table":
        return int(BODY_TOP + (BODY_BOT - BODY_TOP) * spec.get("split_ratio", 0.45)) + 8
    y = BODY_TOP + 10
    if (spec.get("table") or {}).get("title"):
        y += 22
    return y


def _tree_top(spec):
    y = BODY_TOP + 18
    if (spec.get("tree") or {}).get("title"):
        y += 22
    return y


def _co(spec, c):
    """callout 指定 → [説明, x, y, 吹き出し] に変換する。

    指定形式:
      (説明, 吹き出し, row, col)            行・列から座標計算
      (説明, 吹き出し, row, col, "table")   split 画面で下段の表を指す
      (説明, 吹き出し, None, x, y)          座標を直接指定
    """
    text, bubble = c[0], c[1]
    kind = spec.get("kind")
    if len(c) >= 5 and c[2] is None:
        x, y = float(c[3]), float(c[4])
    else:
        row = c[2] if len(c) > 2 else 0
        col = c[3] if len(c) > 3 else 0
        part = c[4] if len(c) > 4 else None
        tbl = spec.get("table") or {}
        xmin = 40
        if kind == "tree" or part == "tree":
            y = _tree_top(spec) + TREE_RH * row - 3
            x = 300
        elif kind == "table" or part == "table":
            top = _table_top(spec, part)
            y = top + 12 if row < 0 else top + 24 + TBL_RH * row + 13
            geom = _cols_geom(tbl.get("widths"), len(tbl.get("columns") or []))
            if geom and col < len(geom):
                cx0, cw = geom[col]
            else:
                cx0, cw = TBL_CURSOR, 120
            x = cx0 + cw - 16
            xmin = cx0 + 20          # 列の先頭の文字は隠さない
        else:
            # form / split の上段は「フィールドの番号（0 始まり）」で指定されている。
            # 描画は 2 列（左→右）に流れるので、番号 → (行, 列) に変換する。
            nf = len(spec.get("fields") or [])
            if isinstance(row, int) and 0 <= row < nf:
                row, col = row // 2, row % 2
            y = BODY_TOP + FORM_DY + (24 if spec.get("section") else 0) + FORM_ROW_W * row + 31
            x = 350 if col == 0 else 900
            xmin = 380 if col == 0 else 800      # 2 列目の入力欄の文字を隠さない
    if bubble:
        # 吹き出しが右端からはみ出さないよう左へ寄せ、それでも入らなければ短縮する
        need = 20 + len(bubble) * 12.5 + 16
        if x + need > 1168:
            x = max(xmin, 1168 - need)
        maxlen = int((1168 - (x + 20) - 16) / 12.5)
        bubble = bubble[:maxlen] if maxlen >= 3 else ""
    return [text, x, y, bubble]


def _finish(spec, callouts):
    if callouts:
        spec["callouts"] = [_co(spec, c) for c in callouts]
    return spec


TOOL_CHANGE = [["↩", "Enter"], ["▣", "保存"], ["✖", "取消"], ["⇦", "戻る"]]
TOOL_SHOW = [["↩", "Enter"], ["⇩", "次頁"], ["⇧", "前頁"], ["⇦", "戻る"]]


def F(tx, title, sub=None, aria=None, fields=None, section=None, tabs=None, active_tab=None,
      note=None, status=None, toolbar=None, callouts=(), tip=None, window_title=None,
      kind="form", caption=None, **kw):
    s = {"tx": tx, "title": title, "kind": kind, "section": section, "tabs": tabs,
         "active_tab": active_tab, "fields": fields, "note": note,
         "status": status, "toolbar": toolbar or TOOL_CHANGE,
         "caption": caption or sub, "aria": aria, "tip": tip, "window_title": window_title}
    s.update(kw)
    return _finish({k: v for k, v in s.items() if v is not None}, callouts)


def T(tx, title, sub=None, aria=None, columns=None, rows=None, widths=None, ttitle=None,
      selected=None, tfooter=None, status=None, toolbar=None, callouts=(), tip=None, note=None,
      window_title=None, kind="table", caption=None, **kw):
    t = {"columns": columns, "widths": widths, "rows": rows, "selected": selected}
    if ttitle:
        t["title"] = ttitle
    if tfooter:
        t["footer"] = tfooter
    s = {"tx": tx, "title": title, "kind": kind, "table": t, "section": None, "note": note,
         "status": status, "toolbar": toolbar or TOOL_SHOW,
         "caption": caption or sub, "aria": aria, "tip": tip, "window_title": window_title}
    s.update(kw)
    return _finish({k: v for k, v in s.items() if v is not None}, callouts)


def TR(tx, title, sub=None, aria=None, rows=None, ttitle=None, selected=None, note=None,
       status=None, toolbar=None, callouts=(), tip=None, window_title=None, caption=None):
    tr = {"rows": rows, "selected": selected}
    if ttitle:
        tr["title"] = ttitle
    s = {"tx": tx, "title": title, "kind": "tree", "tree": tr, "note": note,
         "status": status, "toolbar": toolbar or TOOL_SHOW,
         "caption": caption or sub, "aria": aria, "tip": tip, "window_title": window_title}
    return _finish({k: v for k, v in s.items() if v is not None}, callouts)


def SP(tx, title, sub=None, aria=None, fields=None, columns=None, rows=None, widths=None,
       ttitle=None, selected=None, split_ratio=0.45, section=None, status=None, toolbar=None,
       callouts=(), tip=None, note=None, tfooter=None, window_title=None, caption=None):
    t = {"columns": columns, "widths": widths, "rows": rows, "selected": selected}
    if ttitle:
        t["title"] = ttitle
    if tfooter:
        t["footer"] = tfooter
    s = {"tx": tx, "title": title, "kind": "split", "split_ratio": split_ratio,
         "fields": fields, "table": t, "section": section, "note": note,
         "status": status, "toolbar": toolbar or TOOL_CHANGE,
         "caption": caption or sub, "aria": aria, "tip": tip, "window_title": window_title}
    return _finish({k: v for k, v in s.items() if v is not None}, callouts)


PARTS = ["spec_config_a.py", "spec_config_b.py", "spec_h12.py", "spec_h345.py", "spec_h5.py"]


def merge_existing(pages, path):
    """既存 gui_spec.json にあってモジュールが生成しないキー（手で足した画面）を
    元の位置のまま残す。「既存のエントリを消さない」ための保険。"""
    if not os.path.exists(path):
        return pages, []
    try:
        old = (json.load(open(path, encoding="utf-8")).get("pages") or {})
    except Exception:
        return pages, []
    if not old:
        return pages, []
    merged, preserved = {}, []
    for page, old_steps in old.items():
        new_steps = pages.get(page)
        if new_steps is None:                       # モジュールが作らないページは丸ごと残す
            merged[page] = old_steps
            preserved += [(page, k) for k in old_steps]
            continue
        merged[page] = {}
        for key, screens in old_steps.items():
            if key in new_steps:
                merged[page][key] = new_steps[key]
            else:
                merged[page][key] = screens
                preserved.append((page, key))
        for key, screens in new_steps.items():      # モジュール側の新規キーは末尾へ
            if key not in merged[page]:
                merged[page][key] = screens
    for page, steps in pages.items():
        if page not in merged:
            merged[page] = steps
    return merged, preserved


def main():
    g = dict(globals())
    g.pop("main", None)
    for p in PARTS:
        path = os.path.join(HERE, p)
        code = compile(open(path, encoding="utf-8").read(), p, "exec")
        exec(code, g)

    out = os.path.join(SITE, "tools", "gui_spec.json")
    pages, preserved = merge_existing(PAGES, out)
    doc = {
        "_comment": "sapeto（受注設計生産 ETO）の手顺ページ用 SAP GUI 画面イメージ仕様。"
                    "tools/gui_spec_build.py が生成する（直接編集しない）。"
                    "生成物は実機のスクリーンショットではなく標準レイアウトに基づく再現イメージ。",
        "pages": pages,
    }
    n = sum(len(v) for p in pages.values() for v in p.values())
    if "--check" in sys.argv:
        print("steps=%d screens=%d (check only)" % (STEP_COUNT[0], n))
        return
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print("wrote %s : steps=%d screens=%d%s" % (
        os.path.relpath(out, SITE), STEP_COUNT[0], n,
        " / 既存キーを保持: %s" % ", ".join("%s#%s" % t for t in preserved) if preserved else ""))


if __name__ == "__main__":
    main()
