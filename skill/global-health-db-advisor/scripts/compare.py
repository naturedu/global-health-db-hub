#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""横向对比 2-6 个数据库（开放度、规模、申请方式、变量可得性、常见坑）。

用法:
  python compare.py "CHARLS" "HRS" "ELSA"
  python compare.py "UK Biobank" "CKB" "泰州队列" --out cmp.md
  python compare.py "MIMIC-IV" "eICU" --json
"""
import json, os, sys, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "..", "data", "databases.json"), encoding="utf-8") as f:
    B = json.load(f)
DBS = B["databases"]
ACCESS = {int(k): v for k, v in B["access"].items()}

def find(name):
    """按 全名 → 英文名 → 名称前缀 → 包含 四级匹配，避免 NHANES 命中 KNHANES。"""
    n = " ".join(name.strip().lower().split())
    for d in DBS:                                   # 1. 中文/全名字面相同
        if d["name"].lower() == n:
            return d
    for d in DBS:                                   # 2. 英文名或缩写相同
        en = (d.get("en") or "").lower().strip()
        if en and (en == n or en.split("(")[0].split("（")[0].strip() == n):
            return d
    pre = [d for d in DBS if d["name"].lower().startswith(n)]   # 3. 前缀命中
    if pre:
        pre.sort(key=lambda d: len(d["name"]))
        return pre[0]
    cands = [d for d in DBS if n in d["name"].lower() or n in (d.get("en") or "").lower()]
    cands.sort(key=lambda d: len(d["name"]))        # 4. 包含命中，短名优先
    return cands[0] if cands else None

def vac(d):
    return {
        1: "公开直接下载", 2: "注册后下载（免费）",
        3: "培训 + 签 DUA（2-6 周）", 4: "正式申请 + 付费（1-6 月）",
        5: "必须本地合作（常含共同署名）"}[d["access"]]

ROWS = [
    ("开放度", lambda d: ACCESS[d["access"]]),
    ("地区", lambda d: d.get("region") or "—"),
    ("规模", lambda d: d.get("scale") or "—"),
    ("时间跨度", lambda d: d.get("timeSpan") or "—"),
    ("主办单位", lambda d: d.get("host") or "—"),
    ("核心内容", lambda d: d.get("content") or "—"),
    ("经典指标", lambda d: d.get("indicators") or "—"),
    ("申请方式", lambda d: d.get("usage") or "—"),
    ("变量可得性", lambda d: vac(d)),
    ("常见坑", lambda d: d.get("notes") or "—"),
    ("官网", lambda d: " ".join(u["url"] for u in d.get("urls", [])) or "—"),
]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("names", nargs="+")
    ap.add_argument("--out")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    ds = []
    for n in a.names:
        d = find(n)
        if not d:
            print("未找到：%s（用 apply_pack.py --list 查看可选库名）" % n, file=sys.stderr)
            continue
        if d not in ds:
            ds.append(d)
    if len(ds) < 2:
        print("至少需要 2 个能识别出来的数据库。")
        return 1
    if len(ds) > 6:
        ds = ds[:6]
        print("（超过 6 个，已截取前 6 个）", file=sys.stderr)

    if a.json:
        out = []
        for d in ds:
            item = {"name": d["name"], "en": d.get("en", "")}
            for k, fn in ROWS:
                item[k] = fn(d)
            out.append(item)
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return 0

    L = ["# 数据库对比（%d 个）\n" % len(ds)]
    L.append("| 维度 | " + " | ".join(d["name"] for d in ds) + " |")
    L.append("|---|" + "|".join("---" for _ in ds) + "|")
    for k, f in ROWS:
        L.append("| %s | " % k + " | ".join(str(f(d)).replace("|", "/").replace("\n", " ") for d in ds) + " |")
    L.append("")
    L.append("> 由「全球健康数据库整合网页 / global-health-db-advisor」生成。")
    L.append("> 引用：杜思娴. 全球健康数据库整合网页 [EB/OL]. 2026. 联系：dusixian16@163.com")
    md = "\n".join(L)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(md)
        print("WROTE %s（%d 个库）" % (a.out, len(ds)))
    else:
        print(md)
    return 0

if __name__ == "__main__":
    sys.exit(main())
