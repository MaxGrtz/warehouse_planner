import numpy as np

class Algorithm(object):
    '''
    parent class for all algorithms to define commonly used methods
    '''

    def __init__(self, psu_dict, order, decode_dict, item_overview):
        '''
        initialize psu_dict, order list and dict to decode items
        '''
        self.psu_dict = psu_dict
        self.order = order
        self.decode_dict = decode_dict
        self.item_overview = item_overview

    def get_initial_state(self, item_overview):
        '''
        get a random initial state
        parameters: psu_dict - dictionary of PSUs (key) and the numerically encoded items they hold (value)
                    order - list of numerically encoded order
        returns: initial_state - random initial state as a list of length equal to the number of items in order 
                --> idea: we need one PSU for every item in the order (worst case)
        '''
        init_state = np.random.randint(0,2, item_overview.shape[1], dtype=np.bool)
        return init_state

    def get_neighbors(self, state):
        '''
        get neighbors of current state
        parameters: state - current state (list of PSUs)
                    psu_dict - filtered dictionary of PSUs (key) and the numerically encoded items they hold (value)
        returns: neighbors - list of all neighboring states of the given current state
                --> idea: neighboring states are states with only one PSU different from current state
        '''
        neighbors = np.tile(state,(state.shape[0],1))
        mask = np.eye(neighbors.shape[0], dtype=np.bool)
        neighbors[mask] = np.logical_not(neighbors[mask])
        return neighbors

    def calculate_cost(self, state, item_overview, order):
        '''
        calculate cost based on number of psus used and order items fulfilled/provided with current state
        parameters: state - current state (list of PSUs)
                    psu_dict - filtered dictionary of PSUs (key) and the numerically encoded items they hold (value)
                    order - list of numerically encoded order
        returns: cost - cost associated with current state based on number of PSUs (non zero PSUs ids in state) 
                        and number of provided items (items of order satisfied by current state)
        '''
        num_psus_used = np.sum(state)
        items_provided = np.sum(np.any(np.squeeze(item_overview[:, np.where(state)]), axis=1))
        return num_psus_used + 10*(len(order)-items_provided)
        
    def get_min_cost_neighbor(self, item_overview, neighbors, order, state):
        '''
        method to get neighbor with lowest cost 
        parameters: neighbors - neighbors of current state
                    psu_dict - filtered dictionary of PSUs (key) and the numerically encoded items they hold (value)
                    order - list of numerically encoded order
                    state - current state 
        returns: least cost neighbor or False if no neighbor has lower cost than current state
        '''

        # calculate cost of all neighbors
        costs = [self.calculate_cost(state, item_overview, order) for state in neighbors]
        min_cost = np.amin(costs) # get minimum cost
        idx = np.argmin(costs) # get neighbor index of minimum cost

        print(min_cost)
        # return neighbor with minimum cost or False if min_cost is not lower than current state cost
        if min_cost < self.calculate_cost(state, item_overview, order): 
            return neighbors[idx]
        else:
            return state

    def post_processing(self, state, decode_dict, item_overview, order, psu_dict):
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
        num_psus = "Number of PSUs required: " + str(np.sum(state))

         # get number of provided items 
        provided_items = np.sum(np.any(np.squeeze(item_overview[:, np.where(state)]), axis=1)) 

        # create result dict - PSUs of result state (keys) and decoded items they carry (values)
        # items that are in the order are casted to upper case for emphasis
        result_dict = {}
        for idx in np.where(state)[0]:
                psu = list(psu_dict.keys())[idx]
                print(idx, psu)
                result_dict[psu] = [decode_dict[item] for item in psu_dict[psu]]
        

        # create a string from result_dict - every line one PSU with its items 
        result_str = ""
        for psu in list(result_dict.keys()):
            result_str += str(psu) + ":\t"
            for item in result_dict[psu]:
                result_str += item + ", "
            result_str = result_str[:-2] + " \n"
        
        # create string to summarize number of items of order that are satisfied
        provided_items_str = "Provided Items: {}/{}".format(provided_items, len(order))
        
        return provided_items_str, num_psus, result_str

   

    
