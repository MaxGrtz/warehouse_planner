import hill_climbing, first_choice_hill_climbing, simulated_annealing, parallel_hill_climbing, local_beam_search
import time
import pandas as pd
import numpy as np

class Comparator(object):
    '''
    Class to compare all algorithms
    '''
    def __init__(self, psu_dict, order, decode_dict):
        self.psu_dict = psu_dict
        self.order = order
        self.decode_dict = decode_dict

    def compare_all(self):
        # create algorithm instances 
        hill_climbing_alg = hill_climbing.Hill_Climbing(self.psu_dict, self.order, self.decode_dict)
        first_choice_hill_climbing_alg = first_choice_hill_climbing.First_Choice_Hill_Climbing(self.psu_dict, self.order, self.decode_dict)
        simulated_annealing_alg = simulated_annealing.Simulated_Annealing(self.psu_dict, self.order, self.decode_dict)
        algorithms = [hill_climbing_alg, first_choice_hill_climbing_alg, simulated_annealing_alg]
        n_start_states = ["25","50","75","100"]  # algorithm instances with different number of start states
        for n in n_start_states:
            algorithms.append(parallel_hill_climbing.Parallel_Hill_Climbing(self.psu_dict, self.order, self.decode_dict, n))
            
        for n in n_start_states:
            algorithms.append(local_beam_search.Local_Beam_Search(self.psu_dict, self.order, self.decode_dict, n))

        # create comparison result dict
        result_dict = {}
        for alg in algorithms:
            start = time.time()
            try:
                provided_items_str, num_psus, result_str = alg.run()
            except:
                provided_items_str, num_psus, result_str, n_states = alg.run()
                alg.name = alg.name + " " + n_states
            end = time.time()
            items_provided = provided_items_str[16:].split('/') # get number of provided items and number of items in order from returned str
            # for every algorithm safe in dict: percentage of provided items, number of psus used, time needed for calculation
            result_dict[alg.name] = [int(items_provided[0])/int(items_provided[1])*100, num_psus[-2:], np.round(end-start, decimals=4)]
        # create result dataframe
        self.result = pd.DataFrame.from_dict(result_dict, orient='index', columns=["items provided [%]","number of PSUs required", "duration [sec.]"])



    def download(self, path):
        '''
        safe result dataframe as .cvs file
        parameter: path - path to which to safe the file
        '''
        self.result.to_csv(path)