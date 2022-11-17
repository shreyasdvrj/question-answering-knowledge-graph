import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def createGraph(dataEntities):
        entity_list = dataEntities.values.tolist()
        source, relations, target = [],[],[]

        for i in entity_list:
           
            source.append(i[0])
            relations.append(i[1])
            # aux_relations = i[2]
            target.append(i[3])
            # time = i[4]
            # place = i[5]

        kg_df = pd.DataFrame({'source':source,'edge':relations, 'target':target, })
        kg_df.to_csv('./content/triples.csv')
        G=nx.from_pandas_edgelist(kg_df, "source", "target", edge_attr=True, create_using=nx.MultiDiGraph())

        plt.figure(figsize=(20,20))
        pos = nx.shell_layout(G)
        nx.draw(G, with_labels=True, node_color='skyblue', edge_cmap=plt.cm.Blues, pos = pos)
        nx.draw_networkx_edge_labels(G, pos=pos)
        plt.savefig('./static/kg.png')