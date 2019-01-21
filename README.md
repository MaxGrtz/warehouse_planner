# warehouse planning project

## Goal: 
development of a simple warehouse planning system based on local search algorithms with a graphical user interface.
    - for a given warehouse configuration, the goal is to find a combination of portable storage units (PSUs) that:
        a) provides all items of a given order
        b) minimizes the number of PSUs required to fulfill the order

## Input: 
two text-files and choice of algorithm
    - problem.txt file that contains an inventory and a list of PSUs, each associated with a list of items they store 
    - order.txt file that contains items of that order
    - buttons provide a means of chooing the desired algorithm for solving the given problem

## Output: 
local search result state
    - number of items of the order that are provided 
    - number of PSUs required to provide all items of the order
    - list of specific PSUs and the items of the order they provide

## General information and requirements: 
    - Python 3.7x
    - dependecies are specified in the requirements.txt file
    - either install dependencies yourself or install the latest version of pip
    - if Python and pip are up to date, follow the instructions upon starting the application to install dependencies automatically
    - run the application with >> python warehouse_app.py

## Code Structure overview:
###     warehouse_app.py 
    contains the main script: 
        -> handles the automatic dependency installation 
        -> runs a main loop for the Gui object created
###     gui.py 
    contains the Gui class
        -> upon initialization the user interface is created
        -> two buttons for initiating filedialogs for loading the problem.txt and order.txt files
        -> buttons allow to choose one of the local search algorithms implemented
        -> labels used to display status information and results
###     file_parser.py 
    contains two functions for parsing the input files
        -> read_problem: parses chosen problem.txt file
        -> read_order: parses chosen order.txt file
###     algorithm.py
    contains Algorithm class for defining general functions used by all/most algorithms
        -> get_initial_state: creates a random inital state
        -> get_neighbors: returns neighbors of given state
        -> calculate_cost: calculates costs of a given state
        -> get_min_cost_neighbor: returns the neighbor with lowest costs
        -> post_processing: translates algorithms results into string (to display result on Gui)
###     hill_climbing.py, first_choice_hill_climbing.py, simulated_annealing.py, random_restart_hill_climbing.py, local_beam_search.py
    contain classes inheriting from the Algorithm class
        -> are initialized with the information from the input files 
        -> contain a run method that implements the corresponding algorithm
        -> make use of the shared functions of the Algorithm class 
        -> return the postprecessed solution states
###     comparator.py
    contains Comparator class
        -> upon calling compare_all, instatiates all different algorithms and executes them
        -> tracks results and lets you download the a .csv file containing an overview

## Problem Representation:
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
    - a state is therefore is represented by a list of PSU ids of the same length as the order
    - zeros in the state represent "no PSU" (allows for the state to consist of less PSUs, maintaining a constant state length)
###     neighborhood definition
    - the neighborhood is defined by all states that differ from the current state in max. one position
###     cost definition
    - the costs of a state are defined by two aspects:
        -> missing_items: number of items not provided by the current state (goal: provide all items of order)
        -> num_psus: number of PSUs used by the state to provide the order items (goal: minimize PSUs used)
    - since it is more important to provide all items that to minimize the PSUs used, both factors are weighed differently
    - cost = 10*(missing_items) + num_psus




