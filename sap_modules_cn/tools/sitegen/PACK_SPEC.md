# 模块课程包编写规范（`pack_<code>.py` 系列）

本站 = `~/Desktop/work/training/sap_modules_cn/`，是 **MM / PP / FI / CO 四个模块的培训课程站**，
参照已有的 SD 课程站（`~/Desktop/work/training/sap_cn/`，线上 `https://sap-cn-sd.vercel.app/`）的做法：
**静态 HTML、离线可开、真实 SAP GUI 截图 + 自绘 SVG**，教学顺序是「概念 → 组织 → 主数据 → 流程 →
分步操作手顺 → SPRO 配置 → 实训 → 自测」。

共享代码（**不要修改**）：`tools/sitegen/{common.py, walk.py, svgkit.py}`、`tools/{build_pages.py,
build_diagrams.py, build_hub.py, verify_site.py, prep_data.py}`、`work/modules.json`、`assets/*`。
一个模块只允许新增/修改自己的四个文件：`tools/sitegen/pack_<code>.py`、`<code>_p2.py`、`<code>_p3.py`、
`<code>_p4.py`（`<code>` = `mm`/`pp`/`fi`/`co`）。**参考实现：`pack_mm.py` + `mm_p2.py` + `mm_p3.py` +
`mm_p4.py`** —— 先完整读一遍，风格、密度、写法照它来。

---

## 1. 四个文件的分工与入口契约（照 MM 抄结构）

`pack_<code>.py`（入口，必须能在 `tools/sitegen/` 下被 `importlib.import_module("pack_<code>")` 导入）

```python
from common import (box, cards, esc, flowchart, note, oplist, pathline, route, shot, shot_grid,
                    stat_cards, steps_list, tbl, toc)
from walk import render_config, render_task
from <code>_p2 import page_flow, page_master, page_org
from <code>_p3 import page_<procA>, page_<procB>, page_<procC>
from <code>_p4 import (CONFIG_GROUPS, CONFIG_NOTES, DIAGRAMS, GLOSSARY, page_config, page_glossary,
                       page_instructor, page_practice, page_quiz, page_worksheet)

def page_index(ctx, stats): ...   # 首页 + 概念页放这个文件里
def page_concept(ctx, stats): ...

PAGES = [  # 必须正好 14 条，slot 顺序固定（build_pages.py 会校验，顺序错直接报错）
    dict(slot="index",     file="index.html",     title="首页 · 课程地图与学习路线", kicker="…", tip="…", fn=page_index),
    dict(slot="concept",   file="concept.html",   title="概念与定位",     kicker="…", tip="…", fn=page_concept),
    dict(slot="org",       file="org.html",       title="组织结构",       kicker="…", tip="…", fn=page_org),
    dict(slot="master",    file="master.html",    title="主数据",         kicker="…", tip="…", fn=page_master),
    dict(slot="flow",      file="flow.html",      title="端到端流程",     kicker="…", tip="…", fn=page_flow),
    dict(slot="proc1",     file="<procA>.html",   title="…", kicker="…", tip="…", fn=page_<procA>),
    dict(slot="proc2",     file="<procB>.html",   title="…", kicker="…", tip="…", fn=page_<procB>),
    dict(slot="proc3",     file="<procC>.html",   title="…", kicker="…", tip="…", fn=page_<procC>),
    dict(slot="config",    file="config.html",    title="配置路线（NN 个任务）", kicker="…", tip="…", fn=page_config),
    dict(slot="practice",  file="practice.html",  title="实训：五个动手任务", kicker="…", tip="…", fn=page_practice),
    dict(slot="instructor",file="instructor.html",title="讲师版",   kicker="…", tip="…", fn=page_instructor),
    dict(slot="worksheet", file="worksheet.html", title="学员版（记入表）", kicker="…", tip="…", fn=page_worksheet),
    dict(slot="quiz",      file="quiz.html",      title="自测（30 题）", kicker="…", tip="…", fn=page_quiz),
    dict(slot="glossary",  file="glossary.html",  title="术语与 T-code 速查", kicker="…", tip="…", fn=page_glossary),
]
```

**三个流程页的文件名必须与 `work/modules.json` 里该模块的 `procs[].file` 完全一致**（构建脚本会校验）：

| 模块 | proc1 | proc2 | proc3 |
|---|---|---|---|
| `mm` | `purchase.html` | `inventory.html` | `invoice.html` |
| `pp` | `planning.html` | `execution.html` | `cost.html` |
| `fi` | `gl.html` | `arap.html` | `close.html` |
| `co` | `cca.html` | `io.html` | `pc.html` |

页面函数签名：`def page_xxx(ctx, stats):` → 返回 **字符串列表**（每个元素一段 HTML，构建脚本用 `\n` 连接）。

## 2. 可选用的组件（全部来自 `common.py`，都有中文注释）

