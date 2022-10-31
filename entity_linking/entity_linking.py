from wikidata.client import Client
import json
import csv
from collections import defaultdict
import numpy as np
import pickle
from pathlib import Path
import pathlib
import os
import pandas as pd
import argparse
from log import logger
import shutil
os.environ['KMP_DUPLICATE_LIB_OK']='True'






            
            
class entityLinking:
    def __init__(self, DICT_DIR='../MAP_DICTS'):
        self.client = Client()
        self.DICT_DIR = DICT_DIR
        self.country_dict, \
        self.country_dict_r, \
        self.c2code, self.code2c, \
        self.d, self.place2country, \
        self.id2geo = self.load_dicts(self.DICT_DIR)
        print('country_dict:', self.country_dict[list(self.country_dict.keys())[0]])
        print('country_dict_r:',self.country_dict_r[list(self.country_dict_r.keys())[0]])
        print('c2code:',self.c2code[list(self.c2code.keys())[0]])
        print('code2c:',self.code2c[list(self.code2c.keys())[0]])
        self.to_check=False
        self.to_continue=False
        self.countries_to_check = []
        self.count=0
        
    def load_dicts(self,DICT_DIR='../MAP_DICTS'):
        self.DICT_DIR = DICT_DIR
        try:
            # with open(Path(DICT_DIR,'country_dict.json')) as inp:
            #     lines = inp.read()
            # country_dict = json.loads(lines)
            country_dict = self.json_load(DICT_DIR,'country_dict.json')
        except:
            country_dict = self.load_alt('country_dict.json')
        #except:
        #    country_dict = {}
        #try:
        try:
            # with open(Path(DICT_DIR,'country_dict_r.json')) as inp:
            #     lines = inp.read()
            # country_dict_r = json.loads(lines)
            country_dict_r = self.json_load(DICT_DIR,'country_dict_r.json')
        except:
            country_dict_r = self.load_alt('country_dict_r.json')


        c2code = {}
        code2c = {}
        with open(Path(DICT_DIR,"wikipedia-iso-country-codes.csv")) as f:
            file= csv.DictReader(f, delimiter=',')
            for line in file:
                c2code[line['English short name lower case']] = line['Alpha-3 code']  
                code2c[line['Alpha-3 code']] = line['English short name lower case']
        
        try:
            json_name = 'all_d.json'
            logger.info(Path(DICT_DIR,json_name))
            d = self.json_load(DICT_DIR,'all_d.json')
        except:
            d = self.load_alt('all_d.json')
        
        try:
            # with open(Path(DICT_DIR,'place2country.json')) as inp:
            #     lines = inp.read()
            # place2country = json.loads(lines)
            place2country = self.json_load(DICT_DIR,'place2country.json')
            #place2country = {}
        except:
            place2country = self.load_alt('place2country.json')

        try:
            # with open(Path(DICT_DIR,'id2geo.json')) as inp:
            #     lines = inp.read()
            # id2geo = json.loads(lines)
            id2geo = self.json_load(DICT_DIR,'id2geo.json')
        except:
            id2geo = self.load_alt('id2geo.json')

        #id2geo = {}
        return country_dict, country_dict_r, c2code, code2c, d, place2country, id2geo

    def load_alt(self,name, dirs='../MAP_DICTS'):
        try:
            logger.info(Path(dirs,name))
            with open(Path(dirs,name),'r', encoding='utf-8') as inp:
                json_file = json.load(inp)
        except:
            json_file={}
        return json_file

    def json_load(self,dirs,name):
        logger.info(Path(dirs,name))
        with open(Path(dirs,name),'r', encoding='utf-8') as inp:
            json_file = json.load(inp)
        return json_file

    
    def draw_fig(self):
        '''
        #fig = px.choropleth(df, 
        fig = go.Figure(data=go.Choropleth(
                locations=df["iso_alpha"],
                z=df["log_counts"], # lifeExp is a column of gapminder
                text=df["text"], # column to add to hover information
                #colorscale="Viridis",
                colorscale="Reds",
                marker_line_color='black',
                marker_line_width=0.5,
                colorbar_title = 'log(#entities)',
                ))
        fig.update_layout(title_text=f'Geographic Coverage: TREx-{LANG}', 
            geo=dict(
            showframe=True,
            showcoastlines=True,
            projection_type='natural earth'
        ))
        fig.write_image(f"plots/TREx-{LANG}.png")
        fig.show()
        '''



    #================================================
        LANG="en"
        fig = go.Figure(data=go.Scattergeo(
                locations=df["iso_alpha"],
                #size=df["log_counts"], # lifeExp is a column of gapminder
                text=df["text"], # column to add to hover information
                #colorscale="Viridis",
                mode = 'markers',
                marker_color = df['log_counts'],

                marker_size = df["log_counts"],
                #marker_sizemin = 6,
                marker_colorscale="Bluered",
                marker_sizeref = 0.08,
                #marker_line_color='black',
                #marker_line_width=0.5,
                marker_colorbar_title = 'log(#entities)',
                marker_colorbar_ticktext = [0,10,100,1000],
                ))
        fig.update_layout(title_text=f'Geographic Coverage: tydiqa-{LANG}', 
            geo=dict(
            showframe=True,
            showcoastlines=True,
            showcountries=True,
            projection_type='natural earth'
        ))
        fig.write_image(f"plots/tydiqa-{LANG}.scatter.png")
        fig.show()
    #=================================================   
    
    def get_name(self,ent):
        if str(ent).count("\'") == 2:
            return str(ent)[str(ent).find("\'")+1:str(ent).rfind("\'")]
        elif str(ent).count('\"') == 2:
            return str(ent)[str(ent).find("\"")+1:str(ent).rfind("\"")]
    
    def check_flag(self,l):
        codes_to_check = [self.country_dict_r[ccc] for ccc in self.countries_to_check]
        if 'country' in self.d[l]:
            if self.d[l]['country'] in codes_to_check:
                self.to_check=True
        if 'citizen' in self.d[l]:
            if self.d[l]['citizen'] in codes_to_check:
                self.to_check=True
        if 'born' in self.d[l]:
            if self.d[l]['born'] in codes_to_check:
                self.to_check=True
        if 'died' in self.d[l]:
            if self.d[l]['died'] in codes_to_check:
                self.to_check=True
    def check_continue(self, key):
        if 'country' in self.id2geo[key]:
            if self.id2geo[key]['country'] in self.countries_to_check:
                self.to_continue=False
        if 'citizen' in self.id2geo[key]:
            if self.id2geo[key]['citizen'] in self.countries_to_check:
                self.to_continue=False
        if 'born' in self.id2geo[key]:
            if self.id2geo[key]['born'] in self.countries_to_check:
                self.to_continue=False
        if 'died' in self.id2geo[key]:
            if self.id2geo[key]['died'] in self.countries_to_check:
                self.to_continue=False
        return self.to_continue
                
    def entity_define(self, entity, key, l):
        if key.id == 'P31':
            #print(f'instance of: {entity[key].id}')
            #print(key.id, entity[key])
            if entity[key].id == 'Q5':
                #print('\thuman')
                self.d[l]['instance'] = 'human'
            elif entity[key].id == 'Q515':
                #print('\tcity')
                self.d[l]['instance'] = 'city'
            elif entity[key].id == 'Q6256':
                #print('\tcountry')
                self.d[l]['instance'] = 'country'
        if key.id in 'P27,P19,P20,P17,P1376,P625,P69,P276,P495,P159'.split(','):
            #print(key.id, entity[key])
            if key.id == 'P17':
                #print(f'\tcountry: {entity[key].id}')
                self.d[l]['country'] = entity[key].id
            elif key.id == 'P20':
                #print(f'\tdied in: {entity[key].id}')
                self.d[l]['died'] = entity[key].id
            elif key.id == 'P19':
                #print(f'\tborn in: {entity[key].id}')
                self.d[l]['born'] = entity[key].id
            elif key.id == 'P27':
                #print(f'\tcitizen of: {entity[key].id}')
                self.d[l]['citizen'] = entity[key].id
            elif key.id == 'P69':
                #print(f'\teducated at: {entity[key].id}')
                self.d[l]['educated'] = entity[key].id
            elif key.id == 'P276':
                #print(f'\tlocated at: {entity[key].id}')
                self.d[l]['located'] = entity[key].id
            elif key.id == 'P159':
                #print(f'\theadquartered at: {entity[key].id}')
                self.d[l]['headquartered'] = entity[key].id
            elif key.id == 'P495':
                #print(f'\toriginated from: {entity[key].id}')
                self.d[l]['from'] = entity[key].id
            elif key.id == 'P1376':
                #print(f'\tcapital of: {entity[key].id}')
                self.d[l]['capital'] = entity[key].id
            elif key.id == 'P625':
                #print(f'\tcoordinates: {entity[key]}')
                temp = str(entity[key]).split('(')[1]
                latitude = float(temp.split(',')[0])
                longtidute = float(temp.split(',')[1])
                self.d[l]['coordinates'] = (latitude,longtidute)
                
    def if_country(self,key):
        if self.d[key]['country'] in self.country_dict:
            print(f"{key}\t{self.d[key]['name']}\tcountry:{self.country_dict[self.d[key]['country']]}")
            if key not in self.id2geo:
                self.id2geo[key] = {}
            self.id2geo[key]['name'] = self.d[key]['name']
            self.id2geo[key]['country'] = self.country_dict[self.d[key]['country']]
        else:
            country = self.client.get(self.d[key]['country'], load=True)
            country_name = self.get_name(country)
            print(f"{key}\t{self.d[key]['name']}\tcountry:{country_name}")
            self.country_dict[country.id] = country_name
            self.country_dict_r[country_name] = country.id
            self.count += 1
            if key not in self.id2geo:
                self.id2geo[key] = {}
            self.id2geo[key]['name'] = self.d[key]['name']
            self.id2geo[key]['country'] = country_name
            
    def if_citizen(self, key):
        if self.d[key]['citizen'] in self.country_dict:
            print(f"{key}\t{self.d[key]['name']}\tcitizen:{self.country_dict[self.d[key]['citizen']]}")    
            if key not in self.id2geo:
                self.id2geo[key] = {}
            self.id2geo[key]['name'] = self.d[key]['name']
            self.id2geo[key]['citizen'] = self.country_dict[self.d[key]['citizen']]
        else:
            place = self.client.get(self.d[key]['citizen'], load=True)
            country_name = self.get_name(place)
            print(f"{key}\t{self.d[key]['name']}\tcitizen:{country_name}")
            self.country_dict[place.id] = country_name
            self.country_dict_r[country_name] = place.id
            self.count += 1
            if key not in self.id2geo:
                self.id2geo[key] = {}
            self.id2geo[key]['name'] = self.d[key]['name']
            self.id2geo[key]['citizen'] = country_name
    
    def if_born(self,key):
        if self.d[key]['born'] in self.place2country:
            print(f"{key}\t{self.d[key]['name']}\tborn:{self.place2country[self.d[key]['born']]['country']}")
            if key not in self.id2geo:
                self.id2geo[key] = {}
            self.id2geo[key]['name'] = self.d[key]['name']
            self.id2geo[key]['born'] = self.place2country[self.d[key]['born']]['country']
        else:
            if self.d[key]['born']=='Q2042400':
                print('')
            place = self.client.get(self.d[key]['born'], load=True)
            for key2 in place.keys():
                if key2.id == 'P17':
                    try:
                        countryid = place[key2].id
                    except:
                        print(key2, key, self.d[key], place)
                        continue
                    if countryid in self.country_dict:
                        print(f"{key}\t{self.d[key]['name']}\tborn:{self.country_dict[countryid]}")
                        if key not in self.id2geo:
                            self.id2geo[key] = {}
                        self.id2geo[key]['name'] = self.d[key]['name']
                        self.id2geo[key]['born'] = self.country_dict[countryid]
                        self.place2country[self.d[key]['born']] = {}
                        self.place2country[self.d[key]['born']]['name'] = self.get_name(place)
                        self.place2country[self.d[key]['born']]['country'] = self.country_dict[countryid]
                    else:
                        country = self.client.get(countryid, load=True)
                        country_name = self.get_name(country)
                        print(f"{key}\t{self.d[key]['name']}\tborn:{country_name}")
                        self.country_dict[country.id] = country_name
                        self.country_dict_r[country_name] = country.id
                        self.place2country[self.d[key]['born']] = {}
                        self.place2country[self.d[key]['born']]['name'] = self.get_name(place)
                        self.place2country[self.d[key]['born']]['country'] = country_name
                        self.count += 1
                        if key not in self.id2geo:
                            self.id2geo[key] = {}
                        self.id2geo[key]['name'] = self.d[key]['name']
                        self.id2geo[key]['born'] = country_name
    def if_died(self,key):
        if self.d[key]['died'] in self.place2country:
            print(f"{key}\t{self.d[key]['name']}\tdied:{self.place2country[self.d[key]['died']]['country']}")
            if key not in self.id2geo:
                self.id2geo[key] = {}
            self.id2geo[key]['name'] = self.d[key]['name']
            self.id2geo[key]['died'] = self.place2country[self.d[key]['died']]['country']
        else:
            place = self.client.get(self.d[key]['died'], load=True)
            for key2 in place.keys():
                if key2.id == 'P17':
                    try:
                        countryid = place[key2].id
                    except:
                        print(key2, key, self.d[key], place)
                        continue
                    if countryid in self.country_dict:
                        print(f"{key}\t{self.d[key]['name']}\tdied:{self.country_dict[countryid]}")
                        if key not in self.id2geo:
                            self.id2geo[key] = {}
                        self.id2geo[key]['name'] = self.d[key]['name']
                        self.id2geo[key]['died'] = self.country_dict[countryid]
                        self.place2country[self.d[key]['died']] = {}
                        self.place2country[self.d[key]['died']]['name'] = self.get_name(place)
                        self.place2country[self.d[key]['died']]['country'] = self.country_dict[countryid]
                    else:
                        country = self.client.get(countryid, load=True)
                        country_name = self.get_name(country)
                        print(f"{key}\t{self.d[key]['name']}\tdied:{country_name}")
                        self.country_dict[country.id] = country_name
                        self.country_dict_r[country_name] = country.id
                        self.place2country[self.d[key]['died']] = {}
                        self.place2country[self.d[key]['died']]['name'] = self.get_name(place)
                        self.place2country[self.d[key]['died']]['country'] = country_name
                        self.count += 1
                        if key not in self.id2geo:
                            self.id2geo[key] = {}
                        self.id2geo[key]['name'] = self.d[key]['name']
                        self.id2geo[key]['died'] = country_name
                  
                        
    def country_mapping(self, lang_entities):
        from urllib.request import urlopen
        #with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        #    counties = json.load(response)

        #print(counties["features"][0])

        

        # import plotly.express as px
        # import plotly.graph_objects as go

        country_list = list(self.c2code.keys())
        iso_list = [self.c2code[c] for c in country_list]
        # print(len(country_list))
        # print(country_list)
        # print(iso_list)

        mapping = {}
        mapping['United States of America'] = 'United States'
        mapping["People's Republic of China"] = 'China'
        mapping["The Bahamas"] = 'Bahamas'
        mapping["Ivory Coast"] = "Côte d'Ivoire"
        mapping["Democratic Republic of the Congo"] = "D.R. Congo"
        mapping["Republic of the Congo"] = 'Congo'
        mapping["Dutch East Indies"] = 'Netherlands Antilles'
        mapping["Russian Republic"] = 'Russian Federation'
        mapping["The Gambia"] = 'Gambia'
        mapping["England"] = 'United Kingdom'
        mapping["Scotland"] = 'United Kingdom'
        mapping["Wales"] = 'United Kingdom'
        mapping["East Timor"] = 'Timor-Leste'
        mapping["North Macedonia"] = 'Macedonia'
        mapping["People's Republic of Angola"] = 'Angola'
        mapping["State of Palestine"] = 'Palestine'
        mapping["Federated States of Micronesia"] = 'Micronesia'
        mapping["Democratic Republic of Georgia"] = 'Georgia'
        mapping["Great Britain"] = 'United Kingdom'
        mapping["United Kingdom of Great Britain and Ireland"] = 'United Kingdom'
        mapping["Russia"] = 'Russian Federation'
        mapping["Laos"] = "Lao People's Democratic Republic"
        mapping["São Tomé and Príncipe"] = 'Sao Tome and Principe'
        mapping["Mongolian People's Republic"] = 'Mongolia'
        mapping["Sahrawi Arab Democratic Republic"] = 'Western Sahara'
        mapping["Serbia and Montenegro"] = 'Serbia'
        mapping["Somaliland"] = 'Somalia'
        mapping["Palestinian territories"] = 'Palestine'
        mapping["Northern Ireland"] = 'United Kingdom'
        mapping["Vatican City"] = 'Holy See'
        mapping["Czech REpublic"] = 'Czech Republic'
        mapping["AustriA"] = 'Austria'
        mapping["LIthuania"] = 'Lithuania'
        mapping[""] = ''
        mapping[""] = ''


        # for key in self.country_dict_r:
        #     if key in country_list:
        #         logger.info(f"found! {key}")
        #         if key in self.c2code:
        #             logger.info(f"\talso found ISO code: {self.c2code[key]}")
        #         else:
        #             logger.info(f"\tdid not find ISO code: {key}")
        #     elif key in mapping:
        #         if mapping[key] in country_list:
        #             logger.info(f"found! {mapping[key]}")
        #             if mapping[key] in self.c2code:
        #                 logger.info(f"\talso found ISO code (map): {self.c2code[mapping[key]]}")
        #             else:
        #                 logger.info(f"\tdid not find ISO code (map): {mapping[key]}")
        #     else:
        #         logger.info(f"not! {key}")

        self.dataset_counts = defaultdict(lambda:0)
        for key in lang_entities:
            if key in self.id2geo:
                name = self.id2geo[key]['name']
                if 'country' in self.id2geo[key] or 'citizen' in self.id2geo[key]:
                    if 'country' in self.id2geo[key]:
                        country = self.id2geo[key]['country']
                    else:
                        country = self.id2geo[key]['citizen']
                    #print(country)
                    if country in mapping:
                        country = mapping[country]
                    if country in self.c2code:
                        code = self.c2code[country]
                        self.dataset_counts[code] += 1
                if 'born' in self.id2geo[key]:
                    #print("BORN: ", id2geo[key]['born'])
                    born = self.id2geo[key]['born']
                    if born in mapping:
                        born = mapping[born]
                    if born in self.c2code:
                        code = self.c2code[born]
                        self.dataset_counts[code] += 1
                if 'died' in self.id2geo[key]:
                    #print("DIED: ", id2geo[key]['died'])
                    died = self.id2geo[key]['died']
                    if died in mapping:
                        died = mapping[died]
                    if died in self.c2code:
                        code = self.c2code[died]
                        self.dataset_counts[code] += 1

        codes = list(self.code2c.keys())
        # print(codes)
        # print(self.dataset_counts)
        #logcounts = [np.log10(self.dataset_counts[c]) for c in codes]
        logcounts = []
        for c in codes:
            if self.dataset_counts[c]>0:
                logcounts.append(np.log10(self.dataset_counts[c]))
            else:
                logcounts.append(0)
        counts = [self.dataset_counts[c] for c in codes]
        sqrtcounts = np.sqrt(counts)
        #print(counts)
        names = [self.code2c[c] for c in codes]
        #print(names)
        texts = [f"{names[i]}<br>#entities: {counts[i]}" for i in range(len(codes))]

        df = pd.DataFrame({'iso_alpha': codes, 
        'country':names, 'counts':counts, 
        'log_counts':logcounts, 
        'text':texts, 
        'sqrt_counts':sqrtcounts})
