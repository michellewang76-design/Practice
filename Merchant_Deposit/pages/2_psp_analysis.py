import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import os

# ==========================================
# 1. 页面基本设置
# ==========================================
st.set_page_config(page_title="PSP Analysis", page_icon="🔀", layout="wide")

# 🌟 2. 在页面最顶端渲染导航栏
from navbar import create_top_nav
create_top_nav()

st.title("🔀 PSP Smart Routing & Cost Analysis")
st.markdown("""
**Business Analysis Objectives:**
* Explore the approval rate differences of various PSPs for the same merchant and credit card type.
* Identify if certain PSPs have high transaction volumes, (but tend to reject large transactions, TBC).
""")
st.markdown("---")
st.info("💡 **Note:** The data displayed on this page is filtered based on the date range selected in the **cc type analysis** tab.")

# 注入 CSS：统一标签颜色
st.markdown("""
<style>
span[data-baseweb="tag"] { background-color: #808080 !important; }
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
    
    df['Approved_Count'] = df.apply(lambda x: x['Count'] if str(x['Status']).strip().lower() == 'approved' else 0, axis=1)
    return df

df = load_data()

# ==========================================
# 3. 侧边栏 Filter (专属交互)
# ==========================================
st.sidebar.header("Filter Options")

all_merchants = df['Group'].unique().tolist()
all_card_types = df['CardType'].unique().tolist()

# PSP 分析页面只需要商户和卡种作为过滤条件，不需要过滤 PSP 本身（因为要在主界面对比所有 PSP）
selected_merchants = st.sidebar.multiselect("Merchants", all_merchants, default=all_merchants[:2] if len(all_merchants)>=2 else all_merchants)
selected_card_types = st.sidebar.multiselect("Card Type", all_card_types, default=all_card_types)

# ==========================================
# 4. 数据过滤与图表渲染
# ==========================================
mask = (
    (df['Group'].isin(selected_merchants)) &
    (df['CardType'].isin(selected_card_types))
)

# 新增：从 session_state 获取日期范围并叠加到 mask 过滤条件中
if 'global_date_range' in st.session_state and len(st.session_state['global_date_range']) == 2:
    start_date, end_date = st.session_state['global_date_range']
    mask = mask & (df['Date'].dt.date >= start_date) & (df['Date'].dt.date <= end_date)

filtered_df = df.loc[mask].copy()

if not filtered_df.empty and len(selected_merchants) > 0 and len(selected_card_types) > 0:
    
    col1, col2 = st.columns(2)
    
    # ----------------------------------------
    # 左侧：热力图 (Heatmap)
    # ----------------------------------------
    with col1:
        st.markdown("#### 1. PSP vs CardType (Approval Rate)")
        
        # 准备热力图数据：按 PSP 和 卡组 聚合
        psp_heat_df = filtered_df.groupby(['PspName', 'CardType'])[['Count', 'Approved_Count']].sum().reset_index()
        psp_heat_df['Approval Rate'] = (psp_heat_df['Approved_Count'] / psp_heat_df['Count']).fillna(0)
        
        # 转换为矩阵供 Heatmap 使用
        pivot_df = psp_heat_df.pivot(index='CardType', columns='PspName', values='Approval Rate')
        
        fig_heat = px.imshow(
            pivot_df,
            text_auto='.1%', 
            aspect="auto",
            color_continuous_scale='Blues',
            labels=dict(x="PSP Name", y="Card Type", color="Approval Rate")
        )
        
        # 修改悬停时的提示格式 (z 代表数值，.0% 代表没有小数的百分比)
        fig_heat.update_traces(
            hovertemplate="PSP Name: %{x}<br>Card Type: %{y}<br>Approval Rate: %{z:.0%}<extra></extra>"
        )

        fig_heat.update_layout(
            margin=dict(l=0, r=0, t=30, b=0), 
            height=450,
            # 将图表右侧的颜色图例 (Colorbar) 格式化为整数百分比
            coloraxis_colorbar=dict(tickformat='.0%')
        )
        
        # 将 X 轴的标签倾斜角度设为 45 度，与右侧的柱状图保持一致
        fig_heat.update_xaxes(tickangle=45)
        
        st.plotly_chart(fig_heat, use_container_width=True)
        
    # ----------------------------------------
    # 右侧：双轴柱状图 (Dual-axis Bar Chart)
    # ----------------------------------------
    with col2:
        st.markdown("#### 2. Volume & Approval Performance")
        
        # 准备双轴图数据：仅按 PSP 聚合
        psp_dual_df = filtered_df.groupby('PspName')[['Count', 'Approved_Count', 'Amount']].sum().reset_index()
        psp_dual_df['Approval Rate'] = (psp_dual_df['Approved_Count'] / psp_dual_df['Count']).fillna(0)
        
        # 创建双轴图表
        fig_dual = make_subplots(specs=[[{"secondary_y": True}]])
        
        # 主轴：交易额柱状图 (浅灰色)
        fig_dual.add_trace(
            go.Bar(x=psp_dual_df['PspName'], y=psp_dual_df['Amount'], name="Total Amount ($)", marker_color='#E0E0E0'),
            secondary_y=False,
        )
        
        # 次轴：通过率折线图 (橙色高亮)
        fig_dual.add_trace(
            go.Scatter(x=psp_dual_df['PspName'], y=psp_dual_df['Approval Rate'], name="Approval Rate (%)", mode="lines+markers", line=dict(color='#FF9800', width=3)),
            secondary_y=True,
        )
        
        fig_dual.update_layout(
            margin=dict(l=0, r=0, t=30, b=0),
            height=450,
            legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1),
            hovermode="x unified" # 鼠标悬停时同时显示柱状图和折线图的数据
        )
        
        fig_dual.update_yaxes(title_text="Total Amount ($)", secondary_y=False)
        fig_dual.update_yaxes(title_text="Approval Rate", tickformat='.0%', secondary_y=True)
        
        st.plotly_chart(fig_dual, use_container_width=True)

else:
    st.warning("Please select at least one Merchant and Card Type from the sidebar.")