import os
import shutil
import re
import pandas as pd
from pyxpdf import Document
from pyxpdf.xpdf import TextControl
from src.peak import Peak


class InstrumentStrategy():

    def __init__(self):
        self.temp_dir = os.path.join(os.getenv('programdata'), 'BioPy_Temp')
        self.logs = os.path.join(os.getenv('programdata'), 'BioPy_Logs')

    def convert_pdf(self, pdf_tuples: tuple):
        """Takes a pdf file and converts it to a txt file.

        :param pdf_tuples: a tuple of pdf file paths.
        :type pdf_tuples: tuple
        """

        try:
            os.mkdir(self.temp_dir)
        except FileExistsError:
            shutil.rmtree(self.temp_dir)
            os.mkdir(self.temp_dir)

        for i in pdf_tuples:
            tmp_arr = i.split('/')
            pdf_file = tmp_arr[len(tmp_arr) - 1]  # find the file name
            name = os.path.splitext(pdf_file)[0]  # returns name w/o ext
            with open(f"{self.temp_dir}/{name}.txt", 'x') as file:
                with open(i, 'rb') as fp:
                    doc = Document(fp)
                    label_page = doc[0]
                    text_control = TextControl('simple', discard_clipped=True)
                    text = label_page.text(control=text_control)
                    file.write(text)

    def wrapper_decode(self, arr: list):
        """Decode the bytes to string in the list.

        :param arr: A list of bytes
        :type arr: list
        :return: A new list of strings
        :rtype: list
        """

        '''
        Decode the bytes to string in the list.

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
        """Searches for \"Unknowns\" in the list.

           If duplicates of \"Unknowns\" exsists
           the function will append a number at the
           end of the string to distingush between
           other Unknown values.

        :param lst: Headers of peak names.
        :type lst: list
        :return: A string literal.
        :rtype: str
        """

        if(len(lst) == 0):
            return "List is empty."

        if(Peak.UNKNOWN.value in lst):
            num_unknown = lst.count(Peak.UNKNOWN.value)
            for i in range(num_unknown):
                lst[lst.index("Unknown")] += str(i+1)
        else:
            return "There are no %ss in the list." % Peak.UNKNOWN.value

    def to_nested(self, table: list):
        """Converts the peak list to a nested list.

           A peak list consists of:
           peak name, retention time, height, area, area percent.
           The list may contain multiple peak names each consisting of their
           respective retention time, height, area, and area percent.

        :param table: Peak names and their values.
        :type table: list
        :return: a nested list of peak names and values.
        :rtype: list
        """

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
        """Sorts headers in the csv file.

           Sorts unknown values towawrds the end of the file.
           Sorts key info headers towards the beginning of the file.

        :param x: Header to be evaluated.
        :type x: str
        :return: proxy value used to sort headers.
        :rtype: number
        """
        info_headers = ('Sample|Date|Time|Inj|Rack|Total Hb Area|Pattern|'
                        'Well|Plate|Tube|Run|Lot|Expiration Date')
        unknown_match = re.search('^Unknown\d', x)
        info_match = re.match(info_headers, x)
        if(info_match):
            return 0
        elif(unknown_match):
            return 2
        else:
            return 1

    def build_csv(self, save_location: str):
        """Generates a csv from a dictionary.

           Appends additional dictionaries to a dataframe.

        :param save_location: path to save csv file.
        :type save_location: str
        """

        # Empty dataframe
        df = pd.DataFrame()
        with os.scandir(self.temp_dir) as it:
            for entry in it:
                df = df.append(self.parse_text(entry), ignore_index=True)

        # sort headers & save to csv file format
        header_list = list(df.columns.values)
        sorted_header_list = sorted(header_list,
                                    key=lambda x: self.sort_headers(x))
        df2 = df.reindex(columns=sorted_header_list)
        df2.to_csv(save_location, index=False)
        shutil.rmtree(self.temp_dir)
