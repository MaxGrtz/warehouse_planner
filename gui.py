from tkinter import Tk, Frame, Label, Button, Entry, GROOVE, N,S, W, LEFT, StringVar
from tkinter import filedialog
import parser, hill_climbing, first_choice_hill_climbing, simulated_annealing, parallel_hill_climbing, local_beam_search
import time

class Gui(object):

    def __init__(self, window):
        '''
        create graphical user interface consisting of three components: input, algorithm and output 
        '''
        self.window = window
        # dictionary of algortihms for numeric encoding
        self.algorithms = { 1: "Hill-Climbing", 
                            2: "First-Choice Hill-Climbing",
                            3: "Simulated Annealing",
                            4: "Parallel Hill-Climbing",
                            5: "Local Beam search" }
        # window config
        window.title("Warehouse Planner") 
        window.geometry('1400x400')
        window.grid_columnconfigure(3, minsize=50)
        window.grid_rowconfigure(4, minsize=20)

        # initialize input related buttons and labels
        self.problem_file_name = StringVar() # contains the file name of the problem.txt file chosen 
        self.problem_file_name.set("Problem FilePath")
        self.order_file_name = StringVar() # contains the file name of the order.txt file chosen 
        self.order_file_name.set("Order FilePath")
        file_label = Label(window, text="Input Files", font=("Arial Bold", 15)).grid(column=1, row=1)
        # problem button and label
        problem_btn = Button(window, text="Browse problem .txt file", command=self.load_problem, width=20).grid(column=1, row=2)
        problem_lbl = Label(window, textvariable=self.problem_file_name, width=20).grid(column=2, row=2)
        # order button and label
        order_btn = Button(window, text="Browse order .txt file", command=self.load_order, width=20).grid(column=1, row=3)        
        order_lbl = Label(window, textvariable=self.order_file_name, width=20).grid(column=2, row=3)

        # ouput variables and labels
        self.status = StringVar() # contains information about the status of the programm
        self.status.set("")
        self.provided_items = StringVar() # contains information about how many items of the order are provided with the current solution
        self.provided_items.set("")
        self.num_psus = StringVar() # contains number of PSUs required for current solution
        self.num_psus.set("")
        self.result_dict = StringVar() # contains all PSUs required for solution and the items they carry
        self.result_dict.set("")
        solution_lbl = Label(window, text="Output", font=("Arial Bold", 15)).grid(column=4, row=1)
        lbl_status = Label(window, textvariable=self.status).grid(column=4, row=2)
        label_provided_items = Label(window, textvariable=self.provided_items).grid(column=4, row=4)
        label_num_psu = Label(window, textvariable=self.num_psus).grid(column=4, row=5)
        label_result_dict = Label(window, textvariable=self.result_dict, anchor=W, justify=LEFT).grid(column=4, row=7, rowspan=50, columnspan=5)

        # initialize algorithm related buttons, labels and entry-fields
        input_lbl = Label(window, text="Algorithm Input", font=("Arial Bold", 15), width=20).grid(column=1, row=5)
        self.n_states_parallel = Entry(window, width=20).grid(column=1, row=9) # input number of start states for parallel hill climbing
        self.n_states_beam = Entry(window, width=20).grid(column=1, row=10) # input number of start states for local beam search
        algorithm_lbl = Label(window, text="Choose Algorithm", font=("Arial Bold", 15)).grid(column=2, row=5)
        btn_1 = Button(window, text=self.algorithms[1], command=lambda: self.choose_algorithm(1), width = 20).grid(column=2, row=6)
        btn_2 = Button(window, text=self.algorithms[2], command=lambda: self.choose_algorithm(2), width = 20).grid(column=2, row=7)
        btn_3 = Button(window, text=self.algorithms[3], command=lambda: self.choose_algorithm(3), width = 20).grid(column=2, row=8)
        btn_4 = Button(window, text=self.algorithms[4], command=lambda: self.choose_algorithm(4), width = 20).grid(column=2, row=9)
        btn_5 = Button(window, text=self.algorithms[5], command=lambda: self.choose_algorithm(5), width = 20).grid(column=2, row=10)

        

    def load_problem(self):
        '''
        method to initiate filedialog for reading the selected problem.txt file
        creates encoding, decoding and psu dictionaries
            - encoding_dict: dictinary for encoding item names into numeric values
            - decoding_dict: dictionary for decoding item names from numeric into string
            - psu_dict: dictionary with psu id as key and the list of items they carry as value 
        '''
        # read file via filedialog
        problem = filedialog.askopenfilename(filetypes=[("problemfiles", "*.txt")]) 
        # parse the problem file to create encoding, decoding and psu doctionaries
        self.encode_dict, self.decode_dict, self.psu_dict = parser.read_problem(problem)   
        if not self.encode_dict is None:
            self.problem_file_name.set("..." + problem[-19:]) # set label to filename
        # reset output labels to empty strings
        self.provided_items.set("")
        self.num_psus.set("")
        self.result_dict.set("")

    def load_order(self):
        '''
        method to initiate filedialog for reading the selected order.txt file
        creates order and missing item lists
            - order: list of (valid) items in the order encoded numerically
            - missing_items: list of items from the order which are not in the inventory of the given problem.txt file
        '''
        # if there is an encoding dict - ie. a problem is already loaded, initiate filedialog for order file
        if not self.encode_dict is None:
            # read the order file via filedoalog
            order = filedialog.askopenfilename(filetypes=[("orderfiles", "*.txt")])
            # parse the order file to get numerically encoded order and filter out items that are not in the inventory
            self.order, self.missing_items = parser.read_order(order, self.encode_dict)
            if not self.order is None:
                self.order_file_name.set("..." + order[-18:]) # set label to filename
                if self.missing_items:
                    # show items that are not in the inventory in the status label
                    self.status.set("Invalid order, solved by ignoring following items, which are not in the inventory: {}".format(self.missing_items))
                else:
                    self.status.set("")
            # reset output labels to empty strings
            self.provided_items.set("")
            self.num_psus.set("")
            self.result_dict.set("")

    def choose_algorithm(self, name):
        '''
        method for choosing and calling the correct algorithm (depending on the button used to call the method)
        given the outputs of the respective algortihms, the method updates the output labels of the GUI
        '''
        self.status.set("running {} ...".format(self.algorithms[name]))
        if name == 1:
            # hill climbing
            alg = hill_climbing.Hill_Climbing(self.psu_dict, self.order, self.decode_dict)
            provided_items_str, num_psus, result_str = alg.run()
        elif name == 2:
            # first choice hill climbing
            alg = first_choice_hill_climbing.First_Choice_Hill_Climbing(self.psu_dict, self.order, self.decode_dict)
            provided_items_str, num_psus, result_str = alg.run()
        elif name == 3:
            # simulated annealing
            alg = simulated_annealing.Simulated_Annealing(self.psu_dict, self.order, self.decode_dict)
            provided_items_str, num_psus, result_str = alg.run()
        elif name == 4:
            # parallel hill climbing with n start states
            alg = parallel_hill_climbing.Parallel_Hill_Climbing(self.psu_dict, self.order, self.decode_dict, self.n_states_parallel)
            provided_items_str, num_psus, result_str = alg.run()
        elif name == 5:
            # local beam search with n start states
            alg = local_beam_search.Local_Beam_Search(self.psu_dict, self.order, self.decode_dict, self.n_states_beam)
            provided_items_str, num_psus, result_str = alg.run()

        # update labels with local search result
        self.provided_items.set(provided_items_str)
        self.num_psus.set(num_psus)
        self.result_dict.set(result_str)
        self.status.set("done with {} - ignored items: {}".format(self.algorithms[name], self.missing_items))
    



