"""=====================================================================================================================
This scripts takes a pretty printed data structure and converts it into fasta file format.

Ben Iovino  1/28/2022   BIOL494, lncRNA Sequence and Folding
====================================================================================================================="""

import os

def make_fasta(file, filestring):
    """=================================================================================================================
    This function accepts a fasta file and reads each line into a new fasta file. It also accepts a string of the
    original file name as to name the new file.
    ================================================================================================================="""

    # Define folder path
    path = "C:/Users/biovi/PycharmProjects/BIOL494/"

    # Open text file
    with open(path+"RawData/"+file, 'r') as file:

        with open(path+"CleanData/"+filestring+'_clean', 'w') as f:

            # Clean the file
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

def main():
    """=================================================================================================================
    The main function is used to define the folder path and creates a directory for "cleaned" files. It then opens each
    file in the "RawData" folder, grabs their file as a name, then calls the make_fasta() function to create one large
    fasta file with all of the sequences.
    ================================================================================================================="""

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

