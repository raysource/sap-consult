# -*- coding: utf-8 -*-
"""sapvc の SAP GUI 画面イメージ仕様（tools/gui_spec.json）を組み立てるヘルパー。

生成物は実機のスクリーンショットではなく、標準レイアウトに基づく再現イメージ。
座標系（tools/GUI_SPEC_FORMAT.md）:
  1180x760 / タイトルバー 0-32 / メニュー 32-56 / ツールバー 56-84 / タブ 84-110
  本文は y=110 から。form は 1 行目 y≈150 から 50px 刻み、2 列目 x≈600。
  table はヘッダー y≈150 付近、行は 26px 刻み。
"""

# 標準ツールバー（Enter / 保存 / 戻る）
TB = [["↩", "Enter"], ["▣", "保存"], ["⇦", "戻る"], ["✖", "取消"]]
TB_VIEW = [["↩", "Enter"], ["⌕", "検索"], ["⇦", "戻る"], ["▤", "全体"]]


def callout(text, x, y, badge=None):
    return [text, x, y] if badge is None else [text, x, y, badge]


def form(tx, title, caption, aria, tip, status, section=None, fields=None, tabs=None,
         active_tab=0, note=None, callouts=None, toolbar=None):
    s = {"tx": tx, "title": title, "kind": "form", "caption": caption,
         "aria": aria, "tip": tip, "status": list(status)}
    if section:
        s["section"] = section
    if fields:
        s["fields"] = fields
    if tabs:
        s["tabs"] = tabs
        s["active_tab"] = active_tab
    if note:
        s["note"] = note
    if callouts:
        s["callouts"] = callouts
    s["toolbar"] = toolbar or TB
    return s


def table(tx, title, caption, aria, tip, status, columns, widths, rows,
          table_title=None, selected=None, footer=None, note=None, callouts=None, toolbar=None):
    t = {"columns": columns, "widths": widths, "rows": rows}
    if table_title:
        t["title"] = table_title
    if selected is not None:
        t["selected"] = selected
    if footer:
        t["footer"] = footer
    s = {"tx": tx, "title": title, "kind": "table", "table": t, "caption": caption,
         "aria": aria, "tip": tip, "status": list(status)}
    if note:
        s["note"] = note
    if callouts:
        s["callouts"] = callouts
    s["toolbar"] = toolbar or TB_VIEW
    return s


# よく使う注意書き（tip の定型）
def tip_check(txt):
    return "自システムでの確認：" + txt
