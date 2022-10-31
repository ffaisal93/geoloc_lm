#!/bin/bash
#SBATCH --partition=gpuq                    # the DGX only belongs in the 'gpu'  partition
#SBATCH --qos=gpu                           # need to select 'gpu' QoS
#SBATCH --job-name=python-gpu
##SBATCH --output=python-gpu.%j.out
##SBATCH --error=python-gpu.%j.err
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1                 # up to 128; 
#SBATCH --gres=gpu:A100.40gb:4              # up to 8; only request what you need
#SBATCH --mem-per-cpu=35G                 # memory per CORE; total memory is 1 TB (1,000,000 MB)
#SBATCH --export=ALL 
#SBATCH --time=1-06:00:00                   # set to 1hr; please choose carefully

# set echo
# umask 0027

# to see ID and state of GPUs assigned
nvidia-smi




source env-h/bin/activate



dir=$1
base=$2
model=$3
c_limit=${4:-10}



if ((${c_limit} == -1)); then
	mode='compute'
elif ((${c_limit} == -2)); then
	mode='generate_single'
else
	mode='generate_all'
fi 


./new_scripts/run.sh ${dir} ${base} ${model} ${c_limit} ${mode}










# python3 -m pip install -U pip wheel
# python3 -m pip install -r frozen_requirements.txt

# python temp.py





# sbatch -o tr_output/${dir}.out -e tr_output/${dir}.err inference.slurm test
# sbatch -o tr_output/${dir}.out -e tr_output/${dir}.err inference.slurm testsample
# sbatch -o tr_output/${dir}.out -e tr_output/${dir}.err inference.slurm dev
# sbatch -o tr_output/${dir}.out -e tr_output/${dir}.err inference.slurm devtest

# for dir in ${dirs}/*
# do
# 	if [ "$dir" != "${dirs}/concept_list.csv" ]; then
# 		echo ${dir}
#         base=$(basename $dir /)
# 		# v2=${base: -3}
# 		./new_scripts/run.sh ${dir} ${base} ${model}

# 	fi

# done