#!/bin/bash
#SBATCH --job-name=water
#SBATCH --ntasks=8
#SBATCH --cpus-per-task=1
#SBATCH --mem=32G
#SBATCH --time=24:00:00
#SBATCH --partition=batch
#SBATCH --output=logs/water_%j.out
#SBATCH --error=logs/water_%j.err

# NWChem parallelism is MPI (Global Arrays / ARMCI), not OpenMP.
# Scale by increasing --ntasks; launch with srun.

module purge
module load NWChem/7.3.0
mkdir -p logs

echo "Job started: $(date)"
echo "Node: $SLURMD_NODENAME"
echo "MPI ranks: $SLURM_NTASKS"

srun nwchem water.nw > water.log

echo "Job finished: $(date)"
