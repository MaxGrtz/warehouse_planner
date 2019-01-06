import algorithm
import numpy as np

class Local_Beam_Search(algorithm.Algorithm):
    
    def __init__(self, psu_dict, order, decode_dict, num_start_states):
        '''
        initialize algorithm object with psu_dict, order list and dict to decode items via parent class
        '''
        super().__init__(psu_dict, order, decode_dict)
        self.name = "Local Beam Search"
        self.default = False
        try: 
            self.num_start_states = int(num_start_states.replace(" ", ""))
            if self.num_start_states > 100:
                self.num_start_states = 100
                self.default = True
            elif self.num_start_states < 1:
                self.num_start_states = 1
                self.default = True
        except ValueError:
            self.default = True
            self.num_start_states = 1

    def run(self):
        '''
        method to run the algorithm from the constructed algrotihm object
            returns: post precessed result - provided items, number of psus required, result state, number of initial states
        '''

        # preprocess psu_dict - filter for relevant PSUs 
        psu_dict = self.pre_processing(self.psu_dict, self.order)

        # random initial states
        states = [self.get_initial_state(psu_dict, self.order) for _ in range(self.num_start_states)]

        # costs of initial states
        costs = [self.calculate_cost(state, psu_dict, self.order) for state in states]
        cost_sum = sum(costs)
        min_cost = min(costs)

        flag = True
        while flag:
            # get neighbors of current states, that have lower cost than the lowest cost current state
            neighbors = [nb for state in states for nb in self.get_neighbors(state, psu_dict) if self.calculate_cost(nb, psu_dict, self.order) < min_cost]

            # get n lowest cost states from neighbors and current states
            new_states = self.get_n_min_cost_states(states, neighbors, psu_dict, self.order, self.num_start_states) 
            # calculate new costs
            new_costs = [self.calculate_cost(state, psu_dict, self.order) for state in new_states]

            # if the cumulative cost of the new_states is lower than of the current states, then some improvement occured and we update
            # else end the search
            if sum(new_costs) < cost_sum:
                cost_sum = sum(new_costs)
                min_cost = min(new_costs)
                states = new_states
                costs = new_costs
            else:
                flag = False

        # get state with lowest cost from final list of states
        min_cost_state = states[np.argmin(costs)]

        # return postprocessed results
        provided_items_str, num_psus, result_str = self.post_processing(min_cost_state, self.decode_dict, psu_dict, self.order)
        if self.default:
            default = "default: "
        else:
            default = ""
        num_states = "(" + default + str(self.num_start_states) + " initial states)"
        return provided_items_str, num_psus, result_str, num_states


    def get_n_min_cost_states(self, states, neighbors, psu_dict, order, num_start_states):
        '''
        method to get the n (num_start_states) lowest cost states from neighbors and current states
        parameters: states - current states 
                    neighbors - neighbor states of current states in one list
                    psu_dict - dictionary of items the psus carry
                    order - list of items in the selected order
                    num_start_states - defines number of inital states for local beam search
        returns: n lowest cost states from neighbors and current states

        '''
        # concatenate current states with their neighbors
        for state in states:
            neighbors.append(state)
        
        # calculate costs for every state, save as tuples (state, cost) in list
        costs = np.asarray([(c, self.calculate_cost(nb, psu_dict, order)) for c,nb in enumerate(neighbors)], dtype=[('state', int), ('cost', int)])
        # sort by cost
        sorted_costs = np.sort(costs, order='cost')
        # get n lowest cost (state, cost) tuples
        temp = sorted_costs[:num_start_states]
        # return the n states with lowest cost
        return [neighbors[i[0]] for i in temp]