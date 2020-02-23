import pdfminer.high_level as pdf
import PyPDF2
import pandas as pd
from pdfreader import SimplePDFViewer
from enum import Enum

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
    # del table[0::5] # delete peak names
    start = 0
    end = 5
    size = len(table) // 5
    output = []
    for e in range(size):
        print("Appending: %r to output" % table[start:end])
        output.append(table[start:end])
        start += 5
        end += 5
    return output
    # df = pd.DataFrame(output, peak_names)
    # print(df[Peak.A1A])
    # return df

nested_list = to_nested(reader('test.pdf'))
nested_list

# sorts unknowns to the end of the list
def sort_unknown(list):
    for i, e in enumerate(nested_list):
        print("Index: %r, Element: %r" % (i, e))

    for j, ls in enumerate(nested_list[i]):
        print("Index: %r, Element: %r" % (j, ls))
        
        if(ls == "Unknown"):
            temp = nested_list[i]
            del nested_list[i]
            nested_list.append(temp)



my_dict = dict(A1a_Rtime=123, A1a_Height=452345, A1a_Area=123354, A1a_Areap=34554,
                A1c_Rtime=123, A1c_height=897, A1c_Area=342, A1c_Areap=5635,
                )
# my_dict

# df = pd.DataFrame(my_dict, index=[0])
# df