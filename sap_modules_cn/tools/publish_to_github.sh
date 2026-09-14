#!/usr/bin/env bash
# 把 sap_modules_cn 作为独立仓库发布到 GitHub（可重复执行）。
#
#   bash tools/publish_to_github.sh [repo-name]        # 默认 raysource/sap_modules_cn
#
# 说明：本站的截图与 SD 课程站（raysource/sap_cn_sd）同源，都来自教材《S4.docx》，
# 用户此前已把同批素材公开（raysource/sap-consult 含 sap_sd_cn/assets/img）。
# 若要改为私有：gh repo edit <owner>/<repo> --visibility private
set -euo pipefail
cd "$(dirname "$0")/.."

REPO="${1:-raysource/sap_modules_cn}"

if [ ! -d .git ]; then git init -b main; fi
git remote remove origin 2>/dev/null || true
git remote add origin "https://github.com/${REPO}.git"
git add -A
echo "--- staged ---"
git status --short | wc -l | tr -d ' '
git status --short | awk '{print $2}' | sed 's#/.*##' | sort | uniq -c | sort -rn | head -12
echo "--- size ---"
du -sh . | tr -d '\n'; echo ""
echo "--- commit ---"
git -c user.name='Jason' -c user.email='jason@localhost' commit -q -m "SAP MM / PP / FI / CO 培训课件（4 模块 × 14 页 + 总览）

- 每模块 14 页：概念 → 组织 → 主数据 → 端到端流程 → 三篇操作手顺 → SPRO 配置（覆盖教材全部任务）
  → 实训 → 讲师版 → 学员版 → 30 题自测 → 术语与 T-code 速查
- 真实 SAP GUI 截图（中文界面，教材《S4.docx》原图，保留原文件名可回查）
- 自绘 SVG：思维导图 / 组织结构树 / 主数据结构 / 端到端流程图 / 泳道图 / 集成图 / 决定链
- 生成器与验证器：tools/{prep_data,build_diagrams,build_pages,build_hub,make_xlsx,make_readme,verify_site}.py
  （verify_site.py：结构 / 导航 / 链接 / 图注 / 配置篇任务覆盖 / 统计一致 / 离线自足）
- Excel：每模块 8 张表 + 全模块总览" || echo "(nothing to commit)"
echo "--- push ---"
git push -u origin main 2>&1 | tail -5
echo "--- local HEAD ---"
git rev-parse HEAD
git log --oneline -1
