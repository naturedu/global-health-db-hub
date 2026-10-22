#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成「数据使用申请材料」草稿（Markdown）。

用法:
  python apply_pack.py "CHARLS" --title "血压轨迹与肾功能下降" --name 张三 --org "XX 大学" --mail a@b.com
  python apply_pack.py "UK Biobank" --q "血压变异性与 eGFR 下降" --vars "血压,血肌酐,胱抑素C,eGFR"
  python apply_pack.py "MIMIC-IV" --out my_pack.md          # 写入文件
  python apply_pack.py --list                                # 看可选库名

输出包含：申请人信息 / 研究摘要 / 数据清单 / 伦理合规声明 / 申请步骤 checklist / 致谢与数据可用性声明 / 平台引用。
所有 [XXXXX] 为占位，需替换为真实伦理批件号与批准编号。
"""
import json, os, sys, argparse, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "..", "data", "databases.json"), encoding="utf-8") as f:
    B = json.load(f)
DBS = B["databases"]
ACCESS = {int(k): v for k, v in B["access"].items()}
CATS = dict((k, v) for k, v in B["cats"])

FENCE = "`" * 3
TODAY = datetime.date.today().isoformat()

def find(name):
    """全名 → 英文名 → 名称前缀 → 包含，四级匹配（避免 NHANES 命中 KNHANES）。"""
    n = " ".join(name.strip().lower().split())
    for d in DBS:                                   # 1) 全名字面相同
        if d["name"].lower() == n:
            return d
    for d in DBS:                                   # 2) 英文名/缩写相同
        en = (d.get("en") or "").lower().strip()
        if en and (en == n or en.split("(")[0].split("（")[0].strip() == n):
            return d
    pre = [d for d in DBS if d["name"].lower().startswith(n)]   # 3) 前缀
    if pre:
        pre.sort(key=lambda d: len(d["name"]))
        return pre[0]
    cands = [d for d in DBS if n in d["name"].lower() or n in (d.get("en") or "").lower()]
    if cands:                                       # 4) 包含，短名优先
        cands.sort(key=lambda d: len(d["name"]))
        return cands[0]
    return None

def var_access_text(d):
    return {
        1: "变量级数据可公开获取：无需申请，直接下载；发表须引用来源。",
        2: "注册账号并说明用途后即可下载变量级数据（免费）；部分受限变量需额外协议。",
        3: "需完成指定培训（如 CITI）并签署数据使用协议（DUA）后获取，周期约 2-6 周，免费。",
        4: "需提交研究计划、机构审批并付费，按获批字段范围提供数据；受控数据还需 ISO 签署与 DAC 评审，周期 1-6 个月。",
        5: "不公开下载、走合作制：需联系数据持有团队、签协议，通常涉及共同署名，周期半年起。",
    }[d["access"]]

def steps(d):
    a = d["access"]
    if a == 1:
        return ["确认官网许可条款（CC0 / CC-BY / 自定义）与商用限制",
                "下载 codebook / Data Dictionary，核对变量名与年份",
                "下载数据文件（可用 R/Python 官方包直接取数）",
                "论文中注明数据来源与版本，并按官网要求引用"]
    if a == 2:
        return ["在官网注册账号（建议机构邮箱，通过更快）",
                "填写研究用途 / 项目名称 / 简要研究问题",
                "同意数据使用条款（不得再分发、不得再识别）",
                "下载 codebook + 问卷 + 数据集，核对各轮变量编码是否变化"]
    if a == 3:
        return ["完成 CITI「Data or Specimens Only Research」等培训并取得证书编号",
                "在平台建立项目，填写研究摘要、所需字段/表、分析计划",
                "由所在机构签署数据使用协议（DUA）——个人签无效，需科研管理部门盖章",
                "平台审核（自动 + 人工），按需缴费（如 UK Biobank 按项目规模收费）",
                "获得访问权限（云端/受控环境），记录 Application Number 用于论文致谢"]
    if a == 4:
        return ["阅读官方 Data Use Certification / 申请指南",
                "由机构签署官（Signing Officer）提交申请，附 Research Use Statement",
                "准备伦理批件、研究计划、变量清单与预算说明",
                "等待 DAC 评审（月度/季度），按获批字段与年数计价",
                "在受控环境内分析，导出结果需审核",
                "签署补充协议后获取扩展变量"]
    return ["撰写 1-2 页研究意向书，说明问题、变量需求、预期产出",
            "通过官网/通讯作者联系数据持有团队，确认变量可行性",
            "双方 PI 沟通署名、知识产权与数据边界（多数要求共同署名）",
            "签署合作协议 + 双方伦理审批（IRB）",
            "派研究者驻场或远程受控环境分析，论文投稿前经数据方审阅"]

def data_availability(d):
    if d["access"] >= 3:
        return ("The data are available from %s under a data use agreement and cannot be shared by the "
                "authors. Requests for access should be directed to the data custodian. Approval under "
                "application number [XXXXX] was obtained." % (d.get("en") or d["name"]))
    url = (d.get("urls") or [{}])[0].get("url", "")
    return ("The data analyzed in this study are publicly available from %s at %s. Analysis code is "
            "available from the corresponding author on reasonable request."
            % (d.get("en") or d["name"], url))

def build(d, a):
    L = []
    L.append("# 数据使用申请材料 · %s" % d["name"])
    L.append("> 生成日期：%s　｜　生成工具：全球健康数据库整合网页 / global-health-db-advisor" % TODAY)
    L.append("> 本文件为**申请草稿**，提交前请按 %s 官方最新要求逐项核对；[XXXXX] 处需替换为真实编号。"
             % d["name"])
    L.append("")
    L.append("## 一、申请人信息")
    L.append("")
    L.append("| 项目 | 内容 |")
    L.append("|---|---|")
    L.append("| 申请人 | %s |" % a.name)
    L.append("| 机构 / 单位 | %s |" % a.org)
    L.append("| 联系邮箱 | %s |" % a.mail)
    L.append("| 拟申请时间 | %s |" % a.when)
    L.append("| 经费 / 预算 | %s |" % a.fee)
    L.append("")
    L.append("## 二、研究摘要")
    L.append("")
    L.append("**题目**：%s" % a.title)
    L.append("")
    L.append("**研究问题**：%s" % a.q)
    L.append("")
    L.append("**研究设计**：%s" % a.design)
    L.append("")
    L.append("**研究背景与目的**：（补 100-150 字：公共卫生意义、现有证据缺口、本研究要回答什么）")
    L.append("")
    L.append("**方法与分析计划**：（补：研究人群与纳排标准、暴露与结局的操作化定义、协变量、"
             "主分析模型、敏感性分析、缺失值处理）")
    L.append("")
    L.append("**预期产出**：（补：拟投期刊/报告、对政策或临床的意义）")
    L.append("")
    L.append("## 三、拟申请数据清单")
    L.append("")
    L.append("| 项目 | 说明 |")
    L.append("|---|---|")
    L.append("| 数据库 | %s%s |" % (d["name"], "（%s）" % d["en"] if d.get("en") else ""))
    L.append("| 分类 | %s |" % CATS.get(d["cat"], "—"))
    L.append("| 主办单位 | %s |" % (d.get("host") or "—"))
    L.append("| 开放度 | %s %s |" % ("★" * d["access"], ACCESS[d["access"]]))
    L.append("| 覆盖地区 / 规模 / 时间 | %s / %s / %s |" % (d.get("region") or "—",
                                                       d.get("scale") or "—",
                                                       d.get("timeSpan") or "—"))
    L.append("| 拟用变量 / 字段 | %s |" % (a.vars or d.get("indicators") or "【待填】").replace("\n", "；"))
    L.append("| 官方入口 | %s |" % (" ； ".join(u["url"] for u in d.get("urls", [])) or "—"))
    L.append("")
    L.append("**变量级数据可得性**：%s" % var_access_text(d))
    L.append("")
    L.append("## 四、伦理与合规声明")
    L.append("")
    L.append("- 本研究已/将提交 %s 伦理委员会审查，批件号 [XXXXX]（如为公开匿名数据，请说明豁免依据）。" % a.org)
    L.append("- 承诺仅将数据用于本申请所述研究目的，**不尝试再识别**任何个体，不再向第三方分发原始数据。")
    L.append("- 数据仅存储在受控设备/环境，分析结果导出前做小样本抑制（n<10 不单独报告）。")
    L.append("- 涉及跨境传输的，按《人类遗传资源管理条例》等规定另行备案/审批（如适用）。")
    L.append("- 发表时按数据方要求撰写致谢与数据可用性声明，并注明数据版本号。")
    L.append("")
    L.append("## 五、申请步骤清单")
    L.append("")
    for i, s in enumerate(steps(d), 1):
        L.append("- [ ] %d. %s" % (i, s))
    L.append("")
    L.append("## 六、致谢与数据可用性声明（获批后使用）")
    L.append("")
    L.append("**Acknowledgements（EN）**")
    L.append("")
    L.append(FENCE)
    L.append(d.get("ackEn") or "")
    L.append(FENCE)
    L.append("")
    L.append("**致谢（中文）**")
    L.append("")
    L.append(FENCE)
    L.append(d.get("ackCn") or "")
    L.append(FENCE)
    L.append("")
    L.append("**Data Availability Statement**")
    L.append("")
    L.append(FENCE)
    L.append(data_availability(d))
    L.append(FENCE)
    L.append("")
    L.append("**引用本平台（使用了本平台的检索与匹配结果，请一并引用）**")
    L.append("")
    L.append(FENCE)
    L.append("杜思娴. 全球健康数据库整合网页 [EB/OL]. 2026. 联系：dusixian16@163.com")
    L.append(FENCE)
    L.append("")
    L.append("## 七、联系方式")
    L.append("")
    L.append("%s ｜ %s ｜ %s" % (a.name, a.org, a.mail))
    return "\n".join(L)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("db", nargs="?", help="数据库名称（中文名一部分即可）")
    ap.add_argument("--title", default="【项目/论文题目】")
    ap.add_argument("--name", default="【申请人姓名】")
    ap.add_argument("--org", default="【机构】")
    ap.add_argument("--mail", default="【邮箱】")
    ap.add_argument("--q", default="【研究问题：在 XX 人群中，XX 暴露是否与 XX 结局相关】")
    ap.add_argument("--vars", default="")
    ap.add_argument("--design", default="前瞻性队列研究")
    ap.add_argument("--when", default="【拟申请时间】")
    ap.add_argument("--fee", default="【预算】")
    ap.add_argument("--out", default=None, help="写入文件（默认打印到 stdout）")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()

    if a.list:
        for d in DBS:
            print(("%s %s" % ("★" * d["access"], d["name"])).ljust(46), d.get("en", ""))
        return 0
    if not a.db:
        ap.print_help()
        return 1
    d = find(a.db)
    if not d:
        print("未找到「%s」。用 --list 查看可选库名。" % a.db)
        return 1
    md = build(d, a)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(md)
        print("WROTE %s (%d chars) → %s" % (a.out, len(md), d["name"]))
    else:
        print(md)
    return 0

if __name__ == "__main__":
    sys.exit(main())
