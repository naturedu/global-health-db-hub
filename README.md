# 全球健康数据库整合网页 · Global Health Database Integration Platform

> 面向医学科研的**公共数据库检索、分类、申请导航与研究匹配**平台（内测版 Beta）。
> 收录 **100 个**全球健康与医学研究公共数据库、**145 条**官方入口链接，覆盖老龄追踪、生物样本库、中国本土队列、医保与电子病历（真实世界）、澳大利亚与大洋洲、重症 ICU、临床试验数据二次利用、组学仓储、卫生经济与卫生服务管理。

- 🌐 在线访问（推荐，稳定直链）：**<https://naturedu.github.io/global-health-db-hub/>**
- 🌐 备用（WorkBuddy 托管）：<https://global-health-db-hub.app.workbuddy.host/?sharecode=OPMUXAOLWT>
- 🧩 Skill 版（可装进 Claude Code / WorkBuddy / GPT）：见 [第九节](#九skill-版装进-claude-code--workbuddy--gpt)
- 👩‍🔬 创建人：**杜思娴**
- ✉️ 合作与引用联系：**dusixian16@163.com**

---

## 一、它解决什么问题

医学科研找数据的三座大山：**不知道有哪些库、不知道该用哪个库、不知道该怎么申请**。
本项目把三者合成一条路径：

1. **按研究性质分层浏览** —— 12+1 大类，每类给出该领域的主力库。
2. **输入科学问题 → 锁定数据库** —— 查询器给出 1 个主推库 + 参考范式 + 备选，并附**通用研究范式模板**。
3. **点开任意库 → 一页看清** —— 库介绍、官网直达、**注册/申请方式（流程·费用·周期）**、**变量申请情况**、经典指标、代表性文献、**论文致谢/数据可用性声明模板**。

## 二、核心功能

| 模块 | 说明 |
|---|---|
| 总览速查表 | 按地区/规模/时间跨度/开放度快速定位，**整行可点开** |
| 开放度分级 | ★ 完全公开 → ★★★★★ 必须本地合作，颜色由易到难 |
| 分类目录 | 12+1 大类卡片，含网址、核心内容、使用情况、常见坑 |
| 研究匹配查询器 | 一句话科学问题 + 地区/数据类型/设计/主题筛选 → 锁定主推库 + 参考范式 + 备选 + 通用范式模板 |
| 详情弹窗 | 库介绍 / 核心内容 / 经典指标 / 申请方式 / **变量申请情况** / 官方入口 / 代表文献 + PubMed 检索 / 常见坑 / 研究范式 / **论文致谢模板（可复制）** |
| 变量查询 | 输入「肌酐 / eGFR / PHQ-9 / PBS / 影像」等，反查哪些库收录该指标 + 变量申请情况 |
| 官方入口直达 | 一页列出 **100 库 × 145 条**官网/检索/申请入口，按分类分组，逐条可点、可核对 |
| 数据库对比 | 勾选 2–6 个库 → 生成横向对比表（开放度/规模/申请方式/变量可得性/常见坑），可导出 Markdown |
| 申请材料生成 | 选库 + 填信息 → 自动生成研究计划/数据使用申请草稿（含变量清单、DUA 要点、致谢句式） |
| 深链接与分享 | `?db=UK Biobank` 直达某库、`?ref=...` 直达查询结果，链接可复制转发 |
| 内测注册门 | 姓名 / **机构/单位** / 邮箱 / 验证码（前端 localStorage 演示）+ 邀请码 |
| 引用与联系 | **中文 GB/T 7714 / APA 7th / Vancouver / BibTeX 四种引用**一键复制，强制「使用本站须引用」 |
| 实战阶梯 | 按获取难度 ★→★★★★★ 排列的落地路径 |
| 打印与导出 | 一键打印各库要点、导出对比表与本机注册数据 |

## 三、目录结构

```
.
├── build_site.py     # 数据驱动的站点生成器（改数据 → 重跑即可）
├── index.html        # 生成的自包含单页站点（可直接双击打开 / 部署）
├── site/index.html   # 发布用副本（静态托管入口）
├── invite_qr.png     # 邀请二维码
├── skill/
│   └── global-health-db-advisor/   # 可移植 Skill（Claude Code / WorkBuddy / GPT）
│       ├── SKILL.md                    # 技能定义与工作流
│       ├── data/databases.json         # 100 库结构化数据（单一数据源）
│       ├── scripts/advise.py           # 科学问题 → 锁定库 + 申请指南
│       ├── scripts/varsearch.py        # 变量 → 反查哪些库收录
│       ├── scripts/compare.py          # 2–6 库横向对比（Markdown / JSON）
│       ├── scripts/apply_pack.py       # 申请材料包生成（研究计划 + DUA 要点）
│       ├── scripts/finddb.py           # 按机构/地区/分类/开放度筛选
│       ├── scripts/linkcheck.py        # 官网链接批量核对（并发 + 判读）
│       ├── linkreport.md               # 最近一次链接核对报告
│       └── references/                 # 开放度分级 / 引用致谢 / 研究范式
├── README.md
├── LICENSE
└── CONTRIBUTING.md
```

## 四、本地运行

无需安装任何依赖（`build_site.py` 只用标准库）：

```bash
# 1) 生成/更新站点
python build_site.py
# 输出：WROTE .../index.html entries=100 urls=145 bytes=...
#      WROTE .../skill/global-health-db-advisor/data/databases.json entries=100 urls=145

# 2) 直接打开
#   Windows: 双击 index.html
#   或起一个本地服务：
python -m http.server 8000
# 浏览器访问 http://localhost:8000
```

> 生成器仅依赖 Python 3.8+ 标准库（`json`、`os`），不需要 pip 安装。

## 五、如何修改数据（最重要）

所有内容都在 `build_site.py` 里，**改字即可，不用碰 HTML**：

| 变量 | 作用 |
|---|---|
| `CATS` | 分类清单（key + 中文名） |
| `D.append(e(...))` | 每个数据库一条记录：`name/en/cat/access/urls/region/scale/timeSpan/host/content/intro/usage/notes/tags/paradigm` |
| `IND` | 各库「经典指标」补充字典（key = 库名） |
| `PAPERS` | 代表性/里程碑文献 |
| `ACK_SPECIAL` | 论文致谢专用句式（UKB、MIMIC、dbGaP、NHANES、CHARLS、CKB、GEO） |
| `OVR` / `USAGE_FIX` | 重点库的介绍/申请流程加厚 |
| `QR` | 总览速查表分组 |

新增一个库的最小写法：

```python
D.append(e("我的队列", "My Cohort", "china_cohort", 3,
    [{"label":"官网","url":"https://example.org"}],
    region="中国", scale="约 1 万", timeSpan="2015 至今",
    host="XX 大学",
    content="……",
    intro="……",
    usage="……",
    notes="……",
    tags=["中国","队列"],
    paradigm="……"))
```

改完执行 `python build_site.py` 重新生成即可。若想同时更新 Skill 的数据，重跑导出（`build_site.py` 已内置 `data/databases.json` 导出）。

## 六、链接核对

100 个库的 145 条入口全部可核对，避免论文写作时贴错网址：

```bash
cd skill/global-health-db-advisor
python scripts/linkcheck.py                          # 全量并发核对，打印报告
python scripts/linkcheck.py --region 中国 --out linkreport.md   # 只核对某地区并写文件
python scripts/linkcheck.py --cat china_cohort --timeout 8
python scripts/linkcheck.py --only-fail              # 报告只保留问题项
```

判读规则（脚本已在表头说明）：

| 结果 | 含义 |
|---|---|
| `200` / `30x` | ✅ 可用 |
| `401` / `403` / `429` | 🔒 反爬/需登录，**不算失效**，浏览器通常能开 |
| `404` / `410` | ❌ 真失效，需换链接 |
| `0` / `502` / `timeout` | ⚠️ 本机网络/代理问题，**需人工复点**，勿直接判定失效 |

## 七、部署到线上

站点是**纯静态单页**，任何静态托管都能放（GitHub Pages / Cloudflare Pages / Vercel / Nginx / 对象存储）：

**GitHub Pages（推荐，和开源一起）**
```bash
# 仓库 Settings → Pages → Source 选 main 分支 /(root)
# 或把 index.html 放到 docs/ 目录，Source 选 /docs
```

**任意静态服务器**
```bash
python -m http.server 8000   # 临时预览
# 生产环境把 index.html 放到 Nginx 根目录即可
```

## 八、开源与许可

- 许可证：**MIT**（见 [LICENSE](LICENSE)），可自由使用、修改、分发，请保留版权声明。
- 请注意：**数据库条目内容**整理自用户提供的《医学与健康研究公共数据库汇总》PDF 及各库公开资料，**不构成官方申请入口或承诺**；引用与投稿前请**实点核对各库官网**。
- 标注「待核」的条目表示编制时无法核实（如「北方生活方式队列」的依托单位/样本量），请以官方为准。

## 九、如何引用

若你在论文、报告或标书中使用了本平台的检索、匹配或变量查询结果，**请引用**（网页「引用」区四种格式均可一键复制）：

**中文（GB/T 7714）**
```
杜思娴. 全球健康数据库整合网页：Global Health Database Integration Platform
[EB/OL]. 2026[2026-10-22]. https://naturedu.github.io/global-health-db-hub/.
联系邮箱: dusixian16@163.com.
```

**English（APA 7th）**
```
Du, S. (2026). Global health database integration platform
[Online database and research navigator].
https://naturedu.github.io/global-health-db-hub/
```

**English（Vancouver）**
```
Du S. Global Health Database Integration Platform [Internet]. 2026
[cited 2026 Oct 22]. Available from: https://naturedu.github.io/global-health-db-hub/
```

**BibTeX**
```bibtex
@misc{du2026ghdip,
  author       = {Du, Sixian},
  title        = {Global Health Database Integration Platform
                  (全球健康数据库整合网页)},
  year         = {2026},
  howpublished = {\url{https://naturedu.github.io/global-health-db-hub/}},
  note         = {Online database and research navigator; Contact: dusixian16@163.com}
}
```

正文夹注可用：中文 `（杜思娴，2026）`；英文 `(Du, 2026)`。

同时建议按各数据库要求注明版本号与数据来源，并引用该库的标志性文献/官网。

## 十、Skill 版（装进 Claude Code / WorkBuddy / GPT）

网页是给人看的，Skill 是给 AI 用的。同一套数据被封装成一个**可移植技能**：

> 输入一个科学问题 → 输出「锁定哪个库 + 研究范式 + 申请方式（费用/周期）+ 变量怎么拿 + 致谢模板」。

位置：`skill/global-health-db-advisor/`

### 直接用（不需要任何 Agent）

仅需 Python 3.8+ 标准库，零依赖：

```bash
cd skill/global-health-db-advisor

# 1) 科学问题 → 锁定库
python scripts/advise.py "中国老年人长期血压变化与肾功能下降的关系"
# → 锁定数据库：CHARLS 中国健康与养老追踪调查（★★）

python scripts/advise.py "儿童重症监护的公开数据，做预测模型" --topic 重症ICU
# → 锁定数据库：PIC 浙江大学附属儿童医院重症数据库（★★★）

# 2) 变量反查
python scripts/varsearch.py 肌酐 --top 5
# → NHANES / CHARLS / UK Biobank / QResearch …

# 3) 横向对比（2–6 个库，可存 Markdown）
python scripts/compare.py "UK Biobank" "CHARLS" "NHANES" --out cmp.md

# 4) 申请材料包（研究计划 + 变量清单 + DUA 要点 + 致谢句式）
python scripts/apply_pack.py "UK Biobank" \
    --name 杜思娴 --org 某大学公共卫生学院 --mail dusixian16@163.com \
    --q "长期血压轨迹与肾功能下降" --vars "肌酐,eGFR,血压" --out apply.md

# 5) 按机构/地区/分类/开放度筛库
python scripts/finddb.py --host 广州
python scripts/finddb.py --region 中国 --max-access 3
python scripts/finddb.py --cat china_cohort --json

# 6) 链接批量核对
python scripts/linkcheck.py --region 中国 --out skill/global-health-db-advisor/linkreport.md
```

### 装到 Claude Code

```bash
# 用户级（所有项目可用）
cp -r skill/global-health-db-advisor ~/.claude/skills/
# 或项目级
cp -r skill/global-health-db-advisor ./.claude/skills/
```

### 装到 WorkBuddy

```bash
cp -r skill/global-health-db-advisor ~/.workbuddy/skills/
# Windows: C:\Users\<用户名>\.workbuddy\skills\
```

放好后新开一个会话，说「我想用公共数据库研究 XX」即会自动触发；也可直接点名「用 global-health-db-advisor 帮我选库」。

### 装到 GPT / 只吃文本的模型

1. 把 `SKILL.md` 全文粘进「自定义指令」或 GPT Instructions；
2. 上传 `data/databases.json` 作为知识文件（或按 12 类拆成多个 md）；
3. 若平台支持 Code Interpreter，直接上传 `scripts/*.py` 让它运行。

## 十一、路线图

- [x] 100 个库的结构化条目（介绍/申请/指标/文献/致谢）+ 145 条官方入口
- [x] 研究匹配查询器 + 通用研究范式模板
- [x] 变量查询（元数据级）+ 变量申请情况
- [x] 内测注册门（姓名/机构/邮箱/验证码）+ 邀请码
- [x] 数据库对比、申请材料生成、深链接分享、打印导出
- [x] 四版引用（GB/T 7714 / APA / Vancouver / BibTeX）
- [x] **Skill 版封装（Claude Code / WorkBuddy / GPT 通用，6 个 CLI 脚本）**
- [x] **链接批量核对（`linkcheck.py` + `linkreport.md`）**
- [ ] 真实邮件验证码 + 服务端校验（需后端）
- [ ] 账号体系 + 邀请码/白名单 + 注册名单管理
- [ ] 开放库（NHANES / GEO 等）的**变量级实时提取**适配器

## 十二、致谢

内容基础来自《医学与健康研究公共数据库汇总》；澳大利亚与大洋洲条目（45 and Up、CUPL、PLIDA/ABS DataLab、MBS/PBS、AIHW、HILDA、ALSWH、Ten to Men）与中国新增条目（CCC 中国队列共享平台、GBCS 广州生物库队列、BIGCS 广州出生队列、CMHS 中国精神卫生调查、NRDRS 国家罕见病注册系统、CNRDS 全国血液净化病例信息登记、ChiCTR、NMPA 药物临床试验登记平台、CHFS、NCCR 中国肿瘤登记）已联网核实。

---

**© 2026 杜思娴 · 全球健康数据库整合网页** ｜ 合作：dusixian16@163.com
