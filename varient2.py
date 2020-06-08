from instrument import InstrumentStrategy
from peak import Peak
import re
import os
import shutil
import subprocess
import pandas as pd
class VarientStrategy(InstrumentStrategy):

    def convert_pdf(self, pdf_tuples: tuple):
        super().convert_pdf(pdf_tuples)
        
    def rename_unknown(self, lst: list):
        super().rename_unknown(lst)

    def wrapper_decode(self, arr: list):
        return super().wrapper_decode(arr)
    
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

            # info table indicies
            sampleid_index = decoded_arr.index('ID:') + 1
            date_index = decoded_arr.index('Performed:') + 1
            time_index = date_index + 1
            injection_index = decoded_arr.index('Name:') - 1
            racknum_index = decoded_arr.index('Physician:') - 1
            rackpos_index = decoded_arr.index('DOB:') - 1
        
            # peak table indicies for Varient systems only
            start = decoded_arr.index('(min)') + 2 # inclusive
            if(('*Values' in decoded_arr) and (('V2_A1c_NU' in decoded_arr) or ('V2TURBO_A1C_2.0' in decoded_arr))):
               end = decoded_arr.index('*Values') # exclusive
            else:
               end = decoded_arr.index('Total') # exclusive

            if('SAMP' in decoded_arr):
               info_table.append(decoded_arr[sampleid_index] + decoded_arr[sampleid_index + 1])
            else:
                  info_table.append(decoded_arr[sampleid_index])

            info_table.append(decoded_arr[date_index])
            info_table.append(decoded_arr[time_index])
            info_table.append(decoded_arr[injection_index])
            info_table.append(decoded_arr[racknum_index])
            info_table.append(decoded_arr[rackpos_index])

            peak_table = decoded_arr[start: end]

            # create nested list
            nested_table = self.to_nested(peak_table)
            nested_table.insert(0, info_table)

            # create dictionary
            test_dict = self.map_to_dictionary(nested_table)
            f.close()
        return test_dict