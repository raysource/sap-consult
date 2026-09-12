#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""表記揺れの一括修正（tools/term_consistency_audit.py の指摘に対する修正）。

  - 明細タイプ / 項目カテゴリ / 請求項目カテゴリ → 明細カテゴリ / 請求明細カテゴリ
  - 受入予定 / 受入処理時間 / 受入数量        → 入庫予定 / 入庫処理時間 / 入庫数量
  - ワークセンター                            → 作業区
  - 顧客                                      → 得意先
  - 払出                                      → 出庫
生成ツール（make_*_xlsx.py, spec_*.py）にも同じ語が出るので併せて直す（再生成で戻らないように）。
ページ生成器を持つサイト（sap_sd）は pg_*.py を直して build_pages.py で再生成する。

  python3 tools/fix_term_drift.py [--dry]
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

FIXES = [
    ('sapmts/config.html', '明細タイプ', '明細カテゴリ', 3),
    ('sapmts/worksheet.html', '明細タイプ', '明細カテゴリ', 1),
    ('sapmts/tools/make_mts_xlsx.py', '明細タイプ', '明細カテゴリ', 1),
    ('sapmts/config.html', '明细：一般データを确认（明細カテゴリ', '明細：一般データを確認（明細カテゴリ', 1),
    ('sapmts/config.html', '受入処理時間', '入庫処理時間', 1),
    ('sapmts/tools/make_mts_xlsx.py', '受入予定', '入庫予定', 2),
    ('sapmto/config.html', '請求項目カテゴリ', '請求明細カテゴリ', 1),
    ('sapmto/config.html', '受入処理時間', '入庫処理時間', 2),
    ('sapmto/tools/make_mto_xlsx.py', '受入処理時間', '入庫処理時間', 1),
    ('sapmto/handson-5.html', 'で部品を受入 → 库存恢复。', 'で部品を入庫 → 在庫が回復します。', 1),
    ('sapmto/handson-5.html', 'で受入します。', 'で入庫します。', 1),
    ('sapeto/handson-5.html', '支給/受入の流れ', '支給/入庫の流れ', 1),
    ('sapeto/handson-5.html', '支給と受入', '支給と入庫', 1),
    ('sapeto/tools/spec_config_b.py', '受入/払出数量', '入庫/出庫数量', 1),
    ('sapeto/tools/spec_h12.py', '受入/払出数量', '入庫/出庫数量', 1),
    ('sapeto/tools/spec_h5.py', '支給と受入', '支給と入庫', 1),
    ('sapeto/handson-5.html', 'ワークセンター', '作業区', 1),
    ('sapeto/handson-4.html', 'からの払出しになる', 'からの出庫になる', 1),
    ('sapvc/handson-4.html', '材料払出', '材料の出庫', 1),
    ('sap_sd/tools/pg_config.py', '顧客', '得意先', 20),
    ('sap_sd/tools/pg_extras.py', '顧客', '得意先', 8),
    ('sap_sd/tools/pg_index.py', '顧客', '得意先', 5),
    ('sap_sd/tools/pg_concept.py', '顧客', '得意先', 2),
    ('sap_sd/tools/pg_handson.py', '顧客', '得意先', 1),
    ('sap_sd/tools/make_sd_xlsx.py', '顧客', '得意先', 3),
    ('sapvc/concept.html', '顧客', '得意先', 2),
    ('saporderflow/compare.html', '顧客', '得意先', 3),
    ('saporderflow/vc.html', '顧客', '得意先', 1),
    ('saporderflow/quiz.html', '顧客', '得意先', 2),
    ('saporderflow/scenario-eq.html', '顧客', '得意先', 2),
    ('saporderflow/instructor.html', '顧客', '得意先', 7),
    ('saporderflow/tools/make_cmp_xlsx.py', '顧客', '得意先', 4),
    # --- GUI モックアップ（tools/gui_spec*.json / spec_*.py）内の文字も同じ語に寄せる
    #     ※ MD04 の列名「受入/払出」「受入/払出数量」は日本語 SAP の画面表記なので触らない
    ('sap_sd/tools/gui_spec.d/config_c0_c5.json', '顧客', '得意先', 11),
    ('sapmts/tools/gui_spec.json', '受入予定', '入庫予定', 9),
    ('sapmts/tools/gui_spec.json', '受入数量', '入庫数量', 8),
    ('sapmts/tools/gui_spec.json', '明細タイプ', '明細カテゴリ', 1),
    ('sapmto/tools/gui_spec.json', '項目カテゴリ', '明細カテゴリ', 1),
    ('sapmto/tools/gui_spec.json', '受入処理時間', '入庫処理時間', 2),
    ('sapmto/tools/gui_spec.json', '受入します。', '入庫します。', 1),
    ('sapeto/tools/spec_config_b.py', 'Q からの払出しです。', 'Q からの出庫です。', 1),
    ('sapeto/tools/spec_h345.py', 'Q からの払出しになる', 'Q からの出庫になる', 1),
    ('sapeto/tools/spec_h345.py', '"Q からの払出し"', '"Q からの出庫"', 1),
    ('sapvc/tools/gui_spec_handson.py', '指図への材料払出', '指図への材料の出庫', 1),
    ('sapvc/tools/gui_spec_handson.py', '（指図への払出）', '（指図への出庫）', 1),
]

# 翻訳サイト側（sap_sd_jp）は「译文の地図」を直して再適用する
MAP_FIX = [('sap_sd_jp/work/ja/model_map.json', '項目カテゴリ', '明細カテゴリ')]


def main():
    dry = '--dry' in sys.argv
    bad = []
    for path, old, new, want in FIXES:
        s = open(path, encoding='utf-8').read()
        n = s.count(old)
        if n != want:
            if n == 0 and new in s:
                continue                      # すでに適用済み（再実行）
            bad.append('%s: %r は %d 件（想定 %d）' % (path, old[:22], n, want))
            continue
        if not dry:
            open(path, 'w', encoding='utf-8').write(s.replace(old, new))
        print('  %-38s %-16s ×%d → %s' % (path, old[:16], n, new[:18]))

    for path, old, new in MAP_FIX:
        m = json.load(open(path, encoding='utf-8'))
        n = sum(1 for v in m.values() if old in v)
        if n:
            for k, v in list(m.items()):
                if old in v:
                    m[k] = v.replace(old, new)
            if not dry:
                json.dump(m, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=0,
                          sort_keys=True)
            print('  %-38s %-16s ×%d → %s' % (path.split('/')[-1], old, n, new))

    if bad:
        print('\n想定件数と違う箇所:')
        for b in bad:
            print('  -', b)
        sys.exit(1)
    print('term drift fixes applied%s' % (' (dry)' if dry else ''))


if __name__ == '__main__':
    main()
