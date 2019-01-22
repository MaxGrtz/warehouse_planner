import algorithm

class First_Choice_Hill_Climbing(algorithm.Algorithm):
    
    def __init__(self, psu_dict, order, decode_dict):
        '''
        initialize algorithm object with psu_dict, order list and dict to decode items via parent algorithm class
        '''
        super().__init__(psu_dict, order, decode_dict)
        self.name = "First Choice Hill Climbing"

    def run(self):
        '''
        method to run the algorithm from the constructed algorithm object
            returns: post precessed result - provided items, number of psus required, result state
        '''
        psu_dict = self.psu_dict
        order = self.order
        decode_dict = self.decode_dict

        # get random initial state 
        state = self.get_initial_state(psu_dict, order)

        # actual algorithm
        # in every iteration the first neighbor with lower cost than the current state is selected 
        # done if there is no neighbor with lower cost than current state
        flag = True  
        while flag:
            # get nieghbors of current state
            neighbors = self.get_neighbors(state, psu_dict) 
            current_cost = self.calculate_cost(state, psu_dict, order)
            # get first neighbor with lower cost than current neighbor
            updated = False  
            for nb in neighbors:
                nb_cost = self.calculate_cost(nb, psu_dict, order)
                if nb_cost < current_cost:
                    state = nb
                    updated = True 
                    break

            if not updated:
                flag = False
            
        # return postprocessed result
        return self.post_processing(state, decode_dict, psu_dict, order)
            
        