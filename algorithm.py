import numpy as np

class Algorithm(object):
    '''
    parent class for all algorithms to define commonly used methods
    '''

    def __init__(self, psu_dict, order, decode_dict):
        '''
        initialize psu_dict, order list and dict to decode items
        '''
        self.psu_dict = psu_dict
        self.order = order
        self.decode_dict = decode_dict
    
    def pre_processing(self, psu_dict, order):
        '''
        filter psu_dict for relevant psus (psus that contain at least one item from the order)
            parameters: psu_dict - complete dictionary of PSUs (key) and the nuerically encoded items they hold (value)
                        order - list of numerically encoded order
            returns: filtered_psu_dict - only PSUs that contain at leat one relevant item for the order
        '''
        filtered_psu_dict = psu_dict.copy()
        # find useless psus from dict - psus that dont carry any item needed for the given order
        useless_psu = []
        for psu in filtered_psu_dict.keys():
            flag = False
            for item in order:
                if item in filtered_psu_dict[psu]:
                    flag = True
                    break
            if flag == False:
                useless_psu.append(psu)

        # drop useless psus from dict and return filtered psu dict
        for psu in useless_psu:
            filtered_psu_dict.pop(psu)
        filtered_psu_dict[0] = []
        return filtered_psu_dict

    def get_initial_state(self, psu_dict, order):
        '''
        get a random initial state
        parameters: psu_dict - dictionary of PSUs (key) and the numerically encoded items they hold (value)
                    order - list of numerically encoded order
        returns: initial_state - random initial state as a list of length equal to the number of items in order 
                --> idea: we need one PSU for every item in the order (worst case)
        '''
        flag = False
        while not flag:
            # initial_state_idx - list of indices to get PSUs from psu_dict key list
            initial_state_idx = np.random.randint(0,len(psu_dict), len(order))
            if len(set(initial_state_idx)) == len(order):  # check if every PSU is in the list only once
                flag = True

        # get inital state by getting the PSUs from psu_dict key list by initial_state_idx list
        initial_state = [list(psu_dict.keys())[idx] for idx in initial_state_idx]
        return initial_state

    def get_neighbors(self, state, psu_dict):
        '''
        get neighbors of current state
        parameters: state - current state (list of PSUs)
                    psu_dict - filtered dictionary of PSUs (key) and the numerically encoded items they hold (value)
        returns: neighbors - list of all neighboring states of the given current state
                --> idea: neighboring states are states with only one PSU different from current state
        '''
        neighbors = []
        for i in range(len(state)):
            for psu in psu_dict.keys():
                if psu != state[i]:
                    temp_state = state.copy()
                    temp_state[i] = psu
                    neighbors.append(temp_state)
        np.random.shuffle(neighbors) # get some randomness into the neighbor list 
        return neighbors

    def calculate_cost(self, state, psu_dict, order):
        '''
        calculate cost based on number of psus used and order items fulfilled/provided with current state
        parameters: state - current state (list of PSUs)
                    psu_dict - filtered dictionary of PSUs (key) and the numerically encoded items they hold (value)
                    order - list of numerically encoded order
        returns: cost - cost associated with current state based on number of PSUs (non zero PSUs ids in state) 
                        and number of provided items (items of order satisfied by current state)
        '''
        # get list of all unique items in the PSUs of the current state
        items_in_psus = list(set([item for psu in state for item in psu_dict[psu]]))

        # count number of items of the order that are not in items_in_psus (could also use length of difference set here)
        missing_items = 0
        for item in order:
            if item not in items_in_psus:
                missing_items += 1
        state = np.asarray(state)

        # calculate cost 
        cost = missing_items*10 + len(state[state!=0]) # missing items are counted 10 times compared to number of PSUs required
        return cost
        
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
        costs = [self.calculate_cost(neighbor, psu_dict, order) for neighbor in neighbors]
        min_cost = np.amin(costs) # get minimum cost
        idx = np.argmin(costs) # get neighbor index of minimum cost

        # return neighbor with minimum cost or False if min_cost is not lower than current state cost
        if min_cost < self.calculate_cost(state, psu_dict, order): 
            return neighbors[idx]
        else:
            return False

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
        state = np.asarray(state)
        # get number of non zero PSUs in state (where 0 is placeholder for no PSU) 
        num_psus = "Number of PSUs required: " + str(len(state[state!=0]))

        # create result dict - PSUs of result state (keys) and decoded items they carry (values)
        # items that are in the order are casted to upper case for emphasis
        result_dict = {}
        for psu in state:
                result_dict[psu] = [decode_dict[item].upper() if item in order else decode_dict[item] for item in psu_dict[psu]]
        
        # create set of items of the order that are provided by the result state PSUs 
        provided_items = set([item for psu in state for item in psu_dict[psu] if item in order])

        # create a string from result_dict - every line one PSU with its items 
        result_str = ""
        for psu in state:
            if psu != 0:
                result_str += str(psu) + ": "
                for item in result_dict[psu]:
                    result_str += item + ", "
                result_str = result_str[:-2] + " \n"
        
        # create string to summarize number of items of order that are satisfied
        provided_items_str = "Provided Items: {}/{}".format(len(provided_items), len(order))
        
        return provided_items_str, num_psus, result_str

   

    
