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

        return legal_moves



    def finish_up(self, output_file: str):

        # the final fold is no direction, because there is no next direction
        self.protein.folds.append(0)

        self.protein.data_to_csv(self.protein.amino_acids, self.protein.folds, output_file)
        self.protein.visualise(self.protein.amino_acids)
