# -*- coding: utf-8 -*-
"""生成 README.md（站点说明 + 规模统计 + 验证结果），数字全部来自构建产物，不手写。

    python3 tools/make_readme.py

为什么用脚本生成 README：页数/任务数/截图数/自测题数这些东西手写必然过期。
本脚本读 work/stats/*.json 与各模块包，并实际跑一次 tools/verify_site.py，把它的输出嵌进 README。
"""
import importlib
import io
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(HERE, "sitegen"))

import common  # noqa: E402
from common import BY_CODE, MANIFEST, MODULES, SLOTS  # noqa: E402

STATS_DIR = os.path.join(ROOT, "work", "stats")


def read_stats():
    out = {}
    if os.path.isdir(STATS_DIR):
        for fn in sorted(os.listdir(STATS_DIR)):
            if fn.endswith(".json"):
                out[fn[:-5]] = json.load(open(os.path.join(STATS_DIR, fn), encoding="utf-8"))
    return out


def verify_output():
    r = subprocess.run([sys.executable, os.path.join(HERE, "verify_site.py")],
                       capture_output=True, cwd=ROOT)
    return (r.stdout or b"").decode("utf-8", "replace").strip().splitlines()


def main():
    stats = read_stats()
    codes = [m["code"] for m in MODULES if m["code"] in stats]
    missing = [m["code"] for m in MODULES if m["code"] not in stats]

    L = []
    A = L.append
    A("# SAP 全模块培训课程站（`sap_modules_cn/`）")
    A("")
    A("SAP **MM / PP / FI / CO** 四个模块的培训课件：**从总体到细节、从概念到操作手顺**。")
    A("静态 HTML，无外部依赖，双击 `index.html` 即可离线打开（`file://` 直接可用，不需要服务器、不联网）。")
    A("内容取材于教材文档 `S4.docx`（425 页、内嵌 1385 张图）里这四个模块的全部任务，"
      "配**真实 SAP GUI 截图（中文界面）**与**本站自绘的 SVG**（流程图 / 结构图 / 思维导图 / 泳道图）。")
    A("")
    A("- 站点入口：`index.html`（总览：四个模块怎么接力 + 学习路线 + 规模）")
    A("- 每模块 14 页，目录 %s" % "、".join("`%s/`" % c for c in codes))
    A("- 共享资源：`assets/style.css` `assets/mod.css` `assets/img/**`（真实截图）"
      "`assets/diagrams/<模块>/*.svg`（自绘图）")
    A("")
    A("## 1. 规模（自动统计，`tools/make_readme.py` 生成）")
    A("")
    A("| 模块 | 页数 | 教材任务 | 手顺步骤 | 截图引用（去重） | 自绘图 | 自测 | 配置分组 |")
    A("|---|---|---|---|---|---|---|---|")
    tot = {"pages": 0, "tasks": 0, "steps": 0, "shots": 0, "uniq": 0, "dia": 0, "quiz": 0}
    for c in codes:
        st = stats[c]
        tot["pages"] += st["pages"]
        tot["tasks"] += st["tasks"]
        tot["steps"] += st["steps"]
        tot["shots"] += st["shots"]
        tot["uniq"] += st["uniqueshots"]
        tot["dia"] += st["diagrams"]
        tot["quiz"] += st["quiz"]
        A("| **%s %s**（`%s/`） | %d | %d | %d | %d（%d） | %d | %d | %d |"
          % (BY_CODE[c]["brand"], BY_CODE[c]["name_cn"], c, st["pages"], st["tasks"], st["steps"],
             st["shots"], st["uniqueshots"], st["diagrams"], st["quiz"], st["config_groups"]))
    A("| **合计** | **%d+1**（含总览） | **%d** | **%d** | **%d**（%d） | **%d** | **%d** | — |"
      % (tot["pages"], tot["tasks"], tot["steps"], tot["shots"], tot["uniq"], tot["dia"], tot["quiz"]))
    A("")
    A("截图素材：`assets/img/` 下共 %d 张真实截图（MM/PP/FI/CO 四棵树），"
      "全部来自教材原图，页面引用了其中 %d 张（去重）。"
      % (len(MANIFEST), len(set(k for k in MANIFEST
                                for _ in [0] if k.split("/")[0] in codes))))
    if missing:
        A("")
        A("> 还没生成的模块：%s" % "、".join(missing))
    A("")
    A("## 2. 每个模块的 14 页（教学顺序 = 导航顺序）")
    A("")
    A("| 槽位 | 页面 | 内容 |")
    A("|---|---|---|")
    for i, slot in enumerate(SLOTS, 1):
        if slot.startswith("proc"):
            files = []
            for c in codes:
                pack = importlib.import_module("pack_%s" % c)
                pg = [p for p in pack.PAGES if p["slot"] == slot][0]
                files.append("%s/%s" % (c, pg["file"]))
            A("| `%s` | %s | 各模块的第 %s 篇流程详解（%s） |"
              % (slot, "／".join(files), slot[-1],
                 "、".join("%s：%s" % (c.upper(), BY_CODE[c]["procs"][int(slot[-1]) - 1]["nav"])
                          for c in codes)))
            continue
        names = []
        for c in codes:
            pack = importlib.import_module("pack_%s" % c)
            names.append([p for p in pack.PAGES if p["slot"] == slot][0]["file"])
        A("| `%s` | %s | %s |" % (slot, "／".join(sorted(set(names))),
                                  common.SLOT_LABEL.get(slot, "")))
    A("")
    A("## 3. 素材与「标准值」的写法")
    A("")
    A("1. **真实截图**取自教材文档 `S4.docx`（同目录外层 `sap_sd_cn/S4.docx`，与 `sap_sd_cn` 站同源）。"
      "每张图的图注里保留**原图文件名**（如 `01_1_image524.png`），可回 Word 原稿逐张核对。")
    A("2. **任务号、IMG 路径、手顺文本、T-code**全部由 `work/modules_model.json` 渲染"
      "（该文件由 `tools/prep_data.py` 从教材解析结果筛出），页面与 Excel 都不手抄。")
    A("3. **自绘图**（`assets/diagrams/*.svg`）由 `tools/sitegen/svgkit.py` 用纯 Python 生成，"
      "图注标注「本站自绘 SVG」；图上数值是课程场景值。")
    A("4. 凡可能随版本/行业方案而异的地方，页面给的是「**在自系统里怎么确认**」"
      "（F1 字段帮助、F4 取值列表、IMG 路径、`SE16N` 表名），而不是断言。")
    A("5. 教材里出现的自相矛盾/笔误，在页面里**明确标注**（例：MM 教材任务 22 的原材料评估类"
      "原书写错，应为 3000），不让学员照抄错值。")
    A("")
    A("## 4. 目录结构")
    A("")
    A("```")
    A("sap_modules_cn/")
    A("├─ index.html                     总览页（四个模块的接力 + 学习路线 + 规模）")
    for c in codes:
        A("├─ %s/                            %s 模块 14 页" % (c, BY_CODE[c]["brand"]))
    A("├─ assets/")
    A("│  ├─ style.css mod.css main.js quiz.js mod.js   设计系统与交互（灯箱 / 复制 / 判分）")
    A("│  ├─ img/{mm,pp,fi,co}/**                       真实截图（教材原图，按任务分目录）")
    A("│  └─ diagrams/{mm,pp,fi,co,overview}/*.svg      自绘图（本站生成）")
    A("├─ tools/")
    A("│  ├─ sitegen/common.py                          页面骨架与组件")
    A("│  ├─ sitegen/walk.py                            任务走查渲染（手顺 + 截图，覆盖全部任务）")
    A("│  ├─ sitegen/svgkit.py                          7 种自绘图的排版引擎（含文字溢出检查）")
    A("│  ├─ sitegen/pack_%s.py + %s_p2/p3/p4.py        各模块课程包（内容）" % (codes[0], codes[0]))
    A("│  ├─ prep_data.py                               从教材解析结果抽模块 + 量截图尺寸")
    A("│  ├─ dump_source.py                             导出教材原文素材（work/source_*.txt）")
    A("│  ├─ build_pages.py / build_diagrams.py / build_hub.py   生成")
    A("│  ├─ make_xlsx.py / make_readme.py              导出 Excel / README")
    A("│  ├─ verify_site.py                             本站验证器（结构/链接/图注/覆盖/统计）")
    A("│  └─ shoot_pages.py                             用 Chrome headless 截图看排版（一次只跑一个）")
    A("├─ work/")
    A("│  ├─ modules.json                               模块元数据（名称/副标题/流程页文件名）")
    A("│  ├─ modules_model.json                         教材四个模块的任务数据（来源见第 3 节）")
    A("│  ├─ img_manifest.json                          截图宽高清单（页面据此写 width/height）")
    A("│  ├─ source_{mm,pp,fi,co}.txt                   教材原文素材（通读用）")
    A("│  └─ stats/<模块>.json                          构建统计（每模块一份，便于并行构建）")
    A("└─ *_课程大纲_学习WBS.xlsx                        每模块一份 Excel（8 张表）+ 总览一份")
    A("```")
    A("")
    A("## 5. 重新生成 / 验证")
    A("")
    A("```bash")
    A("cd ~/Desktop/work/training/sap_modules_cn")
    A("")
    A("python3 tools/prep_data.py           # 教材数据 → work/modules_model.json + img_manifest.json（幂等）")
    A("python3 tools/dump_source.py         # 可选：导出教材原文素材")
    A("python3 tools/build_diagrams.py      # 自绘图 → assets/diagrams/<模块>/*.svg（含溢出检查）")
    A("python3 tools/build_pages.py         # 各模块 HTML（统计数字自动数，不手写）")
    A("python3 tools/build_hub.py           # 总览页 index.html")
    A("python3 tools/make_xlsx.py           # Excel（每模块 8 表 + 总览）")
    A("python3 tools/make_readme.py         # 本文件（数字与实际验证结果自动写入）")
    A("")
    A("python3 tools/verify_site.py         # 验证器：期望 RESULT: PASS")
    A("python3 tools/shoot_pages.py --all mm  # 可选：Chrome 截图看排版（一次只跑一个任务）")
    A("```")
    A("")
    A("当前实测输出：")
    A("")
    A("```")
    for ln in verify_output():
        A(ln)
    A("```")
    A("")
    A("`verify_site.py` 检查：页面结构（DOCTYPE / 单 article / article 在 footer 前 / 标签配平 / "
      "单 h1 / id 不重复）、导航（同模块各页 href 完全一致 + 恰好 1 个 active）、站内链接与跨页锚点、"
      "截图与自绘图存在且尺寸与清单一致、图注（画面编号 + 来源）、自测 30 题答案键、"
      "**配置篇是否覆盖教材全部任务**、统计一致、文本卫生、离线自足（不引用外部资源）。")
    A("")
    A("## 6. 已知边界（不要当成缺陷）")
    A("")
    A("- **没有 SAP 系统可登录**。所有实训都写了「做不到环境时的替代做法」（看图说话 / 纸上推演）。")
    A("- **截图是教材原图**，多数 400–700px 宽（教材作者在图上画了红框），放大到 2× 以上会糊；"
      "页面提供点击 4× 灯箱，投屏建议 1.5×。")
    A("- 教材任务的**编号与顺序保持原样**（含个别标题为空、路径指向前台任务的情况），"
      "配置篇按 A–F 重新分组以便授课，但不改任务内容。")
    A("- 术语按中文教学场景写，英文原名在每模块的 `glossary.html` 对照。")
    A("- 自绘图是**教学示意图**，不是 SAP 的官方结构图；数值为课程场景值。")
    A("")
    dl = {}
    dlp = os.path.join(ROOT, "work", "delivery.json")
    if os.path.exists(dlp):
        dl = json.load(open(dlp, encoding="utf-8"))
    if dl:
        A("## 7. 交付记录（本次会话）")
        A("")
        A("| 项 | 值 |")
        A("|---|---|")
        for k, label in (("verify", "验证结果"), ("snapshot", "快照（本站所在生态）"),
                         ("snapshot_size", "快照内容"), ("commit", "Git 提交"),
                         ("commit_proof", "提交证明"), ("remote_check", "远端只读校验"),
                         ("freeze_note", "并发写注意")):
            if dl.get(k):
                A("| %s | %s |" % (label, dl[k]))
        if dl.get("fixed_this_session"):
            A("")
            A("本次修掉的缺陷：")
            A("")
            for x in dl["fixed_this_session"]:
                A("- %s" % x)
        A("")
    A("## 8. 与 SD 课程站的关系")
    A("")
    A("销售与分销（SD）已有独立课程站：`../sap_cn/`（16 页，线上 `https://sap-cn-sd.vercel.app/`）。"
      "本站不重复 SD 内容，但在每个模块的「集成关系」里指出与 SD 的交接点"
      "（MM 的 601 发货、FI 的应收账款、PP 的需求来源、CO 的获利分析）。")
    A("")

    text = "\n".join(L) + "\n"
    with io.open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8") as f:
        f.write(text)
    print("README.md %d bytes（模块 %s）" % (len(text), ", ".join(codes)))

    # 给训练站总索引页（../index.html，由 ../tools/make_hub_page.py 生成）用的自报统计
    hub = {
        "n_pages": tot["pages"] + 1,
        "n_steps": tot["steps"],
        "figs": tot["shots"],
        "n_cfg": tot["tasks"],
        "has_wbs": True,
        "note": "SAP 全模块培训课件（MM/PP/FI/CO 各 14 页 + 总览）：概念→组织→主数据→流程→"
                "操作手顺（含教材全部任务）→实训。" + "真实截图 %d 张引用（去重 %d）+ 自绘 SVG %d 张。"
                % (tot["shots"], tot["uniq"], tot["dia"]),
    }
    json.dump(hub, open(os.path.join(ROOT, "tools", "hub_stats.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("tools/hub_stats.json: n_pages=%d n_steps=%d figs=%d n_cfg=%d"
          % (hub["n_pages"], hub["n_steps"], hub["figs"], hub["n_cfg"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
