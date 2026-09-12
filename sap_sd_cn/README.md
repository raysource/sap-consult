# SAP S/4HANA 中文实训站（sap_sd_cn）

在线仓库（私有）：**https://github.com/raysource/sap-s4hana-cn-training**

```bash
git clone https://github.com/raysource/sap-s4hana-cn-training.git
cd sap-s4hana-cn-training && open index.html     # 纯静态，离线可看
```

同目录下的 **`S4.docx`（425 页中文教材文档）** 整理成的可离线浏览的中文培训网站。
每个任务都有 **IMG 后台路径 + T-code + 逐步手顺 + 原文档的实机画面截图**。

| 项目 | 数值（由代码自动统计，非手写） |
|---|---|
| 模块 | 6（准备工作 / FI / CO / MM / PP / SD） |
| 任务 | 222 |
| 手顺步骤 | 879 |
| 实机画面 | 1385 处引用（去重后 1209 个文件，20.7 MB） |
| 页面 | 13 |
| 配套 Excel | `S4CN_手順書_学習WBS.xlsx`（9 sheet） |

> 全部画面都是**原教材文档里作者在真实 S/4HANA 系统中截取的中文界面截图**，
> 本站只做抽取与排版：没有重绘、没有生成图、没有模拟。每张图下方都保留原文档文件名
> （`imageNNN.png`）与像素尺寸，可与 Word 原文逐张对照。

## 页面一览

| 文件 | 内容 |
|---|---|
| `index.html` | 总览：来源与规模、学习路线、6 模块卡片、页面使用说明、画面与取值的说明、姊妹站 |
| `prep.html` | 准备工作（登录系统 / 进入 SPRO 后台） |
| `fi.html` `co.html` `mm.html` `pp.html` `sd.html` | 5 个模块的手顺页：每任务 = 说明 → IMG 路径 → 输入值 → 手顺步骤（每步配画面）→ 教材笔记 |
| `tcode.html` | T-code 速查（64 个）+ IMG 后台路径（203 条） |
| `issues.html` | 排错与踩坑：原文档记录的现象 → 原因 → 处理 + 6 项前提检查 + 全站踩坑笔记索引 |
| `tasks.html` | 任务索引：222 个任务，可按模块/关键词（任务名、T-code）过滤 |
| `instructor.html` | 讲师版：5 天课时安排、每模块必演示任务、12 个必出问答、评分建议 |
| `worksheet.html` | 学员版：222 行进度打勾表 + 自系统取值栏 + 修了判定清单（可打印） |
| `quiz.html` | 自测 30 题（自动评分，75% 合格）+ 实机验收清单 |
| `S4CN_手順書_学習WBS.xlsx` | 0_説明 / 1_模块总览 / 2_手順一覧 / 3_画面索引 / 4_T-code速查 / 5_IMG路径一覧 / 6_踩坑与报错 / 7_学習WBS / 8_進捗サマリ |

站点脚本：`assets/s4cn.js` = 截图灯箱（1×/2×/3×/4×、ESC 关闭）+ 画面显示大小切换（投屏用）
+ 任务索引过滤 + IMG 路径一键复制。设计系统沿用共享的 `assets/style.css` / `main.js` / `quiz.js`，
本站只在 `assets/s4cn.css` 里追加页面族样式。

## 数据流（重建方法）

```
S4.docx
  └─ work/parse_docx.py        → work/doc_stream.json      （段落/表格/图片引用，按文档顺序）
      └─ work/build_model.py   → work/curriculum.json      （模块 → 任务 → 文本块）
          └─ work/extract_images.py → assets/img/<mod>/tNN/…（语义命名 + 内容去重 + 图标过滤）
                                       work/images.json / work/images_summary.json
              └─ work/build_site_model.py → work/site_model.json（步骤分组、IMG 路径、T-code、输入值、笔记分类）
                  ├─ tools/build_pages.py  → 13 个 HTML（+ tools/hub_stats.json）
                  └─ tools/make_cn_xlsx.py → S4CN_手順書_学習WBS.xlsx
```

```bash
cd ~/Desktop/work/training/sap_sd_cn

# 1) 从 docx 重建素材层（只在源文档变化时需要）
python3 work/parse_docx.py
python3 work/resolve_media.py
python3 work/build_model.py
python3 work/extract_images.py
python3 work/build_site_model.py

# 2) 重建站点与 Excel
python3 tools/build_pages.py          # 全部页面（也可只重建某页：… build_pages.py modules）
python3 tools/make_cn_xlsx.py

# 3) 验证（两个都必须 PASS）
python3 tools/verify_site_cn.py                                   # 本站专用：图片/锚点/nav/计数/quiz
python3 ~/.hermes/skills/productivity/sap-training-sites/scripts/verify_site.py .
```

