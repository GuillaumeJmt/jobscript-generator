#!/bin/bash
#SBATCH --job-name=train
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=12:00:00
#SBATCH --partition=batch
#SBATCH --output=logs/train_%j.out
#SBATCH --error=logs/train_%j.err

module purge
module load Python/3.11

mkdir -p logs

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export MKL_NUM_THREADS=$SLURM_CPUS_PER_TASK

source $HOME/envs/ml/bin/activate

echo "Job started: $(date)"
echo "Python: $(python3 --version)"

python3 train.py

echo "Job finished: $(date)"