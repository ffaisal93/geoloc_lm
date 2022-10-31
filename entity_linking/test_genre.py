from genre.fairseq_model import mGENRE
import pickle
from genre.trie import Trie, MarisaTrie
import sys
import pickle
import os
import subprocess
import multiprocessing
import itertools

    # sentences = sentences[:3]


# model_mlpath = '../models/fairseq_multilingual_entity_disambiguation'
# model = mGENRE.from_pretrained(model_mlpath).eval()
# print('model loaded')

# with open("../models/titles_lang_all105_marisa_trie_with_redirect.pkl", "rb") as f:
#     trie = pickle.load(f)

# print('trie loaded')

# with open("../models/lang_title2wikidataID-normalized_with_redirect.pkl", "rb") as f:
#     lang_title2wikidataID = pickle.load(f)

#sentences = ["Dkt [START] Geoffrey William Griffin [END] aliandika vitabu vingapi?"]
# sentences = ["[START] Einstein [END] era un fisico tedesco."]


# sentences  = ['Wizara ya afya ya [START] Tanzania [END] imeripoti [START] Jumatatu [END] kuwa , watu takriban 14 zaidi wamepata maambukizi ya Covid - 19 .', 
# 'Walioambukizwa wote ni raia wa [START] Tanzania [END] , 13 wakiwa [START] Dar - es - salaam [END] na mmoja mjini [START] Arusha [END] .', 
# 'Wizara ya afya imeripoti kwamba juhudi za kufuatilia watu waliokuwa karibu na wagonjwa zinaendelea .']




# x=model.sample(
#     sentences,
#     prefix_allowed_tokens_fn=lambda batch_id, sent: [
#         e for e in trie.get(sent.tolist()) if e < len(model.task.target_dictionary)
#     ],
# )

# getting predictions
# x=0



# alls=[]
# for aa in sentences:
#     try:
#         news=[aa]
#         # news= ['በምርጫው እንደማይወዳደሩ ቀደም ሲል ካስታወቁ በኋላ ፓርቲው በመጨረሻ ባካሄደው ጉባዔው [START] ዦዋዎ ሉሬንቾን [END] ቀዳሚው እጩ አድርጎ ሰይሟል ።']
#         one = model.sample(
#                 news,
#                 prefix_allowed_tokens_fn=lambda batch_id, sent: [
#                     e for e in trie.get(sent.tolist()) if e < len(model.task.target_dictionary)
#                 ],
#                 text_to_id=lambda x: max(lang_title2wikidataID[tuple(reversed(x.split(" >> ")))], key=lambda y: int(y[1:])),
#                 marginalize=True,
#             )
#         alls.append(one[0])
#     except IndexError:
#         print(news)


# with open('/scratch/ffaisal/ner_linking/{}.pickle'.format(name),'wb') as f:
#     pickle.dump(alls, f)


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
        print(news)
        return ''




def check_out(name):
    out_root  = '/scratch/ffaisal/ner_linking'
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


if __name__ == "__main__":
    datafile = str(sys.argv[1])
    name=str(sys.argv[2])
    if check_out(name)==True:
        print('file exist')
    else:
        with open(datafile,'rb') as f:
            sentences =  pickle.load(f)
        print('{} file loaded'.format(name))
        model_mlpath = '../models/fairseq_multilingual_entity_disambiguation'
        model = mGENRE.from_pretrained(model_mlpath).eval()
        print('model loaded')

        with open("../models/titles_lang_all105_marisa_trie_with_redirect.pkl", "rb") as f:
            trie = pickle.load(f)

        print('trie loaded')

        with open("../models/lang_title2wikidataID-normalized_with_redirect.pkl", "rb") as f:
            lang_title2wikidataID = pickle.load(f)
        # do_operation(sentences)






