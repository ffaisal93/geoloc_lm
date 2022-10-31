import pandas as pd
import typing as t
import random
import os
import pickle
from pathlib import Path
import country_converter as coco
import traceback


COUNTRY_DATABASE='/Users/faisal/a/projects/IP2LOCATION-COUNTRY-MULTILINGUAL/IP2LOCATION-COUNTRY-MULTILINGUAL.CSV'
cdb = pd.read_csv(COUNTRY_DATABASE)

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

GENDIR={
        "root":"/Users/faisal/a/scratch/ml-selfcond/generated",
        "group":"sense",
        "concept":"concept_list.csv"
    }

OUTDIR={
    #/projects/antonis/fahim/ner_linking/data
    "root":"/Users/faisal/a/projects/ner_linking/data/geoloc"
}

MDIR={
    "gpt2":"gpt2-medium",
    "bloom":"bloom-560m",
    "mgpt":"sberbank-ai/mGPT"
}


DISCARD=['.DS_Store','._DS_Store']

model='gpt2'


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
        if f not in DISCARD and 'DS_Store' not in str(f) and 'other' not in str(f) and not str(f).startswith('.'):
            if len(str(f).split('.json')[0])==8 and str(f).split('.json')[0][2]=='_' and str(f).split('.json')[0][5]=='_':
                with os.scandir(Path(concept_dir,f)) as it:
                    if any(it):
#                         print(str(f))
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

#                         print(coun, ccode2, ccode3, lang)
                        country_names.append([str(f).split('.json')[0],coun])
                    else:
                        print(f'{Path(concept_dir,f)} empty')
            else:
                country_names.append([str(f).split('.json')[0],str(f).split('.json')[0]])
    return country_names


# def get_concept_countries(concept_dir):
#     country_names=[]
#     for f in os.listdir(concept_dir):
#         if not str(f).startswith('.') and 'other' not in str(f):
#             with os.scandir(Path(concept_dir,f)) as it:
#                 if any(it):
#                     country_names.append(str(f).split('.json')[0])
#                 else:
#                     print(f'{Path(concept_dir,f)} empty')
#     return country_names

def create_country_prompts(condition_countries, base_name,condition_countries_eng) -> t.List[str]:
#     prompts = []
#     for template in templates:
#         for country in condition_countries:
#             prompts.append((template.replace("<country>", country),country.lower().replace(' ','_')))
#     return prompts
    prompts = []
#     print(base_name)
    if len(base_name)==5 and base_name[2]=='-' and base_name[3:]!='en':
        for template in multiling_templates[base_name]:
            for i,country in enumerate(condition_countries):
                prompts.append((template.replace("<country>", country),
                                condition_countries_eng[i]))
        random.shuffle(prompts)
    else:
        for template in templates:
            for country in condition_countries:
                prompts.append((template.replace("<country>", country),country.lower().replace(' ','_')))
        random.shuffle(prompts)
    return prompts



if __name__ == '__main__':
    all_prompts={}
    all_concepts: t.List[str] = []
    
    model='bloom'
    dataset='dataset-en_COUN-TOPIC-100'
    dataset='CN-zh'
    
    country_names=get_concept_countries(os.path.join(GENDIR['root'],dataset,MDIR[model]))
    condition_countries_eng = [coco.convert(x[0].split('_')[-1]
                                , to='name_short').lower().replace(' ','_')
                               for x in country_names]
    for concept_count in country_names:
        concept_country = concept_count[0]
        condition_countries=country_names.copy()
        condition_countries_n = [x[1].capitalize().replace('_',' ') for x in condition_countries]
        returned_prompts=create_country_prompts(condition_countries_n,dataset,condition_countries_eng)
        all_prompts[concept_country]=returned_prompts


    
    all_files={}
    for c in all_prompts:
        all_files[c]={}
        for pr,pr1 in all_prompts[c]:
            all_files[c][pr]=("{}/{}/{}/{}/gen_sentences#{}#{}.csv".format(
                GENDIR['root'],dataset,MDIR[model],c,c,pr.replace(" ", "_")),pr1)
    
    outpath_data=Path("{}/{}/{}/data".format(OUTDIR['root'],dataset,model))
    outpath_key=Path("{}/{}/{}/key".format(OUTDIR['root'],dataset,model))
    outpath_entity=Path("{}/{}/{}/entity".format(OUTDIR['root'],dataset,model))
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
            try:
                if Path(all_files[coun][keys[i]][0]).is_file():
                    df = pd.read_csv(all_files[coun][keys[i]][0],index_col=[0])
                    sents=df.sort_values(by="perplexity", ascending=True)['sentence'].to_list()[:5]
                    sents=[x.replace(keys[i],"") for x in sents]
                    all_sents.extend(sents)
                    all_keys.extend([all_files[coun][keys[i]][1]]*len(sents))
                else:
                    print(f'{all_files[coun][keys[i]][0]} not found')
            except Exception:
                traceback.print_exc()
                print(Path(all_files[coun][keys[i]][0]))
        with open(Path(outpath_data,'{}.pickle'.format(coun)),'wb') as outf:
            pickle.dump(all_sents,outf)
        with open(Path(outpath_key,'{}.pickle'.format(coun)),'wb') as outf:
            pickle.dump(all_keys,outf)