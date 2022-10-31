#!/bin/bash
#SBATCH --partition=normal                 # will run on any cpus in the 'normal' partition
#SBATCH --job-name=python-cpu
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1                   # up to 48 per node
#SBATCH --mem-per-cpu=96G  

## Deal with output and errors.  Separate into 2 files (not the default).
## NOTE: %u=userID, %x=jobName, %N=nodeID, %j=jobID, %A=arrayMain, %a=arraySub
##SBATCH -o /scratch/%u/mbert_align_acl.out    # Output file
##SBATCH -e /scratch/%u/mbert_align_acl.err    # Error file
##SBATCH --mail-type=BEGIN,END,FAIL     # NONE,BEGIN,END,FAIL,REQUEUE,ALL,...
##SBATCH --mail-user=ffaisal@gmu.edu   # Put your GMU email address here


##SBATCH --time=1-11:55    # Total time needed for your job: Days-Hours:Minutes
#SBATCH --time=1-10:55    # Total time needed for your job: Days-Hours:Minutes



## Load the relevant modules needed for the job
##module load tensorflow/gpu/1.8.0-py36
#module load python/3.6.4
#source /projects/antonis/fahim/ner_linking/bin/activate
source /scratch/ffaisal/mgenre/mgenre/bin/activate


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




