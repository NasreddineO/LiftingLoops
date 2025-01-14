from .algorithm_class import Algorithm
from collections import OrderedDict
import random

class Random(Algorithm):
    def __init__(self, protein):
        super().__init__(protein)



    def step(self, type: str):
        legal_moves = self.check_legal_moves(self.protein.amino_acids)
        next_move = self.evaluate_moves(legal_moves, self.protein.amino_acids)
        self.protein.add_coordinate(self.protein.amino_acids, next_move, type)

    def evaluate_moves(self, legal_moves: set, dict: OrderedDict):

        if legal_moves is not None:
            # pick a random move by taking the first one from the set of legal moves
            x_next, y_next, z_next = random.choice(list(legal_moves))
            x, y, z = next(reversed(dict))

            # check the direction of the move by checking the difference between te current coordinate and next move
            if x_next - x == 1:
                fold = 1
            elif x_next - x == -1:
                fold = -1
            elif y_next - y == 1:
                fold = 2
            elif y_next - y == -1:
                fold = -2
            elif z_next - z == 1:
                fold = 3
            elif z_next - z == -1:
                fold = -3

            next_move = (x_next, y_next, z_next)
            self.protein.folds.append(fold)

            return next_move

        # pass None if no legal moves
        else:
            return None
