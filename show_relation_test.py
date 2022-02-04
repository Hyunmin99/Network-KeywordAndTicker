import numpy as np
import pandas as pd
import re
import networkx as nx
import matplotlib.pyplot as plt
import string
from datetime import datetime
import datetime as dt
import os.path

articles = pd.read_csv('D:/CSV/US_CNBC_'+str(datetime.today().strftime("%y%m%d"))+'_tfidf_7.csv')
#articles = pd.read_csv('D:/CSV/US_CNBC_220120_tfidf_7.csv')
words = pd.read_csv('D:/CSV/new_words.csv')
date_id = pd.read_csv('D:/CSV/US_CNBC_date.csv')
att_words = pd.read_csv('D:/CSV/att_words.csv')
relation_path = 'D:/CSV/relations/US_CNBC_relations_'

g_date = ''
date_b = 0
key_w = 'battery'
s_words = pd.DataFrame(columns=['WORD','DATE','support'])
exw = ["year","company","u","s","cnbcfed","acornscnbc","athttpswwwcnbceventscomworksummit",
       "cnbccouncilscomwec","cnbcmomentive","cnbcmost","cnbcnbcuniversal","cnbcon","cnbcs",
       "cnbcsbetsy","cnbcssquawk","cnbcsurveymonkey","cnbctechnology","cnbcthe","employercnbc",
       "httpswwwcnbceventscomworksummit","newcnbc","yearscnbc","cnbcrichard","cnbcbrainards",
       "cnbcthis","cnbcafter","cnbcfink","cnbcmorgan","cnbcunitedhealth","cnbcpeloton",
       "cnbccryptocurrency","cnbcbond","investor","market","world","stock","country","week","month","day",
       "people","yearolds","madcapcnbc","athome","athreemonth","athttpswwwcnbceventscomworksummit",
       "attwarnermedias","atwalmartandkrogerstores","augustbaidulaunchedits","awsamazonwould",
       "backendfraudprocesses","backtoback","backtoschool","backtowork","bankratecom","beatfourthquarter",
       "beathealthcare","becarefulwhatyouwishfor","becausehe","becybersmart","behindthecamera","behindthescenes",
       "behindwalmart","beinefficient","benefitat","benefitits","benefitshere","benefitshow","benefitsinflation",
       "benefitsis","betterairports","bettercom","betterfouryoubeer","betweenpresidents","beyondthe",
       "biggerthanexpects","biggesttransformations","billionaireversusbillionaireversusmillionaire",
       "billionandbillion","bitcoinhow","bitcoinira","blackberryblackberry","blizzardactivision","boeingshares",
       "bombconsider","booksandrecords","bothboxofficecomchief","bothjohnson","bottleneckssupply","boxofficecom",
       "brickandmortar","bricksandmortars","broadcombroadcoms","carbonfeestoindividualsectors","carmenreinickenbcunicom", "number"]
limt = 15

for k in range(0, len(words)):
    if words['WORD'][k] == key_w:
        date_b = words['DATE'][k] - 1
        break

#print(date_b)
exw.append(key_w)
#for i in range(date_b+7,len(date_id)):
for i in range(len(date_id)-20,len(date_id)):
    g_date = date_id.iloc[i][1]
    print(key_w, ' ', g_date)
    if os.path.isfile(relation_path + key_w +'_'+ g_date+'.csv'):
        rel_d1 = pd.read_csv(relation_path + key_w +'_'+ g_date+'.csv')
        rel_d1 = rel_d1.sort_values(by='support', ignore_index=True, ascending=False)
        
        for j in range(0, len(rel_d1)):
            e_cnt = 0
            key_s = rel_d1['target'][j]
            for w in range(0, len(exw)):
                if exw[w] == key_s:
                    e_cnt=1
            if e_cnt==0:
                exw.append(key_s)
         
        if len(rel_d1) < limt:
            retr = len(rel_d1)
        else:
            retr = limt
        for j in range(0, retr):
            e_cnt = 0
            key_s = rel_d1['target'][j]
            #for w in range(0, len(exw)):
            #    if exw[w] == key_s:
            #        e_cnt=1
            if e_cnt==0:
                data_to_insert = {'WORD': (key_w, rel_d1['target'][j]), 'DATE': g_date, 'support' : rel_d1['support'][j]}
                s_words = s_words.append(data_to_insert, ignore_index=True)
#'''
                print(key_s)
                if os.path.isfile(relation_path + key_s +'_'+ g_date+'.csv'):
                    rel_d2 = pd.read_csv(relation_path + key_s +'_'+ g_date+'.csv')
                    rel_d2 = rel_d2.sort_values(by='support', ignore_index=True, ascending=False)
                    
                    if len(rel_d2) < limt:
                        retrs = len(rel_d2)
                    else:
                        retrs = limt
                    for k in range(0, retrs):
                        ee_cnt=0
                        for w in range(0, len(exw)):
                            if exw[w] == rel_d2['target'][k]:
                                ee_cnt=1
                        if ee_cnt==0:
                            data_to_insert = {'WORD': (key_s, rel_d2['target'][k]), 'DATE': g_date, 'support' : rel_d2['support'][k]}
                            s_words = s_words.append(data_to_insert, ignore_index=True)
#'''
if set(['Unnamed: 0']).issubset(s_words.columns):
    s_words = s_words.drop(['Unnamed: 0'],axis='columns')
'''
ret_txt = ''
for i in range(0, len(s_words)):
        if len(s_words)==1:
            ret_txt = ret_txt+ '{' + s_words['WORD'][i] +':' +s_words['DATE'][i] + '}'
        else:
            if i==0:
                ret_txt = ret_txt+ '{' + s_words['WORD'][i] +':' +s_words['DATE'][i]
            elif i==len(s_words)-1:
                ret_txt = ret_txt+ ', ' +s_words['WORD'][i] +':' +s_words['DATE'][i] + '}'
            else:
                ret_txt = ret_txt+ ', ' +s_words['WORD'][i] +':' +s_words['DATE'][i]
print(ret_txt)
'''

G = nx.Graph()
ar = (s_words['WORD'])
G.add_edges_from(ar)

pr = nx.pagerank(G)
nsize = np.array([v for v in pr.values()])
nsize = 2000 * (nsize - min(nsize))/(max(nsize) - min(nsize))

#pos = nx.planar_layout(G)
#pos = nx.spring_layout(G)
#pos = nx.spectral_layout(G)
#pos = nx.shell_layout(G)
#pos = nx.layout.fruchterman_reingold_layout(G)
pos = nx.kamada_kawai_layout(G)
#pos = nx.random_layout(G)
#pos = nx.circular_layout(G)

plt.figure(figsize = (20,20))
plt.axis('off')
nx.draw_networkx(G, pos=pos, node_color=list(pr.values()), node_size= nsize, alpha=0.7, edge_color='.5', cmap = plt.cm.YlGn)

