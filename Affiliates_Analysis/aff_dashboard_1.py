import streamlit as st
import pandas as pd
import plotly.express as px

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
            selected_year = st.selectbox("📌 Choose a Year", years)

        with col2:
            months = sorted(df[df['Year'] == selected_year]['Month'].dropna().unique().tolist())
            selected_month = st.selectbox("🎯 Choose a Month", months)

        st.success(f"✅ You selected: **Month {selected_month}, {selected_year}**")

        st.info("""
        **📢 Notice**
        * The data displayed represents the figures available **at the time it is run**.
        * The data shown reflects **Affiliate commissions earned during the prior month**.
        * Discrepancies between the Original Unpaid List Total and Actual Paid Total will occur due to reviews or payment transfer issues.
        * **Unpaid_No_Bank + Unpaid_BounceBack** changes back to **Unpaid** when affiliate updates their bank account.
        """)

        filtered_df = df[(df['Year'] == selected_year) & (df['Month'] == selected_month)]

        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Summary of Monthly Payout", 
            "Breakdown of Payout Status", 
            "Payout Processed", 
            "📊 Charts & Visuals",
            "📈 Trend Analysis"  # 新增的第五个 Tab
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
                    
                    fig = px.pie(final_df, values=values_col, names=names_col, color_discrete_sequence=colors)
                    
                    fig.update_traces(
                        textinfo='percent+label',
                        texttemplate='%{label}<br>%{percent:.0%}', 
                        hovertemplate='<b>%{label}</b><br>Value: %{value:,.0f}<br>Percent: %{percent:.0%}',
                        marker=dict(line=dict(color='#FFFFFF', width=1.5))
                    )
                    
                    fig.update_layout(showlegend=False)
                    return fig
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("**1. Payout by Status**")
                    fig1 = create_custom_pie(filtered_df, 'Status', 'Approved_Fee')
                    if fig1:
                        st.plotly_chart(fig1, use_container_width=True)
                    
                with col2:
                    st.markdown("**2. Affiliates by Status**")
                    count_df = filtered_df.groupby('Status')['Affiliate_ID'].nunique().reset_index()
                    count_df.rename(columns={'Affiliate_ID': 'Count'}, inplace=True)
                    fig2 = create_custom_pie(count_df, 'Status', 'Count')
                    if fig2:
                        st.plotly_chart(fig2, use_container_width=True)
                
                with col3:
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
                    color_discrete_map={'Monthly Actual': '#1f77b4', 'Annual Average': '#FFC000'} # 蓝色和黄色的搭配
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

    except Exception as e:
        st.error(f"An error occurred while processing the files: {e}")
else:
    # 当没有上传文件时，主页面显示的引导语
    st.info("👈 Please open the sidebar on the left and upload your `.csv` files to get started.")