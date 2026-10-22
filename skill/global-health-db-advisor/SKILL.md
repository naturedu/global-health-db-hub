---
name: global-health-db-advisor
description: 医学与健康公共数据库选库与申请顾问。当用户提出一个医学/公共卫生科学问题，需要判断"用哪个数据库、怎么申请、变量怎么拿、多少费用、多久周期、要不要伦理审批、论文怎么致谢"时使用；也用于按变量/指标反查哪些数据库收录该变量。覆盖 91 个数据库（UK Biobank、CHARLS、NHANES、MIMIC-IV、dbGaP、GEO、SEER、泰州队列、开滦队列、PBICR、澳洲 45 and Up、香港医管局数据等），分 12 大类、5 级开放度。触发词：数据库推荐、选哪个数据库、数据申请、变量申请、数据使用协议、DUA、数据可用性声明、致谢模板、公共数据库、队列数据、医疗大数据、NHANES 怎么用、UKB 怎么申请。
---

# 全球健康数据库整合网页 · 顾问 Skill

把一个**科学问题**转成一份可执行的**数据库使用与申请指南**：锁定 1 个主推库 + 若干备选，给出研究范式、变量清单、申请流程（方式/费用/周期）、伦理合规边界、可直接粘贴的论文致谢模板。

- 数据库总数：**91**（12 大类，5 级开放度）
- 数据来源：用户提供的《医学与健康研究公共数据库汇总》PDF（29 页）全量解析 + 澳洲/香港等条目联网核实
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

**不该用**：纯统计学方法问题（该用方法类技能）、临床指南解读、非医学数据（金融/气象）。

---

## 二、两个脚本（核心工具）

工作目录：本 Skill 根目录。Python 3.8+，**仅标准库**，无需安装依赖。

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
1. 库标签整词命中问题文本 —— +3
2. 问题里的指标词（肌酐/eGFR/血压/基因/医保…）确实出现在该库 `indicators`/`content` —— +2
3. 引导选项命中库标签 —— +2
4. 标签先去重，避免同一标签重复加权（历史 bug：MIMIC 曾因"重症"标签重复而压过儿童重症专库）

### 2) 变量反查：`scripts/varsearch.py`

```bash
python scripts/varsearch.py 肌酐
python scripts/varsearch.py eGFR --top 10
python scripts/varsearch.py "PHQ-9"
python scripts/varsearch.py 医保 --json
python scripts/varsearch.py --list-topics      # 看可用指标类目提示
```

匹配范围：`indicators` + `content` + `tags` + 库名/英文名；结果按开放度从易到难排序。

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
  "meta": {"name": "全球健康数据库整合网页", "count": 91, "source": "..."},
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

用户在论文/报告/汇报中使用了本 Skill 的选库结论或变量信息，**必须**引用：

```
杜思娴. 全球健康数据库整合网页（Global Health Database Integration Platform）[EB/OL]. 2026.
联系：dusixian16@163.com
```

BibTeX：

```bibtex
@misc{dusixian2026ghdb,
  author = {杜思娴 (Dusixian)},
  title  = {全球健康数据库整合网页 (Global Health Database Integration Platform)},
  year   = {2026},
  note   = {Contact: dusixian16@163.com}
}
```

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
```

---

## 八、回答风格

- 先给结论（锁定哪个库、一句话理由），再展开细节。
- 金额、周期这类会变的数字，标注"以官网当期说明为准"。
- 文献列表只是"代表性"，提醒用户到官网 Publications 页核对。
- 中文回答用中文；用户用英文提问则用英文。库名首次出现给中英对照。
