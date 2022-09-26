import sys
import os
from pathlib import Path
import argparse
import json
import random
import pandas as pd
import math
from nltk import tokenize
import spacy
import shutil
import string
nlp = spacy.load('en_core_web_sm')





PACKAGE_gnews=str(Path(__file__).parent.parent)+'/GNews'
ROOT_DIR =str(Path(__file__).parent.parent)
sys.path.insert(0, PACKAGE_gnews)
sys.path.insert(1, ROOT_DIR)

from gnews.utils.constants import AVAILABLE_COUNTRIES, AVAILABLE_LANGUAGES, TOPICS, BASE_URL, USER_AGENT
from gnews.gnews import GNews


DISCARD=['.DS_Store']
COUN_LANG={'US': 'en',
 'ID': 'id',
 'IN':'hi',
 'DE': 'de',
 'MX': 'es',
 'FR': 'fr',
 'IT': 'it',
 'LV': 'lv',
 'LT': 'lt',
 'HU': 'hu',
 'NL': 'nl',
 'NO': 'no',
 'PL': 'pl',
 'BR': 'pt',
 'PT': 'pt',
 'RO': 'ro',
 'SK': 'sk',
 'SI': 'sl',
 'SE': 'sv',
 'VN': 'vi',
 'TR': 'tr',
 'GR': 'el',
 'BG': 'bg',
 'RU': 'ru',
 'RS': 'sr',
 'UA': 'uk',
 'IL': 'he',
 'SA': 'ar',
 'IN': 'hi',
 'BD': 'bn',
 'TH': 'th',
 'CN': 'zh',
 'HK': 'zh',
 'JP': 'ja',
 'KR': 'ko'}

LEFT_LANG = {'CN': 'zh', 'HK':'zh','BR': 'pt', 'PT': 'pt', 'IN':'hi'}

# COUN_LANG={'US': 'en',
#  'GR': 'el',
#  'BD': 'bn',
#  'ID': 'id',
#  'DE': 'de',
#  'MX': 'es-419',
#  'FR': 'fr',
#  'IT': 'it',
#  'HU': 'hu',
#  'NL': 'nl',
#  'NO': 'no',
#  'PL': 'pl',
#  'RO': 'ro',
#  'SI': 'sl',
#  'SE': 'sv',
#  'VN': 'vi',
#  'TR': 'tr',
#  'BG': 'bg',
#  'RU': 'ru',
#  'RS': 'sr',
#  'UA': 'uk',
#  'IL': 'he',
#  'SA': 'ar',
#  'IN': 'hi',
#  'JP': 'ja',
#  'KR': 'ko'}

