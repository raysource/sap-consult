# -*- coding: utf-8 -*-
"""共享的「任务走查」渲染器：把教材里的一个任务（IMG 路径 + 手顺 + 截图 + 原书提示）
渲染成一段可直接放进页面的 HTML。

为什么要共享：四个模块的配置篇都要覆盖教材的**全部任务**（MM 42 / PP 51 / FI 45 / CO 34），
手写必然漏。这里从 work/modules_model.json 直接渲染，模块包只提供「分组」与「一句话要点」，
于是「站上写的手顺 = 教材里的手顺」这条路是短的、可核对的（脚本会检查任务有没有漏）。
"""
from common import box, esc, note, oplist, pathline, route, steph, tbl, toc


def _cap(text):
    """原书 caption 可能多行、含全角空格，统一成一段安全 HTML。"""
    t = (text or "").strip()
    t = t.replace("\r", "")
    lines = [x.strip() for x in t.split("\n") if x.strip()]
    if not lines:
        return ""
    return "<br>".join(esc(x) for x in lines)


def _notes_after(task, idx):
    out = []
    for n in task.get("notes") or []:
        if int(n.get("after") or 0) == idx:
            kind = n.get("kind") or "tip"
            label = {"tip": "原书提示", "warn": "注意", "info": "说明"}.get(kind, "原书提示")
            out.append(note(kind if kind in ("tip", "warn", "info") else "tip",
                            label, _cap(n.get("text"))))
    return "".join(out)


def render_task(ctx, no, note_text="", max_imgs=None, show_path=True, show_values=True,
                anchor=None, compact=False):
    """渲染教材第 no 个任务的完整手顺。max_imgs 限制截图张数（流程篇用，配置篇不限制）。"""
    t = ctx.task(no)
    tags = [("tc", c) for c in (t.get("tcodes") or [])]
    parts = [steph("任务 %02d" % no, t["title"], tags=tags, anchor=anchor or ("t%02d" % no))]
    if note_text:
        parts.append(note("tip", "教学要点", note_text))
    if show_path and t.get("path"):
        parts.append(pathline("IMG 路径（教材后台菜单）", t["path"]))
    if t.get("subs"):
        heads = [s["text"] for s in t["subs"] if s.get("kind") == "head"]
        if heads:
            parts.append('<p class="subheads">教材小节：%s</p>'
                         % esc(" / ".join(heads)))

    used = 0
    lis = []
    for i, st in enumerate(t["steps"], 1):
        cap = _cap(st.get("caption"))
        seen = []
        for p in st.get("imgs") or []:
            if p not in seen:
                seen.append(p)
        if max_imgs is not None:
            room = max(0, max_imgs - used)
            seen = seen[:room]
        used += len(seen)
        body = ""
        if cap:
            body += '<p class="stepcap">%s</p>' % cap
        if seen:
            if len(seen) == 1:
                body += ctx.shot(seen[0], task=no, cap="")
            else:
                body += ctx.shot_grid([(p, "") for p in seen])
        body += _notes_after(t, i)
        if not body:
            continue
        lis.append("<li>%s</li>" % body)
        if max_imgs is not None and used >= max_imgs:
            break
    if lis:
        parts.append('<ol class="tasksteps">%s</ol>' % "".join(lis))
    if show_values and t.get("values"):
        # 教材数据里输入值是 {k: 字段, v: 值} 的结构（也允许是纯字符串），渲染成两列表
        rows, pairs = [], []
        for v in t["values"]:
            if isinstance(v, dict):
                pairs.append([esc(v.get("k") or ""), "<code>%s</code>" % esc(v.get("v") or "")])
            else:
                rows.append([esc(v)])
        if pairs:
            parts.append(tbl(["输入值（教材画面）：字段", "值"], pairs, cls="tbl idx"))
        if rows and not pairs:
            parts.append(tbl(["输入值（教材画面）"], rows))
    if compact:
        return '<div class="taskblk compact">%s</div>' % "".join(parts)
    return '<div class="taskblk">%s</div>' % "".join(parts)


def render_config(ctx, groups, notes, intro="", missing_ok=False):
    """配置篇：按分组覆盖教材的全部任务。

    groups = [(组标题, [任务号…], 组说明)]
    notes  = {任务号: 一句话要点}
    返回 HTML 片段；任务有漏 / 重复会直接抛错（宁可生成失败，也不要站上悄悄少一页内容）。
    """
    known = set(t["no"] for t in ctx.tasks)
    covered = []
    for _title, nos, _blurb in groups:
        covered.extend(nos)
    dup = [n for n in set(covered) if covered.count(n) > 1]
    if dup:
        raise ValueError("配置分组里任务重复：%s（模块 %s）" % (sorted(dup), ctx.code))
    miss = sorted(known - set(covered))
    if miss and not missing_ok:
        raise ValueError("配置篇漏了 %s 个任务：%s（模块 %s）" % (len(miss), miss, ctx.code))
    extra = sorted(set(covered) - known)
    if extra:
        raise ValueError("配置篇出现教材没有的任务号：%s（模块 %s）" % (extra, ctx.code))

    out = []
    if intro:
        out.append(intro)
    out.append(toc([(title, "g%s" % idx) for idx, (title, _nos, _b) in enumerate(groups, 1)]))
    out.append(tbl(["组", "内容", "任务数", "任务号"],
                   [["<b>%s</b>" % esc(title), esc(blurb), str(len(nos)),
                     ", ".join('<a href="#t%02d">%02d</a>' % (n, n) for n in nos)]
                    for title, nos, blurb in groups],
                   cls="tbl idx"))
    for idx, (title, nos, blurb) in enumerate(groups, 1):
        out.append('<h2 id="g%d">%s <span class="cnt">%d 个任务</span></h2>' % (idx, esc(title), len(nos)))
        if blurb:
            out.append('<p class="lead2">%s</p>' % esc(blurb))
        for no in nos:
            out.append(render_task(ctx, no, note_text=notes.get(no, "")))
    return "\n".join(out)
