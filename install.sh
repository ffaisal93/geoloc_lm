#!/bin/bash

IF_HOPPER=${IF_HOPPER:-"no"}
INSTALL=${INSTALL:-"no"}
DELETE=${DELETE:-"no"}
DOWNLOAD=${DOWNLOAD:-"no"}
PLOT=${PLOT:-"no"}
IT=${IT:-1}


while [ $# -gt 0 ]; do

   if [[ $1 == *"--"* ]]; then
        param="${1/--/}"
        declare $param="$2"
        echo $1 $2 #Optional to see the parameter:value result
   fi

  shift
done

if [[ "${IF_HOPPER}" == "yes" ]] ;then
    module load python/3.8.6-ff
fi


if [[ "${INSTALL}" == "yes" ]] ;then
    # python -m venv vnv/geo_vnv
    source vnv/geo_vnv/bin/activate
    pip install -r requirements.txt
    python -m spacy download en_core_web_sm
    python -m pip install --upgrade pip
    git clone https://github.com/ranahaani/GNews.git
    git clone https://github.com/ffaisal93/newspaper.git
    cd newspaper
    pip install -r requirements.txt
    python3 setup.py install
    cd ..
    mkdir data
    deactivate
fi


if [[ "${DELETE}" == "yes" ]] ;then
    rm -rf vnv
    rm -rf data
    rm -rf GNews
fi

if [[ "${DOWNLOAD}" == "ALL" ]] ;then
    source vnv/geo_vnv/bin/activate
    python scripts/getData.py -download_data 'ALL' -mode 'en_COUN'
    python scripts/getData.py -download_data 'ALL' -mode 'LANG_COUN'
    python scripts/getData.py -download_data 'TOPIC' -mode 'en_US'
    deactivate
fi

if [[ "${DOWNLOAD}" == "SINGLE" ]] ;then
    source vnv/geo_vnv/bin/activate
    python scripts/getData.py -download_data 'SINGLE' -mode 'LANG_COUN' -lang 'bn' -coun 'BD'
    deactivate
fi


if [[ "${DOWNLOAD}" == "TOPIC" ]] ;then
    source vnv/geo_vnv/bin/activate
    python scripts/getData.py -download_data 'TOPIC' -mode 'en_US'
    deactivate
fi

if [[ "${DOWNLOAD}" == "CONSTRACT" ]] ;then
    source vnv/geo_vnv/bin/activate
    python scripts/getData.py -download_data 'NONE' -mode 'CONSTRACT'
    deactivate
fi

if [[ "${DOWNLOAD}" == "MULTILING" ]] ;then
    source vnv/geo_vnv/bin/activate
    python scripts/getData.py -download_data 'MULTILING' -mode 'LANG_COUN1' -it ${IT}
    deactivate
fi

if [[ "${PLOT}" == "yes" ]] ;then
    source vnv/geo_vnv/bin/activate
    python scripts/plot_similarity.py --expert_dir ../ml-selfcond/all_response_h/dataset-en_COUN-TOPIC-100\
    --data_dir data \
    --model gpt2 \
    --base dataset-en_COUN-TOPIC-100-random

    deactivate
fi
