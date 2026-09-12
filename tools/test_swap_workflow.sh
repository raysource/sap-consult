#!/usr/bin/env bash
# 実機スクリーンショット差し替えワークフローの自己テスト（saporderflow で実行）
# 生成 SVG を「撮影した画像」に見立てて .png を作り、apply → note --sync → 検証 → revert まで通す。
set -euo pipefail
cd "$(dirname "$0")"
R=/Users/jason/Desktop/work/training
SITE=saporderflow
G=$R/$SITE/assets/gui
CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

echo "=== 0. 事前状態 ==="
PAGES="compare.html scenario-eq.html vc.html"
for p in $PAGES; do shasum "$R/$SITE/$p" | cut -c1-12 | tr '\n' ' '; echo "$p"; done
python3 $R/tools/verify_gui_figures.py $SITE | tail -1

echo "=== 1. テスト画像を作る（SVG をラスタライズして『差し替え後』の名前で置く） ==="
# vc.html の全 6 枚 + compare/scenario-eq の 1 枚ずつを「撮影済み」に見立てる
ALL=$(ls $G/vc_s*.svg | xargs -n1 basename | sed 's/.svg//')
for f in $ALL compare_s01_1 scenario-eq_s01_1; do
  "$CH" --headless=new --disable-gpu --hide-scrollbars --screenshot="$G/$f.png" \
        --window-size=1180,760 "file://$G/$f.svg" >/dev/null 2>&1
  echo "  作成: $f.png ($(stat -f%z "$G/$f.png") bytes)"
done

echo "=== 2. --status（何枚差し替えできるか） ==="
python3 $R/tools/swap_gui_images.py $SITE --status

echo "=== 3. dry-run ==="
python3 $R/tools/swap_gui_images.py $SITE | grep -E "^(compare|scenario-eq|vc|    )" | head -6

echo "=== 4. --apply（src を .png に書き換え） ==="
python3 $R/tools/swap_gui_images.py $SITE --apply | tail -2

echo "=== 5. 注意書きを同期（実機画像だけのページは外れる） ==="
python3 $R/tools/add_gui_note.py $SITE --sync

echo "=== 6. 構造・網羅の検証 ==="
(cd $R/$SITE && python3 ~/.hermes/skills/productivity/sap-training-sites/scripts/verify_site.py . | tail -1)
python3 $R/tools/verify_gui_figures.py $SITE | tail -1

echo "=== 7. --revert（生成図に戻す）＋ 注意書きを戻す ==="
python3 $R/tools/swap_gui_images.py $SITE --revert | tail -1
python3 $R/tools/add_gui_note.py $SITE --sync

echo "=== 8. 事前状態と一致するか（ハッシュ比較） ==="
ok=1
for p in $PAGES; do
  h=$(shasum "$R/$SITE/$p" | cut -c1-12)
  echo "  $h $p"
done
rm -f "$G"/*.png
echo "  （テスト画像を削除）"
python3 $R/tools/verify_gui_figures.py $SITE | tail -1
