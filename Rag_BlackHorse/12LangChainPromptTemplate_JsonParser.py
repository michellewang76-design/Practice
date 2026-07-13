import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
import os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser



model = ChatGroq(model="llama-3.3-70b-versatile")

str_parser = StrOutputParser()
json_parser = JsonOutputParser()

# 第一个提示词模板
first_prompt = PromptTemplate.from_template(
    "我邻居姓: {lastname}, 刚生了{gender}, 请帮忙起名字, "
    "并封装为JSON格式返回给我。要求key是name, value就是你起的名字, 请严格遵守格式要求。 "
)

# 第二个提示词模板
second_prompt = PromptTemplate.from_template(
    "姓名: {name}, 请帮我解析含义。"
)

# 构建链        （AIMessage("{name: 张若曦}")）
chain = first_prompt | model | json_parser | second_prompt | model | str_parser

for chunk in chain.stream({"lastname": "陈", "gender": "女儿"}):
    print(chunk, end="", flush=True)