import algorithm

class Local_Beam_Search(algorithm.Algorithm):
    
    def __init__(self, psu_dict, order, decode_dict, num_start_states):
        super().__init__(psu_dict, order, decode_dict)
        self.name = "Local Beam Search"
        self.num_start_states = num_start_states

    def run(self):
        print(self.num_start_states)

        return "5", "local beam search"