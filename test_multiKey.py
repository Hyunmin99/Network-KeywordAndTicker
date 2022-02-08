import pandas as pd
import streamlit as st
import re
import networkx as nx
import matplotlib.pyplot as plt
import string

################################################
# Header and preprocessing

# Set Title
st.title('Network Graph - Keyword and Ticker Count')

#Read data
data = pd.read_csv('data/Match Keyword and Ticker Count_day.csv')

################################################
# Sidebar section

sel_date, sel_chart, sel_save = None, None, None

st.sidebar.header('Choose selections below')

# Select date
#st.sidebar.markdown('Select date')
sel_date = st.sidebar.selectbox('Date',['None']+data['date'].unique().tolist()) 

sel_head = st.sidebar.slider('Top...', min_value=1, max_value=10)

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

# Generate Keyword - Count DataFrame
sel_data = data.groupby('date').get_group(sel_date)
sel_data['count'] = sel_data['ticker count'].apply(lambda x: sum(map(int, re.findall(r'\d+', x))))
sel_data = sel_data.sort_values(by=['count'], axis=0, ascending=False).head(sel_head).reset_index(drop = True)
st.dataframe(sel_data)
key_rank = sel_data.sort_values(by=['count'], axis=0, ascending=False).head(sel_head)['keyword'].tolist()

# keyword_list = sel_data.loc[(sel_data['keyword']==sel_key), 'ticker count'].values[0]
# keyword_list = keyword_list[1:-1]
# keyword_list2 = re.findall(r'\(\'\D+\', \d\)', keyword_list)

'''
tmp_list = []

for idx, data in enumerate(keyword_list2):
    data = re.sub('[(,\),\',\']', '', data)
    tmp = re.split(' ', data)
    tmp[1] = int(tmp[1])
    tmp_list.append(tmp)

df_keyword = pd.DataFrame(tmp_list, columns=['ticker', 'count'])
st.dataframe(df_keyword)

edge_list = []
df_keyword.apply(lambda x: edge_list.append((sel_key, x['ticker'], x['count'])), axis=1)

G = nx.Graph()
G.add_weighted_edges_from(edge_list)
pr = nx.pagerank(G)
pos = nx.layout.fruchterman_reingold_layout(G)
fig = plt.figure(figsize=(20,20))
plt.axis('off')
nx.draw_networkx(G, pos=pos,node_color=list(pr.values()), width=list(map(lambda x:x[-1],edge_list)), alpha=0.7, edge_color='.5', font_size=16, cmap = plt.cm.YlGn)
#plt.savefig(f'data/{sel_key}_img.png')

if sel_chart:
    st.pyplot(fig)
    if sel_save:
        plt.savefig(f'img/{sel_date}_TOP{sel_head}_img.{sel_save.lower()}')
'''