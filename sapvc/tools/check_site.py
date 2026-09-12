#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sapvc 追加検証（verify_site.py を補完する）。

チェック内容（verify_site.py が拾わないもの）:
  1) すべての href="file.html#anchor" のリンク先ファイルとアンカーが存在するか（同一ページ内 #anchor も含む）
  2) id 属性の重複がないか（ページ内）
  3) quiz-q が「4 択・キー A〜D ちょうど 1 回ずつ・data-answer がその中に含まれる・div.explain が 1 つ」か
  4) <td> の中に紛れた裸の "|" がないか（表が崩れる typo）
  5) 全アセット参照（css/js/img）が実在するか
  6) ページ数の申告（11）と、各ページの h1 が 1 つだけか

Usage: python3 tools/check_site.py [site_dir]
"""
import glob
import os
import re
import sys

REQUIRED = ["index.html", "concept.html", "config.html",
            "handson-1.html", "handson-2.html", "handson-3.html",
            "handson-4.html", "handson-5.html",
            "instructor.html", "worksheet.html", "quiz.html"]


def main(root=None):
    root = root or os.getcwd()
    issues = []
    pages = sorted(glob.glob(os.path.join(root, "*.html")))
    names = {os.path.basename(p) for p in pages}

    # 6) 必須ページ
    for req in REQUIRED:
        if req not in names:
            issues.append(f"missing required page: {req}")

    total_q = 0
    for path in pages:
        base = os.path.basename(path)
        s = open(path, encoding="utf-8").read()

        # 2) id 重複
        ids = re.findall(r'\sid="([^"]+)"', s)
        dup = {i for i in ids if ids.count(i) > 1}
        if dup:
            issues.append(f"{base}: duplicate id -> {sorted(dup)}")

        # 1) アンカー解決
        for href in re.findall(r'href="([^"]+)"', s):
            if href.startswith(("http://", "https://", "mailto:")):
                continue
            file_part, _, frag = href.partition("#")
            if file_part == "":
                if frag and frag not in ids:
                    issues.append(f"{base}: in-page anchor not found -> #{frag}")
                continue
            if file_part.endswith(".html"):
                if file_part not in names:
                    issues.append(f"{base}: link target missing -> {file_part}")
                elif frag:
                    tgt = open(os.path.join(root, file_part), encoding="utf-8").read()
                    tgt_ids = set(re.findall(r'\sid="([^"]+)"', tgt))
                    if frag not in tgt_ids:
                        issues.append(f"{base}: {file_part}#{frag} anchor not found")

        # 5) アセット参照
        for src in re.findall(r'src="([^"]+)"', s) + re.findall(r'<link[^>]+href="([^"]+\.css)"', s):
            if src.startswith(("http://", "https://")):
                continue
            if not os.path.exists(os.path.join(root, src)):
                issues.append(f"{base}: asset missing -> {src}")

        # 3) quiz 設問の構造
        qs = re.findall(r'<div class="quiz-q" data-answer="([A-Z])">(.*?)<div class="explain">', s, re.S)
        total_q += len(qs)
        if qs:
            for i, (ans, body) in enumerate(qs, 1):
                keys = re.findall(r'data-key="([A-Z])"', body)
                if len(keys) != 4 or sorted(keys) != ["A", "B", "C", "D"]:
                    issues.append(f"{base}: quiz #{i} keys={keys} (want exactly A,B,C,D)")
                if ans not in keys:
                    issues.append(f"{base}: quiz #{i} data-answer={ans} not in keys")
            n_expl = len(re.findall(r'<div class="explain">', s))
            if n_expl != len(qs):
                issues.append(f"{base}: explain count {n_expl} != question count {len(qs)}")

        # 4) <td> 内の裸の "|"
        for td in re.findall(r"<td[^>]*>(.*?)</td>", s, re.S):
            if re.search(r"(?<![&]) \| ", td) and "<code>" not in td:
                issues.append(f"{base}: stray '|' inside <td> -> {td[:40]!r}")

        # h1 は 1 つ
        if len(re.findall(r"<h1[ >]", s)) != 1:
            issues.append(f"{base}: h1 count != 1")

    if issues:
        print("ISSUES (%d):" % len(issues))
        for it in issues:
            print("  -", it)
        return 1
    print(f"PASS: {len(pages)} pages, anchors+ids+assets resolved, quiz {total_q} questions "
          "(4 options A-D each, answer in keys, 1 explain each), no stray '|' in <td>")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
