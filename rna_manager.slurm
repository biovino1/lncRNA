#!/bin/bash
#SBATCH --job-name fasta2xios
#SBATCH --output=%x_%j.out
#SBATCH --error=%x_%j.err
#SBATCH --account standby
#SBATCH --nodes=1
#SBATCH --ntasks=20
#SBATCH --time=4:00:00 

################################################################################
#
# base = directory of fasta files, jobs = number of concurrent jobs to work on
# pythonexe = directory of python files, rnaexe = directory of RNAstructure files
# w = window, d = deltaG (both arguments for xios_from_rnastructure.py)
#     base = sys.argv[1]
#     pythonexe = sys.argv[2]
#     rnaexe = sys.argv[3]
#     jobs = int(sys.argv[4])
#     w = int(sys.argv[5])
#     d = int(sys.argv[6])
# 
# usage
################################################################################
cd $SLURM_SUBMIT_DIR
python3 ../rna_manager.py \
./ \
../../RNA \
../../RNAstructure \
20 \
4 \
5
