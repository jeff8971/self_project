'''
Vlad's reactions by plates well and primer list.
author: Jeff (Yuan Zhao)
version: 1.1
data: 04-26-2023
'''

import sys
import os


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


def to_plate(file_list: list):
    '''
    :param file_list:
    :return: the plate list [[well1, primer], [well2, primer], [well3,
    primer]....]
    '''

    all_primers_l = primer_list(file_list)
    all_well_l = plate_well(file_list)
    well_primer_d = well_primers_dict(file_list)

    plate_l = []

    for i in range(len(all_primers_l)):
        curr_primer = all_primers_l[i]

        for j in range(len(all_well_l)):
            curr_well = all_well_l[j]
            curr_w_p_l = []

            if curr_primer in well_primer_d[curr_well]:
                curr_w_p_l.append(curr_well)
                curr_w_p_l.append(curr_primer)
                plate_l.append(curr_w_p_l)

    return plate_l


def type_to_plate(file_list: list):

    '''
    plate list for type, sample, primer
    :param file_list: file_original list
    :return: plate list for type.
    '''
    all_primers_l = primer_list(file_list)
    all_sample_l = sample_list(file_list)
    samp_primer_d = sample_primers_dict(file_list)

    # plate layout for type in
    plate_type_l = []

    for i in range(len(all_primers_l)):
        curr_primer = all_primers_l[i]

        for j in range(len(all_sample_l)):
            curr_sample = all_sample_l[j]
            curr_s_p_l = []

            if curr_primer in samp_primer_d[curr_sample]:
                curr_s_p_l.append(curr_sample)
                curr_s_p_l.append(curr_primer)
                plate_type_l.append(curr_s_p_l)

    return plate_type_l






def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_dir = os.path.join(current_dir, "../resourses", "vlad4.txt")

    file_out_put_list = read_file(file_dir)
    print(primer_list(file_out_put_list))
    print(to_plate(file_out_put_list))
    print(len(to_plate(file_out_put_list)))
    print(well_primers_dict(file_out_put_list))
    print(type_to_plate(file_out_put_list))
    print(len(type_to_plate(file_out_put_list)))

    """
    print(current_dir)
    print(file_dir)



    print(file_out_put_list)

    print("\n")
    print(sample_list(file_out_put_list))
    print(plate_well(file_out_put_list))



    print(sample_primers_dict(file_out_put_list))
    print(well_primers_dict(file_out_put_list))
"""


if __name__ == '__main__':
    main()