#         df.to_csv(f'tydiqa_count_csvs/tydiqa-{LANG}.csv')


    def save_file(self, DATADIR, BASENAME, mode):
        FILEPATH = Path(DATADIR, '{}_dist.csv'.format(mode))
        if FILEPATH.is_file():
            print ("File exist")
            save_df = pd.read_csv(FILEPATH,index_col=[0])
            print(save_df)
            save_df['index']=save_df.index
            save_df[BASENAME]=save_df.apply(lambda row:self.dataset_counts[row['index']],axis=1)
            save_df = save_df.drop('index', axis=1)
            save_df.to_csv(FILEPATH)
            print(f"updated file at{FILEPATH}")
        else:
            print ("File not exist")
            save_df =pd.DataFrame.from_dict(self.dataset_counts, columns=[BASENAME],orient='index')
            save_df.to_csv(FILEPATH)
            print(f"saved file at{FILEPATH}")

    def json_dump(self,DIR,fname,dname):
        with open(Path(DIR,fname), 'w', encoding='utf-8') as f:
            json.dump(dname, f, ensure_ascii=False)

                
    def link_enity(self,DATAFILE, DATADICT, dtype='file'):
        if dtype=='file':
            print(DATAFILE)
            with open(DATAFILE, 'rb') as inp:
                lines = pickle.load(inp)
        else:
            print(DATAFILE[:3])
            lines=DATAFILE
        lang_entities = []
        countc = 0
        for k in lines:
            for lec,kk in enumerate(k):
                if lec>10:
                    break
                try:
                    # l = k[0]['id']
                    l=kk['id']
                except:
                    continue
                countc += 1
                #l = l.strip().split('\t')[0]
                lang_entities.append(l)
                self.to_check = False
                
                if l in self.d:
                    self.check_flag(l)
                    
                if (l not in self.d) or self.to_check:
                    try:
                        entity = self.client.get(l, load=True)
                    except:
                        lang_entities.remove(l)
                        continue
                    name = self.get_name(entity)
                    self.d[l] = {}
                    self.d[l]['name'] = name
                    for key in entity.keys():
                        try:
                            self.entity_define(entity, key, l)
                        except:
                            pass
                if countc == 100:
                    countc = 0
                    json_name = DATADICT
                    with open(json_name, 'w', encoding='utf-8') as f:
                        json.dump(self.d, f, ensure_ascii=False)
                    # jsonString = json.dumps(self.d)
                    # print(json_name)
                    # with open(json_name, 'w') as op:
                    #     op.write(jsonString)

        new_d = {}
        for l in lang_entities:
            try:
                new_d[l] = self.d[l]
            except:
                continue
        # print(new_d)

        # jsonString = json.dumps(self.d)
        # json_name = DATADICT
        # with open(json_name, 'w') as op:
        #     op.write(jsonString)
        json_name = DATADICT
        with open(json_name, 'w', encoding='utf-8') as f:
            json.dump(self.d, f, ensure_ascii=False)

