import PyPDF2
import re
import pdfminer.high_level as pdf
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

#pdfreader
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

# creates a nested list from the peak table
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

# renames unknown peaks
def rename_unknown(lst):
    if(Peak.UNKNOWN.value in lst):
        num_unknown = lst.count(Peak.UNKNOWN.value)
        if(num_unknown >= 2):
            for i in range(num_unknown):
                lst[lst.index("Unknown")] += str(i+1)
    else: print("There are no %ss in the list." % Peak.UNKNOWN.value)


my_dict = dict(A1a_Rtime=123, A1a_Height=452345, A1a_Area=123354, A1a_Areap=34554,
                A1c_Rtime=123, A1c_height=897, A1c_Area=342, A1c_Areap=5635,
                )
# my_dict

# df = pd.DataFrame(my_dict, index=[0])
# df

nested_list = to_nested(reader('test.pdf'))
nested_list
