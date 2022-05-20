"""=================================================================================================
Run multiple jobs using subprocess.Popen().

total is the total number of jobs to run.
run is the number to keep running at the same time

Ben Iovino    19 April 2022
================================================================================================="""

import subprocess as sub
import time
import os
import sys


def current_time():
    """---------------------------------------------------------------------------------------------
    Gets and returns current time.

    :return now: string with no spaces i.e. DayMonthHourMinutesSecondsMonthYear
    ---------------------------------------------------------------------------------------------"""

    t = time.localtime()
    now = time.strftime("%c", t)
    now = now.replace(' ','').replace(':','')

    return now


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
    filelist.sort()

    # Return list of file names
    return filelist


def check_logs(base, filelist):
    """---------------------------------------------------------------------------------------------
    Checks existing log files to check what fasta files have already been processed.

    :param directory: list of files i.e. [fasta1.fa, fasta2.fa, fasta3.fa]
    :return startwith: position on list to start processing i.e. 0, filelist[0]
    ---------------------------------------------------------------------------------------------"""

    path = base + '/Logs/rna_manager/'

    # Open latest file in log directory and make a list of fasta file names
    files = os.listdir(path)
    paths = [os.path.join(path, basename) for basename in files]
    latestfile = max(paths, key=os.path.getctime)
    loglist = list()
    with open(latestfile, 'r') as logfile:
        for line in logfile:
            loglist.append(line.split('\t')[0])

    # Sort loglist so it is sorted like filelist
    # If loglist is empty, return with index of 0
    loglist.sort()
    if len(loglist) == 0:
        startwith = 0
        return startwith

    # If loglist is not empty, return with corresponding index in filelist if lastfasta is in filelist
    lastfasta = loglist[-1]
    if lastfasta in filelist:
        startwith = filelist.index(lastfasta) + 1  # Add one to index so fasta sequence after last is next up
    else:
        startwith = 0
    return startwith


def manager(base, pythonexe, rnaexe, jobs, w, d, filelist, startwith, directory):
    """---------------------------------------------------------------------------------------------
    Accepts a directory and list of files, runs xios_from_rnastructure.py on each file. Runs a
    certain amount of jobs at once, logs xios_from_rnastructure.py output and logs fasta files
    that went through complete job. Polls every x amount of seconds to check which jobs are complete.

    :param base: directory of directories i.e. /scratch/scholar/user/data/
    :param pythonexe: directory with python executable files
    :param rnaexe: directory with RNAstructure executable files
    :param jobs: number of jobs to run at once
    :param w: window for RNAstructure
    :param d: delta delta G for RNAstructure
    :param filelist: list of files i.e. [fasta1.fa, fasta2.fa, fasta3.fa]
    :param startwith: index of filelist to start running
    :param directory: directory of fasta files i.e. /scratch/scholar/user/data/avocado
    ---------------------------------------------------------------------------------------------"""

    print(f'manager:directory={directory}')

    # logfile for output
    now = current_time()
    xios_log = open(f'{base}/Logs/xios_from_rnastructure/xios{now}.log', 'wb')
    manager_log = open(f'{base}/Logs/rna_manager/manager{now}.log', 'w')
    error_log = open(f'{base}/Logs/manager_error/error{now}.log', 'w')

    # total number of jobs
    total = len(filelist)
    total_finished = 0
    total_started = 0

    # number of jobs to run simultaneously
    run = jobs
    running = 0
    delay = 5  # time to wait after polling

    # check if list of fasta files left to run is shorter than total or run
    # if total or run are too big, index errors occur
    listlength = len(filelist[startwith:])
    if listlength < total:
      total = listlength
    if listlength < jobs:
      run = listlength

    # start n jobs, each job sleeps a random number of seconds, then terminates
    joblist = []
    job_id = 0
    while total_finished < total:

        while running < run and total_started < total:
            job_id += 1
            fasta = filelist[startwith + total_started]
            command = f'python {pythonexe}/xios_from_rnastructure.py -i {directory} ' \
                      f'-c {directory}/ctfiles -x {directory}/xiosfiles -f {fasta} -y {pythonexe} -r {rnaexe}'
            print(f'starting job {job_id}: {fasta} ')
            job = sub.Popen(command, shell=True, stdout=xios_log, stderr=xios_log)
            joblist.append([job_id, job, fasta])
            running += 1
            total_started += 1

        # poll all jobs in joblist
        time.sleep(delay)
        print('\nPolling')
        to_remove = []
        for j in joblist:
            id, job, fasta = j

            print(f'\tjob {id} ...', end='')
            result = job.poll()

            if result != None:  # None indicates job is still running
                j.append(result)
                print('finished')
                to_remove.append(j)

            else:
                print('still running')

        # remove all finished jobs. Can't do it above because it shortens the joblist
        # and some jobs don't get polled
        for j in to_remove:

            # check for exit status
            # write fasta file name to file, and other marked attributes
            now = current_time()
            if j[3] == 2:
                error_log.write(f'{j[2]}\t job id: {j[0]}\t exit status: {j[3]}\t time: {now}\n')
                error_log.flush()
            else:
                manager_log.write(f'{j[2]}\t job id: {j[0]}\t time: {now}\n')
                manager_log.flush()

            # remove finished jobs
            joblist.remove(j)
            running -= 1
            total_finished += 1

        print(f'\nrunning:{running}\tfinished: {total_finished}')

    xios_log.close()
    manager_log.close()
    error_log.close()


def main():
    """---------------------------------------------------------------------------------------------
    Initializes directory, gets list of files from get_file_list(), checks if there is a log file and
    reads it to find last fasta file worked on, and sends to manager()
    ---------------------------------------------------------------------------------------------"""

    base = sys.argv[1]  # directory of fasta files
    pythonexe = sys.argv[2]  # directory of python executables
    rnaexe = sys.argv[3]  # directory of RNAstructure executables
    jobs = int(sys.argv[4])  # number of concurrent jobs to work on
    w = int(sys.argv[5])  # window param for xios_from_rnastructure.py
    d = int(sys.argv[6])  # delta delta G param for xios_from_rnastructure.py

    # directory of fasta files, get filelist
    directory = base + '/lncRNA2500'
    print(f'base={base} directory={directory}')
    filelist = get_file_list(directory)

    # create directory for log files if one does not exist
    path = base + '/Logs/'
    if os.path.isdir(path) != True:
        os.mkdir(path)
        os.mkdir(path+'xios_from_rnastructure')
        os.mkdir(path+'rna_manager')
        os.mkdir(path+'manager_error')
        startwith = 0
    else:
        startwith = check_logs(base, filelist)

    # call manager
    manager(base, pythonexe, rnaexe, jobs, w, d, filelist, startwith, directory)

    # python /scratch/scholar/biovino/BIOL494/rna_manager.py /scratch/scholar/biovino/RNAdata /scratch/scholar/mgribsko/RNA /scratch/scholar/mgribsko/RNAstructure 5 4 5


if __name__ == '__main__':
    main()
