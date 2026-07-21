import streamlit as st
from llm_service import LLMService

def render_rag_chat(db_manager):
    """
    渲染右侧的 AI RAG 查询助手 (带固定高度和滚动条)
    """
    # 1. 初始化聊天历史
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # ================= 核心修改区 =================
    # 创建一个固定高度的容器，它会自动生成内部滚动条 (Scroll bar)
    # 这里的 height=650 像素可以保证它不会超出左侧 Data Insights 的高度
    # 你可以根据实际屏幕视觉效果，随时修改这个数字 (如改成 600 或 700)
    chat_container = st.container(height=650)
    
    # 2. 在固定容器【内部】展示所有历史消息
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    # ===============================================

    # 3. 聊天输入框放在容器的【外部】正下方，这样它就永远固定在底部了
    if prompt := st.chat_input("Example: What campaigns did we have in 2020?"):
        
        # 将用户的新问题立刻写进固定容器【内部】
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # 4. 将 AI 的思考过程和回答也写进固定容器【内部】
        with chat_container:
            with st.chat_message("assistant"):
                with st.spinner("Searching..."):
                    try:
                        # 检索知识库
                        context_list = db_manager.search_similar_context(prompt, top_k=3) 
                        context_text = "\n".join(context_list)
                        
                        # 调用 LLM 生成回答
                        llm = LLMService()
                        response = llm.generate_rag_response(prompt, context_text)
                        
                        st.markdown(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                    except Exception as e:
                        st.error(f"Error: {e}")