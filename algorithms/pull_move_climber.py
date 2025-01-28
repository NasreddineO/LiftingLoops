import random
from classes.protein_class import Protein
from algorithms.random import Random
from .algorithm_class import Algorithm
from collections import OrderedDict

class Climber(Algorithm):
    def __init__(self, sequence: str,  iterations: int, output_file: str, threeD: bool, protein: Protein):

        super().__init__(sequence, 1, output_file, threeD)
        self.protein = protein
        self.best_protein = protein
        self.best_score = self.protein.calculate_score()
        self.scores.append(self.best_score)
        self.improvement_attempts = iterations

    def run(self):
        i = 0
        while i < self.improvement_attempts:
            self.previous_best = self.best_score
            self.step()
            if self.previous_best != self.best_score:
                i = 0
            else:
                i += 1

    def step(self):
            for amino_acid in range(len(self.protein.amino_acids)):

                print('')
                print('Help')
                print(self.protein.amino_acids)
                print('')
                amino_list = list(self.protein.amino_acids.keys())
                x,y,z = amino_list[amino_acid]
                pull_move, direction = self.check_legal_moves(amino_acid, (x,y,z), amino_list)

                print('Pull move:')
                print(pull_move)

                self.pull(pull_move, amino_acid, amino_list, direction)

    def check_legal_moves(self, amino_acid: int, coordinate: tuple[int,int,int], amino_list: list[tuple[int,int,int]]):

        direction = None
        legal_moves = set()
        amino_set = set(amino_list)
        x,y,z = coordinate

        diagonal_coordinates = set([
            (x+1, y+1, z), (x+1, y-1, z),
            (x-1, y+1, z), (x-1, y-1, z)
        ])

        orthogonal_coordinates = set([
            (x+1, y, z), (x-1, y, z),
            (x, y+1, z), (x, y-1, z)
        ])

        if self.threeD:
            diagonal_coordinates.update([
                (x+1, y, z+1), (x+1, y, z-1),
                (x, y+1, z+1), (x, y+1, z-1),
                (x-1, y, z+1), (x-1, y, z-1),
                (x, y-1, z+1), (x, y-1, z-1)
            ])

            orthogonal_coordinates.update([
                (x, y, z+1), (x, y, z-1),
            ])


        free_diagonal_coordinates = diagonal_coordinates - amino_set

        print('')
        print('Free diagonals:')
        print(free_diagonal_coordinates)

        for diagonal_coordinate in free_diagonal_coordinates:
            x_current,y_current,z_current = diagonal_coordinate

            current_orthogonal_coordinates = set([
                (x_current+1, y_current, z_current),
                (x_current-1, y_current, z_current),
                (x_current, y_current+1, z_current),
                (x_current, y_current-1, z_current)
            ])

            if self.threeD:
                current_orthogonal_coordinates.update([
                (x_current, y_current, z_current+1),
                (x_current, y_current, z_current-1)
                ])

            for element in current_orthogonal_coordinates:

                # if I and C are adjacent:
                if self.protein.is_adjacent(element, coordinate):

                    # if it is not the last amino_acid:
                    if amino_acid+1 < len(amino_list):

                        #if I is adjacent to I+1
                        if self.protein.is_adjacent(diagonal_coordinate, amino_list[amino_acid+1]):
                            direction = True
                            if amino_acid != 0:
                                if element not in amino_set or element == amino_list[amino_acid-1] or element == amino_list[amino_acid+1]:
                                    legal_moves.add((diagonal_coordinate, element))
                            elif element not in amino_set or element == amino_list[amino_acid+1]:
                                legal_moves.add((diagonal_coordinate, element))
                    if amino_acid != 0:
                        if self.protein.is_adjacent(diagonal_coordinate, amino_list[amino_acid-1]):
                            direction = False
                            if amino_acid+1 < len(amino_list):
                                if element not in amino_set or element == amino_list[amino_acid+1] or element == amino_list[amino_acid-1]:
                                    legal_moves.add((diagonal_coordinate, element))
                            elif element not in amino_set or element == amino_list[amino_acid-1]:
                                legal_moves.add((diagonal_coordinate, element))

        print('legal moves: L/C')
        print(legal_moves) if legal_moves != set() else None

        return random.choice(list(legal_moves)), direction if legal_moves != set() else None



    def pull(self, move: tuple[tuple[int,int,int],tuple[int,int,int]], amino_acid: int, amino_list: list[tuple[int,int,int]], direction: bool):

        if move is not None:
            if direction:
                amino_list[amino_acid] = move[0]

                if not self.is_legal(amino_list):
                    amino_list[amino_acid+1] = move[1]

                i = 0
                while not self.is_legal(amino_list):
                    previous_position = list(self.protein.amino_acids)[amino_acid+i]
                    print('PP:')
                    print(previous_position)
                    print(amino_list)
                    print('')

                    if not self.protein.is_adjacent(amino_list[amino_acid+1+i], amino_list[amino_acid+2+i]):
                        amino_list[amino_acid+2+i] = previous_position
                    i+=1

            else:
                amino_list[amino_acid] = move[0]

                if not self.protein.is_legal(amino_list):
                    amino_list[amino_acid-1] = move[1]

                i = 0
                while not self.is_legal(amino_list):
                    previous_position = list(self.protein.amino_acids)[amino_acid+i]

                    if not self.protein.is_adjacent(amino_list[amino_acid-1+i], amino_list[amino_acid-2+i]):
                        amino_list[amino_acid-2+i] = previous_position
                    i-=1


        self.protein.amino_acids = OrderedDict()
        for amino in range(len(amino_list)):
            self.protein.amino_acids[amino_list[amino]] = self.protein.sequence[amino]


    def is_legal(self, amino_list: list[int, int, int]):

        for i in range(len(amino_list)-1):

            if not self.protein.is_adjacent(amino_list[i], amino_list[i+1]):
                print('debug')
                print(amino_list)
                print(amino_list[i], amino_list[i+1])
                print('')
                return False

        print('true')
        return True
