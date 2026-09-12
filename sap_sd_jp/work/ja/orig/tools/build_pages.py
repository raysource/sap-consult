#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build every page of the S/4HANA 中文实训站 from work/site_model.json.

Usage:  python3 tools/build_pages.py [page ...]
        (no args = all pages)
After a rebuild, re-run the verifiers:
        python3 ~/.hermes/skills/productivity/sap-training-sites/scripts/verify_site.py .
        python3 tools/verify_site_cn.py
"""
import os
import sys
import importlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, 'sitegen'))
os.chdir(ROOT)

import common  # noqa: E402
import pg_module  # noqa: E402
import pg_static  # noqa: E402
import pg_teach  # noqa: E402

WANT = sys.argv[1:]


def want(name):
    return not WANT or name in WANT


def write(fname, html_text):
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(html_text)
    print(f'  {fname:20s} {len(html_text) / 1024:8.1f} KB  {len(html_text.splitlines()):6d} 行')


def main():
    print('build pages →', ROOT)
    if want('modules'):
        for code in pg_module.ORDER:
            write(pg_module.mod_of(code)['file'], pg_module.build(code))
    if want('index'):
        write('index.html', pg_static.build_index())
    if want('tasks'):
        write('tasks.html', pg_static.build_tasks())
    if want('tcode'):
        write('tcode.html', pg_static.build_tcode())
    if want('issues'):
        write('issues.html', pg_static.build_issues())
    if want('instructor'):
        write('instructor.html', pg_teach.build_instructor())
    if want('worksheet'):
        write('worksheet.html', pg_teach.build_worksheet())
    if want('quiz'):
        write('quiz.html', pg_teach.build_quiz())

    # report our real numbers to the shared hub generator (this site has no SVG mockups)
    import json
    pages = [pg_module.mod_of(c)['file'] for c in pg_module.ORDER] + \
            ['index.html', 'tasks.html', 'tcode.html', 'issues.html',
             'instructor.html', 'worksheet.html', 'quiz.html']
    import pg_static as _ps
    st = _ps.stats()
    json.dump({'n_pages': len(pages), 'n_steps': st['steps'], 'figs': st['shots'],
               'n_cfg': 0, 'has_wbs': True, 'note': 'S/4HANA 中文实训站: 実機スクリーンショット站（生成 SVG ではない）'},
              open('tools/hub_stats.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('  tools/hub_stats.json  pages=%d steps=%d figs=%d' % (len(pages), st['steps'], st['shots']))
    print('done.')


if __name__ == '__main__':
    main()
