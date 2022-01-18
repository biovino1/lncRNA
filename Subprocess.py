#
# Ben Iovino
# BIOL494, 1/17/22
# Subprocess
# This script runs several scripts to create the desired directories/files
#

import subprocess as sub
import shutil

def main():

    # Define folder path
    path = "C:/Users/biovi/PycharmProjects/BIOL494/RawData"

    sub.run(['python', 'Genome_Reading.py'])

    sub.run(['python', 'Fasta_Cleaning.py'])

    # Delete directory for raw data
    shutil.rmtree(path + "/RawData")

    sub.run(['python', 'Fasta_Parsing.py'])

    # Delete directory for clean data
    shutil.rmtree(path + "/CleanData")

main()