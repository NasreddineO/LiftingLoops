from Classes_Protein_power import AminoAcid, Protein
import argparse

if __name__ == '__main__':

    # parse the input sequence
    parser = argparse.ArgumentParser(description="A script to find the best protein fold")

    parser.add_argument(
    'sequence',
    help="An ordered string of letters, where each different letter stands for an amino acid of the type indicated by that letter"
    )

    parser.add_argument(
    '-threeD',
    action= 'store_true',
    help="A flag that changes the algorithm to work in three-dimensional space rather than two-dimensional space."
    )

    # convert to variables for legibility
    args = parser.parse_args()
    sequence = args.sequence
    three_dimensional = args.threeD

    print(three_dimensional)

    # check for correct input types:
    if not type(sequence) is str:
        raise TypeError("Please enter a string as a sequence")

    if not type(three_dimensional) is bool:
        raise TypeError("Please enter a boolean for adding a 3rd dimension")

    # initialize Protein
    Proteïne = Protein(sequence)
