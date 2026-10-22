---
name: global-health-db-advisor
description: 医学与健康公共数据库选库与申请顾问。当用户提出一个医学/公共卫生科学问题，需要判断"用哪个数据库、怎么申请、变量怎么拿、多少费用、多久周期、要不要伦理审批、论文怎么致谢"时使用；也用于按变量/指标反查哪些数据库收录该变量、按机构或地区筛库、多个库横向对比、生成数据使用申请材料、批量核对官网链接。覆盖 100 个数据库（UK Biobank、CHARLS、NHANES、MIMIC-IV、dbGaP、GEO、SEER、泰州队列、开滦队列、PBICR、CCC 中国队列共享平台、NRDRS 国家罕见病注册系统、广州生物库队列 GBCS、澳洲 45 and Up、香港医管局数据等），分 12 大类、5 级开放度、145 条官方入口。触发词：数据库推荐、选哪个数据库、数据申请、变量申请、数据使用协议、DUA、数据可用性声明、致谢模板、公共数据库、队列数据、医疗大数据、数据库对比、申请材料、NHANES 怎么用、UKB 怎么申请。
---

# 全球健康数据库整合网页 · 顾问 Skill

把一个**科学问题**转成一份可执行的**数据库使用与申请指南**：锁定 1 个主推库 + 若干备选，给出研究范式、变量清单、申请流程（方式/费用/周期）、伦理合规边界、可直接粘贴的论文致谢模板。

- 数据库总数：**100**（12 大类，5 级开放度，**145 条**官方入口链接）
- 数据来源：用户提供的《医学与健康研究公共数据库汇总》PDF（29 页）全量解析 + 澳洲/中国新增条目（CCC、GBCS、BIGCS、CMHS、NRDRS、CNRDS、ChiCTR、NMPA、CHFS、NCCR 等）联网核实
- 维护人：杜思娴（dusixian16@163.com）

---

## 一、什么时候用这个 Skill

| 用户说的话 | 该做什么 |
|---|---|
| "我想研究中国老年人血压变化和肾功能下降，用哪个数据库？" | 跑 `advise.py`，输出锁定库 + 范式 + 申请指南 |
| "UK Biobank 怎么申请？多少钱？多久？" | 跑 `advise.py "UK Biobank"` 或直接读 `data/databases.json` 对应条目 |
| "哪些数据库有 eGFR / PHQ-9 / 医保理赔数据？" | 跑 `varsearch.py <变量名>` |
| "我要发文章，数据可用性声明怎么写？" | 取该库 `ackEn` / `ackCn`，按 `references/citation-ack.md` 填编号 |
| "受控数据能不能爬下来？" | 查 `references/access-levels.md`，明确说**不能**，给申请路由 |
| "帮我找儿童重症的公开数据" | `advise.py "儿童重症" --topic 重症ICU --datatype 电子病历` |
| "UKB、CHARLS、NHANES 哪个更适合我？" | 跑 `compare.py`，出横向对比表 |
| "帮我找广州/中国能拿到数据的库" | 跑 `finddb.py --host 广州` / `--region 中国 --max-access 3` |
| "帮我把申请材料写出来" | 跑 `apply_pack.py`，生成研究计划 + 变量清单 + DUA 要点 |
| "这些官网链接还有效吗？" | 跑 `linkcheck.py`，按判读规则区分真失效与反爬 |

**不该用**：纯统计学方法问题（该用方法类技能）、临床指南解读、非医学数据（金融/气象）。

---

## 二、六个脚本（核心工具）

工作目录：本 Skill 根目录。Python 3.8+，**仅标准库**，无需安装依赖。

| 脚本 | 一句话职责 | 典型命令 |
|---|---|---|
| `advise.py` | 科学问题 → 锁定库 + 范式 + 申请指南 | `python scripts/advise.py "中国老年人血压与肾功能"` |
| `varsearch.py` | 变量 → 反查哪些库收录 | `python scripts/varsearch.py 肌酐` |
| `compare.py` | 2–6 库横向对比 | `python scripts/compare.py "UK Biobank" "CHARLS" --out cmp.md` |
| `apply_pack.py` | 生成申请材料包（Markdown） | `python scripts/apply_pack.py "UK Biobank" --name 张三 --org XX大学` |
| `finddb.py` | 按机构/地区/分类/开放度筛库 | `python scripts/finddb.py --region 中国 --max-access 3` |
| `linkcheck.py` | 批量并发核对官网链接 | `python scripts/linkcheck.py --region 中国` |

### 1) 选库 + 申请指南：`scripts/advise.py`

