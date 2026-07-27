import streamlit as st
import pandas as pd
import os
import plotly.express as px
from anomaly_detector import show_anomaly_alerts
from streamlit_autorefresh import st_autorefresh

# ==========================================
# ⏱️ 设置页面自动刷新机制
# ==========================================
# interval: 以毫秒为单位。10 分钟 = 10 * 60 * 1000 = 600000 毫秒
# limit: None 表示无限次刷新
# key: 必须指定，用于在 session_state 中追踪刷新状态
st_autorefresh(interval=600000, limit=None, key="10min_db_refresh")

# ==========================================
# 1. 页面基本设置
# ==========================================
st.set_page_config(page_title="Payment Manager", page_icon="💼", layout="wide")

# 🌟 2. 在页面最顶端渲染导航栏
from navbar import create_top_nav
create_top_nav()

st.title("💼 Payment Manager: Cost & Risk Control")
st.markdown("""
**For Payment Managers Only:**
Use this interface to manage PSP contract terms, processing rates, and reserve policies. 
Updates here will serve as the foundation for the Smart Routing Engine and Liquidity Analysis.
""")

# 调用异常警报组件
show_anomaly_alerts()

# 提取全局密码状态 (输入框已移至下方，这里仅获取状态以防止上方组件报错)
admin_password = st.session_state.get("admin_pw", "")

