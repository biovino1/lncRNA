#
# Ben Iovino
# BIOL494, 1/17/22
# Fasta Cleaning
# This scripts takes a pretty printed data structure and
# converts it into fasta file format.
#

import os
import shutil

# Define a function that accepts a text file and reads
# each line into a new text file. It also accepts a string
# of the original file name as to name the new file.
def make_fasta(file, filestring):

    # Define folder path
    path = "C:/Users/biovi/PycharmProjects/BIOL494/"

    # Open text file
    with open(path+"RawData/"+file, 'r') as file:

        with open(path+"CleanData/"+filestring+'_clean', 'w') as f:

            for line in file:

                line = line.lstrip()
                line = line.replace('[', '')
                line = line.replace("'", '')
                line = line.replace('{', '')
                line = line.replace(',', '')
                line = line.replace(']', '')

                if str(line)[0:2] == 'id':
                    line = line.split(':')

                    line = line[0]+'-'+line[1]+line[2]

                if str(line)[0:2] == 'id':

                    line = '>' + str(line)

                f.write(str(line))

            # Add extra '>' at the end so Fasta_Parsing.py reads last sequence
            f.write(str('>'))

# Use main function to call for data structure file
def main():

    # Define folder path
    path = "C:/Users/biovi/PycharmProjects/BIOL494"

    # Make directory for clean files
    os.mkdir(path+"/CleanData")

    # Open RawData folder
    for file in os.listdir(path+"/RawData"):

        # Grab file name
        filestring = str(file).strip('.txt')

        # Call make_fasta function
        make_fasta(file, filestring)

# End the main function
main()

