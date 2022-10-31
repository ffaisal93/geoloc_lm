dirr="../data/geoloc"
outdir="../data/geoloc"
mode="bloom"
label='CONSTRUCT_MLING'


for dir in $dirr/*
do
  echo dir: ${dir}
  if [ "$dir" != '${dirr}/**DS_Store**' ] && [ "$dir" != '${dirr}/._**' ] && [ "$dir" == "${dirr}/dataset-en_COUN-TOPIC-100" ]; then
      dir=${dir}/${mode}/entity
      for file in ${dir}/*
      do
          if [ "$file" != '${dir}/**DS_Store**' ] && [ "$file" != '${dir}/._**' ]; then
              echo file: $file
              base=$(basename $file .pickle)
              echo base: $base
              # echo ../tr_output/${label}_${base}.err
              echo ${mode} ${base} ${file} ${outdir}
              # sbatch -o ../tr_output/${label}_${base}.out -e ../tr_output/${label}_${base}.err entity_linking.slurm $file $base $outdir $mode
              # python entity_linking.py --mode ${mode} \
              #   --name ${base} \
              #   --data_file ${file} \
              #   --out_dir ${outdir}
          fi
      done
  fi
done
