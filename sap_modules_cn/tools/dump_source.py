# -*- coding: utf-8 -*-
"""把教材某个模块的全部文字（任务标题 / IMG 路径 / 手顺步骤 / 原书提示 / 输入值）导出成纯文本，
方便写课程包时通读原始素材，不用在 JSON 里翻。

    python3 tools/dump_source.py            # 四个模块都导出
    python3 tools/dump_source.py pp fi      # 只导出指定模块

输出：work/source_<模块>.txt
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
MODEL = json.load(open(os.path.join(ROOT, "work", "modules_model.json"), encoding="utf-8"))


def dump(code):
    mod = MODEL[code]
    out = ["# 教材《S4.docx》 %s 模块（%s）—— 原文素材" % (code.upper(), mod["title"]),
           "# 任务 %d 个 / 手顺步骤 %d 个。下面的文字与画面引用都直接来自教材解析结果。" %
           (len(mod["tasks"]), sum(len(t["steps"]) for t in mod["tasks"])), ""]
    for t in mod["tasks"]:
        out.append("=" * 78)
        out.append("任务 %02d %s（教材任务号 %02d）" % (t["no"], t["title"], t["no"]))
        if t.get("path"):
            out.append("IMG 路径: %s" % t["path"])
        if t.get("tcodes"):
            out.append("事务码: %s" % ", ".join(t["tcodes"]))
        if t.get("values"):
            out.append("输入值: %s" % " | ".join(
                v if isinstance(v, str) else json.dumps(v, ensure_ascii=False) for v in t["values"]))
        for n in t.get("notes") or []:
            out.append("[%s] %s" % (n.get("kind") or "tip",
                                    (n.get("text") or "").replace("\n", " ")))
        for i, st in enumerate(t["steps"], 1):
            cap = (st.get("caption") or "").replace("\n", " ")
            imgs = st.get("imgs") or []
            out.append("  步骤 %02d: %s" % (i, cap or "（教材此步无文字）"))
            for p in imgs:
                out.append("      画面: %s" % p)
        out.append("")
    path = os.path.join(ROOT, "work", "source_%s.txt" % code)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("%-4s -> work/source_%s.txt  %d KB" % (code, code, os.path.getsize(path) // 1024))


def main(argv):
    codes = [a for a in argv[1:] if not a.startswith("-")] or list(MODEL.keys())
    for c in codes:
        dump(c)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
