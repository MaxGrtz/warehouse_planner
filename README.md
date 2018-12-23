# warehouse_planner

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

