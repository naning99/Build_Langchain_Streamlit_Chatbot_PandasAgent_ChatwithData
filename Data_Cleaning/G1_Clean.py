import pandas as pd
import numpy as np
import openpyxl

G1_file_2018 = pd.read_excel('Data/T_G1_2018.xlsx', sheet_name = 0)
G1_file_2019 = pd.read_excel('Data/T_G1_2019.xlsx', sheet_name = 0)
G1_file_2020 = pd.read_excel('Data/T_G1_2020.xlsx', sheet_name = 0)
G1_file_2021 = pd.read_excel('Data/T_G1_2021.xlsx', sheet_name = 0)
G1_file_2022 = pd.read_excel('Data/T_G1_2022.xlsx', sheet_name = 0)

def clean_G1(df, FY):
    #Category
    cat = ['Accident & Health', 'Motor Vehicle', 'Aircraft', 'Ships', 'Goods in Transit', 'Property Damage', 'General Liability', 'Pecuniary Loss', 'Non-Proportional Treaty Reinsurance', 'Proportional Treaty Reinsurance', 'Total']
    print(len(cat))
    
    #Values
    start_index = df[df.iloc[:, 1].str.contains('Gross Premiums', na=False)].index[0]
    end_index = df[df.iloc[:, 1].str.contains('Underwriting Profit', na=False)].index[0]
    df_value_frame = df.iloc[start_index:end_index+1, 2:]
    df_value_frame_transpose = df_value_frame.transpose()
    print(df_value_frame_transpose.shape)

    #Metrics
    metrics_lst = df.iloc[start_index:end_index+1, 1].to_list()
    print(len(metrics_lst))

    #combine
    df_value_frame_transpose.columns = metrics_lst
    df_value_frame_transpose['Category'] = cat
    df_value_frame_transpose['FY'] = FY

    return df_value_frame_transpose

df_clean_2018 = clean_G1(G1_file_2018, '2018')
df_clean_2019 = clean_G1(G1_file_2019, '2019')
df_clean_2020 = clean_G1(G1_file_2020, '2020')
df_clean_2021 = clean_G1(G1_file_2021, '2021')
df_clean_2022 = clean_G1(G1_file_2022, '2022')
df_clean_G1_18to22 = pd.concat([df_clean_2018, df_clean_2019, df_clean_2020, df_clean_2021, df_clean_2022])
df_clean_G1_18to22.to_csv('Data/df_clean_G1_18to22.csv', index = False)




