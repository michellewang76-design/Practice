import streamlit as st
import pandas as pd

# 页面配置
st.set_page_config(page_title="CSV Merger Tool", page_icon="🔗")

st.title("🔗 Multiple CSV Files Merger")
st.markdown("Please upload multiple `.csv` files at once. The system will automatically concatenate them and provide the complete merged file for download.")

# 1. 上传组件：注意这里加了 accept_multiple_files=True，允许一次选多个文件
uploaded_files = st.file_uploader("Please upload your CSV files here", type=['csv'], accept_multiple_files=True)

# 只有当用户确实上传了文件（且文件数量大于0）时才执行
if uploaded_files:
    try:
        # 创建占位符，用于处理完毕后清空提示（阅后即焚）
        status_text = st.empty()
        progress_bar_placeholder = st.empty()
        
        status_text.info(f"Processing... Reading {len(uploaded_files)} file(s).")
        progress_bar = progress_bar_placeholder.progress(0)
        
        df_list = []
        total_files = len(uploaded_files)
        
        # 2. 遍历读取所有用户上传的文件
        for i, file in enumerate(uploaded_files):
            # 将上传的文件读取为 DataFrame
            df = pd.read_csv(file, encoding='utf-8-sig')
            df_list.append(df)
            
            # 更新进度条
            progress_bar.progress((i + 1) / total_files)
            
        status_text.info("All files read successfully, executing merge...")
        
        # 3. 开始合并
        if df_list:
            # 使用 concat 将所有数据框按行上下拼接起来
            merged_df = pd.concat(df_list, ignore_index=True)
            
            # 将合并后的数据转回 CSV 格式的字符串
            csv_data = merged_df.to_csv(index=False, encoding='utf-8-sig')
            
            # 处理完成后，清空占位符（让 Processing 提示消失）
            status_text.empty()
            progress_bar_placeholder.empty()
            
            # 显示最终的成功信息
            st.success(f"🎉 Completed! Successfully merged **{total_files}** files. Total rows: **{len(merged_df)}**.")
            
            # 4. 生成下载按钮
            st.download_button(
                label="⬇️ Click and download Merged CSV",
                data=csv_data,
                file_name="Merged_Data.csv",
                mime="text/csv"
            )
            
    except Exception as e:
        # 完整的错误捕获，防止页面崩溃
        st.error(f"An error occurred during merging: {e}")