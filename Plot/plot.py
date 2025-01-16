import matplotlib.pyplot as plt
import numpy as np

# protein and list of scores
protein = 'HHPHHHPHPHHHPH'
scores = [-3, -3, -2, -2, -2, -2, -3, 0, -3, -1]

# create the histogram
plt.figure(figsize=(10, 6))
n, bins, patches = plt.hist(scores, bins=10, edgecolor='black')

# set x-axis ticks to integer
plt.xticks(ticks=np.arange(min(scores), 1, 1))

"""
The goal is to adjust the color of each histogram bar based on its frequency.
To do this, you scale the frequencies to a range between 0 and 1,
making it easier to map them to colors.
"""
# normalise between 0 and 1
normalized_frequencies = n / max(n)

# use a colormap to set bar colours based on normalised frequencies
cm = plt.cm.Blues

# https://stackoverflow.com/questions/46123927/how-can-i-change-this-code-to-output-an-histogram-with-colors-depending-on-heigh
# combines each normalised frequency with its corresponding patch (histogram bar)
for intensity, patch in zip(normalized_frequencies, patches):
    # 0.3 is the base color, 0.7 * intensity (makes the color darker based on the frequency)
    plt.setp(patch, 'facecolor', cm(0.3 + 0.7 * intensity))


# https://www.geeksforgeeks.org/how-to-annotate-bars-in-barplot-with-matplotlib-in-python/
# annotate bar hight only when higher than zero
for patch in patches:
    # get the height of the bar
    height = patch.get_height()
    # only annotate if the height is greater than 0
    if height > 0:
        plt.text(patch.get_x() + patch.get_width() / 2,
                 height,
                 f'{int(height)}',
                 ha='center', va='bottom', fontsize=10)

# labels and title
plt.title(f'Frequency of Scores for Protein: {protein} in {len(scores)} iterations', fontsize=10)
plt.xlabel('Score', fontsize=10)
plt.ylabel('Frequency', fontsize=10)

# add gridlines
plt.grid(axis='y', linestyle='--', alpha=0.7)

# save the plot as an image file
filename = f"{protein}_{len(scores)}_iterations.png"
plt.tight_layout()
plt.savefig(filename)
plt.show()
