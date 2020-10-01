from shutil import rmtree
from re import search
from re import match
from pandas import DataFrame
from os import getenv
from os import mkdir
from os import path
from os import scandir
from datetime import datetime
from pyxpdf import Document
from pyxpdf.xpdf import TextControl
from src.peak import Peak


class InstrumentStrategy():

    def __init__(self):
        self.temp_dir = path.join(getenv('programdata'), 'BioPy_Temp')
        self.logs = path.join(getenv('programdata'), 'BioPy_Logs')

    def convert_pdf(self, pdf_tuples: tuple):
        """Takes a pdf file and converts it to a txt file.

        :param pdf_tuples: a tuple of pdf file paths.
        :type pdf_tuples: tuple
        """

        try:
            mkdir(self.temp_dir)
        except FileExistsError:
            rmtree(self.temp_dir)
            mkdir(self.temp_dir)

        for i in pdf_tuples:
            with open(i, 'rb') as fp:
                doc = Document(fp)
                if(doc.num_pages == 1):
                    tmp_arr = i.split('/')
                    pdf_file = tmp_arr[len(tmp_arr) - 1]  # find file name
                    name = path.splitext(pdf_file)[0]  # remove extenstion
                    with open(f"{self.temp_dir}/{name}.txt", 'x') as file:
                        label_page = doc[0]
                        text_ctrl = TextControl('simple', discard_clipped=True)
                        text = label_page.text(control=text_ctrl)
                        file.write(text)
                else:
                    for j in range(doc.num_pages):
                        now = datetime.now()
                        hour = now.hour
                        minute = now.minute
                        seconds = now.second
                        micro = now.microsecond
                        with open(f"{self.temp_dir}/{hour}_{minute}_{seconds}_{micro}_{j}.txt", 'x') as file:
                            label_page = doc[j]
                            text_ctrl = TextControl('simple', discard_clipped=True)
                            text = label_page.text(control=text_ctrl)
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
        unknown_match = search('^Unknown\\d', x)
        info_match = match(info_headers, x)
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
        df = DataFrame()
        with scandir(self.temp_dir) as it:
            for entry in it:
                df = df.append(self.parse_text(entry), ignore_index=True)

        # sort headers & save to csv file format
        header_list = list(df.columns.values)
        sorted_header_list = sorted(header_list,
                                    key=lambda x: self.sort_headers(x))
        df2 = df.reindex(columns=sorted_header_list)
        df2.to_csv(save_location, index=False)
        rmtree(self.temp_dir)
