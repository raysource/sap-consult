# -*- coding: utf-8 -*-
"""本站验证器：一页一页地核对生成结果，退出码 0 = PASS。

    python3 tools/verify_site.py            # 全部模块 + 总览页
    python3 tools/verify_site.py mm         # 只验 MM

检查项：
  A 页面结构：DOCTYPE / lang / 单 article / article 在 footer 之前 / 标签配平 / 单 h1 / id 不重复
  B 导航：同模块各页的导航 href 列表完全一致、恰好 1 个 active、active = 当前页
  C 链接：站内 .html 与 #锚点 都能解析（含模块间链接与总览页）
  D 资源：截图与自绘图都存在；截图带 width/height 且与 work/img_manifest.json 一致
  E 图注：截图有「画面 N」+ 来源；自绘图有类型标签
  F 自测：题目数 = 30；data-answer 必须落在某个 data-key 上；每题有解说
  G 配置篇覆盖：教材该模块的每个任务都在 config.html 里有锚点（漏任务 = 失败）
  H 文本卫生：无残留 Markdown（**…**）/ TODO / lorem / 占位符
  I 统计一致：work/build_stats.json 与实际生成物一致
  J 离线自足：不引用 http(s) 资源、不引用绝对路径
"""
import importlib
import json
import os
import re
import sys
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(HERE, "sitegen"))

import common  # noqa: E402

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
        "param", "source", "track", "wbr"}
ERRS, WARNS = [], []


def err(m):
    ERRS.append(m)


def warn(m):
    WARNS.append(m)


class Doc(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self, convert_charrefs=True)
        self.stack = []
        self.bad = []
        self.ids = []
        self.tags = []
        self.imgs = []          # (src, width, height)
        self.links = []         # href
        self.nav = []           # (href, classes)
        self.articles = 0
        self.h1 = 0
        self.q = []             # quiz: (answer, [keys], has_explain)
        self.figs = []          # ('shot'|'dia', raw)
        self.cur_q = None
        self.in_nav = 0
        self.in_fig = None
        self.figbuf = []
        self.in_cap = 0
        self.raw = ""

    # --- 结构 ---
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        self.tags.append(tag)
        if "id" in d:
            self.ids.append(d["id"])
        if tag == "article":
            self.articles += 1
        if tag == "h1":
            self.h1 += 1
        if tag == "img":
            self.imgs.append((d.get("src", ""), d.get("width"), d.get("height"), d.get("loading")))
        if tag == "a" and "href" in d:
            self.links.append(d["href"])
            if self.in_nav:
                self.nav.append((d["href"], d.get("class", "")))
        if tag == "nav" and "main" in (d.get("class") or ""):
            self.in_nav += 1
        if tag == "figure":
            cls = d.get("class", "")
            self.in_fig = "shot" if "shot" in (cls or "") else ("dia" if "dia" in (cls or "") else None)
            self.figbuf = []
        if self.in_fig and tag == "figcaption":
            self.in_cap += 1
        if tag == "div" and "quiz-q" in (d.get("class") or ""):
            self.cur_q = {"answer": (d.get("data-answer") or "").strip().upper(), "keys": [],
                          "explain": False}
        if self.cur_q is not None and tag == "div" and "opt" in (d.get("class") or "").split():
            self.cur_q["keys"].append((d.get("data-key") or "").strip().upper())
        if self.cur_q is not None and tag == "div" and "explain" in (d.get("class") or ""):
            self.cur_q["explain"] = True
        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))

    def handle_data(self, data):
        if self.in_fig:
            self.figbuf.append(data)

    def handle_endtag(self, tag):
        if tag == "figure" and self.in_fig:
            self.figs.append((self.in_fig, " ".join("".join(self.figbuf).split())))
            self.in_fig = None
            self.figbuf = []
        if tag == "figcaption":
            self.in_cap = max(0, self.in_cap - 1)
        if tag == "nav" and self.in_nav:
            self.in_nav -= 1
        if self.cur_q is not None and tag == "div":
            # 一个 quiz-q 结束：靠 data-answer 与 keys 都已经收齐再挂到列表
            pass
        if tag in VOID:
            return
        if not self.stack:
            self.bad.append("多余的 </%s> @%s" % (tag, self.getpos()[0]))
            return
        top, ln = self.stack.pop()
        if top != tag:
            self.bad.append("标签不配平：<%s>（第 %d 行）被 </%s> 关闭" % (top, ln, tag))


