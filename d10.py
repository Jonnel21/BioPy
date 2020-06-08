from instrument import InstrumentStrategy
from peak import Peak
import re
import os
import shutil
import subprocess
import pandas as pd
class D10Strategy(InstrumentStrategy):

    def convert_pdf(self, pdf_tuples: tuple):
        super().convert_pdf(pdf_tuples)

    def wrapper_decode(self, arr: list):
        return super().wrapper_decode(arr)

    def rename_unknown(self, lst: list):
        super().rename_unknown(lst)

    def to_nested(self, table: list):
        return super().to_nested(table)

    def sort_headers(self, x):
        return super().sort_headers(x)

    def map_to_dictionary(self, nested_list: list):
        return super().map_to_dictionary(nested_list)

    def build_csv(self, save_location: str):
        super().build_csv(save_location)

    def parse_text(self, txt_file):
        arr = []
        with open(txt_file, 'rb') as f:
            info_table = []
            nested_table = []
            temp = ""
            arr = f.read().split()
            decoded_arr = self.wrapper_decode(arr)

            # Checks for edge case characters
            if '*' in decoded_arr:
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
                    del decoded_arr[asterisk_index - 1 : asterisk_index + 1]
            elif '<' in decoded_arr:
                lessthan_index = decoded_arr.index('<')
                value_index = decoded_arr.index('<') + 1
                temp = "".join(decoded_arr[lessthan_index : value_index + 1])
                decoded_arr.insert(lessthan_index, temp)
                del decoded_arr[decoded_arr.index('<') : decoded_arr.index('<') + 2]
            else:
                pass

            # info table indicies
            sampleid_index = decoded_arr.index('ID:') + 1
            date_index = decoded_arr.index('date') + 1
            time_index = date_index + 1
            injection_index = decoded_arr.index('D-10') - 1
            racknum_index = decoded_arr.index('Rack') + 2
            rackpos_index = decoded_arr.index('Bio-Rad') - 1
        
            # peak table indicies for D-10 only
            start = decoded_arr.index('%') # inclusive
            end = decoded_arr.index('Total') # exclusive

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