```bash
python scripts/advise.py "中国老年人长期血压变化与肾功能下降的关系"
python scripts/advise.py "英国大样本队列做基因与心血管疾病" --top 5
python scripts/advise.py "儿童重症监护公开数据做预测模型" --topic 重症ICU --datatype 电子病历
python scripts/advise.py "..." --json > result.json     # 机器可读
python scripts/advise.py "..." --lang en                # 英文输出（默认 zh）
```

可选筛选项（可组合，也可全部省略）：

| 参数 | 可选值 |
|---|---|
| `--region` | 中国 / 美国 / 欧洲 / 英国 / 韩国 / 日本 / 港台 / 墨西哥 / 印度 / 北欧 / 多国 |
| `--datatype` | 问卷 / 体检 / 基因 / 电子病历 / 影像 / 死亡随访 / 文本 |
| `--design` | 前瞻队列 / 横断面 / RCT二次 / 真实世界 / 预测模型 / IPD / 重复横断面 |
| `--topic` | 老龄与认知 / 心血管与肾脏 / 肿瘤 / 营养代谢 / 职业环境 / 精神心理 / 卫生经济 / 重症ICU / 妇幼儿童 / 遗传组学 / 罕见病 / 卫生政策 |
| `--top N` | 返回前 N 个（默认 4，第 1 个为锁定库） |

输出结构：`锁定数据库` → `库介绍/核心内容/经典指标/申请方式/变量申请情况/官方入口/代表文献/研究范式/致谢模板/常见坑` → `备选数据库` → `通用研究范式模板` → `引用本平台`。

**打分逻辑**（回答用户"为什么是它"时要能解释）：
1. 库标签整词命中问题文本 —— 按词频加权：该标签在库中出现 ≤6 个 → 3 分，≤15 → 2 分，>15 → 1 分（泛标签自动降权）
2. 问题里的指标词（肌酐/eGFR/血压/基因/医保…）确实出现在该库 `indicators`/`content` —— +2
3. 引导选项命中库标签 —— +2
4. 用户点名某个库：全名出现在问题里 —— **+8**；别名（英文缩写如 UKB/CHARLS，或库名里的中文片段）—— **+6**
5. 标签先去重，避免同一标签重复加权（历史 bug：MIMIC 曾因"重症"标签重复而压过儿童重症专库）
6. **平局裁决**：分数相同时，稀有标签命中更多者优先，再取名称较短者（专库优先于系列库/总平台）
7. 同义词表 `SYN`、病名词表 `DISEASE`（如"子宫内膜异位症"→妇科/女性、"卒中"→脑血管、"脓毒症"→感染/重症）、意图词表 `INTENT`（"有哪些/目录/平台"→目录型库）负责把口语问题翻译成库标签

网页端与 Skill 端使用**同一套词表与权重**，改一侧必须同步另一侧。

### 2) 变量反查：`scripts/varsearch.py`

```bash
python scripts/varsearch.py 肌酐
python scripts/varsearch.py eGFR --top 10
python scripts/varsearch.py "PHQ-9"
python scripts/varsearch.py 医保 --json
python scripts/varsearch.py --list-topics      # 看可用指标类目提示
```

匹配范围：`indicators` + `content` + `tags` + 库名/英文名；结果按开放度从易到难排序。

### 3) 横向对比：`scripts/compare.py`

```bash
python scripts/compare.py "UK Biobank" "CHARLS" "NHANES"
python scripts/compare.py "泰州队列" "开滦队列" "CCC" --out cmp.md
python scripts/compare.py "MIMIC-IV" "eICU" --json
```

输出 11 行对比：开放度 / 地区 / 规模 / 时间跨度 / 主办单位 / 核心内容 / 经典指标 / 申请方式 / 变量可得性 / 常见坑 / 官网。
库名匹配四级：全名 → 英文名/缩写 → 名称前缀 → 包含（所以 `NHANES` 不会误命中 `KNHANES`）。最多 6 个库。

### 4) 申请材料包：`scripts/apply_pack.py`

```bash
python scripts/apply_pack.py --list                        # 查看 100 个库名
python scripts/apply_pack.py "UK Biobank" \
    --name 杜思娴 --org "某大学公共卫生学院" --mail dusixian16@163.com \
    --q "长期血压轨迹与肾功能下降的关联" \
    --vars "肌酐,eGFR,血压,降糖药" \
    --design "前瞻队列" --when "2026-12" --fee "约 9000 英镑" \
    --out apply.md
```

生成结构：申请人信息 → 研究背景与目的 → 拟用变量清单 → 研究设计与统计方法 → 伦理与合规承诺 → 数据使用与保密 → 致谢与成果约定 → 提交前核对清单（`[XXXXX]` 为待替换编号）。
**这是草稿**，必须提醒用户按官网当期模板逐项核对。

### 5) 按机构/地区/分类筛库：`scripts/finddb.py`

