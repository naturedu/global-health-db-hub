# 引用、致谢与数据可用性声明规范

> 论文里"数据从哪来"这三处最容易写错：Acknowledgements、Data Availability Statement、References。
> 写错会被审稿人要求补，写漏属于学术不端边缘。本文件给出可直接套用的模板。

---

## 一、三处文本的分工

| 位置 | 写什么 | 不写什么 |
|---|---|---|
| **Acknowledgements（致谢）** | 感谢数据提供方与资助，含**批准编号** | 不写具体变量、不写结论 |
| **Data Availability（数据可用性）** | 数据在哪、怎么申请、能不能共享 | 不要只写"数据可向作者索取"（受控数据禁止） |
| **References（参考文献）** | 数据资源本身的正式引用条目 | 不要把致谢句塞进参考文献 |

---

## 二、通用致谢模板

### 英文（通用）
```
This research used data from <DATABASE NAME>. Data access was granted under
approved application / project number [XXXXX] (or through a collaboration
agreement with the data custodian). The findings and conclusions are those of
the authors and do not necessarily represent the views of the data provider.
```

### 中文（通用）
```
本研究使用了 <数据库名称> 的数据，数据获取经批准的项目编号为 [XXXXX]
（或依据与数据管理方的合作协议）。本研究的发现与结论由作者负责，不代表
数据提供方的观点。
```

> `[XXXXX]` 必须替换为真实批准编号；合作制数据改为写"依据与 XX 团队的合作协议（协议编号 [XXXXX]）"。

---

## 三、重点库的官方/推荐句式

### UK Biobank（官方指定句式，不可改写）
```
This research has been conducted using the UK Biobank Resource under
Application Number [XXXXX].
```
中文说明：UKB 要求逐字使用上述英文句，编号为 AMS 系统中的 Application Number；若使用其派生队列（如 UKB-PPP），需另加一句说明。

### MIMIC-IV / MIMIC-CXR（PhysioNet）
```
The authors used data from the MIMIC-IV database (v[X.X]), which is hosted on
PhysioNet and made available under the PhysioNet Credentialed Health Data
License. The authors thank the MIT Laboratory for Computational Physiology for
maintaining the database.
```
另需在 Data Availability 中写明：**数据不可再分发**，仅可通过 PhysioNet 申请获取。

### dbGaP
```
Data were obtained from the Database of Genotypes and Phenotypes (dbGaP)
through accession number [phsXXXXXX], with data access approved under
project [XXXXX]. Genomic data were analyzed in a controlled-access
environment in accordance with the NIH Genomic Data Sharing Policy.
```
中国研究者需注意：涉及人类遗传资源出境，须在方法学或伦理部分说明国内审批情况。

### NHANES（公开数据）
```
This study used data from the National Health and Nutrition Examination Survey
(NHANES), conducted by the National Center for Health Statistics, Centers for
Disease Control and Prevention. All analyses accounted for the complex survey
design.
```

### CHARLS
```
This study used data from the China Health and Retirement Longitudinal Study
(CHARLS). The authors thank the CHARLS team and the Peking University National
School of Development for providing the data. The data are publicly available
upon registration at http://charls.pku.edu.cn.
```

### CHNS / CLHLS / CFPS
```
This study used data from the <China Health and Nutrition Survey /
Chinese Longitudinal Healthy Longevity Survey / China Family Panel Studies>.
The authors acknowledge the <XXX> team for data collection and curation.
```
> 三者均要求注册后使用，致谢中须写出数据来源全称与官网，不可只写缩写。

### GEO（基因表达）
```
The gene expression data analyzed in this study are available from the NCBI
Gene Expression Omnibus (GEO) under accession number GSE[XXXXX].
```
放在 Data Availability 更合适，Acknowledgements 可省略。

### SEER
```
This study used the SEER [18/22] registries database, released [Month Year],
based on the [November Year] submission. The interpretation of these data is
solely that of the authors and does not necessarily endorse the views of the
SEER registries or the NCI.
```

### 香港医管局（HA）
```
The authors thank the Hospital Authority of Hong Kong for providing the data
used in this study. Data access was approved by the Hospital Authority Data
Collaboration Centre / Institutional Review Board (Reference No. [XXXXX]).
```
（具体审批主体名称以实际获批文件为准。）

### 澳洲 45 and Up / MBS-PBS
```
This research was completed using data collected through the 45 and Up Study
(Sax Institute). The 45 and Up Study is managed by the Sax Institute in
collaboration with major partner Cancer Council NSW and other partners.
```
MBS/PBS 数据（Services Australia）须写明经其 Data Access 审批并给出批准号。

---

## 四、Data Availability Statement 模板

**公开数据（★/★★）**
```
The data analyzed in this study are publicly available from <DATABASE> at
<URL>. <Derived variables / analysis code> are available from the corresponding
author on reasonable request.
```
→ 注意：不能说"原始数据可向作者索取"却又用了受控数据。

**受控数据（★★★/★★★★）**
```
The data are available from <DATABASE> under a data use agreement and cannot be
shared by the authors. Requests for access should be directed to <数据管理方 /
DAC>. Approval under application number [XXXXX] was obtained.
```

**合作制数据（★★★★★）**
```
The data are owned by <机构> and were used under a collaboration agreement. The
data are not publicly available due to <隐私/伦理/协议> restrictions. Requests
may be directed to <联系人/邮箱>.
```

**代码共享（推荐做法）**
```
Analysis code is available at <GitHub URL>.
```
MIMIC/UKB 等场景：代码可开源，数据不可。这一条写清能显著提升可信度。

---

## 五、引用本平台（使用了本 Skill 的选库结论时必须加）

中文：
```
杜思娴. 全球健康数据库整合网页（Global Health Database Integration Platform）[EB/OL]. 2026.
```

英文：
```
Dusixian. Global Health Database Integration Platform [EB/OL]. 2026.
Available from: https://naturedu.github.io/global-health-db-hub/
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

---

## 六、自查清单（投稿前逐项打勾）

- [ ] 数据库全称 + 缩写首次出现处已给全
- [ ] 批准编号 `[XXXXX]` 已全部替换，没有残留占位符
- [ ] 致谢里的编号与获批文件上的编号**完全一致**
- [ ] 受控数据没有写"数据可向作者索取"
- [ ] 没有把数据上传到公开仓库（含 Supplementary、GitHub、OSF）
- [ ] 涉及中国人类遗传资源出境，已在伦理/方法部分说明
- [ ] 版本号写清（MIMIC-IV v3.1、SEER 2023 提交、UKB refresh 批次）
- [ ] 使用了本 Skill 结论的，已加平台引用
