import re
import os
import pandas as pd
import itertools as it
from pdfreader import SimplePDFViewer
from enum import Enum
from collections import Counter

class Peak(Enum):
    RTIME = 1
    HEIGHT = 2
    AREA = 3
    AREAP = 4
    SAMPLE = 0
    DATE = 1
    TIME = 2
    INJ = 3
    RACK = 4
    RACKPOS = 5
    UNKNOWN = "Unknown"

# Parse pdf and returns list of dictionaries
def reader(str):
    file = open(str, 'r+b')
    view = SimplePDFViewer(file)
    all_pages = [p for p in view.doc.pages()]

    if(len(all_pages) >= 1):
        dict_to = []
        for i, e in enumerate(all_pages):
            view.navigate(i+1) # iterate the page
            view.render() # display the page
            my_pdf = view.canvas.strings # list data
            str = my_pdf[6]
            my_pdf[6] = str[str.index(':')+1 :].strip() # parse injection # to just the number

            start = my_pdf.index('Area % ') # inclusive
            end = my_pdf.index('Total Area: ') # exclusive
            peak_table = my_pdf[start + 1 : end]

            sampleID_index = my_pdf.index('Sample ID:')
            peak_index = my_pdf.index('Peak ')
            info_table = my_pdf[sampleID_index : peak_index]

            ex_info = info_table[1:4:2] + info_table[4:7:2] + info_table[7:8]

            final_table = ex_info + peak_table

            print("page: %d, reading: %r" % (i, view.canvas.strings))
            dict_to.append(map_to_dictionary(to_nested(final_table)))

    return dict_to

# Helper function to sort headers
def sort_headers(x):
    unknown_match = re.search('^Unknown\d', x)
    info_match = re.match('Sample|Date|Time|Inj|Rack', x)
    if(info_match):
         return -1
    elif(unknown_match):
        return 1
    else: return 0

# Helper function to create a nested list
def to_nested(table):
    rename_unknown(table)
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

# Helper function to rename unknown peaks
def rename_unknown(lst):
    if(Peak.UNKNOWN.value in lst):
        num_unknown = lst.count(Peak.UNKNOWN.value)
        for i in range(num_unknown):
            lst[lst.index("Unknown")] += str(i+1)
    else: print("There are no %ss in the list." % Peak.UNKNOWN.value)

# Helper function to map 2d array into a dictionary
def map_to_dictionary(nested_list):
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

def build_csv(str, save_location):
    # Empty dataframe
    df = pd.DataFrame()

    # Loop through result folder
    with os.scandir(str) as it:
        for entry in it:
            df = df.append(reader(entry))

    # sort headers & save to csv file format
    header_list = list(df.columns.values)
    sorted_header_list = sorted(header_list, key= lambda x:sort_headers(x))
    df2 = df.reindex(columns=sorted_header_list)
    df2.to_csv(save_location, index=False)

# def build_csv(file_tuple, save_location):
#     # Empty dataframe
#     df = pd.DataFrame()

#     for element in file_tuple:
#         df = df.append(reader(element))

#     # sort headers & save to csv file format
#     header_list = list(df.columns.values)
#     sorted_header_list = sorted(header_list, key= lambda x:sort_headers(x))
#     df2 = df.reindex(columns=sorted_header_list)
#     df2.to_csv(save_location, index=False)

# build_csv("Result", 'v2.csv')
# build_csv("hell.pdf")
# build_csv()