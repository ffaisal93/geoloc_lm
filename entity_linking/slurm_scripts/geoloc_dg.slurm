#!/bin/sh

## Specify the name for your job, this is the job name by which Slurm will
## refer to your job.  This can be different from the name of your executable
## or the name of your script file.
#SBATCH --job-name mbert_acl

#SBATCH --qos normal  # normal,cdsqos,phyqos,csqos,statsqos,hhqos,gaqos,esqos
##SBATCH -p gpuq       # partition (queue): all-LoPri, all-HiPri,
                      #   bigmem-LoPri, bigmem-HiPri, gpuq, CS_q, CDS_q, ...

#SBATCH -p all-HiPri

## Deal with output and errors.  Separate into 2 files (not the default).
## NOTE: %u=userID, %x=jobName, %N=nodeID, %j=jobID, %A=arrayMain, %a=arraySub
##SBATCH -o /scratch/%u/mbert_align_acl.out    # Output file
##SBATCH -e /scratch/%u/mbert_align_acl.err    # Error file
##SBATCH --mail-type=BEGIN,END,FAIL     # NONE,BEGIN,END,FAIL,REQUEUE,ALL,...
##SBATCH --mail-user=ffaisal@gmu.edu   # Put your GMU email address here

## Specifying an upper limit on needed resources will improve your scheduling
## priority, but if you exceed these values, your job will be terminated.
## Check your "Job Ended" emails for actual resource usage info.
#SBATCH --mem=96G          # Total memory needed for your job (suffixes: K,M,G,T)
##SBATCH --time=1-11:55    # Total time needed for your job: Days-Hours:Minutes
#SBATCH --time=0-11:55    # Total time needed for your job: Days-Hours:Minutes

## These options are more useful when running parallel and array jobs
#SBATCH --nodes 1         # Number of nodes (computers) to reserve
#SBATCH --tasks 1         # Number of independent processes per job
## SBATCH --gres=gpu:1      # Reserve 1 GPU
## SBATCH --exclude=NODE040,NODE050,NODE056

## Load the relevant modules needed for the job
##module load tensorflow/gpu/1.8.0-py36
#module load python/3.6.4
#source /projects/antonis/fahim/ner_linking/bin/activate
source ~/fairseq/bin/activate
module load cuda/10.0

## Setup the environment
##export PYTHONPATH=$HOME/python/models-r1.8.0-packages:$PYTHONPATH
##export PYTHONPATH=<path/to>/models:$PYTHONPATH

## Start the job
##python3 prepare_tydi_data.py \
##  --input_jsonl=data/tydiqa-v1.0-dev.jsonl.gz \
##  --output_tfrecord=/scratch/ffaisal/dev.tfrecord \
##  --vocab_file=mbert_modified_vocab.txt \
##  --is_training=false

##python3 ../tydiqa/baseline/prepare_tydi_data.py \
##  --input_jsonl=../tydiqa/baseline/data/tydiqa-v1.0-train.jsonl.gz \
##  --output_tfrecord=/scratch/ffaisal/train_samples \
##  --vocab_file=../tydiqa/baseline/mbert_modified_vocab.txt \
##  --record_count_file=/scratch/ffaisal/train_samples_record_count.txt \
##  --include_unknowns=0.1 \
##  --is_training=true

file=$1
name=$2
outdir=$3
mode=$4

cd ../GENRE
python geoloc_dg.py --mode ${mode} \
--name ${name} \
--data_file ${file} \
--out_dir ${outdir}




