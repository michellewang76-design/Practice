# 🧠 Affiliate智能看板与 AI 助手 (Affiliate Dashboard) - 全流程开发思维导图

## 1. 🎯 需求分析与定义 (Discovery & Requirements)
* **目标用户锁定**
  * Affiliate经理 (Affiliate Managers)
  * 合作伙伴总监 (Partnership Directors)
  * 财务运营团队 (Financial Ops)
* **核心痛点挖掘**
  * 🧩 数据碎片化：每月 CSV 文件分散，难以跨期对比，高度依赖 Excel 手动透视。
  * 🧠 知识流失：历史活动、政策变更记录分散，数据波动时难以追溯原因。
  * ✍️ 报告负担：每月耗费数小时手动制表和撰写财务总结。
* **产品愿景**
  * 打造自动化、AI 辅助的运营中心，统一数据与知识，赋能数据驱动决策。

## 2. 🏗️ 技术选型与架构设计 (Architecture & Tech Stack)
* **前端与路由 (Frontend & UI)**
  * Streamlit (Python) -> 快速搭建交互式 Web 界面与状态管理
* **数据处理引擎 (Data Engine)**
  * Pandas -> 复杂数据合并、分组与聚合
  * Plotly -> 动态交互式可视化图表
* **大语言模型 (LLM Engine)**
  * Google Gemini (Flash/Pro) -> 自然语言对话与自动生成分析报告
* **RAG 向量数据库 (Vector DB)**
  * ChromaDB (本地持久化) + Sentence-Transformers -> 文档分块与向量检索

## 3. 🚀 敏捷开发与核心迭代 (Agile Development: V1 - V5)
* **V1: 最小可行性产品 (MVP) - 静态数据查看**
  * 构建基础 Streamlit 框架。
  * 实现单月 CSV 上传、基础 DataFrame 展示与简单图表。
* **V2: 数据持久化与主表合并**
  * 建立本地物理仓库 (`uploaded_monthly_data/`)。
  * 开发 `merge.py`：自动去重、递归读取、多月数据动态拼接。
  * 引入全局年份/月份过滤器与高级 Plotly 图表。
* **V3: 引入生成式 AI - 商业洞察自动化**
  * 集成 Gemini API (`llm_service.py`)。
  * 开发 `DashboardContextBuilder`，将图表数据序列化为 AI 提示词。
  * 实现“一键生成” Markdown 格式的专业财务分析报告。
* **V4: 知识库与 RAG 架构融合**
  * 建立 ChromaDB 本地向量数据库 (`knowledge_base.py`)。
  * 支持业务文档（.txt, .docx）上传与嵌入 (Embeddings)。
  * 将硬数据指标与历史活动/政策上下文交叉引用。
* **V5: 交互式 UI 与极致体验优化 (Final Polish)**
  * 开发独立且持久化的 AI 侧边栏 (`chat_sidebar.py`)，支持滚动条。
  * 引入动态 UI 切换开关（展开/收起侧边栏），优化屏幕画布空间。
  * 实现双模式 LLM 调度（大报告生成 vs. 碎片化即席查询）。

## 4. 🛡️ 测试、加固与交付 (Testing & Delivery)
* **异常拦截与鲁棒性**
  * 模型版本兼容 (404 错误)：统一环境依赖，切换稳定模型版本。
* **代码规范与安全管控**
  * 配置 `.gitignore`：严格拦截敏感数据文件夹、数据库缓存与 API Keys 上传云端。
* **环境封装**
  * 锁定核心依赖版本，输出 `requirements.txt`。
* **产品文档交付**
  * 撰写标准化的 `README.md` (包含环境配置、启动指引与文件结构)。
  * 输出最终 PRD (产品需求文档) 与 版本迭代复盘报告。