from collections import OrderedDict
from queue import Queue
import copy
from .algorithm_class import Algorithm

class Beam(Algorithm):
    def __init__(self, protein, max_size: int):
        super().__init__(protein)
        self.states = [protein]
        self.max_size = max_size



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
        self.temporary_states[new_state] = new_state.calculate_score()



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
