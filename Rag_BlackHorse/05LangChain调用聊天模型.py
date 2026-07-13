import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
import os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

chat = ChatGroq(model="llama-3.3-70b-versatile")

# 准备消息 list (这一部分完全不需要改)
messages = [
    SystemMessage(content="你是一名来自边塞的诗人"),
    HumanMessage(content="给我写一首唐诗"),
    AIMessage(content="锄禾日当午，汗滴禾下土，谁知盘中餐，粒粒皆辛苦。"),
    HumanMessage(content="按照你上一首的格式，再来一首")
]

# 流式输出 
for chunk in chat.stream(input=messages):
    print(chunk.content, end="", flush=True)