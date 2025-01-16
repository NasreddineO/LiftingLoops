import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.lines import Line2D
from collections import OrderedDict
import csv

class Visualise():
    """
    A class to visualize protein folds in 2D or 3D space, using data from a Protein instance.
    """

    def draw(protein):
        """
        Visualize a protein fold in 2D or 3D space.

        Parameters:
            self: object
                An instance of the class containing the method, with attributes:
                - `threeD` (bool): Indicates whether to visualize in 3D (True) or 2D (False).
                - `adjacent_amino_acids` (dict): A dictionary mapping pairs of coordinates
                  to bond types (e.g., 'H-H', 'H-C').
            dict: dict
                A dictionary where keys are tuples of coordinates (x, y, z) and values
                are amino acid types ('H', 'P', 'C').

        Behavior:
            - Plots the backbone of the folded protein.
            - Colors and labels amino acids based on their type.
            - Adds dashed lines for specific bonds between adjacent amino acids.
            - Supports both 2D and 3D visualizations, depending on the `threeD` attribute.

        Returns:
            None
        """
        types = list(protein.amino_acids.values())
        amino_colors = {'H': 'red', 'P': 'yellow', 'C': 'blue'}
        line_colors = {'H-H': 'red', 'H-C': 'black', 'C-C': 'blue'}
        scatter_handles = []
        line_handles = []
        seen_line_types = set()

        # Determine coordinates based on dimensionality
        if protein.threeD:
            coordinates = list(protein.amino_acids.keys())
            x, y, z = zip(*coordinates)
        else:
            coordinates = [(x, y) for x, y, z in protein.amino_acids.keys()]
            x, y = zip(*coordinates)

        # Create figure
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(projection='3d' if protein.threeD else None)

        # Scatter plot for amino acids
        for coord, label in zip(coordinates, types):
            scatter_args = {'s': 100, 'c': amino_colors[label], 'label': label}
            sc = ax.scatter(*coord, **scatter_args) if protein.threeD else ax.scatter(*coord[:2], **scatter_args)
            if label not in [handle.get_label() for handle in scatter_handles]:
                scatter_handles.append(sc)

        # Plotting the folded protein backbone
        if protein.threeD:
            ax.plot(x, y, z, color='black', linewidth=3, alpha=0.6)
        else:
            ax.plot(x, y, color='black', linewidth=3, alpha=0.6)

        # Plot dashed lines between adjacent amino acids
        for (coord1, coord2), line_type in protein.adjacent_amino_acids.items():
            line_color = line_colors[line_type]
            if protein.threeD:
                x1, y1, z1 = coord1
                x2, y2, z2 = coord2
                ax.plot([x1, x2], [y1, y2], [z1, z2], linestyle=':', color=line_color, linewidth=2)
            else:
                x1, y1, _ = coord1
                x2, y2, _ = coord2
                ax.plot([x1, x2], [y1, y2], linestyle=':', color=line_color, linewidth=2)

            if line_type not in seen_line_types:
                seen_line_types.add(line_type)
                line_handles.append(Line2D([0], [0], color=line_color, linestyle=':', linewidth=2, label=f'{line_type} Bond'))

        # Add labels and title
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        if protein.threeD:
            ax.set_zlabel('Z')
            ax.set_title('3D Amino Acid Fold Visualization')
        else:
            ax.set_title('2D Amino Acid Fold Visualization')

        # Add legend
        legend_handles = scatter_handles + line_handles

        plt.legend(handles=legend_handles, loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0.)
        # ax.axis('off')
        plt.tight_layout()
        plt.show()


    def data_to_csv(dict: OrderedDict, folds: list, output_file: str, protein):
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

            score = protein.calculate_score()
            file.write(f"score,{score}")

        print(f"CSV file created successfully.")
