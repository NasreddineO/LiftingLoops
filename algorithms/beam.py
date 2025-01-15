from collections import OrderedDict
from queue import Queue
import copy
from .algorithm_class import Algorithm

class Beam(Algorithm):
    def __init__(self, protein, max_size: int, lookahead_depth: int = 2):
        super().__init__(protein)
        self.states = [protein]
        self.max_size = max_size
        # control how many steps ahead the algorithm evaluates
        self.lookahead_depth = lookahead_depth


    def step(self, type: str):

        # keep track of all possible next states
        self.temporary_states = {}

        # populate next possible states
        for state in self.states:
            legal_moves = self.check_legal_moves(state.amino_acids)

            for move in legal_moves:
                self.evaluate_move(state,move, type)

        # prune next possible states
        self.prune_states()



    def evaluate_move(self, state, move:tuple[int,int,int], type:str):
        new_state = copy.deepcopy(state)
        new_state.add_coordinate(new_state.amino_acids,move,type)
        # self.temporary_states[new_state] = new_state.calculate_score()

        # evaluate a move by simulating future steps and calculating the predicted score
        predicted_score = self.simulate(new_state, self.lookahead_depth)
        self.temporary_states[new_state] = predicted_score

    def simulate(self, state, depth: int):

        if depth == 0:
            return state.calculate_score()

        # generate legal moves for the current state
        legal_moves = self.check_legal_moves(state.amino_acids)
        # no moves available, return current score
        if not legal_moves:
            return state.calculate_score()

        # simulate each move and repeat calculating scores
        scores = []
        for move in legal_moves:
            temp_state = copy.deepcopy(state)
            temp_state.add_coordinate(temp_state.amino_acids, move, type)
            scores.append(self.simulate(temp_state, depth - 1))

        # return the maximum score from the simulated future moves
        return max(scores)


    def prune_states(self):
        # add all states if below max_size
        if len(self.temporary_states) <= self.max_size:
            self.states = self.temporary_states

        # otherwise add the max_size amount of best-scoring folds to the list of new states to iterate from.
        else:
            # overwrite self.states
            self.states = {}
            for i in range(self.max_size):
                minimum = min(self.temporary_states, key=self.temporary_states.get)
                self.states[minimum] = self.temporary_states[minimum]
                self.temporary_states.pop(minimum)


    def finish_up(self, output_file):
        self.protein = min(self.states, key=self.states.get)
        super().finish_up(output_file)
