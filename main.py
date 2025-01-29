# Names: Hendrik DuPont, Jeppe Mul & Nasreddine Ouchene
# This script contains an algorithm that folds a protein. It does so on the basis of a TBD algorithm.
# This script is in partial fulfillment of the requirements for Algoritmen en Heuristieken at the University of Amsterdam.

from classes.protein_class import Protein
from classes.visualise_class import Visualise
from algorithms.algorithm_class import Algorithm
from algorithms.random import Random
from algorithms.random_folding import RandomFolding
from algorithms.beam import Beam
# from algorithms.pull_move_climber import Climber
from algorithms.hill_climber_test import Climber
import argparse
import matplotlib.pyplot as plt

def file_to_parameters(filename):
    """
    Parses the input file and extracts parameters.
    """
    try:
        with open(filename, 'r') as file:
            data = file.readlines()
            sequence = data[0].split('=')[1].strip().upper()
            algorithm = data[1].split('=')[1].strip().lower()
            iterations = int(data[2].split('=')[1].strip())
            lookahead_depth = int(data[3].split('=')[1].strip() or 0)
        return algorithm, sequence, iterations, lookahead_depth
    except (IndexError, ValueError) as e:
        raise ValueError("Invalid input file format. Ensure all fields are correctly specified.") from e

def handle_error_conditions(sequence, algorithm, iterations, lookahead_depth):
    """
    Handles all the validation logic and shows relevant error messages for each input condition.
    Returns True if any error occurs, otherwise False.
    """
    # Validate protein sequence
    if not type(sequence) is str:
        raise TypeError("Please enter a string as a sequence")
    if not sequence:
        raise ValueError("Protein sequence cannot be empty!")
    if len(sequence) < 2:
        raise ValueError("Protein sequence must be longer than 2 amino acids!")
    if any(char not in "HPC" for char in sequence):
        raise ValueError("Protein sequence can only contain 'H', 'P', and 'C'.")

    # Validate algorithm selection
    if algorithm == "":
        raise TypeError("Please select an algorithm.")
    if algorithm == "Hill Climber":
        raise TypeError("Hill Climber not yet implemented. Please select another one.")

    # Validate algorithm-specific entry
    if iterations == None:
        if algorithm == "random":
            raise TypeError("Please enter a value for the iterations.")
        elif algorithm == "beam search":
            raise TypeError("Please enter a value for the beams")
        else:
            print("To be finished")

    if not type(output_file) is str:
        raise TypeError("Please enter a string as a sequence")
    if not type(threeD) is bool:
        raise TypeError("Please enter a boolean for adding a 3rd dimension")

if __name__ == '__main__':

    # parse the input sequence
    parser = argparse.ArgumentParser(description="A script to find the best protein fold")

    parser.add_argument(
    'experiment',
    help="A .txt file containing the paramters that will be used by the algorithm"
    )

    parser.add_argument(
    'output_file',
    help="The name of the csv file to put the data in"
    )

    parser.add_argument(
    '-threeD',
    action= 'store_true',
    help="A flag that changes the algorithm to work in three-dimensional space rather than two-dimensional space"
    )

    # # convert to variables for legibility
    args = parser.parse_args()
    experiment = args.experiment
    output_file = args.output_file
    threeD = args.threeD

    algorithm, sequence, iterations, lookahead_depth = file_to_parameters(experiment)
    handle_error_conditions(sequence, algorithm, iterations, lookahead_depth)

    if algorithm == "random":
        Random(sequence, iterations, output_file, threeD).run_experiment()
    elif algorithm == "random_folding":
        RandomFolding(sequence, iterations, output_file, threeD).run_experiment()
    elif algorithm == "beam search":
        Beam(sequence, iterations, output_file, threeD).run_experiment()
    elif algorithm == "hill climber":
        Climber(sequence, iterations, output_file, threeD).run_experiment()

    plt.show()

     # --------------------------- Random ---------------------------------------
    #Random(sequence, iterations, output_file, threeD).run_experiment()

     # --------------------------- Beam (with lookahead) ---------------------------------------
    # Beam(sequence, iterations, output_file, threeD).run_experiment()
    # #plt.show()
    #
    # P = Protein('HHPH', 'output.csv', False)
    # P.add_coordinate(P.amino_acids, (1,1,0), 'P')
    # P.add_coordinate(P.amino_acids, (2,1,0), 'H')
    #

    #Climber(sequence, iterations, output_file, threeD, P).run()

    #test =Climber(sequence, iterations, output_file, threeD, P)

    #print(test.is_legal([(1,-1,0),(1,0,0),(1,1,0),(2,1,0)]))
