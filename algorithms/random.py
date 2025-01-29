from .algorithm_class import Algorithm
from classes.protein_class import Protein
from collections import OrderedDict
import random

class Random(Algorithm):
    """
    A random algorithm for protein folding prediction.

    This algorithm attempts to fold the protein by randomly selecting valid moves
    for each amino acid until a valid structure is formed. If placement fails,
    the process restarts with a new protein instance.
    """
    def __init__(self, sequence: str,  iterations: int, output_file: str, threeD: bool):
        """
        Initializes the Random folding algorithm with the given parameters.

        Parameters:
            sequence (str): The amino acid sequence of the protein.
            iterations (int): Number of iterations to run the algorithm.
            output_file (str): Path to save the results.
            threeD (bool): Whether the protein folding is in 3D (True) or 2D (False).
        """
        super().__init__(sequence, iterations, output_file, threeD)

    def run(self):
        """
        Executes the random folding algorithm.

        This method attempts to fold the protein sequence by iterating through its amino acids,
        randomly selecting valid moves, and adding them to the structure. If the structure
        is valid (all amino acids placed and not crossing), it calculates the score, appends it to the scores
        list, and finishes the process.

        Returns:
            int: The calculated score of the protein after successful folding.
        """
        self.protein = Protein(self.sequence, self.output_file, self.threeD)
        success = False

        while not success:
            # Try to place each subsequent amino acid (starting from index 2)
            for amino_acid in range(2, len(self.protein.sequence)):
                self.step(self.protein.sequence[amino_acid])

            if len(self.protein.amino_acids) == len(self.protein.sequence):
                success = True
                score = self.protein.calculate_score()
                self.scores.append(score)
                self.finish_up()
            else:
                # Reset protein for new attempt
                self.protein = Protein(self.sequence, self.output_file, self.threeD)
        return score

    def step(self, type: str):
        """
        Performs a single folding step by evaluating and applying a move.

        Parameters:
            type (str): The type of the current amino acid in the sequence.

        Returns:
            None
        """
        legal_moves = self.check_legal_moves(self.protein.amino_acids)
        next_move = self.evaluate_moves(legal_moves, self.protein.amino_acids)
        self.protein.add_coordinate(self.protein.amino_acids, next_move, type)

    def evaluate_moves(self, legal_moves: set, dict: OrderedDict):
        """
        Evaluates legal moves and selects one randomly.

        Parameters:
            legal_moves (set): A set of possible coordinates for the next move.
            dict (OrderedDict): The current structure of the protein (coordinates and amino acids).

        Returns:
            tuple or None: The selected move as a coordinate tuple (x, y, z),
                       or None if no legal moves are available.
        """
        # Check for non-empty set
        if legal_moves:
            return random.choice(list(legal_moves))

        return None
