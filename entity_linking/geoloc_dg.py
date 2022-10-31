from genre.fairseq_model import mGENRE
import pickle
from genre.trie import Trie, MarisaTrie
import sys
import pickle
import os
import subprocess
import multiprocessing
import itertools
from log import logger
import argparse
import json
import pathlib
from pathlib import Path


    # sentences = sentences[:3]



def ParallelExtractDir(sentence):
    try:
        news=[sentence]
        one = model.sample(
                news,
                prefix_allowed_tokens_fn=lambda batch_id, sent: [
                    e for e in trie.get(sent.tolist()) if e < len(model.task.target_dictionary)
                ],
                text_to_id=lambda x: max(lang_title2wikidataID[tuple(reversed(x.split(" >> ")))], key=lambda y: int(y[1:])),
                marginalize=True,
            )
        return one[0]
    except IndexError:
        logger.info(news)
        return ''




def check_out(name, out_root='/scratch/ffaisal/ner_linking'):
    result = False
    for x in os.listdir(out_root):
        discarded = ['.DS_Store']
        if name==str(x[:-7]):
            result= True
            break
        else:
            result= False
    return result


def do_operation(sentences):
    p = multiprocessing.Pool(12)
    alls = p.map(ParallelExtractDir, sentences)

    with open('/scratch/ffaisal/ner_linking/{}.pickle'.format(name),'wb') as f:
        pickle.dump(alls, f)


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-mode', 
                        '--mode', 
                        default='en_COUN',
                        type=str, 
                        help='download data mode.', 
                        required=False)
    parser.add_argument('-name', 
                        '--name', 
                        default='en_COUN',
                        type=str, 
                        help='download data mode.', 
                        required=False)
    parser.add_argument("--data_file", type=pathlib.Path, required=False)
    parser.add_argument("--out_dir", type=pathlib.Path, required=False)
    args=parser.parse_args()
    return args


if __name__ == "__main__":
    # ./geoloc_dg.sh /scratch/ffaisal/ml-selfcond/data/dataset-en_COUN-TOPIC-100/sense ../data/geoloc concept 
    args= get_arguments()
    datafile=args.data_file
    out_dir=args.out_dir
    mode=args.mode
    name=args.name

    
    print(out_dir)
    print(mode)
    print(name)


    if str(datafile).split('/')[-2]=='sense':
        dataname = str(datafile).split('/')[-3]
        savedir = pathlib.Path(out_dir,dataname, 'concept', 'entity')
    else:
        savedir = pathlib.Path(out_dir, 'entity')
    savedir.mkdir(exist_ok=True, parents=True)



    # datafile = str(sys.argv[1])
    # name=str(sys.argv[2])
    if check_out(name, savedir)==True:
        logger.info('file exist')
    else:
        if str(datafile).endswith('.pickle'):
            with open(datafile,'rb') as f:
                sentences =  pickle.load(f)
        elif str(datafile).endswith('.json'):
            with open(datafile,'r') as f:
                data=json.load(f)
            sentences = data["sentences"]["positive"]
        logger.info(sentences)

        logger.info('{} file loaded'.format(name))
        model_mlpath = '../models/fairseq_multilingual_entity_disambiguation'
        model = mGENRE.from_pretrained(model_mlpath).eval()
        logger.info('model loaded')
        with open("../models/titles_lang_all105_marisa_trie_with_redirect.pkl", "rb") as f:
            trie = pickle.load(f)
        logger.info('trie loaded')

        with open("../models/lang_title2wikidataID-normalized_with_redirect.pkl", "rb") as f:
            lang_title2wikidataID = pickle.load(f)
        logger.info('wikimap loaded')
        # do_operation(sentences)




        if str(name).endswith('.pickle') or str(name).endswith('.json'):
            name = name.replace('.pickle','')
            name = name.replace('.json','')
            temp_path = savedir / '{}-temp.pickle'.format(name)
            out_path = savedir / '{}.pickle'.format(name)
        else:
            temp_path = savedir / '{}-temp.pickle'.format(name)
            out_path = savedir / '{}.pickle'.format(name)
        left_sent = []
        if os.path.exists(temp_path)==True:
            with open(temp_path,'rb') as f:
                done_sent =  pickle.load(f)
            left_sent = sentences[len(done_sent):]
            sent_save=done_sent
        else:
            left_sent = sentences
            sent_save = []
        logger.info('left sent:{}, done_sent:{}'.format(len(left_sent),len(sent_save)))


        for i in range(0,len(left_sent),200):
            try:
                news=left_sent[i:i+200]
                one = model.sample(
                        news,
                        prefix_allowed_tokens_fn=lambda batch_id, sent: [
                            e for e in trie.get(sent.tolist()) if e < len(model.task.target_dictionary)
                        ],
                        text_to_id=lambda x: max(lang_title2wikidataID[tuple(reversed(x.split(" >> ")))], key=lambda y: int(y[1:])),
                        marginalize=True,
                    )
                sent_save.extend(one)
            except Exception as err:
                for k,sent in enumerate(news):
                    try:
                        news1=[sent]
                        one = model.sample(
                                news1,
                                prefix_allowed_tokens_fn=lambda batch_id, sent: [
                                    e for e in trie.get(sent.tolist()) if e < len(model.task.target_dictionary)
                                ],
                                text_to_id=lambda x: max(lang_title2wikidataID[tuple(reversed(x.split(" >> ")))], key=lambda y: int(y[1:])),
                                marginalize=True,
                            )
                        sent_save.append(one[0])
                    except Exception as err1:
                        logger.info(news1)
                        sent_save.append('')

                logger.info('error:-------------------------{}-{}'.format(i,i+200))
            if i%200==0:
                logger.info('total done: {}, left:{}'.format(len(sent_save), len(left_sent)-i))
                with open(temp_path,'wb') as f:
                    pickle.dump(sent_save, f)        

        with open(out_path,'wb') as f:
            pickle.dump(sent_save, f)
        
        if os.path.isfile(temp_path):
            os.remove(temp_path)

        print(sent_save)


