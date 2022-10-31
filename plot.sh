#!/bin/bash

dirs=$1


declare -a models1=("gpt2" "bloom" "mgpt")
declare -a models2=("bloom" "mgpt")
# declare -a models=("bigscience/bloom-350m")



for dir in ${dirs}/*
do
	base=$(basename $dir /)
	if [ "$base" != '${dirs}/**DS_Store**' ] && ((${#base} > 5 )) && ((${#base} !=28 )); then
		echo ${dir}
		echo ${base}
		echo ${#base}
		for model in "${models1[@]}"
		do
			errorf="tr_output/plot-${model}#${base}.err"
			outf="tr_output/plot-${model}#${base}.out"
			echo ${model}
			echo ${errorf}
			echo ${errorf} >> tr_output/jobs.txt
			echo ${outf}
			sbatch -e ${errorf} -o ${outf} plot.slurm ${model} ${base} ${dir} >> tr_output/jobs.txt
		done
	elif [ "$base" != '${dirs}/**DS_Store**' ] && ((${#base} == 28 )); then
		echo ${dir}
		echo ${base}
		echo ${#base}
		for model in "${models2[@]}"
		do
			errorf="tr_output/plot-${model}#${base}.err"
			outf="tr_output/plot-${model}#${base}.out"
			echo ${model}
			echo ${errorf}
			echo ${errorf} >> tr_output/jobs.txt
			echo ${outf}
			sbatch -e ${errorf} -o ${outf} plot.slurm ${model} ${base} ${dir} >> tr_output/jobs.txt
		done
	else
		echo ${dir}
		echo ${base}
		echo ${#base}
		for model in "${models2[@]}"
		do
			errorf="tr_output/plot-${model}#${base}.err"
			outf="tr_output/plot-${model}#${base}.out"
			echo ${model}
			echo ${errorf}
			echo ${errorf} >> tr_output/jobs.txt
			echo ${outf}
			sbatch -e ${errorf} -o ${outf} plot.slurm ${model} ${base} ${dir} >> tr_output/jobs.txt
		done

	fi


	

done

DATE_WITH_TIME=`date "+%Y%m%d-%H%M%S"`
echo "finished at ${DATE_WITH_TIME} --------------" >>tr_output/jobs.txt

#&& [[ "${base}" == 'AU-en' ]]
