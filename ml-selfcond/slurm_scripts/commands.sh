python scripts/compute_responses.py \
--model-name-or-path 'gpt2-medium' \
--data-path 'data-demo/data_self_cond_country_s[all]' \
--responses-path all_response_h \
--model-cache ../models \
--device cuda

python scripts/compute_expertise.py \
--root-dir all_response_h \
--model-name gpt2-medium \
--concepts 'data-demo/data_self_cond_country_s[all]/concept_list.csv'

python scripts/generate_seq.py \
--model-name-or-path gpt2-medium \
--expertise all_response_h/gpt2-medium/sense/afganistan/expertise/expertise.csv \
--length 30 \
--prompt "In Germany" \
--seed 0 10 \
--temperature 1.0 \
--metric ap \
--forcing on_p50  \
--num-units 50 \
--no-save


python scripts/compute_responses.py \
--model-name-or-path 'bigscience/bloom-350m' \
--data-path assets/football \
--responses-path all_response_h \
--model-cache ../models \
--device cuda


python scripts/compute_responses.py \
--model-name-or-path 'sberbank-ai/mGPT' \
--data-path assets/football \
--responses-path all_response_h \
--model-cache ../models \
--device cuda


python scripts/compute_expertise.py \
--root-dir all_response_h \
--model-name gpt2-medium \
--concepts assets/football/concept_list.csv

python scripts/compute_expertise.py \
--root-dir all_response_h \
--model-name 'sberbank-ai/mGPT' \
--concepts assets/football/concept_list.csv

python scripts/compute_expertise.py \
--root-dir all_response_h \
--model-name 'bigscience/bloom-350m' \
--concepts assets/football/concept_list.csv


python scripts/generate_seq.py \
--model-name-or-path gpt2-medium \
--expertise all_response_h/gpt2-medium/sense/ukraine/expertise/expertise.csv \
--length 30 \
--prompt "In Germany" \
--seed 0 10 \
--temperature 1.0 \
--metric ap \
--forcing on_p50  \
--num-units 50 \
--no-save

python scripts/generate_seq.py \
--model-name-or-path 'sberbank-ai/mGPT' \
--expertise all_response_h/sberbank-ai/mGPT/sense/ukraine/expertise/expertise.csv \
--length 30 \
--prompt "Once" \
--seed 0 10 \
--temperature 1.0 \
--metric ap \
--forcing on_p50  \
--num-units 50 \
--cache-dir ../models \
--no-save


python scripts/generate_seq.py \
--model-name-or-path 'bigscience/bloom-350m' \
--expertise all_response_h/bigscience/bloom-350m/sense/ukraine/expertise/expertise.csv \
--length 30 \
--prompt "In Germany" \
--seed 0 10 \
--temperature 1.0 \
--metric ap \
--forcing on_p50  \
--num-units 50 \
--cache-dir ../models \
--no-save
