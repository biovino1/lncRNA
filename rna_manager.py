"""=================================================================================================
Run multiple jobs using subprocess.Popen().

total is the total number of jobs to run.
run is the number to keep running at the same time

Ben Iovino    11 March 2022
================================================================================================="""

import subprocess as sub
import random
import time
import os


def get_file_list(directory):
    """---------------------------------------------------------------------------------------------
    Goes through the input directory and returns a list of each file in the directory.

    :param directory: full path of desired files i.e. /scratch/scholar/user/data/
    :return filelist: list of files i.e. [fasta1.fa, fasta2.fa, fasta3.fa]
    ---------------------------------------------------------------------------------------------"""

    # Initialize a list of file names
    filelist = list()

    # Read each file name in the directory path
    for file in os.listdir(directory):

        # Append file name to list
        if '.fa' in file:
          filelist.append(file)

    # Return list of file names
    return filelist


def check_logs(filelist):
    """---------------------------------------------------------------------------------------------
    Checks existing log files to check what fasta files have already been processed.

    :param directory: list of files i.e. [fasta1.fa, fasta2.fa, fasta3.fa]
    :return startwith: position on list to start processing i.e. 0, filelist[0]
    ---------------------------------------------------------------------------------------------"""

    path = '/scratch/scholar/biovino/RNAdata/Logs/rna_manager/'

    # Open latest file in directory and get last line in file
    files = os.listdir(path)
    paths = [os.path.join(path, basename) for basename in files]
    latestfile = max(paths, key=os.path.getctime)
    with open(latestfile, 'r') as logfile:
        lastline = logfile.readlines()[-1]
        lastfasta = lastline.split('\n')[0]

    startwith = filelist.index(lastfasta) + 1 # Add 1 to start with index position after
    print(startwith)

    return startwith


def manager(directory, filelist, startwith):
    """---------------------------------------------------------------------------------------------
    Accepts a directory and list of files, runs xios_from_rnastructure.py on each file. Runs a
    certain amount of jobs at once, logs xios_from_rnastructure.py output and logs fasta files
    that went through complete job. Polls every x amount of seconds to check which jobs are complete.

    :param directory: full path of desired files i.e. /scratch/scholar/user/data/
    :param filelist: list of files i.e. [fasta1.fa, fasta2.fa, fasta3.fa]
    ---------------------------------------------------------------------------------------------"""

    # logfile for output
    t = time.localtime()
    now = time.strftime("%c ", t)
    xios_log = open(f'/scratch/scholar/biovino/RNAdata/Logs/xios_from_rnastructure/xios {now}.log', 'wb')
    manager_log = open(f'/scratch/scholar/biovino/RNAdata/Logs/rna_manager/manager {now}.log', 'w')

    # total number of jobs and number to run simultaneously
    total = len(filelist[startwith:])
    total_finished = 0
    total_started = 0

    # number of jobs to run simultaneously
    run = 5
    running = 0
    delay = 2  # time to wait after polling

    # start n jobs, each job sleeps a random number of seconds, then terminates
    joblist = []
    job_id = 0
    while total_finished < total:

        while running < run and total_started < total:
            job_id += 1
            fasta = filelist[startwith + total_started]
            command = f'python /scratch/scholar/biovino/RNA/xios_from_rnastructure.py -i {directory} ' \
                      f'-c {directory}ctfiles -x {directory}xiosfiles -f {fasta}'
            print(f'starting job {job_id}: {fasta} ')
            job = sub.Popen(command, shell=True, stdout=xios_log, stderr=xios_log)
            joblist.append([job_id, job, fasta])
            running += 1
            total_started += 1

        # poll all jobs in joblist
        print('\nPolling')
        to_remove = []
        for j in joblist:
            id, job, fasta = j

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
            manager_log.write(f'{j[2]}\n') # third index has fasta file name
            manager_log.flush()
            joblist.remove(j)
            running -= 1
            total_finished += 1

        print(f'\nrunning:{running}\tfinished: {total_finished}')
        time.sleep(delay)

    xios_log.close()
    manager_log.close()


def main():
    """---------------------------------------------------------------------------------------------
    Initializes directory, gets list of files from get_file_list() and sends to manager()
    ---------------------------------------------------------------------------------------------"""

    # directory of fasta files, get filelist
    directory = '/scratch/scholar/biovino/RNAdata/TestData/'
    filelist = get_file_list(directory)

    # create directory for log files if one does not exist
    path = '/scratch/scholar/biovino/RNAdata/Logs/'
    if os.path.isdir(path) != True:
        os.mkdir(path)
        os.mkdir(path+'xios_from_rnastructure')
        os.mkdir(path+'rna_manager')
        startwith = 0
    else:
        startwith = check_logs(filelist)

    # call manager
    manager(directory, filelist, startwith)


main()
