#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""按机构 / 地区 / 分类 / 开放度检索数据库（相当于站点的筛选器）。

用法:
  python finddb.py --host 北京大学
  python finddb.py --host 医院 --access 3
  python finddb.py --region 中国 --cat china_cohort
  python finddb.py --cat icu --access 3
  python finddb.py --keyword 影像
  python finddb.py --host 大学 --json
  python finddb.py --cats            # 列出分类 id
"""
import json, os, sys, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "..", "data", "databases.json"), encoding="utf-8") as f:
    B = json.load(f)
DBS = B["databases"]
ACCESS = {int(k): v for k, v in B["access"].items()}
CATS = dict((k, v) for k, v in B["cats"])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", help="主办单位关键词，如 北京大学 / 医院 / CDC")
    ap.add_argument("--region", help="地区关键词，如 中国 / 英国 / 美国 / 澳大利亚")
    ap.add_argument("--cat", help="分类 id，见 --cats")
    ap.add_argument("--access", type=int, help="开放度 1-5（可写 3 表示恰好三级）")
    ap.add_argument("--max-access", type=int, help="开放度 ≤ N（越容易获取越靠前）")
    ap.add_argument("--keyword", help="在名称/内容/指标/标签中检索关键词")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--cats", action="store_true", help="列出分类 id")
    a = ap.parse_args()

    if a.cats:
        for k, v in CATS.items():
            n = sum(1 for d in DBS if d["cat"] == k)
            print("%-14s %-34s %d 个" % (k, v, n))
        return 0

    hits = list(DBS)
    if a.host:
        h = a.host.lower()
        hits = [d for d in hits if h in (d.get("host") or "").lower()]
    if a.region:
        r = a.region.lower()
        hits = [d for d in hits if r in (d.get("region") or "").lower()]
    if a.cat:
        hits = [d for d in hits if d["cat"] == a.cat]
    if a.access:
        hits = [d for d in hits if d["access"] == a.access]
    if a.max_access:
        hits = [d for d in hits if d["access"] <= a.max_access]
    if a.keyword:
        k = a.keyword.lower()
        def blob(d):
            return " ".join([d.get("name", ""), d.get("en", ""), d.get("host", ""),
                             d.get("content", ""), d.get("indicators", ""),
                             " ".join(d.get("tags") or [])]).lower()
        hits = [d for d in hits if k in blob(d)]

    if not hits:
        print("没有符合条件的数据库。试试放宽 --host / --region / --max-access。")
        return 1
    hits.sort(key=lambda d: (d["access"], d["name"]))

    if a.json:
        print(json.dumps([{"name": d["name"], "en": d.get("en"), "access": d["access"],
                           "region": d.get("region"), "host": d.get("host"),
                           "cat": d["cat"], "urls": d.get("urls")} for d in hits],
                         ensure_ascii=False, indent=1))
        return 0

    print("# 检索结果：%d 个（按开放度从易到难）\n" % len(hits))
    for d in hits:
        u = (d.get("urls") or [{}])[0].get("url", "")
        print("%s %s" % ("★" * d["access"], d["name"]))
        print("   %s ｜ %s ｜ %s" % (CATS.get(d["cat"], "—"), d.get("region") or "—", d.get("host") or "—"))
        if u:
            print("   %s" % u)
    print("\n> 引用：杜思娴. 全球健康数据库整合网页 [EB/OL]. 2026. 联系：dusixian16@163.com")
    return 0

if __name__ == "__main__":
    sys.exit(main())
