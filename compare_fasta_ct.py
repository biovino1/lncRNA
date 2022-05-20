"""=====================================================================================================================
This script reads file names in two directories, compares them, and returns a list of files missing.

Ben Iovino  4/15/22   BIOL494, lncRNA Sequence and Folding
====================================================================================================================="""

import os


def make_dictionary(path):
    """==================================================================================================================
    This function takes a path and returns a dictionary with each file name as a key. Suffix is removed from each name

    :param path: full directory path
    :return dictionary: dict with each file name as key
    =================================================================================================================="""

    path_dict = dict()
    for file in os.listdir(path):
        file_no_suffix = str(file.split('.')[0])
        path_dict.update({file_no_suffix: 1})

    return path_dict


def compare_dictionaries(dict1, dict2):
    """=====================================================================================================================
    This function accepts two dictionaries, compares their keys, and returns a list of missing keys

    :param dict: dict object
    :return missing_keys: list of keys not found in dict
    ====================================================================================================================="""

    missing_keys = list()
    for key in dict1.keys():
        if key not in dict2.keys():
            missing_keys.append(key)

    return missing_keys


def main():
    """=====================================================================================================================
    This function calls make_dictionary() on all initialized paths, compares the differences with compare_dictionaries(),
    and writes the list of differences in a file.
    ====================================================================================================================="""

    path1 = '/scratch/scholar/biovino/RNAdata/lncRNA2500/'
    path2 = '/scratch/scholar/biovino/RNAdata/lncRNA2500/ctfiles/'

    dict1 = make_dictionary(path1)
    dict2 = make_dictionary(path2)

    missing_keys = compare_dictionaries(dict1, dict2)

    print(missing_keys)
    print(len(missing_keys))


if __name__ == '__main__':
    main()
