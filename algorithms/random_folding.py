import random
from .algorithm_class import Algorithm
from classes.protein_class import Protein

class RandomFolding(Algorithm):
    def __init__(self, sequence: str, iterations: int, output_file: str, threeD: bool):
        super().__init__(sequence, iterations, output_file, threeD)
        self.protein = Protein(self.sequence, self.output_file, self.threeD)
        self.failure_count = 0

    def run(self):
        """
        Because we don't know how long it will take to find a valid folding
        configuration, we use a while True loop to allow the computer to
        make unlimited attempts. The while loop stops when we generate a Valid
        solution with the return statement. We keep track of the failure count
        and print it when we find a valid solution.
        """
        while True:
            self.failure_count += 1

            # generate a random list of folds
            folds = self.generate_random_folds()

            # convert the folds to a protein structure
            self.protein = self.calculate_protein(folds)

            # valid solution; every amino acid should have been placed in the protein
            if len(self.protein.amino_acids) == len(self.sequence):
                print(f"Valid solution found after {self.failure_count} attempts.")
                return self.protein.calculate_score()

    def generate_random_folds(self):
        """
        Base folds: Typically, the first amino acid is placed at a fixed coordinate
        ((0,0,0)), and the second one is placed neigboring to it ((1,0,0) in 2D
        or (1,0,0,0) in 3D). This is based on mirroring and symmetry,
        which result in equivalent solutions
        """
        # generate a random list of folds based on whether it's 2D or 3D.
        if self.threeD:
            possible_folds = [1, -1, 2, -2, 3, -3]
        else:
            possible_folds = [1, -1, 2, -2]

        # create an empty list to store the randomly chosen folds
        folds = []

        # loop through the sequence length minus the first two base folds
        for _ in range(len(self.sequence) - 2):
            # randomly select a fold and add the fold to the list
            fold = random.choice(possible_folds)
            folds.append(fold)

        return folds
