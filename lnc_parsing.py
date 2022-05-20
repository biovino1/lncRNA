"""=====================================================================================================================
This scripts takes a fasta file with more than one sequence and prints each individual sequence into it's own file.
Each file is placed in a specific directory based on the length of the sequence.

Ben Iovino  5/6/2022   BIOL494, lncRNA Sequence and Folding
====================================================================================================================="""

import os
import shutil


def parse_fasta(file, path):
    """=================================================================================================================
    This function accepts a file with many fasta sequence and writes them into individual files.

    :param file: file of all fasta seqs
    :param path: directory path that new fasta files go into
    ================================================================================================================="""

    with open(file, 'r') as file:

        # Initialize condition for finding a new sequence in the fasta file
        new_sequence = False
        fasta = list()

        # Read each line in fasta file
        for line in file:

            # Use an if statement to determine if we have not read a new sequence and line starts with '>'
            if new_sequence is False and line.startswith('>'):

                # We are now in a new sequence, update condition to True
                new_sequence = True

                # Initialize sequence ID
                sequence_id = line

            # Use an if statement to determine if we are in a new sequence and line starts with '>'
            elif new_sequence is True and line.startswith('>'):

                # Join the fasta sequence together
                fastastring = ''
                fasta = fastastring.join(fasta)
                fasta_length = len(fasta) - fasta.count('\n')

                # Place fasta file in respective directory
                for i in range(0, 8):
                    if (0+500*i) < fasta_length < (501+500*i):

                        # Make a directory for these sequences if it does not exist
                        if not os.path.exists(f'{path}/lncRNA{500+500*i}'):
                            os.mkdir(f'{path}/lncRNA{500+500*i}')

                        # Open fasta file in respective directory with respective name
                        with open(f'{path}/lncRNA{500+500*i}/'
                                  f'{sequence_id[1:].rstrip().replace(":", "-")}.fa', 'w') as fastafile:

                            # Write sequence ID and sequence into file
                            fastafile.write(sequence_id.rstrip()+' '+str(fasta_length)+'\n')
                            fastafile.write(str(fasta.strip()))

                # Reset the fasta sequence and update seq ID
                fasta = list()
                sequence_id = line

            # Use an if statement to determine if we are in a new sequence and want to add to fasta sequence
            elif new_sequence is True:

                # Update the chromosome fasta sequence
                fasta.append(line)


def main():
    """=================================================================================================================
    The main function is used to define the folder path and to make a directory for the individual, parsed fasta files.
    It then calls parse_fasta() to split the large fasta file into individual fasta files.
    ================================================================================================================="""

    # Make directory for parsed files, call parse_fasta()
    os.mkdir("C:/Users/biovi/PycharmProjects/BIOL494/fdbData")
    path = "C:/Users/biovi/PycharmProjects/BIOL494/fdbData/"
    parse_fasta('lnc_fdb.fa', path)


if __name__ == '__main__':
    main()
