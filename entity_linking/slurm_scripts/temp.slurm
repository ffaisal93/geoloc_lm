#!/bin/bash
#SBATCH --partition=normal                 # will run on any cpus in the 'normal' partition
#SBATCH --job-name=python-cpu
#SBATCH --output=../tr_output/temp.out
#SBATCH --error=../tr_output/temp.err
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1                   # up to 48 per node
#SBATCH --mem-per-cpu=96G                 # memory per CORE; maximum is 180GB per node
#SBATCH --export=ALL
#SBATCH --time=0-01:00:00                   # set to 1hr; please choose carefully

# set echo
# umask 0027

# module load gnu10
# module load python                          # load the recommended python version


/scratch/ffaisal/mgenre/mgenre/bin/activate
# execute your python script


cd ../GENRE
# python genre_pr.py $file $name



python temp.py
