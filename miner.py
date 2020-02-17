import pdfminer.high_level as pdf
import PyPDF2
from pdfreader import SimplePDFViewer

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

def reader(str):
    file = open(str, 'rb')
    view = SimplePDFViewer(file)
    view.render()
    pdf = view.canvas.strings
    return pdf

reader('test1.pdf')
