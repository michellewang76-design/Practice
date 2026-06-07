import pandas as pd
import numpy as np

# 生成 10 行员工薪资数据
df = pd.DataFrame({
    'Name': [f'Employee {i}' for i in range(1, 11)],
    'Salary': np.random.randint(4000, 8001, size=10)
})

# 保存到 Excel，标题写在 A1，表格从第 2 行开始
with pd.ExcelWriter('Employee Salary.xlsx', engine='openpyxl') as writer:
    df.to_excel(writer, index=False, startrow=1)
    worksheet = writer.sheets['Sheet1']
    worksheet['A1'] = '📊 Wenona Test Salary Template：'

print('Employee Salary.xlsx generated successfully!')
