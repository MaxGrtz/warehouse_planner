# Warehouse-Planning Project

## 1. Goal: 
    - development of a simple warehouse planning system based on local search algorithms with a graphical user interface.
    - for a given warehouse configuration, the goal is to find a combination of portable storage units (PSUs) that:
        -> provides all items of a given order
        -> minimizes the number of PSUs required to fulfill the order

## 2. Input: 
    - two textfiles and choice of algorithm
    - problem.txt file that contains an inventory and a list of PSUs, each associated with a list of items they store 
    - order.txt file that contains items of that order
    - buttons provide a means of choosing the desired algorithm for solving the given problem
    - text box to enter the number of start states for random restart hill climbing and local beam search

## 3. Output: 
    - local search result state
    - number of items of the order that are provided 
    - number of PSUs required to provide all items of the order
    - list of result state PSUs and the items of the order they provide

## 4. General information and requirements: 
    - Python 3.7x
    - dependecies are specified in the requirements.txt file
    - either install dependencies yourself or install the latest version of pip
    - if Python and pip are up to date, follow the instructions upon starting the application to install dependencies automatically
    - run the application with >> python warehouse_app.py

## 5. Code Structure overview:
###     warehouse_app.py 
    contains the main script: 
        -> handles the automatic dependency installation 
        -> runs a main loop for the Gui object created
###     gui.py 
    contains the Gui class:
        -> upon initialization the user interface is created
        -> two buttons for initiating filedialogs for loading the problem.txt and order.txt files
        -> buttons allow to choose one of the local search algorithms implemented
        -> labels used to display status information and results
###     file_parser.py 
    contains two functions for parsing the input files:
        -> read_problem: parses chosen problem.txt file
        -> read_order: parses chosen order.txt file
###     algorithm.py
    contains Algorithm class for defining general functions used by all/most algorithms:
        -> get_initial_state: creates a random inital state
        -> get_neighbors: returns neighbors of given state
        -> calculate_cost: calculates costs of a given state
        -> get_min_cost_neighbor: returns the neighbor with lowest costs
        -> post_processing: translates algorithms results into string (to display result on Gui)
###     hill_climbing.py, first_choice_hill_climbing.py, simulated_annealing.py, random_restart_hill_climbing.py, local_beam_search.py
    contain classes inheriting from the Algorithm class:
        -> are initialized with the information from the input files 
        -> contain a run method that implements the corresponding algorithm
        -> make use of the shared functions of the Algorithm class 
        -> return the postprocessed solution states
###     comparator.py
    contains comparator class:
        -> upon calling compare_all, instatiates all different algorithms and executes them
        -> tracks results and lets you download the a .csv file containing an overview

## 6. Problem Representation:
###     representation of warehouse configuration
    - the problem.txt file contains the warehouse configuration
    - this information is stored in a PSU dictionary with:
        -> keys: the PSU ids (line in problem.txt file) 
        -> values: a list of items the PSU carries 
    - also encode/decode dictionaries are used to create a numerical encoding/decoding of all items
###     representation of the order
    - the order.txt file contains items of the order
    - items are encoded using the created encode_dict and safed in a list 
###     filtered psu dictionary
    - the order list is used to filter the PSU dictionary created from the problem.txt file
    - only keeping PSUs that contain at least one item of the order
    - only keeping items that are in the order
###     state representation
    - observation: in the worst case we need as many PSUs as there are items in the order
    - a state is therefore represented by a list of PSU ids of the same length as the order
    - zeros in the state represent "no PSU" (allows for the state to consist of less PSUs, maintaining a constant state length)
###     neighborhood definition
    - the neighborhood is defined by all states that differ from the current state in exactly one position
###     cost definition
    - the costs of a state are defined by two aspects:
        -> missing_items: number of items not provided by the current state (goal: provide all items of order)
        -> num_psus: number of PSUs used by the state to provide the order items (goal: minimize PSUs used)
    - since it is more important to provide all items than to minimize the PSUs used, both factors are weighed differently
    - cost = 10*(missing_items) + num_psus

## 7. Critical Assessment:
###     problem/state representation:
    - the chosen state representation is only useful for fairly small orders, but performs well in this domain
    - the reasoning behind the choice of the state representation was as follows:
        -> the most obvious choice was to use a binary array (length - num PSUs) that represents the state and the index the PSU ids
        -> the value indicates wheher the PSU is part of the id or not
        -> the idea was to condense this representation by only saving the indices of the one values in this array
        -> we reasoned that we could restrict the length of the state to the number of items in the order,
           since in the worst case we would need as many PSUs as there are items in the order 
    - Problems: 
        -> for every additional item in the order the neighborhood of a state increases by the number of considered PSUs
        -> this leads to an extreme decline in performance and worse results (because of the increasingly complex/big neighborhoods)
    - alternative solution:
        -> represent a state by a binaray or boolean numpy array
        -> every position in such a state corresponds to a PSU 
        -> the value indicates if the PSU is part of the current state or not
        -> the size of the neighborhood (only one value is flipped) then only depends on the number of PSUs considered
            - neighborhood size is invariant under change of order size
        -> all calculations for example can be performed on a boolean matrix, where:
            - the rows represent order items (row 1 ~ order item 1)
            - the columns represent PSUs (column 1 ~ PSU 1)
            - it captures the distribution of order items in the PSUs
            - by filtering for PSUs in the current state one can easily check:
                -> the number of PSUs used (number of columns)
                -> the number of order items provided (np.any() on corresponding axis and sum over result vector)
        -> we tested an implementation of this for hill_climbing:
            - it performed worse for small orders
            - but showed less decline in performance with an increase of items in the order
    - another idea could be to restrict the neighborhood in our implementation by subsampling 
      or just considering changes to the current state in one random position (instead of all positions)
        -> here we have to consider a tradeoff between computation times and quality of results


