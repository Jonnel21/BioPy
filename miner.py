import re
import os
import pandas as pd
import itertools as it
from pdfreader import SimplePDFViewer
from enum import Enum
from collections import Counter

class Peak(Enum):
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
    
    return peak_table

# Helper function for sorted
def unk_last(x):
    match = re.search('^Unknown\d', x)
    if(match):
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
    real_dict = {}
    for i, e in enumerate(nested_list):
    
        # result = map(map_func, nested_list)
        key_rtime = "%s_rtime" % e[0] # key retention time
        key_height = "%s_height" % e[0] # key height
        key_area = "%s_area" % e[0] # key area
        key_areap = "%s_areap" % e[0] # key area percent

    # real_dict.update({key_rtime:e[1]}, {key_height:e[2]},
    #                 {key_area:e[3]}, {key_areap:e[4]})

        real_dict.update([(key_rtime, e[1]), (key_height, e[2]),
                        (key_area, e[3]), (key_areap, e[4])])

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

peak_table1 = map_to_dictionary(to_nested(reader('Result\\Test_1.pdf')))
peak_table2 = map_to_dictionary(to_nested(reader('Result\\Test_2.pdf')))
df1 = pd.DataFrame(peak_table1, index=[0])
df2 = pd.DataFrame(peak_table2, index=[0])
result = df1.append(df2)
result.to_csv("Append.csv")

# Empty dataframe

# with os.scandir("Result\\") as it:
#     for entry in it:
#         peak_table = [] 
#         if not entry.name.startswith(".") and entry.is_file():
#             print("Opening: " + entry.path)
#             peak_table = map_to_dictionary(to_nested(reader('test.pdf')))
            



