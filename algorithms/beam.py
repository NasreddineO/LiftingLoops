from collections import OrderedDict
from queue import Queue
import copy
from .algorithm_class import Algorithm

class Beam(Algorithm):
    def __init__(self, protein, max_size: int, lookahead_depth: int = 5):
        super().__init__(protein)
        self.states = [protein]
        self.max_size = max_size

        # control how many steps ahead the algorithm evaluates
        self.lookahead_depth = lookahead_depth

    def run(self):
        for amino_acid in range(len(self.protein.sequence)-2):
            self.step(self.protein.sequence[amino_acid+2], amino_acid+1)


    def step(self, type: str, current_depth: int):

        # keep track of all possible next states
        self.temporary_states = []

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
        # self.temporary_states[new_state] = new_state.calculate_score()

        # evaluate a move by simulating future steps and calculating the predicted score
        predicted_score = self.simulate(new_state, self.lookahead_depth, current_depth)
        self.temporary_states.append((new_state,predicted_score))

    def simulate(self, state, depth: int, current_depth: int):

        if depth == 0:
            return state.calculate_score()

        # because protein is initialized with 2, the actual current depth is always 2 more than current_depth
        if current_depth+2 == len(self.protein.sequence):
            return state.calculate_score()

        # score cannot improve if there are only 'H' amino acids remaining
        proteins_to_go = set(self.protein.sequence[current_depth+2:])
        if proteins_to_go == set('P'):
            return state.calculate_score()

        # generate legal moves for the current state
        legal_moves = self.check_legal_moves(state.amino_acids)

        # if the move will inevitably result in a failure state, return 0 such that the state is not chosen.
        if legal_moves is None:
            return 0


        # simulate each move and repeat calculating scores
        scores = []
        for move in legal_moves:
            temp_state = copy.deepcopy(state)
            temp_state.add_coordinate(temp_state.amino_acids, move, self.protein.sequence[current_depth+2])
            scores.append(self.simulate(temp_state, depth - 1, current_depth+1))

        # return the minimum score from the simulated future moves
        return min(scores)


    def prune_states(self):
        # add all states if below max_size
        if len(self.temporary_states) <= self.max_size:
            self.states = [self.temporary_states[x][0] for x in range(len(self.temporary_states))]

        # otherwise sort and slice out the amount you need.
        else:
            self.temporary_states.sort(key=lambda x: x[1])
            self.states = [self.temporary_states[x][0] for x in range(self.max_size)]



    def finish_up(self):
        self.protein = min(self.states, key=lambda x:x.calculate_score())
        super().finish_up()
