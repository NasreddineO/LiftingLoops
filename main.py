# Names: Hendrik DuPont, Jeppe Mul & Nasreddine Ouchene
# This script contains an algorithm that folds a protein. It does so on the basis of a TBD algorithm.
# This script is in partial fulfillment of the requirements for Algoritmen en Heuristieken at the University of Amsterdam.

from classes.protein_class import Protein
from algorithms.algorithm_class import Algorithm
from algorithms.random import Random
import argparse

if __name__ == '__main__':

    # parse the input sequence
    parser = argparse.ArgumentParser(description="A script to find the best protein fold")

    parser.add_argument(
    'sequence',
    help="An ordered string of letters, where each different letter stands for an amino acid of the type indicated by that letter"
    )

    parser.add_argument(
    'output_file',
    help="The name of the csv file to put the data in"
    )

    parser.add_argument(
    '-threeD',
    action= 'store_true',
    help="A flag that changes the algorithm to work in three-dimensional space rather than two-dimensional space."
    )



    # convert to variables for legibility
    args = parser.parse_args()
    sequence = args.sequence
    output_file = args.output_file
    threeD = args.threeD



    # check for correct input types:
    if not type(sequence) is str:
        raise TypeError("Please enter a string as a sequence")

    if not type(output_file) is str:
        raise TypeError("Please enter a string as a sequence")

    if not type(threeD) is bool:
        raise TypeError("Please enter a boolean for adding a 3rd dimension")



    # initialize Protein
    P = Protein(sequence, output_file, threeD)

    # initialize an algorithm
    algorithm = Random(P)

    # run the algorithm for each node to add
    for amino_acid in algorithm.protein.sequence[2:]:
        algorithm.step(algorithm.protein.amino_acids, amino_acid)

    algorithm.finish_up(output_file)
