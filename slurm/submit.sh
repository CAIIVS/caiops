#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks=3
#SBATCH --cpus-per-task=8
#SBATCH --mem-per-cpu=2G
#SBATCH --time=1400
#SBATCH --job-name=caiops_runner
#SBATCH --partition=gpu
#SBATCH --account=cai_ivs
#SBATCH --output=./slurm_logs/%A-%a-%N-slurm.out
#SBATCH --error=./slurm_logs/%A-%a-%N-slurm.err

# --------------------------------------------------------------------------------------
# env vars
# --------------------------------------------------------------------------------------
source "$(git rev-parse --show-toplevel)/.envrc"

# --------------------------------------------------------------------------------------
# modules
# --------------------------------------------------------------------------------------
module load python/3.12
module load uv/0.6.12

# --------------------------------------------------------------------------------------
# run script
# --------------------------------------------------------------------------------------
uv run caiops
