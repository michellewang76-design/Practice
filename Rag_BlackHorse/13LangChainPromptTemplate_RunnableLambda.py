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
from langchain_core.runnables import RunnableLambda


model = ChatGroq(model="llama-3.3-70b-versatile")

str_parser = StrOutputParser()

first_prompt = PromptTemplate.from_template(
    "我邻居姓: {lastname}, 刚生了{gender}, 请帮忙起名字, 仅告知我名字, 不要额外信息。 "
)

second_prompt = PromptTemplate.from_template(
    "姓名{name}, 请帮我解析含义。 "
)

# 函数的入参：AIMessage -> dict  ({"name": "xxx"})
my_func = RunnableLambda(lambda ai_msg: {"name": ai_msg.content})

# 构建链        （AIMessage("{name: 张若曦}")）
chain = first_prompt | model | my_func | second_prompt | model | str_parser

for chunk in chain.stream({"lastname": "陈", "gender": "女儿"}):
    print(chunk, end="", flush=True)