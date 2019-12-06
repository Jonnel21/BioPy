import tabula
import pandas as pd
import numpy as np

# Read pdf into DataFrame
df = tabula.read_pdf("test.pdf", multiple_tables=True, area=[[47.25,24.183,129.845,234.764],[472.876,27.0,581.514,304.549],[587.467,26.416,624.672,142.495]])

info = df[0].replace(np.nan, " ")
# peak = df[1].replace(np.nan, " ")
# result = df[2].replace(np.nan, " ")

sample_id = info[0:][0:1]
injection_date = info[0:][1:2]
sample_id.to_csv('C:\\Users\\Jonnel\\Documents\\BioPy\\test.csv', header=['test1','test2'], index=False)

injection_header = injection_date[0]
date_time = injection_date.at[1,1]

sample_header = sample_id.at[0,0]
barcode = sample_id.at[0,1]

# tester = sample_id.append(injection_date, ignore_index=True)
# print(tester)
# print(barcode)
# print(info)
# print(peak)
# print(result)
# print(sample_id)
# print(injection_date)
# print(injection_header)
# print(date_time)
# print(sample_header)
# print(barcode)

# csv_result = sample_id.assign(injection_header=date_time)
# print(csv_result)


# todo: parse text for specific keywords
df2 = pd.DataFrame({sample_header:barcode}, index=[0])
df3 = df2.assign(injection_header=date_time)
print(df3)

df3.to_csv('C:\\Users\\Jonnel\\Documents\\BioPy\\test.csv', index=False)
