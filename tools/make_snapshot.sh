#!/usr/bin/env bash
# Snapshot the training ecosystem: index + shared assets/tools + every site's
# source-of-truth only (no source media, no regenerable derived artifacts).
#
#   bash tools/make_snapshot.sh
#
# Excluded on purpose:
#   - the source materials the user provided (S4.docx, *.mp4, work/audio/*)
#   - the docx unpack dir (sap_sd_cn/work/docx_extract: 1385 raw media + document.xml)
#   - everything one build command away from the sources:
#     assets/gui_png/*, *_画面PNG.zip, *_講義用画面集.pdf, *_学员用記入シート.pdf, work/render/*
set -euo pipefail
cd /Users/jason/Desktop/work/training
TS="${TS:-$(date +%Y%m%d_%H%M%S)}"   # TS を渡せば同名で再作成（進捗メモに書いた名前を維持するため）
OUT="_snapshots/sap_training_sites_10sites_${TS}.tar.gz"
LIST=/tmp/snap_list.txt
mkdir -p _snapshots

find PROGRESS.md index.html assets tools \
     sap_sd sapmto sapeto sapmts sapvc saporderflow sap_sd_cn sap_sd_jp sap_cn \
     sap_modules_cn \
     -type f \
  ! -path '*/gui_png/*' \
  ! -path '*/.git/*' \
  ! -path '*/work/audio/*' \
  ! -path 'sap_modules_cn/work/shots/*' \
  ! -path 'sap_sd/work/*' \
  ! -path 'sapmto/work/*' \
  ! -path 'sapeto/work/*' \
  ! -path 'sapmts/work/*' \
  ! -path 'sapvc/work/*' \
  ! -path 'saporderflow/work/*' \
  ! -path 'sap_sd_cn/work/docx_extract/*' \
  ! -path 'sap_sd_cn/work/render/*' \
  ! -path 'sap_sd_jp/work/docx_extract/*' \
  ! -path 'sap_sd_jp/work/render/*' \
  ! -name '*.mp4' \
  ! -name '*.docx' \
  ! -name '*_画面PNG.zip' \
  ! -name '*_講義用画面集.pdf' \
  ! -name '*_学员用記入シート.pdf' \
  ! -name '.DS_Store' \
  -print > "$LIST"

echo "対象ファイル数: $(wc -l < "$LIST" | tr -d ' ')"
tar -czf "$OUT" -T "$LIST"
gzip -t "$OUT"
echo "gzip OK: $OUT"
ls -lh "$OUT"

echo "--- 検算（アーカイブ内 == ディスク上）---"
echo "svg  : list=$(grep -c '\.svg$' "$LIST")  disk=$(find sap_sd sapmto sapeto sapmts sapvc saporderflow -name '*.svg' -path '*/gui/*' | wc -l | tr -d ' ')"
echo "html : list=$(grep -c '\.html$' "$LIST")  disk=$(find index.html assets tools sap_sd_jp sap_sd_cn sap_cn sap_modules_cn sap_sd sapmto sapeto sapmts sapvc saporderflow -name '*.html' ! -path '*/work/*' | wc -l | tr -d ' ')"
echo "xlsx : list=$(grep -c '\.xlsx$' "$LIST")  disk=$(find sap_sd_jp sap_sd_cn sap_cn sap_modules_cn sap_sd sapmto sapeto sapmts sapvc saporderflow -maxdepth 1 -name '*.xlsx' | wc -l | tr -d ' ')"
echo "py   : list=$(grep -c '\.py$' "$LIST")"
echo "sap_cn 画面: list=$(grep -c 'sap_cn/assets/img/.*\.\(png\|jpeg\|jpg\)$' "$LIST")  disk=$(find sap_cn/assets/img -type f | wc -l | tr -d ' ')"
echo "sap_cn 自绘图: list=$(grep -c 'sap_cn/assets/diagrams/.*\.svg$' "$LIST")  disk=$(find sap_cn/assets/diagrams -name '*.svg' | wc -l | tr -d ' ')"
echo "sap_modules_cn 画面: list=$(grep -c 'sap_modules_cn/assets/img/.*\.\(png\|jpeg\|jpg\)$' "$LIST")  disk=$(find sap_modules_cn/assets/img -type f | wc -l | tr -d ' ')"
echo "sap_modules_cn 自绘图: list=$(grep -c 'sap_modules_cn/assets/diagrams/.*\.svg$' "$LIST")  disk=$(find sap_modules_cn/assets/diagrams -name '*.svg' | wc -l | tr -d ' ')"
echo "sap_sd_jp 画面: list=$(grep -c 'sap_sd_jp/assets/img/.*\.\(png\|jpeg\|jpg\)$' "$LIST")  disk=$(find sap_sd_jp/assets/img -type f | wc -l | tr -d ' ')"
echo "sap_sd_cn 画面: list=$(grep -c 'sap_sd_cn/assets/img/.*\.\(png\|jpeg\|jpg\)$' "$LIST")  disk=$(find sap_sd_cn/assets/img -type f | wc -l | tr -d ' ')"
echo "除外確認 → mp4=$(grep -c '\.mp4$' "$LIST" || true)  docx=$(grep -c 'S4\.docx$' "$LIST" || true)  docx_extract=$(grep -c 'docx_extract' "$LIST" || true)  gui_png=$(grep -c 'assets/gui_png' "$LIST" || true)  pdf=$(grep -c '題用画面集\.pdf\|講義用画面集\.pdf' "$LIST" || true)"
