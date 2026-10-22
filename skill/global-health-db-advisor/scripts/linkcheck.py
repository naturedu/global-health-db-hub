#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""核对 databases.json 里所有官网链接是否可访问（HTTP 状态 + 重定向后的真实地址）。

用法:
  python linkcheck.py                     # 全量检查（并发 8，超时 12s）
  python linkcheck.py 北京大学            # 只看名称/主办匹配该词的条目
  python linkcheck.py --region 中国       # 只看某地区
  python linkcheck.py --cat china_cohort  # 只看某分类
  python linkcheck.py --only-fail         # 报告只保留问题项
  python linkcheck.py --out report.md     # 写 Markdown 报告
  python linkcheck.py --json
  python linkcheck.py --workers 16        # 提高并发

判读约定（重要，务必按此向用户解释）:
  · 200/30x            → OK        正常
  · 401/403/406/429    → BLOCKED   站点存在但拒绝脚本访问（反爬/需登录），**不算失效**
  · 404/410            → BROKEN    确实失效，需要换链接
  · 5xx                → GATEWAY   上游/网关报错，**需人工复点**
  · DNS/超时/代理错    → NETFAIL   本机网络问题，**不能据此判定链接错误**
"""
import json, os, sys, argparse, urllib.request, urllib.error, socket, ssl
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "..", "data", "databases.json"), encoding="utf-8") as f:
    B = json.load(f)

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE


def check(url, timeout=12):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
            return r.status, r.geturl(), ""
    except urllib.error.HTTPError as e:
        return e.code, url, str(e.reason)
    except urllib.error.URLError as e:
        return 0, url, str(getattr(e, "reason", e))
    except socket.timeout:
        return 0, url, "timeout"
    except Exception as e:                       # noqa: BLE001
        return 0, url, type(e).__name__ + ": " + str(e)


def verdict(code):
    if 200 <= code < 400:
        return "OK"
    if code in (401, 403, 405, 406, 429):
        return "BLOCKED"
    if code in (404, 410):
        return "BROKEN"
    if 500 <= code < 600:
        return "GATEWAY"
    if code == 0:
        return "NETFAIL"
    return "WARN"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("kw", nargs="?", help="按库名/主办单位关键词过滤")
    ap.add_argument("--region", help="按地区过滤，如 中国")
    ap.add_argument("--cat", help="按分类 key 过滤，如 china_cohort")
    ap.add_argument("--only-fail", action="store_true", help="报告只保留问题项")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--out", help="写 Markdown 报告到文件")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--timeout", type=int, default=12)
    a = ap.parse_args()

    rows = []
    for d in B["databases"]:
        if a.kw and a.kw not in (d["name"] + " " + (d.get("host") or "")):
            continue
        if a.region and a.region not in (d.get("region") or ""):
            continue
        if a.cat and d.get("cat") != a.cat:
            continue
        for u in d.get("urls", []):
            url = u["url"]
            if not url.startswith(("http://", "https://")):
                rows.append({"db": d["name"], "label": u.get("label", ""),
                             "url": url, "code": 0, "final": url,
                             "err": "非网页链接，跳过", "verdict": "SKIP"})
                continue
            rows.append({"db": d["name"], "label": u.get("label", ""), "url": url})

    todo = [r for r in rows if r.get("verdict") != "SKIP"]
    if not todo:
        print("没有匹配的可核对链接，请检查过滤条件。")
        return 1

    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = [(r, ex.submit(check, r["url"], a.timeout)) for r in todo]
        for r, fu in futs:
            code, final, err = fu.result()
            r.update(code=code, final=final, err=err, verdict=verdict(code))

    if a.json:
        print(json.dumps(rows, ensure_ascii=False, indent=1))
        return 0

    groups = {"OK": [], "BLOCKED": [], "BROKEN": [], "GATEWAY": [], "NETFAIL": [], "WARN": [], "SKIP": []}
    for r in rows:
        groups[r["verdict"]].append(r)

    L = ["# 链接核对报告\n"]
    L.append("- 检查链接：**%d** 条（覆盖 %d 个库的条目）" % (len(rows), len({r["db"] for r in rows})))
    L.append("- 正常 **%d**　反爬/需登录 **%d**　真失效(404/410) **%d**　网关错误(5xx) **%d**　网络失败 **%d**　其他 **%d**"
             % (len(groups["OK"]), len(groups["BLOCKED"]), len(groups["BROKEN"]),
                len(groups["GATEWAY"]), len(groups["NETFAIL"]), len(groups["WARN"])))
    L.append("")

    if groups["BROKEN"]:
        L.append("## 一、确实失效，必须换链接（404/410）\n")
        L.append("| 数据库 | 链接名 | URL | 状态 |")
        L.append("|---|---|---|---|")
        for r in groups["BROKEN"]:
            L.append("| %s | %s | %s | %s |" % (r["db"], r["label"], r["url"], r["code"]))
        L.append("")

    if groups["GATEWAY"] or groups["WARN"]:
        L.append("## 二、异常状态，需人工复点（5xx / 其他）\n")
        for r in groups["GATEWAY"] + groups["WARN"]:
            L.append("- %s → %s（%s%s）" % (r["db"], r["url"], r["code"],
                                           "，" + r["err"][:40] if r["err"] else ""))
        L.append("")

    if groups["NETFAIL"]:
        L.append("## 三、网络失败（本机 DNS/代理问题，不能判定失效）\n")
        for r in groups["NETFAIL"]:
            L.append("- %s → %s（%s）" % (r["db"], r["url"], (r["err"] or "")[:60]))
        L.append("")

    if groups["BLOCKED"]:
        L.append("## 四、站点存在但拒绝脚本访问（反爬/需登录，**不算错**）\n")
        for r in groups["BLOCKED"]:
            L.append("- %s → %s（%s）" % (r["db"], r["url"], r["code"]))
        L.append("")

    L.append("> 判读：401/403/405/406/429 属反爬，浏览器通常能正常打开；5xx 与超时多为本机网络/代理，请手动复点后再决定是否改链接。")
    L.append("> 由「全球健康数据库整合网页 / global-health-db-advisor」生成。联系：dusixian16@163.com")

    if a.only_fail:
        L = [x for x in L if x.startswith(("#", "|", "-", ">")) and not x.startswith("- 正常")]

    md = "\n".join(L)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(md)
        print("WROTE %s（%d 条链接）" % (a.out, len(rows)))
    print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
