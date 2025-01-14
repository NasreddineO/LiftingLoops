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

        # dictionary {coordinate: type}
        self.amino_acids = OrderedDict()
        self.folds = []
        self.adjacent_amino_acids = []

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
                        self.adjacent_amino_acids.append((amino_list[acid1][0], amino_list[acid2][0]))
                        score -= 1
                    elif set(amino_list[acid1][1] + amino_list[acid2][1]) == {'H', 'C'}:
                        self.adjacent_amino_acids.append((amino_list[acid1][0], amino_list[acid2][0]))
                        score -= 1
                    elif set(amino_list[acid1][1] + amino_list[acid2][1]) == {'C'}:
                        self.adjacent_amino_acids.append((amino_list[acid1][0], amino_list[acid2][0]))
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

    def add_coordinate(self, dict: OrderedDict, coordinate:tuple[int, int, int], type: str):
        dict[coordinate] = type

        return dict

    def data_to_csv(self, dict: OrderedDict, folds: list, output_file: str):
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
        with open(f"{output_file}", mode="w", newline="") as file:

            writer = csv.writer(file)

            writer.writerow(["amino", "fold"])

            for amino, fold in zip(dict.values(), folds):
                writer.writerow([amino, fold])

            score = self.calculate_score(self.amino_acids)
            file.write(f"score,{score}")

        print(f"CSV file created successfully.")


    def visualise(self, dict):
        types = list(dict.values())
        colors = {'H': 'red', 'P': 'blue', 'C': 'green'}

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
            ax.plot(x, y, color='gray', linewidth=2, alpha=0.6)

            scatter_handles = []
            for xi, yi, label in zip(x, y, types):
                sc = ax.scatter(xi, yi, s=100, c=colors[label], label=label)

                if label not in [handle.get_label() for handle in scatter_handles]:
                    scatter_handles.append(sc)

            for (x1, y1, z1), (x2, y2, z2) in self.adjacent_amino_acids:
                ax.plot([x1, x2], [y1, y2], linestyle=':', color='purple', linewidth=2)

            # Labels and title
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_title('2D Amino Acid Fold Visualization')

            # Place the legend outside the plot area
            plt.legend(handles=scatter_handles, loc='upper left')

            # Show the plot
            plt.show()
