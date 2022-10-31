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
source vnv/geo_vnv/bin/activate

pip install spacy
pip install spacy-langdetect
python -m spacy download en
python -m spacy download bn
python -m spacy download ru
python -m spacy download zh
python -m spacy download kr
python -m spacy download fr
python -m spacy download ar






