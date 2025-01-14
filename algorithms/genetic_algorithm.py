from classes.protein_class import Protein
from algorithms.random import Random
import random

class Genetic(Random):
    def __init__(self, protein):
        super().__init__(protein)

    def populate(self):
        populations = {}

        for _ in range(3):
            population = Random(protein)
            print(population)
        #     score = self.protein.calculate_score(population)
        #     populations[population] = score
        #
        # print(populations)
        # return populations

# def calculate_fitness():
#
# def select_parents():
#
# def crossover():
#
# def mutate():
#
# def algorithm():
