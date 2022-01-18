**************************************************************************************************************
# DETERMING LNCRNA STRUCTURE FROM ITS SEQUENCE
**************************************************************************************************************
This project takes known lncRNA exons from a GTF file, locates their positions in the human genome (g37), and 
grabs their fasta sequence. This is all performed by the Genome_Reading.py script. Using Fasta_Cleaning.py, the
data structure resulting from Genome_Reading.py is removed so that the files are now in fasta format. 
Fasta_Parsing.py creates a file for each individual fasta sequence. 

Because the end goal of these lncRNA fasta sequences is to see how they fold, sequences are broken up into five
categories: 50-500 bp, 501-1000 bp, 1001-1500 bp, 1501-2000 bp, and 2001-2500 bp in length. More categories can 
be added if necessary, whether higher or more specific lengths are desired. 

G37_Parsing.py reads the human genome fasta file and pulls out the sequences of the 23 chromosomes. This was
performed so that a local blast database containing only the chromosomes could be used to test the validity
of the fasta sequences for each exon.

Resulting fasta files will be uploaded to a university computer cluster. Using Mathews Lab "RNAstructure" package,
the secondary structure of these RNA fasta sequences are to be determined.

Two verions of the Genome_Reading.py file exist. Genome_Reading_PT.py obtains the primary transcripts (PT) of each
gene, while Genome_Reading obtains the transcripts for each exon. There are also PT verions of Fasta_Cleaning.py and
Fasta_Parsing.py due to the change in how the scripts read the gene ID's versus exon ID's.

The Subprocess.py script runs Genome_Reading.py, Fasta_Cleaning.py, and Fasta_Parsing.py in sequence while creating
deleting directories for each script to work in.

**************************************************************************************************************
# WORKFLOW
**************************************************************************************************************
Homo_sapiens.GRCh37.dna.alt --> G37_Parsing.py --> g37_chroms.fa
lncipedia_5_2_hc_hg19.gtf + Homo_sapiens.GRCh37.dna.alt --> Genome_Reading.py --> lncRNA_fasta_{X}.fa
lncRNA_fasta_{X}.fa --> Fasta_Cleaning.py --> lncRNA_fasta_{X}_clean.fa
lncRNA_fasta_{X}_clean.fa --> Fasta_Parsing.py --> {exon_id}.fa

Subprocess.py was made to run each program sequentially for the desired fasta sequences. It creates directories for
each set of files that spawn from each script. All files except for the individual exon fasta sequences are deleted
by the Subprocess.py script.

Some manual file manipulation occured:
1) The first line of the gtf file used in this project contained "##gtf" and was deleted before running 
Genome_Parsing.py. 

A local blast database was made using g37_chroms.fa on a unix server using the bioinfo module. Several sequences were
blasted using this database to ensure they were taken correctly.





