#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""同語多訳（terminology drift）の横断監査。

並列に翻訳したバッチ間で「同じ中国語が違う日本語になっている」箇所を機械的に洗い出す。

  1) IMG パスのセグメント整列 — 同じ中国語セグメントに複数の日本語訳があるものを列挙
     （SPRO のメニュー名は学習者が画面で探す語なので、ここが揺れると実害が出る）
  2) 用語集の期待訳が本文に現れない行 — glossary.json の対訳を使っていない疑いのある行
  3) 概念ごとの表記揺れチェック — 明細行/明細レベル、ヘッダ/伝票ヘッダ などの候補形を数える

  python3 work/term_audit.py
"""
import json
import os
import re
import sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

SEP = re.compile(r'\s*(?:→|->|－|-＞)\s*')


def load():
    mz = json.load(open('work/ja/model_atoms.json', encoding='utf-8'))
    mj = json.load(open('work/ja/model_map.json', encoding='utf-8'))
    sz = json.load(open('work/ja/src_atoms.json', encoding='utf-8'))
    sj = json.load(open('work/ja/src_map.json', encoding='utf-8'))
    return list(mz.items()) + list(sz.items()), dict(mj, **sj)


def path_segments(text):
    return [x for x in SEP.split(text) if x.strip()]


def audit_paths(pairs, tr):
    """同じ中国語セグメント → 複数の日本語セグメント を検出。"""
    zh2ja = defaultdict(Counter)
    for k, zh in pairs:
        ja = tr.get(k)
        if not ja:
            continue
        zs, js = path_segments(zh), path_segments(ja)
        if len(zs) < 3 or len(zs) != len(js):
            continue
        for a, b in zip(zs, js):
            zh2ja[a.strip()][b.strip()] += 1
    drift = {a: c for a, c in zh2ja.items() if len(c) > 1}
    return drift, len(zh2ja)


def audit_glossary(pairs, tr):
    """用語集の日本語訳が訳文に現れない行（＝別の語で訳された疑い）。"""
    g = json.load(open('work/ja/glossary.json', encoding='utf-8'))['terms']
    out = defaultdict(list)
    for k, zh in pairs:
        ja = tr.get(k)
        if not ja:
            continue
        for zt, jt in g.items():
            # 用語集の日本語の「核」で照合（長いものだけ：短い語は誤検知が多い）
            core = re.sub(r'（[^）]*）', '', jt).strip()
            if len(core) < 3 or zt not in zh:
                continue
            if core not in ja:
                out[(zt, jt)].append((zh, ja))
    return out


CONCEPTS = [
    ('明細行（伝票の明細）', ['明細行', '明細レベル', '行項目', 'アイテム行']),
    ('伝票ヘッダ', ['伝票ヘッダ', 'ヘッダレベル', 'ヘッダ']),
    ('得意先', ['得意先', '顧客', 'カスタマ']),
    ('仕入先', ['仕入先', 'ベンダ', 'サプライヤ']),
    ('品目', ['品目', 'マテリアル', '資材']),
    ('プラント', ['プラント', '工場']),
    ('保管場所', ['保管場所', '倉庫', 'ストレージロケーション']),
    ('転記', ['転記', '記帳', 'ポスティング']),
    ('伝票', ['伝票', 'ドキュメント']),
    ('配賦', ['配賦', 'ディストリビューション']),
    ('按分', ['按分', 'アセスメント']),
    ('指図', ['指図', 'オーダ']),
    ('所要量チェック', ['所要量チェック', '在庫チェック', 'アベイラビリティチェック']),
    ('決済', ['決済', '精算', 'セツルメント']),
    ('販売エリア', ['販売エリア', 'セールスエリア']),
    ('原価センタ', ['原価センタ', 'コストセンター']),
    ('評価クラス', ['評価クラス', 'バリュエーションクラス']),
    ('与信管理領域', ['与信管理領域', 'クレジット管理領域']),
    ('品目タイプ', ['品目タイプ', 'マテリアルタイプ']),
    ('計画手配', ['計画手配', '計画オーダ']),
    ('購買発注', ['購買発注', '購買オーダ']),
    ('出荷', ['出荷', 'シッピング']),
    ('請求書', ['請求書', 'インボイス']),
    ('入庫', ['入庫', 'グッズレシート', 'GR']),
    ('勘定', ['勘定', 'アカウント']),
    ('マスタデータ', ['マスタデータ', 'マスタレコード']),
    ('作業区', ['作業区', 'ワークセンタ']),
    ('工順', ['工順', 'ルーティング']),
    ('完成品', ['完成品', '製品']),
    ('会社コード', ['会社コード', 'カンパニーコード']),
    ('原価要素', ['原価要素', 'コストエレメント']),
    ('管理会計領域', ['管理会計領域', 'コントローリング領域']),
    ('棚卸資産', ['棚卸資産', '在庫']),
    ('機能', ['機能', 'ファンクション']),
]


def audit_concepts(maps):
    allv = []
    for m in maps:
        allv += list(m.values())
    rows = []
    for label, forms in CONCEPTS:
        c = Counter()
        for v in allv:
            for f in forms:
                c[f] += v.count(f)
        present = [f for f in forms if c[f]]
        if len(present) > 1:
            ctx = {}
            for f in present:
                for v in allv:
                    if f in v:
                        i = v.find(f)
                        ctx[f] = v[max(0, i - 26):i + len(f) + 26].replace('\n', ' ')
                        break
            rows.append((label, [(f, c[f]) for f in present], ctx))
    return rows


def main():
    pairs, tr = load()
    print('=== 1) IMG パスのセグメント揺れ ===')
    drift, nseg = audit_paths(pairs, tr)
    print('（整列できた中国語セグメント %d 種 / 揺れ %d 種）' % (nseg, len(drift)))
    for a, c in sorted(drift.items(), key=lambda kv: -sum(kv[1].values())):
        print('  %-28s → %s' % (a, ' ／ '.join('%s ×%d' % (b, n) for b, n in c.most_common())))

    print('\n=== 2) 用語集の訳語が本文に無い行 ===')
    g = audit_glossary(pairs, tr)
    for (zt, jt), rows in sorted(g.items(), key=lambda kv: -len(kv[1]))[:25]:
        print('  %-16s (期待: %s)  例: %s' % (zt, jt, rows[0][1][:80]))
    print('  計 %d 語で不一致' % len(g))

    print('\n=== 3) 概念ごとの表記揺れ ===')
    maps = [json.load(open('work/ja/model_map.json', encoding='utf-8')),
            json.load(open('work/ja/src_map.json', encoding='utf-8'))]
    for label, forms, ctx in audit_concepts(maps):
        print('  %-22s %s' % (label, ' ／ '.join('%s ×%d' % (f, n) for f, n in forms)))
        for f, _, in [(f, n) for f, n in forms]:
            print('        %-14s … %s' % (f, ctx.get(f, '')[:88]))


if __name__ == '__main__':
    main()
