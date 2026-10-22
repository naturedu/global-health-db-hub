#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""输入一个科学问题 -> 锁定最合适的数据库 + 研究范式 + 申请指南。

用法:
  python advise.py "中国老年人血压变化与肾功能下降的关系"
  python advise.py "想找儿童重症的公开数据" --topic 重症 --datatype 电子病历
  python advise.py "..." --top 5 --json        # 机器可读
  python advise.py "..." --lang en             # 英文输出

可选筛选: --region 中国/美国/欧洲/英国/韩国/日本/港台/墨西哥/印度/北欧/多国
          --datatype 问卷/体检/基因/电子病历/影像/死亡随访/文本
          --design 前瞻队列/横断面/RCT二次/真实世界/预测模型/IPD/重复横断面
          --topic 老龄与认知/心血管与肾脏/肿瘤/营养代谢/职业环境/精神心理/
                  卫生经济/重症ICU/妇幼儿童/遗传组学/罕见病/卫生政策
"""
import json, os, sys, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data", "databases.json")

with open(DATA, encoding="utf-8") as f:
    BUNDLE = json.load(f)
DBS = BUNDLE["databases"]
ACCESS = {int(k): v for k, v in BUNDLE["access"].items()}
CATS = dict(BUNDLE["cats"])

# 引导选项 -> 库 tags 关键词
MAP = {
 "region": {
   "中国": ["中国"], "美国": ["美国"], "欧洲": ["欧洲"], "英国": ["英国"],
   "韩国": ["韩国"], "日本": ["日本"], "港台": ["香港", "台湾"], "墨西哥": ["墨西哥"],
   "印度": ["印度"], "北欧": ["北欧"], "多国": ["全球", "国际", "多国"]},
 "datatype": {
   "问卷": ["问卷", "自报", "量表"], "体检": ["体检", "生化", "肌酐", "血压", "检验"],
   "基因": ["基因", "组学", "测序", "转录组", "多组学"],
   "电子病历": ["电子病历", "医保", "理赔", "处方", "真实世界"],
   "影像": ["影像"], "死亡随访": ["死亡登记", "随访"], "文本": ["文本", "NLP"]},
 "design": {
   "前瞻队列": ["前瞻性", "队列"], "横断面": ["横断面", "回顾性"],
   "RCT二次": ["RCT", "二次利用", "IPD"], "真实世界": ["真实世界", "观察性", "目标试验"],
   "预测模型": ["预测模型", "风险"], "IPD": ["IPD", "meta"],
   "重复横断面": ["重复横断面"]},
 "topic": {
   "老龄与认知": ["老龄", "认知", "痴呆", "失能", "长寿", "衰弱"],
   "心血管与肾脏": ["心血管", "肾脏", "高血压", "CKD", "卒中", "心衰", "eGFR"],
   "肿瘤": ["肿瘤", "癌症"], "营养代谢": ["营养", "膳食", "代谢", "肥胖", "糖尿病"],
   "职业环境": ["职业", "暴露", "环境"],
   "精神心理": ["心理", "抑郁", "焦虑", "睡眠", "行为"],
   "卫生经济": ["卫生经济", "卫生服务", "费用", "医疗质量", "医保"],
   "重症ICU": ["ICU", "重症"], "妇幼儿童": ["儿童", "妇幼", "儿科", "青少年"],
   "遗传组学": ["基因", "组学", "遗传"], "罕见病": ["罕见病"],
   "卫生政策": ["政策", "公平", "社会"]},
}

SYN = {"肾功能": "肾脏", "肾病": "肾脏", "慢性肾脏病": "肾脏", "CKD": "肾脏",
       "中风": "卒中", "脑卒中": "卒中", "心梗": "心血管", "冠心病": "心血管",
       "心肌梗死": "心血管", "血糖": "糖尿病", "肥胖": "代谢", "老年人": "老龄",
       "老年": "老龄", "长者": "老龄", "ICU": "重症", "重症监护": "重症",
       "心理": "心理", "精神": "心理", "肿瘤": "肿瘤", "癌症": "肿瘤"}

# 具体疾病/结局词 -> 数据里实际使用的标签词（否则"肺癌"无法命中标签"肿瘤"）
DISEASE = {
 "肺癌": ["肿瘤", "癌症"], "胃癌": ["肿瘤", "癌症"], "肝癌": ["肿瘤", "癌症"],
 "结直肠癌": ["肿瘤", "癌症"], "乳腺癌": ["肿瘤", "癌症"], "食管癌": ["肿瘤", "癌症"],
 "宫颈癌": ["肿瘤", "癌症"], "前列腺癌": ["肿瘤", "癌症"], "甲状腺癌": ["肿瘤", "癌症"],
 "淋巴瘤": ["肿瘤", "癌症"], "白血病": ["肿瘤", "癌症"], "癌": ["肿瘤", "癌症"],
 "糖尿病": ["代谢", "糖尿病", "血糖"], "糖代谢": ["代谢", "糖尿病"],
 "高血压": ["血压", "高血压", "心血管"], "降压": ["血压", "高血压"],
 "卒中": ["卒中", "心血管"], "脑梗": ["卒中", "心血管"], "脑出血": ["卒中", "心血管"],
 "心衰": ["心血管", "心衰"], "心力衰竭": ["心血管", "心衰"],
 "冠心病": ["心血管", "心血管"], "动脉粥样硬化": ["心血管", "ASCVD"],
 "肾功能": ["肾脏", "eGFR"], "肾衰": ["肾脏", "ESRD"], "透析": ["肾脏", "ESRD"],
 "痴呆": ["认知", "痴呆"], "阿尔茨海默": ["认知", "痴呆", "神经"],
 "认知": ["认知"], "抑郁": ["心理", "抑郁"], "焦虑": ["心理", "焦虑"],
 "精神": ["心理", "心理健康"], "心理健康": ["心理健康", "心理"],
 "睡眠": ["睡眠", "行为"], "生活方式": ["生活方式", "膳食", "运动"],
 "肥胖": ["肥胖", "代谢"], "超重": ["肥胖", "代谢"], "营养": ["营养", "膳食"],
 "膳食": ["膳食", "营养"], "空气污染": ["环境", "暴露"], "PM2.5": ["环境", "暴露"],
 "环境": ["环境", "暴露"], "职业": ["职业", "暴露"], "粉尘": ["职业", "暴露"],
 "生存分析": ["随访", "死亡登记", "癌症登记", "登记"],
 "生存率": ["随访", "死亡登记", "癌症登记"], "预后": ["随访", "死亡登记"],
 "发病率": ["登记", "癌症登记", "监测"], "死亡": ["死亡登记", "随访"],
 "医保": ["医保", "理赔"], "报销": ["医保", "理赔"], "费用": ["费用", "医疗支出"],
 "支出": ["医疗支出", "卫生经济"], "灾难性卫生支出": ["灾难性卫生支出"],
 "健康公平": ["公平", "健康不平等"], "不平等": ["公平", "健康不平等"],
 "影像": ["影像"], "CT": ["影像"], "MRI": ["影像"], "心电图": ["心电"],
 "基因": ["基因"], "基因组": ["基因", "基因组"], "测序": ["测序"],
 "单细胞": ["单细胞"], "蛋白组": ["蛋白组"], "代谢组": ["代谢组"],
 "儿童": ["儿童", "儿科"], "儿科": ["儿童", "儿科"], "青少年": ["儿童", "青少年"],
 "妇幼": ["妇幼", "儿童"], "孕产妇": ["妇幼"],
 "失能": ["失能"], "衰弱": ["衰弱", "老龄"], "肌少症": ["肌少症", "老龄"],
 "多病共存": ["多病共存", "慢病"], "慢病": ["慢病"], "共病": ["多病共存", "慢病"],
 "预测模型": ["预测模型", "风险"], "机器学习": ["预测模型", "风险"],
}

LEX_VARS = ["肌酐", "eGFR", "胱抑素", "尿蛋白", "UACR", "血压", "血糖", "血脂",
            "糖化血红蛋白", "生化", "体检", "基因", "WGS", "RNA-seq", "单细胞",
            "甲基化", "蛋白组", "代谢组", "影像", "MRI", "CT", "死亡登记",
            "随访", "医保", "理赔", "处方", "住院", "费用"]

def expand(q):
    q = q.lower()
    extra = [v for k, v in SYN.items() if k.lower() in q]
    for k, vs in DISEASE.items():
        if k.lower() in q:
            extra += vs
    return q + " " + " ".join(extra)

# 标签词频 -> 权重（"队列""中国""公开"这类泛词几乎人人都有，权重必须压低）
FREQ = {}
for _d in DBS:
    for _t in dict.fromkeys(_d.get("tags") or []):
        FREQ[_t] = FREQ.get(_t, 0) + 1

def tag_weight(t):
    f = FREQ.get(t, 1)
    if f <= 6:
        return 3      # 特征词：CKD、卒中、空气污染、癌症登记
    if f <= 15:
        return 2      # 中等：基因、医保、重症
    return 1          # 泛词：队列、中国、合作、公开、真实世界

def var_access_text(d):
    a = d["access"]
    return {
      1: "变量级数据可公开获取：无需申请，直接下载；个体级记录通常在遵守许可（CC0/CC-BY）下可用，发表须引用来源。",
      2: "注册账号并说明用途后即可下载变量级数据（免费）；部分受限变量需额外协议。建议先查官方 codebook 核对变量名。",
      3: "需完成指定培训（如 CITI）并签署数据使用协议（DUA）后获取，周期约 2-6 周，免费；多在安全环境或授权账号内使用。",
      4: "需提交研究计划、机构审批并付费，按获批字段范围提供数据；受控数据还需 ISO 签署与 DAC 评审，周期约 1-6 个月。",
      5: "不公开下载、走合作制：需联系数据持有团队、提交方案、签协议，通常涉及共同署名；周期半年起。",
    }[a]

def score(qtext, sel):
    q = expand(qtext)
    rows = []
    for d in DBS:
        s = 0
        why = []
        tags = list(dict.fromkeys(d.get("tags") or []))  # 去重，避免同一标签重复加权
        # 1) 关键词命中：库标签出现在问题里（或前两字命中，处理"前瞻性/前瞻"）
        for t in tags:
            if len(t) >= 2 and (t in q or t[:2] in q):
                s += tag_weight(t)
                why.append(t)
        # 2) 该库确实拥有该变量（指标/内容字段命中）
        ind = (d.get("indicators", "") + " " + d.get("content", "")).lower()
        for v in LEX_VARS:
            if v.lower() in q and v.lower() in ind:
                s += 2
                why.append(v)
        # 3) 引导选项
        for g, v in sel.items():
            for kw in MAP.get(g, {}).get(v, []):
                if any(kw in t or t in kw for t in tags):
                    s += 2
                    why.append(v)
        if s > 0:
            rows.append((s, d, list(dict.fromkeys(why))[:8]))
    rows.sort(key=lambda x: -x[0])
    return rows

def fmt_db(d):
    urls = "、".join(f"[{u['label']}]({u['url']})" for u in d.get("urls", []))
    papers = d.get("papers") or []
    plist = "\n".join(f"  - {p}" for p in papers) if papers else "  - 未列出，建议到官网 Publications 页核对"
    return (
f"""### {d['name']}
**{d.get('en','')}**

