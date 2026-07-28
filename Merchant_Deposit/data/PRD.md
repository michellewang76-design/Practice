# 产品需求文档 (PRD)

**项目名称**: Payment Manager: Cost & Risk Control Dashboard

## 1. 产品愿景
将原本分散在 Excel 表格、内部邮件和多个第三方支付网关后台的数据，统一整合为一个现代化的、交互式的“控制塔（Control Tower）”。通过实时风险监控、动态成本结构管理以及沙盒模拟功能，赋能 Payment Manager 和财务团队做出数据驱动的智能路由（Smart Routing）决策，从而最大化支付成功率并最小化处理成本。

## 2. 目标受众与问题陈述
*   **目标用户**: Payment Manager, COO, Finance Team, Risk Management Team.
*   **当前痛点**:
    *   **数据孤岛与滞后**: 各个 PSP（支付服务提供商）的费率、滚动保证金（Rolling Reserve）和结算周期散落在不同的合同中，难以直观比对。
    *   **风控响应慢**: 支付通道出现异常（如通过率暴跌、资金冻结）时，缺乏集中的预警和追踪机制。
    *   **策略评估困难**: 想要调整路由策略（例如将 20% 的流量从 Stripe 切到 Adyen），由于缺乏模拟工具，无法预估成本变化和财务影响（What-If Scenario）。
    *   **挽回价值难以量化**: 缺乏对 Retry（重试）策略所挽回的具体营收金额的直观漏斗分析。

## 3. 端到端核心功能与工作流

*   **模块 1：中央控制台 (Main Page: `payment_manager.py`)**
    *   **Gantt 进度追踪**: 宏观展示计划接入的 Payment Gateways 的集成进度（合同阶段、技术联调、UAT及上线）。
    *   **Admin 权限控制**: 提供全局密码（Session State 绑定），保护敏感财务数据的编辑权限。
    *   **交互式数据看板 (Data Editor)**: 允许管理员直接在前端双击修改、增加或删除 PSP 的费率结构（`psp_costs.csv`）和动态风险事件（`psp_risks.csv`），并一键保存至本地持久化数据库。
    *   **实时异常监控**: 前端通过 UI Toasts / Banner 提示，后端支持解耦的定时任务报警。

*   **模块 2：深度分析子页面 (Analytics Pages)**
    *   **CC Type Analysis**: 分析不同信用卡品牌（Visa, Mastercard, Amex 等）在各商户下的通过率趋势。
    *   **PSP Analysis**: 提供高密度热力图和折线柱状图组合，深度挖掘 PSP 和卡种之间的通过率差异，为智能路由提供数据基础。
    *   **Retry Analysis**: 通过瀑布图（Waterfall）和桑基图/漏斗图（Sankey/Funnel），精准量化“重试策略”挽回的实际美元营收（Salvage Value）。

*   **模块 3：决策沙盒 (Routing Simulator)**
    *   提供交互式滑块，允许用户动态分配各 PSP 的预期月流量。系统会根据底层费率数据，实时推算“混合通过率（Blended Approval Rate）”、“预估总成本”以及对比历史基准的“净节省金额（Net Savings）”。

## 4. 技术架构与依赖
*   **Frontend**: Python, Streamlit (自定义 Navbar 替代默认侧边栏)
*   **Backend / Cron**: Python, `schedule`, `requests` (用于Team/Slack Webhook 报警)
*   **Data Layer**: 本地 CSV 存储 (`data/` 目录), Pandas 进行数据清洗与聚合。