def parse(path):
    d = Doc()
    d.raw = open(path, encoding="utf-8").read()
    d.feed(d.raw)
    return d


# ---------------------------------------------------------------- 页面检查
CHAPTER_RE = re.compile(r"^[0-9A-Za-z._\-\u4e00-\u9fff]+\.html$")


def check_page(path, rel, module_files, page_ids, module):
    name = os.path.basename(path)
    d = parse(path)
    raw = d.raw
    # A
    if not raw.lstrip().lower().startswith("<!doctype html>"):
        err("%s/%s: 缺少 DOCTYPE" % (module, name))
    if '<html lang="zh-CN">' not in raw:
        err("%s/%s: <html lang> 不是 zh-CN" % (module, name))
    if d.articles != 1:
        err("%s/%s: <article> 出现 %d 次（应为 1）" % (module, name, d.articles))
    if d.bad:
        err("%s/%s: 标签问题 %s" % (module, name, d.bad[:3]))
    if d.stack:
        err("%s/%s: 未闭合标签 %s" % (module, name, [t for t, _l in d.stack][:5]))
    if d.h1 != 1:
        err("%s/%s: <h1> 有 %d 个（应为 1）" % (module, name, d.h1))
    dup = sorted(set(i for i in d.ids if d.ids.count(i) > 1))
    if dup:
        err("%s/%s: id 重复 %s" % (module, name, dup[:5]))
    if raw.find("</article>") > raw.find("<footer"):
        err("%s/%s: footer 出现在 article 之前" % (module, name))
    page_ids[name] = set(d.ids)

    # B 导航
    navs = [h for h, _c in d.nav]
    actives = [h for h, c in d.nav if "active" in c.split()]
    if len(navs) < 10:
        err("%s/%s: 导航项只有 %d 个" % (module, name, len(navs)))
    if len(actives) != 1 or actives[0] != name:
        err("%s/%s: active 应为 1 个且指向自己，实际 %s" % (module, name, actives))
    for h in navs:
        if h not in module_files:
            err("%s/%s: 导航指向不存在的页面 %s" % (module, name, h))
    key = tuple(navs)
    if d_nav.get(module) is None:
        d_nav[module] = key
    elif d_nav[module] != key:
        err("%s/%s: 导航顺序与其他页不一致" % (module, name))

    # C 链接
    for h in d.links:
        if h.startswith(("http://", "https://", "mailto:", "javascript:")):
            continue
        if h.startswith("#"):
            if h[1:] and h[1:] not in page_ids[name]:
                err("%s/%s: 页内锚点 #%s 不存在" % (module, name, h[1:]))
            continue
        target = h.split("#")[0]
        frag = h.split("#")[1] if "#" in h else ""
        # 跨模块链接（../pp/index.html）与资源链接（../assets/img/... 灯箱）只检查存在性
        if target.startswith("../") or re.search(r"\.(png|jpe?g|gif|svg|css|js)$", target):
            tpath = os.path.normpath(os.path.join(os.path.dirname(path), target))
            if not os.path.exists(tpath):
                # 跨模块链接：另一个模块还没生成时只提醒（构建完再验）
                if target.startswith("../") and not os.path.isdir(os.path.dirname(tpath)):
                    warn("%s/%s: 目标模块还没生成 %s" % (module, name, h))
                else:
                    err("%s/%s: 目标不存在 %s" % (module, name, h))
            continue
        if not CHAPTER_RE.match(target):
            err("%s/%s: 可疑链接 %s" % (module, name, h))
            continue
        tpath = os.path.join(os.path.dirname(path), target)
        if not os.path.exists(tpath):
            err("%s/%s: 链接目标不存在 %s" % (module, name, h))
        elif frag:
            ids = page_ids.get(target)
            if ids is None:
                td = parse(tpath)
                ids = set(td.ids)
                page_ids[target] = ids
            if frag not in ids:
                err("%s/%s: 跨页锚点 %s 不存在" % (module, name, h))

    # D 资源
    for src, w, hgt, loading in d.imgs:
        if not src:
            err("%s/%s: img 没有 src" % (module, name))
            continue
        if src.startswith(("http://", "https://")) or src.startswith("/"):
            err("%s/%s: 图片不是站内相对路径：%s" % (module, name, src))
            continue
        full = os.path.normpath(os.path.join(os.path.dirname(path), src))
        if not os.path.exists(full):
            err("%s/%s: 图片文件不存在 %s" % (module, name, src))
            continue
        if "/assets/img/" in src:
            relkey = src.split("/assets/img/")[1]
            m = common.MANIFEST.get(relkey)
            if not m:
                err("%s/%s: 截图不在 manifest：%s" % (module, name, relkey))
            elif str(m["w"]) != str(w) or str(m["h"]) != str(hgt):
                err("%s/%s: 尺寸与 manifest 不一致 %s（页面 %sx%s / 清单 %sx%s）"
                    % (module, name, relkey, w, hgt, m["w"], m["h"]))
        if not loading:
            warn("%s/%s: 图片缺少 loading=\"lazy\"（%s）" % (module, name, src))

    # E 图注
    for kind, text in d.figs:
        if kind == "shot":
            if "画面" not in text:
                err("%s/%s: 截图缺少「画面 N」编号" % (module, name))
            if "教材" not in text:
                err("%s/%s: 截图缺少来源说明" % (module, name))
        else:
            if "自绘" not in text:
                err("%s/%s: 自绘图缺少类型/来源标签" % (module, name))

    # F 自测
    if name == "quiz.html":
        qs = re.findall(r'<div class="quiz-q" data-answer="([^"]+)">(.*?)'
                        r'(?=<div class="quiz-q"|</article>)', raw, re.S)
        if len(qs) != 30:
            err("%s/quiz.html: 题目数 %d（应为 30）" % (module, len(qs)))
        for i, (ans, body) in enumerate(qs, 1):
            keys = re.findall(r'data-key="([^"]+)"', body)
            if ans.strip().upper() not in [k.strip().upper() for k in keys]:
                err("%s/quiz.html: 第 %d 题 data-answer=%s 不在选项中 %s" % (module, i, ans, keys))
            if len(keys) < 3:
                err("%s/quiz.html: 第 %d 题选项少于 3 个" % (module, i))
            if 'class="explain"' not in body:
                err("%s/quiz.html: 第 %d 题缺少解说" % (module, i))

    # G 配置覆盖
    if name == "config.html":
        tasks = common.MODEL[module]["tasks"]
        miss = [t["no"] for t in tasks if 'id="t%02d"' % t["no"] not in raw]
        if miss:
            err("%s/config.html: 漏了任务 %s" % (module, miss))
        if len(re.findall(r'class="tasksteps"', raw)) < len(tasks):
            err("%s/config.html: 手顺块 %d 个 < 任务 %d 个"
                % (module, len(re.findall(r'class="tasksteps"', raw)), len(tasks)))
        for t in tasks:
            if t.get("path"):
                seg = t["path"][:16]
                if seg not in raw:
                    err("%s/config.html: 任务 %02d 的 IMG 路径没出现在页面上" % (module, t["no"]))
                break

    # H 文本卫生
    for pat, label in ((r"\*\*[^*]{2,}\*\*", "残留 Markdown 粗体"), (r"\bTODO\b", "TODO"),
                       (r"lorem", "lorem"), (r"占位符", "占位符"), (r"\{\{", "模板占位")):
        m = re.search(pat, raw, re.I)
        if m:
            err("%s/%s: %s（%s）" % (module, name, label, m.group(0)[:30]))

    # J 离线自足
    for pat in (r'src="https?://', r'href="https?://[^"]*\.(css|js)"', r'src="/'):
        m = re.search(pat, raw)
        if m:
            err("%s/%s: 引用了外部/绝对资源 %s" % (module, name, m.group(0)))


