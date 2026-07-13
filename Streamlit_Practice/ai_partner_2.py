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
                base_url="https://api.groq.com/openai/v1",
                api_key=os.environ.get("GROQ_API_KEY")
            )

system_prompt = "你是一名非常专业的AI助理,你的名字叫哈哈,请你用专业简洁礼貌的语气回答用户的问题"

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


# 调用LLM
# 测试一下
    # print([
    #         {"role": "system", "content": system_prompt},
    #         *st.session_state.messages
    #     ])

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                # 解包列表里的元素，前面加一个*, 可以这么做是因为格式完全一致，key都是role、content
                *st.session_state.messages
            ],
            stream=True,
        )

        # 流式输出：在 chat_message 容器内用 empty 占位符逐字更新
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    response_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})

    except Exception as e:
        st.error(f"调用 LLM 失败: {e}")

