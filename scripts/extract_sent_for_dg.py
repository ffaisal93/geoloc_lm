import pandas as pd
import typing as t
import random
import os
import pickle
from pathlib import Path


templates = [
    "In <country>,",
    "<country> is known for",
    "Inside <country>",
    "In <country>'s",
    "However, in <country>",
    "Yesterday <country>"   
]

GENDIR={
        "root":"/Users/faisal/a/scratch/ml-selfcond/generated/dataset-en_COUN-TOPIC-100",
        "group":"sense",
        "concept":"concept_list.csv"
    }

OUTDIR={
    #/projects/antonis/fahim/ner_linking/data
    "root":"/Users/faisal/a/projects/ner_linking/data"
}

MDIR={
    "gpt2":"gpt2-medium",
    "bloom":"bigscience/bloom-560m",
    "mgpt":"sberbank-ai/mGPT"
}



model='gpt2'



def get_concept_countries(concept_dir):
    country_names=[]
    for f in os.listdir(concept_dir):
        if not str(f).startswith('.') and 'other' not in str(f):
            country_names.append(str(f).split('.json')[0])
    return country_names

def create_country_prompts(condition_countries) -> t.List[str]:
    prompts = []
    for template in templates:
        for country in condition_countries:
            prompts.append((template.replace("<country>", country),country.lower().replace(' ','_')))
    return prompts



if __name__ == '__main__':
    all_prompts={}
    all_concepts: t.List[str] = []
    
    model='gpt2'
    country_names=get_concept_countries(os.path.join(GENDIR['root'],MDIR[model]))

    for concept_country in country_names:
        condition_countries=country_names.copy()
        condition_countries_n = [x.capitalize().replace('_',' ') for x in condition_countries]
        returned_prompts=create_country_prompts(condition_countries_n)
        all_prompts[concept_country]=returned_prompts



    all_files={}
    for c in all_prompts:
        all_files[c]={}
        for pr,pr1 in all_prompts[c]:
            all_files[c][pr]=("{}/{}/{}/gen_sentences#{}#{}.csv".format(
                GENDIR['root'],MDIR[model],c,c,pr.replace(" ", "_")),pr1)
    
    dataset='dataset-en_COUN-TOPIC-100'        
    outpath_data=Path("{}/{}/data".format(OUTDIR['root'],dataset))
    outpath_key=Path("{}/{}/key".format(OUTDIR['root'],dataset))
    outpath_entity=Path("{}/{}/entity".format(OUTDIR['root'],dataset))
    print(outpath_data)
    outpath_data.mkdir(parents=True, exist_ok=True)
    print(outpath_key)
    outpath_key.mkdir(parents=True, exist_ok=True)
    print(outpath_entity)
    outpath_entity.mkdir(parents=True, exist_ok=True)
  
    for coun in all_files.keys():
        keys=list(all_files[coun].keys())
        all_sents=[]
        all_keys=[]
        cnt=0
        for i,k in enumerate(keys):
            df = pd.read_csv(all_files[coun][keys[i]][0],index_col=[0])
            sents=df.sort_values(by="perplexity", ascending=True)['sentence'].to_list()[:10]
            sents=[x.replace(keys[i],"") for x in sents]
            all_sents.extend(sents)
            all_keys.extend([all_files[coun][keys[i]][1]]*len(sents))
        with open(Path(outpath_data,'{}.pickle'.format(coun)),'wb') as outf:
            pickle.dump(all_sents,outf)
        with open(Path(outpath_key,'{}.pickle'.format(coun)),'wb') as outf:
            pickle.dump(all_keys,outf)