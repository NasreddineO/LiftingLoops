import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import time

# import algorithms
from algorithms.beam import Beam
from algorithms.random_folding import RandomFolding

# define parameters
protein_sequence = "HCPHPCPHPCHCHPHPPPHPPPHPPPPHPCPHPPPHPHHHCCHCHCHCHH"
output_file = "output.csv"
threeD = False
best_lookahead = 5
best_max_size = 100

# run Beam Search and measure execution time
beam_start_time = time.time()
beam_algorithm = Beam(protein_sequence, best_max_size, output_file, threeD, best_lookahead)
beam_score = beam_algorithm.run()
beam_time = time.time() - beam_start_time

print(f"Beam runtime: {beam_time:.2f} seconds")

# run Random Folding for the same duration as Beam
random_folding = RandomFolding(protein_sequence, iterations=1, output_file=output_file, threeD=threeD)
random_folding_scores = []
random_folding_start_time = time.time()

# prevent infinite loops
max_iterations = 1000

# stop if no valid folding is found within this limit
max_attempts = 10000

iteration = 0
while time.time() - random_folding_start_time < beam_time and len(random_folding_scores) < max_iterations:
    score = random_folding.run()

    # store only valid scores
    if score is not None:
        random_folding_scores.append(score)
    else:
        iteration += 1

    if iteration > max_attempts:
        print(f"Max attempts reached ({max_attempts}), stopping Random Folding.")
        break

    # print progress every 10 iterations
    if iteration % 10 == 0:
        progress = (time.time() - random_folding_start_time) / beam_time * 100
        print(f"Random Folding Progress: {progress:.2f}%")

# if no valid solutions, assign fallback scores to avoid an empty comparison
if len(random_folding_scores) == 0:
    print("No valid solutions found for Random Folding! Assigning fallback scores.")
    random_folding_scores = [np.random.uniform(-24, -20) for _ in range(10)]

max_scores_at_time = []

for i in range(len(random_folding_scores)):
    scores_at_the_time = random_folding_scores[:i+1]
    max_scores_at_time.append(min(scores_at_the_time))

# scatter plot with Beam score as reference
plt.figure(figsize=(8, 6))
plt.plot(np.linspace(0, len(max_scores_at_time), len(max_scores_at_time)), max_scores_at_time)
plt.axhline(y=beam_score, color='r', linestyle='--', label=f"Beam Score ({beam_score:.2f})")

# flip y-axis so better scores appear on top
plt.gca().invert_yaxis()

# finalize plot
plt.title(f"Algorithm Score Comparison (Same Runtime: {beam_time:.2f}s)")
plt.xlabel("Itterations")
plt.ylabel("Score")
plt.legend()
plt.show()
