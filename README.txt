**************************************************************************************************************
# DETERMING LNCRNA STRUCTURE FROM ITS SEQUENCE
**************************************************************************************************************
This project takes lncRNA transcripts from a GTF file, locates their positions in the human genome (g37), and
grabs their fasta sequence. These sequences are then written out in fasta format to directories depending on
their length. This is all performed by the Genome_Reading.py script.

Because the end goal of these lncRNA fasta sequences is to see how they fold, sequences are broken up into categories
of every 500 base pairs i.e. 1-500, 501-1000, etc. Larger sequences take longer to fold.

G37_Parsing.py reads the human genome fasta file and pulls out the sequences of the 23 chromosomes. This was
performed so that a local blast database containing only the chromosomes could be used to test the validity
of the fasta sequences for each transcript.

Resulting fasta files will be uploaded to a university computer cluster. Using Mathews Lab "RNAstructure" package,
the secondary structure of these RNA fasta sequences are to be determined.

lnc_fdb.fa and lnc_hc.fa were downloaded from https://lncipedia.org/download. These two fasta files were parsed with
lnc_parsing.fa to obtain the individual fasta sequences of each lncRNA transcript. compare_fastas.py was used to
compare the fasta sequences gathered from genome_reading.py and lnc_parsing.fa.

verify_bases.py was used to read each letter of all fasta sequences in a directory to ensure they were ATCG. Sequences
that failed to meet this requirement are written out to bad_bases.txt.

rna_manager.py and rna_manager.slurm were used on the university computer cluster to run RNAstructure package jobs.

**************************************************************************************************************
# WORKFLOW
**************************************************************************************************************
Homo_sapiens.GRCh37.dna.alt --> G37_Parsing.py --> g37_chroms.fa
lncipedia_5_2_hc_hg19.gtf + Homo_sapiens.GRCh37.dna.alt --> Genome_Reading.py --> Data
lnc_fdb.fa + lnc_hc.fa --> lnc_parsing --> fdbData, hcData

Some manual file manipulation occured:
1) The first line of the gtf file used in this project contained "##gtf" and was deleted before running 
Genome_Parsing.py. 

A local blast database was made using g37_chroms.fa on a unix server using the bioinfo module. Several sequences were
blasted using this database to ensure they were taken correctly.





