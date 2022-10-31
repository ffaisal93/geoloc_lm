#!/bin/bash

dir=$1
base=$2
model=$3
c_limit=${4:-10}
mode=${5:-'generate_all'}
echo model ${model}

python -c 'import torch'

if [[ ${mode} == "compute" ]]; then

	# python scripts/compute_responses.py \
	# --model-name-or-path ${model} \
	# --data-path ${dir} \
	# --responses-path all_response_h/${base} \
	# --model-cache ../models \
	# --device cuda

	python scripts/compute_expertise.py \
	--root-dir all_response_h/${base} \
	--model-name ${model} \
	--concepts ${dir}'/concept_list.csv'
	
fi


if [[ ${mode} == "generate_single" ]]; then

	cdir=all_response_h/${base}/${model}/sense

	for country in ${cdir}/*
	do
		if [[ "$country" != *"DS_Store"* ]]; then
				cbase=$(basename $country /)
				base_m=$(basename $model /)
				echo ${cbase},${country}
				python scripts/generate_seq.py \
				--model-name-or-path ${model} \
				--expertise all_response_h/${base}/${model}/sense/${cbase}/expertise/expertise.csv \
				--length 30 \
				--prompt "In China" \
				--seed 0 10 \
				--temperature 1.0 \
				--metric ap \
				--forcing on_p50  \
				--num-units 50 \
				--results-file outputs/${base}#${base_m}#${cbase}.csv
		fi
	done
fi

if [[ ${mode} == "generate_all" ]]; then
	echo -----${dir} ${base} ${model} ${c_limit} ${mode}
	echo ${c_limit}
	base_m=$(basename $model /)
	python scripts/generate_country_batch.py \
	--concept_dir all_response_h/${base}/${model}/sense \
	--model_name ${model} \
	--country_limit ${c_limit} \
	--device cuda \
	--prompts country \
	--method self-cond \
	--folder generated/${base}/${base_m}
fi


deactivate
