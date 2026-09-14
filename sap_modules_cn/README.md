# SAP 全模块培训课程站（`sap_modules_cn/`）

SAP **MM / PP / FI / CO** 四个模块的培训课件：**从总体到细节、从概念到操作手顺**。
静态 HTML，无外部依赖，双击 `index.html` 即可离线打开（`file://` 直接可用，不需要服务器、不联网）。
内容取材于教材文档 `S4.docx`（425 页、内嵌 1385 张图）里这四个模块的全部任务，配**真实 SAP GUI 截图（中文界面）**与**本站自绘的 SVG**（流程图 / 结构图 / 思维导图 / 泳道图）。

- 站点入口：`index.html`（总览：四个模块怎么接力 + 学习路线 + 规模）
- 每模块 14 页，目录 `mm/`、`pp/`、`fi/`、`co/`
- 共享资源：`assets/style.css` `assets/mod.css` `assets/img/**`（真实截图）`assets/diagrams/<模块>/*.svg`（自绘图）

## 1. 规模（自动统计，`tools/make_readme.py` 生成）

| 模块 | 页数 | 教材任务 | 手顺步骤 | 截图引用（去重） | 自绘图 | 自测 | 配置分组 |
|---|---|---|---|---|---|---|---|
| **MM 物料管理**（`mm/`） | 14 | 42 | 168 | 301（226） | 8 | 30 | 6 |
| **PP 生产计划**（`pp/`） | 14 | 51 | 220 | 431（271） | 8 | 30 | 8 |
| **FI 财务会计**（`fi/`） | 14 | 45 | 181 | 391（263） | 8 | 30 | 10 |
| **CO 管理会计**（`co/`） | 14 | 34 | 126 | 288（181） | 8 | 30 | 9 |
| **合计** | **56+1**（含总览） | **172** | **695** | **1411**（941） | **32** | **120** | — |

截图素材：`assets/img/` 下共 940 张真实截图（MM/PP/FI/CO 四棵树），全部来自教材原图，页面引用了其中 940 张（去重）。

## 2. 每个模块的 14 页（教学顺序 = 导航顺序）

| 槽位 | 页面 | 内容 |
|---|---|---|
| `index` | index.html | 首页 |
| `concept` | concept.html | 概念 |
| `org` | org.html | 组织 |
| `master` | master.html | 主数据 |
| `flow` | flow.html | 流程 |
| `proc1` | mm/purchase.html／pp/planning.html／fi/gl.html／co/cca.html | 各模块的第 1 篇流程详解（MM：采购、PP：计划、FI：总账、CO：成本中心） |
| `proc2` | mm/inventory.html／pp/execution.html／fi/arap.html／co/io.html | 各模块的第 2 篇流程详解（MM：库存、PP：执行、FI：应收应付、CO：内部订单） |
| `proc3` | mm/invoice.html／pp/cost.html／fi/close.html／co/pc.html | 各模块的第 3 篇流程详解（MM：发票校验、PP：成本、FI：期末报表、CO：产品成本） |
| `config` | config.html | 配置 |
| `practice` | practice.html | 实训 |
| `instructor` | instructor.html | 讲师 |
| `worksheet` | worksheet.html | 学员 |
| `quiz` | quiz.html | 自测 |
| `glossary` | glossary.html | 术语 |

## 3. 素材与「标准值」的写法

1. **真实截图**取自教材文档 `S4.docx`（同目录外层 `sap_sd_cn/S4.docx`，与 `sap_sd_cn` 站同源）。每张图的图注里保留**原图文件名**（如 `01_1_image524.png`），可回 Word 原稿逐张核对。
2. **任务号、IMG 路径、手顺文本、T-code**全部由 `work/modules_model.json` 渲染（该文件由 `tools/prep_data.py` 从教材解析结果筛出），页面与 Excel 都不手抄。
3. **自绘图**（`assets/diagrams/*.svg`）由 `tools/sitegen/svgkit.py` 用纯 Python 生成，图注标注「本站自绘 SVG」；图上数值是课程场景值。
4. 凡可能随版本/行业方案而异的地方，页面给的是「**在自系统里怎么确认**」（F1 字段帮助、F4 取值列表、IMG 路径、`SE16N` 表名），而不是断言。
5. 教材里出现的自相矛盾/笔误，在页面里**明确标注**（例：MM 教材任务 22 的原材料评估类原书写错，应为 3000），不让学员照抄错值。

## 4. 目录结构

