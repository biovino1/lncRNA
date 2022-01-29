"""=====================================================================================================================
This program reads a GTF file and creates a multilayered data structure. Every exon in each transcript is stored as a
dictionary ID with it's chromosome number, beginning, and end positions store as a list for the value. The script then
reads the human genome file one chromosome at a time. The dictionary from the GTF file is used to check the genome file
for each exon's fasta sequence.

Ben Iovino  1/28/2022   BIOL494, lncRNA Sequence and Folding
====================================================================================================================="""

from pprint import pprint
import os

def get_dict(file):
    """=================================================================================================================
    This function accepts a GTF file as a parameter and returns a sorted dictionary containing each exon as a dictionary
    id and list as its value. The list contains the chromosome number, beginning, and end positions on the chromosome.
    ================================================================================================================="""

    # Initialize a dictionary for transcript ID's, used as an exon counter
    genedict = dict()

    # Initialize a dictionary for exons
    exondict = dict()

    # Open the GTF file
    with open(file, 'r') as file:

        # Use a for loop to read each line in the file
        for line in file:

            # Store line in a variable
            line = ("{}".format(line.strip("\n")))

            # Split line by each tab and create a list of each component
            line = line.split("\t")

            # Split gene ID  by the semicolon
            # This creates a second list inside of the first one
            line[8] = line[8].split(";")

            # Use an if statement to determine if transcript has been added as a key
            if line[8][1] not in genedict:

                # If transcript is not a key, add transcript as a dictionary key
                # Set it's value to 1, meaning this is the first exon with this transcript ID
                genedict.update({line[8][1]: 1})

                # Store exon name as a string for the exondict
                # 'id [transcript id]_exon[#]
                exon = str('id ' + line[8][1].split(' ')[2] + '_' + line[2] + str(genedict[line[8][1]]))

                # Add exon to exon dictionary along with chromosome, beginning, and end positions in the value list
                exondict.update({exon: list((line[0], line[3], line[4]))})

            # If gene is already a key, then update exon dictionary
            else:

                # Access transcript ID and add one to the value
                genedict[line[8][1]] += 1

                # Store exon name as a string for the exondict
                exon = str('id ' + line[8][1].split(' ')[2] + '_' + line[2] + str(genedict[line[8][1]]))

                # Add exon to exondict
                exondict.update({exon: list((line[0], line[3], line[4]))})

    # Initialize sorted exon dictionary
    exondict_sorted = dict()

    # Sort the exons by chromosome number and beginning position
    for id in sorted(exondict, key=lambda x: exondict[x][0]):

        # Add each exon to dictionary of sorted exons
        exondict_sorted[id] = exondict[id]

    return exondict_sorted

def process_chromosome(chromosome_id, chromosome, exondict_sorted):
    """=================================================================================================================
    This accepts a chromosome id, entire chromosome sequence, and the sorted dictionary from get_dict(). It returns a
    dictionary of the exon ID from the sorted dictionary and its fasta sequence from the genome.
    ================================================================================================================="""

    # Split chromosome ID by spaces
    chromosome_id = chromosome_id.split(' ')

    # Initialize dictionary with exon ID as dict ID and fasta sequence as value
    fastadict = dict()

    # Join the chromosome list as a string
    s = ''
    chromosome = s.join(chromosome)

    # Check which exons share the same chromosome
    for item in exondict_sorted.items():

        # Check chromosome of exon vs chromosome from genome
        if item[1][0] == chromosome_id[0][1:]:

            # Determine which part of chromosome belongs to exon's sequence
            sequence = chromosome[int(item[1][1]):int(item[1][2])+1]

            # Update the dictionary with the exon ID and a list for its value
            fastadict.update({item[0]: list()})

            # Append the length of the fasta sequence to the exon ID value
            fastadict[item[0]].append(len(sequence))

            # Append the fasta sequence to the exon ID value
            fastadict[item[0]].append(sequence)

    return fastadict

