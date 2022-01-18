#
# Ben Iovino
# BIOL494, 1/17/22
# Genome Reading
# This program reads a GTF file and creates a multilayered data structure.
# Every exon in each transcript is stored as a dictionary ID with it's chromosome,
# beginning, and end positions stored as a list for the value. The script then
# reads the human genome file one chromosome at a time. The dictionary from the
# GTF file is used to check the genome file for each transcript's FASTA sequence.
# Exons with the same transcript ID have their FASTA sequence combined, and these
# combined sequences are printed out into files according to their length.
#

from pprint import pprint
import os

# Define a function that accepts a GTF file and returns a sorted dictionary
def get_dict(file):

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

    # Return the sorted data structure
    return exondict_sorted

# Define a function that accepts a chromosome_id, chromosome sequence, and
# the sorted dictionary. This function returns a dictionary of the transcript ID
# from the sorted dictionary and fasta sequence from the genome
def process_chromosome(chromosome_id, chromosome, exondict_sorted):

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

    # Return the dictionary of sequences
    return fastadict

# Define a function that accepts the genome file and sorted dictionary
def get_fasta(genome, exondict_sorted):

    # Initialize a dictionary with gene ID as keys and a list as their value
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

    # Return dictionary of fasta sequences
    return transcriptdict

# Define a function that accepts the dictionary of fasta sequences, measures length of seqs,
# and adds them to a corresponding dictionary
def measure_dicts(transcriptdict):

    # Initialize dictionaries
    fastadict500 = dict()
    fastadict1000 = dict()
    fastadict1500 = dict()
    fastadict2000 = dict()
    fastadict2500 = dict()
    fastadictlarge = dict()

    count500 = 0
    count1000 = 0
    count1500 = 0
    count2000 = 0
    count2500 = 0
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

        # Determine length of fasta sequence and update the corresponding dictionary
        if 0 < item[1][0] <= 500:
            count500 += 1
            fastadict500.update({item[0]: item[1]})

        if 500 < item[1][0] <= 1000:
            count1000 += 1
            fastadict1000.update({item[0]: item[1]})

        if 1000 < item[1][0] <= 1500:
            count1500 += 1
            fastadict1500.update({item[0]: item[1]})

        if 1500 < item[1][0] <= 2000:
            count2000 += 1
            fastadict2000.update({item[0]: item[1]})

        if 2000 < item[1][0] <= 2500:
            count2500 += 1
            fastadict2500.update({item[0]: item[1]})

        if 2500 < item[1][0]:
            countlarge +=1
            fastadictlarge.update({item[0]: item[1]})

    print(count500, count1000, count1500, count2000, count2500, countlarge)
    # Return each dictionary
    return fastadict500, fastadict1000, fastadict1500, fastadict2000, fastadict2500, fastadictlarge

# Use main function to store FASTA sequences into a file
def main():

    # Prompt the user for GTFoutput file name
    file = input("Enter GTF file name: ")
    print()

    # Prompt the user for genome file name
    file1 = input("Enter genome file name: ")
    print()

    # Call the get_dict function providing the GTF file name as a parameter
    exondict_sorted = get_dict(file)

    # Call the get_fasta function providing the genome file name and sorted dict as parameters
    transcriptdict = get_fasta(file1, exondict_sorted)

    # Call the measure_dicts function providing the fasta dictionary as a parameter
    fastadict500, fastadict1000, fastadict1500, fastadict2000, fastadict2500, fastadictlarge = measure_dicts(transcriptdict)

    # Define folder path
    path = "C:/Users/biovi/PycharmProjects/BIOL494/RawData"

    # Make directory for fastadict files
    os.mkdir(path)

    # Open and write to file for fasta sequences <= x in length
    with open(path+"/lncRNA_fasta_500.txt", "w") as file500:

        # Pretty print the dictionary into output file
        pprint(fastadict500, stream=file500, sort_dicts=False)

    with open(path+"/lncRNA_fasta_1000.txt", "w") as file1000:

        pprint(fastadict1000, stream=file1000, sort_dicts=False)

    with open(path+"/lncRNA_fasta_1500.txt", "w") as file1500:

        pprint(fastadict1500, stream=file1500, sort_dicts=False)

    with open(path+"/lncRNA_fasta_2000.txt", "w") as file2000:

        pprint(fastadict2000, stream=file2000, sort_dicts=False)

    with open(path+"/lncRNA_fasta_2500.txt", "w") as file2500:

        pprint(fastadict2500, stream=file2500, sort_dicts=False)

    with open(path+"/lncRNA_fasta_large.txt", "w") as filelarge:

        pprint(fastadictlarge, stream=filelarge, sort_dicts=False)

# End main function
main()