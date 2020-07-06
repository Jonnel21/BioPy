from device.instrument import InstrumentStrategy


class NbsStrategy(InstrumentStrategy):

    def parse_text(self, text_file: str):
        arr = []
        with open(text_file, 'rb') as f:
            offset = 5
            info_table = []
            nested_table = []
            arr = f.read().split()
            decoded_arr = self.wrapper_decode(arr)

            # delete peak numbers that appear in VNBS
            peak_start = decoded_arr.index('1')
            peak_end = decoded_arr.index('Pattern:') - offset
            del decoded_arr[peak_start: peak_end: 6]

            # info table indicies
            sampleid_index = decoded_arr.index('ID:') + 1
            date_index = decoded_arr.index('Run') - 2
            time_index = date_index + 1
            injection_index = decoded_arr.index('Injection') + 2
            racknum_index = decoded_arr.index('Well#:') + 1
            rackpos_index = decoded_arr.index('Position:') + 1

            # peak table indicies for VNBS only
            start = decoded_arr.index('(min)')  # inclusive
            end = decoded_arr.index('Pattern:')  # exclusive

            info_table.append(decoded_arr[sampleid_index])
            info_table.append(decoded_arr[date_index])
            info_table.append(decoded_arr[time_index])
            info_table.append(decoded_arr[injection_index])
            info_table.append(decoded_arr[racknum_index])
            info_table.append(decoded_arr[rackpos_index])

            peak_table = decoded_arr[start + 1: end]

            # create nested list
            nested_table = self.to_nested(peak_table)
            nested_table.insert(0, info_table)

            # create dictionary
            test_dict = self.map_to_dictionary(nested_table)
            f.close()
        return test_dict
