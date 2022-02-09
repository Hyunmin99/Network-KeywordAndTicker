import pandas as pd
import streamlit as st
import re
import networkx as nx
import matplotlib.pyplot as plt
import string
from ast import literal_eval

################################################
# Header and preprocessing

# Set Title
st.title('Network Graph - Tickers and Keyword Count')

#Read data
data = pd.read_csv('data/Match Ticker and Keyword Count_day.csv')

################################################
# Sidebar section

sel_date, sel_chart, sel_save = None, None, None

st.sidebar.header('Choose selections below')

# Select date
#st.sidebar.markdown('Select date')
sel_date = st.sidebar.selectbox('Date',['None']+data['date'].unique().tolist()) 

sel_head = st.sidebar.slider('Top...', min_value=1, max_value=10, value=5)

# Show network/graph chart
st.sidebar.markdown('Show network graph?')
sel_chart = st.sidebar.checkbox('WHY NOT??')

# Show chart to image
if sel_chart:
    st.sidebar.markdown('Which file extenstion to save the file into?')
    # sel_save = st.sidebar.button('Save')
    sel_save = st.sidebar.radio('Filetype',[None,'PNG','SVG','PDF'])

################################################
# Main section
if sel_date:
    # Get Top Keywords' Data
    sel_data = data.groupby('date').get_group(sel_date)
    sel_data['count'] = sel_data['keyword count'].apply(lambda x: sum(map(int, re.findall(r'\d+', x))))
    sel_data = sel_data.sort_values(by=['count'], axis=0, ascending=False).head(sel_head).reset_index(drop = True)
    st.dataframe(sel_data)
    sel_data['keyword count'] = sel_data['keyword count'].map(lambda x: literal_eval(x))
    

    edge = pd.DataFrame()
    for idx in range(len(sel_data)):
        tmp = sel_data['keyword count'][idx]

        df = pd.DataFrame(tmp, columns = ['keyword', 'count'])
        df['ticker'] = sel_data['symbol'][idx]
        df = df[['ticker', 'keyword', 'count']]
        edge = pd.concat([edge, df]).reset_index(drop=True)

    st.dataframe(edge)
    edge_list = []
    edge.apply(lambda x: edge_list.append((x['ticker'], x['keyword'], x['count'])), axis=1)

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
    #plt.savefig(f'data/{sel_key}_img.png')

    if sel_chart:
        st.pyplot(fig)
        if sel_save:
            plt.savefig(f'img/TICKER_{sel_date}_TOP{sel_head}_img.{sel_save.lower()}')
