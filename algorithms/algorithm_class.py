from collections import OrderedDict
from classes.visualise_class import Visualise
from classes.protein_class import Protein

class Algorithm():
    def __init__(self, sequence: str, iterations: int, output_file: str, threeD: bool):

        self.sequence = sequence
        self.iterations = iterations
        self.output_file = output_file
        self.threeD = threeD

        self.best_score = 0
        self.best_protein = None
        self.scores = []

    def run_experiment(self):
        for i in range(self.iterations):
            score = self.run()

            if score <= self.best_score:
                self.best_score = score
                self.best_protein = self.protein

        self.create_output(self.output_file)

    def check_legal_moves(self, dict: OrderedDict):
        x, y, z = next(reversed(dict))
        # 3D:
        legal_moves = set([
            (x + 1, y, z), (x - 1, y, z),
            (x, y + 1, z), (x, y - 1, z)])

        if self.protein.threeD:
            legal_moves.update([(x, y, z + 1), (x, y, z - 1)])


        legal_moves -= dict.keys()

        # remove moves
        moves_to_remove = set()
        for x,y,z in legal_moves:
            if (x+1,y,z) in self.protein.amino_acids and (x-1,y,z) in self.protein.amino_acids and (x,y+1,z) in self.protein.amino_acids and (x,y-1,z) in self.protein.amino_acids:
                if not self.protein.threeD or ((x,y,z+1) in self.protein.amino_acids and (x-1,y,z-1) in self.protein.amino_acids):
                    moves_to_remove.add((x,y,z))

        legal_moves -= moves_to_remove

        if legal_moves != set():
            return legal_moves

        #pass None if no legal moves are found
        else:
            return None



    def finish_up(self):

        # calculate the folds
        self.calculate_folds()

        # the final fold is no direction, because there is no next direction
        self.protein.folds.append(0)

    def create_output(self, output_file: str):

        Visualise.data_to_csv(self.best_protein.amino_acids, self.best_protein.folds, output_file, self.best_protein)
        Visualise.draw(self.best_protein)

    def calculate_folds(self):

        if len(self.protein.amino_acids) == len(self.protein.sequence):

            for amino_acid in range(len(self.protein.amino_acids)-1):
                x,y,z = list(self.protein.amino_acids.items())[amino_acid][0]
                x_next, y_next, z_next = list(self.protein.amino_acids.items())[amino_acid+1][0]

                if x_next - x == 1:
                    fold = 1
                elif x_next - x == -1:
                    fold = -1
                elif y_next - y == 1:
                    fold = 2
                elif y_next - y == -1:
                    fold = -2
                elif z_next - z == 1:
                    fold = 3
                elif z_next - z == -1:
                    fold = -3

                self.protein.folds.append(fold)
        else:
            pass

    def calculate_protein(self, folds:list[int]):
        x,y,z = 1,0,0

        new_protein = Protein(self.protein.sequence, self.protein.output_file, self.protein.threeD)

        # We wish to avoid 3 folds, namely the first two which are initialized as base cases and the last 0 fold.
        for fold in range(len(folds)-3):

            # Avoiding the first 2 folds by adding two to the index
            if folds[fold+2] == 1:
                x += 1
            elif folds[fold+2] == -1:
                x -= 1
            elif folds[fold+2] == 2:
                y += 1
            elif folds[fold+2] == -2:
                y -= 1
            elif folds[fold+2] == 3:
                z += 1
            elif folds[fold+2] == -3:
                z -= 1

            new_protein.add_coordinate(new_protein.amino_acids, (x,y,z), self.protein.sequence[fold])

        print(new_protein.amino_acids)
