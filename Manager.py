"""=====================================================================================================================
This script runs multiple jobs using subprocess.Popen() until all jobs are complete.

Ben Iovino  1/28/2022   BIOL494, lncRNA Sequence and Folding
====================================================================================================================="""

import subprocess
import random
from time import sleep

def manager():
    """=================================================================================================================
    This function runs jobs
    ================================================================================================================="""

    # Initialize jobs list and number of jobs
    jobs = []
    n = 20

    # Use a for loop to run through each job
    for i in range(n):

        # Have each job sleep a random number of seconds
        sec = random.randrange(30)
        command = 'sleep {}'.format(sec)

        # Print job number and which command is running
        print('job {}: {}'.format(i, commmand))

        # Update commands started
        job = sub.Popen(command, shell=True, stdout=sub.DEVNULL, stderr=sub.DEVNULL)
        jobs.append(job)

    # Initialize how many jobs are done and the delay between polling
    done = 0
    delay = 5

    # Use a while loop to poll until all jobs are completed
    while done < n:
        print('/nPolling')
        for i in range(n):
            if jobs[i] == 'Done':
                continue
            print('job {} ...'.format(i), end='')
            result = jobs[i].poll()

            if result != None:
                print('finished')
                jobs[i] = 'Done'
                done += 1

            else:
                print('still running')

        sleep(delay)