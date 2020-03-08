#%%
import re
import os
import pandas as pd
import itertools as it
from pdfreader import SimplePDFViewer
from enum import Enum
from collections import Counter

class Peak(Enum):
    RTIME = 1
    HEIGHT = 2
    AREA = 3
    AREAP = 4
    UNKNOWN = "Unknown"
    VARIANT_WINDOW = "Variant-Window"
    A1A = "A1a"
    A1B = "A1b"
    F = "F"
    LA1C = "LA1c/CHb-1"
    A1C = "A1c"
    P3 = "P3"
    A0 = "A0"

# Parse pdf and returns peak table
def reader(str):
    file = open(str, 'rb')
    view = SimplePDFViewer(file)
    view.render()
    pdf = view.canvas.strings
    start = pdf.index('Area % ') # inclusive
    end = pdf.index('Total Area: ') # exclusive
    peak_table = pdf[start + 1 : end]

    sampleID_index = pdf.index('Sample ID:')
    peak_index = pdf.index('Peak ')
    info_table = pdf[sampleID_index : peak_index]
    extracted_info = info_table[1:4:2] + info_table[4:7:2] + info_table[7:8]

    return extracted_info + peak_table

# Helper function for sorted
def unk_last(x):
    match = re.search('^Unknown\d', x)
    info_match = re.match('Sample|Date|Inj|Rack', x)
    if(info_match):
         return -1
    elif(match):
        return 1
    else: return 0

# Creates a nested list from the peak table
def to_nested(table):
    #del table[0::5] # delete peak names
    rename_unknown(table)
    start = 0
    end = 5
    size = len(table) // 5
    output = []
    for e in range(size):
        print("Appending: %r to output" % table[start:end])
        output.append(table[start:end])
        start += 5
        end += 5
    sorted_list = sorted(output, key= lambda x:unk_last(x[0]))
    return sorted_list

# Helper function to rename unknown peaks
def rename_unknown(lst):
    if(Peak.UNKNOWN.value in lst):
        num_unknown = lst.count(Peak.UNKNOWN.value)
        for i in range(num_unknown):
            lst[lst.index("Unknown")] += str(i+1)
    else: print("There are no %ss in the list." % Peak.UNKNOWN.value)

def map_func(e):
    # access each element
    # assign a key  for each value
    new_dict = {}

    key_rtime = e[0] + "_rtime" # key retention time
    key_height = e[0] + "_height" # key height
    key_area = e[0] + "_area" # key area
    key_areap = e[0] + "_areap" # key area percent

    key_rtime
    key_height
    key_area
    key_areap

# Maps 2d array into a dictionary
def map_to_dictionary(nested_list):
    header_index = 0
    peak_index = 0
    real_dict = {}
    for i, e in enumerate(nested_list):
        if(i == 0):
            key_sampleID = "Sample_ID" 
            key_date = "Date" 
            key_injection = "Inj #"
            key_rack = "Rack #"
            key_rackpos = "Rack Position"
            real_dict.update([(key_sampleID, e[0]), (key_date, e[1]),
                            (key_injection, e[2]), (key_rack, e[3]),
                            (key_rackpos, e[4])])
            i += 1
            continue

        # result = map(map_func, nested_list)

        key_rtime = "%s_rtime" % e[peak_index] # key retention time
        key_height = "%s_height" % e[peak_index] # key height
        key_area = "%s_area" % e[peak_index] # key area
        key_areap = "%s_areap" % e[peak_index] # key area percent

        real_dict.update([(key_rtime, e[Peak.RTIME.value]), (key_height, e[Peak.HEIGHT.value]),
                        (key_area, e[Peak.AREA.value]), (key_areap, e[Peak.AREAP.value])])

    return real_dict

# df = pd.DataFrame(real_dict, index = [0])
# df
# df.to_csv("test.csv")

# Open multiple PDF'S
# with os.scandir("Result\\") as it:
#     for entry in it:
#         peak_table = [] 
#         if not entry.name.startswith(".") and entry.is_file():
#             print("Opening: " + entry.path)
#             peak_table = reader(entry.path)
#             nested_list = to_nested(peak_table)

# nested_list = to_nested(reader('test.pdf'))
# nested_list

# peak_table1 = map_to_dictionary(to_nested(reader('Result\\Test_1.pdf')))
# peak_table2 = map_to_dictionary(to_nested(reader('Result\\Test_2.pdf')))
# df1 = pd.DataFrame(peak_table1, index=[0])
# df2 = pd.DataFrame(peak_table2, index=[0])
# result = df1.append(df2)
# result.to_csv("Append.csv")

# Empty dataframe
df = pd.DataFrame()

# Loop through result folder
with os.scandir("Test_PDF\\") as it:
    df = df.append([map_to_dictionary(to_nested(reader(entry))) for entry in it],
                    ignore_index=False, sort=False)
# df.to_csv("Append1.csv")
header_list = list(df.columns.values)
sorted_header_list = sorted(header_list, key= lambda x:unk_last(x))
df2 = df.reindex(columns=sorted_header_list)
df2.to_csv("Append3.csv")
#     for entry in it:
#         peak_table = [] 
#         if not entry.name.startswith(".") and entry.is_file():
#             print("Opening: " + entry.path)
#             peak_table = map_to_dictionary(to_nested(reader('test.pdf')))



# %%
