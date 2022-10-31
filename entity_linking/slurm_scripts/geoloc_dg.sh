# dir=${1:-"/scratch/ffaisal/ml-selfcond/data/dataset-en_COUN-TOPIC-100/sense"}
# outdir=${2:-"../data/geoloc"}
# mode=${3:-"concept"}
# label='dataset-en_COUN-TOPIC-100'

# for file in $dir/*
# do
# 	if [ "$file" != "${dir}/**DS_Store**" ] && [ "$file" != "${dir}/**._**" ]; then
# 		echo $file
# 		base=$(basename $file .json)
# 		echo $base
# 		echo ../tr_output/${label}_${base}.err
# 		echo ${outdir}
# 		sbatch -o ../tr_output/${label}_${base}.out -e ../tr_output/${label}_${base}.err geoloc_dg.slurm $file $base $outdir $mode
# 	fi
# done




##########generated output------------------------bloom
# dir=${1:-"/projects/antonis/fahim/ner_linking/data/geoloc/dataset-en_COUN-TOPIC-100/bloom/data"}
# outdir=${2:-"/projects/antonis/fahim/ner_linking/data/geoloc/dataset-en_COUN-TOPIC-100/bloom"}
# mode=${3:-"generate"}
# label='dataset-en_COUN-TOPIC-100'

# for file in $dir/*
# do
# 	if [ "$file" != "${dir}/**DS_Store**" ] && [ "$file" != "${dir}/**._**" ]; then
# 		echo $file
# 		base=$(basename $file .pickle)
# 		base=$(basename $base .json)
# 		echo $base
# 		echo ../tr_output/${label}_${base}.err
# 		echo ${outdir}
# 		sbatch -o ../tr_output/${label}_${base}.out -e ../tr_output/${label}_${base}.err geoloc_dg.slurm $file $base $outdir $mode
# 	fi
# done


##########generated output------------------------CN-zh
dir=${1:-"/projects/antonis/fahim/ner_linking/data/geoloc/RU-ru/bloom/data"}
outdir=${2:-"/projects/antonis/fahim/ner_linking/data/geoloc/RU-ru/bloom"}
mode=${3:-"generate"}
label='RU-ru'

for file in $dir/*
do
	if [ "$file" != "${dir}/**DS_Store**" ] && [ "$file" != "${dir}/**._**" ]; then
		echo $file
		base=$(basename $file .pickle)
		base=$(basename $base .json)
		echo $base
		echo ../tr_output/${label}_${base}.err
		echo ${outdir}
		sbatch -o ../tr_output/${label}_${base}.out -e ../tr_output/${label}_${base}.err geoloc_dg.slurm $file $base $outdir $mode
	fi
done



# dir="/scratch/ffaisal/ml-selfcond/data/dataset-en_COUN-TOPIC-100-masked/sense"
# outdir="../data/geoloc"
# mode="concept"
# label='dataset-en_COUN-TOPIC-100-masked'


# for file in $dir/*
# do
# 	if [ "$file" != '${dir}/**DS_Store**' ] && [ "$file" != '${dir}/._**' ]; then
# 		echo $file
# 		base=$(basename $file .json)
# 		echo $base
# 		echo ../tr_output/${label}_${base}.err
# 		echo ${outdir}
# 		sbatch -o ../tr_output/${label}_${base}.out -e ../tr_output/${label}_${base}.err geoloc_dg.slurm $file $base $outdir $mode
# 	fi
# done


# dir="/scratch/ffaisal/ml-selfcond/data/dataset-en_COUN-TOPIC-100-random/sense"
# outdir="../data/geoloc"
# mode="concept"
# label='dataset-en_COUN-TOPIC-100-random'


# for file in $dir/*
# do
# 	if [ "$file" != '${dir}/**DS_Store**' ] && [ "$file" != '${dir}/._**' ]; then
# 		echo $file
# 		base=$(basename $file .json)
# 		echo $base
# 		echo ../tr_output/${label}_${base}.err
# 		echo ${outdir}
# 		sbatch -o ../tr_output/${label}_${base}.out -e ../tr_output/${label}_${base}.err geoloc_dg.slurm $file $base $outdir $mode
# 	fi
# done



# dirr="/scratch/ffaisal/ml-selfcond/data/CONSTRUCT_MLING"
# outdir="../data/geoloc"
# mode="concept"
# label='CONSTRUCT_MLING'


# for dir in $dirr/*
# do
# 	if [ "$dir" != '${dirr}/**DS_Store**' ] && [ "$dir" != '${dirr}/._**' ]; then
# 		dir=${dir}/sense
# 		for file in $dir/*
# 		do
# 			if [ "$file" != '${dir}/**DS_Store**' ] && [ "$file" != '${dir}/._**' ]; then
# 				echo $file
# 				base=$(basename $file .json)
# 				echo $base
# 				echo ../tr_output/${label}_${base}.err
# 				echo ${outdir}
# 				sbatch -o ../tr_output/${label}_${base}.out -e ../tr_output/${label}_${base}.err geoloc_dg.slurm $file $base $outdir $mode
# 			fi
# 		done
# 	fi
# done


# dirr="/scratch/ffaisal/ml-selfcond/data/CONSTRUCT_MLING_COMPARE"
# outdir="../data/geoloc"
# mode="concept"
# label='CONSTRUCT_MLING_COMPARE'


# for dir in $dirr/*
# do
# 	if [ "$dir" != '${dirr}/**DS_Store**' ] && [ "$dir" != '${dirr}/._**' ]; then
# 		dir=${dir}/sense
# 		for file in $dir/*
# 		do
# 			if [ "$file" != '${dir}/**DS_Store**' ] && [ "$file" != '${dir}/._**' ]; then
# 				echo $file
# 				base=$(basename $file .json)
# 				echo $base
# 				echo ../tr_output/${label}_${base}.err
# 				echo ${outdir}
# 				sbatch -o ../tr_output/${label}_${base}.out -e ../tr_output/${label}_${base}.err geoloc_dg.slurm $file $base $outdir $mode
# 			fi
# 		done
# 	fi
# done




