import pandas as pd

# 读取员工基本信息表
print("=== 员工基本信息表 ===")
basic_info_df = pd.read_excel('员工基本信息表.xlsx')
print(basic_info_df)
print()

# 读取员工绩效表，并筛选2024年第4季度的数据
print("=== 员工绩效表（2024年第4季度） ===")
performance_df = pd.read_excel('员工绩效表.xlsx')
# 筛选2024年第4季度的数据
perf_2024_q4 = performance_df[(performance_df['年度'] == 2024) & (performance_df['季度'] == 4)]
print(perf_2024_q4)
print()

# 合并基本信息表和2024年第4季度绩效数据
print("=== 合并后的员工信息表（包含2024年第4季度绩效） ===")
merged_df = pd.merge(basic_info_df, perf_2024_q4, on='员工ID', how='left')
print(merged_df)
print()

# 保存合并后的数据到新的Excel文件
merged_df.to_excel('员工信息及绩效表.xlsx', index=False)
print("合并后的数据已保存到 '员工信息及绩效表.xlsx' 文件中！")