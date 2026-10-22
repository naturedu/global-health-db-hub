# 全球健康数据库整合网页 · Global Health Database Integration Platform

> 面向医学科研的**公共数据库检索、分类、申请导航与研究匹配**平台（内测版 Beta）。
> 收录 **91 个**全球健康与医学研究公共数据库，覆盖老龄追踪、生物样本库、中国本土队列、医保与电子病历（真实世界）、澳大利亚与大洋洲、重症 ICU、临床试验数据二次利用、组学仓储、卫生经济与卫生服务管理。

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
| 内测注册门 | 姓名 / **机构/单位** / 邮箱 / 验证码（前端 localStorage 演示） |
| 引用与联系 | 中文 / 英文 / BibTeX 三种引用格式 + 一键复制，强制「使用本站须引用」 |
| 实战阶梯 | 按获取难度 ★→★★★★★ 排列的落地路径 |

## 三、目录结构

```
.
├── build_site.py     # 数据驱动的站点生成器（改数据 → 重跑即可）
├── index.html        # 生成的自包含单页站点（可直接双击打开 / 部署）
├── site/index.html   # 发布用副本（静态托管入口）
├── invite_qr.png     # 邀请二维码
├── skill/
│   └── global-health-db-advisor/   # 可移植 Skill（Claude Code / WorkBuddy / GPT）
│       ├── SKILL.md                # 技能定义与工作流
│       ├── data/databases.json     # 91 库结构化数据（单一数据源）
│       ├── scripts/advise.py       # 科学问题 → 锁定库 + 申请指南
│       ├── scripts/varsearch.py    # 变量 → 反查哪些库收录
│       └── references/             # 开放度分级 / 引用致谢 / 研究范式
├── README.md
├── LICENSE
└── CONTRIBUTING.md
```

## 四、本地运行

无需安装任何依赖（`build_site.py` 只用标准库）：

```bash
# 1) 生成/更新站点
python build_site.py
# 输出：WROTE .../index.html entries=91 ...

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

改完执行 `python build_site.py` 重新生成即可。

## 六、部署到线上

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

## 七、开源与许可

- 许可证：**MIT**（见 [LICENSE](LICENSE)），可自由使用、修改、分发，请保留版权声明。
- 请注意：**数据库条目内容**整理自用户提供的《医学与健康研究公共数据库汇总》PDF 及各库公开资料，**不构成官方申请入口或承诺**；引用与投稿前请**实点核对各库官网**。
- 标注「待核」的条目表示编制时无法核实（如「北方生活方式队列」的依托单位/样本量），请以官方为准。

## 八、如何引用

若你在论文、报告或标书中使用了本平台的检索、匹配或变量查询结果，**请引用**：

**中文**
```
杜思娴. 全球健康数据库整合网页 [EB/OL]. 2026.
Global Health Database Integration Platform. 联系邮箱: dusixian16@163.com.
```

**English**
```
Dusixian. Global Health Database Integration Platform [EB/OL]. 2026.
Contact: dusixian16@163.com.
```

**BibTeX**
```bibtex
@misc{ghdip2026,
  author       = {Dusixian},
  title        = {Global Health Database Integration Platform
                  (全球健康数据库整合网页)},
  year         = {2026},
  howpublished = {[EB/OL]},
  note         = {Contact: dusixian16@163.com}
}
```

同时建议按各数据库要求注明版本号与数据来源，并引用该库的标志性文献/官网。

## 九、Skill 版（装进 Claude Code / WorkBuddy / GPT）

网页是给人看的，Skill 是给 AI 用的。同一套数据被封装成一个**可移植技能**：

> 输入一个科学问题 → 输出「锁定哪个库 + 研究范式 + 申请方式（费用/周期）+ 变量怎么拿 + 致谢模板」。

位置：`skill/global-health-db-advisor/`

```
SKILL.md                  # 技能定义（frontmatter: name + description）+ 工作流 + 安装说明
data/databases.json       # 91 库结构化数据（与网页同源）
scripts/advise.py         # 选库 + 申请指南
scripts/varsearch.py      # 变量反查
references/access-levels.md   # 5 级开放度与申请流程详解
references/citation-ack.md    # 引用、致谢、数据可用性声明模板
references/paradigms.md       # 12 大类研究范式骨架
```

### 直接用（不需要任何 Agent）

仅需 Python 3.8+ 标准库，零依赖：

```bash
cd skill/global-health-db-advisor

python scripts/advise.py "中国老年人长期血压变化与肾功能下降的关系"
# → 锁定数据库：CHARLS（★★）

python scripts/advise.py "儿童重症监护的公开数据，做预测模型" --topic 重症ICU
# → 锁定数据库：PIC 浙江大学附属儿童医院重症数据库（★★★）

python scripts/varsearch.py 肌酐 --top 5
# → NHANES / CHARLS / UK Biobank / QResearch …
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

放好后新开一个会话，说「我想用公共数据库研究 XX」即会自动触发。

### 装到 GPT / 只吃文本的模型

1. 把 `SKILL.md` 全文粘进「自定义指令」或 GPT Instructions；
2. 上传 `data/databases.json` 作为知识文件（或按 12 类拆成多个 md）；
3. 若平台支持 Code Interpreter，直接上传 `scripts/*.py` 让它运行。


## 十、路线图

- [x] 91 个库的结构化条目（介绍/申请/指标/文献/致谢）
- [x] 研究匹配查询器 + 通用研究范式模板
- [x] 变量查询（元数据级）+ 变量申请情况
- [x] 内测注册门（姓名/机构/邮箱/验证码）
- [x] **Skill 版封装（Claude Code / WorkBuddy / GPT 通用，含选库与变量反查 CLI）**
- [ ] 真实邮件验证码 + 服务端校验（需后端）
- [ ] 账号体系 + 邀请码/白名单 + 注册名单管理
- [ ] 开放库（NHANES / GEO 等）的**变量级实时提取**适配器
- [ ] 受控库的「申请包自动生成」

## 十一、致谢

内容基础来自《医学与健康研究公共数据库汇总》；澳大利亚条目（45 and Up、CUPL、PLIDA/ABS DataLab、MBS/PBS、AIHW、HILDA、ALSWH、Ten to Men）已联网核实。

---

**© 2026 杜思娴 · 全球健康数据库整合网页** ｜ 合作：dusixian16@163.com
