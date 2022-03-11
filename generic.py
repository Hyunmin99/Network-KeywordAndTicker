import pandas as pd
import re
import streamlit as st
from ast import literal_eval

def read_data(sel_dtype):
    if sel_dtype in ('Keyword_single','Keyword_multi'): #Keyword 기준 그래프 데이터 가져오기
        data = pd.read_csv('data/Match Keyword and Ticker Count_day.csv')
    else: #Ticker 기준 그래프 데이터 가져오기
        data = pd.read_csv('data/Match Ticker and Keyword Count_day.csv')
    return data

def get_date_list(data):
    date_list = data['date'].unique().tolist()
    return date_list

def get_sel_data(data, sel_date, sel_head):
    key_type, count_type, sub_key_type = get_key_type(data)
    
    sel_data = data.groupby('date').get_group(sel_date)
    sel_data['count'] = sel_data[count_type].apply(lambda x: sum(map(int, map(lambda x: x.replace(', ', ''), re.findall(r'\, \d+', x)))))
    sel_data = sel_data.sort_values(by=['count'], axis=0, ascending=False).head(sel_head).reset_index(drop = True)
    
    sel_key_list = sel_data[key_type].tolist() # for single key graph
    return sel_data, sel_key_list
    
def get_key_type(sel_data):
    key_type = sel_data.columns[1] #[keyword or symbol]
    count_type = sel_data.columns[2] #[keyword count or ticker count]
    sub_key_type = 'ticker' if key_type == 'keyword' else 'keyword'
    return key_type, count_type, sub_key_type

def single_key_df(sel_data, sel_key):
    key_type, count_type, sub_key_type = get_key_type(sel_data)
    
    sel_data = sel_data.loc[(sel_data[key_type]==sel_key)]
    cov_list = sel_data[count_type].map(lambda x: literal_eval(x)) #count data [string -> list]
    
    cov_df = pd.DataFrame(cov_list.iloc[0], columns = [sub_key_type, 'count'])
    cov_df[key_type] = cov_df.apply(lambda x: sel_key, axis = 1)
    cov_df = cov_df[[key_type, sub_key_type, 'count']]
    
    return cov_df

def multi_key_df(sel_data):
    key_type, count_type, sub_key_type = get_key_type(sel_data)

    sel_data[count_type] = sel_data[count_type].map(lambda x: literal_eval(x)) #count data [string -> list]

    cov_df = pd.DataFrame()
    for idx in range(len(sel_data)):
        tmp = sel_data[count_type][idx]
        
        df = pd.DataFrame(tmp, columns = [sub_key_type, 'count'])
        df[key_type] = sel_data[key_type][idx]
        df = df[[key_type, sub_key_type, 'count']]
        cov_df = pd.concat([cov_df, df]).reset_index(drop=True)    

    return cov_df
