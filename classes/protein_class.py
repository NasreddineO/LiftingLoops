# Names: Hendrik DuPont, Jeppe Mul & Nasreddine Ouchene
# This script contains a Protein class with methods that are intended to come together in an algorithm to fold the protein.
# This script is in partial fulfillment of the requirements for Algoritmen en Heuristieken at the University of Amsterdam.
from collections import OrderedDict
class Protein():
    def __init__(self, sequence: str, output_file: str, threeD: bool):

        self.sequence = sequence
        self.output_file = output_file
        self.threeD = threeD

        # dictionary {coordinate: type}
        self.amino_acids = OrderedDict()
        self.folds = []
        self.adjacent_amino_acids = {}

        # add initial amino acids and fold, as rotational symmetry dictates that the first 2 amino acids are functionally identical no matter how they are placed
        self.amino_acids[(0,0,0)] = self.sequence[0]
        self.amino_acids[(1,0,0)] = self.sequence[1]
        self.folds.append(1)


    def calculate_score(self):
        score = 0

        amino_list = list(self.amino_acids.items())

        for acid1 in range(len(self.amino_acids)):
            for acid2 in range(acid1+3, len(self.amino_acids)):

                # check whether the amino acids are adjacent
                if self.is_adjacent(amino_list[acid1][0], amino_list[acid2][0]):

                    # assign points to strong bonds
                    if set(amino_list[acid1][1] + amino_list[acid2][1]) == {'H'}:
                        self.adjacent_amino_acids[(amino_list[acid1][0], amino_list[acid2][0])] = 'H-H'
                        score -= 1
                    elif set(amino_list[acid1][1] + amino_list[acid2][1]) == {'H', 'C'}:
                        self.adjacent_amino_acids[(amino_list[acid1][0], amino_list[acid2][0])] = 'H-C'
                        score -= 1
                    elif set(amino_list[acid1][1] + amino_list[acid2][1]) == {'C'}:
                        self.adjacent_amino_acids[(amino_list[acid1][0], amino_list[acid2][0])] = 'C-C'
                        score -= 5

        return score

    def is_adjacent(self, coordinate1: tuple[int, int, int], coordinate2: tuple[int, int, int]):

        # check for horizontal adjacency in 2d
        if coordinate1[0] == coordinate2[0] and coordinate1[2] == coordinate2[2]:
            if abs(coordinate1[1] - coordinate2[1]) == 1:
                return True

        # check for vertical adjacency in 2d
        elif coordinate1[1] == coordinate2[1] and coordinate1[2] == coordinate2[2]:
            if abs(coordinate1[0] - coordinate2[0]) == 1:
                return True

        # check for 3d adjacency
        elif coordinate1[0] == coordinate2[0] and coordinate1[1] == coordinate2[1]:
            if abs(coordinate1[2] - coordinate2[2]) == 1:
                return True
        return False

    def add_coordinate(self, dict: OrderedDict, coordinate: tuple[int, int, int], type: str):
        if coordinate is not None:
            dict[coordinate] = type
