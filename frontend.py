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
    sel_dtype = st.sidebar.radio('Which data do you want to show?',['Keyword_single', 'Keyword_multi', 'Ticker_single', 'Ticker_multi'])
    
    # read data by sel_dtype
    data = generic.read_data(sel_dtype) #Just read csv 
    
    # 2) Select date
    sel_date = st.sidebar.selectbox('Choose a Date',['None']+generic.get_date_list(data))
    
    # 3) Number of head data
    if sel_dtype in ('Keyword_single','Ticker_single'):
        sel_head = st.sidebar.slider('How many data do you want to show?', min_value=5, max_value=30, value=10)
    else: 
        sel_head = st.sidebar.slider('How many data do you want to show?', min_value=1, max_value=10, value=5)
        
    # slice data
    sel_data, sel_key_list = generic.get_sel_data(data, sel_date, sel_head)
    
    # 4) Select Keyword or Ticker 
    if sel_dtype in ('Keyword_single','Ticker_single'):
        sel_key = st.sidebar.selectbox('Choose a single [Keyword / Ticker]',['None']+sel_key_list)
    else: 
        sel_key = None
    
    return sel_dtype, sel_date, sel_head, sel_key, sel_data

def show_chart(fig):
    
    st.pyplot(fig)

'''
    # 5) Show graph to image
    if sel_chart:
        st.sidebar.markdown('Which file extenstion to save the file into?')
        # sel_save = st.sidebar.button('Save')
        sel_save = st.sidebar.radio('Filetype',[None,'PNG','PDF'])
'''