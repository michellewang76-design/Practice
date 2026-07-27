import streamlit as st
import random
import time

def run_anomaly_detection():
    """后台计算逻辑"""
    has_anomaly = random.choice([True, False]) 
    if has_anomaly:
        return [
            {"psp": "Adyen", "card": "Visa", "drop": 5.8},
            {"psp": "Eximbay", "card": "Mastercard", "drop": 7.2}
        ]
    return []

def show_anomaly_alerts():
    """负责渲染 UI 和弹窗的主函数"""
    st.markdown("### 📡 Real-time Anomaly Monitor")

    if 'toast_shown' not in st.session_state:
        st.session_state['toast_shown'] = False

    if not st.session_state['toast_shown']:
        anomalies = run_anomaly_detection()
        
        if anomalies:
            for alert in anomalies:
                msg = f"{alert['psp']} {alert['card']} approval rate dropped by {alert['drop']}% in the last hour!"
                st.toast(msg, icon="🚨")
                time.sleep(0.5)
                
            st.session_state['toast_shown'] = True
            st.session_state['current_anomalies'] = anomalies 
        else:
            st.session_state['toast_shown'] = True
            st.session_state['current_anomalies'] = []

    if st.session_state.get('current_anomalies'):
        for alert in st.session_state['current_anomalies']:
            st.error(f"**CRITICAL ALERT:** {alert['psp']} {alert['card']} approval rate dropped by {alert['drop']}% in the last hour! Immediate routing adjustment recommended.", icon="🚨")

    if st.button("🔄 Manually Re-run Anomaly Check"):
        st.session_state['toast_shown'] = False
        st.rerun()

    st.markdown("---")