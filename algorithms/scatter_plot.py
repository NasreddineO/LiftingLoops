import matplotlib.pyplot as plt
import numpy as np
from algorithms.beam import Beam

# define the protein sequence and experiment parameters
protein_sequence = "HHPHHHPHPHHHPH"
output_file = "output.txt"
threeD = True

# define the range of lookahead depths to test
lookahead_depths = range(1, 11)

# store results for plotting
depth_values = []
score_values = []

# run the experiment for different lookahead depths
for depth in lookahead_depths:
    beam_algorithm = Beam(sequence=protein_sequence, max_size=10, output_file=output_file, threeD=threeD, lookahead_depth=depth)
    final_score = beam_algorithm.run()

    depth_values.append(depth)
    score_values.append(final_score)

    print(f"Lookahead depth: {depth}, Final score: {final_score}")

# create scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(depth_values, score_values, color='blue', edgecolors='black', alpha=0.7)
plt.plot(depth_values, score_values, color='red', linestyle='--', label="Trend Line")

# adding labels, title and grid
if threeD == False:
    plt.title(f'Influence of Lookahead Depth on Beam Algorithm Score for {protein_sequence} in 2D', fontsize=16)
else:
    plt.title(f'Influence of Lookahead Depth on Beam Algorithm Score for {protein_sequence} in 3D', fontsize=16)
plt.xlabel('Lookahead Depth', fontsize=14)
plt.ylabel('Final Score', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.6)

# show legend
plt.legend()

# save the plot
if threeD == False:
    plt.savefig(f"Lookahead_vs_Score_{protein_sequence}.png")
    print("Plot saved as Lookahead_vs_Score.png")
else:
    plt.savefig(f"Lookahead_vs_Score_3D_{protein_sequence}.png")

# show the plot
plt.show()
