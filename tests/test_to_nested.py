from instrument import InstrumentStrategy

class TestToNested:
    def test_happy_path(self):
        instrument = InstrumentStrategy()
        test_list = ['A1c', '23', '234', '23425', '3252', 'Unknown', '23', '234', '23425', '3252']
        expected_list =[
            ['A1c', '23', '234', '23425', '3252'],
            ['Unknown1', '23', '234', '23425', '3252']
        ]
        _list = instrument.to_nested(test_list)
        assert _list == expected_list