* `esc(s)` —— 转义纯文本（写自由文本时务必用）
* `ctx.dia(name, cap, kind="自绘流程图", wide=True)` —— 引用自绘图，`name` = DIAGRAMS 里的 `file` 去掉 `.svg`
* `ctx.shot(rel, cap="…", task=NN)` —— 插一张真实截图，`rel` = `tNN/01_1_imageNNN.png` 或完整键 `mm/tNN/…`；
  画面编号自动递增；`task=NN` 让图注写出「教材《S4.docx》· XX 任务 NN 标题 · 原图 …」
* `ctx.shot_grid([(rel, cap), …])` —— 并排小图（首页/概念页的「教材画面」区用它）
* `ctx.simg(task_no, step=1, k=0)` —— 取教材第 task 步第 k 张截图的路径（写「代表性画面」时用）
* `render_task(ctx, task_no, note_text="…", max_imgs=None)` —— **整段任务走查**：任务标题 + 教学要点 +
  IMG 路径 + 手顺步骤（编号圆点）+ 原书提示 + 全部截图。流程页用它（`max_imgs` 限制张数），
  配置页由 `render_config` 自动调用它。
* `render_config(ctx, CONFIG_GROUPS, CONFIG_NOTES, intro="…")` —— 配置篇正文；**不重不漏覆盖全部任务，否则抛错**
* `tbl(headers, rows, cls="tbl idx")` —— 表格；单元格可以传 HTML；`cls` 用 `"tbl idx"`（首列等宽）或 `"tbl"`
* `note(kind, title, html)`，`kind ∈ {"tip","info","warn"}`；`box(kind, title, html)`，`kind ∈ {"info","ok","warn","danger"}`
* `oplist([...])` / `steps_list([...])` / `steph(no, title, tags, anchor)` / `toc([(标题, 锚点), …])`
* `cards([(标题, 说明), …])` / `stat_cards([(数字, 单位, 说明), …])` / `modcards([...])`
* `flowchart([(标题, 副标题), …])` —— 一行横向流程（首页学习路线用）
* `pathline(label, path)` —— 可复制的路径行；`route(["菜单","子菜单",…])` —— 一行路径

页面里所有站内链接用相对文件名（`concept.html#def`、`config.html#t12`）；跨模块用 `../pp/index.html`。

## 3. 配置篇的数据契约

```python
CONFIG_GROUPS = [("A 组标题", [1, 2, 3], "这一组在干什么（一两句）"), …]   # 不重不漏覆盖该模块全部任务
CONFIG_NOTES  = {1: "任务 01 的一句话教学要点", …}                        # 每个任务一条，别漏
```

`render_config` 会：① 先出目录 + 分组索引表；② 每组一个 `h2`；③ 每个任务调用 `render_task`
（有 `id="tNN"` 锚点，别的页面靠 `config.html#tNN` 指过来）。
任务号、标题、IMG 路径、手顺文本、截图**全部来自数据**，不要手抄、不要改。

## 4. 自绘图（`DIAGRAMS`）

```python
DIAGRAMS = [spec, …]     # spec 交给 tools/sitegen/svgkit.py 排版
```

| kind | 必填字段 | 用途 |
|---|---|---|
| `mindmap` | `w`(默认1420) `title` `sub` `center_title` `center_sub` `center_en` `center_note` `card_w` `branches=[{title,color,side:"L"/"R",leaves:[…]}]` | 首页知识地图（3 左 3 右） |
| `layers` | `w` `title` `sub` `bands=[{title,color,note,per_row,boxes=[{t,lines:[…]}]}]` | 组织结构/主数据层级/字段矩阵 |
| `flow` | `w` `title` `sub` `steps=[{no,t,sub,color,note?}]` `note?` | 单据流/步骤链（自动折行） |
| `tree` | `w` `title` `sub` `level_h` `box_w` `levels=[{nodes:[{t,lines,parent,color}]}]` | 组织树（parent = 上层索引） |
| `swimlane` | `w` `title` `sub` `lane_head` `cols=[{t,sub}]` `rows=[{t,color,cells:[…]}]` | 端到端泳道（行=角色，列=步骤） |
| `star` | `w` `title` `sub` `center_title` `center_sub` `center_en` `satellites=[{t,color,ang,down,up}]` `note?` | 与邻近模块的集成（ang：0 右 / 180 左 / 45 右下 / 135 左下） |
| `chains` | `w` `title` `sub` `items=[{title,color,chain:[…],texts:[…]}]` | 决定链/规则卡（如容差、科目确定） |

`color` 取值：`blue teal amber green red purple gray`。**建议 7–8 张**：mindmap、star（集成）、
end-to-end flow（或 swimlane）、org tree、master layers、再加 3 张与该模块强相关的
（如 FI 的「记账到报表」链、CO 的「成本流」、PP 的「MRP 到订单」）。

## 5. 自测题（30 题，必须正好 30）

```python
def _q(n, tag, text, opts, ans, expl):
    o = "".join('<div class="opt" data-key="%s">%s</div>' % (k, t) for k, t in opts)
    return ('<div class="quiz-q" data-answer="%s">\n<div class="q-meta"><span class="tag gray">%s</span></div>\n'
            '<h4>%d. %s</h4>\n<div class="opts">%s</div>\n'
            '<div class="explain">%s</div>\n</div>') % (ans, tag, n, text, o, expl)
```

