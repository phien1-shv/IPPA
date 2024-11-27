#Sơ lược về dữ liệu# 

import pandas as pd
import numpy as np

# Đọc dữ liệu từ file CSV
df = pd.read_csv('ObesityDataSet_raw_and_data_sinthetic.csv')

num_rows, num_columns = df.shape
print(f'Dữ liệu có {num_rows-1} hàng dữ liệu  và {num_columns} cột dữ liệu\n')

print('Kiểu dữ liệu của từng cột:')
print(df.dtypes)  # Kiểu dữ liệu của từng cột
print()

df_numeric = list(df.select_dtypes(include=[np.number]))  # Lấy các cột có kiểu dữ liệu số

df_non_numeric =list(df.select_dtypes(exclude=[np.number]))  # Lấy các cột không phải số


print('Các cột với kiểu dữ liệu là số (int64):')
print(df_numeric)  # In ra tên các cột số

print()
print('Các cột với kiểu dữ liệu là object:')
print(df_non_numeric)  # In ra tên các cột không phải số