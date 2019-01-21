# warehouse planning project

## Goal: development of a simple warehouse planning system based on local search algorithms with a graphical user interface.
    - for a given warehouse configuration, the goal is to find a combination of portable storage units (PSUs) that:
        a) provides all items of a given order
        b) minimizes the number of PSUs required to fulfill the order

## Input: two text-files and choice of algorithm
    - problem.txt file that contains an inventory and a list of PSUs, each associated with a list of items they store 
    - order.txt file that contains items of that order
    - buttons provide a means of chooing the desired algorithm for solving the given problem

## Output: local search result state
    - number of items of the order that are provided 
    - number of PSUs required to provide all items of the order
    - list of specific PSUs and the items of the order they provide

## General information and requirements for execution of the application: 
    - Python 3.7x
    - dependecies are specified in the requirements.txt file
    - either install dependencies yourself or install the latest version of pip
    - if Python and pip are up to date, follow the instructions upon starting the application to install dependencies automatically
    - run the application with >> python warehouse_app.py

## Code Structure overview:
###    - warehouse_app.py file contains the main script: 
        -> handles the automatic dependency installation 
        -> runs a main loop for the Gui object created
###    - gui.py file contains the Gui class
        -> upon initialization the user interface is created
        -> two buttons for initiating filedialogs for loading the problem.txt and order.txt files
        -> buttons allow to choose one of the local search algorithms implemented
###    - file_parser.py contains to functions for parsing the input files
        -> read_problem: parses chosen problem.txt file
        -> read_order: parses chosen order.txt file

            




main: script for running the application

gui class: class for graphical user interface 
    - 3 frames: data input, algorithm, output

parser class:
    - parse data input after reading (problem, order)

algorithm class: parent algorithm class
    - preprocessing
    - common functions (eg. get neighbors)
    - postprocessing

specific algorithm subclasses: algorithms with run method
    - Hill-Climbing
    - First-Choice Hill-Climbing
    - Parallel Hill-Climbing
    - Simulated Annealing
    - Local Beam Search
    - Comparison (all algorithms with timing as csv download)

