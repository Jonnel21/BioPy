from instrument import InstrumentStrategy

class TestRenameUnknown:
    def test_happy_path(self):
        instrument = InstrumentStrategy()
        _list = ['one', 'two', 'three', 'Unknown']
        expected_list = ['one', 'two', 'three', 'Unknown1']
        test_list = instrument.rename_unknown(_list)
        assert test_list == expected_list