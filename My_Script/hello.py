import pandas as pd
import numpy as np
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "Data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# 生成 10 行员工薪资数据
df = pd.DataFrame({
    'Name': [f'Employee {i}' for i in range(1, 11)],
    'Salary': np.random.randint(4000, 8001, size=10)
})

output_file = DATA_DIR / "Employee Salary.xlsx"

# 保存到 Excel，标题写在 A1，表格从第 2 行开始
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    df.to_excel(writer, index=False, startrow=1)
    worksheet = writer.sheets['Sheet1']
    worksheet['A1'] = '📊 Wenona Test Salary Template：'

print(f'{output_file} generated successfully!')