d_nav = {}
STATS_DIR = os.path.join(ROOT, "work", "stats")


def read_stats():
    """每模块一个统计文件（并行构建时不会互相覆盖）。"""
    out = {}
    if os.path.isdir(STATS_DIR):
        for fn in sorted(os.listdir(STATS_DIR)):
            if fn.endswith(".json"):
                try:
                    out[fn[:-5]] = json.load(open(os.path.join(STATS_DIR, fn), encoding="utf-8"))
                except ValueError:
                    pass
    return out


def check_hub():
    path = os.path.join(ROOT, "index.html")
    if not os.path.exists(path):
        err("总览页 index.html 不存在（跑 tools/build_hub.py）")
        return
    raw = open(path, encoding="utf-8").read()
    for m in common.MODULES:
        if '"%s/index.html"' % m["code"] not in raw:
            err("总览页没有指向 %s 模块的入口" % m["code"])
    if re.search(r"\{\{|\*\*", raw):
        err("总览页有残留占位/Markdown")
    stats = read_stats()
    for m in common.MODULES:
        st = stats.get(m["code"])
        if not st:
            if os.path.isdir(os.path.join(ROOT, m["code"])):
                err("总览页：%s 模块有页面但没有构建统计（重跑 build_pages.py）" % m["code"])
            else:
                warn("总览页：%s 模块还没生成" % m["code"])
            continue
        if str(st["tasks"]) not in raw:
            warn("总览页没有出现 %s 的任务数 %d" % (m["code"], st["tasks"]))


