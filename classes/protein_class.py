# Names: Hendrik DuPont, Jeppe Mul & Nasreddine Ouchene
# This script contains a Protein class with methods that are intended to come together in an algorithm to fold the protein.
# This script is in partial fulfillment of the requirements for Algoritmen en Heuristieken at the University of Amsterdam.
from collections import OrderedDict
class Protein():
    def __init__(self, sequence: str, output_file: str, threeD: bool):
        """
        Initializes the protein object with a sequence, output file, and 3D folding option.

        Parameters:
            sequence (str): The sequence of amino acids.
            output_file (str): The path/filename for the output file.
            threeD (bool): Indicates if the protein should be folded and visualized in 3D (True) or 2D (False).

        Initializes amino acids, folds, and adjacent amino acid relationships.
        """
        self.sequence = sequence
        self.output_file = output_file
        self.threeD = threeD

        # Dictionary {coordinate: type}, representing the positions and types of amino acids
        self.amino_acids = OrderedDict()
        self.folds = []
        self.adjacent_amino_acids = {}

        # add initial amino acids and fold, as rotational symmetry dictates that the first 2 amino acids are functionally identical no matter how they are placed
        self.amino_acids[(0,0,0)] = self.sequence[0]
        self.amino_acids[(1,0,0)] = self.sequence[1]
        self.folds.append(1)

    def calculate_score(self):
        """
        Calculates the stability score for the current protein fold configuration.

        The score is based on the types of bonds formed between adjacent amino acids:
        - H-H bonds: score -1
        - H-C bonds: score -1
        - C-C bonds: score -5

        The function iterates through the list of amino acids, checking if each pair of amino acids is adjacent,
        and assigns points based on their interaction.

        Returns:
            int: The calculated stability score of the protein.
        """
        score = 0
        amino_list = list(self.amino_acids.items())

        # Check pairs of amino acids for adjacency and assign score based on interaction
        for acid1 in range(len(self.amino_acids)):
            for acid2 in range(acid1+3, len(self.amino_acids)):

                # check whether the amino acids are adjacent
                if self.is_adjacent(amino_list[acid1][0], amino_list[acid2][0]):

                    # Assign points based on bond type
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
        """
        Determines if two amino acids are adjacent in the protein fold based on their coordinates.

        The function checks for adjacency in 2D (horizontal and vertical) and 3D space.

        Parameters:
            coordinate1 (tuple): The (x, y, z) coordinates of the first amino acid.
            coordinate2 (tuple): The (x, y, z) coordinates of the second amino acid.

        Returns:
            bool: True if the amino acids are adjacent, False otherwise.
        """
        return sum(abs(c1 - c2) for c1, c2 in zip(coordinate1, coordinate2)) == 1

    def add_coordinate(self, coordinate: tuple[int, int, int], type: str):
        """
        Adds a new amino acid coordinate and type to the provided dictionary.

        Parameters:
            coordinate (tuple): The (x, y, z) coordinates of the amino acid.
            type (str): The type of the amino acid ('H', 'P', 'C').

        This method ensures that the coordinate is not None before adding it to the dictionary.
        """
        if coordinate is not None:
            self.amino_acids[coordinate] = type
