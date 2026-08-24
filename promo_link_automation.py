#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
推广链接自动化监控脚本框架 (promo_link_automation.py)
功能：
  1. 抓取并分类各推广链接
  2. 检测链接有效性 (HTTP 状态)
  3. 汇总渠道转化数据
  4. 定时生成报表 (Markdown / 可扩展 HTML)
适用：Windows 10/11, Python 3.8+（纯标准库，无需 pip install）
运行：python promo_link_automation.py --report weekly
      python promo_link_automation.py --report daily --email you@example.com
"""

import argparse
import csv
import json
import re
import smtplib
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime
from email.mime.text import MIMEText
from pathlib import Path

# ---------- 路径配置（与脚本同目录）----------
BASE = Path(__file__).parent
CONFIG_PATH = BASE / "promo_links.json"
CONVERSION_CSV = BASE / "conversion_data.csv"   # 手动/导出填入：channel,visits,orders,revenue
REPORT_DIR = BASE / "reports"

# ---------- 链接分类规则（按域名/关键词，按需维护）----------
CLASSIFY_RULES = [
    ("商品页",     [r"taobao\.com", r"tmall\.com", r"item\.taobao", r"goofish\.com", r"2\.taobao"]),
    ("第三方市场", [r"microsoft\.com/store", r"softpedia\.com", r"softonic\.com",
                   r"cncrk\.com", r"pcsoft\.com\.cn", r"mydown\.com"]),
    ("下载站",     [r"duote\.com", r"onlinedown\.net", r"pcdown\.net",
                   r"crsky\.com", r"newhua\.com", r"skycn\.com"]),
    ("官网落地页", [r"yourdomain\.com", r"your-product\.cn", r"cscape\.com"]),
    ("社交媒体",   [r"bilibili\.com", r"zhihu\.com", r"weixin\.qq\.com", r"mp\.weixin\.qq\.com",
                   r"douyin\.com", r"xiaohongshu\.com", r"t\.cn"]),
]


@dataclass
class LinkRecord:
    url: str
    category: str = "未分类"
    status: int = None
    reachable: bool = False
    title: str = ""
    last_checked: str = ""
    note: str = ""


def load_links() -> list:
    """读取推广链接清单；首次运行写入模板。"""
    if not CONFIG_PATH.exists():
        template = [
            {"url": "https://your-product.taobao.com/item/xxx", "channel": "淘宝商品页", "owner": "你"},
            {"url": "https://yourdomain.com/download", "channel": "官网下载页", "owner": "你"},
            {"url": "https://space.bilibili.com/your/video/xxx", "channel": "B站视频", "owner": "你"},
        ]
        CONFIG_PATH.write_text(json.dumps(template, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[初始化] 已生成模板: {CONFIG_PATH}，请替换为你的真实链接")
        return template
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def classify(url: str) -> str:
    for cat, patterns in CLASSIFY_RULES:
        for p in patterns:
            if re.search(p, url, re.I):
                return cat
    return "其他"


def check_link(url: str, timeout: int = 10) -> LinkRecord:
    rec = LinkRecord(url=url)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (promo-monitor)"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read(50000).decode("utf-8", "ignore")
            rec.status = resp.status
            rec.reachable = resp.status < 400
            m = re.search(r"<title[^>]*>(.*?)</title>", data, re.I | re.S)
            if m:
                rec.title = m.group(1).strip()[:80]
    except urllib.error.HTTPError as e:
        rec.status = e.code
        rec.reachable = e.code < 400
        rec.note = f"HTTP错误 {e.code}"
    except Exception as e:  # 超时/解析/连接失败
        rec.note = f"请求失败: {e}"
        rec.reachable = False
    rec.category = classify(url)
    rec.last_checked = datetime.now().strftime("%Y-%m-%d %H:%M")
    return rec


def load_conversion() -> list:
    if not CONVERSION_CSV.exists():
        return []
    with open(CONVERSION_CSV, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def summarize(records: list, conversions: list) -> dict:
    link_health = {}
    for r in records:
        d = link_health.setdefault(r.category, {"total": 0, "ok": 0})
        d["total"] += 1
        if r.reachable:
            d["ok"] += 1
    conv_summary = {}
    for row in conversions:
        ch = row.get("channel", "未知")
        d = conv_summary.setdefault(ch, {"visits": 0, "orders": 0, "revenue": 0.0})
        d["visits"] += int(row.get("visits", 0) or 0)
        d["orders"] += int(row.get("orders", 0) or 0)
        d["revenue"] += float(row.get("revenue", 0) or 0)
    return {"link_health": link_health, "conversion": conv_summary}


def build_report(summary: dict, records: list, period: str) -> str:
    L = [f"# 推广链接监控报表 ({period})", f"生成时间: {datetime.now():%Y-%m-%d %H:%M}", ""]
    L.append("## 链接有效性（按类别）")
    for cat, v in summary["link_health"].items():
        L.append(f"- {cat}: 有效 {v['ok']}/{v['total']}")
    L.append("")
    L.append("## 渠道转化汇总")
    if summary["conversion"]:
        for ch, v in summary["conversion"].items():
            cvr = (v["orders"] / v["visits"] * 100) if v["visits"] else 0
            L.append(f"- {ch}: 访问 {v['visits']} / 订单 {v['orders']} / 转化 {cvr:.1f}% / 营收 ¥{v['revenue']:.2f}")
    else:
        L.append("- （暂无转化数据，请维护 conversion_data.csv）")
    L.append("")
    L.append("## 异常链接（失效需处理）")
    bad = [r for r in records if not r.reachable]
    if bad:
        for r in bad:
            L.append(f"- [失效] {r.url} (状态:{r.status}) {r.note}")
    else:
        L.append("- 全部链接正常")
    return "\n".join(L)


def send_email(report: str, to: str):
    # TODO: 接入 SMTP（QQ/企业邮箱）或 WorkBuddy agent-mail 工具
    # 示例（需填真实凭据，建议放环境变量，勿硬编码）：
    # msg = MIMEText(report, "markdown", "utf-8")
    # msg["Subject"] = "推广链接周报"
    # msg["From"] = "reports@yourdomain.com"
    # msg["To"] = to
    # with smtplib.SMTP_SSL("smtp.yourmail.com", 465) as s:
    #     s.login(user, pwd); s.send_message(msg)
    print(f"[提醒] 邮件发送未配置，报表已存盘。目标邮箱: {to}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", default="daily", choices=["daily", "weekly", "monthly"])
    ap.add_argument("--email", default=None, help="接收报表的邮箱（可选）")
    args = ap.parse_args()

    REPORT_DIR.mkdir(exist_ok=True)
    links = load_links()
    records = [check_link(l["url"]) for l in links]
    conversions = load_conversion()
    summary = summarize(records, conversions)
    report = build_report(summary, records, args.report)

    fname = f"report_{args.report}_{datetime.now():%Y%m%d}.md"
    out = REPORT_DIR / fname
    out.write_text(report, encoding="utf-8")
    print(f"[完成] 报表已生成: {out}")

    if args.email:
        send_email(report, args.email)


if __name__ == "__main__":
    main()
