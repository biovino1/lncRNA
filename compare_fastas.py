"""=====================================================================================================================
This script reads file names in two directories, compares files with the same names, and returns any differences in the
fasta sequences.

Ben Iovino  5/19/22   BIOL494, lncRNA Sequence and Folding
====================================================================================================================="""

import os
import hashlib
import collections


def get_directories(path):
    """=================================================================================================================
    This function accepts a directory path and returns a lists of all files in them

    :param path: full directory path
    :return dir_list: list of files
    ================================================================================================================="""

    # Obtain all directories in the path and then get a list of files
    file_list = list()
    dir_list = os.listdir(path)
    for directory in dir_list:
        dir_path = path + directory
        files = os.listdir(dir_path)
        for file in files:  # Add directory to each file name so it can be opened later
            file_list.append(directory+'/'+file)
    return file_list


def compare_files(path1, path2, file_list1, file_list2):
    """=================================================================================================================
    This function accepts lists of files and writes out differences between files with the same name, if any exist.
    Each line of both files is hashed, if hash does not match then the result is noted.

    :param path: directory path used to open files
    :param file_list: list of files
    ================================================================================================================="""

    # Dict for storing which files and how many lines don't match
    mismatches = collections.defaultdict(int)

    # Using bigger file_list to move through smaller one
    for file in file_list1:
        if file in file_list2:
            with open(path1+file, 'r') as file1, open(path2+file, 'r') as file2:

                # Hash both lines at same time and compare
                for line1, line2, in zip(file1, file2):
                    line1_hash = hashlib.sha256(str.encode(line1))
                    line2_hash = hashlib.sha256(str.encode(line2))

                    # If hashes don't match, determine how many characters don't match and update dict
                    if line1_hash.digest() != line2_hash.digest():
                        for x, y in zip(line1, line2):
                            if x != y:
                                mismatches[file] += 1

    # Write mismatches in file
    with open('fasta_mismatches.txt', 'w') as file:
        for key, value in mismatches.items():
            file.write(f'{key}: {value} \n')


def main():
    """=================================================================================================================
    This function initializes two paths and calls read_directories() to get a list of files in both. compare_files() is
    called to get a written output of differences in files with the same name.
    ================================================================================================================="""

    # Obtain list of directories in path
    path1 = 'C:/Users/biovi/PycharmProjects/BIOL494/Data/'
    path2 = 'C:/Users/biovi/PycharmProjects/BIOL494/fdbData/'

    # Call read_directories to get list of files in both directories
    file_list1 = get_directories(path1)
    file_list2 = get_directories(path2)

    # Call compare_files to get written output of differences between files in the file lists
    compare_files(path1, path2, file_list1, file_list2)


if __name__ == '__main__':
    main()
