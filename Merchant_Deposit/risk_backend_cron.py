import requests
import time
import schedule
import random # 仅作演示用

# 🔗 替换为真实的 Slack 或 Teams Webhook URL
WEBHOOK_URL = "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"

def fetch_db_and_check_anomaly():
    """
    真实场景：连接 SQL 数据库，执行查询并比对阈值。
    """
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Checking SQL Database for anomalies...")
    
    # 模拟：10% 的概率发现重大异常
    if random.random() < 0.1:
        # 发现异常，立刻触发报警函数
        send_alert_to_slack(psp="Adyen", card_type="Visa", drop_rate=6.5)
    else:
        print("✅ All systems stable. No anomalies found.")

def send_alert_to_slack(psp, card_type, drop_rate):
    """
    组装报警消息并发送至 Slack
    """
    # Slack 的消息格式 (如果是 Teams，JSON 结构略有不同，需参考官方文档)
    payload = {
        "text": f"🚨 *URGENT PAYMENT ALERT* 🚨\n*Gateway:* {psp}\n*Card Type:* {card_type}\n*Issue:* Approval rate dropped by *{drop_rate}%* in the last 10 minutes.\n<!channel> Please check the Streamlit Dashboard immediately!"
    }
    
    try:
        # 发送 POST 请求将消息推送到群组
        response = requests.post(WEBHOOK_URL, json=payload)
        
        if response.status_code == 200:
            print("🚨 Alert successfully sent to Slack!")
        else:
            print(f"❌ Failed to send alert. Status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Network error occurred: {e}")

# ==========================================
# ⏱️ 任务调度器 (Scheduler)
# ==========================================
# 设定每 10 分钟执行一次检查任务
schedule.every(10).minutes.do(fetch_db_and_check_anomaly)

print("🛡️ Risk Backend Cron Job started. Monitoring database every 10 minutes...")

# 保持脚本永久运行的死循环
while True:
    schedule.run_pending()
    time.sleep(1) # 每秒醒来一次检查时间是否到了