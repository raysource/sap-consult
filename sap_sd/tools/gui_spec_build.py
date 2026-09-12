#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sap_sd の SAP GUI 画面イメージ仕様（tools/gui_spec.json）を組み立てる。

    python3 sap_sd/tools/gui_spec_build.py

断片（tools/gui_spec.d/*.json）を決まった順序でマージして gui_spec.json を作る。
gui_spec.json はこのスクリプトの出力であり、直接編集しないこと。
断片は担当ページごとに 1 ファイル（並行作業しても衝突しない）。

生成物は実機のスクリーンショットではなく、標準レイアウトに基づく再現イメージ。
図の生成と挿入は親ディレクトリの tools/make_gui_mockups.py が行う。
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
FRAG_DIR = os.path.join(HERE, "gui_spec.d")
OUT = os.path.join(HERE, "gui_spec.json")

# キーの正式な順序（この順に出力する。断片が欠けているキーはエラー）
ORDER = {
    "config.html": ["c%d" % i for i in range(17)],
    "handson-1.html": ["1-1 VA01 初期画面", "1-2 概況画面", "1-3 明細の入力",
                       "1-4 保存と伝票フロー", "1-5 証拠を取る"],
    "handson-2.html": ["2-1 変更の 3 方式", "2-2 プラント変更", "2-3 得意先変更と再決定",
                       "2-4 ブロックの 3 階層", "2-5 証拠を取る"],
    "handson-3.html": ["3-1 初期画面と照会", "3-2 情報ビュー", "3-3 与信情報",
                       "3-4 Last SD documents", "3-5 出荷伝票へのドリルダウン",
                       "3-6 出てこないときの切り分け"],
    "handson-4.html": ["4-1 出荷できる受注", "4-2 出荷伝票の作成", "4-3 ピッキングと出庫過帳",
                       "4-4 出荷伝票の照会", "4-5 請求", "4-6 伝票フローと Sales Summary"],
    "handson-5.html": ["5-1 ツールとヘルプ", "5-2 発展①", "5-3 発展②", "5-4 発展③",
                       "5-5 発展④", "5-6 故障対応の 4 画面"],
}

COMMENT = ("sap_sd（SAP SD 受注処理 / Sales Order Processing）の手顺ページ用 SAP GUI 画面イメージ仕様。"
           "sap_sd/tools/gui_spec_build.py が tools/gui_spec.d/*.json から生成する（直接編集しない）。"
           "生成物は実機のスクリーンショットではなく標準レイアウトに基づく再現イメージ。")


def main():
    frags = {}
    if os.path.isdir(FRAG_DIR):
        for fn in sorted(os.listdir(FRAG_DIR)):
            if not fn.endswith(".json"):
                continue
            d = json.load(open(os.path.join(FRAG_DIR, fn), encoding="utf-8"))
            for page, steps in d.items():
                frags.setdefault(page, {}).update(steps)

    pages = {}
    missing = []
    for page, keys in ORDER.items():
        got = frags.get(page, {})
        pages[page] = {}
        for k in keys:
            if k not in got:
                missing.append("%s / %s" % (page, k))
                continue
            pages[page][k] = got[k]
        extra = [k for k in got if k not in keys]
        for k in extra:
            missing.append("%s / %s (順序定義に無いキー)" % (page, k))

    if missing:
        print("断片が不足しています（%d 件）:" % len(missing))
        for m in missing:
            print("  -", m)
        print("\n※ 断片は tools/gui_spec.d/ に置いてください（1 ページ 1 ファイル推奨）。")
        return 1

    n_sc = sum(len(v) for st in pages.values() for v in st.values())
    n_step = sum(len(st) for st in pages.values())
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump({"_comment": COMMENT, "pages": pages}, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    print("wrote %s : %d steps / %d screens" % (os.path.relpath(OUT, SITE), n_step, n_sc))
    return 0


if __name__ == "__main__":
    sys.exit(main())
