from instrument import InstrumentStrategy
from peak import Peak
import re
import os
import shutil
import subprocess
import pandas as pd
class D10Strategy(InstrumentStrategy):

    def convert_pdf(self, pdf_tuples: tuple):
        try:
            os.mkdir('txt_files')
        except FileExistsError:
            shutil.rmtree('txt_files')
            os.mkdir('txt_files')

        #with os.scandir(f'{pdf_location}') as it:
        for i in pdf_tuples:
            tmp_arr = i.split('/')
            pdf_file = tmp_arr[len(tmp_arr) - 1]
            name = os.path.splitext(pdf_file)[0] # returns filename without extenstion
            with open(f"./txt_files/{name}.txt", 'x') as file:
                subprocess.run(['pdftotext', '-simple', f'{i}', '-'], stdout=file)
                file.close()

    def rename_unknown(self, lst: list):
        if(Peak.UNKNOWN.value in lst):
            num_unknown = lst.count(Peak.UNKNOWN.value)
            for i in range(num_unknown):
                lst[lst.index("Unknown")] += str(i+1)
        else: print("There are no %ss in the list." % Peak.UNKNOWN.value)

    def wrapper_decode(self, arr: list):
        newarr = []
        for a in arr:
            newarr.append(a.decode())
        return newarr
    
    def to_nested(self, table: list):
        self.rename_unknown(table)
        start = 0
        end = 5
        size = len(table) // 5
        output = []
        for e in range(size):
            print("Appending: %r to output" % table[start:end])
            output.append(table[start:end])
            start += 5
            end += 5
        return output

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

    def sort_headers(self, x):
        unknown_match = re.search('^Unknown\d', x)
        info_match = re.match('Sample|Date|Time|Inj|Rack', x)
        if(info_match):
            return -1
        elif(unknown_match):
            return 1
        else: return 0

    def map_to_dictionary(self, nested_list: list):
        header_index = 0
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
                real_dict.update([(key_sampleID, e[Peak.SAMPLE.value]),
                                (key_date, e[Peak.DATE.value]),
                                (key_time, e[Peak.TIME.value] ),
                                (key_injection, e[Peak.INJ.value]), 
                                (key_rack, e[Peak.RACK.value]),
                                (key_rackpos, e[Peak.RACKPOS.value])])
                continue

            key_rtime = "%s_rtime" % e[peak_index] # key retention time
            key_height = "%s_height" % e[peak_index] # key height
            key_area = "%s_area" % e[peak_index] # key area
            key_areap = "%s_areap" % e[peak_index] # key area percent

            real_dict.update([(key_rtime, e[Peak.RTIME.value]), 
                            (key_height, e[Peak.HEIGHT.value]),
                            (key_area, e[Peak.AREA.value]), 
                            (key_areap, e[Peak.AREAP.value])])

        return real_dict

    def build_csv(self, save_location: str):
        # Empty dataframe
        df = pd.DataFrame()
        with os.scandir('txt_files') as it:
            for entry in it:
                df = df.append(self.parse_text(entry), ignore_index=True)

        # sort headers & save to csv file format
        header_list = list(df.columns.values)
        sorted_header_list = sorted(header_list, key= lambda x:self.sort_headers(x))
        df2 = df.reindex(columns=sorted_header_list)
        df2.to_csv(save_location, index=False)
        shutil.rmtree('txt_files')