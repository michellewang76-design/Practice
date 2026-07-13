import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
import os
from langchain_groq import ChatGroq

model = ChatGroq(model="llama-3.3-70b-versatile")

# 调用 stream 向模型提问，实现打字机流式输出
res = model.stream("你是谁呀能做什么？")

for chunk in res:
    # 注意：ChatGroq 推荐返回的是消息对象，需要加上 .content 来提取文字
    print(chunk.content, end="", flush=True)