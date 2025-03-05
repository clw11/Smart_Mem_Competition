import pandas as pd
import numpy as np
import os
input_dir = "parity"
output_dir = "parity"
ticket_file = "D:/competition_data/ticket.csv"
ticket_df = pd.read_csv(ticket_file)
ticket_df = ticket_df[ticket_df['sn_type'] == 'A']

# 1、 筛选出未在正常内存条中出现过的parity
df = pd.read_csv(f"{input_dir}/parity_analysis.csv")
df = df[df['normal'] == 0]
df = df[['Unnamed: 0']]
df.columns = ['uce_parity']
df['uce_parity'] = df['uce_parity'].astype(np.int64)
output_file = f"{output_dir}/uce_parity.csv" 
df.to_csv(output_file, index=False)
num1 = len(df)

# 2、 筛选出在正常内存条中对半出现的parity  (在故障/正常内存条中均仅出现过一次)
df = pd.read_csv(f"{input_dir}/parity_analysis.csv")
df = df[(df['normal'] == 1) & (df['fault'] == 1)]
df = df[['Unnamed: 0']]
df.columns = ['possible_uce_parity']
df['possible_uce_parity'] = df['possible_uce_parity'].astype(np.int64)
output_file = f"{output_dir}/possible_uce_parity.csv" 
df.to_csv(output_file, index=False)
num2 = len(df)

# 3、 按照f1_score 筛选parity
ticket_count = len(ticket_df)
df = pd.read_csv(f"{input_dir}/parity_analysis.csv")
df['recall'] = df['fault'] / ticket_count
df['precision'] =df['fault'] / (df['fault'] + df['normal'])
df['f1_score'] = 2 * df['recall'] * df['precision'] / (df['recall'] + df['precision'])
df = df.sort_values(by='f1_score', ascending=False)
df = df.head(int((num1 + num2) / 2))
df = df[['Unnamed: 0']]
df.columns = ['f1_score_uce_parity']
df['f1_score_uce_parity'] = df['f1_score_uce_parity'].astype(np.int64)
output_file = f"{output_dir}/f1_score_uce_parity.csv" 
df.to_csv(output_file, index=False)