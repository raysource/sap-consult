#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sapvc の SAP GUI 画面イメージ仕様（tools/gui_spec.json）を生成する。

    python3 sapvc/tools/gui_spec_build.py      # → sapvc/tools/gui_spec.json

生成物そのものは実機のスクリーンショットではなく、標準レイアウトに基づく再現イメージ。
図の生成と挿入は（親ディレクトリの）tools/make_gui_mockups.py が行う。

gui_spec.json はこのスクリプトの出力であり、手で編集しないこと。
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from gui_spec_config import CONFIG      # noqa: E402
from gui_spec_handson import HANDSON    # noqa: E402
from gui_spec_fixups import apply_fixups  # noqa: E402

SITE_DIR = os.path.dirname(HERE)
OUT = os.path.join(HERE, "gui_spec.json")

COMMENT = ("sapvc（バリアント設定付き受注生産 VC / AVC）の手顺ページ用 SAP GUI 画面イメージ仕様。"
           "sapvc/tools/gui_spec_build.py が生成する（直接編集しない）。"
           "生成物は実機のスクリーンショットではなく標準レイアウトに基づく再現イメージ。")

PAGES = {"config.html": CONFIG}
PAGES.update(HANDSON)


def main():
    fixed = apply_fixups(PAGES)
    n = sum(len(v) for steps in PAGES.values() for v in steps.values())
    steps = sum(len(steps) for steps in PAGES.values())
    doc = {"_comment": COMMENT, "pages": PAGES}
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote %s : %d steps / %d screens / %d callout fixups"
          % (os.path.relpath(OUT, SITE_DIR), steps, n, fixed))


if __name__ == "__main__":
    main()
