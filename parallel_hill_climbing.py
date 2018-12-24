import hill_climbing

class Parallel_Hill_Climbing(hill_climbing.Hill_Climbing):
    '''
    Parallel hill climbing inherited from hill climbing - make use of method for getting least cost nieghbor
    '''
    
    def __init__(self, psu_dict, order, decode_dict, num_start_states):
        '''
        initialize algorithm object with psu_dict, order list and dict to decode items via parent class
        '''
        super().__init__(psu_dict, order, decode_dict)
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

        results = []
        for i in range(self.num_start_states):
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
                new_state = self.get_min_cost_neighbor(neighbors, psu_dict, self.order, state) 
                if new_state == False:
                    flag = False
                else:
                    state = new_state # update state with new state 
            # safe result state for iteration
            results.append(state)

        # get result from list with lowest cost
        min_cost_state = self.get_min_cost_neighbor(results, psu_dict, self.order, results[0])
        if min_cost_state == False:
            min_cost_state = results[0]
        # return postprocessed results
        provided_items_str, num_psus, result_str = self.post_processing(min_cost_state, self.decode_dict, psu_dict, self.order)
        if self.default:
            default = "default: "
        else:
            default = ""
        num_states = "(" + default + str(self.num_start_states) + " initial states)"
        return provided_items_str, num_psus, result_str, num_states

