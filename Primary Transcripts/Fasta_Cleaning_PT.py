#
# Ben Iovino
# BIOL494
# Fasta Cleaning
# This scripts takes a pretty printed data structure and
# converts it into fasta file format.
#

# Define a function that accepts a text file and reads
# each line into a new text file. It also accepts a string
# of the original file name as to name the new file.
def make_fasta(file, filestring):

    # Open text file
    with open(file, 'r') as file:

        with open(filestring+'_clean', 'w') as f:

            for line in file:

                line = line.lstrip()
                line = line.replace('[', '')
                line = line.replace("'", '')
                line = line.replace('{', '')
                line = line.replace(':', '')
                line = line.replace(' ', '')
                line = line.replace(',', '')
                line = line.replace(']', '')

                if str(line)[0:2] == 'ge':

                    line = '>' + str(line)
                    line = str(line)[0:8] + ' ' + str(line)[8:]

                f.write(str(line))

# Use main function to call for data structure file
def main():

    # Prompt the user for file
    file = input("Enter file name: ")
    print()

    filestring = str(file).strip('.txt')

    make_fasta(file, filestring)

# End the main funciton
main()

