import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import calendar

# ==================== 1. 页面基本配置 ====================
st.set_page_config(page_title="Affiliate Payout Dashboard", page_icon="📊", layout="wide")

# ==================== 2. 数据处理与缓存函数 ====================
@st.cache_data
def process_and_merge_files(uploaded_files):
    df_list = []
    for file in uploaded_files:
        file.seek(0)
        df = pd.read_csv(file, encoding='utf-8-sig')
        df_list.append(df)
    
    merged_df = pd.concat(df_list, ignore_index=True)
    return merged_df

# ==================== 3. 左侧边栏 (Sidebar) ====================
with st.sidebar:
    st.header("📂 Data Upload")
    st.markdown("Please upload **multiple monthly `.csv` data files** at once. The system will merge them automatically.")
    
    # 将上传组件放入侧边栏
    uploaded_files = st.file_uploader("Upload Monthly Data Files (CSV)", type=['csv'], accept_multiple_files=True)
    
    # 给用户一个手动收起侧边栏的提示
    if uploaded_files:
        st.success(f"✅ Successfully merged **{len(uploaded_files)}** files.")
        st.info("💡 Tip: You can close this sidebar to view the dashboard in full screen.")

# ==================== 4. 主页面头部 ====================
st.markdown("<h1 style='text-align: center;'>📊 Affiliate Payout Dashboard</h1>", unsafe_allow_html=True)

