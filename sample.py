import tabula

# Read pdf into DataFrame
# df = tabula.read_pdf("test.pdf", pages='all')

# Read remote pdf into DataFrame
pdf_path = "https://github.com/chezou/tabula-py/raw/master/tests/resources/data.pdf"
df2 = tabula.read_pdf(pdf_path)
print(df2)

