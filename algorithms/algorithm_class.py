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
        """
        Executes the experiment by running the folding algorithm for a specified number of iterations.
        Tracks the best protein configuration based on the score and generates the output after all iterations.

        Attributes:
            self.iterations (int): The number of iterations to run the algorithm.
            self.best_score (float): The best score observed during the experiment.
            self.best_protein (Protein): The protein configuration corresponding to the best score.
            self.output_file (str): The file where results will be saved.
        """
        # Initialize the progress bar at the start of the experiment
        self.progress_bar(0, self.iterations)

        for i in range(self.iterations):
            # Execute the folding algorithm for the current iteration
            score = self.run()

            # If the current score is better (lower), update the best score and configuration
            self.progress_bar(i + 1, self.iterations)
            if score <= self.best_score:
                self.best_score = score
                self.best_protein = self.protein

        # Generate output files and visualizations after completing all iterations
        self.create_output(self.output_file)

    def check_legal_moves(self, amino_acids: OrderedDict):
        """
        Determines the set of legal moves for the next amino acid in the sequence.

        Legal moves are positions adjacent to the last placed amino acid that are:
        1. Not already occupied by other amino acids.
        2. Not surrounded in all possible directions by existing amino acids (to prevent overlap).

        Parameters:
            amino_acids (OrderedDict): A dictionary where keys are coordinates (x, y, z)
                                       and values are the corresponding amino acid types.

        Returns:
            set[tuple[int, int, int]] or None: A set of legal moves (coordinates) or None
                                               if no legal moves are available.
        """
        # Get the coordinates of the last placed amino acid
        x, y, z = next(reversed(amino_acids))

        # Define possible movement directions for 2D or 3D
        directions = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0)]
        if self.threeD:
            directions += [(0, 0, 1), (0, 0, -1)]

        # Calculate potential legal moves by applying all directions to the current position
        legal_moves = {(x + dx, y + dy, z + dz) for dx, dy, dz in directions}

        # Remove moves that overlap with existing amino acids
        legal_moves -= amino_acids.keys()

        # Remove moves surrounded in all directions by existing amino acids
        moves_to_remove = {
            move for move in legal_moves
            if all(
                (move[0] + dx, move[1] + dy, move[2] + dz) in amino_acids
                for dx, dy, dz in directions
                if (dx, dy, dz) != (0, 0, 0)
            )
        }
        legal_moves -= moves_to_remove

        # Return the legal moves or None if no valid moves remain
        return legal_moves if legal_moves else None

    def finish_up(self):
        """
        Finalizes the folding process for the protein.

        This method calculates the folds for the current protein configuration
        and appends a placeholder fold (0) to indicate the end of the sequence.

        The final fold is added as `0` because there is no subsequent amino acid
        to determine a direction.
        """
        self.calculate_folds()
        self.protein.folds.append(0)

    def create_output(self, output_file: str):
        """
        Creates an output file and visualizations for the protein folding results.

        This method performs the following actions:
        1. Converts the best protein's amino acid sequence and fold data to a CSV file.
        2. Draws a visualization of the best protein's folding structure.
        3. Analyzes and visualizes the folding process of the current protein.

        Parameters:
            output_file (str): The path where the output CSV file will be saved.

        Returns:
            None
        """
        # Convert the best protein's data (amino acids and folds) to a CSV file
        Visualise.data_to_csv(self.best_protein.amino_acids, self.best_protein.folds, output_file, self.best_protein)

        # Draw a visualization of the best protein's folding structure
        Visualise.draw(self.best_protein, self.best_score)

        # Perform an analysis for the algorithm
        # Visualise.analysis(self.protein, self.scores)

    def calculate_folds(self):
        """
        Calculates the folding directions of the protein based on the coordinates of its amino acids.

        This method compares the coordinates of consecutive amino acids in the protein sequence,
        calculates the differences between their positions, and maps those differences to specific
        fold directions. The fold directions are then stored in the `protein.folds` attribute.

        If the length of the amino acids does not match the length of the sequence, no folding
        calculation is performed.

        Returns:
            None
        """
        if len(self.protein.amino_acids) == len(self.protein.sequence):
            # Map differences in coordinates to fold directions
            direction_map = {
                (1, 0, 0): 1, (-1, 0, 0): -1,
                (0, 1, 0): 2, (0, -1, 0): -2,
                (0, 0, 1): 3, (0, 0, -1): -3
            }

            # Iterate through amino acids to calculate folds
            amino_acids_list = list(self.protein.amino_acids.items())
            for i in range(1, len(amino_acids_list) - 1):
                # Current and next coordinates
                x, y, z = amino_acids_list[i][0]
                x_next, y_next, z_next = amino_acids_list[i + 1][0]

                # Calculate the difference in coordinates
                delta = (x_next - x, y_next - y, z_next - z)

                # Determine the fold direction and append to folds
                fold = direction_map.get(delta)
                if fold is not None:
                    self.protein.folds.append(fold)
        else:
            pass

    def calculate_protein(self, folds:list[int]):
        """
        Calculates the 3D coordinates of the protein based on its fold directions.

        This method uses the provided list of fold directions to iteratively calculate the
        3D coordinates for each amino acid in the protein sequence, starting from a fixed
        initial coordinate. It updates the new protein object with these coordinates and
        returns the newly constructed protein.

        Parameters:
            folds (list[int]): A list of fold directions representing changes in coordinates.
                            Each integer corresponds to a specific fold direction, with
                            positive and negative values indicating direction.

        Returns:
            Protein: A new Protein object with the calculated 3D coordinates.
        """
        x,y,z = 1,0,0

        new_protein = Protein(self.protein.sequence, self.protein.output_file, self.protein.threeD)

        # Map fold directions to coordinate changes
        direction_map = {
            1: (1, 0, 0), -1: (-1, 0, 0),
            2: (0, 1, 0), -2: (0, -1, 0),
            3: (0, 0, 1), -3: (0, 0, -1)
        }

        # Skip the first 2 folds and exclude the last fold (0 is a placeholder)
        for i, fold in enumerate(folds[2:-1], start=2):

            # Update coordinates based on the fold direction
            dx, dy, dz = direction_map.get(fold, (0, 0, 0))
            x, y, z = x + dx, y + dy, z + dz

            # Add the new coordinate and amino acid to the protein
            new_protein.add_coordinate((x, y, z), self.protein.sequence[i])

        return new_protein

    def progress_bar(self, progress, total):
        """
        Displays a progress bar in the console to visualize the completion percentage.

        This method calculates the percentage of completion based on the current progress
        and the total amount. It then prints a text-based progress bar along with the percentage.

        Parameters:
            progress (int): The current progress value (should be between 0 and total).
            total (int): The total value representing the target or goal of the progress.

        Returns:
            None
        """
        percent = 100 * (progress / float(total))
        bar = chr(9608) * int(percent) + '-'* (100 - int(percent))
        print(f"\r|{bar}| {percent: .2f}%", end="")
