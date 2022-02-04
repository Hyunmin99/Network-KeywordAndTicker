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
data = pd.read_csv('data/sample_data.csv')

################################################
# Sidebar section

sel_date, sel_key, sel_chart, sel_save = None, None, None, None

st.sidebar.header('Choose selections below')

# 1) Select date
st.sidebar.markdown('Select date')
sel_date = st.sidebar.selectbox('Date',['None']+data['date'].unique().tolist()) 

# 2) Select Keyword
if sel_date == 'None':
    st.sidebar.markdown('Select Keyword')
    sel_key = st.sidebar.selectbox('keyword', ['None'], disabled=True)
else:
    sel_data = data.groupby('date').get_group(sel_date)
    sel_data['count'] = sel_data['ticker count'].apply(lambda x: sum(map(int, re.findall(r'\d+', x))))
    key_rank = sel_data.sort_values(by=['count'], axis=0, ascending=False).head(20)['keyword'].tolist()
    sel_data = sel_data.sort_values(by=['count'], axis=0, ascending=False).head(20).reset_index(drop = True)
    
    st.sidebar.markdown('Select Keyword')
    sel_key = st.sidebar.selectbox('Keyword',['None']+key_rank)
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
# Sidebar section

sel_data.loc[(sel_key['keyword']==sel_key), 'ticker count'].values[0]







G = nx.Graph()
