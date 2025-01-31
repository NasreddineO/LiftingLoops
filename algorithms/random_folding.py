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
                self.finish_up()
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
            possible_folds = set([1, -1, 2, -2, 3, -3])
        else:
            possible_folds = set([1, -1, 2, -2])

        # create an empty list to store the randomly chosen folds
        folds = [1]
        previous_fold = 1

        # loop through the sequence length minus the first two base folds
        for _ in range(len(self.sequence) - 2):
            # randomly select a fold and add the fold to the list
            fold = random.choice(tuple(possible_folds.difference([previous_fold * -1])))
            previous_fold = fold
            folds.append(fold)

        return folds

    def calculate_protein(self, folds:list[int]):
        """
        Calculates the 3D coordinates of the protein based on its fold directions.

        This method uses the provided list of fold directions to iteratively calculate the
        3D coordinates for each amino acid in the protein sequence, starting from a fixed
        initial coordinate. It updates the new protein object with these coordinates and
        returns the newly constructed protein.

        Parameters:
            folds (list[int]): A list of fold directions representing changes in coordinates.
                            Each integer corresponds to a specific fold direction, with
                            positive and negative values indicating direction.

        Returns:
            Protein: A new Protein object with the calculated 3D coordinates.
        """
        x,y,z = 1,0,0

        new_protein = Protein(self.protein.sequence, self.protein.output_file, self.protein.threeD)

        # Map fold directions to coordinate changes
        direction_map = {
            1: (1, 0, 0), -1: (-1, 0, 0),
            2: (0, 1, 0), -2: (0, -1, 0),
            3: (0, 0, 1), -3: (0, 0, -1)
        }

        # Skip the first 2 folds and exclude the last fold (0 is a placeholder)
        for i, fold in enumerate(folds[1:]):

            # Update coordinates based on the fold direction
            dx, dy, dz = direction_map.get(fold, (0, 0, 0))
            x, y, z = x + dx, y + dy, z + dz

            # Add the new coordinate and amino acid to the protein
            new_protein.add_coordinate((x, y, z), self.protein.sequence[i+2])

        return new_protein
