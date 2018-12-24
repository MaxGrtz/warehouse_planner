import algorithm

class First_Choice_Hill_Climbing(algorithm.Algorithm):
    
    def __init__(self, psu_dict, order, decode_dict):
        super().__init__(psu_dict, order, decode_dict)


    def run(self):
        return "2", "first choice hill climbing"