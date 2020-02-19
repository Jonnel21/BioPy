import tabula
import pandas as pd
import numpy as np

# Read pdf into DataFrame
df = tabula.read_pdf("test.pdf", multiple_tables=True, 
area=[[47.25,24.183,129.845,234.764],[487.013,20.463,567.376,294.292],[587.467,26.416,624.672,142.495]])

info = df[0].replace(np.nan, " ")
peak = df[1].replace(np.nan, " ")
# result = df[2].replace(np.nan, " ")

sample_id = info[0:][0:1]
injection_date = info[0:][1:2]
rack_pos_list = info.at[3,1].split(': ')
# sample_id.to_csv('C:\\Users\\Jonnel\\Documents\\BioPy\\test.csv', header=['test1','test2'], index=False)

# Injection Date/Time
injection_header = injection_date[0]
date_time = injection_date.at[1,1]
injection = info.at[2,0]

# Sample ID
sample_header = sample_id.at[0,0]
barcode = sample_id.at[0,1]


# tester = sample_id.append(injection_date, ignore_index=True)
# print(tester)
# print(barcode)
# print(info)
# print(rack_pos_list)
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
# print(info)
injection_list = injection.split(': ')
# print(injection_list)

# Special case parsing for injection number
injection_h = injection_list[0]
injection_number = injection_list[1]

# Special case parsing for Rack position
rack_pos_h = rack_pos_list[0]
rack_pos = rack_pos_list[1]

# Possible Peak variables
A1a_list = peak.iloc[0]
A1a_ht = peak.at[2,1]
A1a_area = peak.at[3,1]
A1a_areap = peak.at[4,1]
print(A1a_rt)
# print(A1a_ht)
# print(A1a_area)
# print(A1a_areap)
# print(peak)

# todo: parse text from peak table
df2 = pd.DataFrame({sample_header:barcode}, index=[0])
df3 = df2.assign(injection_date=date_time, 
                injection_number=injection_number, 
                rack_position=rack_pos,
                A1a_retention_time=A1a_rt,
                )
# print(df3)

df3.to_csv('C:\\Users\\Jonnel\\Documents\\BioPy\\test.csv', index=False)
