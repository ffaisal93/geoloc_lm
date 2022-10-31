import pandas as pd
from scipy.spatial.distance import cosine
import os
import itertools
import argparse
import country_converter as coco
import networkx as nx
import plotly.graph_objs as go
from pathlib import Path
import networkx.algorithms.community as nx_comm
from langcodes import Language
import country_converter as coco
import plotly.express as px
p_colors = px.colors.sequential.Rainbow
from collections import Counter

DIRS={
    "gpt2":"gpt2-medium",
    "bloom":"bigscience/bloom-560m",
    "mgpt":"sberbank-ai/mGPT"
}

template={
    'dataset-en_COUN-TOPIC-100-fr':'US-fr',
    'dataset-en_COUN-TOPIC-100-zh':'US-zh',
    'dataset-en_COUN-TOPIC-100-ru':'US-ru',
    'dataset-en_COUN-TOPIC-100-bn':'US-bn',
    'dataset-en_COUN-TOPIC-100-ar':'US-ar',
    'dataset-en_COUN-TOPIC-100-hi':'US-hi',
    'dataset-en_COUN-TOPIC-100-el':'US-el',
    'dataset-en_COUN-TOPIC-100-ko':'US-ko',
    'dataset-en_COUN-TOPIC-100':'US-en',
#     'dataset-en_COUN-TOPIC-100':'US-en',
    'masked':'[M]',
    'random':'[R]',
    'bloom':'BLOOM',
    'mgpt':'mGPT',
    'gpt2':'GPT2',
    '-csim-all.csv':''
}

def iso_single(coun):
    iso_3 = coco.convert(coun, to='ISO3')
    return iso_3

def lang_3(lang):
    return Language.get(lang).to_alpha3()

class PLOT:
    def __init__(self,color="Peach"):
        self.G = nx.Graph()
        self.node_size={}
        self.title="title"
        self.color=color
        self.edge_trace=go.Scatter()
        self.node_trace=go.Scatter()
        self.fig = go.Figure()
        self.comm_fig = go.Figure()
    
    def create_graph(self,df,weight_col='jac'):
        ls = list(zip(df['c1'],df['c2'],df[weight_col]))
        self.G.add_weighted_edges_from(ls)
    
    def set_layout(self,name,iterations=500):
        if name=='spectral':
            pos = nx.spectral_layout(self.G,weight='weight')
        if name=='spring':
            pos = nx.spring_layout(self.G,weight='weight',iterations=iterations)
        if name=='planner':
            pos = nx.planar_layout(self.G)
        if name=='kamada':
            pos = nx.kamada_kawai_layout(self.G,weight='weight')
        if name=='multi':
            pos = nx.multipartite_layout(self.G)
        if name=='bi':
            pos = nx.bipartite_layout(self.G)
        for n, p in pos.items():
            self.G.nodes[n]['pos'] = p
    
    def set_nodesizes(self):
        for i,z in self.G.degree:
            self.node_size[i]=z
        return self.node_size
    
    def set_edge_trace(self):
        self.edge_trace = go.Scatter(
            x=[],
            y=[],
            line=dict(width=1, color='#FB4'),
            hoverinfo='none',
            mode='lines')
        weights=[]
        for edge in self.G.edges():
            x0, y0 = self.G.nodes[edge[0]]['pos']
            x1, y1 = self.G.nodes[edge[1]]['pos']
            self.edge_trace['x'] += tuple([x0, x1, None])
            self.edge_trace['y'] += tuple([y0, y1, None])
