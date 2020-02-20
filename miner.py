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
    del table[0::5] # delete peak names
    start = 0
    end = 4
    size = len(table) // 4
    output = []
    for e in range(size):
        print("Appending: %r to output" % table[start:end])
        output.append(table[start:end])
        start += 4
        end += 4

    df = pd.DataFrame(output, peak_names, columns=['R.time', 'Height', 'Area', 'Area %'])
    return df

to_nested(reader('test.pdf'))
