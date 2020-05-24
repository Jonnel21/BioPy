import subprocess
import os
import shutil
import miner
import pandas as pd

# decode bytes to string
def wrapper_decode(arr):
    newarr = []
    for a in arr:
        newarr.append(a.decode())
    return newarr

# Creates txt files from pdfs
def convert_pdf(pdf_location):
    try:
        os.mkdir('txt_files')
    except FileExistsError:
        shutil.rmtree('txt_files')
        os.mkdir('txt_files')

    with os.scandir(f'{pdf_location}') as it:
        for i in it:
            name = os.path.splitext(i.name)[0] # returns filename without extenstion
            with open(f"./txt_files/{name}.txt", 'x') as file:
                subprocess.run(['pdftotext', '-simple', f'./{pdf_location}/{name}.pdf', '-'], stdout=file)

# takes a txt file and returns a dictionary
def parse_text(txt_path):
    arr = []
    with open(txt_path, 'rb') as f:
        info_table = []
        nested_table = []
        temp = ""
        arr = f.read().split()
        decoded_arr = wrapper_decode(arr)

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
        nested_table = miner.to_nested(peak_table)
        nested_table.insert(0, info_table)

        # create dictionary
        test_dict = miner.map_to_dictionary(nested_table)
        f.close()
    return test_dict

# converts dataframe into csv          
def build_csv(save_location):
    # Empty dataframe
    df = pd.DataFrame()
    with os.scandir('txt_files') as it:
        for entry in it:
            df = df.append(parse_text(entry), ignore_index=True)

    # sort headers & save to csv file format
    header_list = list(df.columns.values)
    sorted_header_list = sorted(header_list, key= lambda x:miner.sort_headers(x))
    df2 = df.reindex(columns=sorted_header_list)
    df2.to_csv(save_location, index=False)

convert_pdf('Result')
build_csv('test.csv')