#             self.edge_trace['line']=dict(width=self.G[edge[0]][edge[1]]['weight']*50, color='#888')
    
    def set_node_trace(self, color_dict):
        self.node_trace = go.Scatter(
            x=[],
            y=[],
            text=[],
            mode='markers+text',
            hoverinfo='text',
            marker=dict(
                showscale=False,
                colorscale=self.color,
                opacity=0.3,
                reversescale=True,
                color=[],
                size=[],
                colorbar=dict(
                    thickness=1,
                    title='Node Connections',
                    xanchor='left',
                    titleside='right'
                ),
                line=dict(width=0))
        )
        for node in self.G.nodes():
            x, y = self.G.nodes[node]['pos']
            self.node_trace['x'] += tuple([x])
            self.node_trace['y'] += tuple([y])
            self.node_trace['marker']['size'] += tuple([self.node_size[node]*10])
            self.node_trace['marker']['color'] +=tuple([color_dict[node]])

        for node, adjacencies in enumerate(self.G.adjacency()):
            # self.node_trace['marker']['color'] += tuple([len(adjacencies[1])])
            node_info = adjacencies[0]
            self.node_trace['text'] += tuple([node_info])
    
    def draw_graph(self,title="Country Similarity",text=""):
        self.title=title
        print(title)
        self.fig = go.Figure(data=[self.edge_trace, self.node_trace],
                        layout=go.Layout(
                        title=self.title,
                        titlefont=dict(size=16),
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=2, r=2, t=40),
                        annotations=[dict(
                            text=text,
                            showarrow=False,
                            xref="paper", yref="paper")],
                        xaxis=dict(showgrid=False, zeroline=False,
                                showticklabels=False, mirror=True),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, mirror=True)))

        self.fig.update_layout({
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'paper_bgcolor': 'rgba(0,0,0,0)'
        })
        # self.save_graph(fname=f"{self.title}.pdf",IMAGE_DIR='./images')
        # self.fig.show()
        
    
    def show_graph(self):
        self.fig.show()
    
    def save_graph(self,fname="",is_comm = "no",IMAGE_DIR='./images'):
        print(IMAGE_DIR)
        if fname=="":
            fname=os.path.join(IMAGE_DIR,self.title.replace(" ","_")+".png")
        if not os.path.exists(IMAGE_DIR):
            os.mkdir(IMAGE_DIR)
        print(fname)
        if is_comm!="no":
            self.comm_fig.write_image(os.path.join(IMAGE_DIR,fname))
        else:
            self.fig.write_image(os.path.join(IMAGE_DIR,fname))

    def comm_draw(self, df):
        fig = go.Figure(data=go.Scattergeo(
                locations=df["ISO"],
                #size=df["log_counts"], # lifeExp is a column of gapminder
                text=df["ISO"], # column to add to hover information
        #         colorscale="Viridis",
                mode = 'markers',
                marker_color = df['color'],

                marker_size = df["DEGREE"],
                #marker_sizemin = 6,
                marker_colorscale='Rainbow',
                marker_sizeref = 0.08,
                opacity=0.8
                #marker_line_color='black',
                #marker_line_width=0.5,
        #         marker_colorbar_title = 'log(#entities)',
        #         marker_colorbar_ticktext = [0,10,100,1000],
                ))
        fig.update_layout(title_text=f'', 
            geo=dict(
            showframe=True,
            showcoastlines=True,
            showcountries=True,
            projection_type='natural earth'
        ),paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)')
        self.comm_fig = fig

def get_similarity(cpair):
    try: 
        df1 = pd.read_csv(os.path.join(ROOT_DIR,cpair[0],"expertise","expertise.csv"))
        df2 = pd.read_csv(os.path.join(ROOT_DIR,cpair[1],"expertise","expertise.csv"))
        set1=set(df1.sort_values(by="ap", ascending=False).groupby('layer').head(10)['uuid'])
        set2=set(df2.sort_values(by="ap", ascending=False).groupby('layer').head(10)['uuid'])
        set_union=set1.union(set2)
        set_inter=set1.intersection(set2)
        jaccard= len(set_inter)/len(set_union)
        cos_s=1-cosine(df1[df1.uuid.isin(set_union)]['ap'], df2[df2.uuid.isin(set_union)]['ap'])
        return jaccard, cos_s
    except FileNotFoundError:
        return 0,0

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-expert_dir', 
                        '--expert_dir', 
                        default='all_response_h/dataset-en_COUN-TOPIC-100',
                        type=str, 
                        help='expertise unit base dir.', 
                        required=False)
    parser.add_argument('-data_dir', 
                        '--data_dir', 
                        default='data',
                        type=str, 
                        help='data dir.', 
                        required=False)
    parser.add_argument('-model', 
                        '--model', 
                        default='gpt2',
                        type=str, 
                        help='model name.', 
                        required=False)
    parser.add_argument('-base', 
                        '--base', 
                        default='dataset-en_COUN-TOPIC-100-random',
                        type=str, 
                        help='base dir portion.', 
                        required=False)
    args=parser.parse_args()
    return args