`tools/verify_site_cn.py` 检查：1369 处 `<img src>` 与 1369 处灯箱链接是否都真实存在、
页内锚点与 `page.html#anchor` 是否都能解析、13 页的导航链接列表是否一致（每页恰好 1 个 active）、
`</article>` 位置、标签平衡、无 Markdown 残留、`<td>` 内无游离 `|`、quiz 的答案与选项键是否一致、
以及「任务数 222 / 画面引用 1369 / 索引行数 222」与模型是否一致。

## 与其他训练站的关系

本机 `~/Desktop/work/training/` 下还有 6 个**日文语境的专题站**（sap_sd / sapmto / sapeto / sapmts / sapvc /
saporderflow）。它们各自聚焦一个业务形态、使用**生成的 SVG 画面イメージ**（因为那里没有实机截图）；
本站是**中文的全模块手册站**，画面全部来自教材文档的真实截图，两者互补：

- 想要「有哪些配置点、在哪儿配、长什么样」→ 本站；
- 想要「一种业务形态从配置到练习的完整闭环」→ 专题站。

已在共享的 `tools/make_hub_page.py`（SITES/ORDER）里登记本站：因为本站不产出 `assets/gui/*.svg`，
hub 的统计改用本站写的 `tools/hub_stats.json`（页面数/步骤数/画面数）读取真实数字，
其余 6 个站的卡片与数字保持原样（本会话已用 `diff` 对比确认）。
**没有**把本站加入 `tools/verify_all_sites.py` / `verify_gui_figures.py`：那两个工具的手顺-画面契约是
「每个手顺步骤必须有一张生成的 `figure.gui` + 画面イメージ标注」，与本站「真实截图 + `figure.shot`」
的形态不同；本站用自带的 `tools/verify_site_cn.py` 做等效（更贴合）的检查。

## 已知局限（如实说明）

1. **原文文字偏少**：`S4.docx` 是「说明 + 截图」型手册，部分步骤原文只有画面没有文字。
   本站对这类步骤标注「按上一屏继续操作（画面 N）」，不做臆测补写。
2. **文档尾部有一页是扫描件**：SD 模块最后一个任务（运行资产负债表）末尾混入了 OCR 乱码段落，
   已按「连续无中文字符的乱码行」整段剔除，只保留可读的「问题 / 思路 / 解决方法」与画面。
3. **画面分辨率受原始文档限制**：多数截图宽 400〜700 px（原文档即如此），页面按自然尺寸显示，
   可点开灯箱放大 2×〜4×；投屏建议用页面顶部的「画面显示大小 1.5×/2×」。
4. **示例值属于原作者的教材环境**：公司代码 `C999`、工厂 `F999`、物料 `R999-100` / `T999-100` / `F999-100`、
   客户 `K001` / `K002` 等。操作顺序与配置点可以照搬，编号与名称请换成自己系统的值。
5. **不臆造**：标准值、字段清单、表名、SAP Note 编号若原文档未给出，本站不补；需要精确字段时请用
   系统内的 F1 / F4 与 SPRO 的文档按钮确认。

## 仓库里没有什么（以及为什么）

`.gitignore` 排除了下面这些，克隆本仓库后**不能**从零重建站点，这是有意为之：

| 排除项 | 原因 |
|---|---|
| `S4.docx`（27 MB） | 用户提供的教材文档本体，版权属于原文档/原作者，不随站点一起分发。 |
| `work/docx_extract/`（28 MB） | docx 解包结果（1385 张原图 + `document.xml`），可由 `work/parse_docx.py` 重建。 |
| `work/doc_stream*.json` `work/outline.json` | 纯中间产物（段落流/大纲），可由 `work/parse_docx.py` + `work/build_model.py` 重建。 |
| `work/render/` | 目视检查用的 Chrome 截图。 |

**站点本身是自足的**：`assets/img/` 里的 1209 张截图就是内容本体（已在仓库内），
打开 `index.html` 即可离线浏览全部 13 页，不需要 `S4.docx`。

## 素材去向

- `S4.docx` —— 原始教材文档（**保留在站点目录内**，是内容与截图的出处）。
  同一份文档在本机的 `../sap_sd/100H_S4_中国語_拆分文件_合并文件.docx` 存在同内容副本（md5 均为 `8d52c85f6957b001dc078a8e3ff75e5b`）。
- `work/docx_extract/` —— docx 解包结果（`word/media/` 里是 1385 张原图，`document.xml` 是正文）。
  属于中间产物，可随时删除后由 `work/parse_docx.py` 重建。
- `assets/img/` —— 站点实际使用的截图（语义路径 + 去重后的 1209 个文件）。
