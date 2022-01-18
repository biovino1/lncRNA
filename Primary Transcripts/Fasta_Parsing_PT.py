#
# Ben Iovino
# BIOL494
# Fasta Cleaning
# This scripts takes a fasta file with more than one sequence and
# prints each individual sequence into it's own file.
#

def parse_fasta(file):

    with open(file, 'r') as file:

        # Initialize condition for finding a new sequence in the fasta file
        new_sequence = False

        # Initialize a list for the fasta sequence of a chromosome
        fasta = list()

        # Use a for loop to read through each line in genome file
        for line in file:

            # Use an if statement to determine if we have not read a new sequence and line starts with '>'
            if new_sequence is False and line.startswith('>'):

                # We are now in a new sequence, update condition to True
                new_sequence = True

                # Initialize sequence ID
                sequence_id = line

            # Use an if statement to determine if we are in a new sequence and line starts with '>'
            elif new_sequence is True and line.startswith('>'):

                # Write fasta sequence to file named after gene ID
                with open('C:/Users/biovi/PycharmProjects/BIOL494/Data/lncRNA2000/'
                          '{}.txt'.format(sequence_id.split()[1]), 'w') as fastafile:

                    # Write sequence ID into file
                    fastafile.write(sequence_id)

                    # Join the fasta sequence together
                    fastastring = ''
                    fasta = fastastring.join(fasta)

                    # Write fasta sequence into file
                    fastafile.write(str(fasta))

                # Reset the fasta sequence
                fasta = list()

                # Update the sequence ID
                sequence_id = line

            # Use an if statement to determine if we are in a new sequence and want to add to fasta sequence
            elif new_sequence is True:

                # Update the chromosome fasta sequence
                fasta.append(line)

# Use main function to call for data structure file
def main():

    # Prompt the user for file
    file = input("Enter file name: ")
    print()

    parse_fasta(file)

# End the main function
main()
