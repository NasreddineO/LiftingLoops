# Names: Hendrik DuPont, Jeppe Mul & Nasreddine Ouchene
# This script contains an algorithm that folds a protein. It does so on the basis of a TBD algorithm.
# This script is in partial fulfillment of the requirements for Algoritmen en Heuristieken at the University of Amsterdam.

from classes.protein_class import Protein
from algorithms.algorithm_class import Algorithm
from algorithms.random import Random
from algorithms.random_greedy import Random_Greedy
import argparse

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
    output_file = args.output_file
    iterations = int(args.iterations)
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



    def run_trial(protein: Protein):

        # initialize an algorithm
        algorithm = Random(protein)

        # run the algorithm for each node to add
        for amino_acid in protein.sequence[2:]:
            algorithm.step(protein.amino_acids, amino_acid)

        return algorithm

    def run_experiment():

        best_score = 0
        best_protein = None
        scores = []

        for i in range(iterations):

            # initialize Protein
            P = Protein(sequence, output_file, threeD)

            success = False
            while not success:
                try:
                    algorithm = run_trial(P)
                    success = True
                    score = P.calculate_score(P.amino_acids)
                    scores.append(score)

                    if score < best_score:
                        best_score = score
                        best_protein = algorithm

                # reset the protein if we get a fatal error
                except IndexError:
                    P =Protein(sequence, output_file, threeD)
        best_protein.finish_up(output_file)

    run_experiment()
