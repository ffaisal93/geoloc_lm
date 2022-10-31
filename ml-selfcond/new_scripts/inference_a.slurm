#!/bin/sh

## Specify the name for your job, this is the job name by which Slurm will
## refer to your job.  This can be different from the name of your executable
## or the name of your script file.
#SBATCH --job-name consistent_qa_training

#SBATCH --qos normal  # normal,cdsqos,phyqos,csqos,statsqos,hhqos,gaqos,esqos
#SBATCH -p gpuq       # partition (queue): all-LoPri, all-HiPri,
                      #   bigmem-LoPri, bigmem-HiPri, gpuq, CS_q, CDS_q, ...

## Deal with output and errors.  Separate into 2 files (not the default).
## NOTE: %u=sakter6, %x=consistent_qa, %N=nodeID, %j=jobID, %A=arrayMain, %a=arraySub
##SBATCH -o ../tr_output/find_ex.out    # Output file
##SBATCH -e ../tr_output/find_ex.err    # Error file
##SBATCH --mail-type=BEGIN,END,FAIL     # NONE,BEGIN,END,FAIL,REQUEUE,ALL,...
##SBATCH --mail-user=ffaisal@gmu.edu   # Put your GMU email address here

## Specifying an upper limit on needed resources will improve your scheduling
## priority, but if you exceed these values, your job will be terminated.
## Check your "Job Ended" emails for actual resource usage info.
#SBATCH --mem=128G          # Total memory needed for your job (suffixes: K,M,G,T)
#SBATCH --time=1-11:00    # Total time needed for your job: Days-Hours:Minutes

## These options are more useful when running parallel and array jobs
#SBATCH --nodes 1         # Number of nodes (computers) to reserve
#SBATCH --tasks 1         # Number of independent processes per job
#SBATCH --gres=gpu:4      # Reserve 1 GPU
##SBATCH --exclude=NODE040,NODE050,NODE056

## Load the relevant modules needed for the job
##module load tensorflow/gpu/1.8.0-py36
##module load python/3.6.7
#module load python/3.8.4



module load cuda/11.2
source env-a/bin/activate



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