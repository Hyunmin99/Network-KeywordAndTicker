import pandas as pd
import streamlit as st
import re
import networkx as nx
import matplotlib.pyplot as plt
import string

################################################
# Header and preprocessing

# Set Title
st.title('Network Graph - Ticker and Keyword Count')

#Read data
data = pd.read_csv('data/Match Ticker and Keyword Count_day.csv')

################################################
# Sidebar section

sel_date, sel_tic, sel_chart, sel_save = None, None, None, None

st.sidebar.header('Choose selections below')

# 1) Select date
#st.sidebar.markdown('Select date')
sel_date = st.sidebar.selectbox('Date',['None']+data['date'].unique().tolist()) 

sel_head = st.sidebar.slider('Top...', min_value=5, max_value=30)

# 2) Select Keyword
if sel_date == 'None':
    #st.sidebar.markdown('Select Keyword')
    sel_tic = st.sidebar.selectbox('ticker', ['None'], disabled=True)
else:
    sel_data = data.groupby('date').get_group(sel_date)
    #st.sidebar.markdown('Select Number of Keyword')
    #head_num = st.sidebar.selectbox('Number of Keyword', ['None', 5, 10, 15, 20, 30], disabled=True)
    sel_data['count'] = sel_data['keyword count'].apply(lambda x: sum(map(int, re.findall(r'\d+', x))))
    tic_rank = sel_data.sort_values(by=['count'], axis=0, ascending=False).head(sel_head)['symbol'].tolist()
    sel_data = sel_data.sort_values(by=['count'], axis=0, ascending=False).head(sel_head).reset_index(drop = True)
    
    #st.sidebar.markdown('Select Keyword')
    sel_tic = st.sidebar.selectbox('Ticker',['None']+tic_rank)
    st.dataframe(sel_data)


# 3) Show network/graph chart
st.sidebar.markdown('Show network graph?')
sel_chart = st.sidebar.checkbox('WHY NOT??')

# 4) Show chart to image
if sel_chart:
    st.sidebar.markdown('Which file extenstion to save the file into?')
    # sel_save = st.sidebar.button('Save')
    sel_save = st.sidebar.radio('Filetype',[None,'PNG','SVG','PDF'])

################################################
# Main section

# Generate Keyword - Count DataFrame
if sel_tic != 'None':
    ticker_list = sel_data.loc[(sel_data['symbol']==sel_tic), 'keyword count'].values[0]
    ticker_list = ticker_list[1:-1]
    ticker_list2 = re.findall(r'\(\'\D+\', \d\)', ticker_list)

    tmp_list = []

    for idx, data in enumerate(ticker_list2):
        data = re.sub('[(,\),\',\']', '', data)
        tmp = re.split(' ', data)
        tmp[1] = int(tmp[1])
        tmp_list.append(tmp)

    df_ticker = pd.DataFrame(tmp_list, columns=['keyword', 'count'])
    st.dataframe(df_ticker)

    edge_list = []
    df_ticker.apply(lambda x: edge_list.append((sel_tic, x['keyword'], x['count'])), axis=1)

    G = nx.Graph()
    G.add_weighted_edges_from(edge_list)
    pr = nx.pagerank(G)
    pos = nx.layout.fruchterman_reingold_layout(G)
    size = {sel_tic: (sel_data.loc[(sel_data['symbol']==sel_tic), 'count'].values[0]/100)}
    keyword_size = df_ticker[['keyword', 'count']].set_index('keyword').to_dict()
    size.update(keyword_size["count"])
    fig = plt.figure(figsize=(20,20))
    plt.axis('off')
    nx.draw_networkx(G, pos=pos,node_color=list(pr.values()), node_size=[v*1000 for v in size.values()], width=list(map(lambda x:x[-1],edge_list)), alpha=0.7, edge_color='.5', font_size=16, cmap = plt.cm.YlGn)
    #plt.savefig(f'data/{sel_key}_img.png')

if sel_chart:
    st.pyplot(fig)
    if sel_save:
        plt.savefig(f'img/TICKER_{sel_date}_{sel_tic}_img.{sel_save.lower()}')
        