```bash
python scripts/finddb.py --host 广州                    # 按主办单位关键词
python scripts/finddb.py --region 中国 --max-access 3   # 中国且开放度 ≤★★★
python scripts/finddb.py --cat china_cohort             # 按分类 key
python scripts/finddb.py --keyword 医保 --json          # 全文关键词
```

结果按开放度从易到难排列，每条给出「名称 / 分类 / 地区 / 主办单位 / 官网」。

### 6) 链接批量核对：`scripts/linkcheck.py`

```bash
python scripts/linkcheck.py                                   # 全量并发
python scripts/linkcheck.py --region 中国 --out linkreport.md  # 只核对某地区并写文件
python scripts/linkcheck.py --cat china_cohort --timeout 8
python scripts/linkcheck.py 广州 --only-fail                   # 按关键词过滤，只看问题项
```

**判读规则（必须照此向用户解释，不要一概说"链接失效"）**：

| 结果 | 判定 |
|---|---|
| `200` / `30x` | ✅ 可用 |
| `401` / `403` / `429` / `406` | 🔒 反爬或需登录，**不算失效**，浏览器通常能开 |
| `404` / `410` | ❌ 真失效，需换链接 |
| `0` / `502` / 超时 | ⚠️ 本机网络或代理问题，**必须人工复点**，不得直接判定失效 |

已知历史误报：CCC 官网、GDBIG、`chinacohort.bjmu.edu.cn` 在代理环境下返回 502，实际可访问；ChiCTR 的 `searchproj.html` 返回 405 属正常（仅支持 POST）。

---

## 三、标准工作流（照着走）

1. **判定意图**：是"给问题找库"还是"给变量找库"。
2. **抽取要素**：从用户问题里抓出 `人群/地区`、`暴露`、`结局`、`数据类型`、`研究设计`、`样本量诉求`。缺失就问一句，不要编。
3. **先跑脚本**，不要凭记忆答。
4. **锁定库后必须补齐四件事**（这是本 Skill 的验收线）：
   - 申请方式：**谁批、填什么、要不要钱、多久**
   - 变量申请情况：按 5 级开放度说明能不能拿到变量级数据
   - 官方入口：把 `urls` 里的链接原样给出（不要自己拼 URL）
   - 致谢/数据可用性声明：给 `ackEn` + `ackCn`，`[XXXXX]` 注明是批准编号占位
5. **给研究范式**：暴露-结局-协变量-统计方法-敏感性分析，能直接写进 protocol。
6. **点明风险**：样本代表性与外推限制、变量缺失年份、再识别禁令、共同署名要求。
7. **收尾**：附"引用本平台"一句（见下）。

### 四条专项工作流

**A. 对比选库（"到底选哪个"）**
1. 用 `compare.py` 把 2–6 个候选库拉成一张表；
2. 结合用户的**数据可得性**（能付多少、能等多久、有无本地合作方）先砍掉开放度过高的；
3. 明确给结论："以你现在条件，先做 X，Y 作为敏感性分析的第二数据源"，并说明代价差异（费用/周期/署名）。

**B. 申请材料（"帮我写申请"）**
1. 先确认三件事：库名、申请人姓名/机构/邮箱、拟研究问题与变量；
2. 跑 `apply_pack.py` 出 Markdown 草稿；
3. 交付时**必须**加一句："这是草稿，`[XXXXX]` 是批准编号占位，请按官网当期模板逐项核对后再提交。"

**C. 按机构/地区找库（"我们学校/广州有哪些能用的库"）**
1. `finddb.py --host <机构关键词>` 或 `--region <地区> --max-access <N>`；
2. 按开放度分组呈现，★★★ 及以上直接标注"需签 DUA/培训"，★★★★★ 标注"须本地合作+共同署名"。

**D. 链接核对（"这些网址还能打开吗"）**
1. 跑 `linkcheck.py`；
2. **严格按判读表分类**，把 403/406 归为"反爬，浏览器能开"，把 502/超时归为"本机网络问题，需人工复点"，只有 404/410 才说"失效"；
3. 给出替换建议（换官网首页 / 换检索页 / 换镜像）。

---

## 四、5 级开放度（判断"能不能拿到变量"的唯一标准）

| 级别 | 含义 | 变量能否拿到 | 典型库 |
|---|---|---|---|
| ★ | 完全公开 | 可，直接下载，注意许可 | NHANES、GEO、SEER、GBD、World Bank |
| ★★ | 注册后下载 | 可，免费，需说明用途 | CHARLS、CHNS、CLHLS、PBICR |
| ★★★ | 培训 + 协议（DUA） | 可，完成 CITI 等培训、签 DUA，2–6 周 | UK Biobank、MIMIC-IV、All of Us |
| ★★★★ | 正式申请 + 付费 | 部分可，按获批字段，1–6 个月 | dbGaP、部分医保/商保数据 |
| ★★★★★ | 必须本地合作 | 通常不可，需合作+共同署名，半年起 | 中国大型队列的原始个体数据、香港医管局 |

