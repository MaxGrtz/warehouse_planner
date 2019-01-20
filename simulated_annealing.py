import algorithm, hill_climbing
import numpy as np

class Simulated_Annealing(algorithm.Algorithm):
    
    def __init__(self, psu_dict, order, decode_dict, item_overview):
        '''
        initialize algorithm object with psu_dict, order list and dict to decode items via parent algorithm class
        '''
        super().__init__(psu_dict, order, decode_dict, item_overview)
        self.name = "Simulated Annealing"


    def run(self):
        '''
        method to run the algorithm from the constructed algorithm object
            returns: post precessed result - provided items, number of psus required, result state
        '''
        item_overview = self.item_overview
        psu_dict = self.psu_dict
        order = self.order
        decode_dict = self.decode_dict

        # get random initial state 
        state = self.get_initial_state(item_overview)

        temp = 10000 # starting temperature

        while temp > 0:            
            # get nieghbors of current state
            neighbors = self.get_neighbors(state) 

            # choose random neighbor state
            next_state = neighbors[np.random.randint(0, len(neighbors))]

            # difference between cost of new and current state
            delta = self.calculate_cost(next_state, item_overview, order) - self.calculate_cost(state, item_overview, order)

            if delta > 0:
                # if random neighbor is better than current state, update current state 
                state = next_state
            else:
                # else update with some probability
                if np.random.random() <= np.exp(delta/temp):
                    state = next_state
            
            temp -= 1
        
        # get local maximum of final state via hillclimbing from this state and return it
        alg = hill_climbing.Hill_Climbing(psu_dict, order, decode_dict, item_overview)
        return alg.run(state)
        # return self.post_processing(state, decode_dict, item_overview, order, psu_dict) 
        
