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

# PDF Miner
def test(str):
    text = pdf.extract_text(str)
    list = text.split()
    return list

# report = test('test1.pdf')

# PyPDF2
def test2(f):
    file = PyPDF2.PdfFileReader(f)
    text = file.getPage(0).extractText()
    list = text.split()
    return list

# report1 = test2('test1.pdf')

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

# creates a nested list from the peak table
def to_nested(table):
    peak_names = table[0::5]

    cnt = Counter(peak_names)
    print(cnt)
    # del table[0::5] # delete peak names
    #rename_unknown(table)
    start = 0
    end = 5
    size = len(table) // 5
    output = []
    for e in range(size):
        print(e)
        print("Appending: %r to output" % table[start:end])
        output.append(table[start:end])
        start += 5
        end += 5
    return output
    # df = pd.DataFrame(output, peak_names)
    # print(df[Peak.A1A])
    # return df

# renames unknown peaks
def rename_unknown(list):
    if(Peak.UNKNOWN.value in list):
        num_unknown = list.count(Peak.UNKNOWN.value)
        if(num_unknown >= 2):
            for i in range(num_unknown):
                list[list.index("Unknown")] += str(i+1)
    else: print("There are no %ss in the list." % Peak.UNKNOWN.value)

# sorts unknowns to the end of the list
# TODO: Optimize algorithm!
# TODO: Exit sort when algorithm finishes sorting unknowns
# TODO: Add a counter to exit algorithm early
# TODO: add check when unknown are sorted already
def sort_unknown(peak_table):
    flatten = list(it.chain.from_iterable(peak_table)) # flatten list
    cnt = Counter(flatten[0::5])
    num_unknown = cnt["Unknown"]
    for i, e in enumerate(peak_table):
        if(num_unknown == 0):
            break
        print("Index: %r, Element: %r" % (i, e))
        match = re.search('^Unknown\d', e[0])
        if(e[0] == Peak.UNKNOWN.value):
            temp = peak_table[i]
            del peak_table[i]
            peak_table.append(temp)
            num_unknown -= 1

    return peak_table

my_dict = dict(A1a_Rtime=123, A1a_Height=452345, A1a_Area=123354, A1a_Areap=34554,
                A1c_Rtime=123, A1c_height=897, A1c_Area=342, A1c_Areap=5635,
                )
# my_dict

# df = pd.DataFrame(my_dict, index=[0])
# df

nested_list = to_nested(reader('test.pdf'))
nested_list
sort_unknown(nested_list)