| 项目 | 内容 |
|---|---|
| 开放度 | {'★'*d['access']} {ACCESS.get(d['access'],'').lstrip('★ ')} |
| 地区 / 规模 / 时间 | {d.get('region','—')} / {d.get('scale','—')} / {d.get('timeSpan','—')} |
| 主办单位 | {d.get('host','—')} |

**数据库介绍**：{d.get('intro') or d.get('content') or '—'}

**核心内容**：{d.get('content') or '—'}

**经典指标**：{d.get('indicators') or '详见官网 codebook'}

**注册 / 申请方式（流程·费用·周期）**：{d.get('usage') or '—'}

**变量申请情况**：{var_access_text(d)}

**官方入口**：{urls or '—'}

**代表性文献**（建议核对官网 Publications）：
{plist}
- PubMed 检索：{d.get('pubmed','')}

**研究范式**：{d.get('paradigm') or '—'}

**论文致谢 / 数据可用性声明（[XXXXX] 填批准编号）**
- EN: {d.get('ackEn','')}
- 中文: {d.get('ackCn','')}

**常见坑**：{d.get('notes') or '遵守数据使用协议、禁止再识别；发表注明数据来源。'}
""")

def generic_template(d):
    return f"""### 通用研究范式模板（可套用于任一数据库）
