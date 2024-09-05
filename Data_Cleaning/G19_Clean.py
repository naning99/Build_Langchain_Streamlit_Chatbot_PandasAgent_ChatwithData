import pandas as pd
import openpyxl

xls = pd.ExcelFile('Data/T_G19_18to22.xlsx')
df_2018 = pd.read_excel(xls, '2018')
df_2019 = pd.read_excel(xls, '2019')
df_2020 = pd.read_excel(xls, '2020')
df_2021 = pd.read_excel(xls, '2021')
df_2022 = pd.read_excel(xls, '2022')
df_clean_G19_18to22 = pd.concat([df_2018, df_2019, df_2020, df_2021, df_2022], ignore_index=True)
df_clean_G19_18to22.to_csv('Data/df_clean_G19_18to22.csv', index=False)