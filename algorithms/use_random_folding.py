from .random_folding import RandomFolding

protein_sequence = "HHPHHHPH"
output_file = "output.csv"
random_folding = RandomFolding(sequence=protein_sequence, iterations=100, output_file=output_file, threeD=False)
score = random_folding.run()

print(f"Best score obtained: {score}")
