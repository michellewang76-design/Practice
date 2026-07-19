import pandas as pd
import os

def split_csv_by_time(file_path):
    """
    根据 Year 和 Month 列将 CSV 文件拆分为多个独立文件。
    """
    print(f"正在读取文件: {file_path}")
    try:
        # 用 read_csv 读取 CSV 文件
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"读取文件出错: {e}")
        return

    if 'Year' not in df.columns or 'Month' not in df.columns:
        print("错误：CSV 中未找到 'Year' 或 'Month' 列，请确保首行包含这两个表头（区分大小写）。")
        return

    base_dir = os.path.dirname(os.path.abspath(file_path))
    output_dir = os.path.join(base_dir, "Affiliates_Monthly")
    os.makedirs(output_dir, exist_ok=True)

    grouped = df.groupby(['Year', 'Month'])

    count = 0
    for (year, month), group_data in grouped:
        # 将后缀改为 .csv
        filename = f"{int(year)}_{int(month):02d}.csv"
        output_path = os.path.join(output_dir, filename)
        
        # 改用 to_csv 导出，并去掉索引
        group_data.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"✅ file generated: {filename} (包含 {len(group_data)} rows)")
        count += 1
        
    print(f"\n🎉 拆分成功！共生成了 {count} 个 CSV 文件。")
    print(f"📂 所有文件保存在: {output_dir}")

if __name__ == "__main__":
    # 请将此处替换为您实际的 .csv 文件路径
    my_file = r"C:\Users\Michelle Wang\Desktop\Jobs\TMGM\case study\Affiliates\Affliate raw data.csv"
    split_csv_by_time(my_file)