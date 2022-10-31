dir=$1

for file in $dir/*
do
	echo $file
	base=$(basename $file .pickle)
	echo $base
	echo ../tr_output/$base.err
	sbatch -o ../tr_output/$base.out -e ../tr_output/$base.err genre_pr.slurm $file $base
    #whatever you need with "$file"
done
