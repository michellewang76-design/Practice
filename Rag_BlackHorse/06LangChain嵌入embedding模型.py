import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
import os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_google_genai import GoogleGenerativeAIEmbeddings

embed = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

# 测试代码（跟之前的用法完全一样！）
query_result = embed.embed_query("我喜欢你")
print(f"查询语句转化成功！向量维度为: {len(query_result)}") # Gemini 默认输出 768 维的向量

doc_results = embed.embed_documents(['我喜欢你', '我稀罕你', '晚上吃啥'])
print(f"文档列表转化成功！共生成了 {len(doc_results)} 条向量数据。")

