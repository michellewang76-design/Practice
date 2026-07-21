# 产品迭代与复盘[cite: 8]
*从脚本到 AI 应用：Affiliate Analysis Dashboard的五次迭代*[cite: 8]

本文档记录了Affiliate Analysis dashboard的开发周期。[cite: 8]在Affiliate Manger和用户反馈实际操作中所遇瓶颈的严格驱动下，从一个简单的数据查看器，迭代进化为一个复杂的、AI 辅助的工作应用工具。[cite: 8]

---

## V1：静态数据查看器[cite: 8]
* **文件参考**：`aff_dashboard_1.py`[cite: 8]
* **用户需求**：“我不想总是仅仅为了查看每月基本的佣金统计数据和状态就得打开Excel。”[cite: 8]
* **交付功能**：一个基础的 Streamlit 界面，允许用户上传单个月份的 CSV 文件，并将其作为数据框 (DataFrame) 以及简单的静态图表进行查看。[cite: 8]
* **用户反馈**：“但是下个月我必须上传一个新文件，旧文件就没了。[cite: 8]我想跨月比较并查看趋势，而不想每次都重新上传所有内容。”[cite: 8]

---

## V2：数据持久化与主表合并[cite: 8]
* **文件参考**：`aff_dashboard_2.py` / `merge.py`[cite: 8]
* **用户需求**：自动化的历史记录追踪，消除重复的数据录入。[cite: 8]
* **交付功能**：实现了本地物理存储（`uploaded_monthly_data/`）。[cite: 8]添加了 `merge.py` 逻辑，以递归扫描、去重并将所有历史 CSV 文件拼接到一个动态 DataFrame 中。[cite: 8]添加了带有全局年份/月份过滤器的交互式 Plotly 图表。[cite: 8]
* **用户反馈**：“我老板要求我每个月写一段 affiliate performance analysis。[cite: 8]这个工具能帮我写吗？”[cite: 8]

---

## V3：自动化商业洞察（生成式 AI）[cite: 8]
* **文件参考**：`aff_dashboard_3.py` / `llm_service.py` / `context_builder.py`[cite: 8]
* **用户需求**：通过自动化的评论生成，减少手动撰写报告的工作量。[cite: 8]
* **交付功能**：集成了 Google Gemini。[cite: 8]构建了 `DashboardContextBuilder` 将可视化图表数据序列化为文本提示词。[cite: 8]添加了“生成 AI 洞察”按钮，严格基于当前看板的状态，输出专业的、Markdown 格式的财务总结。[cite: 8]
* **用户反馈**：“总结很准确，但 AI 缺乏背景信息。[cite: 8]它看到了 3 月份的数据激增，但它不知道这是因为我们举办了‘春季助力活动’。[cite: 8]它需要了解我们的历史。”[cite: 8]

---

## V4：知识库与 RAG 架构[cite: 8]
* **文件参考**：`aff_dashboard_4.py` / `knowledge_base.py`[cite: 8]
* **用户需求**：AI 必须具备关于过去营销活动、政策转变和佣金层级调整的机构记忆，以解释数据“为什么”会呈现出特定的形态。[cite: 8]
* **交付功能**：构建了本地化的检索增强生成 (RAG) 管道。[cite: 8]添加了 ChromaDB 向量存储。[cite: 8]允许经理上传内部备忘录（`.txt`、`.docx`）。[cite: 8]现在，AI 洞察报告会将硬数据与检索到的历史上下文进行交叉引用。[cite: 8]
* **用户反馈**：“有时我不想要一份完整的报告。[cite: 8]我只想快速问一个问题，比如‘Did we ever had any campaign in 2021 related to RevShare?’，并且不想离开当前dashboard页面。”[cite: 8]

---

## V5：交互式聊天与动态 UI（最终产品）[cite: 8]
* **文件参考**：`app.py` / `chat_sidebar.py`[cite: 8]
* **用户需求**：即席查询能力、更好的屏幕空间管理以及稳定性。[cite: 8]
* **交付功能**：[cite: 8]
  * 开发了一个独立的 `chat_sidebar.py`，具有固定高度、可滚动的容器和持久化的输入框。[cite: 8]
  * 添加了动态 UI 切换开关（“✨ Show/Hide AI Assistant”），用于展开/收起侧边栏，在不需要 AI 时将全屏宽度还给数据图表。[cite: 8]
  * 优化了 LLM 服务以支持双模式：完整报告模式 vs. 聊天查询模式。[cite: 8]
  * 配置了 `.gitignore`，以防止敏感数据/数据库泄漏到 GitHub。[cite: 8]
* **成果**：一个完整的、可用于生产环境的工作空间，平衡了宏观层面的数据可视化与微观层面的对话式 AI 问询。[cite: 8]