import time
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from algorithms.beam import Beam

# define the parameter ranges to test (fixed iterations at 1000)
lookahead_values = [1, 3, 5, 7, 10]
max_size_values = [5, 10, 20, 50]
iterations = 1000

# store results for heatmap: Each row will contain [lookahead, max_size, best_score]
experiment_results = []

protein_sequence = "HHPHHHPHPHHHPH"
output_file = "beam_experiment.csv"
threeD = False

# Iterate over all combinations of lookahead depth and beam size
for lookahead in lookahead_values:
    for max_size in max_size_values:
        start_time = time.time()  

        # Run the Beam Search algorithm
        beam_algorithm = Beam(sequence=protein_sequence, max_size=max_size, output_file=output_file, threeD=threeD, lookahead_depth=lookahead)
        beam_algorithm.iterations = iterations
        beam_algorithm.run_experiment()

        # Record results and compute runtime
        best_score = beam_algorithm.best_score
        runtime = time.time() - start_time

        # Store data
        experiment_results.append([lookahead, max_size, best_score, runtime])

        print(f"Lookahead: {lookahead}, Max size: {max_size}, Best Score: {best_score}, Time: {runtime:.2f}s")

# Convert results into a NumPy array for visualization
experiment_results = np.array(experiment_results)

# Reshape data for heatmap plotting
best_scores = experiment_results[:, 2].reshape(len(lookahead_values), len(max_size_values))
runtimes = experiment_results[:, 3].reshape(len(lookahead_values), len(max_size_values))

# Create heatmap for Best Score analysis
plt.figure(figsize=(12, 8))
ax = sns.heatmap(
    best_scores,
    annot=runtimes,
    fmt=".2f",
    xticklabels=max_size_values,
    yticklabels=lookahead_values,
    cmap="coolwarm"
)

# Add title and labels
plt.title(f'Heatmap of Lookahead Depth vs Max Size (Best Score + Runtime)')
plt.xlabel('Max Size')
plt.ylabel('Lookahead Depth')

# Save and show the heatmap
plt.savefig(f"heatmap_lookahead_vs_maxsize_{protein_sequence}.png")
plt.show()
