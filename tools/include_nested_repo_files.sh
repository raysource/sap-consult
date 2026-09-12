#!/usr/bin/env bash
# ============================================================
# include_nested_repo_files.sh <parent-repo-dir> <nested-dir> [nested-dir ...]
#
# Why: `git add` **silently does nothing** for paths inside an embedded repository
#      (a subdirectory that has its own .git). Verified on git 2.39 (Apple Git):
#        $ git add -f sap_sd_cn/README.md ; echo $?   → 0
#        $ git ls-files -- sap_sd_cn                  → (empty)
#      So to publish a nested repo's *files* inside a parent repo (e.g. an umbrella
#      repo that should contain everything), go through plumbing:
#        1. read the nested repo's own index (mode + blob sha + path)
#        2. materialise the blobs in the parent object DB (`git hash-object -w`).
#           SHA-1 is content-addressed, so it must equal the nested repo's recorded
#           sha — asserted here, which proves the bytes are identical.
#        3. `git update-index --add --index-info` with "mode sha<TAB>path" lines
#
# The nested repo keeps working as its own repo (its .git is untouched); the parent
# simply also tracks those paths as ordinary files.
#
# Note: run from anywhere; paths are made relative to the parent repo.
# ============================================================
set -uo pipefail
PARENT="${1:?usage: include_nested_repo_files.sh <parent-dir> <nested-dir> [...]}"
shift
[ $# -ge 1 ] || { echo "usage: include_nested_repo_files.sh <parent-dir> <nested-dir> [...]"; exit 2; }

cd "$PARENT" || exit 2
[ -d .git ] || { echo "not a git repo: $PARENT"; exit 2; }

INFO=$(mktemp)
for d in "$@"; do
  name=$(basename "$d")
  [ -d "$d/.git" ] || { echo "skip $d (not a nested repo)"; continue; }
  ( cd "$d" && git -c core.quotePath=false ls-files ) | sed "s|^|$name/|" > "/tmp/${name}_paths.txt"
  git hash-object -w --stdin-paths < "/tmp/${name}_paths.txt" > "/tmp/${name}_shas.txt"
  ( cd "$d" && git ls-files -s ) | awk '{print $2}' > "/tmp/${name}_recorded.txt"
  if diff -q "/tmp/${name}_recorded.txt" "/tmp/${name}_shas.txt" >/dev/null; then
    n=$(wc -l < "/tmp/${name}_paths.txt" | tr -d ' ')
    echo "$name: $n blobs written · sha == nested repo index · OK"
  else
    echo "$name: SHA MISMATCH — aborting"; rm -f "$INFO"; exit 1
  fi
  paste "/tmp/${name}_paths.txt" "/tmp/${name}_shas.txt" \
    | awk -F'\t' '{printf "100644 %s\t%s\n", $2, $1}' >> "$INFO"
done

git update-index --add --index-info < "$INFO"
rm -f "$INFO"
echo "indexed files under the given dirs: $(git ls-files -- "$@" | wc -l | tr -d ' ')"
echo "next: git commit … ; git push"
