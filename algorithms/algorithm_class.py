from collections import OrderedDict

class Algorithm():
    def __init__(self, protein):
        self.protein = protein



    def check_legal_moves(self, dict: OrderedDict):

        x, y, z = next(reversed(dict))
        # 3D
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

        self.protein.data_to_csv(self.protein.amino_acids, self.protein.folds, output_file)
        self.protein.visualise(self.protein.amino_acids)

    def calculate_folds(self):
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