* 每题 4 个选项（`data-key` = `A/B/C/D`），`data-answer` 必须是其中之一（验证器会核对）
* 每题必须有 `.explain` 解说，**答案要正确**（这是教学内容，不能猜）
* 分布建议：概念 5 · 组织 5 · 主数据 6 · 流程 8 · 配置 3 · 集成 3

## 6. 每页内容要求（教学密度参考 MM，不要缩水也不要灌水）

| 页 | 内容 |
|---|---|
| `index` | lead 段（这个模块管什么）+ `stat_cards`（页数/任务数/手顺步数/截图数，数字用 `stats` 里的真实值）+ 学习路线 `flowchart` + mindmap + star + 六大板块 `cards` + **教材场景值表**（公司代码/工厂/关键对象，来自教材画面）+ 「怎么用这个站」 |
| `concept` | 一句话定义 + 职能表 + **凭证/对象清单表**（谁产生、T-code、影响）+ 与其他模块的分界表 + **10–12 个常见误解表**（「常见说法 vs 实际上」）+ 1 张自绘图 + 6 张代表性截图 + 提示框 |
| `org` | 组织结构图（tree）+ 分层对象表（对象/教材任务/含义/决定什么）+ 分配关系表（含基数）+ 「组织数据决定什么」+ 8 张左右截图 + 指引到 config.html |
| `master` | 主数据分层图（layers）+ 视图/字段表（含教材值）+ 关键字段「填错的后果」表 + T-code + 6–8 张截图 |
| `flow` | 泳道图 + 单据流图 + **逐步表（步骤/T-code/产生什么凭证/库存影响/会计影响）** + 记账影响（该模块涉及的科目/成本）+ 顺序错误后果表 + 8 张截图 |
| `proc1..3` | 每页：教学场景与前置条件表 + **手顺（`render_task`，含截图）** + 字段读法表 + 常见错误排查表（症状/原因/处理）+ 与上下游的关系。**锚点用 `id="secNN"`**（不要用 `tNN`，那是配置页的锚点），toc 里也指向 `secNN` |
| `config` | `render_config(...)` + 使用说明 box + 完整性由脚本保证 |
| `practice` | 5 个实训任务，每个：做什么 / 完成基准（打勾）/ 常见错误 / 对应画面（`config.html#tNN` 链接）+ 环境准备清单 + 交作业要求 |
| `instructor` | 课时分配表 + 板书路线（oplist）+ **必问 12 题与答案** + 评分标准（合计 100 分）+ 教学注意（教材里的坑） |
| `worksheet` | 可打印记入表：组织值 / 主数据 / 单据号 / 凭证号与分录 / 自评表（用 `tbl` + `cls="tbl ws"` 与 `.ws-block` + `<div class="lines"><i></i>…</div>`） |
| `quiz` | 30 题 |
| `glossary` | 术语中英对照 ≥35 条（`GLOSSARY = [(中文, English, 说明)]`）+ T-code 速查（教材出现的事务码自动列出 + `TCODES_EXTRA` 补充）+ 常用表 + 教材任务总索引（参考 MM 的写法） |

**每页至少 4 张真实截图**（流程页因为有 `render_task` 会更多）；`concept/org/master/flow` 各配自绘图。

## 7. 内容底线（会被人当教材用）

1. **只用教材里真实存在的任务/T-code/路径**，任务文本与路径不要手抄（从数据取）。
   教材没演示、但项目必用的标准功能，要**明确标注**「教材未演示」（参考 `mm_p3.py` 的写法）。
2. 场景值（公司代码、工厂、物料、供应商、科目号等）必须来自本模块教材画面；写「换个环境请自行确认」的口径。
3. 术语用中文教学说法，首次出现给英文原名；事务码统一 `<code>ME21N</code>` 样式。
4. 不要出现「TODO / 占位符 / **markdown 粗体**」（验证器会把它们当错误）。
5. 讲不清的地方**不要编**：改成「在自系统里怎么确认（F1/F4、IMG 路径、表名）」。

## 8. 自检流程（必须全部跑完并看到 PASS）

```bash
cd ~/Desktop/work/training/sap_modules_cn
python3 tools/build_diagrams.py <code>        # 期望「溢出图 0」
python3 tools/build_pages.py <code>           # 期望一行统计输出
python3 tools/verify_site.py <code>           # 期望 RESULT: PASS
```

`verify_site.py` 会检查：页面结构/导航/链接/锚点、截图与自绘图存在、图注齐全、自测 30 题答案键、
**配置篇覆盖全部任务**、统计一致、文本卫生。

> 说明：只构建一个模块时，跨模块链接（`../pp/index.html`）与「总览页」检查会出现
> **WARN：目标模块还没生成** —— 这是正常的；`RESULT: PASS` 即通过。
> 只要看到 `发现 N 个问题 / RESULT: FAIL` 就必须修到通过。

排版目视检查（可选，一次只跑一个 Chrome 任务）：

```bash
python3 tools/shoot_pages.py --h 3000 <code>/index.html <code>/concept.html
# → work/shots/<code>_index.png，用看图工具检查是否有溢出/重叠
```
