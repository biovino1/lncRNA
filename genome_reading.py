"""=====================================================================================================================
This program reads a GTF file and creates a multilayered data structure. Every exon in each transcript is stored as a
dictionary ID with it's chromosome number, beginning, and end positions store as a list for the value. The script then
reads the human genome file one chromosome at a time. The dictionary from the GTF file is used to check the genome file
for each exon's fasta sequence.

Ben Iovino  1/28/2022   BIOL494, lncRNA Sequence and Folding
====================================================================================================================="""

import os


def get_dict(file):
    """=================================================================================================================
    This function accepts a GTF file as a parameter and returns a sorted dictionary containing each exon as a dictionary
    id and list as its value. The list contains the chromosome number, beginning, and end positions on the chromosome.
    ================================================================================================================="""

    # Initialize a dictionary for transcript ID's, used as an exon counter
    transcript_dict = dict()

    # Initialize a dictionary for exons
    exondict = dict()

    # Read gtf file and split each line
    with open(file, 'r') as file:
        for line in file:
            line = ("{}".format(line.strip("\n")))
            line = line.split("\t")

            # Split gene ID  by the semicolon
            # This creates a second list inside of the first one
            line[8] = line[8].split(";")

            # Determine if transcipt is a dict key
            if line[8][1] not in transcript_dict:

                # If transcript is not a key, add transcript as a dictionary key
                # Set it's value to 1, meaning this is the first exon with this transcript ID
                transcript_dict.update({line[8][1]: 1})

                # Store exon name as a string for the exondict
                # 'id [transcript id]_exon[#]
                exon = str('id ' + line[8][1].split(' ')[2] + '_' + line[2] + str(transcript_dict[line[8][1]]))

                # Add exon to exon dictionary along with chromosome, beginning, and end positions in the value list
                exondict.update({exon: list((line[0], line[3], line[4]))})

            # Update transcript dict with new exon
            else:

                # Access transcript ID and add one to the value
                transcript_dict[line[8][1]] += 1

                # Store exon name as a string for the exondict
                exon = str('id ' + line[8][1].split(' ')[2] + '_' + line[2] + str(transcript_dict[line[8][1]]))
                exondict.update({exon: list((line[0], line[3], line[4]))})

    # # Sort the exons by chromosome number and beginning position
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
            sequence = chromosome[int(item[1][1]):int(item[1][2])]

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
    sequence, which is stored in a new dictionary. The exon sequences belonging to the same transcript ID are then
    combined and their lengths are added together.
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

            # If entering new chromosome, obtain fasta sequences for all exons in chrom with process_chromosome
            elif new_chromosome is True and line.startswith('>'):

                # Also update the dictionary with this key:value pair
                fastadict.update(process_chromosome(chromosome_id, chromosome, exondict_sorted))

                # Reset the chromosome fasta sequence and update chrom id
                chromosome = list()
                chromosome_id = line[:1] + 'chr' + line[1:]

            # If remaining in chromosome, add to chrom fasta sequence
            elif new_chromosome is True:
                chromosome.append(line.rstrip())

    # Initialize another dictionary of fasta sequences
    transcriptdict = dict()

    # Read through each exon in the fastadict
    for item in fastadict.items():

        # item is ('id TTTY11:3_exon1', [94, 'TTTTTTTATG...'])

        # Set the transcript ID as a variable. This makes referring to the transcript ID easier
        keyid = item[0].split('_')[0]

        # key id is ('id TTY11:3')

        # Add first exon's length and fasta sequence to the value list if new transcript
        if keyid not in transcriptdict:
            transcriptdict.update({keyid: list((int(item[1][0]), str(item[1][1])))})

        # Add the length of the new exon to transcript
        if keyid in transcriptdict:
            transcriptdict[keyid][0] += int(item[1][0])

            # Add the fasta sequence of the new exon to transcript
            transcriptdict[keyid][1] += str(item[1][1])

    return transcriptdict


def write_fasta(transcriptdict, path):
    """=================================================================================================================
    This function accepts a dictionary with transcripts of varying lengths. The length of each transcript is measured
    and written out to its respective directory as a fasta file.

    :param transcriptdict: transcript id is key, value is a list with length and fasta sequence
    :param path: full directory path for files
    ================================================================================================================="""

    # Place fasta file in respective directory
    # Change end of range to change number of directories
    for item in transcriptdict.items():
        fasta_length = item[1][0]
        sequence_id = item[0].replace('id ', '>')
        fasta = item[1][1]
        for i in range(0, 8):
            if (0 + 500 * i) < fasta_length < (501 + 500 * i):

                # Make a directory for these sequences if it does not exist
                if not os.path.exists(f'{path}/lncRNA{500 + 500 * i}'):
                    os.mkdir(f'{path}/lncRNA{500 + 500 * i}')

                # Open fasta file in respective directory with respective name
                with open(f'{path}/lncRNA{500 + 500 * i}/'
                        f'{sequence_id[1:].replace(":", "-")}.fa', 'w') as fastafile:

                    # Write sequence ID and sequence into file
                    fastafile.write(sequence_id + ' ' + str(fasta_length) + '\n')
                    fastafile.write(str(fasta))


def main():
    """=================================================================================================================
    The main function is used to ask for a GTF and genome file, calls each function to create dictionaries with fasta
    sequences of bounded lengths, creates a directory for files, and then pretty prints these dictionaries to
    corresponding files in the new directory.
    ================================================================================================================="""

    # Initialize files and directories
    gtffile = 'lncipedia_5_2_hc_hg19.gtf'
    genomefile = 'Homo_sapiens.GRCh37.dna.alt.fa'

    if not os.path.exists("C:/Users/biovi/PycharmProjects/BIOL494/Data"):
        os.mkdir("C:/Users/biovi/PycharmProjects/BIOL494/Data")
    path = "C:/Users/biovi/PycharmProjects/BIOL494/Data/"

    # Call the each function providing previous outputs as parameters
    exondict_sorted = get_dict(gtffile)
    print('Exons have been gathered.')
    print()

    transcriptdict = get_fasta(genomefile, exondict_sorted)
    print('Fasta sequences have been gathered.')
    print()

    write_fasta(transcriptdict, path)
    print('Fasta files have been created.')


main()
