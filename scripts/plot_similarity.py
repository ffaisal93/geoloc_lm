import pandas as pd
from scipy.spatial.distance import cosine
import os
import itertools
import argparse
import country_converter as coco
import networkx as nx
import plotly.graph_objs as go

ROOT_DIR="/Users/faisal/a/scratch/ml-selfcond/all_response_h/dataset-en_COUN-TOPIC-100/gpt2-medium/sense"
DIRS={
    "gpt2":"gpt2-medium",
    "bloom":"bigscience/bloom-560m",
    "mgpt":"sberbank-ai/mGPT"
}
DATA_DIR="data"
DISCARDED=['.DS_Store','._DS_Store']
IMAGE_DIR="images"

class PLOT:
    def __init__(self):
        self.G = nx.Graph()
        self.node_size={}
        self.title="title"
        self.edge_trace=go.Scatter()
        self.node_trace=go.Scatter()
        self.fig = go.Figure()
    
    def create_graph(self,df):
        node_list = list(set(df['c1']).union(set(df['c2'])))
        from_list=df['c1'].to_list()
        to_list=df['c2'].to_list()
        for i in range(len(node_list)):
            self.G.add_node(node_list[i])
        for i in range(len(from_list)):
            self.G.add_edges_from([(from_list[i], to_list[i])])
    
    def set_layout(self):
        pos = nx.spring_layout(self.G)
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
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines')
        for edge in self.G.edges():
            x0, y0 = self.G.nodes[edge[0]]['pos']
            x1, y1 = self.G.nodes[edge[1]]['pos']
            self.edge_trace['x'] += tuple([x0, x1, None])
            self.edge_trace['y'] += tuple([y0, y1, None])
    
    def set_node_trace(self):
        self.node_trace = go.Scatter(
            x=[],
            y=[],
            text=[],
            mode='markers+text',
            hoverinfo='text',
            marker=dict(
                showscale=True,
                colorscale='pinkyl',
                reversescale=True,
                color=[],
                size=[],
                colorbar=dict(
                    thickness=1,
                    title='Node Connections',
                    xanchor='left',
                    titleside='right'
                ),
                line=dict(width=0)))
        for node in self.G.nodes():
            x, y = self.G.nodes[node]['pos']
            self.node_trace['x'] += tuple([x])
            self.node_trace['y'] += tuple([y])
            self.node_trace['marker']['size'] += tuple([self.node_size[node]*10])

        for node, adjacencies in enumerate(self.G.adjacency()):
            self.node_trace['marker']['color'] += tuple([len(adjacencies[1])])
            node_info = adjacencies[0]
            self.node_trace['text'] += tuple([node_info])
    
    def draw_graph(self,title="Country Similarity",text=""):
        self.title=title
        self.fig = go.Figure(data=[self.edge_trace, self.node_trace],
                        layout=go.Layout(
                        title=self.title,
                        titlefont=dict(size=16),
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=21, l=5, r=5, t=40),
                        annotations=[dict(
                            text=text,
                            showarrow=False,
                            xref="paper", yref="paper")],
                        xaxis=dict(showgrid=False, zeroline=False,
                                showticklabels=False, mirror=True),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, mirror=True)))
        
    
    def show_graph(self):
        self.fig.show()
    
    def save_graph(self,fname=""):
        if fname=="":
            fname=os.path.join(IMAGE_DIR,self.title.replace(" ","_")+".pdf")
        if not os.path.exists(IMAGE_DIR):
            os.mkdir(IMAGE_DIR)
        print(fname)
        self.fig.write_image(os.path.join(IMAGE_DIR,fname))

def get_similarity(cpair):
    df1 = pd.read_csv(os.path.join(ROOT_DIR,cpair[0],"expertise","expertise.csv"))
    df2 = pd.read_csv(os.path.join(ROOT_DIR,cpair[1],"expertise","expertise.csv"))
    set1=set(df1.sort_values(by="ap", ascending=False).groupby('layer').head(10)['uuid'])
    set2=set(df2.sort_values(by="ap", ascending=False).groupby('layer').head(10)['uuid'])
    set_union=set1.union(set2)
    set_inter=set1.intersection(set2)
    jaccard= len(set_inter)/len(set_union)
    cos_s=1-cosine(df1[df1.uuid.isin(set_union)]['ap'], df2[df2.uuid.isin(set_union)]['ap'])
    return jaccard, cos_s

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
    args=parser.parse_args()
    return args

if __name__ == '__main__':
    args= get_arguments()
    BASE_DIR=args.expert_dir
    DATA_DIR=args.data_dir
    model_name=args.model
    ROOT_DIR=os.path.join(BASE_DIR,DIRS[model_name],'sense')

    all_country=[]
    all_similarity=[]
    count=0
    for f in os.listdir(ROOT_DIR):
        if 'DS_Store' not in str(f):
            count+=1
            if count>4:
                break
            all_country.append(str(f))
    cpairs=[pair for pair in itertools.combinations(all_country,2)]
    for pair in itertools.combinations(all_country,2):
        jaccard, cos_s = get_similarity(pair)
        p1=coco.convert(pair[0].replace('_',' '), to='ISO3')
        p2=coco.convert(pair[1].replace('_',' '), to='ISO3')
        all_similarity.append([p1,p2,jaccard,cos_s])
    df = pd.DataFrame(all_similarity, columns=['c1','c2','jac','cos'])
    df=df.sort_values(by="jac", ascending=False).groupby('c1').head(1)
    if not os.path.exists(DATA_DIR):
            os.mkdir(DATA_DIR)
    df.to_csv(os.path.join(DATA_DIR,model_name+"-similarty_df.csv"))
    df = pd.read_csv(os.path.join(DATA_DIR,model_name+"-similarty_df.csv"),index_col=[0])
    # print(df)

    plot=PLOT()
    plot.create_graph(df)
    plot.set_layout()
    plot.set_nodesizes()
    plot.set_node_trace()
    plot.set_edge_trace()
    plot.draw_graph()
    plot.save_graph(model_name+"-country_similarity.pdf")


# python scripts/plot_similarity.py