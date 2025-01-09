class AminoAcid():
    def __init___(self, type, x, y):
        # type amino acid
        self.type = type

        # coordinaten
        self.x = x
        self.y = y

class Grid():
    def __init__(self, size):
        self.size = size
        self.score = 0

        """
        2D => Mijn manier van denken + onderaan list comprehension
        """
        grid = []

        # maak een lege row voor elke itteratie gebaseerd op size
        for i in range(size):
            row = []

            # voeg een None toe voor elke itteratie gebaseerd op size (columns)
            for j in range(size):
                row.append(None)

            # voeg de rows en columns toe aan de grid
            grid.append(row)

        # list comprehension
        self.grid = [[None for _ in range(size)] for _ in range(size)]

        """
        3D => Mijn manier van denken, onderaan list comprehension
        """
        for i in range(size):
            layer = []
            for j in range(size):
                row =[]
                for k in range(size):
                    row.append(None)
                layer.append(row)
            grid.append(layer)

        # list comprehension
        self.grid = [[[None for _ in range(size)] for _ in range(size)]for _ in range(size)]

    def place_amino_acid(self, aminoacid):

        # check of de x en y van de amino acid vallen binnen de grid
        if 0 <= amino_acid.x < self.size and 0 <= amino_acid.y < self.size:

            # check of de positie in de grid leeg is
            if self.grid[amino_acid.x][amino_acid.y] is None:

                """
                als de positie leeg is verander hem dan met het gehele amino acid
                object en niet allen het type, dit omdat we later willen refereren
                naar de waardes van de amino acid.
                """
                self.grid[amino_acid.x][amino_acid.y] = amino_acid
            else:
                raise ValueError("There is already an amino acid at this position.")


    def calculate_score(self):
        score = 0
        """
        2D
        """
        # loop door de 2D grid van de eiwitstructuur
        for i in range(self.size):
            for j in range(self.size):

                # controleer of er een aminozuur aanwezig is
                if self.grid[i][j] is not None:

                    # check voor aangrenzende aminozuren in de 2D ruimte (H-H bonds)
                    directions = [
                        (1, 0),  # rechts
                        (0, 1),  # beneden
                        (-1, 0), # links
                        (0, -1)  # boven
                    ]
                    """
                    Voor elke richting voegen we de dx en dy toe aan de
                    huidige coördinaten (i, j) om de nieuwe coördinaten (nx, ny)
                    van de buurcel te berekenen.
                    """
                    for dx, dy in directions:
                        nx, ny = i + dx, j + dy

                        # controleer of buurcel binnen de grid valt
                        if 0 <= nx < self.size and 0 <= ny < self.size:

                            # controle van het type aminozuur van de buurcel
                            neighbor = self.grid[nx][ny]

                            """
                            De voorwaarde if neighbor zorgt ervoor dat je alleen
                            verdergaat als er daadwerkelijk een aminozuur
                            (niet None) in de buurcel aanwezig is. De andere
                            if statements spreken voor zich.
                            """
                            if neighbor and self.grid[i][j].type == 'H' and neighbor.type == 'H':

                                # elke H-H binding verlaagt de score
                                score -= 1

        return score

class Protein:
    def __init__(self, sequence):
        # string van aminozuren
        self.sequence = sequence

        # populate list of amino acids
        self.amino_acids = [AminoAcid(x, None, None) for x in self.sequence]

        self.fold_protein()

    def fold_protein(self):
        # start in het midden
        pass

    def evaluate_stability(self):
        pass

    def update_2d_coordinates(aminoacid, coordinate):
        """
        Updates the coordinates of individual aminoacid objects.
        Aminoacid objects contain the Type and their location.

        Parameters:
        - aminoacids (list): list with aminoacid instances
        """
        x, y = coordinate

        for aminoacid in self.amino_acids:
            aminoacid.x = x
            aminoacid.y = y
            y += 1

        # startposition for the first aminoacid (for now)
        x, y = 0, 0
        fold = 2

        # update the coordinates of an aminoacid based on the fold (only in x or y for now, straight line)
        for aminoacid in self.amino_acids:
            if fold == 1:
                x += 1
            elif fold == -1:
                x -= 1
            elif fold == 2:
                y += 1
            elif fold == -2:
                y -= 1
            # Hier kun je later ook de Z-richting toevoegen als je dat wilt

            # Update de coördinaten van het aminozuur
            aminoacid.x = x
            aminoacid.y = y
