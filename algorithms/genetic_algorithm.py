from classes.protein_class import Protein
from algorithms.random import Random
import random

class Genetic(Random):
    def __init__(self, protein):
        super().__init__(protein)

    def populate(self):
        populations = {}

        for _ in range(3):
            self.population = Random(protein)
            print(self.population)
        #     score = self.protein.calculate_score(population)
        #     populations[population] = score
        #
        # print(populations)
        # return populations

def calculate_fitness(self):
    """
    Calculates the score of a folded protein using the calculate_score method from the Protein class.
    """
    return self.protein.calculate_score(self.population)

def select_parents(self, scores):
    """
    selects parents from the population to generate a new generation.
    """
    sorted_scores = dict(sorted(scores.items(), key=lambda item: item[1]))
    parents = list(sorted_scores.keys())[:2]

    return parents[0], parents[1]

def crossover(parent1, parent2):
    split = random.randint(1, len(parent1) - 1)

    # Maak een kind door de eerste helft van parent1 en de tweede helft van parent2
    child = parent1[:split] + parent2[split:]

    # Bereken de vouw van het kind op basis van de nieuwe structuur
    child_fold = calculate_fold(child)

    # Update de score van de vouw van het kind
    child_score = fold_dict.get(child_fold, None)

    return child, child_fold, child_score

    return parent1[:split] + parent2[split:]

def mutate():
    if random.random() < mutation_rate:
        index = random.randint(0, len(folding) - 1)
        directions = ['U', 'D', 'L', 'R']
        folding[index] = random.choice(directions)
    return folding
#
# def algorithm():
