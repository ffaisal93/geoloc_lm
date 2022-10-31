#
# For licensing see accompanying LICENSE file.
# Copyright (C) 2022 Apple Inc. All Rights Reserved.
#

import argparse
import pathlib
from pathlib import Path
import threading
import typing as t
import os
import random
import pandas as pd
import country_converter as coco
import numpy as np
import subprocess
import torch
import json

DISCARD=['.DS_Store','._DS_Store']

COUNTRY_DATABASE='/projects/antonis/fahim/IP2LOCATION-COUNTRY-MULTILINGUAL/IP2LOCATION-COUNTRY-MULTILINGUAL.CSV'
cdb = pd.read_csv(COUNTRY_DATABASE)

COMMANDS = {
    "self-cond": (
        "python scripts/generate_seq.py "
        "--model-name-or-path PARAM_MODEL "
        "--expertise PARAM_CONCEPT "
        "--num-units 10 "
        "--length 30 "
        '--prompt "PARAM_PROMPT" '
        "--seed 0 5 "
        "--temperature 1.0 "
        "--metric ap "
        "--forcing PARAM_FORCING "
        "--device PARAM_DEVICE "
        "--results-file PARAM_RESULTS "
    )
}

templates = [
    "In <country>,",
    "<country> is known for",
    "Inside <country>",
    "In <country>'s",
    "However, in <country>",
    "Yesterday <country>"   
]


multiling_templates = {'GR-el': ['Στη <country>,',
  'Η <country> είναι γνωστή για',
  'Μέσα στη <country>',
  'Σε <country>',
  'Ωστόσο, στη <country>',
  'Χθες <country>'],
 'TZ-en': ['In <country>,',
  '<country> is known for',
  'Inside <country>',
  "In <country>'s",
  'However, in <country>',
  'Yesterday <country>'],
 'PE-es': ['En <country>,',
  '<country> es conocido por',
  'Dentro de <country>',
  'En <country>',
  'Sin embargo, en <country>',
  'Ayer <country>'],
 'HK-zh': ['在<country>，', '<country> 以', '<country>内部', '在<country>的', '但是，在 <country>', '昨天 <country>'],
 'GB-en': ['In <country>,',
  '<country> is known for',
  'Inside <country>',
  "In <country>'s",
  'However, in <country>',
  'Yesterday <country>'],
 'ET-en': ['In <country>,',
  '<country> is known for',
  'Inside <country>',
  "In <country>'s",
  'However, in <country>',
  'Yesterday <country>'],
 'CU-es': ['En <country>,',
  '<country> es conocido por',
  'Dentro de <country>',
  'En <country>',
  'Sin embargo, en <country>',
  'Ayer <country>'],
 'AU-en': ['In <country>,',
  '<country> is known for',
  'Inside <country>',
  "In <country>'s",
  'However, in <country>',
  'Yesterday <country>'],
 'VN-vi': ['Ở <country>,',
  '<country> được biết đến với',
  'Bên trong <country>',
  'Trong <country> của',
  'Tuy nhiên, ở <country>',
  'Hôm qua <country>'],
 'SA-ar': ['في <country> ،',
  '<country> معروف بـ',
  'داخل <country>',
  'في <country>',
  'ومع ذلك ، في <country>',
  'أمس <country>'],
 'RU-ru': ['В <country>,',
  '<country> известна',
  'Внутри <country>',
  'В <country>',
  'Однако в <country>',
  'Вчера <country>'],
 'NO-no': ['I <country>,',
  '<country> er kjent for',
  'Inne i <country>',
  "I <country>'s",
  'Men i <country>',
  'I går <country>'],
 'MX-es': ['En <country>,',
  '<country> es conocido por',
  'Dentro de <country>',
  'En <country>',
  'Sin embargo, en <country>',
  'Ayer <country>'],
 'BD-bn': ['<country>,',
  '<country> এর জন্য পরিচিত',
  '<country> এর ভিতরে',
  '<country> এর',
  'তবে, <country>',
  'গতকাল <country> এ'],
 'CN-zh': ['在<country>，', '<country> 以', '<country>内部', '在<country>的', '但是，在 <country>', '昨天 <country>'],
 'FR-fr': ['En <country>,',
  '<country> est connu pour',
  "À l'intérieur de <country>",
  'En <country>',
  'Cependant, en <country>',
  'Hier <country>'],
 'IN-hi': ['<country> में,',
  '<country> के लिए जाना जाता है',
  'अंदर <country>',
  "<country>'एस . में",
  'हालांकि, <country> . में',
  'कल <country>'],
 'JP-ja': ['<country>では、',
  '<country> は',
  '<country> 内',
  '<country> で',
  'ただし、<country> では',
  '昨日 <country>'],
 'IL-he': ['ב<country>,',
  '<country> ידוע ב',
  'בתוך <country>',
  'ב-<country>',
  'עם זאת, ב<country>',
  'אתמול <country>'],
 'KR-ko': ['<country>에서는', '<country>는', '<country> 내부', '<country>에서', '그러나 <country>에서', '어제 <country>']}


concept_dir='data/en_COUN'


def translate_cname(lang):
    langi=lang.upper()
    if langi=='ZH':
        langi='ZH-CN'
    c_dict2 = dict(zip(cdb.loc[cdb['LANG']==langi]['COUNTRY_ALPHA2_CODE'],
    cdb.loc[cdb['LANG']==langi]['COUNTRY_NAME']))
    c_dict3 = dict(zip(cdb.loc[cdb['LANG']==langi]['COUNTRY_ALPHA3_CODE'],
    cdb.loc[cdb['LANG']==langi]['COUNTRY_NAME']))
    return c_dict2, c_dict3


