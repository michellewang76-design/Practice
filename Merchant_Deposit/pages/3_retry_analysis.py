import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import os

# ==========================================
# 1. 页面基本设置 & CSS
# ==========================================
st.set_page_config(page_title="Retry Analysis", page_icon="🔄", layout="wide")

# 🌟 2. 在页面最顶端渲染导航栏
from navbar import create_top_nav
create_top_nav()

st.title("🔄 Retry & Salvage Value Analysis")
st.markdown("""
**Business Analysis Objectives:**
* Evaluate the effectiveness of the transaction retry strategy.
* Quantify the actual revenue salvaged through retries across different PSPs.
""")
st.markdown("---")

# 引入全局日期提示
st.info("💡 **Note:** The data displayed on this page is filtered based on the date range selected in the **cc type analysis** tab.")

# 注入 CSS：统一侧边栏标签颜色
st.markdown("""
<style>
/* 1. 将所有选中的标签背景色改为灰色 */
span[data-baseweb="tag"] { background-color: #808080 !important; }

/* 2. 精准定位：寻找内部包含 aria-label="PSPs" 的选择框容器，强制拉长 */
div[data-baseweb="select"]:has(input[aria-label="PSPs"]) {
    min-height: 250px !important;
    align-items: flex-start !important;
    align-content: flex-start !important;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 数据加载 (共享缓存)
# ==========================================
@st.cache_data
def load_data():
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    csv_path = os.path.join(parent_dir, 'data', 'deposit.csv')
    df = pd.read_csv(csv_path, encoding='utf-8-sig')

    df.columns = df.columns.str.strip()
    
    string_columns = ['PspName', 'CardType', 'Status', 'Group']
    for col in string_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
            
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y', errors='coerce')
    
    invalid_values = ['Unknown', '(blank)', 'nan', '']
    df = df[~df['Group'].isin(invalid_values)]
    df = df[~df['CardType'].isin(invalid_values)]
    df = df[~df['PspName'].isin(invalid_values)]
    df = df.dropna(subset=['Group', 'CardType', 'PspName'])
    
    return df

df = load_data()

# ==========================================
# 3. 侧边栏 Filter
# ==========================================
st.sidebar.header("Filter Options")

all_merchants = df['Group'].unique().tolist()
all_card_types = df['CardType'].unique().tolist()
all_psps = df['PspName'].unique().tolist() # 🌟 新增：获取所有 PSP 列表

selected_merchants = st.sidebar.multiselect("Merchants", all_merchants, default=all_merchants[:2] if len(all_merchants)>=2 else all_merchants)
selected_card_types = st.sidebar.multiselect("Card Type", all_card_types, default=all_card_types)
selected_psps = st.sidebar.multiselect("PSPs", all_psps, default=all_psps) # 🌟 新增：创建 PSP 的多选下拉框

# ==========================================
# 4. 数据过滤 (接收主页面的日期状态)
# ==========================================
mask = (
    (df['Group'].isin(selected_merchants)) &
    (df['CardType'].isin(selected_card_types)) &
    (df['PspName'].isin(selected_psps)) # 把用户选中的 PSP 加入到过滤条件中
)

# 应用从 cc_type_analysis 传过来的全局日期
if 'global_date_range' in st.session_state and len(st.session_state['global_date_range']) == 2:
    start_date, end_date = st.session_state['global_date_range']
    mask = mask & (df['Date'].dt.date >= start_date) & (df['Date'].dt.date <= end_date)

filtered_df = df.loc[mask].copy()

# ==========================================
# 5. 可视化图表渲染
# ==========================================
# 确保图表渲染前，也要判断 PSP 是否被选中
if not filtered_df.empty and len(selected_merchants) > 0 and len(selected_card_types) > 0 and len(selected_psps) > 0:
    
    col1, col2 = st.columns(2)
    
    # ----------------------------------------
    # 左侧：瀑布图 (Waterfall Chart) - 整体挽回收益
    # ----------------------------------------
    with col1:
        st.markdown("#### 1. Revenue Salvaged")
        
        # 指标计算
        total_request = filtered_df['Amount'].sum()
        # 拒绝金额：Status 不是 Approved 的金额
        initial_declined = filtered_df[filtered_df['Status'].str.lower() != 'approved']['Amount'].sum()
        # 挽回金额：Status 为 Approved 的行中，由 Retry 带来的金额
        salvaged_amount = filtered_df[filtered_df['Status'].str.lower() == 'approved']['Retried_Amount'].sum()
        
        # 绘制瀑布图
        fig_waterfall = go.Figure(go.Waterfall(
            name="Revenue",
            orientation="v",
            measure=["relative", "relative", "relative", "total"],
            x=["Total Requested", "Declined Amount", "Salvaged Amount", "Net Approved"],
            textposition="outside",
            text=[f"${total_request:,.0f}", f"-${initial_declined:,.0f}", f"+${salvaged_amount:,.0f}", ""],
            y=[total_request, -initial_declined, salvaged_amount, 0],
            connector={"line": {"color": "rgb(63, 63, 63)", "width": 1}},
            decreasing={"marker": {"color": "#000000"}}, # 黑色代表流失
            increasing={"marker": {"color": "#FFC107"}}, # 黄色代表挽回
            totals={"marker": {"color": "#808080"}}      # 灰色代表总计
        ))
        
        fig_waterfall.update_layout(
            margin=dict(l=20, r=20, t=40, b=20),
            height=450,
            waterfallgap=0.3
        )
        st.plotly_chart(fig_waterfall, use_container_width=True)

    # ----------------------------------------
    # 右侧：转化漏斗图 (Funnel Chart) - PSP 横向对比
    # ----------------------------------------
    with col2:
        st.markdown("#### 2. Retry Conversion by PSP")
        
        fig_funnel = go.Figure()
        
        # 按 PSP 分组，动态生成漏斗对比
        psp_groups = filtered_df.groupby('PspName')

        for psp, group in psp_groups:
            # 计算对应的三个层级数据
            count_total = group['Count'].sum()
            count_approved = group[group['Status'].str.lower() == 'approved']['Count'].sum()
            # 根据你的要求，这里把 Salvaged (成功挽回的) 数据提取出来，作为漏斗的最后一层
            count_salvaged = group[group['Status'].str.lower() == 'approved']['Count_Retried'].sum()
            
            # 只有当该 PSP 有数据时才画上去
            if count_total > 0:
                fig_funnel.add_trace(go.Funnel(
                    name=psp,
                    # Y 轴现在只有三层，并将最后一层命名为 Retried Count
                    y=["Total Count", "Approved Count", "Retried Count"],
                    # X 轴对应传入上面计算好的三个变量
                    x=[count_total, count_approved, count_salvaged],
                    textinfo="value+percent previous" 
                ))
        
        
        fig_funnel.update_layout(
            margin=dict(l=20, r=120, t=40, b=20), # 右侧留出空间给图例
            height=450,
            legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.02)
        )
        st.plotly_chart(fig_funnel, use_container_width=True)

else:
    st.warning("Please select at least one Merchant and Card Type from the sidebar.")
