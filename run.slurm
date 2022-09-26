#!/bin/bash
#SBATCH --partition=normal               # the DGX only belongs in the 'gpu'  partition
##SBATCH --qos=gpu                           # need to select 'gpu' QoS
#SBATCH --job-name=python-gpu
#SBATCH --output=tr_output/test.out
#SBATCH --error=tr_output/test.err
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1                 # up to 128; 
##SBATCH --gres=gpu:A100.40gb:1              # up to 8; only request what you need
#SBATCH --mem-per-cpu=50500M                 # memory per CORE; total memory is 1 TB (1,000,000 MB)
#SBATCH --export=ALL 
#SBATCH --time=3-01:00:00                   # set to 1hr; please choose carefully




./install.sh --DOWNLOAD 'MULTILING'



##------------------plot

# model=${1:-"PLOT_GPT2"}

# echo ${model}

# ./install.sh --DOWNLOAD ${model}
# sbatch -o tr_output/bloom.out -e tr_output/bloom.err run.slurm PLOT_BLOOM
# sbatch -o tr_output/gpt2.out -e tr_output/gpt2.err run.slurm PLOT_GPT2
# sbatch -o tr_output/mgpt.out -e tr_output/mgpt.err run.slurm PLOT_MGPT

# ./install.sh --DOWNLOAD "MULTILING"
