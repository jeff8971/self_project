import os



class VladReactionAnalyzer:

    def __init__(self, filename):
        self.filename = filename
        self.file_list = self.read_file()

    def read_file(self):
        '''
        :return: the whole file in a big list
        '''
        file_list = []
        try:
            with open(self.filename, 'r') as f:
                for line in f.readlines():
                    file_list.append(line.split())
        except FileNotFoundError:
            print(f"{self.filename} not found")
        return file_list

    def primer_list(self):
        '''
        :function: analysis the directive_file.txt into a list with sublist
        :return all_primer_list
        every sublist is 4 elements
        [0] template: template name
        [1] well: well number
        [2] primer: primer name
        [3] comment: email or order#
        '''
        all_primer_list = []
        for i in range(1, len(self.file_list)):
            reaction = self.file_list[i]
            current_primers = reaction[2]
            current_primers_list = current_primers.split(";")

            for each in current_primers_list:
                if each not in all_primer_list:
                    all_primer_list.append(each)

        return all_primer_list

    def sample_primers_dict(self):
        '''
        :return: the dictionary, key is the sample name, value is the primer list
        '''
        sam_prim_dict = {}
        for i in range(1, len(self.file_list)):
            cur_primer = self.file_list[i][0]
            cur_primer_list = self.file_list[i][2].split(";")
            sam_prim_dict[cur_primer] = cur_primer_list

        return sam_prim_dict

    def well_primers_dict(self):
        '''
        :return: the dictionary, key is the sample name, value is the primer list
        '''
        well_primers_dict = {}
        for i in range(1, len(self.file_list)):
            cur_well = self.file_list[i][1]
            cur_primer_list = self.file_list[i][2].split(";")
            well_primers_dict[cur_well] = cur_primer_list

        return well_primers_dict

    def plate_well(self):
        all_wells_num = []
        for i in range(1, len(self.file_list)):
            reaction = self.file_list[i]
            sample = reaction[1]
            all_wells_num.append(sample)

        return all_wells_num

    def sample_list(self):
        '''
        :return: the sample list
        '''
        all_sample_list = []
        for i in range(1, len(self.file_list)):
            reaction = self.file_list[i]
            sample = reaction[0]
            all_sample_list.append(sample)

        return all_sample_list

    def well_sample_dict(self):
        '''
        :return: the dictionary, key is the well number, value is the sample name
        '''
        well_sam_dict = {}
        for i in range(1, len(self.file_list)):
            cur_sample = self.file_list[i][0]
            cur_well = self.file_list[i][1]
            well_sam_dict[cur_well] = cur_sample

        return well_sam_dict

    def to_plate(self):
        '''
        :return: the plate list [[well1,sample1, primer], [well2,
        sample2 primer], [well3,sample3, primer]....]
        '''
        all_primers_l = self.primer_list()
        all_well_l = self.plate_well()
        well_primer_d = self.well_primers_dict()
        well_sample_d = self.well_sample_dict()

        plate_l = []

        for i in range(len(all_primers_l)):
            curr_primer = all_primers_l[i]

            for j in range(len(all_well_l)):
                curr_well = all_well_l[j]
                curr_w_p_l = []

                if curr_primer in well_primer_d[curr_well]:
                    curr_w_p_l.append(curr_well)
                    curr_w_p_l.append(well_sample_d[curr_well])
                    curr_w_p_l.append(curr_primer)
                if curr_w_p_l:  # Check if the list is not empty
                    plate_l.append(curr_w_p_l)

        return plate_l

    def type_to_plate(self):
        '''
        :return: plate list for type, sample, primer
        '''
        all_primers_l = self.primer_list()
        all_sample_l = self.sample_list()
        samp_primer_d = self.sample_primers_dict()

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

    def analyze_reactions(self):
        print(self.primer_list())
        print(self.to_plate())
        print(len(self.to_plate()))
        print(self.well_primers_dict())
        print(self.type_to_plate())
        print(len(self.type_to_plate()))


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    plate_name = 'plate1.txt'
    file_dir = os.path.join(current_dir, "../resourses", plate_name)

    analyzer = VladReactionAnalyzer(file_dir)

    # Print primer list
    # print("Primer list:", analyzer.primer_list())

    # Print plate layout by well and primer
    # print("Plate layout by well and primer:")
    # for well, primer in analyzer.to_plate():
    # print(well, primer)

    # Print the number of reactions
    # print("Number of reactions:", len(analyzer.to_plate()))

    # Print well and corresponding primers
    # print("Well and corresponding primers:", analyzer.well_primers_dict())

    # Print plate layout by type, sample, and primer
    # print("Plate layout by type, sample, and primer:")
    # for sample, primer in analyzer.type_to_plate():
    # print(sample, primer)

    # Print the number of reactions by type
    # print("Number of reactions by type:", len(analyzer.type_to_plate()))

    plate_layout = analyzer.to_plate()

    # Group the plate_layout into chunks of 96 elements
    plate_chunks = [plate_layout[i:i + 96] for i in
                    range(0, len(plate_layout), 96)]

    # Write each chunk of 96 elements to a separate text file
    for index, chunk in enumerate(plate_chunks):
        output_filename = f"{plate_name}_well_primer_list{index + 1}.csv"
        with open(output_filename, "w") as output_file:
            for well, primer in chunk:
                output_file.write(f"{well}, {primer}\n")





    plate_type_layout = analyzer.type_to_plate()

    # Group the plate_type_layout into chunks of 96 elements

    plate_type_chunks = [plate_type_layout[i:i + 96] for i in
                    range(0, len(plate_type_layout), 96)]

    # Write each chunk of 96 elements to a separate text file
    for index, chunk in enumerate(plate_type_chunks):
        output_filename = f"{plate_name}_typeUp_sample_primer_list{index + 1}.csv"
        with open(output_filename, "w") as output_file:
            for sample, primer in chunk:
                output_file.write(f"{sample}, {primer}\n")


if __name__ == '__main__':
    main()
