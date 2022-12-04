#!pip install google-cloud-translate==3.0.0

import os 
import json
from pathlib import Path
from google.cloud import translate
import shutil



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




text=['I have a cat']
for lang in LANGS:
    outdata = translate_text(text, lang, project_id="clear-beacon-364723")
    print(outdata)

