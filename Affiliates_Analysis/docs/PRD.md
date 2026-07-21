# 产品需求文档 (PRD)[cite: 7]
*Affiliates Analysis Dashboard & AI Agent*[cite: 7]

## 产品愿景[cite: 7]
将Affiliate Manager每月依赖手动操作、繁重电子表格的报告工作流，转变为自动化、AI 辅助的工具看板。[cite: 7]通过统一分散的佣金数据和历史活动知识，使manager快速做出数据驱动的决策。[cite: 7]

---

## 1. 目标受众与问题陈述[cite: 7]
* **目标用户**：Affiliates Manager, COO, Finance。[cite: 7]
* **当前痛点**：[cite: 7]
  * **数据碎片化**：每月的佣金报告 (CSV) 极度分散。[cite: 7]跨季度追踪affiliates的表现需要手动合并 Excel（VLOOKUP、数据透视表）。[cite: 7]
  * **知识流失**：历史活动细节、affiliate payout structure调整和政策变更都存在于静态的 Word 文档或零散的邮件中。[cite: 7]当数据出现激增或骤降时，managers很难回想起到底是哪个具体的活动导致了这种变化。[cite: 7]
  * **报告负担过重**：生成Business Insights和总结每月的affiliates payout健康状况需要耗费数小时进行手动制表和撰写。[cite: 7]

---

## 2. 端到端用户工作流[cite: 7]

* **步骤 1：自动化数据摄取（“即传即忘”阶段）**[cite: 7]
  Users导航到“数据上传”侧边栏，将原始的monthly payout CSV 拖入系统。[cite: 7]系统会自动将其保存到本地持久化仓库，检查重复项，并无缝地与所有历史数据合并。[cite: 7]无需手动对齐 Excel。[cite: 7]

* **步骤 2：交互式可视化探索（“宏观视图”）**[cite: 7]
  看板即时更新。[cite: 7]users使用全局下拉菜单选择目标年份和月份。[cite: 7]他们通过预配置的 Plotly 图表查看交互式指标：已付与未付状态、银行支付分布以及流量比例。[cite: 7]

* **步骤 3：战略性 AI 问询（基于 RAG 聊天的“微观视图”）**[cite: 7]
  发现异常（例如，2021 年 8 月出现大幅激增）后，Users打开 AI 助手侧边栏。[cite: 7]他们提问：“What campaigns did we have in 2020? ”[cite: 7]AI 立即查询本地 ChromaDB 向量数据库（包含过去的历史文档），并在不离开当前页面的情况下结合上下文做出响应。[cite: 7]

* **步骤 4：自动化报告（“输出”阶段）**[cite: 7]
  在审查结束时，经理点击“生成 AI 洞察 (Generate AI Insights)”。[cite: 7]系统将当前看板的数据上下文和相关的知识库历史记录输入给 LLM（大语言模型），生成一份 Markdown 格式的、专业的财务评论，随时可以复制到高管汇报邮件中。[cite: 7]

---

## 3. 核心功能规格[cite: 7]

| 功能模块 | 描述 | 优先级 |[cite: 7]
| :--- | :--- | :--- |[cite: 7]
| **智能数据仓库** | 自动化 CSV 上传、持久化存储 (uploaded_monthly_data/)、去重，以及基于 pandas 的跨时间范围自动合并。 | P0（关键） |[cite: 7]
| **动态 UI 与过滤** | 全局年份/月份状态管理。自动默认选择最新可用月份。可展开/收起的页面布局。 | P0（关键） |[cite: 7]
| **RAG 知识库** | 支持上传 .txt/.docx 文件。文档分块、嵌入向量生成以及 ChromaDB 向量索引。 | P1（高） |[cite: 7]
| **上下文感知 AI 洞察** | ContextBuilder 将看板图表序列化为文本。Gemini LLM 将此与 RAG 数据综合，撰写高管摘要。 | P1（高） |[cite: 7]
| **交互式聊天侧边栏** | 固定高度、可滚动的聊天界面。提供展开/收起切换开关。在 st.session_state 中保留聊天记录。 | P2（中） |[cite: 7]

---

## 4. 技术架构要求[cite: 7]
* **前端/路由**：使用 Streamlit (Python) 进行快速 UI 开发和交互式状态管理。[cite: 7]
* **数据处理**：使用 Pandas 进行繁重的数据处理、合并、分组和聚合。[cite: 7]使用 Plotly 制作响应式图表。[cite: 7]
* **AI 模型引擎**：使用 Google Generative AI (Gemini Flash/Pro) 进行 RAG 问答和综合报告生成。[cite: 7]
* **向量数据库**：使用 ChromaDB（本地持久化）存储文档嵌入向量（基于 sentence-transformers）。[cite: 7]