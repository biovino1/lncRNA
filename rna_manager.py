"""=====================================================================================================================
This script runs multiple jobs using subprocess.Popen() until all jobs are complete.

Ben Iovino  2/17/2022   BIOL494, lncRNA Sequence and Folding
====================================================================================================================="""

import subprocess
import os
import random
from time import sleep


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

    '''
    # Set directory for sleep files
    path = "C:/Users/biovi/PycharmProjects/BIOL494/TestFiles/SleepFiles"
    os.mkdir(path)

    # Generate sleep functions with randomized times, write each one into a file
    for i in range(0, 1000):
        with open(path+f'/sleep_function_{i}', 'w') as sleep_file:
            sleep_file.write(f'time.sleep({random.random()})')
    '''

    sleep_list = list()
    for i in range(0, 100):
        sleep_list.append(f'timeout /t {random.randint(0, 5)}')

    return sleep_list


def manager(filelist, directory, sleep_list):
    """=================================================================================================================
    This function runs jobs using subprocess.Popen() and polls until all jobs are complete.
    ================================================================================================================="""

    # Initialize jobs list and number of jobs
    jobs = []
    njobs = 20
    nrunning = 0
    jobcount = 0
    jobscomplete = []

    while sleep_list:

        while nrunning < njobs:
            print('\nPolling')

            job = sleep_list.pop()
            jobs.append(job)
            print(job)
            process = subprocess.Popen([job], shell=True)
            nrunning += 1
            print(process)

        # Go through each job in job list
        for i in range(njobs):

            # Check if job is done
            if jobs[i] == 'Done':
                jobscomplete.append(jobs[i])

            # If job returns, it is finished
            if jobs[i] != None:
                print('finished')
                jobs[i] = 'Done'
                nrunning -= 1

    '''
    # Use a for loop to iterate over every file in filelist
    for sleepf in sleep_list:

        # file = directory+file

        # Use a while loop to run jobs while
        while nrunning < njobs:

            # Initialize process id from Popen
            pid = subprocess.Popen(sleepf, shell=True)
            print(pid)

            # Add 1 to nrunning and add pid to jobs list
            nrunning += 1
            jobs.append(pid)

            # Check if jobs are finished
            for j in jobs:

                if j == None:
                    nrunning -= 1
                    jobs.remove(pid)
    '''


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

    sleep_list = generate_sleep()
    random.shuffle(sleep_list)

    # Call manager() function
    manager(filelist, directory, sleep_list)

main()

