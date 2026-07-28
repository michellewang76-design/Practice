# 产品迭代与复盘 (Retro)

*从基础报表到全功能中央控制台：Payment Manager Dashboard 的五次核心迭代*

本文档记录了 Payment Manager Dashboard 的演进过程。在业务需求和管理痛点的双重驱动下，将一个纯静态的数据图表页面，一步步拆解、重构并升级为了一个具备权限控制、数据沙盒和后台报警功能的综合级 Web 应用。

## V1: 从大杂烩到模块化 (数据结构拆分)
*   **文件参考**: `app_1.py` (已废弃原型) -> 拆分为 `pages/` 下的 1, 2, 3 号分析脚本。
*   **业务痛点**: 最初所有的图表（通道分析、卡种分析、重试漏斗）都堆叠在一个极长的页面中，导致加载缓慢，且管理者找不到重点。
*   **交付功能**: 引入了 Streamlit 的多页面结构（Multipage App）。将底层流水数据分析细化为独立的维度：`1_cc_type_analysis.py` 专注卡组表现，`2_psp_analysis.py` 专注通道健康度，`3_retry_analysis.py` 专注挽回价值。
*   **复盘洞察**: 拆分页面极大提升了响应速度和代码可维护性，但也暴露出缺少一个“主入口”来统筹全局的问题。

## V2: 业务沙盒的引入 (What-If 模型)
*   **文件参考**: `pages/4_routing_simulator.py`
*   **业务痛点**: 数据分析页面只能看“过去发生了什么”，但管理层经常问：“如果我们把 30% 的拉美流量切给 DLocal，能省多少手续费？”
*   **交付功能**: 上线了“路由模拟器”。结合 Streamlit 的动态 Slider 组件，让业务人员可以拖拽分配流量，并实时联动计算器，直接展示 Estimated Total Cost 和 Net Savings。
*   **复盘洞察**: 这是产品从“BI 报表”走向“生产力工具”的关键转折点，极大地提升了业务部门对该工具的依赖度。

## V3: 打造中央控制台与现代 UI 重构
*   **文件参考**: `payment_manager.py` (Main Entry), `navbar.py`, `config.toml`
*   **业务痛点**: Streamlit 默认的左侧边栏看起来像一个粗糙的数据脚本，不符合企业级内部中台的产品调性。同时，缺少一个宏观视角的 Dashboard 主页。
*   **交付功能**: 
    1. 通过 `.streamlit/config.toml` 隐藏了默认侧边栏，引入了自定义的水平顶部导航栏（`navbar.py`），实现了现代 Web App 的视觉体验。
    2. 新建了 `payment_manager.py` 作为大盘主页，加入了 Gateways Pipeline 的甘特图展示。

## V4: 数据持久化与安全管理 (编辑权限升级)
*   **文件参考**: `payment_manager.py`, `data/` 文件夹规范化
*   **业务痛点**: PSP 的费率结构和动态风险（如某通道临时被冻结资金）以前都是写死在代码里或者存在单独的 Excel 中，业务人员无法自行更新，每次修改都要提 IT 需求。
*   **交付功能**: 
    1. 引入了 `st.data_editor` 组件，实现了 Risk 和 Cost 两个模块的交互式增删改查。
    2. 为了防止误操作，引入了全局管理员密码（`st.text_input(type="password")`）。**解决了一个技术难点**：通过结合 `st.session_state` 将密码输入框移动到页面下方，同时保证页面上方依赖该状态的组件不会因执行顺序而报错。
    3. 建立了标准的 `data/` 目录存放 CSV，并通过 `os.path` 绝对路径彻底解决了部署到云端后的相对路径报错（FileNotFoundError）问题。

## V5: 从被动查看走向主动预警 (前后端解耦)
*   **文件参考**: `anomaly_detector.py`, `risk_backend_cron.py`
*   **业务痛点**: Dashboard 必须被打开时才能看到数据。如果半夜出现支付通道故障，Manager 无法第一时间知晓。
*   **交付功能**: 架构上完成了初步的前后端分离。前端页面调用 `anomaly_detector.py` 进行异常数据渲染；后端部署了独立的 `risk_backend_cron.py` 守护进程任务（Daemon Script），配合 `schedule` 库实现每 10 分钟扫描一次数据库，触发阈值即通过 Webhook 向 Slack 发送 🚨 URGENT ALERT。
*   **下一步计划 (Next Steps)**: 将 `data/` 目录下的 CSV 完全迁移至 PostgreSQL 数据库，并使用 SQLAlchemy ORM 替代 Pandas 的直接读写，以支持更高的并发和真实的生产环境。