#!/bin/bash

dirs=$1
type=${2:-'generate_all'}


declare -a models=("gpt2-medium" "bigscience/bloom-560m" "sberbank-ai/mGPT")
declare -a models=("sberbank-ai/mGPT")
# declare -a models=("bigscience/bloom-560m")
declare -a country_limit=(0 10 20 30 40 50 60)
# declare -a country_limit=(50 60)
declare -a models=("bigscience/bloom-560m")

cd ..

echo ${type}

dir=${dirs}
base=$(basename $dir /)
for model in "${models[@]}"
do
        if [ "$type" == "generate_all" ]; then
                for c_limit in "${country_limit[@]}"
                do
                        echo ${c_limit}
                        base_m=$(basename $model /)
                        outf=tr_output/${base_m}#${base}#${c_limit}.out
                        errorf=tr_output/${base_m}#${base}#${c_limit}.err
                        echo $base
                        echo $model
                        echo $outf
                        echo $errorf
                        echo $errorf >> new_scripts/jobs.txt
                        echo ------------------------------------
                        echo "  "
                        echo ${dir} ${base} ${model} ${c_limit}

                        sbatch -o $outf \
                        -e $errorf \
                        new_scripts/inference.slurm ${dir} ${base} ${model} ${c_limit} >> new_scripts/jobs.txt
                done
        elif [ "$type" == "compute" ]; then
                base_m=$(basename $model /)
                outf=tr_output/${base_m}#${base}#${type}.out
                errorf=tr_output/${base_m}#${base}#${type}.err
                echo $base
                echo $model
                echo $outf
                echo $errorf
                echo $errorf >> new_scripts/jobs.txt
                echo ------------------------------------
                echo "  "

                sbatch -o $outf \
                -e $errorf \
                new_scripts/inference.slurm ${dir} ${base} ${model} -1 >> new_scripts/jobs.txt
        fi

done

# for dir in ${dirs}/*
# do
#       echo ${dir}

#       if [ "$dir" != "${dirs}/dataset*" ] && [ "$dir" != '${dirs}/**DS_Store**' ]; then
#               echo ${dir}
#         base=$(basename $dir /)
#               # v2=${base: -3}
#               for model in "${models[@]}"
#               do
#                       if [ "$type" == "generate_all" ]; then
#                               for c_limit in "${country_limit[@]}"
#                               do
#                                       echo ${c_limit}
#                                       base_m=$(basename $model /)
#                                       outf=tr_output/${base_m}#${base}#${c_limit}.out
#                                       errorf=tr_output/${base_m}#${base}#${c_limit}.err
#                                       echo $base
#                                       echo $model
#                                       echo $outf
#                                       echo $errorf
#                                       echo $errorf >> new_scripts/jobs.txt
#                                       echo ------------------------------------
#                                       echo "  "

#                                       sbatch -o $outf \
#                                       -e $errorf \
#                                       new_scripts/inference.slurm ${dir} ${base} ${model} ${c_limit} >> new_scripts/jobs.txt
#                               done
#                       elif [ "$type" == "compute" ]; then
#                               base_m=$(basename $model /)
#                               outf=tr_output/${base_m}#${base}#${type}.out
#                               errorf=tr_output/${base_m}#${base}#${type}.err
#                               echo $base
#                               echo $model
#                               echo $outf
#                               echo $errorf
#                               echo $errorf >> new_scripts/jobs.txt
#                               echo ------------------------------------
#                               echo "  "

#                               sbatch -o $outf \
#                               -e $errorf \
#                               new_scripts/inference.slurm ${dir} ${base} ${model} -1 >> new_scripts/jobs.txt
#                       fi

#               done

#       fi

# done

DATE_WITH_TIME=`date "+%Y%m%d-%H%M%S"`

echo "finished at ${DATE_WITH_TIME} --------------" >>new_scripts/jobs.txt