# 注入 CSS，将所有多选框的选中标签背景色强制改为灰色
st.markdown("""
<style>
span[data-baseweb="tag"] { 
    background-color: #C0C0C0 !important; 
    color: #333333 !important; 
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 正在计划中的 Payment Gateway 进度图 (Gantt Chart)
# ==========================================

st.markdown("### 🚀 Planned Payment Gateways Pipeline")

# 生成进度图的模拟数据 (可以后续改成从 CSV 读取)
pipeline_data = pd.DataFrame([
    {"Gateway": "Stripe", "Start": "2026-08-01", "Finish": "2026-09-15", "Phase": "1. Contract & Compliance"},
    {"Gateway": "Stripe", "Start": "2026-09-16", "Finish": "2026-10-20", "Phase": "2. Tech Integration"},
    {"Gateway": "Adyen", "Start": "2026-07-20", "Finish": "2026-08-30", "Phase": "2. Tech Integration"},
    {"Gateway": "Adyen", "Start": "2026-09-01", "Finish": "2026-09-15", "Phase": "3. UAT & Live"},
    {"Gateway": "PayPal Asia", "Start": "2026-10-01", "Finish": "2026-11-15", "Phase": "1. Contract & Compliance"},
    {"Gateway": "DLocal", "Start": "2026-08-15", "Finish": "2026-10-10", "Phase": "2. Tech Integration"}
])

# 将字符串转换为日期时间格式
pipeline_data['Start'] = pd.to_datetime(pipeline_data['Start'])
pipeline_data['Finish'] = pd.to_datetime(pipeline_data['Finish'])

# 使用 Plotly Express 绘制甘特图
fig_timeline = px.timeline(
    pipeline_data, 
    x_start="Start", 
    x_end="Finish", 
    y="Gateway", 
    color="Phase",
    color_discrete_sequence=["#5C6BC0", "#42A5F5", "#66BB6A"] # 设定漂亮的蓝绿配色
)

# 倒转 Y 轴，让最先开始的项目排在上面
fig_timeline.update_yaxes(autorange="reversed")

fig_timeline.update_layout(
    height=300,
    margin=dict(l=20, r=20, t=30, b=20),
    legend_title_text="Project Phase",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig_timeline, use_container_width=True)
st.markdown("---")

# ==========================================
# 🚨 Active Risk & Incident Management (Dynamic)
# ==========================================
st.markdown("### 🚨 Active Risk & Incident Management")
st.markdown("Track ongoing operational issues, compliance risks, and settlement delays.")

# 1. 数据加载与初始化

# 获取当前脚本所在目录 (Merchant_Deposit)
current_dir = os.path.dirname(os.path.abspath(__file__))
# 拼接 data 文件夹内的路径
RISK_FILE_PATH = os.path.join(current_dir, 'data', 'psp_risks.csv')

def load_or_create_risk_data():
    if os.path.exists(RISK_FILE_PATH):
        return pd.read_csv(RISK_FILE_PATH)
    
    # 如果不存在，则生成初始默认数据
    initial_risk_data = {
        "PSP Name": ["FsTechnologies", "Eximbay", "PaymentZ"],
        "Severity": ["Critical", "High", "Medium"],
        "Issue": ["PSP filed for bankruptcy / operations ceased.", "CB ratio breached 2.5% threshold.", "Weekly settlement delayed by 4 business days."],
        "Impact": ["$150k settlement funds currently frozen.", "PSP threatening to increase rolling reserve from 10% to 15%.", "Cash flow disruption."],
        "Action": ["Smart routing disabled. Legal team engaged.", "Risk team analyzing CB reasons. Negotiating.", "Finance team following up daily. Routing paused."]
    }
    risk_df = pd.DataFrame(initial_risk_data)
    risk_df.to_csv(RISK_FILE_PATH, index=False)
    return risk_df

risk_df = load_or_create_risk_data()

# 2. 动态渲染卡片 (每 3 个一行排列)
if not risk_df.empty:
    cols = st.columns(3)
    for index, row in risk_df.iterrows():
        col = cols[index % 3] # 使用取模运算，将卡片轮流放入 3 列中
        with col:
            # 组装卡片内部的 Markdown 文本
            card_content = f"**[{row['Severity']}] {row['PSP Name']}**\n* **Issue:** {row['Issue']}\n* **Impact:** {row['Impact']}\n* **Action:** {row['Action']}"
            
            # 根据严重程度决定卡片的颜色
            if row['Severity'] == 'Critical':
                st.error(card_content)
            elif row['Severity'] in ['High', 'Medium']:
                st.warning(card_content)
            else:
                st.info(card_content)
else:
    st.success("🎉 No active risks at the moment. All systems green!")

# 3. 编辑面板 (放置在可折叠区域中)
with st.expander("⚙️ Manage Risk & Incident Records", expanded=False):
    # 复用之前定义的密码变量 (只需在一个地方输入密码即可解锁所有功能)
    if admin_password == "admin123":
        st.info("💡 **Tips:** Select 'Critical', 'High', 'Medium', or 'Info' for Severity to change the card color.")
        
        # 使用 column_config 将 Severity 列变成下拉菜单，防止输错
        edited_risk_df = st.data_editor(
            risk_df,
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "Severity": st.column_config.SelectboxColumn(
                    "Severity Level",
                    help="Critical = Red, High/Medium = Yellow, Info = Blue",
                    options=["Critical", "High", "Medium", "Info"],
                    required=True
                )
            }
        )
        
        col_r1, col_r2, col_r3 = st.columns([1, 2, 1])
        with col_r2:
            if st.button("💾 Save Risk Records", use_container_width=True):
                # 保存最新的 risk 数据
                edited_risk_df.to_csv(RISK_FILE_PATH, index=False)
                st.success("✅ Risk records updated successfully!")
                st.cache_data.clear()
                # 强制刷新页面，让上方的卡片立刻应用最新的数据
                st.rerun() 
    else:
        st.warning("🔒 Enter the Admin Password in the section above to edit risk records.")
        st.dataframe(risk_df, use_container_width=True)

st.markdown("---")

# ==========================================
# 2. 数据加载与初始化
# ==========================================

# current_dir 在上面已经定义过了，这里直接复用即可
COST_FILE_PATH = os.path.join(current_dir, 'data', 'psp_costs.csv')

def load_or_create_cost_data():
    # 如果文件已存在，直接读取
    if os.path.exists(COST_FILE_PATH):
        return pd.read_csv(COST_FILE_PATH)
    
    # 如果文件不存在（第一次运行），则自动生成之前讨论的初始默认数据
    initial_data = {
        "PSP Name": ["Acquiringcom", "Alweave", "CheckoutCom", "Eximbay", "FsTechnologies", "Gmo", "Intraclear", "LateralPay", "PaymentZ", "Paystra", "Powercash21", "SafeCharge", "SafeCharge2", "SBM", "SimpleTransact", "Worldpay"],
        "Processing Rate (%)": [1.35, 1.90, 1.40, 2.20, 1.20, 2.00, 1.25, 1.60, 1.50, 1.45, 1.70, 1.10, 1.05, 2.10, 1.15, 1.80],
        "Fixed Trx Fee ($)": [0.25, 0.10, 0.20, 0.00, 0.20, 0.10, 0.30, 0.15, 0.15, 0.20, 0.15, 0.25, 0.20, 0.10, 0.25, 0.10],
        "Chargeback Fee ($)": [15.0, 22.0, 18.0, 30.0, 15.0, 20.0, 25.0, 20.0, 20.0, 15.0, 18.0, 15.0, 15.0, 25.0, 10.0, 25.0],
        "Refund Fee ($)": [0.50, 0.50, 0.50, 1.00, 0.50, 0.40, 0.50, 0.00, 0.00, 0.50, 0.20, 0.30, 0.30, 0.50, 0.25, 0.20],
        "FX Surcharge (%)": [1.00, 1.70, 1.20, 2.50, 1.00, 1.80, 1.50, 1.20, 1.50, 1.00, 1.50, 0.50, 0.50, 2.00, 0.80, 2.00],
        "Monthly Fee ($)": [25, 0, 0, 0, 0, 30, 0, 0, 50, 0, 40, 100, 150, 0, 99, 0],
        "Settlement Fee": ["Free", "Free", "Free", "0.50%", "Free", "Free", "0.20%", "Free", "0.10%", "Free", "Free", "Free", "Free", "0.30%", "Free", "$10 per payout"],
        "Reserve Type": ["Rolling", "Fixed", "None", "Rolling", "None", "Rolling", "Fixed", "Rolling", "Rolling", "None", "Rolling", "Fixed", "Fixed", "Rolling", "None", "Rolling"],
        "Reserve Amount / Rate": ["5% (6 months)", "$50,000", "N/A", "10% (3 months)", "N/A", "5% (3 months)", "$100,000", "8% (6 months)", "10% (6 months)", "N/A", "5% (6 months)", "$200,000", "$150,000", "10% (6 months)", "N/A", "5% (6 months)"],
        "Release Terms": ["180 days", "90 days", "N/A", "180 days", "N/A", "90 days", "180 days", "180 days", "180 days", "N/A", "180 days", "180 days", "180 days", "180 days", "N/A", "180 days"]
    }
    df = pd.DataFrame(initial_data)
    # 将初始数据保存为 CSV，方便后续读取
    df.to_csv(COST_FILE_PATH, index=False)
    return df

cost_df = load_or_create_cost_data()

# ==========================================
# 3. 过滤组件 & 交互式表格渲染
# ==========================================
st.markdown("### 📝 Comprehensive PSP Cost & Risk Structure Table")

# ----------------------------------------
# 多维度过滤组件 (Multi-filters)
# ----------------------------------------
# 第一行：PSP 名字搜索
search_psp = st.text_input("🔍 Search by PSP Name")

# 第二行：将剩下的 4 个 Filter 平分为 4 列展示
col_f1, col_f2, col_f3, col_f4 = st.columns(4)

with col_f1:
    settlement_fees = cost_df['Settlement Fee'].dropna().unique().tolist()
    selected_settlement = st.multiselect("🏷️ Settlement Fee", settlement_fees, default=[])

with col_f2:
    reserve_types = cost_df['Reserve Type'].dropna().unique().tolist()
    selected_reserve = st.multiselect("🏷️ Reserve Type", reserve_types, default=[])

with col_f3:
    reserve_amounts = cost_df['Reserve Amount / Rate'].dropna().unique().tolist()
    selected_reserve_amount = st.multiselect("🏷️ Reserve Amount / Rate", reserve_amounts, default=[])

with col_f4:
    release_terms = cost_df['Release Terms'].dropna().unique().tolist()
    selected_release = st.multiselect("🏷️ Release Terms", release_terms, default=[])
    
# 应用所有过滤逻辑
filtered_df = cost_df.copy()
if search_psp:
    filtered_df = filtered_df[filtered_df['PSP Name'].str.contains(search_psp, case=False, na=False)]
if selected_settlement:
    filtered_df = filtered_df[filtered_df['Settlement Fee'].isin(selected_settlement)]
if selected_reserve:
    filtered_df = filtered_df[filtered_df['Reserve Type'].isin(selected_reserve)]
if selected_reserve_amount:
    filtered_df = filtered_df[filtered_df['Reserve Amount / Rate'].isin(selected_reserve_amount)]
if selected_release:
    filtered_df = filtered_df[filtered_df['Release Terms'].isin(selected_release)]

# ==========================================
# 4. 折叠区域：权限控制与表格渲染
# ==========================================
# 使用 st.expander 制作可纵向展开/收起的面板 (expanded=True 表示默认打开)
with st.expander("📊 PSP Cost & Risk Data Table (Click to Expand/Collapse)", expanded=True):
    
    # 密码输入框位置：使用 key 绑定到全局状态，这样即使在下方输入，上方的看板也能解锁
    admin_password = st.text_input("🔐 Enter Admin Password to Unlock Editing Features", type="password", key="admin_pw")

    if admin_password == "admin123":
        st.success("✅ Admin Access Granted. You can now edit, add, or delete PSPs.")
        st.info("💡 **How to edit/add:** Double-click any cell. Scroll to bottom and click **'+'** to add.\n💡 **How to DELETE:** Click the grey index box on the far left, then press `Delete`.")
        
        edited_df = st.data_editor(
            filtered_df, 
            num_rows="dynamic", 
            use_container_width=True,
            height=600
        )
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("💾 Save Changes to Database", use_container_width=True):
                updated_original = edited_df[edited_df.index.isin(cost_df.index)]
                cost_df.update(updated_original)
                
                new_rows = edited_df[~edited_df.index.isin(cost_df.index)]
                if not new_rows.empty:
                    cost_df = pd.concat([cost_df, new_rows])
                
                deleted_indices = filtered_df.index.difference(edited_df.index)
                cost_df = cost_df.drop(deleted_indices)
                
                cost_df.to_csv(COST_FILE_PATH, index=False)
                st.success("✅ Changes saved successfully!")
                st.cache_data.clear()

    else:
        if admin_password:
            st.error("❌ Incorrect Password. View-only mode is active.")
        else:
            st.info("ℹ️ View-only mode. Enter the admin password above to make changes.")
            
        st.dataframe(
            filtered_df,
            use_container_width=True,
            height=600
        )

