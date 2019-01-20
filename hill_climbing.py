import algorithm
import numpy as np

class Hill_Climbing(algorithm.Algorithm):
    '''
    Hill Climbing algorithm
    '''
    
    def __init__(self, psu_dict, order, decode_dict, item_overview):
        '''
        initialize algorithm object with psu_dict, order list and dict to decode items via parent algorithm class
        '''
        super().__init__(psu_dict, order, decode_dict, item_overview)
        self.name = "Hill Climbing"

    def run(self, state=None):
        '''
        method to run the algorithm from the constructed algorithm object
            parameter: state - state from which to start hill-climbing, None is default, results in random start state
            returns: post precessed result - provided items, number of psus required, result state
        ''' 
        item_overview = self.item_overview
        psu_dict = self.psu_dict
        order = self.order
        decode_dict = self.decode_dict

        # get random initial state 
        if state is None:
            state = self.get_initial_state(item_overview)

        # actual algorithm
        # in every iteration get neighbors of current state and select neighbor with lowest cost
        # done if there is no neighbor with lower cost than current state
        flag = True
        while flag:
            # get neighbors of current state
            neighbors = self.get_neighbors(state) 

            # get lowest cost neighbor or False if there is no neighbor with lower cost than current state
            result = self.get_min_cost_neighbor(item_overview, neighbors, order, state) 
            if np.all(result == state):
                flag = False 
            else:
                state = result # update state with new state 
        # return postpreocessed result
        return self.post_processing(state, decode_dict, item_overview, order, psu_dict)