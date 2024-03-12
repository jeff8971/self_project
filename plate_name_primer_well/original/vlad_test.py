'''
Vlad's reactions by plates well and primer list.
author: Jeff (Yuan Zhao)
version: 1.0
data: 04-26-2023
'''

import sys
import os

ELEMENT = 2

def read_file(filename) -> list:
    '''
    :param filename: by path, need to fix the path part
    :return: the whole file in a big list
    '''

    file_list = []
    try:
        with open(filename, 'r') as f:
            for line in f.readlines():
                file_list.append(line.split())
    except FileNotFoundError:
        print(f"{filename} not found")

    return file_list


def primer_list(file_list: list) -> list:
    '''
    :function: analysis the directive_file.txt into a list with sublist
    :parameter: .txt
    :return all_primer_list
    every sublist is 4 elements
    [0] template: template name
    [1] well: well number
    [2] primer: primer name
    [3] comment: email or order#
    '''

    all_primer_list = []
    for i in range(1, len(file_list)):
        reaction = file_list[i]
        current_primers = reaction[2]
        current_primers_list = current_primers.split(";")

        for each in current_primers_list:
            if each not in all_primer_list:
                all_primer_list.append(each)

    return all_primer_list


def primer_index(file_list: list):
    '''

    :param file_list: original file list
    :return: an all primer dictionary {primer: index}
    '''

    primer_index_dict = {}
    all_primer_list = primer_list(file_list)

    for i in range(len(all_primer_list)):
        primer_index_dict[all_primer_list[i]] = i

    return primer_index_dict


def sample_list(file_list: list) -> list:
    '''

    :param file_list: whole file list
    :return: the sample list
    '''

    all_sample_list = []
    for i in range(1, len(file_list)):
        reaction = file_list[i]
        sample = reaction[0]
        all_sample_list.append(sample)

    return all_sample_list


def sample_primers_dict(file_list: list) -> list:
    '''

    :param file_list: whole file list
    :return: the dictionary, key is the sample name, value is the primer list
    '''
    sam_prim_dict = {}
    for i in range(1, len(file_list)):
        cur_primer = file_list[i][0]
        cur_primer_list = file_list[i][2].split(";")
        sam_prim_dict[cur_primer] = cur_primer_list

    return sam_prim_dict


def well_primers_dict(file_list: list) -> dict:
    '''

    :param file_list: whole file list
    :return: the dictionary, key is the sample name, value is the primer list
    '''

    well_primers_dict = {}
    for i in range(1, len(file_list)):
        cur_well = file_list[i][1]
        cur_primer_list = file_list[i][2].split(";")
        well_primers_dict[cur_well] = cur_primer_list

    return well_primers_dict


def plate_well(file_list: list) -> list:
    all_wells_num = []
    for i in range(1, len(file_list)):
        reaction = file_list[i]
        sample = reaction[1]
        all_wells_num.append(sample)

    return all_wells_num





def well_primer(file_list: list):
    all_primer_list = primer_list(file_list)
    all_sample_list = sample_list(file_list)
    all_well_list = plate_well(file_list)


    if len(all_sample_list) != len(all_well_list):
        print("wrong with the list, well# != sample#")
        sys.exit(1)

    well_primer_d = well_primers_dict(file_list)

    well_primer_list = []

    primer_num = len(all_primer_list)

    for i in range(len(all_well_list)):
        temp_list =[]
        curr_primer_list = [''] * primer_num
        temp_list.append(all_well_list[i])
        for j in range(len(all_primer_list)):
            
            if all_primer_list[j] in well_primer_d[all_well_list[i]]:
                curr_primer_list[j] = all_primer_list[j]
            else:
                curr_primer_list[j] = ' '

        temp_list.append(curr_primer_list)

        well_primer_list.append(temp_list)

    return well_primer_list






def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_dir = os.path.join(current_dir, "../resourses", "vlad4.txt")


    file_out_put_list = read_file(file_dir)

    """
    print(current_dir)
    print(file_dir)



    print(file_out_put_list)

    print("\n")
    print(sample_list(file_out_put_list))
    
    print(primer_list(file_out_put_list))

    print(plate_well(file_out_put_list))
    print(sample_primers_dict(file_out_put_list))
    print(well_primers_dict(file_out_put_list))
"""


    print(well_primer(file_out_put_list))


if __name__ == '__main__':
    main()
