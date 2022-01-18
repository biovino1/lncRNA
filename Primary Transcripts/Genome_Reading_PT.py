#
# Ben Iovino
# BIOL494
# Genome Reading
# This program reads a GTF file and creates a multilayered data structure.
# Each gene in the GTF file is stored as a dict ID with its chromosome,
# beginning, and end positions stored as a list for the value. The script
# then reads the human genome file one chromosome at a time. The dictionary
# from the GTF file is used to check the genome file for each gene's FASTA
# sequence.
#

# Import pretty print
from pprint import pprint

# Define a function that accepts a GTF file and returns a sorted dictionary
def get_dict(file):

    # Initialize a dictionary for every gene ID
    gtf = dict()

    # Open the GTF file
    with open(file, 'r') as file:

        # Use a for loop to read each line
        for line in file:

            # Store line in a variable
            line = ("{}".format(line.strip("\n")))

            # Split line by each tab and create a list of each component
            line = line.split("\t")

            # Split gene ID  by the semicolon
            # This creates a second list inside of the first one
            line[8] = line[8].split(";")

            # Use an if statement to determine if gene has been added as a key
            if line[8][0] not in gtf:

                # Store the exon as a dictionary
                # Exon is dict ID, beginning and end positions stored as list for value
                exon = ({line[2]: [line[3], line[4]]})

                # If gene is not a key, add gene as a dictionary key
                # Add chromosome number, beginning, and end position of exon as values
                gtf.update({line[8][0]: list((line[0], line[3], line[4]))})

            # If gene is already a key, then update exon dictionary
            else:

                # Store exon dict in a variable same as before
                exon = ({line[2]: [line[3], line[4]]})

            # Change gene beginning position if an exon has a lower beginning position value
            if exon[line[2]][0] < gtf[line[8][0]][1]:

                # Replace gene beginning position with lower exon beginning position
                gtf[line[8][0]][1] = exon[line[2]][0]

            # Change gene end position if an exon has a higher end position value
            if exon[line[2]][1] > gtf[line[8][0]][2]:

                # Replace gene end position with higher exon end position
                gtf[line[8][0]][2] = exon[line[2]][1]

    # Initialize sorted dictionary
    gtfsorted = dict()

    # Sort the genes by chromosome number and beginning position
    for id in sorted(gtf, key=lambda x: gtf[x][0]):

        # Add each gene to dictionary of sorted genes
        gtfsorted[id] = gtf[id]

    # Return the sorted data structure
    return gtfsorted

# Define a function that accepts a chromosome_id, chromosome sequence, and
# the sorted dictionary. This function returns a dictionary of the gene ID
# from the sorted dictionary and fasta sequence from the genome
def process_chromosome(chromosome_id, chromosome, gtfsorted):

    # Split chromosome ID by spaces
    chromosome_id = chromosome_id.split(' ')

    # Initialize dictionary with gene ID as dict ID and fasta sequence as value
    fastadict = dict()

    # Join the chromosome list as a string
    s = ''
    chromosome = s.join(chromosome)

    # Check which genes share the same chromosome
    for item in gtfsorted.items():

        # Check chromosome of gene vs chromosome from genome
        if item[1][0] == chromosome_id[0][1:]:

            # Determine which part of chromosome belongs to gene's sequence
            sequence = chromosome[int(item[1][1]):int(item[1][2])+1]

            # Update the dictionary with the gene ID and a list for its value
            fastadict.update({item[0]: list()})

            # Append the length of the fasta sequence to the gene ID value
            fastadict[item[0]].append(len(sequence))

            # Append the fasta sequence to the gene ID value
            fastadict[item[0]].append(sequence)

    return fastadict

# Define a function that accepts the genome file and sorted dictionary
def get_fasta(genome, gtfsorted):

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

                # Use process_chromosome to obtain fasta sequence for the gene
                # Also update the dictionary with this key:value pair
                fastadict.update(process_chromosome(chromosome_id, chromosome, gtfsorted))

                # Reset the chromosome fasta sequence
                chromosome = list()

                # Update the chromosome number
                chromosome_id = line[:1] + 'chr' + line[1:]

            # Use an if statement to determine if we are in a new chromosome and want to add to fasta sequence
            elif new_chromosome is True:

                # Update the chromosome fasta sequence
                chromosome.append(line.rstrip())

    # Return dictionary of fasta sequences
    return fastadict

# Define a function that accepts the dictionary of fasta sequences, measures length of seqs,
# and adds them to a corresponding dictionary
def measure_dicts(fastadict):

    # Initialize dictionaries
    fastadict500 = dict()
    fastadict1000 = dict()
    fastadict1500 = dict()
    fastadict2000 = dict()
    fastadictlarge = dict()

    # Use a for loop to iterate over each item in the dictionary
    for item in fastadict.items():

        # Use a for loop to break each fasta sequence into a list of strings
        # where each string is 100 characters in length
        n = 100
        fasta = list()
        for i in range(0, len(item[1][1]), n):
            fasta.append(item[1][1][i:i+n])
        item[1][1] = fasta

        # Determine length of fasta sequence and update the corresponding dictionary
        if 50 < item[1][0] <= 500:
            # count500 += 1
            fastadict500.update({item[0]: item[1]})

        if 500 < item[1][0] <= 1000:
            # count1000 += 1
            fastadict1000.update({item[0]: item[1]})

        if 1000 < item[1][0] <= 1500:
            # count1500 += 1
            fastadict1500.update({item[0]: item[1]})

        if 1500 < item[1][0] <= 2000:
            # count2000 += 1
            fastadict2000.update({item[0]: item[1]})

        if 2000 < item[1][0]:
            # countlarge += 1
            fastadictlarge.update({item[0]: item[1]})

    # Return each dictionary
    return(fastadict500,fastadict1000,fastadict1500,fastadict2000, fastadictlarge)

# Use main function to store FASTA sequences into a file
def main():

    # Prompt the user for GTFoutput file name
    file = input("Enter GTF file name: ")
    print()

    # Prompt the user for genome file name
    file1 = input("Enter genome file name: ")
    print()

    # Call the get_dict function providing the GTF file name as a parameter
    gtfsorted = get_dict(file)

    # Call the get_fasta function providing the genome file name and sorted dict as parameters
    fastadict = get_fasta(file1, gtfsorted)

    # Call the measure_dicts function providing the fasta dictionary as a parameter
    fastadict500, fastadict1000, fastadict1500, fastadict2000, fastadictlarge = measure_dicts(fastadict)

    # Open and write to file for fasta sequences <= x in length
    with open("lncRNA_fasta_500.txt", "w") as file500:

        # Pretty print the dictionary into output file
        pprint(fastadict500, stream=file500, sort_dicts=False)

    with open("lncRNA_fasta_1000.txt", "w") as file1000:

        pprint(fastadict1000, stream=file1000, sort_dicts=False)

    with open("lncRNA_fasta_1500.txt", "w") as file1500:

        pprint(fastadict1500, stream=file1500, sort_dicts=False)

    with open("lncRNA_fasta_2000.txt", "w") as file2000:

        pprint(fastadict2000, stream=file2000, sort_dicts=False)

    with open("lncRNA_fasta_large.txt", "w") as filelarge:

        pprint(fastadictlarge, stream=filelarge, sort_dicts=False)

# End main function
main()