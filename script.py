import tabula

# Read pdf into DataFrame
df = tabula.read_pdf("test.pdf", multiple_tables=True, area=[[47.25,24.183,129.845,234.764],[472.876,27.0,581.514,304.549],[587.467,26.416,624.672,142.495]])

print(df)

# todo: parse text for specific keywords