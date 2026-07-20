import pandas as pd

class DashboardContextBuilder:
    @staticmethod
    def generate_llm_context(report_data_dict, selected_year, selected_month):
        """
        接收前端已聚合好的核心 Dataframe，将其转化为 LLM 易读的 Markdown 上下文。
        """
        context_text = f"# 📝 Affiliate Payout Dashboard Data Context\n"
        context_text += f"**Report Period:** {selected_year}-{selected_month}\n\n"
        
        if not report_data_dict:
            return context_text + "No current dashboard data available."

        # 遍历传入的所有 Tab 图表数据
        for section_title, df in report_data_dict.items():
            context_text += f"## {section_title}\n"
            
            if df is None or df.empty:
                context_text += "> No data available for this section.\n\n"
            else:
                # 为了防止 LLM 被过长的小数位干扰，可以选择性地格式化数值列（如果前端未格式化）
                # 这里我们直接利用 pandas 的 to_markdown 渲染表格
                context_text += df.to_markdown(index=False) + "\n\n"

        # ==========================================
        # 核心指令：引导 LLM 如何阅读这些表格并输出专业点评
        # ==========================================
        context_text += """
---
**System Action Required:**
You are an expert financial data analyst and affiliate program manager. Please analyze the data tables provided above and synthesize them with any historical internal documents (from the Knowledge Base) to generate a professional business commentary.

Please structure your response covering the following aspects:
1. **Payout Summary & Status:** Summarize the current month's payout status (Paid, Pending, Rejected) and identify any bottlenecks in the bank processing queue.
2. **Trend Analysis (YoY):** Analyze the "Paid Affiliate Trends" table. Identify if the number of paid affiliates is growing or declining compared to historical performance.
3. **Organic Acquisition Health:** Evaluate the "Organic Affiliates FTT Trend" table. Analyze the relationship between All FTT and Organic FTT, and comment on whether the Organic PCT (%) is at a healthy level or needs attention.
4. **Actionable Insights & Drill-Down:** Based on anomalies, drops, or significant data points in the tables, suggest 1-2 specific areas where the business team should drill down for further investigation.
"""
        return context_text