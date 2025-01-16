from collections import OrderedDict
from queue import Queue
import copy
from .algorithm_class import Algorithm

class Beam(Algorithm):
    def __init__(self, protein, max_size: int, lookahead_depth: int = 1):
        super().__init__(protein)
        self.states = [protein]
        self.max_size = max_size

        # control how many steps ahead the algorithm evaluates
        self.lookahead_depth = lookahead_depth


    def step(self, type: str, current_depth: int):

        # keep track of all possible next states
        self.temporary_states = {}

        # populate next possible states
        for state in self.states:
            legal_moves = self.check_legal_moves(state.amino_acids)

            if legal_moves is not None:
                for move in legal_moves:
                    self.evaluate_move(state,move,type,current_depth)

        # prune next possible states
        self.prune_states()



    def evaluate_move(self, state, move:tuple[int,int,int], type:str, current_depth:int):
        new_state = copy.deepcopy(state)
        new_state.add_coordinate(new_state.amino_acids,move,type)

        # evaluate a move by simulating future steps and calculating the predicted score
        predicted_score = self.simulate(new_state, self.lookahead_depth, type, current_depth)
        self.temporary_states[new_state] = predicted_score

    def simulate(self, state, depth: int, type: str, current_depth:int):

        if depth == 0:
            return state.calculate_score()

        if current_depth+2 == len(self.protein.sequence):
            return state.calculate_score()
            print('debug')

        # generate legal moves for the current state
        legal_moves = self.check_legal_moves(state.amino_acids)

        # if the move will inevitably result in a failure state, return 0 such that the state is not chosen.
        if legal_moves is None:
            return 0


        # simulate each move and repeat calculating scores
        scores = []
        for move in legal_moves:
            temp_state = copy.deepcopy(state)
            temp_state.add_coordinate(temp_state.amino_acids, move, type)
            scores.append(self.simulate(temp_state, depth - 1, self.protein.sequence[current_depth+1], current_depth+1))

        # return the minimum score from the simulated future moves
        return min(scores)


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


    def finish_up(self):
        self.protein = min(self.states, key=self.states.get)
        super().finish_up()
