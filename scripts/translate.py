#!pip install google-cloud-translate==3.0.0

import os 
import json
from pathlib import Path
from google.cloud import translate
import shutil

DATADIR={
        "root":"/Users/faisal/a/scratch/ml-selfcond/data/dataset-en_COUN-TOPIC-100",
        "group":"sense",
        "concept":"concept_list.csv"
    }

LANGS=['bn', 'zh', 'ar', 'fr', 'ru', 'hi', 'ko','el']


GOOGLE_APPLICATION_CREDENTIALS="key_dgnmt3.json"
from google.cloud import translate
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=GOOGLE_APPLICATION_CREDENTIALS

# Initialize Translation client
def translate_text(text, lang, project_id="clear-beacon-364723"):
    """Translating Text."""

    client = translate.TranslationServiceClient()

    location = "global"

    parent = f"projects/{project_id}/locations/{location}"

    # Translate text from English to French
    # Detail on supported types can be found here:
    # https://cloud.google.com/translate/docs/supported-formats
    
    all_trans=[]
    for i in range(0,len(text),20):
        print(i,i+20) 
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": text[i:i+20],
                "mime_type": "text/plain",  # mime types: text/plain, text/html
                "source_language_code": "en-US",
                "target_language_code": lang,
            }
        )

        for translation in response.translations:
#             print(translation.translated_text)
            all_trans.append(translation.translated_text)
    return all_trans


count=0
for lang in LANGS:
    outpath = Path(Path(DATADIR['root']).parent, Path(DATADIR['root']).name + '-'+lang,DATADIR['group'])
    outpath.mkdir(parents=True, exist_ok=True)
    print(outpath)
    for f in os.listdir(os.path.join(DATADIR['root'],DATADIR['group'])):
        if (not str(f).startswith('._')) and ('DS_Store' not in str(f)):
            print(f)
#             count=count+1
#             if count>2:
#                 break
            with open(os.path.join(DATADIR['root'],DATADIR['group'],f)) as json_file:
                    concept = json.load(json_file)
                    new_concept = concept
                    new_concept['sentences']['positive']=translate_text(concept['sentences']['positive'],lang)
                    new_concept['sentences']['negative']=translate_text(concept['sentences']['negative'],lang)
                    
            outfile=Path(outpath,str(f))
            print(outfile)
            with open(outfile,'w', encoding='utf-8') as f:
                json.dump(new_concept, f, ensure_ascii=False, indent=4)
    print('{}/concept_list.csv'.format(DATADIR['root']),str(outpath.parent))        
    shutil.copy('{}/concept_list.csv'.format(DATADIR['root']),str(outpath.parent))