#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""表記揺れの残り（第 2 弾）— tools/fix_term_drift.py のあとに流す。

第 1 弾で拾いきれなかった（または HTML 側にしか無かった）ものを、日本語 SAP の標準表記に寄せる。
sap_sd は生成器（pg_*.py）→ build_pages.py で再生成、sapvc は gui_spec の生成モジュール → gui_spec_build.py →
make_gui_mockups.py の順で反映する。

  python3 tools/fix_term_drift2.py [--dry]
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

# 単純置換（ファイル, 旧, 新）— 件数は問わず全部置換し、数を報告する
SIMPLE = [
    # sapmts: 「受入予定」を「入庫予定」に（第 1 弾の html 側が未適用だった）
    ('sapmts/*.html', '受入予定', '入庫予定'),
    # sapeto: 残り 1 件
    ('sapeto/concept.html', '顧客契約', '得意先契約'),
    # sap_sd: 生成器側を直す（表のセル）
    ('sap_sd/tools/pg_handson.py', 'カスタマ固有', '得意先固有'),
    # sapvc: MB03 = 品目伝票（日本語 SAP の表記）
    ('sapvc/*.html', '資材伝票', '品目伝票'),
    ('sapvc/tools/gui_spec.json', '資材伝票', '品目伝票'),
    ('sapvc/tools/gui_spec_config.py', '資材伝票', '品目伝票'),
    ('sapvc/tools/gui_spec_handson.py', '資材伝票', '品目伝票'),
    ('sapvc/tools/make_vc_xlsx.py', '資材伝票', '品目伝票'),
    # sapmts: 科目 → 勘定（同サイト内は「勘定」で統一）
    ('sapmts/*.html', '転記科目', '転記先の勘定'),
    ('sapmts/*.html', '借方/貸方の科目', '借方/貸方の勘定'),
    ('sapmts/tools/make_mts_xlsx.py', '転記科目', '転記先の勘定'),
    # 分配（＝ assignment）→ 割当
    ('sapvc/*.html', '組織構造の分配未了', '組織構造の割当未了'),
    ('sapvc/*.html', '組織構造が分配済み', '組織構造が割当済み'),
]


def main():
    dry = '--dry' in sys.argv
    total = 0
    for pat, old, new in SIMPLE:
        for path in sorted(glob.glob(pat)):
            s = open(path, encoding='utf-8').read()
            n = s.count(old)
            if not n:
                continue
            if not dry:
                open(path, 'w', encoding='utf-8').write(s.replace(old, new))
            print('  %-42s %-14s ×%d → %s' % (path, old[:14], n, new[:16]))
            total += n
    print('%d 箇所を置換%s' % (total, ' (dry)' if dry else ''))


if __name__ == '__main__':
    main()
