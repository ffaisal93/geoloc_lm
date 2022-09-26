#!/bin/bash


for langc in {0..39}
do
	echo ${langc}
	errorf="tr_output/mling_${langc}.err"
	outf="tr_output/mling_${langc}.out"
	echo ${errorf}, ${outf}
	sbatch -e ${errorf} -o ${outf} run_multiling.slurm ${langc}
done