```
sap_modules_cn/
├─ index.html                     总览页（四个模块的接力 + 学习路线 + 规模）
├─ mm/                            MM 模块 14 页
├─ pp/                            PP 模块 14 页
├─ fi/                            FI 模块 14 页
├─ co/                            CO 模块 14 页
├─ assets/
│  ├─ style.css mod.css main.js quiz.js mod.js   设计系统与交互（灯箱 / 复制 / 判分）
│  ├─ img/{mm,pp,fi,co}/**                       真实截图（教材原图，按任务分目录）
│  └─ diagrams/{mm,pp,fi,co,overview}/*.svg      自绘图（本站生成）
├─ tools/
│  ├─ sitegen/common.py                          页面骨架与组件
│  ├─ sitegen/walk.py                            任务走查渲染（手顺 + 截图，覆盖全部任务）
│  ├─ sitegen/svgkit.py                          7 种自绘图的排版引擎（含文字溢出检查）
│  ├─ sitegen/pack_mm.py + mm_p2/p3/p4.py        各模块课程包（内容）
│  ├─ prep_data.py                               从教材解析结果抽模块 + 量截图尺寸
│  ├─ dump_source.py                             导出教材原文素材（work/source_*.txt）
│  ├─ build_pages.py / build_diagrams.py / build_hub.py   生成
│  ├─ make_xlsx.py / make_readme.py              导出 Excel / README
│  ├─ verify_site.py                             本站验证器（结构/链接/图注/覆盖/统计）
│  └─ shoot_pages.py                             用 Chrome headless 截图看排版（一次只跑一个）
├─ work/
│  ├─ modules.json                               模块元数据（名称/副标题/流程页文件名）
│  ├─ modules_model.json                         教材四个模块的任务数据（来源见第 3 节）
│  ├─ img_manifest.json                          截图宽高清单（页面据此写 width/height）
│  ├─ source_{mm,pp,fi,co}.txt                   教材原文素材（通读用）
│  └─ stats/<模块>.json                          构建统计（每模块一份，便于并行构建）
└─ *_课程大纲_学习WBS.xlsx                        每模块一份 Excel（8 张表）+ 总览一份
```

## 5. 重新生成 / 验证

```bash
cd ~/Desktop/work/training/sap_modules_cn

python3 tools/prep_data.py           # 教材数据 → work/modules_model.json + img_manifest.json（幂等）
python3 tools/dump_source.py         # 可选：导出教材原文素材
python3 tools/build_diagrams.py      # 自绘图 → assets/diagrams/<模块>/*.svg（含溢出检查）
python3 tools/build_pages.py         # 各模块 HTML（统计数字自动数，不手写）
python3 tools/build_hub.py           # 总览页 index.html
python3 tools/make_xlsx.py           # Excel（每模块 8 表 + 总览）
python3 tools/make_readme.py         # 本文件（数字与实际验证结果自动写入）

python3 tools/verify_site.py         # 验证器：期望 RESULT: PASS
python3 tools/shoot_pages.py --all mm  # 可选：Chrome 截图看排版（一次只跑一个任务）
```

当前实测输出：

```
pages=56  shot=1411（去重 940）  dia=38  quiz=120
RESULT: PASS
```

`verify_site.py` 检查：页面结构（DOCTYPE / 单 article / article 在 footer 前 / 标签配平 / 单 h1 / id 不重复）、导航（同模块各页 href 完全一致 + 恰好 1 个 active）、站内链接与跨页锚点、截图与自绘图存在且尺寸与清单一致、图注（画面编号 + 来源）、自测 30 题答案键、**配置篇是否覆盖教材全部任务**、统计一致、文本卫生、离线自足（不引用外部资源）。

## 6. 已知边界（不要当成缺陷）

- **没有 SAP 系统可登录**。所有实训都写了「做不到环境时的替代做法」（看图说话 / 纸上推演）。
- **截图是教材原图**，多数 400–700px 宽（教材作者在图上画了红框），放大到 2× 以上会糊；页面提供点击 4× 灯箱，投屏建议 1.5×。
- 教材任务的**编号与顺序保持原样**（含个别标题为空、路径指向前台任务的情况），配置篇按 A–F 重新分组以便授课，但不改任务内容。
- 术语按中文教学场景写，英文原名在每模块的 `glossary.html` 对照。
- 自绘图是**教学示意图**，不是 SAP 的官方结构图；数值为课程场景值。

## 7. 交付记录（本次会话）

| 项 | 值 |
|---|---|
| 验证结果 | pages=56  shot=1411（去重 940）  dia=38  quiz=120 / RESULT: PASS |
| 快照（本站所在生态） | _snapshots/sap_training_sites_10sites_20260914_223923_modules.tar.gz |
| 快照内容 | 56 MB / 4560 files / gzip -t OK / 内含 sap_modules_cn 1088 项 |
| Git 提交 | cb2a6c77f71ff1469657920f2bd04dbbe36595d5（parent repo raysource/sap-consult, main） |
| 提交证明 | local HEAD == git ls-remote origin main == gh api commits/main |
| 远端只读校验 | raw.githubusercontent 只读校验：index.html / mm/index.html / co/config.html / README.md / PP_课程大纲_学习WBS.xlsx / assets/diagrams/mm/mindmap.svg / assets/img/mm/t22/01_1_image612.png 全部 HTTP 200 |
| 并发写注意 | PROGRESS.md 在保存进度期间被併走セッション改写（82891 → 84426 bytes / 90s），按经验未在改写中编辑它；本站的交付记录改记在本文件（由 make_readme.py 生成）。 |

本次修掉的缺陷：

- build_pages.py 统计口径与 verify_site.py 对齐（原先首页放截图必然统计不一致 FAIL）→ 四个模块首页补上 6 张「代表性画面」
- walk.render_task 把教材 values（{k,v} dict）渲染成「字段 / 值」两列表，不再打印生 dict
- shot-grid 缩略图限制高度（竖长截图不再撑高整行）
- svgkit：画布高度回填 + chip_rows 返回值语义修正（4 面板的图曾涨到 4642px → 688px）

## 8. 与 SD 课程站的关系

销售与分销（SD）已有独立课程站：`../sap_cn/`（16 页，线上 `https://sap-cn-sd.vercel.app/`）。本站不重复 SD 内容，但在每个模块的「集成关系」里指出与 SD 的交接点（MM 的 601 发货、FI 的应收账款、PP 的需求来源、CO 的获利分析）。

