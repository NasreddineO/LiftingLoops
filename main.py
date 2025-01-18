# Names: Hendrik DuPont, Jeppe Mul & Nasreddine Ouchene
# This script contains an algorithm that folds a protein. It does so on the basis of a TBD algorithm.
# This script is in partial fulfillment of the requirements for Algoritmen en Heuristieken at the University of Amsterdam.

from classes.protein_class import Protein
from classes.visualise_class import Visualise
from algorithms.algorithm_class import Algorithm
from algorithms.random import Random
from algorithms.random_greedy import Random_Greedy
from algorithms.beam import Beam
import argparse
import matplotlib.pyplot as plt

if __name__ == '__main__':

    # parse the input sequence
    parser = argparse.ArgumentParser(description="A script to find the best protein fold")

    parser.add_argument(
    'sequence',
    help="An ordered string of letters, where each different letter stands for an amino acid of the type indicated by that letter"
    )

    parser.add_argument(
    'iterations',
    help="The number of iterations to run the experiment"
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

    # convert to variables for legibility
    args = parser.parse_args()
    sequence = args.sequence
    iterations = int(args.iterations)
    output_file = args.output_file
    threeD = args.threeD

    # check for correct input types:
    if not type(sequence) is str:
        raise TypeError("Please enter a string as a sequence")

    if not len(sequence) > 1:
        raise ValueError("Please enter a sequence of more than 1 amino acid. A sequence with only 1 amino acid is not a protein.")

    if not type(iterations) is int:
        raise TypeError("Please enter an integer")

    if not type(output_file) is str:
        raise TypeError("Please enter a string as a sequence")

    if not type(threeD) is bool:
        raise TypeError("Please enter a boolean for adding a 3rd dimension")

     # --------------------------- Random ---------------------------------------
    Random(sequence, iterations, output_file, threeD).run_experiment()

     # --------------------------- Beam (with lookahead) ---------------------------------------
    Beam(sequence, iterations, output_file, threeD).run_experiment()
    plt.show()
