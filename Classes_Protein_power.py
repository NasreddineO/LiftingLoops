# Names: Hendrik DuPont, Jeppe Mul & Nasreddine Ouchene
# This script contains a Protein class with methods that are intended to come together in an algorithm to fold the protein.
# This script is in partial fulfillment of the requirements for Algoritmen en Heuristieken at the University of Amsterdam.

from collections import OrderedDict
import csv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Protein():
    def __init__(self, sequence: str, output_file: str, threeD: bool):

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

    def step(self, dict: OrderedDict, type: str):
        legal_moves = self.check_legal_moves(dict)
        next_move = self.evaluate_moves(legal_moves, dict)
        self.update_values(dict, next_move, type)

    def check_legal_moves(self, dict: OrderedDict):
        x, y, z = next(reversed(dict))
        # 3D:
        legal_moves = set([
            (x + 1, y, z), (x - 1, y, z),
            (x, y + 1, z), (x, y - 1, z)])

        if self.threeD:
            legal_moves.update([(x, y, z + 1), (x, y, z - 1)])


        legal_moves -= dict.keys()

        return legal_moves

    def evaluate_moves(self, legal_moves: set, dict: OrderedDict):
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

        next_move = (x_next, y_next, z_next)
        self.folds.append(fold)

        return next_move

    def update_values(self, dict: OrderedDict, coordinate:tuple[int, int, int], type: str):
        dict[coordinate] = type

        return dict

    def data_to_csv(self, dict: OrderedDict, folds: list):
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

            score = self.calculate_score(self.amino_acids)
            file.write(f"score,{score}")

        print(f"CSV file created successfully.")


    def visualise(self, dict):
        types = list(dict.values())

        if self.threeD:
            # Separate x, y, z
            coordinates = list(dict.keys())
            x, y, z = zip(*coordinates)

            # Plotting
            fig = plt.figure(figsize=(10, 8))
            ax = fig.add_subplot(projection='3d')

            # Scatter plot
            ax.scatter(x, y, z, s=0, label='Aminoacids')

            # Connect points to visualize folding
            ax.plot(x, y, z, color='gray', linewidth=1, alpha=0.6)

            # Add the amino type as marker and give individual color
            for xi, yi, zi, label in zip(x, y, z, types):
                color = 'red' if label == 'H' else 'blue'
                ax.text(xi, yi, zi, label, fontsize=15, ha='center', va='center', color=color)

            # Labels en title
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            ax.set_title('3D Amino Acid Fold Visualization')

            # Legend
            ax.legend(loc='upper left')
            plt.show()

        else:
            coordinates = [(x, y) for x, y, z in dict.keys()]
            x, y = zip(*coordinates)

            # Plotting
            fig = plt.figure(figsize=(10, 8))
            ax = fig.add_subplot()

            # Scatter plot
            ax.scatter(x, y, s=0, label='Aminoacids')

            # Connect points to visualize folding
            ax.plot(x, y, color='gray', linewidth=1, alpha=0.6)

            for xi, yi, label in zip(x, y, types):
                color = 'red' if label == 'H' else 'blue'
                ax.text(xi, yi, label, fontsize=15, ha='center', va='center', color=color)

            # Labels and title
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_title('2D Amino Acid Fold Visualization')

            # Show legend
            plt.legend(loc='upper left')
            plt.show()
