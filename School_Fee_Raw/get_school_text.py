import requests
from bs4 import BeautifulSoup
import re

def extract_text_from_url(url, output_filename):
    """
    抓取网页并提取纯文本保存到本地
    """
    # 1. 伪装成浏览器，防止被直接拒绝
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        print(f"正在访问网页: {url} ...")
        # 2. 发送请求获取网页
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status() # 如果网页打不开（比如 404），这里会直接报错
        
        # 3. 使用 BeautifulSoup 解析网页
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 4. 【核心魔法】提取所有纯文本，并用换行符隔开
        raw_text = soup.get_text(separator='\n')
        
        # 5. 【数据清洗】把连续的多个空行压缩成一个空行，让文本看起来不那么长
        # 这一步不是必须的，但可以让大模型读起来更省字数（省钱/省Token）
        clean_text = re.sub(r'\n+', '\n', raw_text).strip()
        
        # 6. 将清洗后的文字写入 TXT 文件
        # 使用 utf-8 编码，防止中文或特殊符号乱码
        with open(output_filename, 'w', encoding='utf-8') as file:
            file.write(clean_text)
            
        print(f"✅ 成功！纯文本已保存至: {output_filename}")
        
    except Exception as e:
        print(f"❌ 抓取失败: {e}")

# ==========================================
# 在这里填入你想测试的学校网址和保存的文件名
# ==========================================
target_url = "https://www.meriden.nsw.edu.au/enrolment/schedule-of-fees/"  # 替换成真实的学校收费网址
save_name = "school_Meriden_raw_text.txt"

extract_text_from_url(target_url, save_name)
