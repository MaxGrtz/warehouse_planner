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

    def run(self):
        '''
        method to run the algorithm from the constructed algrotihm object
            returns: post precessed result - rovided items, number of psus required, result state
        '''
        # preprocess psu_dict - filter for relevant PSUs 
        psu_dict = self.pre_processing(self.psu_dict, self.order)

        # get random initial state 
        state = self.get_initial_state(psu_dict, self.order)

        # actual algorithm
        # in every iteration get neighbors of current state and select neighbor with lowest cost
        # done if there is no neighbor with lower cost than current state
        flag = True
        while flag:
            # get nieghbors of current state
            neighbors = self.get_neighbors(state, psu_dict) 

            # get lowest cost neighbor or False if there is no neighbor with lower cost than current state
            result = self.get_min_cost_neighbor(neighbors, psu_dict, self.order, state) 
            if result == False:
                flag = False
            else:
                state = result # update state with new state 
        # return postpreocessed result
        return self.post_processing(state, self.decode_dict, psu_dict, self.order)
    

    def get_min_cost_neighbor(self, neighbors, psu_dict, order, state):
        '''
        method to get neighbor with lowest cost 
        parameters: neighbors - neighbors of current state
                    psu_dict - filtered dictionary of PSUs (key) and the nuerically encoded items they hold (value)
                    order - list of numerically encoded order
                    state - current state 
        returns: least cost neighbor or False if no neighbor has lower cost than current state
        '''
        # calculate cost of all neighbors
        costs = [self.calculate_cost(neighbor, psu_dict, order) for neighbor in neighbors]
        min_cost = np.amin(costs) # get minimum cost
        idx = np.argmin(costs) # get neighbor index of minimum cost

        # return neighbor with minimum cost or False if min_cost is not lower than current state cast
        if min_cost < self.calculate_cost(state, psu_dict, order): 
            return neighbors[idx]
        else:
            return False