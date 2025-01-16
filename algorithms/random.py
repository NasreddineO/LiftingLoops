from .algorithm_class import Algorithm
from collections import OrderedDict
import random

class Random(Algorithm):
    def __init__(self, protein):
        super().__init__(protein)

    def run(self):
        for amino_acid in range(len(self.protein.sequence)-2):
            self.step(self.protein.sequence[amino_acid+2])

    def step(self, type: str):
        legal_moves = self.check_legal_moves(self.protein.amino_acids)
        next_move = self.evaluate_moves(legal_moves, self.protein.amino_acids)
        self.protein.add_coordinate(self.protein.amino_acids, next_move, type)

    def evaluate_moves(self, legal_moves: set, dict: OrderedDict):

        if legal_moves is not None:
            # pick a random move by taking the first one from the set of legal moves
            x_next, y_next, z_next = random.choice(list(legal_moves))
            x, y, z = next(reversed(dict))

            next_move = (x_next, y_next, z_next)

            return next_move

        # pass None if no legal moves
        else:
            return None