**合规红线（必须对用户说清）**：
- ★★★ 及以上库，**不可能**通过网页抓取获得个体级记录；平台只能提供变量字典（元数据）+ 申请路由。
- 涉人数据一律不得尝试再识别；跨境传输受《人类遗传资源管理条例》等约束（中国数据出境需备案/审批）。
- 不要把"能查到变量名"说成"能拿到变量值"。

详细流程见 `references/access-levels.md`。

---

## 五、数据文件

`data/databases.json` —— 单一数据源，结构：

```json
{
  "meta": {"name": "全球健康数据库整合网页", "count": 100, "urls": 145, "source": "..."},
  "access": {"1": "★ 完全公开", "2": "★★ 注册后下载", "...": "..."},
  "cats": [["cohort", "大型人群队列"], ["..."], "..."],
  "databases": [
    {
      "name": "中国健康与养老追踪调查", "en": "CHARLS", "cat": "cohort", "access": 2,
      "region": "中国", "scale": "...", "timeSpan": "...", "host": "...",
      "content": "...", "intro": "...", "usage": "...", "notes": "...",
      "tags": ["..."], "paradigm": "...", "qr": "...", "lite": false,
      "indicators": "...", "papers": ["..."], "pubmed": "...",
      "ackEn": "...", "ackCn": "...",
      "urls": [{"label": "官网", "url": "https://..."}]
    }
  ]
}
```

**新增/修改库的规则**：
- 只加 `databases` 数组元素，字段名严格照上表；`access` 用 1–5 整数。
- `tags` 越具体越好（如"血压""肾功能""生物标志物"），不要写"医学""研究"这类泛词——会污染打分。
- 没核实的信息**不要写**，用 `"待核"` 标记，或直接省略字段。
- 改完跑一次自检：`python scripts/advise.py "中国老年人血压" `，确认锁定的库没变味。

---

## 六、引用与署名（强制）

用户在论文/报告/汇报中使用了本 Skill 的选库结论或变量信息，**必须**引用。按目标期刊要求四选一：

**中文（GB/T 7714）**
```
杜思娴. 全球健康数据库整合网页：Global Health Database Integration Platform
[EB/OL]. 2026[2026-10-22]. https://naturedu.github.io/global-health-db-hub/.
联系邮箱: dusixian16@163.com.
```

**English（APA 7th，最通用）**
```
Du, S. (2026). Global health database integration platform
[Online database and research navigator].
https://naturedu.github.io/global-health-db-hub/
```

**English（Vancouver，医学期刊常用）**
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

正文夹注：中文 `（杜思娴，2026）`；英文 `(Du, 2026)`。

数据库本身的致谢句式见各库 `ackEn` / `ackCn`；写法规范见 `references/citation-ack.md`。

---

## 七、安装到不同平台

**Claude Code / Claude Desktop（skills 目录）**
```bash
# 用户级
cp -r global-health-db-advisor ~/.claude/skills/
# 项目级
cp -r global-health-db-advisor ./.claude/skills/
```
Claude 读到 `SKILL.md` 的 `description` 后按需加载。

**WorkBuddy**
```bash
cp -r global-health-db-advisor ~/.workbuddy/skills/
```
（Windows 为 `C:\Users\<用户名>\.workbuddy\skills\`）放好后重开一个会话即可被识别。

**ChatGPT / 其他只吃文本的模型**
- 把本 `SKILL.md` 全文粘进「自定义指令 / GPT Instructions」；
- 再上传 `data/databases.json`（或按分类拆成 12 个 md）作为知识文件；
- 若平台支持 Code Interpreter，可直接上传 `scripts/*.py` 让其运行。

**纯命令行使用**（不依赖任何 Agent）
```bash
python scripts/advise.py "你的科学问题"
python scripts/varsearch.py 变量名
python scripts/compare.py "库A" "库B"
python scripts/apply_pack.py "库名" --name 姓名 --org 机构 --mail 邮箱
python scripts/finddb.py --region 中国 --max-access 3
python scripts/linkcheck.py
```

---

## 八、回答风格

- 先给结论（锁定哪个库、一句话理由），再展开细节。
- 金额、周期这类会变的数字，标注"以官网当期说明为准"。
- 文献列表只是"代表性"，提醒用户到官网 Publications 页核对。
- 中文回答用中文；用户用英文提问则用英文。库名首次出现给中英对照。
