import algorithm

class Parallel_Hill_Climbing(algorithm.Algorithm):
    
    def __init__(self, psu_dict, order, encode_dict, decode_dict, num_start_states):
        super().__init__(psu_dict, order, encode_dict, decode_dict)
        self.num_start_states = num_start_states

    def run(self):
        print(self.num_start_states)

        return "4", "parallel hill climbing"