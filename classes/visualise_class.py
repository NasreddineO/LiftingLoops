import matplotlib.pyplot as plt
import csv
import numpy as np
from scipy.stats import norm
from collections import Counter
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.lines import Line2D
from collections import OrderedDict

class Visualise():
    """
    A class to visualize protein folds in 2D or 3D space, using data from a Protein instance.
    """

    @staticmethod
    def draw(protein, score):
        """
        Visualize a protein fold in 2D or 3D space.

        Parameters:
            protein: object
                An instance of the class containing the method, with attributes:
                - `threeD` (bool): Indicates whether to visualize in 3D (True) or 2D (False).
                - `adjacent_amino_acids` (dict): A dictionary mapping pairs of coordinates
                  to bond types (e.g., 'H-H', 'H-C').
            score: float
                The stability score of the protein.

        Behavior:
            - Plots the backbone of the folded protein.
            - Colors and labels amino acids based on their type.
            - Adds dashed lines for specific bonds between adjacent amino acids.
            - Supports both 2D and 3D visualizations, depending on the `threeD` attribute.

        Returns:
            None
        """
        amino_colors = {'H': 'red', 'P': 'yellow', 'C': 'blue'}
        line_colors = {'H-H': 'red', 'H-C': 'black', 'C-C': 'blue'}
        scatter_handles = []
        line_handles = []
        seen_line_types = set()

        # Convert coordinates and types to NumPy arrays
        coords = np.array(list(protein.amino_acids.keys()))
        types = np.array(list(protein.amino_acids.values()))

        # Create figure
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(projection='3d' if protein.threeD else None)

        # Scatter plot for amino acids (grouped by type for legend clarity)
        for type, color in amino_colors.items():
            mask = (types == type)
            if not np.any(mask):
                continue
            group_coords = coords[mask]
            if protein.threeD:
                sc = ax.scatter(group_coords[:, 0], group_coords[:, 1], group_coords[:, 2], color=color, s=100, label=type)
            else:
                sc = ax.scatter(group_coords[:, 0], group_coords[:, 1], color=color, s=100, label=type)
            scatter_handles.append(sc)

        # Plotting the folded protein backbone
        if protein.threeD:
            ax.plot(coords[:, 0], coords[:, 1], coords[:, 2], color='black', linewidth=3, alpha=0.6)
        else:
            ax.plot(coords[:, 0], coords[:, 1], color='black', linewidth=3, alpha=0.6)

        # Plot dashed lines between adjacent amino acids
        bond_coords = np.array([(coord1, coord2) for (coord1, coord2) in protein.adjacent_amino_acids.keys()])
        bond_types = np.array([bond_type for bond_type in protein.adjacent_amino_acids.values()])

        for bond, bond_type in zip(bond_coords, bond_types):
            line_color = line_colors.get(bond_type)
            x_vals, y_vals = bond[:, 0], bond[:, 1]
            if protein.threeD:
                z_vals = bond[:, 2]
                ax.plot(x_vals, y_vals, z_vals, color=line_color, linestyle=':', linewidth=2)
            else:
                ax.plot(x_vals, y_vals, color=line_color, linestyle=':', linewidth=2)

            if bond_type not in seen_line_types:
                seen_line_types.add(bond_type)
                line_handles.append(Line2D([], [], color=line_color, linestyle=':', linewidth=2, label=f'{bond_type} Bond'))

        # Add labels and title
        ax.set_xlabel('X Axis')
        ax.set_ylabel('Y Axis')
        if protein.threeD:
            ax.set_zlabel('Z Axis')
            ax.set_title(f'3D Protein Structure (Score: {score})')
        else:
            ax.set_title(f'2D Protein Structure (Score: {score})')

        # Add legend
        all_handles = scatter_handles + line_handles

        plt.legend(handles=all_handles, loc='upper left', bbox_to_anchor=(1.05, 1))
        plt.tight_layout()

    @staticmethod
    def data_to_csv(amino_data: OrderedDict, folds: list[int], output_file: str, protein):
        """
        Writes amino acid types and their corresponding folds to a CSV file, including protein stability score.

        Parameters:
            amino_data (OrderedDict):
                Keys: (x, y, z) coordinates as tuples
                Values: Amino acid types ('H', 'P', 'C')
            folds (list[int]):
                List of fold directions corresponding to amino acids
            output_file (str):
                Path/filename for output CSV
            protein (Protein):
                Protein object containing calculate_score() method

        Output:
            CSV file with structure:
            - Header: ["amino", "fold"]
            - Data rows: (amino acid type, fold direction)
            - Final row: ["score", stability_score]
        """

        with open(output_file, mode="w", newline="") as file:
            writer = csv.writer(file)

            # Write header
            writer.writerow(["amino", "fold"])

            # Write data rows
            for amino, fold in zip(amino_data.values(), folds):
                writer.writerow([amino, fold])

            # Calculate and write score
            score = protein.calculate_score()
            writer.writerow(["score", score])

        print(f"\nSuccessfully created CSV file: {output_file}")

    @staticmethod
    def analysis(protein, scores: list[int]):
        """
        Generates a bar plot with a smooth curve for the frequency distribution of scores.

        Parameters:
            protein (Protein): A protein object with __str__ method
            scores (list[int]): List of integer scores to analyze

        Behavior:
            - Properly scales Gaussian curve
            - Ensures plot clarity
        """
        # Count frequencies
        counter = Counter(scores)
        unique_scores = sorted(counter.keys())
        frequencies = [counter[score] for score in unique_scores]

        # Plot the frequencies
        plt.figure(figsize=(10, 6))
        bars = plt.bar(unique_scores, frequencies, color='skyblue', edgecolor='black')

        # Create proper colormap scaling
        cmap = plt.cm.Blues
        max_freq = max(frequencies) or 1  # Prevent division by zero
        normalized = [f/max_freq for f in frequencies]

        # Set bar colors based on the normalized frequencies
        for bar, intensity in zip(bars, normalized):
            bar.set_facecolor(cmap(0.3 + 0.7 * intensity))

        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, height,
                     f'{height}', ha='center', va='bottom', fontsize=9)

        # Calculate Gaussian distribution
        if len(scores) >= 2:
            mean = np.mean(scores)
            std = np.std(scores)
            if std != 0:  # Skip Gaussian if all scores are identical
                x = np.linspace(min(scores) - 1, max(scores) + 1, 500)
                scale_factor = len(scores)
                y = norm.pdf(x, mean, std) * scale_factor
                plt.plot(x, y, 'r--', linewidth=2, label='Gaussian Fit')

        # Configure axes and labels
        plt.title(f'Score Distribution: {protein.sequence} ({len(scores)} iterations)', fontsize=12)
        plt.xlabel('Score', fontsize=10)
        plt.ylabel('Frequency', fontsize=10)
        plt.xticks(np.arange(min(unique_scores), max(unique_scores)+1))
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Save and clean up
        filename = f"analysis/{protein.sequence}_{len(scores)}_iterations.png"
        plt.tight_layout()
        plt.savefig(filename, dpi=300)
        plt.close()

        print(f"Saved analysis plot to {filename}")
