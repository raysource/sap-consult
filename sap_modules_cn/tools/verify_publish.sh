#!/usr/bin/env bash
# 发布对账：不看 push 的输出，直接问远端（ls-remote / API / 文件条数）。
#
#   bash tools/verify_publish.sh [repo]
set -euo pipefail
cd "$(dirname "$0")/.."
REPO="${1:-raysource/sap_modules_cn}"

echo "--- local ---"
git rev-parse HEAD
echo "local tracked files: $(git ls-files | wc -l | tr -d ' ')"

echo "--- remote (ls-remote) ---"
git ls-remote --heads "https://github.com/${REPO}.git" | head -3

echo "--- remote (API) ---"
if command -v gh >/dev/null 2>&1; then
  gh api "repos/${REPO}" --jq '"repo: \(.full_name)  visibility: \(.visibility)  pushed: \(.pushed_at)"'
  gh api "repos/${REPO}" --jq '"default_branch: \(.default_branch)"'
  gh api "repos/${REPO}/git/trees/HEAD?recursive=1" --jq '"remote blobs: \([.tree[] | select(.type=="blob")] | length)"'
else
  echo "（没有 gh，跳过 API 对账）"
fi

echo "--- 关键文件能否从远端读回 ---"
for f in index.html mm/index.html pp/index.html fi/index.html co/index.html \
         mm/config.html README.md; do
  code=$(curl -s -o /dev/null -w '%{http_code}' \
    "https://raw.githubusercontent.com/${REPO}/main/${f}")
  printf '%-22s HTTP %s\n' "$f" "$code"
done
