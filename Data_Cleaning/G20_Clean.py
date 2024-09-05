import pandas as pd
import numpy as np
import openpyxl

#only check first sheet: Direct & Reinsurance Inward Business
G20_file_2018 = pd.read_excel('Data/T_G20_2018.xlsx', sheet_name = 0)
G20_file_2019 = pd.read_excel('Data/T_G20_2019.xlsx', sheet_name = 0)
G20_file_2020 = pd.read_excel('Data/T_G20_2020.xlsx', sheet_name = 'G20a')
G20_file_2021 = pd.read_excel('Data/T_G20_2021.xlsx', sheet_name = 0)
G20_file_2022 = pd.read_excel('Data/T_G20_2022.xlsx', sheet_name = 0)

def clean_premium(df, FY):
    #Insurers
    lst_insurer = df.iloc[:, 1].unique().tolist()
    lst_insurer.remove('Insurer')
    lst_insurer.remove(np.nan)
    print(len(lst_insurer))
    
    #Category
    cat = ['Accident & Health', 'Motor Vehicle', 'Aircraft', 'Ships', 'Goods in Transit', 'Property Damage', 'Employees Compensation', 'Owners Corporation Liability', 'Other Business', 'Pecuniary Loss', 'Non-Proportional Treaty Reinsurance', 'Proportional Treaty Reinsurance', 'Total']
    print(len(cat))
    
    #Values
    start_index = df[df.iloc[:, 1] == 'ABCI'].index[0]
    end_index = df[df.iloc[:, 1] == 'Zurich Insurance'].index[0]
    df_value_frame = df.iloc[start_index:end_index+1, 4:]
    print(df_value_frame.shape)
    
    #Combine
    df_value_transform = pd.DataFrame(columns = ['Gross Premium', 'Net Premium'])
    for i, row in df_value_frame.iterrows():
        gross_premium = row.iloc[::2].tolist()
        net_premium = row.iloc[1::2].tolist()
        cur_insurer_value = pd.DataFrame({'Gross Premium': gross_premium, 'Net Premium': net_premium})
        df_value_transform = pd.concat([df_value_transform, cur_insurer_value], ignore_index=True)
    df_value_transform['Insurer'] = [insurer for insurer in lst_insurer for _ in range(len(cat))]
    df_value_transform['Category'] = cat*len(lst_insurer)
    df_value_transform['FY'] = FY
    df_value_transform = df_value_transform[['Insurer', 'FY', 'Category', 'Gross Premium', 'Net Premium']]
    return df_value_transform

df_clean_2018 = clean_premium(G20_file_2018, '2018')
df_clean_2019 = clean_premium(G20_file_2019, '2019')
df_clean_2020 = clean_premium(G20_file_2020, '2020')
df_clean_2021 = clean_premium(G20_file_2021, '2021')
df_clean_2022 = clean_premium(G20_file_2022, '2022')

df_clean_G20_18to22 = pd.concat([df_clean_2018, df_clean_2019, df_clean_2020, df_clean_2021, df_clean_2022])
df_clean_G20_18to22.to_csv('Data/df_clean_G20_18to22.csv')


