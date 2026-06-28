#!/bin/bash
#SBATCH --job-name=mol
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH --time=48:00:00
#SBATCH --partition=batch
#SBATCH --output=logs/mol_%j.out
#SBATCH --error=logs/mol_%j.err

module purge
module load Gaussian/16-C.02
# NOTE: the .gjf must contain %nprocshared=16 and a %mem matching --mem,
# otherwise Gaussian runs on a single core with default memory.

mkdir -p logs

SCRATCH=/scratch/$USER/$SLURM_JOB_ID
mkdir -p $SCRATCH
export GAUSS_SCRDIR=$SCRATCH

echo "Job started: $(date)"
echo "Node: $SLURMD_NODENAME"
echo "CPUs: $SLURM_CPUS_PER_TASK"

g16 < mol.gjf > mol.log

rm -rf $SCRATCH
echo "Job finished: $(date)"