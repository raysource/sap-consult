#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
站点生成器: 由 Python 模板生成全部静态 HTML
用法(在 btp-dev-hub 根目录):
    python3 tools/sitegen/generate.py
输出: 站点根目录下的 *.html (与 assets/、projects/、data/ 平级)
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_TOOLS = os.path.dirname(_HERE)
_ROOT = os.path.dirname(_TOOLS)
if _TOOLS not in sys.path:
    sys.path.insert(0, _TOOLS)   # 使 `from sitegen.helpers import *` 可用

from sitegen.helpers import shell, esc  # noqa: E402
from sitegen.pages_home import page_index, page_isuite  # noqa: E402
from sitegen.pages_int import page_iflow, page_fiori  # noqa: E402
from sitegen.pages_ext import page_rap, page_cap, page_samples  # noqa: E402
from sitegen.pages_course import page_devcourse  # noqa: E402

PAGES = {
    "index.html": page_index,
    "isuite.html": page_isuite,
    "iflow.html": page_iflow,
    "fiori.html": page_fiori,
    "rap.html": page_rap,
    "cap.html": page_cap,
    "dev-course.html": page_devcourse,
    "samples.html": page_samples,
}


def main():
    for fname, factory in PAGES.items():
        meta = factory()
        html = shell(meta["title"], meta["desc"], meta["active"], meta["body"])
        out = os.path.join(_ROOT, fname)
        with open(out, "w", encoding="utf-8") as f:
            f.write(html)
        print("wrote %-16s (%d KB)" % (fname, len(html.encode("utf-8")) // 1024))
    print("done ->", _ROOT)


if __name__ == "__main__":
    main()
