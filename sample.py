import tabula

# Read pdf into DataFrame
# df = tabula.read_pdf("test.pdf", pages='all')

# Read remote pdf into DataFrame
def test():
    pdf_path = "https://github.com/chezou/tabula-py/raw/master/tests/resources/data.pdf"
    df2 = tabula.read_pdf(pdf_path)
    return df2

test()