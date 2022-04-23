"""=====================================================================================================================
This script runs several scripts at once and creates/deletes the desired directories.

Ben Iovino  1/28/2022   BIOL494, lncRNA Sequence and Folding
====================================================================================================================="""

import subprocess as sub
import shutil

def main():
    """=================================================================================================================
    The main function calls the desired scripts and creates/deletes scripts.
    ================================================================================================================="""

    # Define folder path
    path = "C:/Users/biovi/PycharmProjects/BIOL494"

    print('Running Genome_Reading.py\n')
    sub.run(['python', 'Genome_Reading.py'])

    print('Running Fasta_Cleaning.py\n')
    sub.run(['python', 'Fasta_Cleaning.py'])

    # Delete directory for raw data
    shutil.rmtree(path + "/RawData")

    print('Running Fasta_Parsing.py\n')
    sub.run(['python', 'Fasta_Parsing.py'])

    # Delete directory for clean data
    shutil.rmtree(path + "/CleanData")

main()