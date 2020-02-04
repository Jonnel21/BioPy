import pdfminer.high_level as pdf

def test(str):
    text = pdf.extract_text(str)
    return text

report = test('file.pdf')