class getData:
  def __init__(self):
    self.outdir='data/'
    self.google_news = GNews(language='en', 
        country='US', 
        period='30d', 
        start_date=None, 
        end_date=None, 
        max_results=50, exclude_websites=['yahoo.com', 'cnn.com'])

    
  def download_data(self,mode='en_US',outdir='data/'):
    self.outdir = outdir
    outpath=Path("{}/{}".format(self.outdir,mode)) 
    print(outpath)
    outpath.mkdir(parents=True, exist_ok=True)   
    count=0
    for coun, code in AVAILABLE_COUNTRIES.items():
      count+=1
      # if count>7:
      #     break
      print(coun,code)

      if mode=='en_US':
        self.google_news.language='en'
        self.google_news.country='US'
      elif mode=='en_COUN':
        self.google_news.language='en'
        self.google_news.country=code
      elif mode=='LANG_COUN' and code in COUN_LANG:
          self.google_news.language=COUN_LANG[code]
          self.google_news.country=code
      elif mode=='LANG_COUN' and code not in COUN_LANG:
        continue

      coun=str.strip(coun)
      coun=coun.replace(' ','_')
      json_resp = self.google_news.get_news_by_location(coun)
      all_news={}
      for art in json_resp:
          article = self.google_news.get_full_article(
              art['url'])
          if article!=None:
              all_news[article.title]=article.text
          else:
              print(coun, art)
      outfile=os.path.join(outpath,'{}.json'.format(coun))
      with open(outfile,'w', encoding='utf-8') as f:
          json.dump(all_news, f, ensure_ascii=False, indent=4)

  def download_mling(self,mode='LANG_COUN',outdir='data/'):

    COUN_LANG=LEFT_LANG
    self.outdir = outdir
    outpath=Path("{}/{}".format(self.outdir,mode)) 
    print(outpath)
    outpath.mkdir(parents=True, exist_ok=True)   
    count=0
    for orig, lang in COUN_LANG.items():
      outpath=Path("{}/{}/{}".format(self.outdir,mode,orig)) 
      print(outpath,"---")
      outpath.mkdir(parents=True, exist_ok=True) 

      self.google_news.language=lang
      self.google_news.country=orig

      for coun, code in AVAILABLE_COUNTRIES.items():
        count+=1
        # if count>7:
        #     break
        print(coun,code)
        coun=str.strip(coun)
        coun=coun.replace(' ','_')
        json_resp = self.google_news.get_news(coun)
        all_news={}
        for art in json_resp:
            article = self.google_news.get_full_article(
                art['url'])
            if article!=None:
                all_news[article.title]=article.text
            else:
                print(coun, art)
        if len(all_news)!=0:
          outfile=os.path.join(outpath,'{}_{}_{}.json'.format(orig,lang,code))
          with open(outfile,'w', encoding='utf-8') as f:
              json.dump(all_news, f, ensure_ascii=False, indent=4)

  def download_single(self,mode,language='en',coun='US',outdir='data/'):
    self.outdir = outdir
    outpath=Path("{}/{}".format(self.outdir,mode)) 
    print(outpath)
    outpath.mkdir(parents=True, exist_ok=True)   
    self.google_news.language=language
    self.google_news.country=coun
    coun=str.strip(coun)
    coun=coun.replace(' ','_')
    json_resp = self.google_news.get_news_by_location(coun)
    all_news={}
    for art in json_resp:
        article = self.google_news.get_full_article(
            art['url'])
        if article!=None:
            all_news[article.title]=article.text
        else:
            print(coun, art)
    outfile=os.path.join(outpath,'{}.json'.format(coun))
    with open(outfile,'w', encoding='utf-8') as f:
        json.dump(all_news, f, ensure_ascii=False, indent=4)

  def download_topic(self,mode='en_US',outdir='data/'):
    self.outdir = outdir
    outpath=Path("{}/{}".format(self.outdir,'TOPIC')) 
    print(outpath)
    outpath.mkdir(parents=True, exist_ok=True)   
    
    topics=[]
    #https://getthewordout.com.au/list-of-categories-and-topics/
    with open('topic.txt','r') as f:
      for t in f.readlines():
        topics.append(t.split('\n')[0])
    print(topics)
    count=0

    for coun in topics:
        count+=1
        # if count>7:
        #     break
        print(coun)

        if mode=='en_US':
          self.google_news.language='en'
          self.google_news.country='US'
        coun=str.strip(coun)
        coun=coun.replace(' ','_')
        json_resp = self.google_news.get_news(coun)
        all_news={}
        for art in json_resp:
            article = self.google_news.get_full_article(
                art['url'])
            if article!=None:
                all_news[article.title]=article.text
            else:
                print(coun, art)
        if len(all_news)!=0:
          outfile=os.path.join(outpath,'{}.json'.format(coun))
          with open(outfile,'w', encoding='utf-8') as f:
              json.dump(all_news, f, ensure_ascii=False, indent=4)




  def get_neg(self,negdir,coun,neg_count):
    all_topic=[]
    for f in os.listdir(negdir):
        if f not in DISCARD:
            all_topic.append(f)
    random.shuffle(all_topic)

    all_text=''
    for f in all_topic[:4]:
        with open(os.path.join(negdir,f),'r') as f1:
            data=json.load(f1)
            for title,text in data.items():
                all_text=all_text+'\n'+'\n'+text
    l= nlp(all_text)
    l=[str(line).replace('\n','') for line in l.sents if len(line.text.split(' '))>3
      and coun.lower()[:5] not in str(line).lower()]   
    random.shuffle(l)
    return l[:neg_count]


  def constract_dataset(self,pos_count=100,posdir='data/en_COUN',negdir='data/TOPIC',outdir='data/dataset-en_COUN-TOPIC'):

      outpath=Path(outdir+'-'+str(pos_count))
      print(outpath)
      outpath.mkdir(parents=True, exist_ok=True) 
      coun_list=[]
      for f in os.listdir(posdir):
          if f not in DISCARD:
              all_text=''
              with open(os.path.join(posdir,f),'r') as f1:
                  data=json.load(f1)
                  for title,text in data.items():
                      all_text=all_text+'\n'+'\n'+text
                  l= nlp(all_text)
                  coun=str(f).lower().split('.json')[0]
                  counj=' '.join(str(f).lower().split('.json')[0].split('_'))
                  l=[str(line).replace('\n','') for line in l.sents if counj.lower()[:5] in str(line).lower()]
                  if len(l)>pos_count:
                    pos_ex=l[:pos_count]
                  else:
                    print('total', len(l),coun)
                    needed=math.ceil((pos_count-len(l))/len(l))+1
                    pos_ex=(l*needed)[:pos_count]
                  neg_ex=self.get_neg(negdir,counj, pos_count*3)
                  coun_list.append(coun)
                  concept_new = {'concept': coun,
                      'group': 'sense',
                      'source': 'gnews',
                      'sentences': {'positive':pos_ex,'negative':neg_ex}}
                  print(coun)
                  with open(os.path.join(outpath,'{}.json'.format(coun)),'w', encoding='utf-8') as f:
                    json.dump(concept_new, f, ensure_ascii=False, indent=4)
      senses=['sense']*len(coun_list)
      concept_list = pd.DataFrame({'group':senses, 'concept':coun_list})
      concept_list.to_csv(os.path.join(outpath,'concept_list.csv'),index=False)

  def mask_generator(size=4, chars=string.ascii_uppercase ):
      return ''.join(random.choice(chars) for _ in range(size))


  def mask_dataset(self,tag='masked'):
    DATADIR={
        "root":"/Users/faisal/a/scratch/ml-selfcond/data/dataset-en_COUN-TOPIC-100",
        "group":"sense",
        "concept":"concept_list.csv"
    }

    NEW_DATADIR=Path("{}-{}/{}".format(DATADIR['root'],tag,DATADIR['group']))
    NEW_DATADIR.mkdir(parents=True, exist_ok=True)

    types=['PERSON','ORG','GPE','FAC']
    count=0
    for f in os.listdir(os.path.join(DATADIR['root'],DATADIR['group'])):
        if 'DS_Store' not in str(f):
            count+=1
