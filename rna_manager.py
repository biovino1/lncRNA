"""=====================================================================================================================
This script runs multiple jobs using subprocess.Popen() until all jobs are complete.

Ben Iovino  2/17/2022   BIOL494, lncRNA Sequence and Folding
====================================================================================================================="""

import subprocess
import os
import random
import time


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

def generate_sleep():
    """=================================================================================================================
    This function generates a specified amount of sleep functions with randomized times and writes each command
    into a file.
    ================================================================================================================="""

    # Set directory for sleep files
    path = "C:/Users/biovi/PycharmProjects/BIOL494/TestFiles/SleepFiles"
    os.mkdir(path)

    # Generate sleep functions with randomized times, write each one into a file
    for i in range(0, 1000):
        with open(path+f'/sleep_function_{i}', 'w') as sleep_file:
            sleep_file.write(f'time.sleep({random.random()})')



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

        file = directory+file

        # Use a while loop to run jobs while
        while nrunning < njobs:

            # Initialize process id from Popen
            pid = subprocess.Popen(['python', f'{file}', 'shell=True'])
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
    directory = 'C:/Users/biovi/PycharmProjects/BIOL494/TestFiles/SleepFiles/'

    # Call the get_file_list function providing the directory path as a parameter
    filelist = get_file_list(directory)

    # Call random function to randomize filelist
    random.shuffle(filelist)

    # Call manager() function
    manager(filelist, directory)

main()

