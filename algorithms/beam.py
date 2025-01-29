from collections import OrderedDict
from queue import Queue
import copy
from .algorithm_class import Algorithm
from classes.protein_class import Protein

class Beam(Algorithm):
    """
    Beam Search algorithm for protein folding prediction.

    Maintains a beam of top candidate states and explores possible folds while
    considering potential future moves through lookahead simulation.
    """
    def __init__(self, sequence: str, max_size: int, output_file: str, threeD: bool, lookahead_depth: int = 0):
        """
        Initialize Beam Search algorithm.

        Parameters:
            sequence: Amino acid sequence of the protein
            max_size: Maximum number of states to maintain in the beam (beam width)
            output_file: Path to save output files
            threeD: True for 3D folding, False for 2D
            lookahead_depth: Number of future steps to consider during simulation
        """
        super().__init__(sequence, 1, output_file, threeD)
        self.protein = Protein(sequence, output_file, threeD)
        self.states = [self.protein]
        self.max_size = max_size
        self.lookahead_depth = lookahead_depth

    def run(self):
        """
        Execute the beam search folding process.

        Returns:
            float: Final score of the best found protein configuration
        """
        total_steps = len(self.protein.sequence) - 2
        self.progress_bar(0, total_steps)
        for amino_acid in range(total_steps):
            self.progress_bar(amino_acid, total_steps)
            current_amino_acid = self.protein.sequence[amino_acid + 2]
            self.step(current_amino_acid, amino_acid + 1)

        self.finish_up()
        return self.protein.calculate_score()

    def step(self, type: str, current_depth: int):
        """
        Process a single folding step for the current amino acid.

        Parameters:
            amino_type: Type of amino acid being placed
            current_depth: Current position in the sequence (0-based index)
        """
        # keep track of all possible next states
        self.temporary_states = []

        # Generate all possible next states from current beam
        for state in self.states:
            legal_moves = self.check_legal_moves(state.amino_acids)

            if legal_moves:
                for move in legal_moves:
                    self.evaluate_move(state, move, type, current_depth)

        # Prune states to maintain beam width
        self.prune_states()

    def evaluate_move(self, state, move:tuple[int,int,int], type:str, current_depth:int):
        """
        Evaluate a potential move and add to candidate states.

        Parameters:
            state: Current protein state being evaluated
            position: (x, y, z) coordinates for potential placement
            amino_type: Type of amino acid to place
            current_depth: Current position in sequence processing
        """
        new_state = copy.deepcopy(state)
        new_state.add_coordinate(new_state.amino_acids, move, type)

        # Calculate predicted score with lookahead simulation
        predicted_score = self.simulate(new_state, self.lookahead_depth, current_depth)
        self.temporary_states.append((new_state, predicted_score))

    def simulate(self, state, depth: int, current_depth: int):
        """
        Recursively simulate future moves to predict potential outcomes.

        Parameters:
            state: Current protein state to simulate from
            remaining_depth: Remaining lookahead steps
            current_depth: Current position in sequence processing

        Returns:
            float: Predicted score for this state path
        """
        # Base case: return current score when lookahead exhausted
        if depth == 0:
            return state.calculate_score()

        # Early termination if at end of sequence (current_depth + 2 because we start at the 3rd amino_acid)
        if current_depth + 2 == len(self.protein.sequence):
            return state.calculate_score()

        # Check remaining amino acid types
        remaining_acids = set(self.protein.sequence[current_depth + 2:])

        # No additional points to score in this case
        if remaining_acids == set('P'):
            return state.calculate_score()

        # Generate legal moves for the current state
        legal_moves = self.check_legal_moves(state.amino_acids)

        # If the move will inevitably result in a failure state, return 0 such that the state is not chosen.
        if legal_moves:
            return 0

        # Simulate each move and repeat calculating scores
        scores = []
        next_amino_type = self.protein.sequence[current_depth + 2]
        for move in legal_moves:
            simulated_state = copy.deepcopy(state)
            simulated_state.add_coordinate(simulated_state.amino_acids, move, next_amino_type)
            scores.append(self.simulate(simulated_state, depth - 1, current_depth + 1))

        return min(scores)

    def prune_states(self):
        """
        Select top candidate states to maintain beam width.
        """
        if not self.temporary_states:
            return

        # Sort states by ascending score (lower is better)
        self.temporary_states.sort(key=lambda x: x[1])

        # Select top N states within beam width
        keep_count = min(self.max_size, len(self.temporary_states))
        self.states = [self.temporary_states[i][0] for i in range(keep_count)]

    def finish_up(self):
        """
        Finalize best state and save results.
        """
        self.protein = min(self.states, key=lambda x: x.calculate_score())
        super().finish_up()

    def progress_bar(self, progress, total):
        """
        Visual progress indicator for the folding process.

        Args:
            progress: Current step number
            total: Total number of steps
        """
        percent = 100 * (progress / float(total))
        bar = chr(9608) * int(percent) + '-'* (100 - int(percent))
        print(f"\r|{bar}| {percent: .2f}%", end="")
