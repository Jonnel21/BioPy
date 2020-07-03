from instrument import InstrumentStrategy as instrument

class TestConvert:
    def test_happy_path(self):
        test_tuples = ('C:/Users/Jonnel/Desktop/BioPy/pdf/d10/19BMTA2306_9-9-3-2-2020-RA1.pdf', 'C:/Users/Jonnel/Desktop/BioPy/pdf/d10/19BMTA2308_8-8-3-2-2020-RA1.pdf')
        instrument.convert_pdf(self, test_tuples)
        assert 1