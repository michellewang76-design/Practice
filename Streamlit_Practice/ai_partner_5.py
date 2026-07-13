import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
from datetime import datetime
import json

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

system_prompt = """你是一名非常专业的AI助理,
                你的名字叫%s,
                你的性格是%s.
                """

def generate_session_name():
    return datetime.now().strftime("%Y%m%d_%H%M%S_%f")

# 初始化聊天消息
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'nickname' not in st.session_state:
    st.session_state.nickname = "哈哈"

if 'nature' not in st.session_state:
    st.session_state.nature = "专业简洁礼貌"

# 会话标识 - 设置一个会话的名字
if "current_session" not in st.session_state:
    st.session_state.current_session = generate_session_name()


# 保存会话信息函数
def save_session():
    if st.session_state.current_session:
        # 构建新的会话对象
        session_data = {
            "nickname": st.session_state.nickname,
            "nature": st.session_state.nature,
            "current_session": st.session_state.current_session,
            "messages": st.session_state.messages
        }

        # 如果 sessions 目录不存在，则创建
        if not os.path.exists("sessions"):
            os.mkdir("sessions")

        # 保存会话数据
        with open(f"sessions/{st.session_state.current_session}.json", "w", encoding="utf-8") as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)


# 加载所有的会话列表信息 - 对话title
def load_sessions():
    session_list = []
    # 加载sessions目录下的文件
    if os.path.exists("sessions"):
        file_list = os.listdir("sessions")
        for filename in file_list:
            if filename.endswith(".json"):
                session_list.append(filename[:-5])
    return session_list


# 加载指定的会话信息
def load_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            # 读取会话数据
            with open(f"sessions/{session_name}.json", "r", encoding="utf-8") as f:
                session_data = json.load(f)
                st.session_state.messages = session_data["messages"]
                st.session_state.nickname = session_data["nickname"]
                st.session_state.nature = session_data["nature"]
                st.session_state.current_session = session_name
    except Exception:
        st.error("loading dialogue failed!")


# 左侧侧边栏 - with: streamlit中的上下文管理器
# 把收入的信息保存在session_state当中
with st.sidebar:
    st.subheader("AI Control Panel")

    # 新建会话
    if st.button("Create New", width="stretch", icon="🤑"):
        #1. 保存当前会话
        save_session()

        #2. 创建新的会话
        if st.session_state.messages: # 如果有聊天信息，就是True
            st.session_state.messages = []
            st.session_state.current_session = generate_session_name()
            save_session()
            st.rerun() # 重新加载新页面

    # 会话历史
    st.text("Dialogue History")
    session_list = load_sessions()
    for session in session_list:
        col1,col2 = st.columns([4,1])
        
        with col1:

            if st.button(session, width="stretch", icon="😛", key=f"load_{session}", type="primary" if session == st.session_state.current_session else "secondary"):
                load_session(session)
                st.rerun()

        with col2:
            if st.button("", width="stretch", icon="❌️", key=f"delete_{session}"):
                pass

    # Agent信息等
    st.subheader("Agent信息")
    nickname = st.text_input("Nickname", placeholder="please enter nickname", value = st.session_state.nickname)
    if nickname:
        st.session_state.nickname = nickname
    nature = st.text_area("Personality", placeholder="please enter personality", value = st.session_state.nature)
    if nature:
        st.session_state.nature = nature


# 展示聊天信息(从头到尾)
st.text(f"Dialogue Name: {st.session_state.current_session}")
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
                {"role": "system", "content": system_prompt % (st.session_state.nickname, st.session_state.nature)},
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

# 对话完之后马上保存对话信息
    save_session()