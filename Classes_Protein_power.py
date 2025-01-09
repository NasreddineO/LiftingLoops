from collections import OrderedDict
import csv

class Protein():
    def __init__(self, sequence, output_file, threeD):

        self.sequence = sequence
        self.output_file = output_file
        self.threeD = threeD

        # dictionary {coordinate: {"type": type, "fold": fold}}
        self.amino_acids = OrderedDict()
        self.folds = []

        # add initial amino acids and fold, as rotational symmetry dictates that the first 2 amino acids are functionally identical no matter how they are placed
        self.amino_acids[(0,0,0)] = self.sequence[0]
        self.amino_acids[(1,0,0)] = self.sequence[1]
        self.folds.append(1)

    def step(self, dict, type):
        self.check_legal_moves(dict)
        self.evaluate_moves(self.legal_moves, dict)
        self.update_values(dict, self.next_move, type)

    def check_legal_moves(self, dict):
        x, y, z = next(reversed(dict))
        # 3D:
        self.legal_moves = [
            (x + 1, y, z), (x - 1, y, z),
            (x, y + 1, z), (x, y - 1, z),
            (x, y, z + 1), (x, y, z - 1)
        ]

        self.legal_moves -= dict.keys()

        return self.legal_moves

    def evaluate_moves(self, legal_moves, dict):
        # Voor nu: gewoon de keten verlengen zonder score in gedachten te houden. Oftewel de eerste coor in de set
        x_next, y_next, z_next = next(iter(legal_moves))
        x, y, z = next(reversed(dict))

        # check the direction of the move by checking the difference between te current coordinate and next move
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

        self.next_move = (x_next, y_next, z_next)
        self.folds.append(fold)

        return self.next_move, self.folds

    def update_values(self, dict, coor, type):
        dict[coor] = type

        return dict

    def data_to_csv(self, dict, folds):
        """
        Extracts the type of aminoacid (string) and the corresponding fold (int) from a dictionary
        and writes it to a CSV-file.

        Input:
        - data (dict): a nested dictionary containing the coordinates of the aminoacids as keys
                       and the type and fold as nested dictionaries.

        Output:
        - protein_data.csv: a csv-file containing the type of aminoacid and the fold,
                            including the final score for the stability of the protein
        """
        with open("protein_data.csv", mode="w", newline="") as file:

            writer = csv.writer(file)

            writer.writerow(["Amino", "Fold"])

            for amino, fold in zip(dict.values(), folds):
                writer.writerow([amino, fold])

        # file.write(f"score,{score}")
        
        print(f"CSV file created successfully.")
