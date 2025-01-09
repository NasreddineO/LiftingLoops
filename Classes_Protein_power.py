class Protein:
    def __init__(self, sequence, output_file, threeD):

        self.sequence = sequence
        self.output_file = output_file
        self.threeD = threeD
        self.amino_acids = {}
        self.folds = []


        # add initial amino acids and fold, as rotational symmetry dictates that the first 2 amino acids are functionally identical no matter how they are placed
        self.amino_acids[(0,0,0)] = self.sequence[0]
        self.amino_acids[(1,0,0)] = self.sequence[1]
        self.folds.append(1)
