import streamlit as st

def create_top_nav():
    # 注入 CSS 来放大导航栏的图标和文字
    st.markdown("""
    <style>
    /* 强力覆盖 st.page_link 的所有内部元素 (包含链接本身、段落文本和图标) */
    [data-testid="stPageLink-NavLink"],
    [data-testid="stPageLink-NavLink"] a,
    [data-testid="stPageLink-NavLink"] p,
    [data-testid="stPageLink-NavLink"] span,
    [data-testid="stPageLink"] p,
    [data-testid="stPageLink"] span {
        font-size: 20px !important; 
        font-weight: 600 !important; /* 顺便稍微加粗一点，作为导航栏更醒目 */
    }
    </style>
    """, unsafe_allow_html=True)

    # 使用 columns 将页面平分为 5 份，实现水平排列
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.page_link("payment_manager.py", label="Payment Manager", icon="💼")
    with col2:
        st.page_link("pages/1_cc_type_analysis.py", label="CC Type Analysis", icon="💳")
    with col3:
        st.page_link("pages/2_psp_analysis.py", label="PSP Analysis", icon="📊")
    with col4:
        st.page_link("pages/3_retry_analysis.py", label="Retry Analysis", icon="🔄")
    with col5:
        st.page_link("pages/4_routing_simulator.py", label="Routing Simulator", icon="🔀")
        
    # 添加一条水平分割线，区分导航栏和正文内容
    st.markdown("---")