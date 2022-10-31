#!/bin/bash
#SBATCH --partition=normal               # the DGX only belongs in the 'gpu'  partition
##SBATCH --qos=gpu                           # need to select 'gpu' QoS
#SBATCH --job-name=python-gpu
##SBATCH --output=tr_output/test.out
##SBATCH --error=tr_output/test.err
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1                 # up to 128; 
##SBATCH --gres=gpu:A100.40gb:1              # up to 8; only request what you need
#SBATCH --mem-per-cpu=50500M                 # memory per CORE; total memory is 1 TB (1,000,000 MB)
#SBATCH --export=ALL 
#SBATCH --time=3-01:00:00                   # set to 1hr; please choose carefully


model=$1
base=$2
dir=$3

echo ${model}
echo ${base}
echo ${dir}


source vnv/geo_vnv/bin/activate

python scripts/plot_similarity.py \
	--expert_dir ${dir} \
    --data_dir data \
    --model ${model} \
    --base ${base}
deactivate

##------------------plot

# model=${1:-"PLOT_GPT2"}