import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
import os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser



model = ChatGroq(model="llama-3.3-70b-versatile")

parser = StrOutputParser()

prompt = PromptTemplate.from_template(
    "我邻居姓: {lastname}, 刚生了{gender}, 请起名, 仅告知我名字无需其它内容。"
)

chain = prompt | model | parser | model | parser | model 

res: str = chain.invoke({"lastname": "王", "gender": "女儿"})
print(res)
print(res.content)
print(type(res))