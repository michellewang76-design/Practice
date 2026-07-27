import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ==========================================
# 1. 页面基本设置
# ==========================================
st.set_page_config(page_title="Merchant Dashboard", page_icon="💳", layout="wide")

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
    # 假设数据文件名为 deposit.csv，放在同一目录下
    df = pd.read_csv('deposit.csv')
    
    # 将 Date 转换为 datetime 格式 (根据截图，格式类似 1/01/2021)
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
    
    # 也可以限制日历弹窗的可选范围，这里保持灵活，只改默认值
    date_range = st.date_input("Time Range", value=(default_start, default_end))

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
                # ==========================================

                max_date = agg_df['Date'].max() # 找出当前数据中最新的时间
                last_period_df = agg_df[agg_df['Date'] == max_date]
                
                if not last_period_df.empty:
                    # 获取这一期存在的卡类型，并生成对应数量的子列
                    current_card_types = last_period_df['CardType'].unique()

                    gauge_cols = st.columns(4)
                    
                    
                    for i, c_type in enumerate(current_card_types):
                        # 提取该卡种在最后一期的通过率 (将其转化为 0-100 的数值)
                        rate_val = last_period_df[last_period_df['CardType'] == c_type].iloc[0]['Approval Rate (%)'] * 100
                        
                        
                        # 创建仪表盘对象
                        gauge_fig = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=rate_val,
                            number={'suffix': "%", 'valueformat': ".1f"}, # 显示类似 43.0%
                            title={'text': c_type, 'font': {'size': 14}},
                            gauge={
                                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                                'bar': {'color': color_mapping.get(c_type, '#000000')}, # 指针颜色跟随卡种
                                'bgcolor': "white",
                                'borderwidth': 1,
                                'bordercolor': "gray",
                                'steps': [
                                    {'range': [0, 40], 'color': 'rgba(255, 99, 71, 0.3)'},    # 红色警戒区
                                    {'range': [40, 70], 'color': 'rgba(255, 235, 59, 0.3)'},  # 黄色过渡区
                                    {'range': [70, 100], 'color': 'rgba(76, 175, 80, 0.3)'}   # 绿色安全区
                                ],
                            }
                        ))
                        
                        # 调整仪表盘的间距和高度，使其小巧精致
                        gauge_fig.update_layout(
                            margin=dict(l=15, r=15, t=30, b=10),
                            height=160
                        )
                        
                        # 将仪表盘画在对应的子列中
                        gauge_cols[i].plotly_chart(gauge_fig, use_container_width=True)

            else:
                st.info(f"No data available for {merchant} in this period.")
else:
    st.warning("Please select at least one Merchant and a valid Date Range.")