#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sap_sd 培训站的 HTML 生成器。

    cd sap_sd && python3 tools/build_pages.py

各 pg_*.py が 1 ページ（または複数ページ）を組み立て、
このスクリプトが sap_sd/ 直下に書き出します。
nav・head・footer は tools/pg_common.py が一元管理するので、
ページを追加しても nav は自動で揃います（verify_site.py の要求を満たす）。
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import pg_index          # noqa: E402
import pg_concept        # noqa: E402
import pg_config         # noqa: E402
import pg_handson        # noqa: E402
import pg_extras         # noqa: E402


def main():
    pages = {
        "index.html": pg_index.build(),
        "concept.html": pg_concept.build(),
        "config.html": pg_config.build(),
    }
    pages.update(pg_handson.build_all())
    pages.update(pg_extras.build_all())

    for name, html in pages.items():
        path = os.path.join(SITE, name)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(html)
        print("wrote %-18s %7d bytes" % (name, len(html.encode("utf-8"))))
    print("total %d pages" % len(pages))


if __name__ == "__main__":
    main()