| 要素 | 内容 |
|---|---|
| 研究问题 PICO | 在 **{d.get('region','目标人群')}** 中，探讨【暴露 X】与【结局 Y】的关系（按你的问题替换） |
| 推荐数据库 | {d['name']} |
| 研究设计 | {'RCT/队列二次利用' if d['cat']=='trial' else '真实世界观察性' if d['cat'] in ('icu','rwd') else '组学分析' if d['cat']=='omics' else '前瞻/重复测量队列'} |
| 关键变量 | {d.get('indicators') or '参见 codebook'} |
| 统计方法 | 队列→Cox/GLM/轨迹；横断面→Logistic/线性；预测→C-index/校准/决策曲线 |
| 数据申请 | {d.get('usage','—')} |
| 伦理合规 | {var_access_text(d)} |
| 论文致谢 | {d.get('ackEn','')} |
"""

CITE = ("> 引用本平台：杜思娴. 全球健康数据库整合网页 [EB/OL]. 2026. "
        "Dusixian. Global Health Database Integration Platform. 联系：dusixian16@163.com")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query", nargs="*", help="科学问题（中文/英文）")
    for g in ("region", "datatype", "design", "topic"):
        ap.add_argument("--" + g, default=None)
    ap.add_argument("--top", type=int, default=4)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--lang", default="zh")
    a = ap.parse_args()

    q = " ".join(a.query).strip()
    sel = {g: getattr(a, g) for g in ("region", "datatype", "design", "topic") if getattr(a, g)}
    rows = score(q, sel)

    if not rows:
        print("未匹配到数据库。请放宽条件，或用更通用的词（如「中国 队列 血压」）。")
        return 1

    top = rows[:a.top]
    if a.json:
        print(json.dumps([{"score": s, "why": w, "db": d} for s, d, w in top],
                         ensure_ascii=False, indent=1))
        return 0

    locked = top[0][1]
    print("# 数据库推荐与申请指南\n")
    print(f"**锁定数据库**：{locked['name']}（{'★'*locked['access']}）\n")
    print(fmt_db(locked))
    if len(top) > 1:
        print("## 备选数据库\n")
        for s, d, w in top[1:]:
            u = d.get("urls", [{}])[0].get("url", "")
            print(f"- **{d['name']}**（{'★'*d['access']} {ACCESS.get(d['access'],'').lstrip('★ ')}）— "
                  f"{d.get('region','')} — 匹配：{'、'.join(w[:4])} — {u}")
        print()
    print(generic_template(locked))
    print(CITE)
    return 0

if __name__ == "__main__":
    sys.exit(main())
