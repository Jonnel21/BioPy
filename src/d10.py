from src.device.instrument import InstrumentStrategy
from src.peak import Peak


class D10Strategy(InstrumentStrategy):

    def get_type(self):
        """The type of instrument

        :return: A string literal
        :rtype: str
        """

        return "D-10"

    def which_version(self, nested_list: list):
        """Finds the version in the list.

        :param nested_list: A list containing info from a pdf file.
        :type nested_list: list
        :return: A string literal of the version.
        :rtype: str
        """

        if '5.00-2' in nested_list:
            return '5.00-2'
        elif '4.30-2' in nested_list:
            return '4.30-2'
        else:
            return '-1'

    def is_control(self, nested_list: list):
        """Determines if the list is a control report.

        :param nested_list: A list containing info from a pdf file.
        :type nested_list: list
        :return: A boolean value.
        :rtype: bool
        """

        if('Control' in nested_list):
            return True
        else:
            return False

    def check_edge_case(self, decoded_arr: list):
        """Looks for symbols such as: \"[<, 0.8, *]\" in the list,
        and concats them together.

        :param decoded_arr: A list containing info from a pdf file.
        :type decoded_arr: list
        """

        if '*' in decoded_arr:
            while '*' in decoded_arr:
                asterisk_index = decoded_arr.index('*')
                if decoded_arr[asterisk_index - 2] == '<':
                    lessthan_index = decoded_arr.index('<')
                    temp = "".join(decoded_arr[lessthan_index : asterisk_index + 1])
                    decoded_arr.insert(lessthan_index, temp)
                    del decoded_arr[decoded_arr.index('<') : decoded_arr.index('*') + 1]
                else:
                    temp_arr = decoded_arr[asterisk_index - 1 : asterisk_index + 1]
                    temp = "".join(temp_arr)
                    decoded_arr.insert(asterisk_index - 1, temp)
                    del decoded_arr[decoded_arr.index(temp, asterisk_index - 1, asterisk_index + 2) + 1 : decoded_arr.index(temp, asterisk_index - 1, asterisk_index + 2) + 3]
        elif '<' in decoded_arr:
            lessthan_index = decoded_arr.index('<')
            value_index = decoded_arr.index('<') + 1
            temp = "".join(decoded_arr[lessthan_index : value_index + 1])
            decoded_arr.insert(lessthan_index, temp)
            del decoded_arr[decoded_arr.index('<') : decoded_arr.index('<') + 2]
        else:
            pass

    def create_control_table_43(self, decoded_arr: list, info_table: list):
        """Populates the info table specific to control reports
        in version 4.30-2.

        :param decoded_arr: A list containing info from a pdf file.
        :type decoded_arr: list
        :param info_table: A list of the necessary headers from a pdf file.
        :type info_table: list
        :return: A populated list of necessary headers.
        :rtype: list
        """

        lot_id_index = decoded_arr.index('R.time') - 2
        lot_index = decoded_arr.index('Injection') - 1
        injection_date_index = lot_index + 3
        injection_time_index = injection_date_index + 1
        injection_index = decoded_arr.index('Method:') - 1
        racknum_index = decoded_arr.index('Rack') + 2
        rackpos_index = racknum_index + 3
        total_area_index = decoded_arr.index('Area:') + 1
        serial_index = decoded_arr.index('S/N:') + 1

        info_table.append(decoded_arr[lot_id_index])
        info_table.append(decoded_arr[lot_index])
        info_table.append(decoded_arr[injection_date_index])
        info_table.append(decoded_arr[injection_time_index])
        info_table.append(decoded_arr[injection_index])
        info_table.append(decoded_arr[racknum_index])
        info_table.append(decoded_arr[rackpos_index])
        info_table.append(decoded_arr[serial_index])
        info_table.append(decoded_arr[total_area_index])

        return info_table

    def parse_text(self, txt_file: str):
        """Reads a txt file and saves the strings in a dictionary.

        :param txt_file: path to txt file.
        :type txt_file: str
        :return: A dictionary with values from a pdf file
        :rtype: dict
        """

        arr = []
        with open(txt_file, 'rb') as f:

            info_table = []
            nested_table = []
            arr = f.read().split()
            decoded_arr = self.wrapper_decode(arr)

            self.check_edge_case(decoded_arr)

            if self.which_version(decoded_arr) == '4.30-2':
                if(self.is_control(decoded_arr)):

                    # 4.30 control specific
                    control_info = self.create_control_table_43(decoded_arr,
                                                                info_table)
                    start = decoded_arr.index('%')  # inclusive
                    end = decoded_arr.index('Total')  # exclusive
                    peak_table = decoded_arr[start + 1: end]

                    # create nested list
                    nested_table = self.to_nested(peak_table)
                    nested_table.insert(0, control_info)

                    # create dictionary
                    test_dict = self.map_to_dictionarc(nested_table)
                    f.close()
                    return test_dict

                # 4.30 patient specific
                injection_index = decoded_arr.index('Method:') - 1
                racknum_index = decoded_arr.index('Rack') + 2
                rackpos_index = racknum_index + 3

                # 5.00 patient specific
            if self.which_version(decoded_arr) == '5.00-2':
                injection_index = decoded_arr.index('D-10') - 1
                racknum_index = decoded_arr.index('Rack') + 2
                rackpos_index = decoded_arr.index('Bio-Rad') - 1

            # 4.30 & 5.00 patient
            sampleid_index = decoded_arr.index('ID:') + 1
            date_index = decoded_arr.index('date') + 1
            time_index = date_index + 1
            total_area_index = decoded_arr.index('Area:') + 1
            serial_index = decoded_arr.index('S/N:') + 1

            # peak table indicies for D-10 only
            start = decoded_arr.index('%')  # inclusive
            end = decoded_arr.index('Total')  # exclusive

            info_table.append(decoded_arr[sampleid_index])
            info_table.append(decoded_arr[date_index])
            info_table.append(decoded_arr[time_index])
            info_table.append(decoded_arr[injection_index])
            info_table.append(decoded_arr[racknum_index])
            info_table.append(decoded_arr[rackpos_index])
            info_table.append(decoded_arr[total_area_index])
            info_table.append(decoded_arr[serial_index])

            peak_table = decoded_arr[start + 1: end]

            # create nested list
            nested_table = self.to_nested(peak_table)
            nested_table.insert(0, info_table)

            # create dictionary
            test_dict = self.map_to_dictionary(nested_table)
            f.close()
            return test_dict

    def map_to_dictionary(self, nested_list: list):
        """Converts a nested list of peaks into a dictionary.

        :param nested_list: Values from a pdf file.
        :type nested_list: list
        :return: A dictionary with mappings from a pdf file.
        :rtype: dict
        """

        # print("This is the name: %s" % self.name)
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
                key_serial = "S/N"
                key_total_area = "Total Hb Area"
                real_dict.update([(key_sampleID, e[Peak.SAMPLE.value]),
                                 (key_date, e[Peak.DATE.value]),
                                 (key_time, e[Peak.TIME.value]),
                                 (key_injection, e[Peak.INJ.value]),
                                 (key_rack, e[Peak.RACK.value]),
                                 (key_rackpos, e[Peak.RACKPOS.value]),
                                 (key_serial, e[Peak.SERIAL.value]),
                                 (key_total_area, e[Peak.TOTALAREA.value]), ])
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

    def map_to_dictionarc(self, nested_list: list):
        """Converts a nested list of peaks into a dictionary.
        The dictionary created is specific to Control Reports.

        :param nested_list: Values from a pdf file.
        :type nested_list: list
        :return: A dictionary with mappings from a pdf file.
        :rtype: dict
        """

        peak_index = 0
        real_dict = {}
        for i, e in enumerate(nested_list):
            if(i == 0):

                key_LotID = "Lot ID"
                key_lot = "Lot #"
                key_date = "Date"
                key_time = "Time"
                key_injection = "Inj #"
                key_rack = "Rack #"
                key_rackpos = "Rack Position"
                key_total_area = "Total Hb Area"
                key_serial = "S/N"
                real_dict.update([(key_LotID, e[0]),
                                 (key_lot, e[1]),
                                 (key_date, e[2]),
                                 (key_time, e[3]),
                                 (key_injection, e[4]),
                                 (key_rack, e[5]),
                                 (key_rackpos, e[6]),
                                 (key_serial, e[Peak.SERIAL.value]),
                                 (key_total_area, e[8]), ])
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
