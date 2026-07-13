import requests
from bs4 import BeautifulSoup
import re
import time

def extract_text_from_url(url):
    """
    抓取网页并提取纯文本，直接返回文本内容，不再单独存文件
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status() 
        soup = BeautifulSoup(response.text, 'html.parser')
        raw_text = soup.get_text(separator='\n')
        clean_text = re.sub(r'\n+', '\n', raw_text).strip()
        return clean_text
    except Exception as e:
        return f"抓取失败: {e}"

# ==========================================
# 你的学校名单
# ==========================================
target_schools = [
    {"name": "Meriden", "url": "https://www.meriden.nsw.edu.au/enrolment/schedule-of-fees/"}, 
    {"name": "Shore", "url": "https://www.shore.nsw.edu.au/apply/school-fees"},
    {"name": "Sceggs", "url": "https://www.sceggs.nsw.edu.au/enrolments/fees-and-payment-options/"}
    # 继续添加...
]

# 最终汇聚所有数据的大文件名称
master_filename = "All_Schools_Raw_Text.txt"

print("🚀 开始批量抓取，并将所有数据汇总到一个文件...\n")

# 使用 'w' 模式打开文件（如果文件已存在会覆盖清空重新写）
with open(master_filename, 'w', encoding='utf-8') as master_file:
    
    for school in target_schools:
        print(f"正在抓取: {school['name']} ...")
        
        # 获取网页纯文本
        school_text = extract_text_from_url(school['url'])
        
        # 往大文件里写入明显的分割线和学校名字，方便大模型区分
        master_file.write(f"=========================================\n")
        master_file.write(f"【学校名称】: {school['name']}\n")
        master_file.write(f"=========================================\n")
        
        # 写入抓取到的正文
        master_file.write(school_text + "\n\n")
        
        print(f"✅ {school['name']} 写入完毕。\n")
        time.sleep(2) # 礼貌暂停

print(f"🎉 全部搞定！请打开 {master_filename}，所有学校的内容都在里面了！")