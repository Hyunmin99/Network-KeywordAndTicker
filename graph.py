import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

def make_edge(cov_df):
    col1 = cov_df.columns[0]
    col2 = cov_df.columns[1]
    col3 = cov_df.columns[2]
    edge_list = []
    cov_df.apply(lambda x: edge_list.append((x[col1], x[col2], x[col3])), axis=1)
    return edge_list

def draw_graph(edge_list):
    G = nx.Graph()
    G.add_weighted_edges_from(edge_list)
    
    pr = nx.pagerank(G)
    
    # pos = nx.spring_layout(G)
    # pos = nx.spectral_layout(G)
    # pos = nx.shell_layout(G)
    pos = nx.layout.fruchterman_reingold_layout(G)
    # pos = nx.kamada_kawai_layout(G)
    # pos = nx.random_layout(G)
    # pos = nx.circular_layout(G)
    
    fig = plt.figure(figsize=(50,50))
    plt.axis('off')
    nx.draw_networkx(G, pos=pos, node_color=list(pr.values()), node_size= [v*100000 for v in pr.values()], width=list(map(lambda x:x[-1],edge_list)), alpha=0.7, edge_color='.5', font_size=32, cmap = plt.cm.YlGn)
