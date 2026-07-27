import streamlit as st
import pandas as pd

# ==========================================
# 🔀 "What-If" Routing Simulator
# ==========================================

st.set_page_config(page_title="routing", page_icon="🔀", layout="wide")

# 2. 在页面最顶端渲染导航栏
from navbar import create_top_nav
create_top_nav()

st.markdown("### 🔀 'What-If' Routing Simulator (Scenario Modeling)")
st.info("Adjust the volume allocation sliders to simulate how shifting traffic impacts your overall approval rate and processing costs.")

# 1. 模拟底层数据 (实际应用中，这里的数据可以从cost_df 和历史订单里动态聚合)
# 这里假设 SafeCharge 审批率高但略贵，CheckoutCom 居中，Eximbay 审批率低但最便宜（纯假设）
psp_data = {
    "SafeCharge": {"appr_rate": 0.88, "cost_rate": 0.011}, # 88% Appr, 1.1% Cost
    "CheckoutCom": {"appr_rate": 0.85, "cost_rate": 0.014}, # 85% Appr, 1.4% Cost
    "Eximbay": {"appr_rate": 0.72, "cost_rate": 0.022}      # 72% Appr, 2.2% Cost
}

# 2. 设定业务总量和历史基线 (Baseline)
# 假设上个月的综合审批率是 82%，综合费率是 1.6%
col_input1, col_input2 = st.columns(2)
with col_input1:
    total_volume = st.number_input("💰 Expected Monthly Volume (¥)", min_value=10000, value=1000000, step=100000)
    
baseline_appr = 0.82 
baseline_cost = total_volume * 0.016

# 3. 渲染滑块面板 (Sliders)
st.markdown("#### 🎚️ Allocate Traffic Volume (%)")
col_s1, col_s2, col_s3 = st.columns(3)

with col_s1:
    alloc_sc = st.slider("SafeCharge (88% Appr, 1.1% Fee)", 0, 100, 50)
with col_s2:
    alloc_cc = st.slider("CheckoutCom (85% Appr, 1.4% Fee)", 0, 100, 30)
with col_s3:
    alloc_ex = st.slider("Eximbay (72% Appr, 2.2% Fee)", 0, 100, 20)

total_alloc = alloc_sc + alloc_cc + alloc_ex

# 4. 核心计算与校验逻辑
if total_alloc != 100:
    # 强制用户必须将比例分配到刚好 100%
    st.error(f"⚠️ Total volume allocation must equal exactly 100%. Current total: **{total_alloc}%**")
else:
    # 计算加权综合审批率
    blended_appr = (
        (alloc_sc / 100 * psp_data["SafeCharge"]["appr_rate"]) +
        (alloc_cc / 100 * psp_data["CheckoutCom"]["appr_rate"]) +
        (alloc_ex / 100 * psp_data["Eximbay"]["appr_rate"])
    )
    
    # 计算预估总成本
    total_cost = (
        (total_volume * alloc_sc / 100 * psp_data["SafeCharge"]["cost_rate"]) +
        (total_volume * alloc_cc / 100 * psp_data["CheckoutCom"]["cost_rate"]) +
        (total_volume * alloc_ex / 100 * psp_data["Eximbay"]["cost_rate"])
    )

    # 计算与基线的差距
    appr_delta = blended_appr - baseline_appr
    cost_delta = total_cost - baseline_cost

    # 5. 可视化指标呈现
    st.markdown("#### 📊 Projected Outcomes vs. Baseline")
    m1, m2, m3 = st.columns(3)
    
    with m1:
        st.metric(
            label="🎯 Blended Approval Rate", 
            value=f"{blended_appr * 100:.1f}%", 
            delta=f"{appr_delta * 100:.1f}%",
            delta_color="normal"
        )
        
    with m2:
        st.metric(
            label="💸 Estimated Total Cost", 
            value=f"¥{total_cost:,.0f}", 
            delta=f"¥{cost_delta:,.0f}",
            delta_color="inverse" 
        )
        
    with m3:
        impact_label = "✅ Net Savings" if cost_delta <= 0 else "⚠️ Additional Cost"
        st.metric(
            label=impact_label, 
            value=f"¥{abs(cost_delta):,.0f}"
        )

