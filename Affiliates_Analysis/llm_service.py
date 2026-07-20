import os
from dotenv import load_dotenv
import google.generativeai as genai

# 加载 .env 文件中的环境变量
load_dotenv()

class LLMService:
    def __init__(self):
        """初始化大模型客户端，自动读取本地环境变量"""
        # 从 .env 文件中获取名为 GOOGLE_API_KEY 的值
        api_key = os.getenv("GOOGLE_API_KEY")
        
        if not api_key:
            raise ValueError("❌ GOOGLE_API_KEY is missing! Please check your .env file.")
        
        # 配置 API Key
        genai.configure(api_key=api_key)
        
        # 使用 Gemini 模型
        self.model = genai.GenerativeModel('gemini-flash-latest')

    def generate_insights(self, dashboard_context, db_manager, query_for_rag="affiliate payout trends, organic ftt, processing guidelines"):
        """
        核心 RAG 逻辑：结合实时 Dashboard 数据与历史知识库，生成评论。
        """
        # ==========================================
        # 1. 检索阶段 (Retrieval): 从知识库寻找相关历史信息
        # ==========================================
        historical_docs = db_manager.search_similar_context(query_for_rag, top_k=3)
        
        historical_context = "### Historical Context (From Knowledge Base)\n"
        if historical_docs:
            for i, doc in enumerate(historical_docs):
                historical_context += f"#### Reference Document {i+1}:\n{doc}\n\n"
        else:
            historical_context += "> No relevant historical documents found in the database for this query.\n"

        # ==========================================
        # 2. 增强阶段 (Augmentation): 拼接终极 Prompt
        # ==========================================
        final_prompt = f"""
{dashboard_context}

---
{historical_context}

---
**Final Instruction:**
Based on the "Current Dashboard Data" and the "Historical Context" provided above, please generate the professional business commentary as requested in the System Action Required section. Ensure your tone is analytical, objective, actionable, and formatted cleanly using Markdown. Do not hallucinate numbers that are not in the tables.
"""

        # ==========================================
        # 3. 生成阶段 (Generation): 调用大模型
        # ==========================================
        try:
            # 向大模型发送请求
            response = self.model.generate_content(final_prompt)
            return response.text
        except Exception as e:
            return f"❌ Error generating AI insights: {e}"