from Classes_Protein_power import AminoAcid, Protein
import argparse

if __name__ == '__main__':

    # parse the input sequence
    parser = argparse.ArgumentParser(description="A script to find the best protein fold")

    parser.add_argument(
    'sequence',
    help="An ordered string of capital letters, where each different letter stands for an amino acid of the type indicated by that letter"
    )

    args = parser.parse_args()

    # converteer de geparste argumenten naar variabelen voor leesbaarheid
    sequence = args.sequence

    Proteïne = Protein(sequence)
