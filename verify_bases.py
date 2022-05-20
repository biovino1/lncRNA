"""=====================================================================================================================
This script reads files in a directory and writes into a separate file any characters deemed unacceptable.

Ben Iovino  5/4/22   BIOL494, lncRNA Sequence and Folding
====================================================================================================================="""

import os


def read_directories(path, dir_list):
    """=================================================================================================================
    This function accepts a path and list of directories inside path. It reads each file in each directory and writes
    into a file any unacceptable characters.

    :param path: full directory path
    :param dir_list: list of subdirectories
    ================================================================================================================="""

    bases = ['A', 'C', 'T', 'G']
    fa_dict = dict()
    for dir in dir_list:  # for each directory in dir_list
        dir_path = path+dir
        files = os.listdir(dir_path)
        for file in files:  # for each file in subdirectory
            split_file = file.split('.')
            if split_file[1] == 'fa':  # make sure file is fasta file
                file_path = (dir_path+'/'+file)
                with open(file_path, 'r') as fa_file:  # open fasta file
                    for line in fa_file:  # for each line in fasta file
                        line = line.rstrip()
                        if line.startswith('>'):  # skip lines that start with '>'
                            continue
                        for letter in line:  # for each letter in line
                            if letter not in bases:  # check letter against those in bases list
                                if file_path not in fa_dict.keys():  # add file path to dictionary keys
                                    fa_dict.update({file_path: str()})
                                fa_dict[file_path] += letter  # add letter to dictionary using file path as key

    # Write out dictionary keys and values
    with open('bad_bases.txt', 'w') as file:
        for key in fa_dict.keys():
            file.write(key+'\n')
            file.write(fa_dict[key]+'\n')


def main():
    """=================================================================================================================
    This function initializes a path and gets list of subdirectories. read_directories() is called with both params
    ================================================================================================================="""

    # Obtain list of directories in path
    path = 'C:/Users/biovi/PycharmProjects/BIOL494/Data/'
    dir_list = os.listdir(path)

    read_directories(path, dir_list)


if __name__ == '__main__':
    main()
