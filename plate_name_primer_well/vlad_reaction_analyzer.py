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
                    if not line.strip():
                        break
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
        '''
        all_primer_list = []
        for i in range(1, len(self.file_list)):
            reaction = self.file_list[i]

            if len(reaction) < 3:  # Check if reaction has enough elements
                print(f"Skipping reaction {i} due to insufficient elements")
                continue

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
        '''
        :return: the plate well number
        '''
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


    def analyze_reactions(self):
        print(self.primer_list())
        print(self.to_plate())
        print(len(self.to_plate()))
        print(self.well_primers_dict())

    @classmethod
    def save_plate_layout_to_desktop(cls, input_file_path):
        analyzer = cls(input_file_path)
        plate_layout = analyzer.to_plate()

        # Group the plate_layout into chunks of 96 elements
        plate_chunks = [plate_layout[i:i + 96] for i in
                        range(0, len(plate_layout), 96)]

        # save the files to desktop
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        for index, chunk in enumerate(plate_chunks):
            output_filename = f"{os.path.basename(input_file_path).split('.')[0]}_well_primer_list{index + 1}.csv"
            output_file_path = os.path.join(desktop_path, output_filename)
            with open(output_file_path, "w") as output_file:
                for well, sample, primer in chunk:
                    output_file.write(f"{well},{sample},{primer}\n")


