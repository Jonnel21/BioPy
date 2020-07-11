import os
import subprocess
import shutil
import re
import pandas as pd
from peak import Peak


class InstrumentStrategy():

    def __init__(self):
        self.temp_dir = 'C:/BioPy_Temp'

    def convert_pdf(self, pdf_tuples: tuple):
        print(pdf_tuples)

        pdftotext_path = 'C:/Users/Jonnel/Documents/BioPy/src/pdftotext.exe'  # use this path for build
        # pdftotext_path = '.\\BioPy\\src\\pdftotext'
        '''
        Takes a pdf file and converts it to a txt file.

        Parameters:
            pdf_tuples: tuple

        Returns:
            None
        '''

        try:
            os.mkdir(self.temp_dir)
        except FileExistsError:
            shutil.rmtree(self.temp_dir)
            os.mkdir(self.temp_dir)

        for i in pdf_tuples:
            tmp_arr = i.split('/')
            pdf_file = tmp_arr[len(tmp_arr) - 1]
            name = os.path.splitext(pdf_file)[0]  # returns name without ext
            with open(f"{self.temp_dir}/{name}.txt", 'x') as file:
                subprocess.run([pdftotext_path, '-simple', f'{i}', '-'], stdout=file)
                file.close()

    def wrapper_decode(self, arr: list):

        '''
        A wrapper method for the decode function.

        Parameters:
            arr: list

        Returns:
            newarr: list
        '''

        newarr = []
        for a in arr:
            newarr.append(a.decode())
        return newarr

    def rename_unknown(self, lst: list):

        ''' Searches for \"Unknowns\" in the list.

            If duplicates of \"Unknowns\" exsists
            the function will append a number at the
            end of the string to distingush between
            other Unknown values.

            Parameters:
                lst: list

            Returns:
                "List is empty."
                or
                "There are no Unknowns in the list."
        '''
        if(len(lst) == 0):
            return "List is empty."

        if(Peak.UNKNOWN.value in lst):
            num_unknown = lst.count(Peak.UNKNOWN.value)
            for i in range(num_unknown):
                lst[lst.index("Unknown")] += str(i+1)
        else:
            return "There are no %ss in the list." % Peak.UNKNOWN.value

    def to_nested(self, table: list):

        '''
        Converts the peak list to a nested list.

        A peak list consists of:
        peak name, retention time, height, area, area percent

        The list may contain multiple peak names each consisting of their
        respective retention time, height, area, and area percent.

        Parameters:
            table: list

        Returns:
            output: list
        '''

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

    def sort_headers(self, x: str):

        '''
        Sorts headers in the csv file

        Sorts unknown values toward the end of the file.
        Sorts Sample, Date, Time, Injection Number, and Rack ID towards
        the beginning of the file.

        Paramters:
            x: str

        Returns:
            0: number
            -1: number
            1: number
        '''

        unknown_match = re.search('^Unknown\d', x)
        info_match = re.match('Sample|Date|Time|Inj|Rack|Total Hb Area|Pattern|FAST_*', x)
        if(info_match):
            return -1
        elif(unknown_match):
            return 1
        else:
            return 0

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
                if(len(nested_list[0]) == 8):  # check for a pattern value
                    key_sampleID = "Sample_ID"
                    key_date = "Date"
                    key_time = "Time"
                    key_injection = "Inj #"
                    key_rack = "Rack #"
                    key_rackpos = "Rack Position"
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

    def build_csv(self, save_location: str):

        '''
        Creates a csv from a dictionary.

        Appends additional dictionaries to a dataframe.

        Parameters:
            save_location: str

        Returns:
            None
        '''

        # Empty dataframe
        df = pd.DataFrame()
        with os.scandir(self.temp_dir) as it:
            for entry in it:
                df = df.append(self.parse_text(entry), ignore_index=True)

        # sort headers & save to csv file format
        header_list = list(df.columns.values)
        sorted_header_list = sorted(header_list, key=lambda x: self.sort_headers(x))
        df2 = df.reindex(columns=sorted_header_list)
        df2.to_csv(save_location, index=False)
        shutil.rmtree(self.temp_dir)
