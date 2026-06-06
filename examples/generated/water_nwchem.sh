#!/bin/bash
#SBATCH --job-name=water
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=24:00:00
#SBATCH --partition=batch
#SBATCH --output=logs/water_%j.out
#SBATCH --error=logs/water_%j.err

module purge
module load NWChem/7.3.0

export NWCHEM_BASIS_LIBRARY=$NWCHEM_BASIS_LIBRARY
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

mkdir -p logs

echo "Job started: $(date)"
echo "Node: $SLURMD_NODENAME"
echo "CPUs: $SLURM_CPUS_PER_TASK"

nwchem water.nw > water.log

echo "Job finished: $(date)"