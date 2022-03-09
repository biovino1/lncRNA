"""=================================================================================================
Run multiple jobs using subprocess.Popen(). This version will run on windows (tested) and should
run on unix (not tested)

total is the total number of jobs to run.
run is the number to keep running at the same time

3 March 2022    Michael Gribskov
================================================================================================="""
import subprocess as sub
import random
from time import sleep

# logfile for output
log = open('sleep.log', 'wb')

# total number of jobs and number to run simultaneously
total = 14
total_finished = 0
total_started = 0

# number of jobs to run simultaneously
run = 5
running = 0
delay = 2  # time to wait after polling

# start n jobs, each job sleeps a random number of seconds, then terminates
joblist = []
job_id= 0
while total_finished < total:

    while running < run and total_started < total:
        job_id += 1
        sec = random.randrange(15)
        command = ['py', 'sleep.py', f'{sec}']
        print(f'starting job {job_id}: {sec} seconds')
        job = sub.Popen(command, shell=True, stdout=log, stderr=log)
        joblist.append([job_id, job])
        running += 1
        total_started += 1

    # poll all jobs in joblist
    print('\nPolling')
    to_remove = []
    for j in joblist:
        id, job = j

        print(f'\tjob {id} ...', end='')
        result = job.poll()

        if result != None:
            # None indicates job is still running
            print('finished')
            to_remove.append(j)

        else:
            print('still running')

    # remove all finished jobs. Can't do it above because it shortens the joblist
    # and some jobs don't get polled
    for j in to_remove:
        joblist.remove(j)
        running -= 1
        total_finished += 1

    print(f'\nrunning:{running}\tfinished: {total_finished}')
    sleep(delay)

log.close()
