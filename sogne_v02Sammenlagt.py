# -*- coding: utf-8 -*-
import json
import requests
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go
import re
import numpy as np
#from plotly.graph_objs import Scatter, Figure, Layout
#%% Funktion der regner faldet i sognene
def diffMembership(sogneKode, url_API):
    kald2 = {"table": "KM5", "format": "CSV",\
             "variables": [
                     {"code": "SOGN", "values": [str(sogneKode)]}, \
                     {"code": "ALDER", "values": ["1"]}, \
                     {"code": "FKMED", "values":["*"]},\
                     {"code": "Tid", "values": ["2007", "2017"]}]}
    r = requests.post(url_API, json=kald2)
    print("******************")
    print("Status code:", r.status_code)
    print("******************")
    txtData = StringIO(r.text)
    df = pd.read_csv(txtData, sep=";")
    df2 = df.pivot(index='TID', columns='FKMED', values='INDHOLD')
    df2['Daab'] = df2.apply (lambda row: medlemsPct(row), axis=1)
    diff = (df2.iloc[1,2] - df2.iloc[0,2])*(-1)
    sogn = df.iloc[0,0][9:]
    d = {}
    d['sogn'] = sogn
    d['sognekode'] = sogneKode
    d['difference'] = diff
    d['N_2017'] = sum(df2.iloc[1,[0,1]])
    return d
#%%
sognno = [1017060, 1017058, 1017059,2657156,2657157,2657158,2657159,2657160,2657161,2657166,2657167,2657168,2657169,2657170,
            2657197,2657198,2657210,2657211,2657212,2657213,2697201,2697202,2697203,2697204,2697205]
url = "http://api.statbank.dk/v1/data"

Sdata = []
for s in sognno:
    Sdata.append(diffMembership(s, url))

dfS = pd.DataFrame(Sdata)
#%%
trace = go.Scatter(x = dfS['N_2017'], 
                   y = dfS['difference'], 
                   text = dfS['sogn'],
                   #marker = dict(
                   #        size = dfS['N_2017']/5
                   #        ),
                   mode = 'markers')
plot([trace])

#%%
a = diffMembership(2657156, url)
#%%
p = re.compile('[A-Z]\w+')
p.findall('265-7156 Roskilde Domsogn')


#%%
kald3 = {
   "table": "KM6",
   "format": "CSV",
   "variables": [
      {
         "code": "KOMK",
         "values": [
            "101",
            "*"
         ]
      },
      {
         "code": "FKMED",
         "values": [
            "*"
         ]
      },
      {
         "code": "Tid",
         "values": [
            "2011",
            "2017"
         ]
      }
   ]
}
      
#%%
r = requests.post(url, json=kald3)
print("******************")
print("Status code:", r.status_code)
print("******************")

#%%
txtData = StringIO(r.text)
df = pd.read_csv(txtData, sep=";")
dfPivot = pd.pivot_table(df, values = 'INDHOLD', index = ['KOMK', 'TID'], columns = ['FKMED'])
dfPivot['Daab'] = dfPivot.apply (lambda row: medlemsPct(row), axis=1)
dfPivot['total'] = dfPivot.apply (lambda row: totalBef(row), axis = 1)
dfPivot.head()
#%%
l = []
for kommune, new_df in dfPivot.groupby(level=0):
    d = {}
    d['difference'] = (new_df.iloc[1,2] - new_df.iloc[0,2])*-1
    d['kommune'] = kommune
    d['N_2017'] = new_df.iloc[1,3]
    d['logBefDif'] = np.log(new_df.iloc[1,3]) - np.log(new_df.iloc[0,3])
    l.append(d)

dfKom = pd.DataFrame(l)
print(dfKom.head())
#%% 
#%%
trace = go.Scatter(x = dfKom['logBefDif'], 
                   y = dfKom['difference'], 
                   text = dfKom['kommune'],
                   mode = 'markers')
plot([trace])