# #         jsonString = json.dumps(new_d)
# #         json_name = f"tydiqa_data/{LANG}_d.json"
# #         with open(json_name, 'w') as op:
# #             op.write(jsonString)

        self.d = new_d

        print("************************")
        
        self.count = 0
        count2 = 0
        for key in lang_entities:
            count2 += 1
            if key in self.id2geo:
                self.to_continue = True
                if self.check_continue(key)==True:
                    continue
            if 'country' in self.d[key]:
                print('>found country')
                self.if_country(key)
            if 'citizen' in self.d[key]:
                print('>found citizen')
                self.if_citizen(key)
            if 'born' in self.d[key]:
                print('>found born')
                self.if_born(key)
            if 'died' in self.d[key]:
                print('>found born')
                self.if_died(key)
            
            if self.count == 50:
                # jsonString = json.dumps(self.country_dict)
                # with open(Path(self.DICT_DIR,"country_dict.json"), 'w') as op:
                #     op.write(jsonString)
                # json_name = DATADICT
                self.json_dump(self.DICT_DIR,"country_dict.json",self.country_dict)

                # jsonString = json.dumps(self.country_dict_r)
                # with open(Path(self.DICT_DIR,"country_dict_r.json"), 'w') as op:
                #     op.write(jsonString)

                self.json_dump(self.DICT_DIR,"country_dict_r.json",self.country_dict_r)

                # jsonString = json.dumps(self.id2geo)
                # with open(Path(self.DICT_DIR,"id2geo.json"), 'w') as op:
                #     op.write(jsonString)

                self.json_dump(self.DICT_DIR,"id2geo.json",self.id2geo)

                # jsonString = json.dumps(self.place2country)
                # with open(Path(self.DICT_DIR,"place2country.json"), 'w') as op:
                #     op.write(jsonString)
                self.json_dump(self.DICT_DIR,"place2country.json",self.place2country)


                self.count = 0
            if count2 == 50:
                self.json_dump(self.DICT_DIR,"id2geo.json",self.id2geo)

                # jsonString = json.dumps(self.id2geo)
                # with open(Path(self.DICT_DIR,"id2geo.json"), 'w') as op:
                #     op.write(jsonString)
                count2 = 0



        # jsonString = json.dumps(self.country_dict)
        # with open(Path(self.DICT_DIR,"country_dict.json"), 'w') as op:
        #     op.write(jsonString)

        self.json_dump(self.DICT_DIR,"country_dict.json",self.country_dict)

        # jsonString = json.dumps(self.country_dict_r)
        # with open(Path(self.DICT_DIR,"country_dict_r.json"), 'w') as op:
        #     op.write(jsonString)

        self.json_dump(self.DICT_DIR,"country_dict_r.json",self.country_dict_r)

        # jsonString = json.dumps(self.id2geo)
        # with open(Path(self.DICT_DIR,"id2geo.json"), 'w') as op:
        #     op.write(jsonString)

        self.json_dump(self.DICT_DIR,"id2geo.json",self.id2geo)

        # jsonString = json.dumps(self.place2country)
        # with open(Path(self.DICT_DIR,"place2country.json"), 'w') as op:
        #     op.write(jsonString)

        self.json_dump(self.DICT_DIR,"place2country.json",self.place2country)
            
        self.country_mapping(lang_entities)
