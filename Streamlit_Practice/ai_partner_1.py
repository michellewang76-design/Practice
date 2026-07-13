import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(
    page_title="First AI Partner",
    page_icon="🦄",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        # 'Get Help': "https://aznconnect.com.au/",
        # 'Report a bug': "https://aznconnect.com.au/",
        # 'About': "# Cutest Babies Ever!"
    }
)

st.title("First AI Partner")

st.logo("../Resources/Florence.jpg")


client = OpenAI(
                base_url="https://generativelanguage.googleapis.com/v1beta/openai",
                api_key=os.environ.get("GOOGLE_API_KEY")
            )

system_prompt = "你是一名非常可爱的AI助理,你的名字叫小甜甜,请你使用温柔可爱的语气回答用户的问题"

# 初始化聊天消息
if 'messages' not in st.session_state:
    st.session_state.messages = []

# 展示聊天信息(从头到尾)
for message in st.session_state.messages:
    st.chat_message("role").write(message["content"])
    # if message["role"] == "user":
    #     st.chat_message("user").write(message["content"])
    # else:
    #     st.chat_message("assistant").write(message["content"])


prompt = st.chat_input("Please ask away")

if prompt:
    st.chat_message("user").write(prompt)
    print("-----------> 调用LLM Prompt:", prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        stream=False,
    )

    reply = response.choices[0].message.content
    print("LLM replied: ", reply)
    st.chat_message("assistant").write(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})