#             if count>1:
#                 break
    #         print(f)
            pos_sent=[]
            neg_sent=[]
            with open(os.path.join(DATADIR['root'],DATADIR['group'],f)) as json_file:
                concept = json.load(json_file)
            for line in concept['sentences']['positive']:
                text1=nlp(line)
                text=line
                ls = line.split(' ')
                masks=[ls[random.randint(0, len(ls)-1)]]
                for word in text1.ents:
                    if word.label_ in types and concept['concept'][:4].lower() not in word.text.lower():
                        i=random.randint(0, len(masks))
                        text=text.replace(word.text,masks[i-1])
                    elif concept['concept'][:4].lower() not in word.text.lower():
                        masks.append(word.text.lower())
                pos_sent.append(text)
            for line in concept['sentences']['negative']:
                text1=nlp(line)
                text=line
                ls = line.split(' ')
                masks=[ls[random.randint(0, len(ls)-1)]]
                if concept['concept'][:4].lower() in masks[0]:
                    masks=['mask']
                for word in text1.ents:
                    if word.label_ in types:
                        i=random.randint(0, len(masks))
                        text=text.replace(word.text,masks[i-1]) 
                    elif concept['concept'][:4].lower() not in word.text.lower():
                        masks.append(word.text.lower())
                neg_sent.append(text)

            concept_new = {'concept': concept['concept'],
                             'group': 'sense',
                             'source': 'gnews',
                             'sentences': {'positive':pos_sent,
                                           'negative':neg_sent}}

            with open('{}/{}'.format(str(NEW_DATADIR),str(f)),'w', encoding='utf-8') as f_out:
                json.dump(concept_new, f_out, ensure_ascii=False, indent=4)
    shutil.copy('{}/concept_list.csv'.format(DATADIR['root']),NEW_DATADIR.parent)

  def random_dataset(self,tag='random'):
    DATADIR={
        "root":"/Users/faisal/a/scratch/ml-selfcond/data/dataset-en_COUN-TOPIC-100",
        "group":"sense",
        "concept":"concept_list.csv"
    }

    NEW_DATADIR=Path("{}-{}/{}".format(DATADIR['root'],tag,DATADIR['group']))
    NEW_DATADIR.mkdir(parents=True, exist_ok=True)


    count=0
    for f in os.listdir(os.path.join(DATADIR['root'],DATADIR['group'])):
        if 'DS_Store' not in str(f):
            count+=1