def get_concept_countries(concept_dir):
    country_names=[]
    for f in os.listdir(concept_dir):
        if f not in DISCARD and 'DS_Store' not in str(f):
            if len(str(f).split('.json')[0])==8 and str(f).split('.json')[0][2]=='_' and str(f).split('.json')[0][5]=='_':
                print(str(f))
                pos_2_code=str(f).split('_')[-1].replace('.json','')
                lang=str(f).split('_')[1]
                c_dict2, c_dict3 = translate_cname(lang)
                ccode2 = pos_2_code
                coun = coco.convert(ccode2, to='name_short')
                ccode3 = coco.convert(coun.replace('_',' '), to='ISO3')
                try:
                    coun = c_dict2[ccode2]
                except KeyError:
                    try:
                        coun = c_dict3[ccode3]
                    except KeyError:
                        coun = coun

                print(coun, ccode2, ccode3, lang)
                country_names.append([str(f).split('.json')[0],coun])
            else:
                country_names.append([str(f).split('.json')[0],str(f).split('.json')[0]])
    return country_names

def create_country_prompts(condition_countries, base_name) -> t.List[str]:
    prompts = []
    print(base_name)
    if len(base_name)==5 and base_name[2]=='-' and base_name[3:]!='en':
        for template in multiling_templates[base_name]:
            for country in condition_countries:
                prompts.append(template.replace("<country>", country))
        random.shuffle(prompts)
    else:
        for template in templates:
            for country in condition_countries:
                prompts.append(template.replace("<country>", country))
        random.shuffle(prompts)
    return prompts



def run(
    prompts: t.Sequence[str],
    concept: t.Sequence[str],
    device: str,
    model_name: str,
    concept_dir: pathlib.Path,
    folder: pathlib.Path,
    forcing: str,
    method: str,
) -> None:

    for i,prompt in enumerate(prompts):
        concept_name='{}/{}/expertise/expertise.csv'.format(concept_dir,concept[i])
        folder_n = pathlib.Path(folder,concept[i])
        folder_n.mkdir(exist_ok=True, parents=True)
        results_file = folder_n / f'gen_sentences#{concept[i]}#{prompt.replace(" ", "_")}.csv'
        current_cmd = (
            COMMANDS[method]
            .replace("PARAM_CONCEPT", str(concept_name))
            .replace("PARAM_PROMPT", prompt)
            .replace("PARAM_DEVICE", device)
            .replace("PARAM_RESULTS", f'"{str(results_file)}"')
            .replace("PARAM_FORCING", forcing)
            .replace("PARAM_MODEL", model_name))
        
        # print(results_file)
        print(current_cmd)
        if Path(results_file).is_file():
            print(f'{results_file} exist')
        else:
            print(current_cmd)
            if Path(concept_name).is_file():
                subprocess.Popen(current_cmd, shell=True).wait()
                print(i,'/',len(prompts))
            else:
                print(f'{concept_name} does not exist')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--concept_dir", type=pathlib.Path, required=True)
    parser.add_argument("--model_name", type=str, required=True)
    parser.add_argument("--country_limit", type=int, required=True)
    parser.add_argument("--device", type=str, required=True, choices=["cpu", "cuda"])
    parser.add_argument("--folder", type=pathlib.Path, required=False, default=None)
    parser.add_argument("--forcing", type=str, required=False, default="on_p50")
    parser.add_argument(
        "--prompts",
        type=str,
        required=False,
        choices=["country"],
    )
    parser.add_argument(
        "--method",
        type=str,
        choices=list(COMMANDS.keys()),
        help="Method to use.",
        default="ours",
    )
    args = parser.parse_args()
    print(args)
    n_gpus: int = torch.cuda.device_count() if args.device == "cuda" else 1

    all_prompts: t.List[str] = []
    all_concepts: t.List[str] = []
    if args.prompts=='country':
        country_limit=int(args.country_limit)
        country_names=get_concept_countries(args.concept_dir)

    for concept_count in country_names:
        concept_country = concept_count[0]
        condition_countries=country_names.copy()
        # condition_countries.remove(concept_country)
        # random.shuffle(condition_countries)
        condition_countries_n = [x[1].capitalize().replace('_',' ') for x in condition_countries[country_limit:country_limit+10]]
        print(condition_countries_n,"-----")
        returnen_prompts=create_country_prompts(condition_countries_n, str(args.folder).split('/')[1])
        all_prompts.extend(returnen_prompts)
        c_concept=[concept_country]*len(returnen_prompts)
        all_concepts.extend(c_concept)
        print(returnen_prompts)
        print(c_concept)


    # Split prompts into n_gpus lists
    prompt_lists = np.array_split(all_prompts, n_gpus)
    concept_lists = np.array_split(all_concepts, n_gpus)


    # Run generation multi-threaded (one thread per GPU)
    threads = []
    for i, prompts in enumerate(prompt_lists):
        th = threading.Thread(
            target=run,
            args=(
                prompts,
                concept_lists[i],
                f"{args.device}:{i}",
                args.model_name,
                args.concept_dir,
                args.folder,
                args.forcing,
                args.method,
            ),
        )
        th.start()
        threads.append(th)

    for th in threads:
        th.join()


if __name__ == "__main__":
    main()
