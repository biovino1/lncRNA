#
# Ben Iovino
# BIOL494, 1/19/22
# Job
# This program looks through every fasta file in a directory and uses it
# as an input for a program in the RNAstructure package.


# Import libraries
import os

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
def do_job(filelist):

    python ../RNA/xios_from_rnastructure.py - i fasta - f g1 *.fa - w 1,5 - d 0,5 &>>param.log

# Define the main function to ask for a directory path and run the job function
def main():

    # Prompt the user for directory path
    directory = input("Enter full directory path: ")
    print()

    # Call the get_file_list function providing the directory path as a parameter
    filelist = get_file_list(directory)

# End the main function
main()