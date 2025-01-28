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

protein_sequence = "HPHPPHHPHPPHPHHPPHPH"
output_file = "beam_experiment.csv"
threeD = False

for lookahead in lookahead_values:
    for max_size in max_size_values:
        # run the Beam with fixed iterations but differences in size and depth
        beam_algorithm = Beam(sequence=protein_sequence, max_size=max_size, output_file=output_file, threeD=threeD, lookahead_depth=lookahead)
        beam_algorithm.iterations = iterations
        beam_algorithm.run_experiment()

        best_score = beam_algorithm.best_score

        # store data
        experiment_results.append([lookahead, max_size, best_score])

        print(f"Lookahead: {lookahead}, Max size: {max_size}, Best Score: {best_score}")

# convert results to a NumPy array for visualization
experiment_results = np.array(experiment_results)

# create heatmap for Best Score analysis
plt.figure(figsize=(12, 8))
heatmap_data = experiment_results[:, 2].reshape(len(lookahead_values), len(max_size_values))
sns.heatmap(heatmap_data, annot=True, fmt=".1f", xticklabels=max_size_values, yticklabels=lookahead_values, cmap="coolwarm")

# add title and labels
plt.title('Heatmap of Lookahead Depth vs Max Size (Best Score)')
plt.xlabel('Max Size')
plt.ylabel('Lookahead Depth')

# save and show the heatmap
plt.savefig(f"heatmap_lookahead_vs_maxsize_{protein_sequence}.png")
plt.show()
