from .algorithm_class import Algorithm
from collections import OrderedDict

class Random_Greedy(Algorithm):

    def __init__(self, protein):
        super().__init__(protein)

    def step(self, dict: OrderedDict, type: str):
        legal_moves = self.check_legal_moves(dict)
        next_move = self.evaluate_moves(legal_moves, dict, type)
        self.protein.add_coordinate(dict, next_move, type)

    def evaluate_moves(self, legal_moves: set, dict: OrderedDict, type:str):
        # check for scoring moves
        best_score = self.protein.calculate_score(self.protein.amino_acids)
        print(legal_moves)
        x_next, y_next, z_next = next(iter(legal_moves))

        for move in legal_moves:
            self.protein.add_coordinate(dict, move, type)
            current_score = self.protein.calculate_score(self.protein.amino_acids)
            self.protein.amino_acids.popitem()
            if current_score <= best_score:
                best_score = current_score
                x_next, y_next, z_next = move



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
