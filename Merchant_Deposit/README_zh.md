[🇨🇳 简体中文](README_zh.md) | [🇬🇧 English](README.md)

# 💼 支付管理器：成本与风控看板 (Payment Manager Dashboard)

## 📖 项目概述
**Payment Manager Dashboard** 是一个全面的、基于 Streamlit 的 Web 应用程序，旨在作为支付管理团队的中央控制塔。

该项目最初作为标准分析工具（`app_1.py`）进行原型设计，现已演变为以支付经理为中心的完整平台。主入口文件（`payment_manager.py`）集成了实时风险监控、PSP（支付服务提供商）成本管理和网关接入进度跟踪，而底层的分析标签页则提供了关于路由效率和挽回交易（Salvage）表现的深度业务洞察。

---

## ✨ 核心功能与模块

### 1. 🛡️ 支付管理器 (主页：`payment_manager.py`)
这是支付经理的核心指挥中心。
* **实时异常监控 (Real-time Anomaly Monitor)：** 每 10 分钟自动刷新一次，用于检测审批通过率的骤降。异常情况会通过即时的 UI Toast 弹窗和固定在页面顶部的红色严重警报横幅进行展示。
* **管理员身份验证 (Admin Authentication)：** 安全的访问控制机制，用于编辑敏感的成本和风险数据。
* **计划中的支付网关进度 (Planned Payment Gateways Pipeline)：** 动态甘特图，用于跟踪未来 PSP 的接入阶段（合同审批、技术对接、UAT与上线）。
* **活跃风险与事件管理 (Active Risk & Incident Management)：** 动态、带颜色标识的看板警报系统，用于跟踪正在发生的运营问题、资金冻结或保证金费率上调等风险。
* **PSP 成本与风险结构表 (PSP Cost & Risk Structure Table)：** 交互式数据库界面，允许管理员更新结算费用、保证金比率和释放条款。

### 2. 💳 信用卡类型分析 (`pages/1_cc_type_analysis.py`)
* 展示整体商户洞察与审批率的时间趋势。
* 提供直观的仪表盘（Gauge Charts）图表，按不同商户细分实时展示特定信用卡品牌（VISA, Mastercard, JCB, AMEX）的审批通过率。

### 3. 📊 PSP 分析 (`pages/2_psp_analysis.py`)
* **智能路由与成本分析：** 探索同一商户和信用卡类型在不同 PSP 之间的审批率差异。
* 包含密集的热力图（展示 PSP 与卡片类型的性能对比）以及柱状/折线组合图（用于评估处理量与审批成功率的权衡）。

### 4. 🔄 重试分析 (`pages/3_retry_analysis.py`)
* **挽回价值分析 (Salvage Value Analytics)：** 量化通过智能重试策略成功挽回的确切收入金额。
* 使用瀑布图（Waterfall charts）展示净收入影响，并通过全面的桑基图/漏斗图（Sankey/Funnel diagrams）展示各 PSP 的重试转化率。

### 5. 🔀 路由模拟器 (`pages/4_routing_simulator.py`)
* **“What-If” 假设场景建模：** 专为支付经理打造的交互式沙盒环境。
* 用户可以通过拖动滑块来分配预期的月度交易流量，系统将实时计算并预测**综合审批率 (Blended Approval Rate)**、**预估总成本 (Estimated Total Cost)**，以及与历史基准相比的潜在**净节省 (Net Savings)**。

---

## 🏗️ 架构与脚本设置

为了支持实时警报并保持 UI 代码的整洁，本应用的逻辑被解耦为前端渲染和后端后台任务两部分。

### 前端组件
* **`navbar.py`**: 自定义的水平顶部导航栏组件，取代了 Streamlit 默认的左侧侧边栏（已通过 `.streamlit/config.toml` 隐藏），提供更现代的 Web 应用交互体验。
* **`anomaly_detector.py`**: 导入主页面的 UI 异常警报组件。**注：** 目前使用模拟数据进行演示，已完全准备好在下一阶段接入实时 SQL 数据库查询。

### 后端监控 (Cron Job)
* **`risk_backend_cron.py`**: 一个独立的 Python 守护进程脚本，基于 10 分钟的时间调度（使用 `schedule` 库）持续运行。
* **当前状态：** 已做好 SQL 接入准备。目前处于模拟数据库检查状态。
* **触发动作：** 一旦检测到严重异常，该脚本将利用 Webhooks（`requests` 库）向团队的 Slack 支付频道直接推送一条自动化的 **🚨 紧急支付警报 (URGENT PAYMENT ALERT)**。

---

## 📂 项目结构

```text
Merchant_Deposit/
│
├── .streamlit/
│   └── config.toml                  # 隐藏默认侧边栏导航的配置文件
│
├── pages/
│   ├── 1_cc_type_analysis.py        # 信用卡性能分析页
│   ├── 2_psp_analysis.py            # 路由与成本分析页
│   ├── 3_retry_analysis.py          # 交易挽回价值跟踪页
│   └── 4_routing_simulator.py       # 流量分配模拟沙盒页
│
├── payment_manager.py               # 🌟 主入口文件 (Dashboard 主页)
├── app_1.py                         # 早期原型版本 (已弃用)
├── navbar.py                        # 自定义顶部导航栏组件
├── anomaly_detector.py              # 异常 UI 渲染逻辑 (目前为SQL预留了模拟接口)
├── risk_backend_cron.py             # 负责推送 Slack 警报的后台任务 (目前为SQL预留了模拟接口)
│
├── deposit.csv                      # 交易数据源
├── psp_costs.csv                    # PSP 费率结构
├── psp_fees.csv                     # 费率映射表
└── psp_risks.csv                    # 动态风险记录数据源

🚀 安装与使用指南
1. 安装环境依赖：
请确保您已安装 Python，然后在终端运行以下命令：
pip install streamlit pandas plotly streamlit-autorefresh schedule requests

2. 启动前端看板 (Frontend)：
在项目根目录下运行 Streamlit 应用：
streamlit run payment_manager.py

3. 启动后端报警守护进程 (Backend)：
打开一个新的终端窗口，启动后台监控以启用 Slack 通知：
python risk_backend_cron.py

🗺️ 未来规划 (Roadmap)
SQL 数据库集成： 重构 anomaly_detector.py 和 risk_backend_cron.py，将目前的模拟数据替换为通过 SQLAlchemy 或 psycopg2 执行的活跃 SQL 查询，直接拉取生产环境数据库的数据。

自动静音与解决机制： 允许支付经理在看板上点击异常记录的“确认 (Acknowledge)”按钮，从而暂时静音或暂停针对该特定问题的后续 Slack 报警轰炸。