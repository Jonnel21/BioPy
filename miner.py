import pdfminer.high_level as pdf
import PyPDF2
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

def parse(table):
    
reader('test.pdf')

