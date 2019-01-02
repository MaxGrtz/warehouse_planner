import algorithm
import numpy as np

class Hill_Climbing(algorithm.Algorithm):
    '''
    Hill Climbing algorithm
    '''
    
    def __init__(self, psu_dict, order, decode_dict):
        '''
        initialize algorithm object with psu_dict, order list and dict to decode items via parent algorithm class
        '''
        super().__init__(psu_dict, order, decode_dict)
        self.name = "Hill Climbing"

    def run(self, state=None):
        '''
        method to run the algorithm from the constructed algorithm object
            parameter: state - state from which to start hill-climbing, None is default, results in random start state
            returns: post precessed result - provided items, number of psus required, result state
        '''
        # preprocess psu_dict - filter for relevant PSUs 
        psu_dict = self.pre_processing(self.psu_dict, self.order)

        # get random initial state 
        if state is None:
            state = self.get_initial_state(psu_dict, self.order)

        # actual algorithm
        # in every iteration get neighbors of current state and select neighbor with lowest cost
        # done if there is no neighbor with lower cost than current state
        flag = True
        while flag:
            # get neighbors of current state
            neighbors = self.get_neighbors(state, psu_dict) 

            # get lowest cost neighbor or False if there is no neighbor with lower cost than current state
            result = self.get_min_cost_neighbor(neighbors, psu_dict, self.order, state) 
            if result == False:
                flag = False
            else:
                state = result # update state with new state 
        # return postpreocessed result
        return self.post_processing(state, self.decode_dict, psu_dict, self.order)