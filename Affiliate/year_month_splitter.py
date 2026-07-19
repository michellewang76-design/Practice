import streamlit as st
import pandas as pd
import zipfile
import io

# 页面配置
st.set_page_config(page_title="Year_Month_Splitter", page_icon="✂️")

st.title("✂️ Split your .csv by Year_Month")
st.markdown("Please upload your source document (`.csv` or `.xlsx`), I will split it by `Year` & `Month` into individual CSV files, and provide a ZIP for your to download.")

# 1. 上传文件组件
uploaded_file = st.file_uploader("Please upload your source document", type=['csv', 'xlsx'])

if uploaded_file is not None:
    try:
        # 2. 读取文件 (根据后缀名自动判断)
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        with st.spinner('Processing...'):
            if file_extension == 'csv':
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
        st.success("✅ Upload successful!")
        
        # 3. 验证必需的列名
        if 'Year' not in df.columns or 'Month' not in df.columns:
            st.error("❌ Error: The “Year” or “Month” columns were not found in the file. Please check the header in the first row (case-sensitive).")
        else:
            
            # 4. 准备拆分并打包进 ZIP
            # 【优化点1】：创建两个占位符 (分别用于文本提示和进度条)
            status_text = st.empty()
            progress_bar_placeholder = st.empty()
            
            # 在占位符中显示处理中的信息
            status_text.info("Processing splitting...")
            progress_bar = progress_bar_placeholder.progress(0)
            
            # 创建一个内存中的 ZIP 文件容器
            zip_buffer = io.BytesIO()
            
            # 使用 zipfile 写入数据
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                grouped = df.groupby(['Year', 'Month'])
                count = 0
                total_groups = len(grouped)
                
                for i, ((year, month), group_data) in enumerate(grouped):
                    # 构造每个小文件的文件名
                    filename = f"{int(year)}年{int(month):02d}月.csv"
                    
                    # 将 dataframe 转换为 csv 格式的文本字符串
                    csv_data = group_data.to_csv(index=False, encoding='utf-8-sig')
                    
                    # 将该文本直接写入 ZIP 压缩包内
                    zip_file.writestr(filename, csv_data)
                    count += 1
                    
                    # 更新进度条
                    progress_bar.progress((i + 1) / total_groups)
            
            # 【优化点2】：处理完成后，清空这两个占位符，让它们从页面上消失！
            status_text.empty()
            progress_bar_placeholder.empty()
            
            # 显示最终的成功信息
            st.success(f"🎉 Completed! Splitted into {count} CSV files.")
            
            # 5. 生成下载按钮
            st.download_button(
                label="⬇️ click and download ZIP",
                data=zip_buffer.getvalue(),
                file_name="Splitted_Data.zip",
                mime="application/zip"
            )

    except Exception as e:
        st.error(f"处理文件时出错: {e}")   