if __name__ == '__main__':
    args= get_arguments()
    BASE_DIR=args.expert_dir
    DATA_DIR=args.data_dir
    model_name=args.model
    base_name = args.base
    ROOT_DIR=os.path.join(BASE_DIR,DIRS[model_name],'sense')

    all_country=[]
    all_similarity=[]
    count=0

    print("args:{}".format(args))
    # print("ROOT_DIR:{}".format(ROOT_DIR))

    # for f in os.listdir(ROOT_DIR):
    #     if 'DS_Store' not in str(f) and not str(f).startswith('.'):
    #         # count+=1
    #         # if count>4:
    #         #     break
    #         if len(base_name)==5:
    #             # all_country.append(coco.convert(str(f).split('_')[-1], to='name_short'))
    #             all_country.append(str(f))
    #         else:    
    #             all_country.append(str(f))
    # print(all_country, base_name)
    # cpairs=[pair for pair in itertools.combinations(all_country,2)]
    # count=0
    # for pair in itertools.combinations(all_country,2):
    #     # if count>3:
    #     #     break
    #     # count+=1
    #     jaccard, cos_s = get_similarity(pair)
    #     if len(base_name)==5:
    #         p1=coco.convert(pair[0].split('_')[-1], to='ISO3')
    #         p2=coco.convert(pair[1].split('_')[-1], to='ISO3')
    #     else:
    #         p1=coco.convert(pair[0].replace('_',' '), to='ISO3')
    #         p2=coco.convert(pair[1].replace('_',' '), to='ISO3')
    #     all_similarity.append([p1,p2,jaccard,cos_s])
    #     print(pair,p1,p2,jaccard,cos_s)
    # if not os.path.exists(DATA_DIR):
    #     os.mkdir(DATA_DIR)
    # df = pd.DataFrame(all_similarity, columns=['c1','c2','jac','cos'])
    # save_df_file=os.path.join(DATA_DIR,"{}-{}-csim-all.csv".format(base_name,model_name))
    # df.to_csv(save_df_file)
    # df=df.sort_values(by="jac", ascending=False).groupby('c1').head(1)
    # save_df_file=os.path.join(DATA_DIR,"{}-{}-csim.csv".format(base_name,model_name))
    # print(save_df_file)
    # df.to_csv(save_df_file)
    save_df_file=os.path.join(DATA_DIR,'sim_df',"{}-{}-csim-all.csv".format(base_name,model_name))
    if Path(save_df_file).is_file():
        print(f'{save_df_file} exists')
    else:
        print(save_df_file)
    df = pd.read_csv(save_df_file,index_col=[0])
    df['jac1']=1-df['jac']
    df['jac']=df['jac1']
    df=df.sort_values(by="jac", ascending=True)
    expert_df = df.copy()


    name = base_name
    for i,j in template.items():
        name=name.replace(i,j)
    name = name.replace(name[:2],iso_single(name[:2]))
    print(name)
    name = name.replace(name[4:6],Language.get(name[4:6]).to_alpha3())
    print(name)
    base_name=name
#     if 'US' in name:
#         name = name.replace(c_lang[:2],Language.get(c_lang[:2]).to_alpha3())
#         print(model, c_lang)

#     else:
#         model=name.split('-')[-1]
#         c_lang = '-'.join(name.split('-')[:-1])
#         c_lang = c_lang.replace(c_lang[3:],Language.get(c_lang[3:]).to_alpha3())
#         c_lang = c_lang.replace(c_lang[:2], iso_single(c_lang[:2]))
#         print(model, c_lang)

# #     print(name)
#     if 'US-en' in name and len(name)<13:
#         model=name.split('-')[-1]
#         c_lang = '-'.join(name.split('-')[:-1])
#         c_lang = c_lang.replace(c_lang[3:],Language.get(c_lang[3:]).to_alpha3())
#         c_lang = c_lang.replace(c_lang[:2], iso_single(c_lang[:2]))

    c='Portland'
    plot=PLOT(c)
    expert_df=expert_df[df['jac']!=1]
    plot.create_graph(expert_df,'jac')
    plot.G = nx.minimum_spanning_tree(plot.G,algorithm='prim',weight='weight')
    # plot.set_layout('spring',60)
    # plot.set_nodesizes()
    # plot.set_node_trace()
    # plot.set_edge_trace()
    # plot.draw_graph("{}-{}".format(base_name,model_name))
    # save_image_file="{}-{}-csim.png".format(base_name,model_name)
    # plot.save_graph(save_image_file)


    G = plot.G
    all_com = nx_comm.louvain_communities(G, seed=123)
    all_com_dict={i:com for i,com in enumerate(all_com)}
    data=[]
    for i in G.degree():
        for com_i,com in all_com_dict.items():
            if i[0] in com:
                com_s = com_i
        data.append([i[0],i[1],com_s])

    df=pd.DataFrame.from_records(data,columns=['ISO','DEGREE','COM'])

    ###community color
    comm_color={}
    comms = Counter(df['COM']).most_common()
    for i,x in enumerate(comms):
        if i==len(p_colors):
            comm_color[x[0]]= p_colors[-1]
        else:
            comm_color[x[0]]= p_colors[i]
    df['color']=df.apply(lambda x: comm_color[x['COM']],axis=1)
    color_dict=dict(zip(df['ISO'],df['color']))


    plot.set_layout('spring',60)
    plot.set_nodesizes()
    plot.set_node_trace(color_dict)
    plot.set_edge_trace()
    plot.draw_graph("{}-{}".format(base_name,model_name))
    save_image_file="{}-{}-csim.png".format(base_name,model_name)
    plot.save_graph(save_image_file)


    plot.comm_draw(df)
    save_image_file="{}-{}-csim-c.png".format(base_name,model_name)
    plot.save_graph(save_image_file,"comm")

    # # print(df)

    # plot=PLOT()
    # plot.create_graph(df)
    # plot.set_layout('spring')
    # plot.set_nodesizes()
    # plot.set_node_trace()
    # plot.set_edge_trace()
    # plot.draw_graph("{}-{}".format(base_name,model_name))
    # save_image_file="{}-{}-csim.pdf".format(base_name,model_name)
    # print(save_image_file)
    # plot.save_graph(save_image_file)


# python scripts/plot_similarity.py