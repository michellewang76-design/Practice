import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# ==========================================
# 1. 页面基本设置
# ==========================================
st.set_page_config(page_title="Merchant Dashboard", page_icon="💳", layout="wide")

# 🌟 2. 在页面最顶端渲染导航栏
from navbar import create_top_nav
create_top_nav()

# 注入 CSS 来把侧边栏多选框的标签颜色改为灰色
st.markdown("""
<style>
/* 1. 将所有选中的标签背景色改为灰色 */
span[data-baseweb="tag"] {
    background-color: #808080 !important;
}

/* 2. 精准定位：寻找内部包含 aria-label="PSPs" 的选择框容器，强制拉长 */
div[data-baseweb="select"]:has(input[aria-label="PSPs"]) {
    min-height: 250px !important;
    align-items: flex-start !important;
    align-content: flex-start !important;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. 数据加载与预处理 (使用缓存提升性能)
# ==========================================
@st.cache_data
def load_data():

    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    csv_path = os.path.join(parent_dir, 'data', 'deposit.csv')
    df = pd.read_csv(csv_path, encoding='utf-8-sig')
    
    # 将 Date 转换为 datetime 格式
    # 如果遇到日期格式不匹配报错，请调整 format 参数，例如 format='%d/%m/%Y'
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y', errors='coerce')
    
    # 定义需要剔除的无效值
    invalid_values = ['Unknown', '(blank)', 'nan', '']
    
    # 只要 Group, CardType 或 PspName 中包含这些无效值，直接将该行数据过滤掉
    df = df[~df['Group'].isin(invalid_values)]
    df = df[~df['CardType'].isin(invalid_values)]
    df = df[~df['PspName'].isin(invalid_values)]
    
    # 同时也彻底删除那些存在真实缺失值 (NaN) 的行
    df = df.dropna(subset=['Group', 'CardType', 'PspName'])
    
    # 计算 Approved Count (用于后续计算通过率)
    df['Approved_Count'] = df.apply(lambda x: x['Count'] if str(x['Status']).strip().lower() == 'approved' else 0, axis=1)
    
    return df

df = load_data()

# ==========================================
# 3. 侧边栏 (Sidebar) - 过滤条件
# ==========================================
st.sidebar.title("🛒 Merchant-PSP Dashboard")

# 获取各列的唯一值列表用于下拉框
all_merchants = df['Group'].unique().tolist()
all_card_types = df['CardType'].unique().tolist()
all_psps = df['PspName'].unique().tolist()

# 多选过滤器
selected_merchants = st.sidebar.multiselect("Merchants", all_merchants, default=all_merchants[:3] if len(all_merchants)>=3 else all_merchants)
selected_card_types = st.sidebar.multiselect("Card Type", all_card_types, default=all_card_types)
selected_psps = st.sidebar.multiselect("PSPs", all_psps, default=all_psps)

# ==========================================
# 4. 顶部 - 标题与时间/分组过滤
# ==========================================
st.title("💳 Merchants Insights")
st.subheader("Deposit Date 📅")

col1, col2 = st.columns(2)

with col1:
    # 设定默认的开始和结束日期
    default_start = datetime(2023, 1, 1).date()
    default_end = datetime(2024, 12, 31).date()
    
    # 1. 初始化 session_state
    if 'global_date_range' not in st.session_state:
        st.session_state['global_date_range'] = (default_start, default_end)
        
    # 2. 日期选择器绑定 session_state 中存储的值
    date_range = st.date_input("Time Range", value=st.session_state['global_date_range'])
    
    # 3. 只要用户修改了日期，就实时更新全局 session_state
    st.session_state['global_date_range'] = date_range

with col2:
    # 将 index 设为 1，默认选中列表里的第二个选项 'month'
    group_by_option = st.selectbox("Group By", options=['week', 'month', 'quarter', 'year'], index=1)
    
    # 将用户的选择映射为 pandas resample 的频率代码
    freq_mapping = {'week': 'W', 'month': 'ME', 'quarter': 'QE', 'year': 'YE'}
    freq = freq_mapping[group_by_option]

# ==========================================
# 5. 数据过滤与指标计算
# ==========================================
# 应用过滤条件
if len(date_range) == 2:
    start_date, end_date = date_range
    mask = (
        (df['Date'].dt.date >= start_date) & 
        (df['Date'].dt.date <= end_date) &
        (df['Group'].isin(selected_merchants)) &
        (df['CardType'].isin(selected_card_types)) &
        (df['PspName'].isin(selected_psps))
    )
    filtered_df = df.loc[mask].copy()
else:
    filtered_df = pd.DataFrame() # 如果日期没选全，返回空

st.markdown("### Merchants 🏢")

if not filtered_df.empty and len(selected_merchants) > 0:
    # 为了实现横排展示，动态创建列
    cols = st.columns(len(selected_merchants))
    
    for idx, merchant in enumerate(selected_merchants):
        with cols[idx]:
            st.markdown(f"#### {merchant}")
            
            # 过滤出当前商户的数据
            merchant_df = filtered_df[filtered_df['Group'] == merchant].copy()
            
            if not merchant_df.empty:
                # 按照选定的时间维度 (freq) 和 CardType 进行聚合计算
                # 统计每段时间内，每个卡组的总 Count 和 Approved_Count
                agg_df = merchant_df.groupby([pd.Grouper(key='Date', freq=freq), 'CardType'])[['Count', 'Approved_Count']].sum().reset_index()
                
                # 计算通过率 Approval Rate = Approved_Count / Total Count
                agg_df['Approval Rate (%)'] = (agg_df['Approved_Count'] / agg_df['Count']).fillna(0)
                
                # 画折线图
                color_mapping = {
                    'VISA': '#808080',       # 灰色
                    'MASTERCARD': '#000000', # 黑色
                    'JCB': '#FFC107',        # 黄色
                    'AMEX': '#FF9800',       # 橙色 (增加区分度，避免与 JCB 重复)
                    'Unknown': '#BDBDBD'     # 浅灰兜底
                }

                fig = px.line(
                    agg_df, 
                    x='Date', 
                    y='Approval Rate (%)', 
                    color='CardType',
                    title='Approval Timetrend',
                    markers=True,
                    color_discrete_map=color_mapping # 使用绝对映射取代之前的顺序分配
                )
                
                # 调整图表布局，将 Y 轴 (竖标) 改成显示百分比
                fig.update_layout(
                    xaxis_title="Date",
                    yaxis_title="Approval Rate",
                    yaxis_tickformat='.0%', # 竖轴显示为整数百分比 (例如 80%, 90%)
                    legend_title="CC Type",
                    legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.02),
                    margin=dict(l=0, r=0, t=40, b=0),
                    height=350
                )

                fig.update_traces(
                    hovertemplate='<b>Date</b>: %{x}<br><b>Approval Rate</b>: %{y:.2%}'
                )
                
                st.plotly_chart(fig, use_container_width=True)

                # ==========================================
                # 提取最后一个 Period 并绘制对应的仪表盘

                max_date = agg_df['Date'].max() # 找出当前数据中最新的时间
                last_period_df = agg_df[agg_df['Date'] == max_date]
                
                if not last_period_df.empty:
                    # 获取这一期存在的卡类型，并生成对应数量的子列
                    current_card_types = last_period_df['CardType'].unique()

                    gauge_cols = st.columns(2)
                    
                    for i, c_type in enumerate(current_card_types):
                        # 提取该卡种在最后一期的通过率
                        rate_val = last_period_df[last_period_df['CardType'] == c_type].iloc[0]['Approval Rate (%)'] * 100
                        
                        # 创建仪表盘对象
                        gauge_fig = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=rate_val,
                            number={'suffix': "%", 'valueformat': ".1f"},
                            title={'text': c_type, 'font': {'size': 14}},
                            gauge={
                                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                                'bar': {'color': color_mapping.get(c_type, '#000000')}, # 指针颜色跟随卡种
                                'bgcolor': "white",
                                'borderwidth': 1,
                                'bordercolor': "gray",
                                'steps': [
                                    {'range': [0, 40], 'color': 'rgba(255, 99, 71, 0.3)'},
                                    {'range': [40, 70], 'color': 'rgba(255, 235, 59, 0.3)'},
                                    {'range': [70, 100], 'color': 'rgba(76, 175, 80, 0.3)'}
                                ],
                            }
                        ))
                        
                        # 放宽左右 Margin 防止边缘被切，适当增加一点高度
                        gauge_fig.update_layout(
                            margin=dict(l=30, r=30, t=40, b=15),
                            height=180
                        )
                        
                        # 利用数学取余数 (i % 2) 实现换行效果
                        # 当 i 为 0 (左上), 1 (右上), 2 (左下), 3 (右下)
                        gauge_cols[i % 2].plotly_chart(gauge_fig, use_container_width=True)

            else:
                st.info(f"No data available for {merchant} in this period.")
else:
    st.warning("Please select at least one Merchant and a valid Date Range.")