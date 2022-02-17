"""=================================================================================================
The purpose of this program is to take each fasta file in the specified directory and use it as
an input for a program in the RNAstructure package.

Ben Iovino     17 February 2022
================================================================================================="""

import os
import subprocess


def get_file_list(directory):
    """---------------------------------------------------------------------------------------------
    Goes through the input directory and returns a list of each file in the directory.
    ---------------------------------------------------------------------------------------------"""

    # Initialize a list of file names
    filelist = list()

    # Read each file name in the directory path
    for file in os.listdir(directory):

        # Append file name to list
        filelist.append(file)

    # Return list of file names
    return filelist


def do_job(filelist, directory):
    """---------------------------------------------------------------------------------------------
    Performs a job on each file in the directory.
    ---------------------------------------------------------------------------------------------"""

    # Use a for loop to iterate through each file in filelist
    for file in filelist:

        # Construct command list
        command = []
        command += ["python", "C:/Users/biovi/PycharmProjects/RNA/xios_from_rnastructure.py"]
        command += ["-i", f"{directory}"]
        command += ["-f", f"{file}"]
        command += ["-c", f"{directory + './ctfiles'}"]
        command += ["-x", f"{directory + './xiosfiles'}"]
        command += ["-w", "4"]
        command += ["-d", "5"]

        # Call subprocess
        subprocess.call(command, shell=True)


def main():
    """---------------------------------------------------------------------------------------------
    Asks for directory path, runs get_file_list to obtain list of files, and then performs do_job
    to perform desired job on files.
    ---------------------------------------------------------------------------------------------"""

    # Enter directory path
    directory = "/scratch/scholar/biovino/RNAdata/Test/"

    # Call the get_file_list function providing the directory path as a parameter
    filelist = get_file_list(directory)

    # Call do_job function
    do_job(filelist, directory)


main()
