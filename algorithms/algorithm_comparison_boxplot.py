import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import time

# import the algorithms
from algorithms.beam import Beam
from algorithms.random_folding import RandomFolding
from algorithms.pull_move_climber import PullMoveClimber

# define the protein sequence and output file
protein_sequence = "HHPHHHPH"
output_file = "output.csv"
threeD = False

# define the best parameters found for Beam Search (still loading..)
best_lookahead = 4
best_max_size = 20

# store results in a list for visualization
algorithm_scores = []

# run Beam Search and measure the total execution time
beam_start_time = time.time()
beam_algorithm = Beam(sequence=protein_sequence, max_size=best_max_size, output_file=output_file, threeD=threeD, lookahead_depth=best_lookahead)
beam_algorithm.run_experiment()
beam_time = time.time() - beam_start_time

# append each recorded score from Beam Search to the results list
for score in beam_algorithm.all_scores:
    algorithm_scores.append(("Beam", score))

# run Random Folding for the same duration as Beam
random_folding = RandomFolding(sequence=protein_sequence, iterations=1, output_file=output_file, threeD=threeD)
random_folding_scores = []
random_folding_start_time = time.time()

# this loop ensures that Random Folding runs for the same amount of time as Beam
while time.time() - random_folding_start_time < beam_time:
    random_folding.run()
    random_folding_scores.extend(random_folding.all_scores)

# append scores for Random Folding
for score in random_folding_scores:  # Fixed variable reference
    algorithm_scores.append(("Random Folding", score))

# run Pull Move Climber for the same duration as Beam
protein_instance = Protein(protein_sequence, threeD=threeD) 
pull_climber = PullMoveClimber(sequence=protein_sequence, iterations=1, output_file=output_file, threeD=threeD, protein=protein_instance)
pull_climber_scores = []
pull_climber_start_time = time.time()

# this loop ensures that Pull Move Climber runs for the same amount of time as Beam
while time.time() - pull_climber_start_time < beam_time:
    pull_climber.run()
    pull_climber_scores.extend(pull_climber.scores)

# append scores for Pull Move Climber
for score in pull_climber_scores:
    algorithm_scores.append(("Pull Move Climber", score))

# convert results to a DataFrame for plotting
df = pd.DataFrame(algorithm_scores, columns=["Algorithm", "Score"])

# boxplot comparing score distributions across the algorithms
plt.figure(figsize=(10, 6))
sns.boxplot(x="Algorithm", y="Score", data=df, palette="coolwarm")

# add labels and title to the plot
plt.title(f"Algorithm Comparison with Equal Runtime ({beam_time:.2f} seconds)")
plt.xlabel("Algorithm")
plt.ylabel("Score")
plt.grid(True, linestyle="--", alpha=0.6)

# save the boxplot to a file and display it
plt.savefig("algorithm_comparison_boxplot.png")
plt.show()

# print the execution time for each algorithm to verify that they ran for the same duration
print(f"Beam runtime: {beam_time:.2f} seconds")
print(f"Random Folding runtime: {time.time() - random_folding_start_time:.2f} seconds")
print(f"Pull Move Climber runtime: {time.time() - pull_climber_start_time:.2f} seconds")
