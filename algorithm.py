import numpy as np
import random

class Algorithm(object):
    '''
    parent class for all algorithms to define commonly used methods
    '''

    def __init__(self, psu_dict, order, decode_dict):
        '''
        initialize algorithm with psu_dict, order list and dict to decode items
        '''
        self.psu_dict = psu_dict
        self.order = order
        self.decode_dict = decode_dict

    def get_initial_state(self, psu_dict, order):
        '''
        get a random initial state
        parameters: psu_dict - dictionary of PSUs (key) and the numerically encoded items they hold (value)
                    order - list of numerically encoded order
        returns: initial_state - random initial state as a list of length equal to the number of items in order 
                --> idea: we need one PSU for every item in the order (worst case)
        '''
        return random.sample(list(psu_dict.keys()), len(order)) 


    def get_neighbors(self, state, psu_dict):
        '''
        get neighbors of current state
        parameters: state - current state (list of PSU ids)
                    psu_dict - filtered dictionary of PSUs (key) and the numerically encoded items they hold (value)
        returns: neighbors - list of all neighboring states of the given current state
                --> idea: neighboring states are states with only one PSU different from current state
        '''
        neighbors = []
        # for every position in the state
        for i in range(len(state)):
            # every variation from the current psu at that state position is a neighbor of the current state
            for psu in psu_dict:
                temp_state = state.copy()
                temp_state[i] = psu
                neighbors.append(temp_state)
        return neighbors 

    def calculate_cost(self, state, psu_dict, order):
        '''
        calculate cost based on number of psus used and order items fulfilled/provided with current state
        parameters: state - current state (list of PSUs)
                    psu_dict - filtered dictionary of PSUs (key) and the numerically encoded items they hold (value)
                    order - list of numerically encoded order
        returns: cost - cost associated with current state based on number of PSUs (non zero PSU ids in state) 
                        and number of provided items (items of order satisfied by current state)
        '''
        # get number of items of the order that are not the items provided by the psus
        missing_items = len(set(order) - set([item for psu in state for item in psu_dict[psu]]))

        state = np.asarray(state) # for easier indexing
        # calculate cost - missing items are counted 10 times compared to number of PSUs required
        return missing_items*10 + len(state[state!=0])
        
    def get_min_cost_neighbor(self, neighbors, psu_dict, order, state):
        '''
        method to get neighbor with lowest cost 
        parameters: neighbors - neighbors of current state
                    psu_dict - filtered dictionary of PSUs (key) and the numerically encoded items they hold (value)
                    order - list of numerically encoded order
                    state - current state 
        returns: least cost neighbor or False if no neighbor has lower cost than current state
        '''
        # calculate cost of all neighbors
        costs = [self.calculate_cost(nb, psu_dict, order) for nb in neighbors]
        min_cost = np.amin(costs) # get minimum cost
        idx = np.argmin(costs) # get neighbor index of minimum cost

        # return neighbor with minimum cost or False if min_cost is not lower than current state cost
        return neighbors[idx] if min_cost < self.calculate_cost(state, psu_dict, order) else False
    

    def post_processing(self, state, decode_dict, psu_dict, order):
        '''
        transform results to strings for output
        parameters: state - result state (list of PSUs)
                    decode_dict - dictionary for decoding numeric items
                    psu_dict - filtered dictionary of PSUs (key) and the numerically encoded items they hold (value)
                    order - list of numerically encoded order
        returns: provided_items_str - string to summarize number of items of order that are satisfied
                 num_psus - number of non zero PSUs in state (where 0 is placeholder for no PSU)
        '''
        # get number of non zero PSUs in state (where 0 is placeholder for no PSU) 
        state = np.asarray(state)
        num_psus = "Number of PSUs required: {}".format(len(state[state!=0]))

        # create result dict - PSUs of result state (keys) and decoded items they carry (values)
        result_dict = {psu: [decode_dict[item] for item in psu_dict[psu]] for psu in state}
        
        # get number of items of the order that are provided by the result state PSUs 
        provided_items = set([item for psu in state for item in psu_dict[psu]])

        # create a string from result_dict - every line one PSU with its items 
        result_str = "\n".join(["{}:\t{}".format(psu ,", ".join([item for item in result_dict[psu]])) for psu in state if psu != 0])
        
        # create string to summarize number of items of order that are satisfied
        provided_items_str = "Provided Items: {}/{}".format(len(provided_items), len(order))
        
        return provided_items_str, num_psus, result_str

   

    
