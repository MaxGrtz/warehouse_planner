from tkinter import Tk, Frame, Label, Button, Entry, GROOVE, N,S, W, LEFT, StringVar, filedialog
import file_parser, hill_climbing, first_choice_hill_climbing, simulated_annealing, random_restart_hill_climbing, local_beam_search, comparator
import time
import numpy as np

class Gui(object):

    def __init__(self, window):
        '''
        create graphical user interface
        '''
        self.window = window
        # dictionary of algortihms for numeric encoding
        self.algorithms = { 1: "Hill-Climbing", 
                            2: "First-Choice Hill-Climbing",
                            3: "Simulated Annealing",
                            4: "Random Restart Hill-Climbing",
                            5: "Local Beam search" }
        # window config
        window.title("Warehouse Planner") 
        window.geometry('1400x400')
        window.grid_columnconfigure(3, minsize=50)
        window.grid_rowconfigure(4, minsize=20)
        window.grid_rowconfigure(11, minsize=20)


        # initialize input related buttons and labels
        self.problem_file_name = StringVar() # contains the file name of the problem.txt file chosen 
        self.problem_file_name.set("Problem FilePath")
        self.order_file_name = StringVar() # contains the file name of the order.txt file chosen 
        self.order_file_name.set("Order FilePath")
        # heading label
        Label(window, text="Input Files", font=("Arial Bold", 15)).grid(column=1, row=1)
        # problem button and label
        Button(window, text="Browse problem .txt file", command=self.load_problem, width=20).grid(column=1, row=2)
        Label(window, textvariable=self.problem_file_name, width=20).grid(column=2, row=2)
        # order button and label
        Button(window, text="Browse order .txt file", command=self.load_order, width=20).grid(column=1, row=3)        
        Label(window, textvariable=self.order_file_name, width=20).grid(column=2, row=3)

        # ouput variables and labels
        self.status = StringVar() # contains information about the status of the programm
        self.status.set("")
        self.provided_items = StringVar() # contains information about how many items of the order are provided with the current solution
        self.provided_items.set("")
        self.num_psus = StringVar() # contains number of PSUs required for current solution
        self.num_psus.set("")
        self.result_dict = StringVar() # contains all PSUs required for solution and the items they carry
        self.result_dict.set("")
        Label(window, text="Output", font=("Arial Bold", 15)).grid(column=4, row=1)
        Label(window, textvariable=self.status).grid(column=4, row=2)
        Label(window, textvariable=self.provided_items).grid(column=4, row=4)
        Label(window, textvariable=self.num_psus).grid(column=4, row=5)
        Label(window, textvariable=self.result_dict, anchor=W, justify=LEFT).grid(column=4, row=7, rowspan=50, columnspan=5)

        # initialize algorithm related buttons, labels and entry-fields
        self.n_states_parallel = Entry(window, width=20) # input number of start states for parallel hill climbing
        self.n_states_parallel.grid(column=1, row=9)
        self.n_states_beam = Entry(window, width=20) # input number of start states for local beam search
        self.n_states_beam.grid(column=1, row=10)
        Label(window, text="Algorithm Input", font=("Arial Bold", 15), width=20).grid(column=1, row=5)
        Label(window, text="Choose Algorithm", font=("Arial Bold", 15)).grid(column=2, row=5)
        Button(window, text=self.algorithms[1], command=lambda: self.choose_algorithm(1), width=25).grid(column=2, row=6)
        Button(window, text=self.algorithms[2], command=lambda: self.choose_algorithm(2), width=25).grid(column=2, row=7)
        Button(window, text=self.algorithms[3], command=lambda: self.choose_algorithm(3), width=25).grid(column=2, row=8)
        Button(window, text=self.algorithms[4], command=lambda: self.choose_algorithm(4), width=25).grid(column=2, row=9)
        Button(window, text=self.algorithms[5], command=lambda: self.choose_algorithm(5), width=25).grid(column=2, row=10)
        Button(window, text="download comparison.csv", command=lambda: self.choose_algorithm(6), width=25).grid(column=2, row=12)
        

    def load_problem(self):
        '''
        method to initiate filedialog for reading problem.txt file
        creates encoding, decoding and psu dictionaries:
            - encoding_dict: dictionary for encoding item names into numeric values
            - decoding_dict: dictionary for decoding item names from numeric into string
            - psu_dict: dictionary with psu id as key and the list of items they carry as value 
        '''
        # get filepath via filedialog
        problem = filedialog.askopenfilename(filetypes=[("problemfiles", "*.txt")]) 
        # reset order, problem path and status
        self.order = None
        self.order_file_name.set("Order FilePath")
        self.problem_file_name.set("Problem FilePath")
        self.status.set("")
        # parse the problem file to create encoding, decoding and psu doctionaries
        self.encode_dict, self.decode_dict, self.psu_dict = file_parser.read_problem(problem)   
        if self.encode_dict is not None:
            self.problem_file_name.set("..." + problem[-19:]) # set label to filename
        else:
            self.status.set("Please select a problem file with the correct format and structure!")
        # reset output labels to empty strings
        self.provided_items.set("")
        self.num_psus.set("")
        self.result_dict.set("")

    def load_order(self):
        '''
        method to initiate filedialog for reading order.txt file
        creates order and missing item lists:
            - order: list of (valid) items in the order encoded numerically
            - missing_items: list of items from the order which are not in the inventory of the given problem.txt file
        '''
        try:
            # read the order file via filedoalog
            order = filedialog.askopenfilename(filetypes=[("orderfiles", "*.txt")])
            # parse the order file to get numerically encoded order and filter out items that are not in the inventory
            self.order, self.missing_items = file_parser.read_order(order, self.encode_dict)
            if self.order is not None:
                self.order_file_name.set("..." + order[-18:]) # set label to filename
                # preprocess psu_dict: only relevant psus and items in psu lists are considered in the execution of the algorithms
                self.filtered_psu_dict = self.pre_processing(self.psu_dict, self.order)
                if self.missing_items:
                    # show items that are not in the inventory on the status label
                    self.status.set("Invalid order, solved by ignoring following items, which are not in the inventory: {}".format(self.missing_items))
                else:
                    self.status.set("")
                    self.missing_items = "None"
            else:
                self.status.set("Please select an order file with the correct format and structure!")
            # reset output labels to empty strings
            self.provided_items.set("")
            self.num_psus.set("")
            self.result_dict.set("")
        except (AttributeError, TypeError) as e:
            # if self.encode_dict does not yet exist or is None, no problem file is selected
            self.status.set("Please select a problem file first!")

    def choose_algorithm(self, name):
        '''
        method for choosing and running the correct algorithm (depending on the button used to call the method)
        it updates the output labels of the GUI with the result of the chosen algorithm
        '''
        try:
            start = time.time() # for timing
            n_states = ""
            if name == 1:
                # hill climbing
                alg = hill_climbing.Hill_Climbing(self.filtered_psu_dict, self.order, self.decode_dict)
                provided_items_str, num_psus, result_str = alg.run()
            elif name == 2:
                # first choice hill climbing
                alg = first_choice_hill_climbing.First_Choice_Hill_Climbing(self.filtered_psu_dict, self.order, self.decode_dict)
                provided_items_str, num_psus, result_str = alg.run()
            elif name == 3:
                # simulated annealing
                alg = simulated_annealing.Simulated_Annealing(self.filtered_psu_dict, self.order, self.decode_dict)
                provided_items_str, num_psus, result_str = alg.run()
            elif name == 4:
                # parallel hill climbing with n start states
                alg = random_restart_hill_climbing.Random_Restart_Hill_Climbing(self.filtered_psu_dict, self.order, self.decode_dict, self.n_states_parallel.get())
                provided_items_str, num_psus, result_str, n_states = alg.run()
            elif name == 5:
                # local beam search with n start states
                alg = local_beam_search.Local_Beam_Search(self.filtered_psu_dict, self.order, self.decode_dict, self.n_states_beam.get())
                provided_items_str, num_psus, result_str, n_states = alg.run()
            elif name == 6:
                comparison = comparator.Comparator(self.filtered_psu_dict, self.order, self.decode_dict)
                comparison.compare_all()
                path = filedialog.asksaveasfilename(defaultextension=".csv")
                comparison.download(path)
            
            end = time.time() # for timing
            # calculate duration of the algorithm execution
            duration = "  [duration: " + str(np.round(end-start, decimals=4)) + " sec.]"

            # update labels with local search result
            if name == 6:
                self.status.set("done with Comparison - downloaded to: {}...{}".format(path[:30],path[-30:]))
                self.provided_items.set("")
                self.num_psus.set("")
                self.result_dict.set("")
            else:
                self.status.set("done with {} {} - ignored items: {}".format(self.algorithms[name], n_states, self.missing_items))
                self.provided_items.set(provided_items_str + duration)
                self.num_psus.set(num_psus)
                self.result_dict.set(result_str)
        except AttributeError:
            self.status.set("Please select valid problem and order files first!")


    def pre_processing(self, psu_dict, order):
        '''
        filters psu_dict for relevant psus (psus that contain at least one item from the order) and items (only items that are in the order)
            parameters: psu_dict - complete dictionary of PSUs (key) and the numerically encoded items they hold (value)
                        order - list of numerically encoded order
            returns: filtered_psu_dict - only PSUs that contain at leat one relevant item for the order
        '''
        # filter psu_dict by relevant psus (intersection between order and items in psu is > 0) and items (items that are in the order)
        filtered_psu_dict = {key: list(set(val).intersection(set(order))) for key, val in psu_dict.items() if len(set(order).intersection(set(val))) > 0}
        filtered_psu_dict[0] = [] # add zero key as placeholder for no psu

        #return filtered psu_dic    
        return filtered_psu_dict




