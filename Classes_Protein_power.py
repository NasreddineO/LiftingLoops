from collections import OrderedDict

class Protein:
    def __init__(self, sequence: str, output_file: str, threeD: bool):

        self.sequence = sequence
        self.output_file = output_file
        self.threeD = threeD
        self.amino_acids = OrderedDict()
        self.folds = []


        # add initial amino acids and fold, as rotational symmetry dictates that the first 2 amino acids are functionally identical no matter how they are placed
        self.amino_acids[(0,0,0)] = self.sequence[0]
        self.amino_acids[(1,0,0)] = self.sequence[1]
        self.amino_acids[(1,1,0)] = self.sequence[2]
        self.amino_acids[(0,1,0)] = self.sequence[3]
        self.amino_acids[(-1,1,0)] = self.sequence[4]
        self.amino_acids[(-1,2,0)] = self.sequence[5]
        self.amino_acids[(-1,3,0)] = self.sequence[6]
        self.amino_acids[(0,3,0)] = self.sequence[7]
        self.amino_acids[(0,2,0)] = self.sequence[8]


        self.folds.append(1)


    def calculate_score(self, amino_acids: OrderedDict):
        score = 0

        amino_list = list(amino_acids.items())

        for acid1 in range(len(amino_acids)):
            for acid2 in range(acid1+3, len(amino_acids)):

                # check whether the amino acids are adjacent
                if self.is_adjacent(amino_list[acid1][0], amino_list[acid2][0]):

                    # assign points to strong bonds
                    if set(amino_list[acid1][1] + amino_list[acid2][1]) == {'H'}:
                        score -= 1
                    elif set(amino_list[acid1][1] + amino_list[acid2][1]) == {'H', 'C'}:
                        score -= 1
                    elif set(amino_list[acid1][1] + amino_list[acid2][1]) == {'C'}:
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
