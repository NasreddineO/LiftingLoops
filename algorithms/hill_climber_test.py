import random
from classes.protein_class import Protein
from algorithms.random import Random
from .algorithm_class import Algorithm
from collections import OrderedDict
import copy

class Climber(Algorithm):
    def __init__(self, sequence: str, iterations: int, output_file: str, threeD: bool):
        super().__init__(sequence, 1, output_file, threeD)
        self.protein = Protein(sequence, output_file, threeD)
        # self.protein = protein
        self.best_protein = copy.deepcopy(self.protein)
        self.best_score = self.protein.calculate_score()
        self.scores = [self.best_score]
        self.improvement_attempts = iterations

    def run(self):
        i = 0
        while i < self.improvement_attempts:
            previous_best = self.best_score
            improved = self.step()
            if improved:
                i = 0
            else:
                i += 1

    def step(self):
        improved = False
        # Process amino acids in random order
        amino_acids = list(range(len(self.protein.amino_acids)))
        random.shuffle(amino_acids)

        for amino_acid in amino_acids:
            original_amino_list = list(self.protein.amino_acids.keys())
            legal_moves, directions = self.check_legal_moves(amino_acid, original_amino_list[amino_acid], original_amino_list)

            if not legal_moves:
                continue

            for move, direction in zip(legal_moves, directions):
                new_amino_list = original_amino_list.copy()
                success = self.apply_pull_move(new_amino_list, amino_acid, move, direction)

                if success and self.is_legal(new_amino_list):
                    # Create temporary protein to evaluate score
                    temp_protein = Protein(self.sequence, threeD=self.threeD)
                    temp_protein.amino_acids = OrderedDict()
                    for idx, coord in enumerate(new_amino_list):
                        temp_protein.amino_acids[coord] = self.sequence[idx]

                    current_score = temp_protein.calculate_score()

                    if current_score < self.best_score:
                        self.protein = temp_protein
                        self.best_protein = copy.deepcopy(temp_protein)
                        self.best_score = current_score
                        self.scores.append(current_score)
                        improved = True
                        break  # Accept first improving move
            if improved:
                break
        return improved

    def check_legal_moves(self, amino_idx: int, coord: tuple[int,int,int], amino_list: list[tuple[int,int,int]]):
        legal_moves = []
        directions = []
        amino_set = set(amino_list)
        x, y, z = coord

        # Orthogonal and diagonal neighbors based on 3D
        neighbors = self.get_neighbors(coord, self.threeD)

        for new_coord in neighbors:
            # Check if new_coord is diagonal to current and adjacent to previous/next
            if new_coord in amino_set:
                continue

            # Determine direction (next or previous)
            valid_prev = False
            valid_next = False

            # Check adjacency to previous amino (if not first)
            if amino_idx > 0:
                prev_coord = amino_list[amino_idx - 1]
                valid_prev = Protein.is_adjacent(new_coord, prev_coord)

            # Check adjacency to next amino (if not last)
            if amino_idx < len(amino_list) - 1:
                next_coord = amino_list[amino_idx + 1]
                valid_next = Protein.is_adjacent(new_coord, next_coord)

            if valid_prev or valid_next:
                # Determine direction and required pull
                direction = 'next' if valid_next else 'prev'
                # Find the adjacent coordinate to pull
                if valid_next:
                    adjacent = next_coord
                else:
                    adjacent = prev_coord

                # Check if the pull is possible
                legal_moves.append((new_coord, adjacent))
                directions.append(direction)

        return legal_moves, directions

    def apply_pull_move(self, amino_list, amino_idx, move, direction):
        new_coord, adjacent_coord = move
        original_coord = amino_list[amino_idx]
        amino_list[amino_idx] = new_coord

        # Determine which neighbor to adjust
        if direction == 'next':
            target_idx = amino_idx + 1
        else:
            target_idx = amino_idx - 1

        # Check if the target is now non-adjacent and needs adjustment
        if not Protein.is_adjacent(new_coord, amino_list[target_idx]):
            amino_list[target_idx] = adjacent_coord

            # Propagate changes along the chain
            step = 1 if direction == 'next' else -1
            current_idx = target_idx
            while 0 <= current_idx + step < len(amino_list):
                next_idx = current_idx + step
                if Protein.is_adjacent(amino_list[current_idx], amino_list[next_idx]):
                    break
                # Find a valid position for next_idx
                possible = self.get_adjacent_positions(amino_list[current_idx], amino_list[next_idx - step])
                for pos in possible:
                    if pos not in amino_list:
                        amino_list[next_idx] = pos
                        break
                else:
                    return False  # Couldn't find valid position
                current_idx = next_idx
        return True

    @staticmethod
    def get_neighbors(coord, threeD):
        x, y, z = coord
        neighbors = [
            (x+1, y, z), (x-1, y, z),
            (x, y+1, z), (x, y-1, z)
        ]
        if threeD:
            neighbors += [(x, y, z+1), (x, y, z-1)]
        return neighbors

    @staticmethod
    def get_adjacent_positions(current, exclude):
        x, y, z = current
        positions = [
            (x+1, y, z), (x-1, y, z),
            (x, y+1, z), (x, y-1, z),
            (x, y, z+1), (x, y, z-1)
        ]
        return [p for p in positions if p != exclude]

    def is_legal(self, amino_list):
        # Check for duplicates
        if len(set(amino_list)) != len(amino_list):
            return False
        # Check adjacency
        for i in range(len(amino_list)-1):
            if not Protein.is_adjacent(amino_list[i], amino_list[i+1]):
                return False
        return True
