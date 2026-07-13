import pandas as pd

print("⏳ 正在读取 JSON 数据...")
# 1. 读取刚才保存的 JSON 文件
# df = pd.read_json("result_fromGemini.json")
df = pd.read_json("School_Fee_Raw/result_from_pdf_Gemini.json")

# 2. 把它变成 Excel 文件
excel_filename = "School_Fee_Raw/Schools_Fee_Report_fromPDF.xlsx"
df.to_excel(excel_filename, index=False)

print(f"🎉 搞定！快去左边文件夹看看，你的 {excel_filename} 已经生成了！")