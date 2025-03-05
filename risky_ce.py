import pandas as pd
import numpy as np
import os
from tqdm import tqdm
dataset_dir = "D:/stage1_feather/type_A"
ticket_file = "D:/competition_data/ticket.csv"

ticket_df = pd.read_csv(ticket_file)
ticket_df = ticket_df[ticket_df['sn_type'] == 'A']
sn_names = ticket_df['sn_name'].unique()

output_dir = "parity"
os.makedirs(output_dir, exist_ok=True)

# 使用字典保存retryRdErrLogParity不同值出现在不同SN的次数
fault_parity_dict = {}
for sn_name in tqdm(sn_names, desc="Processing Falut SN Names"):
    file_path = f"{dataset_dir}/{sn_name}.feather"
    sn_df = pd.read_feather(file_path)
    manufacturer = sn_df['Manufacturer'].iloc[0]
    retry_parity = sn_df['RetryRdErrLogParity'].unique()
    # 排除NaN或空值
    retry_parity = [val for val in retry_parity if val not in [None, ""] and not pd.isna(val)]
    if not retry_parity:  # 如果处理后列表为空，则跳过
        continue

    # 遍历整个retry_parity列，统计不同值出现的次数
    for i in range(len(retry_parity)):
        if retry_parity[i] in fault_parity_dict:
            fault_parity_dict[retry_parity[i]] += 1
        else:
            fault_parity_dict[retry_parity[i]] = 1

# 保存故障SN的retryRdErrLogParity统计结果
output_file = f"{output_dir}/fault_parity_analysis.csv"
fault_parity_df = pd.DataFrame(fault_parity_dict, index=['faulty']).T
fault_parity_df.to_csv(output_file)

# 读取所有正常SN文件
normal_parity_dict = {}
for file in tqdm(os.listdir(dataset_dir), desc="Processing Normal SN Names"):
    file_path = f"{dataset_dir}/{file}"
    sn_df = pd.read_feather(file_path)
    sn_name = os.path.basename(file_path).split('.')[0]
    # 仅针对正常内存条进行分析
    if sn_name in sn_names:
        continue
    manufacturer = sn_df['Manufacturer'].iloc[0]

    retry_parity = sn_df['RetryRdErrLogParity'].unique()

    # 遍历整个retry_parity列，统计不同值出现的次数
    for i in range(len(retry_parity)):
        if retry_parity[i] not in fault_parity_dict:
            continue
        if retry_parity[i] in normal_parity_dict:
            normal_parity_dict[retry_parity[i]] += 1
        else:
            normal_parity_dict[retry_parity[i]] = 1
# 合并故障和正常SN的统计结果
combined_parity_dict = {}
for key in set(fault_parity_dict.keys()):
    combined_parity_dict[key] = {
        'faulty': fault_parity_dict.get(key, 0),
        'normal': normal_parity_dict.get(key, 0)
    }
# 结果保存为.csv文件
output_file = f"{output_dir}/parity_analysis.csv"
combined_parity_df = pd.DataFrame(combined_parity_dict).T
combined_parity_df.to_csv(output_file)



