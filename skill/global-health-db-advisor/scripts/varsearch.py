#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""变量查询：输入指标/变量关键词，反查哪些数据库收录它，并给出申请方式与变量申请情况。

用法:
  python varsearch.py 肌酐
  python varsearch.py eGFR --top 10
  python varsearch.py "PHQ-9"
  python varsearch.py 血压 --json
  python varsearch.py --list-topics     # 列出可用的指标类目提示
"""
import json, os, sys, argparse, re

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data", "databases.json")
with open(DATA, encoding="utf-8") as f:
    B = json.load(f)
DBS = B["databases"]
ACCESS = {int(k): v for k, v in B["access"].items()}

def var_access(d):
    return {
      1: "公开直接下载",
      2: "注册后下载（免费）",
      3: "培训+签署协议（DUA）后获取",
      4: "正式申请+付费（受控数据需 ISO/DAC）",
      5: "必须本地合作（常含共同署名）",
    }[d["access"]]

def search(q, top):
    ql = q.lower().strip()
    hits = []
    for d in DBS:
        src = " ".join([d.get("indicators",""), d.get("content",""),
                        " ".join(d.get("tags") or []), d.get("name",""), d.get("en","")]).lower()
        if ql and ql in src:
            hits.append(d)
    hits.sort(key=lambda d: d["access"])
    return hits[:top] if top else hits

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("words", nargs="*")
    ap.add_argument("--top", type=int, default=15)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--list-topics", action="store_true")
    a = ap.parse_args()

    if a.list_topics:
        print("可查的指标关键词示例（也可自由输入）:\n")
        print("  肾功能类: 肌酐、eGFR、胱抑素C、尿素氮、尿酸、尿蛋白、UACR")
        print("  心血管类: 血压、血脂、血糖、糖化血红蛋白、心电图、超声")
        print("  影像/组学: 影像、MRI、CT、基因、WGS、RNA-seq、单细胞、甲基化、蛋白组、代谢组")
        print("  心理行为: PHQ-9、GAD-7、PSQI、CES-D、EQ-5D、健康素养")
        print("  医保经济: 医保、理赔、处方、费用、住院、再入院")
        print("  随访结局: 死亡登记、癌症登记、卒中、心衰、ESRD")
        return 0

    if not a.words:
        ap.print_help()
        return 1
    q = " ".join(a.words)
    hits = search(q, a.top)

    if a.json:
        print(json.dumps([{"name": d["name"], "access": d["access"],
                           "region": d.get("region"), "indicators": d.get("indicators"),
                           "usage": d.get("usage"), "urls": d.get("urls")} for d in hits],
                         ensure_ascii=False, indent=1))
        return 0

    if not hits:
        print(f"未收录含「{q}」的指标。可换更通用的词，例如：血压、基因、费用、抑郁、影像。")
        return 1

    print(f"# 变量查询：{q}\n")
    print(f"共 **{len(hits)}** 个数据库收录相关指标（按开放度从易到难）：\n")
    for i, d in enumerate(hits, 1):
        print(f"## {i}. {d['name']}（{'★'*d['access']} {var_access(d)}）")
        print(f"- 地区：{d.get('region','—')}｜主办：{d.get('host','—')}")
        print(f"- 匹配指标：{d.get('indicators') or d.get('content') or '—'}")
        print(f"- 申请方式：{d.get('usage','—')}")
        u = "、".join(f"[{x['label']}]({x['url']})" for x in d.get("urls", []))
        print(f"- 入口：{u}")
        print()
    print("> 结果为元数据级（依据公开变量说明整理），具体变量名与年份以各库 codebook / Data Dictionary 为准。")
    print("> 引用本平台：杜思娴. 全球健康数据库整合网页 [EB/OL]. 2026. 联系：dusixian16@163.com")
    return 0

if __name__ == "__main__":
    sys.exit(main())
