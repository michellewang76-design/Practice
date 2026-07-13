import pdfplumber
import re
import os

def extract_text_from_pdf(pdf_path):
    """
    读取单个 PDF 文件并返回所有页面的纯文本
    """
    # 检查文件是否存在，防止因为名字写错导致程序崩溃
    if not os.path.exists(pdf_path):
        return f"❌ 提取失败：找不到文件 '{pdf_path}'，请检查文件名和路径是否正确。"
        
    try:
        all_text = []
        # 使用 pdfplumber 打开 PDF
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    # 可选：在每页之间加个标记，方便大模型阅读
                    all_text.append(f"--- 第 {i+1} 页 ---")
                    all_text.append(text)
                    
        # 把所有页的文字拼接到一起
        raw_text = "\n".join(all_text)
        
        # 清洗：把连续的多个空行压缩成一个空行
        clean_text = re.sub(r'\n{2,}', '\n', raw_text).strip()
        return clean_text
        
    except Exception as e:
        return f"❌ 解析 PDF 失败: {e}"

# ==========================================
# 核心改动区域：在这里把你要跑的 PDF 文件排好队
# ==========================================

# 请确保这些 PDF 文件和你现在的 Python 代码文件放在同一个文件夹里！
target_pdfs = [
    {"name": "Abbotsleigh", "file_path": "School_Fee_Raw/Abbotsleigh-Fee-Schedule-2026.pdf"},
    {"name": "PymbleLadies", "file_path": "School_Fee_Raw/PymbleLadies-Fees-2026-FINAL2.pdf"},
    {"name": "MLC", "file_path": "School_Fee_Raw/MLC-2026-Scale-of-Fees-v4.pdf"}
    # 继续添加你需要处理的 PDF...
]

# 最终汇聚所有数据的大文件名称
master_filename = "School_Fee_Raw/All_PDFs_Raw_Text.txt"

print("🚀 开始批量抠取 PDF, 并将所有数据汇总到一个文件...\n")

# 使用 'w' 模式打开大文件
with open(master_filename, 'w', encoding='utf-8') as master_file:
    
    for item in target_pdfs:
        print(f"正在处理: {item['name']} ({item['file_path']}) ...")
        
        # 调用核心函数去抠字
        pdf_text = extract_text_from_pdf(item['file_path'])
        
        # 往大文件里写入分割线和学校名字
        master_file.write(f"=========================================\n")
        master_file.write(f"【学校名称】: {item['name']}\n")
        master_file.write(f"=========================================\n")
        
        # 写入抠出来的正文
        master_file.write(pdf_text + "\n\n")
        
        print(f"✅ {item['name']} 写入完毕。\n")

print(f"🎉 全部搞定！请打开左侧的 {master_filename}，所有 PDF 的内容都在里面了！")