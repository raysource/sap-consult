# -*- coding: utf-8 -*-
"""按模块构建页面：加载模块包（pack_mm / pack_pp / pack_fi / pack_co）→ 写 HTML → 汇总统计。

    python3 tools/build_pages.py            # 全部模块 + 总览页
    python3 tools/build_pages.py mm co      # 只建指定模块

约定（模块包必须遵守，违反会直接报错，不会生成半成品）：
  PAGES         14 页，slot 顺序 = work/modules.json 的 slots，文件名唯一
  DIAGRAMS      自绘图 spec 列表（svgkit 的 dict 格式）
  CONFIG_GROUPS [(组标题, [任务号…], 组说明)]，必须不重不漏地覆盖教材全部任务
  CONFIG_NOTES  {任务号: 一句话教学要点}
  GLOSSARY      [(中文, English, 说明)] 术语表
"""
import importlib
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(HERE, "sitegen"))

import common  # noqa: E402
from common import Ctx, MODULES, SLOTS  # noqa: E402

STATS_DIR = os.path.join(ROOT, "work", "stats")   # 每模块一个文件：并行构建时不互相覆盖


def load_pack(code):
    return importlib.import_module("pack_%s" % code)


def check_pages(code, pages):
    got = [p["slot"] for p in pages]
    if got != SLOTS:
        raise ValueError("[%s] 页面槽位顺序不对。\n  应为 %s\n  实际 %s" % (code, SLOTS, got))
    files = [p["file"] for p in pages]
    if len(set(files)) != len(files):
        raise ValueError("[%s] 页面文件名重复：%s" % (code, files))
    for p in pages:
        for k in ("file", "title", "kicker", "fn"):
            if not p.get(k):
                raise ValueError("[%s] 页面 %s 缺少 %s" % (code, p.get("file"), k))
    # 三个流程页必须与 modules.json 里声明的文件名一致（导航靠它取名）
    procs = [p["file"] for p in common.BY_CODE[code]["procs"]]
    got_procs = [p["file"] for p in pages if p["slot"].startswith("proc")]
    if procs != got_procs:
        raise ValueError("[%s] 流程页文件名与 work/modules.json 不一致：%s vs %s"
                         % (code, procs, got_procs))


def build_module(code):
    """构建一个模块，返回 {页面: 统计}。"""
    pack = load_pack(code)
    ctx = Ctx(code)
    check_pages(code, pack.PAGES)

    diagrams = getattr(pack, "DIAGRAMS", [])
    groups = getattr(pack, "CONFIG_GROUPS", [])
    quiz = 0
    stats = {
        "code": code,
        "pages": len(pack.PAGES),
        "tasks": len(ctx.tasks),
        "steps": sum(len(t["steps"]) for t in ctx.tasks),
        "tcodes": len(set(c for t in ctx.tasks for c in (t.get("tcodes") or []))),
        "config_groups": len(groups),
        "diagrams": len(diagrams),
        "shots": 0, "uniqueshots": 0, "quiz": 0,
    }

    out_dir = os.path.join(ROOT, code)
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    written = {}
    order = [p for p in pack.PAGES if p["slot"] != "index"] + [p for p in pack.PAGES if p["slot"] == "index"]
    bodies = {}
    for pg in order:
        ctx.reset_fig()
        body = "\n".join(pg["fn"](ctx, stats))
        bodies[pg["file"]] = body

    # index 页先按「不含首页」的数字渲染一轮；首页自己也允许放截图（第一轮与第二轮张数相同，
    # 因为它不依赖 stats 里的 shots 值），所以两轮之后统计仍然是自洽的。
    all_body = "\n".join(bodies[k] for k in bodies if k != "index.html")
    idx_body = bodies.get("index.html", "")
    stats["shots"] = len(re.findall(r'<figure class="shot', all_body))
    stats["uniqueshots"] = len(set(re.findall(r'src="\.\./assets/img/[^"]+"', all_body)))
    stats["diagrams_used"] = len(re.findall(r'<figure class="dia', all_body))
    stats["quiz"] = len(re.findall(r'class="quiz-q"', bodies.get("quiz.html", "")))

    idx_page = [p for p in pack.PAGES if p["slot"] == "index"][0]
    ctx.reset_fig()
    stats["shots_total"] = stats["shots"] + len(re.findall(r'<figure class="shot', idx_body))
    idx_body = "\n".join(idx_page["fn"](ctx, stats))
    bodies["index.html"] = idx_body

    # 统计口径 = 全部页面（含首页）—— 验证器就是这么数的，两边必须一致。
    # 以前这里只数非首页，于是「首页放截图」必然报统计不一致（子代理只能绕开，用裸 img）。
    final_all = "\n".join(bodies.values())
    stats["shots"] = len(re.findall(r'<figure class="shot', final_all))
    stats["uniqueshots"] = len(set(re.findall(r'src="\.\./assets/img/[^"]+"', final_all)))
    stats["diagrams_used"] = len(re.findall(r'<figure class="dia', final_all))

    for pg in pack.PAGES:
        nav = common.nav_of(ctx, pack.PAGES)
        html = common.shell(ctx, pack.PAGES, pg["file"], pg["title"], pg["kicker"],
                            bodies[pg["file"]], desc=None)
        path = os.path.join(out_dir, pg["file"])
        with io.open(path, "w", encoding="utf-8") as f:
            f.write(html)
        written[pg["file"]] = len(html)
        assert nav  # 导航非空
    stats["html_bytes"] = sum(written.values())
    stats["files"] = sorted(written)
    return stats


def read_stats():
    """读取全部模块的构建统计（每模块一个文件，便于并行构建）。"""
    out = {}
    if not os.path.isdir(STATS_DIR):
        return out
    for fn in sorted(os.listdir(STATS_DIR)):
        if fn.endswith(".json"):
            try:
                out[fn[:-5]] = json.load(open(os.path.join(STATS_DIR, fn), encoding="utf-8"))
            except ValueError:
                pass
    return out


def main(argv):
    codes = [a for a in argv[1:] if not a.startswith("-")] or [m["code"] for m in MODULES]
    if not os.path.isdir(STATS_DIR):
        os.makedirs(STATS_DIR)
    for code in codes:
        st = build_module(code)
        json.dump(st, open(os.path.join(STATS_DIR, "%s.json" % code), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        print("[%s] %s 页 / 任务 %d / 手顺步骤 %d / 截图引用 %d（去重 %d）/ 自绘图 %d / 自测 %d"
              % (code, st["pages"], st["tasks"], st["steps"], st["shots"], st["uniqueshots"],
                 st["diagrams"], st["quiz"]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
