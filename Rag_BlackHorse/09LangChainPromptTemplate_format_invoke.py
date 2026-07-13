import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
import os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate, ChatPromptTemplate


# model = ChatGroq(model="llama-3.3-70b-versatile")

template = PromptTemplate.from_template("我的邻居是: {lastname}. 最喜欢: {hobby}")

res = template.format(lastname="张大明", hobby="钓鱼")
print(res, type(res))

res2 = template.invoke({"lastname": "周杰伦", "hobby": "唱歌"})
print(res2, type(res2))