# #         self.draw_fig()


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
    parser.add_argument("--key_file", type=pathlib.Path, required=False)
    parser.add_argument("--out_dir", type=pathlib.Path, required=False)
    args=parser.parse_args()
    return args        

    
if __name__ == '__main__':
    args= get_arguments()
    DATAFILE=args.data_file
    mode=args.mode
    DICT_DIR='/projects/antonis/fahim/ner_linking/MAP_DICTS'
    # DATAFILE=f"/Users/faisal/a/projects/ner_linking/data/geoloc/AU-en/concept/entity/AU_en_AR.pickle"
    DATADICT=f"/projects/antonis/fahim/ner_linking/MAP_DICTS/all_d.json"
    print(args)
    print(DATAFILE)
    print(DICT_DIR)
    print(DATADICT)
    DATADIR = Path(DATAFILE).parent.parent
    BASENAME = Path(DATAFILE).name.split('.')[0]
    print(DATADIR, BASENAME)

    Dict_dest = Path(DATAFILE.parent.parent, 'MAP_DICTS')
    if not Dict_dest.is_dir():
        Dict_dest.mkdir(parents=True, exist_ok=True)
        for f in os.listdir(DICT_DIR):
            print(f"dict_dir:{f}, Dict_dest={Dict_dest}")
            src_path = Path(DICT_DIR,f)
            dest_path = Path(Dict_dest,f)
            shutil.copy(src_path, dest_path)
    else:
        print(f'Dict_dest:{Dict_dest} exists')
    DICT_DIR = Dict_dest
    DATADICT = Path(DICT_DIR,'all_d.json')
    print(f'updated datadict path:{DATADICT}')


    if mode=='concept':
        elink = entityLinking(DICT_DIR)
        elink.link_enity(DATAFILE, DATADICT, 'file')
        elink.save_file(DATADIR, BASENAME, mode)
    else:
        KEYFILE=str(DATAFILE).replace('/entity/','/key/')

        print('KEYFILE',KEYFILE)
        with open(KEYFILE, 'rb') as inp:
                keys = pickle.load(inp)
        with open(DATAFILE, 'rb') as inp:
                lines = pickle.load(inp)
        all_keys = set(keys)
        for key in all_keys:
            FILEPATH = Path(DATADIR, '{}_dist.csv'.format(mode))
            if FILEPATH.is_file():
                print ("File exist")
                save_df = pd.read_csv(FILEPATH,index_col=[0])
                if BASENAME+'#'+key in save_df.columns:
                    print(f'{BASENAME}#{key} already in dataframe {FILEPATH}')
                else:
                    select_lines =  [a for i, a in zip(keys, lines) if i==key]
                    select_lines = select_lines[:30]
                    print(BASENAME,key,len(select_lines))
                    elink = entityLinking(DICT_DIR)
                    elink.link_enity(select_lines, DATADICT, 'list')
                    elink.save_file(DATADIR, BASENAME+'#'+key, mode)
            else:
                select_lines =  [a for i, a in zip(keys, lines) if i==key]
                select_lines = select_lines[:30]
                print(BASENAME,key,len(select_lines))
                elink = entityLinking(DICT_DIR)
                elink.link_enity(select_lines, DATADICT, 'list')
                elink.save_file(DATADIR, BASENAME+'#'+key, mode)




                  
    
