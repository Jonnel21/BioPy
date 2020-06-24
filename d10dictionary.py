from createdict import CreateDictionary

class D10Dictionary(CreateDictionary):
    
    def create_dictionary(self, txt_file_path):
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