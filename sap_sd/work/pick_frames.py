#!/usr/bin/env python3
"""Dedupe a 1fps 32x24 gray raw stream into 'distinct screen' timestamps.

Usage: python3 pick_frames.py <g.raw> <out.txt> [w] [h] [thresh]
Writes "index<TAB>seconds<TAB>mad" lines, then a plain list of seconds to extract.
"""
import sys

path, out = sys.argv[1], sys.argv[2]
W = int(sys.argv[3]) if len(sys.argv) > 3 else 32
H = int(sys.argv[4]) if len(sys.argv) > 4 else 24
TH = float(sys.argv[5]) if len(sys.argv) > 5 else 3.0

raw = open(path, 'rb').read()
fsz = W * H
n = len(raw) // fsz
frames = [raw[i * fsz:(i + 1) * fsz] for i in range(n)]


def mad(a, b):
    return sum(abs(x - y) for x, y in zip(a, b)) / fsz


kept = [0]
for i in range(1, n):
    if mad(frames[i], frames[kept[-1]]) > TH:
        kept.append(i)

with open(out, 'w') as fh:
    for i in kept:
        fh.write('%d\t%d\t%.2f\n' % (i, i, mad(frames[i], frames[kept[-1]])))

print('total 1fps frames:', n)
print('distinct screens :', len(kept))
print('seconds (first 60):', kept[:60])
