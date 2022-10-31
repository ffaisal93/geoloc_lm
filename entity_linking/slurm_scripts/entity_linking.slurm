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
##SBATCH -o ../tr_output/link_gpt2.out    # Output file
##SBATCH -e ../tr_output/link_gpt2.err    # Error file
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

# file=$1
# name=$2
# outdir=$3
# mode=$4

cd ../GENRE
# python entity_linking.py --mode ${mode} \
# --name ${name} \
# --data_file ${file} \
# --out_dir ${outdir}







# dirr="../data/geoloc"
# outdir="../data/geoloc"
# mode="concept"
# label='CONSTRUCT_MLING'


# for dir in $dirr/*
# do
#   if [ "$dir" != '${dirr}/**DS_Store**' ] && [ "$dir" != '${dirr}/._**' ]; then
#       dir=${dir}/${mode}/entity
#       for file in $dir/*
#       do
#           if [ "$file" != '${dir}/**DS_Store**' ] && [ "$file" != '${dir}/._**' ]; then
#               echo $file
#               base=$(basename $file .pickle)
#               echo $base
#               echo ../tr_output/${label}_${base}.err
#               echo ${outdir}
#               # sbatch -o ../tr_output/${label}_${base}.out -e ../tr_output/${label}_${base}.err entity_linking.slurm $file $base $outdir $mode
#               python entity_linking.py --mode ${mode} \
#                 --name ${base} \
#                 --data_file ${file} \
#                 --out_dir ${outdir}
#           fi
#       done
#   fi
# done





dirr="../data/geoloc"
outdir="../data/geoloc"
mode=$1
label='CONSTRUCT_MLING'
filep=$2


for dir in $dirr/*
do
  echo dir: ${dir}
  if [ "$dir" != '${dirr}/**DS_Store**' ] && [ "$dir" != '${dirr}/._**' ] && [ "$dir" == "${dirr}/${filep}" ]; then
      dir=${dir}/${mode}/entity
      for file in ${dir}/*
      do
          if [ "$file" != '${dir}/**DS_Store**' ] && [ "$file" != '${dir}/._**' ]; then
              echo file: $file
              base=$(basename $file .pickle)
              echo base: $base
              # echo ../tr_output/${label}_${base}.err
              echo ${mode} ${base} ${file} ${outdir}
              echo ${mode} ${base} ${file} ${outdir} >> jobs.txt
              # sbatch -o ../tr_output/${label}_${base}.out -e ../tr_output/${label}_${base}.err entity_linking.slurm $file $base $outdir $mode
              python entity_linking.py --mode ${mode} \
                --name ${base} \
                --data_file ${file} \
                --out_dir ${outdir}
          fi
      done
  fi
done


# sbatch -e ../tr_output/link_gpt2.err -o ../tr_output/link_gpt2.out entity_linking.slurm gpt2 dataset-en_COUN-TOPIC-100 >> jobs.txt
# sbatch -e ../tr_output/link_bloom.err -o ../tr_output/link_bloom.out entity_linking.slurm bloom dataset-en_COUN-TOPIC-100 >> jobs.txt
# sbatch -e ../tr_output/link_cn.err -o ../tr_output/link_cn.out entity_linking.slurm bloom CN-zh >> jobs.txt
# sbatch -e ../tr_output/link_in.err -o ../tr_output/link_in.out entity_linking.slurm bloom IN-hi >> jobs.txt
# sbatch -e ../tr_output/link_sa.err -o ../tr_output/link_sa.out entity_linking.slurm bloom SA-ar >> jobs.txt
# sbatch -e ../tr_output/link_kr.err -o ../tr_output/link_kr.out entity_linking.slurm bloom KR-ko >> jobs.txt
# sbatch -e ../tr_output/link_fr.err -o ../tr_output/link_fr.out entity_linking.slurm bloom FR-fr >> jobs.txt
# sbatch -e ../tr_output/link_ru.err -o ../tr_output/link_ru.out entity_linking.slurm bloom RU-ru >> jobs.txt
# sbatch -e ../tr_output/link_bd.err -o ../tr_output/link_bd.out entity_linking.slurm bloom BD-bn >> jobs.txt



