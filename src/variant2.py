from device.instrument import InstrumentStrategy
from peak import Peak


class VariantStrategy(InstrumentStrategy):

    def isA1c(self, nested_list):

        '''
        Helper method to determine if the list is strictly A1c
        '''

        if((Peak.V2A1CNU.value in nested_list[0]) or (Peak.V2TURBOA1C.value in nested_list[0])):
            return True
        else:
            return False

    def parse_text(self, txt_file):
        arr = []
        with open(txt_file, 'rb') as f:
            info_table = []
            nested_table = []
            arr = f.read().split()
            decoded_arr = self.wrapper_decode(arr)

            # info table indicies
            sampleid_index = decoded_arr.index('ID:') + 1
            date_index = decoded_arr.index('Performed:') + 1
            time_index = date_index + 1
            injection_index = decoded_arr.index('Name:') - 1
            racknum_index = decoded_arr.index('Physician:') - 1
            rackpos_index = decoded_arr.index('DOB:') - 1
            total_area_index = decoded_arr.index('Area:') + 1
            type_index = Peak.TYPE.value

            # peak table indicies for Varient systems only
            start = decoded_arr.index('(min)') + 2  # inclusive
            if(('*Values' in decoded_arr) and (('V2_A1c_NU' in decoded_arr) or ('V2TURBO_A1C_2.0' in decoded_arr))):
                end = decoded_arr.index('*Values')  # exclusive
            else:
                end = decoded_arr.index('Total')  # exclusive

            if('SAMP' in decoded_arr):
                info_table.append(decoded_arr[sampleid_index] + decoded_arr[sampleid_index + 1])
            else:
                info_table.append(decoded_arr[sampleid_index])

            info_table.append(decoded_arr[date_index])
            info_table.append(decoded_arr[time_index])
            info_table.append(decoded_arr[injection_index])
            info_table.append(decoded_arr[racknum_index])
            info_table.append(decoded_arr[rackpos_index])
            info_table.append(decoded_arr[total_area_index])
            info_table.append(decoded_arr[type_index])

            peak_table = decoded_arr[start: end]

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
                key_rack = "Rack #"
                key_rackpos = "Rack Position"
                key_total_area = "Total Hb Area"
                real_dict.update([(key_sampleID, e[Peak.SAMPLE.value]),
                                 (key_date, e[Peak.DATE.value]),
                                 (key_time, e[Peak.TIME.value]),
                                 (key_injection, e[Peak.INJ.value]),
                                 (key_rack, e[Peak.RACK.value]),
                                 (key_rackpos, e[Peak.RACKPOS.value]),
                                 (key_total_area, e[Peak.TOTALAREA.value])])
                continue
            if(self.isA1c(nested_list)):
                key_ngsp = "%s_ngsp" % e[peak_index]
                key_areap = "%s_areap" % e[peak_index]
                key_rtime = "%s_rtime" % e[peak_index]
                key_area = "%s_area" % e[peak_index]

                real_dict.update([(key_ngsp, e[Peak.NGSP.value]),
                                 (key_areap, e[Peak.V2_AREAP.value]),
                                 (key_rtime, e[Peak.V2_RTIME.value]),
                                 (key_area, e[Peak.V2_AREA.value])])
            else:
                key_calibrated_area = "%s_calareap" % e[peak_index]  # key calibrated area percent
                key_areap = "%s_areap" % e[peak_index]  # key area percent
                key_rtime = "%s_rtime" % e[peak_index]  # key retention time
                key_area = "%s_area" % e[peak_index]  # key area

                real_dict.update([(key_calibrated_area, e[Peak.CALAREA.value]),
                                 (key_areap, e[Peak.V2_AREAP.value]),
                                 (key_rtime, e[Peak.V2_RTIME.value]),
                                 (key_area, e[Peak.V2_AREA.value])])

        print(real_dict)
        return real_dict
