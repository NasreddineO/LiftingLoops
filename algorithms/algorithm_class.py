from collections import OrderedDict
from classes.visualise_class import Visualise
# from classes.visualise2 import Visualise

class Algorithm():
    def __init__(self, protein):
        self.protein = protein

    def check_legal_moves(self, dict: OrderedDict):
        x, y, z = next(reversed(dict))
        # 3D:
        legal_moves = set([
            (x + 1, y, z), (x - 1, y, z),
            (x, y + 1, z), (x, y - 1, z)])

        if self.protein.threeD:
            legal_moves.update([(x, y, z + 1), (x, y, z - 1)])


        legal_moves -= dict.keys()

        return legal_moves



    def finish_up(self, output_file: str):

        # the final fold is no direction, because there is no next direction
        self.protein.folds.append(0)

        Visualise.data_to_csv(self.protein.amino_acids, self.protein.folds, output_file, self.protein)
        Visualise.draw(self.protein)
