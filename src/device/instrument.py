import os
import subprocess
import shutil
import re
import pandas as pd
from src.peak import Peak


class InstrumentStrategy():

    def __init__(self):
        self.temp_dir = '.\\temp'  # local

    def convert_pdf(self, pdf_tuples: tuple):
        print(pdf_tuples)

        # pdftotext_path = './src/pdftotext.exe'
        # pdftotext_path = './src/pdftotext.exe'  # debug
        pdftotext_path = './pdftotext'  # dev & build
        # pdftotext_path = '..\\pdftotext.exe'  # tests
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
            pdf_file = tmp_arr[len(tmp_arr) - 1]  # find the file name
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
        decoded_arr = []
        for a in arr:
            decoded_arr.append(a.decode())
        return decoded_arr

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
        info_match = re.match('Sample|Date|Time|Inj|Rack|Total Hb Area|Pattern|Well|Plate|Tube|Run|Lot|Expiration Date', x)
        if(info_match):
            return 0
        elif(unknown_match):
            return 2
        else:
            return 1

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
        # end_index = sorted_header_list.index('Total Hb Area') + 1
        # info_header = sorted_header_list[0:end_index]
        # peak_header = sorted_header_list[end_index:]
        # sorted_peak_header = sorted(peak_header)
        # final_headers = info_header + sorted_peak_header
        # df2 = df.reindex(columns=final_headers)
        df2 = df.reindex(columns=sorted_header_list)
        df2.to_csv(save_location, index=False)
        shutil.rmtree(self.temp_dir)

    def sort_info_headers(self, header_list):
        update_list = []
        test = ["Date," "Inj #", "Pattern", "Plate Position", "Sample_ID", "Time", "Total Hb Area"]
        headers = {
            "0": "Date",
            "1": "Time",
            "2": "Inj #",
            "3": "Rack #",
            "7": "Total Hb Area"
        }

        if "Pattern" in test:
            headers.update({"4": "Pattern", "5": "Plate Position", "6": "Well #"})
            temp = sorted(headers.items())
            for i in range(len(temp)):
                update_list.append(temp[i][1])
        print(update_list)
