"""=====================================================================================================================
This scripts reads the human G37 file and writes into a file only the chromosomes and corresponding fasta sequences
that you are interested in.

Ben Iovino  1/28/2022   BIOL494, lncRNA Sequence and Folding
====================================================================================================================="""

def write_chromosomes(file):
    """=================================================================================================================
    This function accepts a genome file. A list of chromosomes is initialized and the entire file is read line by line
    until the start of one of these chromosomes is found. The id line and entire fasta sequence of each chromosome
    is read into a new file.
    ================================================================================================================="""

    with open(file, "r") as file:

        # Open file to write into
        with open('g37_chroms_only.txt', 'w') as f:

            # Initialize condition for finding a new chromosome in the genome file
            new_chromosome = False

            # Initialize a list of chromosomes you want to isolate from genome file
            chromosome_list = ('>chr1', '>chr2', '>chr3', '>chr4', '>chr5', '>chr6', '>chr7', '>chr8', '>chr9', '>chr10',
                                '>chr11', '>chr12', '>chr13', '>chr14', '>chr15', '>chr16', '>chr17', '>chr18', '>chr19',
                                '>chr20', '>chr21', '>chr22', '>chr23', '>chrX', '>chrY')

            # Use a for loop to read through each line in genome file
            for line in file:

                # Use an if statement to determine if we have not read a new chromosome and line starts with '>'
                if new_chromosome is False and line.startswith('>'):

                    # We are now in a new chromosome, update condition to True
                    new_chromosome = True

                    # Initialize chromosome number and add 'chr'
                    chromosome_id = line[:1] + 'chr' + line[1:]

                    # Determine if chromosome matches a chromosome from the list
                    if chromosome_id[0:5] in chromosome_list:

                        f.write(chromosome_id)

                # Use an if statement to determine if we are in a new chromosome and line starts with '>'
                elif new_chromosome is True and line.startswith('>'):

                    # Update the chromosome number
                    chromosome_id = line[:1] + 'chr' + line[1:]

                    # Determine if chromosome matches a chromosome from the list
                    if chromosome_id[0:5] in chromosome_list:

                        f.write(chromosome_id)

                # Use an if statement to determine if we are in a new chromosome and matches a chromosome from the list
                elif new_chromosome is True and chromosome_id[0:5] in chromosome_list:

                    # Update the chromosome fasta sequence
                    chromosome = str(line)

                    f.write(chromosome)

    return


def main():
    """=================================================================================================================
    Use the main function to ask for the genome file name and call the write_chromosomes function to write the desired
    chromosomes into a new text file.
    ================================================================================================================="""

    # Prompt the user for a genome file name to process
    file = input("Enter genome file name: ")
    print()

    # Call the write_chromosomes function
    write_chromosomes(file)


if __name__ == '__main__':
    main()