# ==================== 5. 仪表盘主体 ====================
# 只有当用户上传了文件后，才在主页面展示 Dashboard
if uploaded_files:
    try:
        with st.spinner(f"Processing and merging {len(uploaded_files)} files..."):
            df = process_and_merge_files(uploaded_files)
        
        # 将下载按钮也放在侧边栏底部，保持主页面整洁
        with st.sidebar.expander("📥 Download Merged Raw Data (Optional)"):
            csv_data = df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="Click here to download",
                data=csv_data,
                file_name="Merged_Affiliate_Data.csv",
                mime="text/csv"
            )

        st.markdown("<h2 style='text-align: center;'>📅 Select Month-Year 📅</h2>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            years = sorted(df['Year'].dropna().unique().tolist())
            # 💡 将默认 index 设为列表最后一位（最大年份）
            default_year_idx = len(years) - 1 
            selected_year = st.selectbox("📌 Choose a Year", years, index=default_year_idx)

        with col2:
            months = sorted(df[df['Year'] == selected_year]['Month'].dropna().unique().tolist())
            # 💡 将默认 index 设为列表最后一位（当前选中年份的最大月份）
            default_month_idx = len(months) - 1
            selected_month = st.selectbox("🎯 Choose a Month", months, index=default_month_idx)

        # ---------------- 替换原来的 st.success 和 st.info ----------------
        
        # 1. 高级金黄色：用于显示选中结果 (透明度 15%, 左侧带有实色边框修饰)
        
        month_name = calendar.month_name[int(selected_month)] # 将数字月份转换为英文

        selected_html = f"""
        <div style="background-color: rgba(255, 192, 0, 0.8); padding: 12px 20px; border-radius: 6px; border-left: 4px solid #FFC000; margin-bottom: 20px;">
            <span style="font-weight: 500; color: #333;">✅ You selected: <b>{selected_year} {month_name}</b></span>
        </div>
        """

        st.markdown(selected_html, unsafe_allow_html=True)

        # 2. 高级商务灰：用于显示 Notice (透明度 10%, 左侧带有深灰色实色边框修饰)
        notice_html = """
        <div style="background-color: rgba(128, 128, 128, 0.1); padding: 15px 20px; border-radius: 6px; border-left: 4px solid #808080; margin-bottom: 25px;">
            <div style="margin-bottom: 8px; font-weight: bold; color: #333;">📢 Notice</div>
            <ul style="margin: 0; padding-left: 20px; color: #555; font-size: 0.95em; line-height: 1.6;">
                <li>The data displayed represents the figures available <b>at the time it is run</b>.</li>
                <li>The data shown reflects <b>Affiliate commissions earned during the prior month</b>.</li>
                <li>Discrepancies between the Original Unpaid List Total and Actual Paid Total will occur due to reviews or payment transfer issues.</li>
                <li><b>Unpaid_No_Bank + Unpaid_BounceBack</b> changes back to <b>Unpaid</b> when affiliate updates their bank account.</li>
            </ul>
        </div>
        """
        st.markdown(notice_html, unsafe_allow_html=True)
        
        # -------------------------------------------------------------------

        filtered_df = df[(df['Year'] == selected_year) & (df['Month'] == selected_month)]

        # ==================== 注入自定义 CSS 美化 Tabs ====================
        st.markdown("""
        <style>
            /* 给 Tab 按钮之间增加间距 */
            .stTabs [data-baseweb="tab-list"] {
                gap: 6px;
            }
            /* 给每个 Tab 增加卡片式的背景和边框 */
            .stTabs [data-baseweb="tab"] {
                background-color: #F8F9FA;
                border: 1px solid #E5E7EB;
                border-bottom: none;
                border-radius: 6px 6px 0px 0px;
                padding: 10px 16px;
            }
            /* 鼠标悬停时的效果 */
            .stTabs [data-baseweb="tab"]:hover {
                background-color: #F3F4F6;
            }
            /* 当前选中的 Tab 背景变白，显得更突出 */
            .stTabs [aria-selected="true"] {
                background-color: #FFFFFF;
            }
        </style>
        """, unsafe_allow_html=True)

        # ==================== 构建 6 个 Tabs (精简命名 + 图标) ====================
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📋 Payout Summary", 
            "🧩 Status Breakdown", 
            "🏦 Processed by Bank", 
            "📊 Charts & Visuals",
            "📈 Trend Analysis",
            "🌱 Organic Affiliates"
        ])


        # -------------------- Tab 1: Summary --------------------
        with tab1:
            if not filtered_df.empty:
                summary_df = filtered_df.groupby('Status').agg(
                    Total_Affiliate_Count=('Affiliate_ID', 'nunique'),
                    Total_Payout_Amount=('Approved_Fee', 'sum')
                ).reset_index()
                
                summary_df.rename(columns={
                    'Status': 'Payout Status',
                    'Total_Affiliate_Count': 'Total Affiliate Count',
                    'Total_Payout_Amount': 'Total Payout Amount ¥'
                }, inplace=True)
                
                summary_df['Total Payout Amount ¥'] = summary_df['Total Payout Amount ¥'].apply(lambda x: f"{x:,.0f}")
                st.dataframe(summary_df, use_container_width=True, hide_index=True)
            else:
                st.warning("No data available for the selected month/year.")

        # -------------------- Tab 2: Breakdown --------------------
        with tab2:
            if not filtered_df.empty:
                col_left, col_mid, col_right = st.columns([1, 1, 2])
                statuses = sorted(filtered_df['Status'].dropna().unique().tolist())
                
                with col_left:
                    selected_status = st.radio("Select Payout Status", statuses)
                    
                status_df = filtered_df[filtered_df['Status'] == selected_status]
                
                with col_mid:
                    st.markdown(f"**Total Affiliate Count:** {status_df['Affiliate_ID'].nunique()}")
                    total_amt = status_df['Approved_Fee'].sum()
                    st.markdown(f"**Total Payout Amount:** ¥ {total_amt:,.0f}")
                    
                with col_right:
                    st.markdown(f"**Details for {selected_status} status:**")
                    display_cols = ['Affiliate_ID', 'Status', 'Approved_Fee', 'Bank']
                    st.dataframe(status_df[display_cols], use_container_width=True, hide_index=True)
            else:
                st.warning("No data available.")

        # -------------------- Tab 3: Processed --------------------
        with tab3:
            if not filtered_df.empty and 'Bank' in filtered_df.columns:
                valid_bank_df = filtered_df[filtered_df['Bank'].notna()]
                bank_df = valid_bank_df.groupby('Bank').agg(
                    Total_Affiliates=('Affiliate_ID', 'nunique'),
                    Total_Payment=('Approved_Fee', 'sum'),
                    Bank_Accounts_Count=('Affiliate_ID', 'count')
                ).reset_index()
                
                bank_df.rename(columns={
                    'Bank': 'Bank Name',
                    'Total_Affiliates': 'Total # of Affiliates to Pay',
                    'Total_Payment': 'Total Payment ¥',
                    'Bank_Accounts_Count': '# of Bank Accounts to Pay'
                }, inplace=True)
                
                bank_df['Total Payment ¥'] = bank_df['Total Payment ¥'].apply(lambda x: f"{x:,.0f}")
                st.dataframe(bank_df, use_container_width=True, hide_index=True)
            else:
                st.warning("No valid Bank data available.")

    
        # -------------------- Tab 4: Charts --------------------
        with tab4:
            st.markdown("### 📊 Data Visualizations")
            
            if not filtered_df.empty:
                def create_custom_pie(df_subset, names_col, values_col):
                    agg_df = df_subset.groupby(names_col)[values_col].sum().reset_index()
                    total = agg_df[values_col].sum()
                    if total == 0:
                        return None
                        
                    agg_df['pct'] = agg_df[values_col] / total
                    agg_df.loc[agg_df['pct'] < 0.02, names_col] = 'Other (<2%)'
                    
                    final_df = agg_df.groupby(names_col)[values_col].sum().reset_index()
                    final_df = final_df.sort_values(by=values_col, ascending=False).reset_index(drop=True)
                    
                    n_slices = len(final_df)
                    colors = []
                    if n_slices == 1:
                        colors = ['#FFC000']
                    elif n_slices == 2:
                        colors = ['#FFC000', '#000000']
                    else:
                        colors.append('#FFC000')
                        gray_shades = ['#BFBFBF', '#A6A6A6', '#8C8C8C', '#737373', '#595959', '#404040']
                        for i in range(1, n_slices - 1):
                            colors.append(gray_shades[(i - 1) % len(gray_shades)])
                        colors.append('#000000')
                    
                    # 💡 将 px.pie 改为 px.pie 并添加 hole 参数，使其变成更现代的甜甜圈图
                    # hole=0.3 意味着中心空出一个圆，这增加了图表的层次感和立体感
                    fig = px.pie(
                        final_df, 
                        values=values_col, 
                        names=names_col, 
                        color_discrete_sequence=colors,
                        hole=0.3 
                    )
                    
                    # 💡 增加扇区间距 (pull)，让每个块之间有缝隙，产生剥离效果，更具立体感
                    fig.update_traces(
                        textinfo='percent+label',
                        texttemplate='%{label}<br>%{percent:.0%}', 
                        hovertemplate='<b>%{label}</b><br>Value: %{value:,.0f}<br>Percent: %{percent:.0%}',
                        marker=dict(line=dict(color='#FFFFFF', width=2)), # 加粗边框让块与块之间对比更清晰
                        pull=[0.02] * len(final_df) # 这一行是关键：将所有扇区向外拉开 2% 的间距
                    )
                    
                    fig.update_layout(showlegend=False)
                    return fig
                
                # ================= 第一排图表 (两个) =================
                row1_col1, row1_col2 = st.columns(2)
                
                with row1_col1:
                    st.markdown("**1. Payout by Status**")
                    fig1 = create_custom_pie(filtered_df, 'Status', 'Approved_Fee')
                    if fig1:
                        st.plotly_chart(fig1, use_container_width=True)
                    
                with row1_col2:
                    st.markdown("**2. Affiliates by Status**")
                    count_df = filtered_df.groupby('Status')['Affiliate_ID'].nunique().reset_index()
                    count_df.rename(columns={'Affiliate_ID': 'Count'}, inplace=True)
                    fig2 = create_custom_pie(count_df, 'Status', 'Count')
                    if fig2:
                        st.plotly_chart(fig2, use_container_width=True)
                
                # 为了让上下两排图表不要贴得太紧，加入一点视觉留白
                st.markdown("<br>", unsafe_allow_html=True)
                
                # ================= 第二排图表 (两个) =================
                row2_col1, row2_col2 = st.columns(2)
                
                with row2_col1:
                    st.markdown("**3. Payment by Bank**")
                    if 'Bank' in filtered_df.columns:
                        valid_bank_df = filtered_df[filtered_df['Bank'].notna()]
                        if not valid_bank_df.empty:
                            fig3 = create_custom_pie(valid_bank_df, 'Bank', 'Approved_Fee')
                            if fig3:
                                st.plotly_chart(fig3, use_container_width=True)
                        else:
                            st.info("No valid Bank data.")
                    else:
                        st.warning("Bank data unavailable.")
                        
                with row2_col2:
                    st.markdown("**4. Affiliates by Criteria**")
                    if 'Criteria' in filtered_df.columns:
                        # 统计每个 Criteria 类别下的去重代理人数
                        criteria_df = filtered_df.groupby('Criteria')['Affiliate_ID'].nunique().reset_index()
                        criteria_df.rename(columns={'Affiliate_ID': 'Count'}, inplace=True)
                        fig4 = create_custom_pie(criteria_df, 'Criteria', 'Count')
                        if fig4:
                            st.plotly_chart(fig4, use_container_width=True)
                    else:
                        st.warning("Criteria data unavailable.")
                        
            else:
                st.warning("No data available to generate charts for the selected month/year.")

        # -------------------- Tab 5: Trend Analysis --------------------
        with tab5:
            st.markdown("### 📈 Paid Affiliate Trends")
            
            # 1. 时间过滤逻辑：只取 "最早的月" 到 "当前选中的月" 的数据
            # 为数据创建一个用来排序的整数型期间，例如 2024年3月 变成 202403
            df['Period'] = df['Year'] * 100 + df['Month']
            selected_period = int(selected_year) * 100 + int(selected_month)
            
            # 过滤出符合时间段且状态为 'Paid' 的数据
            trend_df = df[(df['Period'] <= selected_period) & (df['Status'] == 'Paid')]
            
            if not trend_df.empty:
                # 2. 按年月分组，统计每月实际获得 Paid 的去重代理人数
                monthly_paid = trend_df.groupby(['Year', 'Month']).agg(
                    Paid_Affiliates=('Affiliate_ID', 'nunique')
                ).reset_index()
                
                # 将年份转为字符串，这样 Plotly 会把它当作不同的分类线条（而不是一条连续的数值线）
                monthly_paid['Year_str'] = monthly_paid['Year'].astype(str)
                
                # ================= Chart 1: 按年叠加折线图 =================
                fig1 = px.line(
                    monthly_paid, 
                    x='Month', 
                    y='Paid_Affiliates', 
                    color='Year_str',
                    markers=True, # 显示数据圆点
                    title='Paid Affiliates (Year-over-Year)',
                    labels={'Month': 'MONTH', 'Paid_Affiliates': 'Number of Paid Affiliates', 'Year_str': 'Year'}
                )
                
                # 强制 X 轴显示为 1-12 的整数
                fig1.update_xaxes(tickmode='linear', tick0=1, dtick=1)
                # 调整图例位置，使其像截图一样排在图表上方
                fig1.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0))
                
                # ================= Chart 2: 连续时间线 + 均线 =================
                # 构建连续时间的 X 轴标签格式 (如 2020-01, 2020-02)，使用 zfill 补零确保排序正确
                monthly_paid['Date_Label'] = monthly_paid['Year_str'] + '-' + monthly_paid['Month'].astype(str).str.zfill(2)
                
                # 计算每一年的月平均值
                annual_avg = monthly_paid.groupby('Year')['Paid_Affiliates'].mean().reset_index()
                annual_avg.rename(columns={'Paid_Affiliates': 'Annual Average'}, inplace=True)
                
                # 将年平均值拼接到原始的月度数据表中
                timeline_df = pd.merge(monthly_paid, annual_avg, on='Year', how='left')
                
                # 为了用 Plotly 画两条线，我们需要把宽表 "融化 (melt)" 成长表
                timeline_melted = timeline_df.melt(
                    id_vars=['Date_Label'], 
                    value_vars=['Paid_Affiliates', 'Annual Average'],
                    var_name='Metric', 
                    value_name='Count'
                )
                
                # 将 'Paid_Affiliates' 重命名，使其在图例中更好看
                timeline_melted['Metric'] = timeline_melted['Metric'].replace({'Paid_Affiliates': 'Monthly Actual'})
                
                fig2 = px.line(
                    timeline_melted,
                    x='Date_Label',
                    y='Count',
                    color='Metric',
                    markers=True,
                    title='Paid Affiliates Trend & Annual Average',
                    labels={'Date_Label': 'MONTH', 'Count': 'Number of Paid Affiliates', 'Metric': ''},
                    color_discrete_map={'Monthly Actual': '#333333', 'Annual Average': '#FFC000'} # 蓝色和黄色的搭配
                )
                
                # 同样将图例放至图表上方
                fig2.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0))
                
                # ================= 渲染展示 =================
                # 并排展示两个折线图
                col1, col2 = st.columns(2)
                with col1:
                    st.plotly_chart(fig1, use_container_width=True)
                with col2:
                    st.plotly_chart(fig2, use_container_width=True)
                    
            else:
                st.warning("No 'Paid' affiliate data available up to the selected month/year.")

        # -------------------- Tab 6: Organic Affiliates --------------------
        with tab6:
            st.markdown("### 🌱 Organic Affiliates FTT Trend")
            
            # 1. 时间过滤逻辑：从最早的月份一直到选中的月份
            df['Period'] = df['Year'] * 100 + df['Month']
            selected_period = int(selected_year) * 100 + int(selected_month)
            organic_df = df[df['Period'] <= selected_period].copy()
            
            # 确保数据中存在我们需要的列
            if not organic_df.empty and 'Organic' in organic_df.columns and 'Ftt_Num' in organic_df.columns:
                
                # 生成连续的 YYYY-MM 时间轴标签
                organic_df['Date_Label'] = organic_df['Year'].astype(str) + '-' + organic_df['Month'].astype(str).str.zfill(2)
                
                # 计算每个月的 All FTT Number
                total_ftt = organic_df.groupby('Date_Label')['Ftt_Num'].sum().reset_index(name='All_FTT')
                
                # 筛选并计算每个月的 Organic FTT Number (忽略大小写匹配更安全)
                is_organic = organic_df['Organic'].fillna('').str.contains('Organic', case=False)
                organic_only = organic_df[is_organic]
                organic_ftt = organic_only.groupby('Date_Label')['Ftt_Num'].sum().reset_index(name='Organic_FTT')
                
                # 合并总数与 Organic 数量，并填补空缺月份为 0
                merged_ftt = pd.merge(total_ftt, organic_ftt, on='Date_Label', how='left').fillna(0)
                
                # 计算占比
                merged_ftt['Organic_PCT'] = (merged_ftt['Organic_FTT'] / merged_ftt['All_FTT']).fillna(0)
                
                # ================= Chart 1: 子母柱状图 (Overlaid Bar Chart) =================
                fig_bar = go.Figure()
                
                # 底部宽柱子 (深灰色：All FTT)
                fig_bar.add_trace(go.Bar(
                    x=merged_ftt['Date_Label'],
                    y=merged_ftt['All_FTT'],
                    name='All FTT Number',
                    marker_color='#595959', # 深灰色
                    width=0.8 # 💡 调大宽度比例
                ))
                
                # 顶部窄柱子 (金黄色：Organic FTT)
                fig_bar.add_trace(go.Bar(
                    x=merged_ftt['Date_Label'],
                    y=merged_ftt['Organic_FTT'],
                    name='Organic FTT Number',
                    marker_color='#FFC000', # 金黄色
                    width=0.4 # 💡 调大宽度比例
                ))
                
                fig_bar.update_layout(
                    barmode='overlay', # 叠加显示
                    title='All FTT Number vs Organic FTT Number',
                    xaxis_title='MONTH',
                    yaxis_title='',
                    # 💡 核心修复：强制 X 轴按“分类”解析，这样柱子才会正常变宽！
                    xaxis=dict(type='category'),
                    # 图例放到正下方中心位置
                    legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5) 
                )
                
                # ================= Chart 2: 占比趋势折线图 (Line Chart) =================
                # 准备显示在数据点上方的百分比文本 (例如 '24%')
                merged_ftt['Label'] = (merged_ftt['Organic_PCT'] * 100).round(0).astype(int).astype(str) + '%'
                
                fig_line = px.line(
                    merged_ftt,
                    x='Date_Label',
                    y='Organic_PCT',
                    markers=True,
                    text='Label',
                    title='Organic FTT %'
                )
                
                # 应用黄、黑主题色调
                fig_line.update_traces(
                    textposition="top center", 
                    textfont=dict(color='#000000', size=11, weight='bold'), # 黑色加粗字体
                    line=dict(color='#FFC000', width=3), # 金黄色粗线
                    marker=dict(size=8, color='#FFC000') # 金黄色圆点
                )
                
                fig_line.update_layout(
                    yaxis_tickformat='.0%',
                    xaxis_title='MONTH',
                    yaxis_title='',
                    yaxis_range=[0, merged_ftt['Organic_PCT'].max() * 1.2] 
                )
                
                # ================= 渲染展示 =================
                st.plotly_chart(fig_bar, use_container_width=True)
                st.plotly_chart(fig_line, use_container_width=True)
                
            else:
                st.warning("Missing 'Organic' or 'Ftt_Num' columns, or no data available for the selected period.")

    except Exception as e:
        st.error(f"An error occurred while processing the files: {e}")
else:
    # 当没有上传文件时，主页面显示的引导语
    st.info("👈 Please open the sidebar on the left and upload your `.csv` files to get started.")