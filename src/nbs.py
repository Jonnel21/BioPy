from device.instrument import InstrumentStrategy
from peak import Peak


class NbsStrategy(InstrumentStrategy):

    def getType(self):
        """The type of instrument

        :return: A string literal
        :rtype: str
        """

        return "VARIANTnbs"

    def parse_text(self, text_file: str):
        arr = []
        with open(text_file, 'rb') as f:
            offset = 5
            info_table = []
            nested_table = []
            arr = f.read().split()
            decoded_arr = self.wrapper_decode(arr)

            # delete peak numbers that appear in VNBS
            peak_start = decoded_arr.index('(min)') + 1
            peak_end = decoded_arr.index('Pattern:') - offset
            del decoded_arr[peak_start: peak_end: 6]

            # info table indicies
            sampleid_index = decoded_arr.index('ID:') + 1
            date_index = decoded_arr.index('Run') - 2
            time_index = date_index + 1
            injection_index = decoded_arr.index('Injection') + 2
            racknum_index = decoded_arr.index('Well#:') + 1
            rackpos_index = decoded_arr.index('Position:') + 1
            total_area_index = decoded_arr.index('Area:') + 1
            pattern_index = decoded_arr.index('Pattern:') + 1

            # peak table indicies for VNBS only
            start = decoded_arr.index('(min)')  # inclusive
            end = decoded_arr.index('Pattern:')  # exclusive

            info_table.append(decoded_arr[sampleid_index])
            info_table.append(decoded_arr[date_index])
            info_table.append(decoded_arr[time_index])
            info_table.append(decoded_arr[injection_index])
            info_table.append(decoded_arr[racknum_index])
            info_table.append(decoded_arr[rackpos_index])
            info_table.append(decoded_arr[total_area_index])
            info_table.append(decoded_arr[pattern_index])

            peak_table = decoded_arr[start + 1: end]

            # create nested list
            nested_table = self.to_nested(peak_table)
            nested_table.insert(0, info_table)

            # create dictionary
            test_dict = self.map_to_dictionary(nested_table)
            f.close()
        return test_dict

    def map_to_dictionary(self, nested_list: list):

        '''
        Converts a nested list of peaks into a dictionary.

        e.g.
        [['A1a', '0.20', '14061', '55103', '1.4'],
         ['A1b', '0.27', '24345', '117458', '3.0'],
         ['F', '0.49', '2183', '24521', '<0.8*'],
         ['LA1c/CHb-1', '0.69', '5293', '32276', '0.8']]
         ------------------------------------------------
        {'A1a_rtime': '0.20', 'A1a_height': '14061', 'A1a_area': '55103', 'A1a_areap': '1.4',
         'A1b_rtime': '0.27', 'A1b_height': '24345', 'A1b_area': '117458', 'A1b_areap': '3.0',
         'F_rtime': '0.49', 'F_height': '2183', 'F_area': '24521', 'F_areap': '<0.8*',
         'LA1c/CHb-1_rtime': '0.69', 'LA1c/CHb-1_height': '5293', 'LA1c/CHb-1_area': '32276', 'LA1c/CHb-1_areap': '0.8'}

         Parameters:
            nested_list: list

        Returns:
            real_dict: dict
        '''
        peak_index = 0
        real_dict = {}
        for i, e in enumerate(nested_list):
            if(i == 0):
                key_sampleID = "Sample_ID"
                key_date = "Date"
                key_time = "Time"
                key_injection = "Inj #"
                key_rack = "Well #"
                key_rackpos = "Plate Position"
                key_total_area = "Total Hb Area"
                key_pattern = "Pattern"
                real_dict.update([(key_sampleID, e[Peak.SAMPLE.value]),
                                  (key_date, e[Peak.DATE.value]),
                                  (key_time, e[Peak.TIME.value]),
                                  (key_injection, e[Peak.INJ.value]),
                                  (key_rack, e[Peak.RACK.value]),
                                  (key_rackpos, e[Peak.RACKPOS.value]),
                                  (key_total_area, e[Peak.TOTALAREA.value]),
                                  (key_pattern, e[Peak.PATTERN.value])])

                continue

            key_rtime = "%s_rtime" % e[peak_index]  # key retention time
            key_height = "%s_height" % e[peak_index]  # key height
            key_area = "%s_area" % e[peak_index]  # key area
            key_areap = "%s_areap" % e[peak_index]  # key area percent

            real_dict.update([(key_rtime, e[Peak.RTIME.value]),
                             (key_height, e[Peak.HEIGHT.value]),
                             (key_area, e[Peak.AREA.value]),
                             (key_areap, e[Peak.AREAP.value])])

        print(real_dict)
        return real_dict
