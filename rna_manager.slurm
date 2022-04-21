#!/bin/bash
#SBATCH --job-name fasta2xios
#SBATCH --output=%x_%j.out
#SBATCH --error=%x_%j.err
#SBATCH --account long
#SBATCH --nodes=1
#SBATCH --ntasks=20
#SBATCH --time=24:00:00

################################################################################
#
#     d = deltaG (both arguments for xios_from_rnastructure.py)
#     base = sys.argv[1]  # base = directory of fasta files
#     pythonexe = sys.argv[2]  # pythonexe = directory of python executables
#     rnaexe = sys.argv[3]  # rnaexe = directory of RNAstructure executables
#     jobs = int(sys.argv[4])  # jobs = number of concurrent jobs to work on
#     w = int(sys.argv[5])  # w = window param for RNAstructure
#     d = int(sys.argv[6])  # d = delta delta G param for RNAstructure
#
# usage
################################################################################
cd $SLURM_SUBMIT_DIR
python3 /scratch/scholar/biovino/BIOL494/rna_manager.py \
/scratch/scholar/biovino/RNAdata/ \
/scratch/scholar/mgribsko/RNA \
/scratch/scholar/mgribsko/RNAstructure \
20 \
4 \
5