#             if count>1:
#                 break
    #         print(f)
            pos_sent=[]
            neg_sent=[]
            with open(os.path.join(DATADIR['root'],DATADIR['group'],f)) as json_file:
                concept = json.load(json_file)
            for line in concept['sentences']['positive']:
                text=line.split(' ')
                textn=[]
                for t in text:
                    k = random.randint(0, 1)
                    if k==0:
                        tx=concept['concept']
                    else:
                        tx=t
                    textn.append(tx)
                textn=' '.join(textn)
                pos_sent.append(textn)
            for line in concept['sentences']['negative']:
                text=line.split(' ')
                textn=[]
                for t in text:
                    k = random.randint(0, 1)
#                     tx=mask_generator(random.randint(0, 1))
                    if k==0:
                        textn.append(t)
                    else:
                        ind=random.randint(0, len(text)-1)
                        textn.append(text[ind])
                textn=' '.join(textn)
                neg_sent.append(textn)

            concept_new = {'concept': concept['concept'],
                             'group': 'sense',
                             'source': 'gnews',
                             'sentences': {'positive':pos_sent,
                                           'negative':neg_sent}}

            with open('{}/{}'.format(str(NEW_DATADIR),str(f)),'w', encoding='utf-8') as f_out:
                json.dump(concept_new, f_out, ensure_ascii=False, indent=4)
    shutil.copy('{}/concept_list.csv'.format(DATADIR['root']),NEW_DATADIR.parent)


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-download_data', 
                        '--download_data', 
                        default='None',
                        type=str, 
                        help='download data mode.', 
                        required=False)
    parser.add_argument('-mode', 
                        '--mode', 
                        default='en_COUN',
                        type=str, 
                        help='download data mode.', 
                        required=False)
    parser.add_argument('-lang', '--lang', default='en',type=str, help='language.', required=False)
    parser.add_argument('-coun', '--coun', default='US',type=str, help='country.', required=False)
    args=parser.parse_args()
    return args

if __name__ == '__main__':
  args= get_arguments()
  download_data=args.download_data
  mode=args.mode
  dataget= getData()
  if download_data=='ALL' and mode!='TOPIC':
    dataget.download_data(mode)
  if download_data=='MULTILING' and 'LANG_COUN' in str(mode):
    dataget.download_mling(mode)
  if download_data=='SINGLE':
    dataget.download_single(mode,args.lang, args.coun)
  if download_data=='TOPIC' and mode=='en_US':
    dataget.download_topic(mode)
  if download_data=='NONE' and mode=='CONSTRACT':
    print(mode)
    dataget.constract_dataset()
    


# python getData.py -download_data \
#   -mode 'en_COUN'