def main(argv):
    codes = [a for a in argv[1:] if not a.startswith("-")] or [m["code"] for m in common.MODULES]
    stats = read_stats()
    total = {"pages": 0, "shots": 0, "unique": set(), "dia": 0, "quiz": 0}
    for code in codes:
        mdir = os.path.join(ROOT, code)
        if not os.path.isdir(mdir):
            err("%s/: 模块目录不存在（先跑 tools/build_pages.py）" % code)
            continue
        files = sorted(f for f in os.listdir(mdir) if f.endswith(".html"))
        if not files:
            err("%s/: 没有 HTML" % code)
            continue
        expect = set(p["file"] for p in importlib.import_module("pack_%s" % code).PAGES)
        if set(files) != expect:
            err("%s/: 页面文件与模块包不一致：多 %s / 少 %s"
                % (code, sorted(set(files) - expect), sorted(expect - set(files))))
        page_ids = {}
        for f in files:
            check_page(os.path.join(mdir, f), f, expect, page_ids, code)
        raw_all = "\n".join(open(os.path.join(mdir, f), encoding="utf-8").read() for f in files)
        shots = len(re.findall(r'<figure class="shot', raw_all))
        uniq = set(re.findall(r'src="\.\./assets/img/([^"]+)"', raw_all))
        dia = len(re.findall(r'<figure class="dia', raw_all))
        quiz = len(re.findall(r'class="quiz-q"', open(os.path.join(mdir, "quiz.html"),
                                                      encoding="utf-8").read()))
        total["pages"] += len(files)
        total["shots"] += shots
        total["unique"] |= uniq
        total["dia"] += dia
        total["quiz"] += quiz
        # I 统计一致
        st = stats.get(code)
        if not st:
            err("%s: work/build_stats.json 里没有该模块" % code)
        else:
            if st["pages"] != len(files):
                err("%s: 统计页数 %s ≠ 实际 %d" % (code, st["pages"], len(files)))
            if st["quiz"] != quiz:
                err("%s: 统计自测题 %s ≠ 实际 %d" % (code, st["quiz"], quiz))
            if st["shots"] != shots:
                err("%s: 统计截图引用 %s ≠ 实际 %d（重建后再验）" % (code, st["shots"], shots))
            if st["uniqueshots"] != len(uniq):
                err("%s: 统计去重截图 %s ≠ 实际 %d" % (code, st["uniqueshots"], len(uniq)))
            if st["diagrams"] != len(importlib.import_module("pack_%s" % code).DIAGRAMS):
                err("%s: 自绘图统计与模块包不一致" % code)
        # 自绘图文件是否都生成
        for spec in importlib.import_module("pack_%s" % code).DIAGRAMS:
            p = os.path.join(ROOT, "assets", "diagrams", code, spec["file"])
            if not os.path.exists(p):
                err("%s: 自绘图没生成 %s（跑 tools/build_diagrams.py）" % (code, spec["file"]))
    check_hub()
    print("pages=%d  shot=%d（去重 %d）  dia=%d  quiz=%d" %
          (total["pages"], total["shots"], len(total["unique"]), total["dia"], total["quiz"]))
    for w in WARNS[:10]:
        print("WARN:", w)
    if len(WARNS) > 10:
        print("WARN: … 另有 %d 条" % (len(WARNS) - 10))
    if ERRS:
        print("\n发现 %d 个问题：" % len(ERRS))
        for e in ERRS[:60]:
            print("  -", e)
        if len(ERRS) > 60:
            print("  … 另有 %d 个" % (len(ERRS) - 60))
        print("RESULT: FAIL")
        return 1
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
