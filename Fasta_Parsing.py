#
# Ben Iovino
# BIOL494, 1/17/22
# Fasta Cleaning
# This scripts takes a fasta file with more than one sequence and
# prints each individual sequence into it's own file.
#

import os
import shutil

# Define a function that accepts a file with many fasta sequences and
# writes them into separate files.
def parse_fasta(file):

    # Define folder path
    path = "C:/Users/biovi/PycharmProjects/BIOL494/"

    # Get length category of the sequence i.e. 500, 1000, etc.
    filenumber = file.split('_')[2]

    # Make a directory for these sequences if it does not exist
    if not os.path.exists(path+"Data/lncRNA{}".format(filenumber)):
        os.mkdir(path+"Data/lncRNA{}".format(filenumber))

    with open(path+"CleanData/"+file, 'r') as file:

        # Initialize condition for finding a new sequence in the fasta file
        new_sequence = False

        # Initialize a list for the fasta sequence of a chromosome
        fasta = list()

        # Use a for loop to read through each line in genome file
        for line in file:

            # Use an if statement to determine if we have not read a new sequence and line starts with '>'
            if new_sequence is False and line.startswith('>'):

                # We are now in a new sequence, update condition to True
                new_sequence = True

                # Initialize sequence ID
                sequence_id = line

            # Use an if statement to determine if we are in a new sequence and line starts with '>'
            elif new_sequence is True and line.startswith('>'):

                # Write fasta sequence to file named after gene ID
                with open('C:/Users/biovi/PycharmProjects/BIOL494/Data/lncRNA{}/'
                          '{}.txt'.format(filenumber, sequence_id.split()[1]), 'w') as fastafile:

                    # Write sequence ID into file
                    fastafile.write(sequence_id)

                    # Join the fasta sequence together
                    fastastring = ''
                    fasta = fastastring.join(fasta)

                    # Write fasta sequence into file
                    fastafile.write(str(fasta))

                # Reset the fasta sequence
                fasta = list()

                # Update the sequence ID
                sequence_id = line

            # Use an if statement to determine if we are in a new sequence and want to add to fasta sequence
            elif new_sequence is True:

                # Update the chromosome fasta sequence
                fasta.append(line)

# Use main function to call for data structure file
def main():

    # Define folder path
    path = "C:/Users/biovi/PycharmProjects/BIOL494"

    # Make directory for parsed files
    os.mkdir(path + "/Data")

    # Open CleanData folder
    for file in os.listdir(path + "/CleanData"):

        # Call the parse_fasta function
        parse_fasta(file)

# End the main function
main()