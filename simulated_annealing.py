import algorithm, hill_climbing
import numpy as np
import random

class Simulated_Annealing(algorithm.Algorithm):
    
    def __init__(self, psu_dict, order, decode_dict):
        '''
        initialize algorithm object with psu_dict, order list and dict to decode items via parent algorithm class
        '''
        super().__init__(psu_dict, order, decode_dict)
        self.name = "Simulated Annealing"


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

        temp = 10000 # starting temperature

        while temp > 0:            
            # get neighbors of current state
            idx = np.random.randint(0,len(state))
            psu = random.choice(list(psu_dict.keys()))
            
            # get random neighbor state
            next_state = state.copy()
            next_state[idx] = psu

            # difference between cost of new and current state
            delta = self.calculate_cost(next_state, psu_dict, order) - self.calculate_cost(state, psu_dict, order)

            if delta > 0:
                # if random neighbor is better than current state, update curretn state 
                state = next_state
            else:
                # else update with some probability
                if np.random.random() <= np.exp(delta/temp):
                    state = next_state
            
            temp -= 1
        
        # get local maximum of final state via hillclimbing from this state and return it
        alg = hill_climbing.Hill_Climbing(psu_dict, order, decode_dict)
        return alg.run(state)
        
