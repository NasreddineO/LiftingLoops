from classes.protein_class import Protein
import random

class Genetic():
    def __init__(self, protein):
        super().__init__(protein)

    def populate(self, dict, type):
        length = len(self.protein.sequence)
        used_positions = [coordinate for coordinate in self.protein.amino_acids.keys()]

        for _ in range(length - 1):
            x, y, z = used_positions[-1]

            directions = set([(x + 1, y, z), (x - 1, y, z),
                                  (x, y + 1, z), (x, y - 1, z)])
            if self.protein.threeD:
                directions.update([(x, y, z + 1), (x, y, z - 1)])

            possible_moves = [pos for pos in directions if pos not in used_positions]

            if not possible_moves:
                break

            next_move = random.choice(possible_moves)
            self.protein.add_coordinate(self.protein.amino_acids, next_move, type)
            used_positions.add(next_move)

        return self.protein.amino_acids


# def calculate_fitness():
#
# def select_parents():
#
# def crossover():
#
# def mutate():
#
# def algorithm():
