# c-scavenger-promo

> C盘清理大师（净盘侠）· 推广链接监控与产品方案

本仓库收录「净盘侠 · C盘清理大师」这款 Windows C 盘清理工具的产品方案，以及一套**推广链接自动化监控脚本**。

> 说明：本仓库**不含**清理工具的可执行程序/源码，仅包含产品规划文档与营销侧的自动化工具。

## 目录结构

| 文件 | 说明 |
|------|------|
| `推广监控自动化_产品方案.md` | 产品方案（名称/功能/平台/渠道/支付/授权/推广链接类型）+ 推广监控自动化任务清单 T1–T9 |
| `promo_link_automation.py` | 推广链接监控脚本：抓取并分类链接、检测 HTTP 有效性、汇总渠道转化、生成周报（纯标准库，无需 pip） |
| `promo_links.json` | 推广链接清单（首次运行自动生成模板，**请勿提交真实链接**） |
| `conversion_data.csv` | 各渠道转化数据（访问/订单/营收，手动或后台导出，**请勿提交**） |
| `.github/workflows/weekly-report.yml` | GitHub Actions 工作流：每周一 09:00（北京时间）自动跑监控并发布周报 Issue |
| `examples/` | 示例数据源（演示用，链接为公开站点 + 失效样例，**不含真实销售数据**） |
| `reports/` | 自动生成的监控报表 |

## 快速开始

```bash
# 1. 安装 Python 3.8+（脚本仅用标准库，无需 pip install）
# 2. 维护数据源
#    - 编辑 promo_links.json，填入你的真实推广链接
#    - 维护 conversion_data.csv（字段：channel,visits,orders,revenue）
# 3. 运行
python promo_link_automation.py --report weekly
# 报表输出到 reports/report_weekly_YYYYMMDD.md
```

## 自动化

脚本可接入定时任务（如 WorkBuddy 自动化 / cron / Windows 任务计划程序），每周自动抓取各推广链接、检测失效、汇总转化并生成报表。

### GitHub Actions 自动周报

仓库内置 `.github/workflows/weekly-report.yml`，**每周一 09:00（北京时间）**自动运行监控脚本，并把报表作为 Issue 发布（标签 `weekly-report` / `automated`）。

- **开箱即跑**：默认使用 `examples/` 下的示例数据演示完整流程（含一个 `.invalid` 失效链接，用于验证异常检测）。
- **接入真实数据**（推荐）：在仓库 **Settings → Secrets and variables → Actions → New repository secret** 添加：
  - `PROMO_LINKS_JSON`：你的 `promo_links.json` 完整内容（JSON 字符串）
  - `CONVERSION_CSV`：你的 `conversion_data.csv` 完整内容
  - 设好后工作流自动改用真实数据，示例数据不再生效。
- **手动触发**：Actions 页面 → 该工作流 → **Run workflow**，可随时立即跑一次。
- 报表同时写入 Job Summary，并在 Issues 中留存，方便追溯每周渠道健康度与转化。

## 许可

文档与脚本以 MIT 许可开源，供学习与二次开发使用。
