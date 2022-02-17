"""=====================================================================================================================
This script runs multiple jobs using subprocess.Popen() until all jobs are complete.

Ben Iovino  2/17/2022   BIOL494, lncRNA Sequence and Folding
====================================================================================================================="""

import subprocess
import os


def get_file_list(directory):
    """=================================================================================================================
    This function takes a directory as an argument and returns a list of each file in the path.
    ================================================================================================================="""

    # Initialize a list of file names
    filelist = list()

    # Read each file name in the directory path
    for file in os.listdir(directory):

        # Append file name to list
        filelist.append(file)

    # Return list of file names
    return filelist

def manager(filelist, directory):
    """=================================================================================================================
    This function runs jobs
    ================================================================================================================="""

    # Initialize jobs list and number of jobs
    jobs = []
    njobs = 20
    nrunning = 0

    # Use a for loop to iterate over every file in filelist
    for file in filelist:

        # Use a while loop to run jobs while
        while nrunning < njobs:

            # Initialize process id from Popen
            pid = subprocess.Popen(['python', 'C:/Users/biovi/PycharmProjects/RNA/xios_from_rnastructure.py', 'i',
                                    f'{directory}', "-f", f"{file}"])

            print(pid)

            # Add 1 to nrunning and add pid to jobs list
            nrunning += 1
            jobs.append(pid)

            # Check if jobs are finished
            for j in jobs:

                if j == None:
                    nrunning -= 1
                    jobs.remove(pid)


def main():
    """=================================================================================================================
    The main function accepts a directory path, creates a list of files using get_file_list(), and sends it to
    manager() to run desired jobs.
    ================================================================================================================="""

    # Enter directory path
    directory = 'C:/Users/biovi/PycharmProjects/BIOL494/TestFiles/TestData/'

    # Call the get_file_list function providing the directory path as a parameter
    filelist = get_file_list(directory)

    # Call manager() function
    manager(filelist, directory)

main()

