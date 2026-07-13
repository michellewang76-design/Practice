import requests
from bs4 import BeautifulSoup
import re
import time  # 引入时间模块，用来控制爬虫速度

def extract_text_from_url(url, output_filename):
    """
    抓取网页并提取纯文本保存到本地
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        print(f"正在访问网页: {url} ...")
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status() 
        
        soup = BeautifulSoup(response.text, 'html.parser')
        raw_text = soup.get_text(separator='\n')
        clean_text = re.sub(r'\n+', '\n', raw_text).strip()
        
        with open(output_filename, 'w', encoding='utf-8') as file:
            file.write(clean_text)
            
        print(f"✅ 成功！纯文本已保存至: {output_filename}\n")
        
    except Exception as e:
        print(f"❌ 抓取失败 ({url}): {e}\n")

# ==========================================
# 核心改动区域：在这里把你要跑的学校排好队
# ==========================================

# 把每家学校的名字和收费网址写在这个大括号列表里
target_schools = [
    # 记得替换成真实的 URL
    {"name": "Meriden", "url": "https://www.meriden.nsw.edu.au/enrolment/schedule-of-fees/"}
    # {"name": "Shore", "url": "https://www.shore.nsw.edu.au/apply/school-fees"},
    # {"name": "Sceggs", "url": "https://www.sceggs.nsw.edu.au/enrolments/fees-and-payment-options/"}
    # 如果还有更多，就在这里加逗号继续写
    # {"name": "School_D", "url": "..."}
]

# 开始批量干活！
print("🚀 开始批量抓取任务...\n")

for school in target_schools:
    # 自动生成文件名，比如 "Meriden_raw_text.txt"
    save_name = f"{school['name']}_raw_text.txt"
    
    # 调用抓取函数
    extract_text_from_url(school['url'], save_name)
    
    # 礼貌性暂停 2 秒，防止被目标网站封锁 IP
    time.sleep(2)

print("🎉 所有抓取任务执行完毕！请查看左侧生成的 txt 文件。")