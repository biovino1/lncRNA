#
# Ben Iovino
# BIOL494, 1/21/22
# Job
# This program looks through every fasta file in a directory and uses it
# as an input for a program in the RNAstructure package.
#


# Import libraries
import os
import subprocess

# Define a function that goes through a directory and makes a list of each
# file in the directory.
def get_file_list(directory):

    # Initialize a list of file names
    filelist = list()

    # Read each file name in the directory path
    for file in os.listdir(directory):

        # Append file name to list
        filelist.append(directory+"/"+file)

    # Return list of file names
    return filelist

# Define a function that performs a job on each file in the filelist
def do_job(filelist, directory):

    # Use a for loop to iterate through each file in filelist
    for file in filelist:

        # Use subprocess to run Unix command
        subprocess.Popen(['python /scratch/scholar/biovino/xios_from_rnastructure.py', '-i {}'.format(directory),
                          '-f {}'.format(file), '-w 4', '-d 5', '&>>{}.xios'.format(file)])

# Define the main function to ask for a directory path and run the job function
def main():

    # Enter directory path
    directory = "/scratch/scholar/biovino/RNAdata/Test"

    # Call the get_file_list function providing the directory path as a parameter
    filelist = get_file_list(directory)

    # Call do_job function
    do_job(filelist, directory)

# End the main function
main()