def get_fasta(genome, exondict_sorted):
    """=================================================================================================================
    This function accepts a genome file and the sorted dictionary from get_dict(). It opens the genome file and moves
    sequentially from each chromosome. The chromosome id is stored along with its entire sequence. The sorted dictionary
    of exons is then read and process_chromosome() is used to read the sequence of the chromosome and extract the exon
    sequence, which is stored in a new dictionary.
    ================================================================================================================="""

    # Initialize a dictionary with exon ID as keys and a list as their value
    fastadict = dict()

    # Open genome file
    with open(genome, 'r') as file:

        # Initialize condition for finding a new chromosome in the genome file
        new_chromosome = False

        # Initialize a list for the fasta sequence of a chromosome
        chromosome = list()

        # Use a for loop to read through each line in genome file
        for line in file:

            # Use an if statement to determine if we have not read a new chromosome and line starts with '>'
            if new_chromosome is False and line.startswith('>'):

                # We are now in a new chromosome, update condition to True
                new_chromosome = True

                # Initialize chromosome number and add 'chr' to match gtf dictionary
                chromosome_id = line[:1] + 'chr' + line[1:]

            # Use an if statement to determine if we are in a new chromosome and line starts with '>'
            elif new_chromosome is True and line.startswith('>'):

                # Use process_chromosome to obtain fasta sequence for the exon
                # Also update the dictionary with this key:value pair
                fastadict.update(process_chromosome(chromosome_id, chromosome, exondict_sorted))

                # Reset the chromosome fasta sequence
                chromosome = list()

                # Update the chromosome number
                chromosome_id = line[:1] + 'chr' + line[1:]

            # Use an if statement to determine if we are in a new chromosome and want to add to fasta sequence
            elif new_chromosome is True:

                # Update the chromosome fasta sequence
                chromosome.append(line.rstrip())

    # Initialize another dictionary of fasta sequences
    transcriptdict = dict()

    # Read through each exon in the fastadict
    for item in fastadict.items():

        # Set the transcript ID as a variable. This makes referring to the transcript ID easier
        keyid = item[0].split('_')[0]

        # Check if the transcript ID is in the dictionary yet
        if keyid not in transcriptdict:

            # If not, add the first exon's length and fasta sequence to the value list
            transcriptdict.update({keyid: list((int(item[1][0]), str(item[1][1])))})

        # If the transcript ID is already a dictionary key, add the next exon
        else:

            # Add the length of the new exon to the previous one(s)
            transcriptdict[keyid][0] += int(item[1][0])

            # Add the fasta sequence of the new exon to the previous one(s)
            transcriptdict[keyid][1] += str(item[1][1])

    return transcriptdict

def measure_dicts(transcriptdict):
    """=================================================================================================================
    This function accepts a dictionary of fasta sequences, measures the length of the sequences, and adds them to a
    dictionary corresponding to their length. The amount of dictionaries is intialized at the very beginning, and the
    lengths are inherent in the loops that create them i.e. dictcount = 5; 'fastadict' + str(500 * i) = fastadict in
    increments of 500 for 5 dictionaries. fastadictlarge catches all sequences above the maximum specified length.
    ================================================================================================================="""

    # Initialize the amount of dictionaries you want to create and a list for the dictionaries
    dictcount = 5
    dictlist = list()

    # Initialize dictionaries and counts
    for i in range(1, dictcount+1):
        globals()['fastadict' + str(500 * i)] = dict()
        globals()['count'+str(500 * i)] = 0
    fastadictlarge = dict()
    countlarge = 0

    # Use a for loop to iterate over each item in the dictionary
    for item in transcriptdict.items():

        # Use a for loop to break each fasta sequence into a list of strings
        # where each string is 100 characters in length
        n = 100
        fasta = list()
        for i in range(0, len(item[1][1]), n):
            fasta.append(item[1][1][i:i+n])
        item[1][1] = fasta

        # Use a for loop to add the fasta sequence to the corresponding dictionary and update the count
        for i in range(1, dictcount+1):
            if ((i-1)*500) < item[1][0] <= (i*500):
                globals()['count'+str(i*500)] += 1
                globals()['fastadict'+str(i*500)].update({item[0]: item[1]})

        # Add sequences above the desired length to fastadictlarge
        if (500*dictcount) < item[1][0]:
            countlarge += 1
            fastadictlarge.update({item[0]: item[1]})

    # Append each dictionary of fasta dictionaries to a list
    for i in range(1, dictcount+1):
        dictlist.append(globals()['fastadict' + str(500 * i)])
    dictlist.append(fastadictlarge)

    # Print counts to check amount of fasta sequences there are in each file
    for i in range(1, dictcount+1):
        print(globals()['count'+str(i*500)])
    print(countlarge)

    return dictlist

def main():
    """=================================================================================================================
    The main function is used to ask for a GTF and genome file, calls each function to create dictionaries with fasta
    sequences of bounded lengths, creates a directory for files, and then pretty prints these dictionaries to
    corresponding files in the new directory.
    ================================================================================================================="""

    # Prompt the user for GTF and genome file names
    file = input("Enter GTF file name: ")
    print()

    file1 = input("Enter genome file name: ")
    print()

    # Call the get_dict function providing the GTF file name as a parameter
    exondict_sorted = get_dict(file)

    # Call the get_fasta function providing the genome file name and sorted dict as parameters
    transcriptdict = get_fasta(file1, exondict_sorted)

    # Call the measure_dicts function providing the fasta dictionary as a parameter
    dictlist = measure_dicts(transcriptdict)

    # Define folder path and make directory for fastadict files
    path = "C:/Users/biovi/PycharmProjects/BIOL494/RawData"
    os.mkdir(path)

    # Use a for loop to open and write files dependent on length of dictlist
    # Each dictionary is written into a separate file
    for i in range(1, len(dictlist)):

        with open(path+"/lncRNA_fasta_"+str(i*500)+".txt", "w") as globals()['file'+str(i*500)]:

            # Pretty print the dictionary into output file
            pprint(globals()['fastadict'+str(i*500)], stream=globals()['file'+str(i*500)], sort_dicts=False)

    # Write fastadictlarge into a separate file
    with open(path+"/lncRNA_fasta_large.txt", "w") as filelarge:
        pprint(dictlist[len(dictlist)-1], stream=filelarge, sort_dicts=False)

main()