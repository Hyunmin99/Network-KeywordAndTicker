import pandas as pd
import networkx as nx
import streamlit as st
import matplotlib.pyplot as plt
import generic
import graph

def display_sidebar():
    sel_dtype, sel_date, sel_head, sel_key = None, None, None, None
    st.sidebar.header('Choose selections below')
    
    # 1) Type of data
    st.sidebar.markdown('Which data do you want to show?')
    sel_dtype = st.sidebar.radio('Data Type',['Keyword_single', 'Keyword_multi', 'Ticker_single', 'Ticker_multi'])
    
    # read data by sel_dtype
    data = generic.read_data(sel_dtype) #Just read csv 
    
    # 2) Select date
    sel_date = st.sidebar.selectbox('Date',['None']+generic.get_date_list(data))
    
    # 3) Number of head data
    st.sidebar.markdown('How many data do you want to show?')
    if sel_dtype in ('Keyword_single','Ticker_single'):
        sel_head = st.sidebar.slider('Top...', min_value=5, max_value=30, value=10)
    else: 
        sel_head = st.sidebar.slider('Top', min_value=1, max_value=10, value=5)
        
    # slice data
    sel_data, sel_key_list = generic.get_sel_data(data, sel_date, sel_head)
    
    # 4) Select Keyword or Ticker 
    if sel_dtype in ('Keyword_single','Ticker_single'):
        st.sidebar.markdown('Choose single [Keyword / Ticker]')
        sel_key = st.sidebar.selectbox('Choose one',['None']+sel_key_list)
    else: 
        sel_key = None
    
    return sel_dtype, sel_date, sel_head, sel_key, sel_data

def show_chart(cov_df):
    edge_list = graph.make_edge(cov_df)
    
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
    
    st.pyplot(fig)

'''
    # 5) Show graph to image
    if sel_chart:
        st.sidebar.markdown('Which file extenstion to save the file into?')
        # sel_save = st.sidebar.button('Save')
        sel_save = st.sidebar.radio('Filetype',[None,'PNG','PDF'])
'''