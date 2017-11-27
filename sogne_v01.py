# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 23:52:33 2017

@author: ntyss
"""

import json
import requests
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.plotly as py
import plotly
import plotly.graph_objs as go
import re
import numpy as np
#from plotly.graph_objs import Scatter, Figure, Layout

#%% Definitioner
def medlemsPct(row):
    total = row['Ikke medlem af Folkekirken'] + row['Medlem af Folkekirken']
    mPct = 100*row['Medlem af Folkekirken']/total
    return mPct
def totalBef(row):
    total = row['Ikke medlem af Folkekirken'] + row['Medlem af Folkekirken']
    return total

#%%
url_API = 'http://api.statbank.dk/v1/data'
sognKode = 1019185
#%%
kald = {'table':'KM1', 'format':'CSV',"delimiter": "Semicolon",'timeOrder':'Ascending',"timeOrder": "Ascending",
        'variables':[{'code':'Tid','values':['*']},\
                      {'code':'FKMED','values':['F','U']},\
                      {'code':'SOGN','values':[str(sognKode)]}]}
kaldDK = {
   "table": "KM1",
   "format": "CSV",
   "variables": [
      {
         "code": "FKMED",
         "values": [
            "*"
         ]
      },
      {
         "code": "Tid",
         "values": [
            "*"
         ]
      }
   ]
}
r = requests.post(url_API, json=kald)
print('Status koden er: ', r.status_code)
txtData = StringIO(r.text)
df = pd.read_csv(txtData, sep=";")
sogn = df.iloc[1][2].split()[1]
df2 = df.pivot(index='TID', columns='FKMED', values='INDHOLD')
df2['MedlPct'] = df2.apply (lambda row: medlemsPct(row), axis=1)
df2['totBef'] = df2.apply (lambda row: totalBef(row), axis=1)

r = requests.post(url_API, json=kaldDK)
print('Status koden er(DK): ', r.status_code)
txtData = StringIO(r.text)
dfDK = pd.read_csv(txtData, sep=";")
df2DK = dfDK.pivot(index='TID', columns='FKMED', values='INDHOLD')
df2DK['M_DK'] = df2DK.apply (lambda row: medlemsPct(row), axis=1)
df2DK['totBEFdk'] = df2DK.apply (lambda row: totalBef(row), axis=1)

dfMerge = df2.merge(pd.DataFrame(df2DK['M_DK']), left_index=True, right_index=True)
del df2DK, dfDK, df, df2, kald, kaldDK

fig, ax = plt.subplots()
#ax.set_title(sogn)
ax.set_ylabel('Medlemsprocent')
ax.set_xlabel(None)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.yaxis.grid()
#ax.set_xticklabels( rotation=45, rotation_mode="anchor")
#ax.yaxis.set_ticks_position('left')
#ax.xaxis.set_ticks_position('bottom')
dfMerge['MedlPct'].plot(label=sogn)
dfMerge['M_DK'].plot(label='Danmark')
ax.legend()
plt.show()


#%% Dåbdsprocent og sammenligning mellem landsgennemsnit

kald2 = {"table": "KM5", "format": "CSV",\
   "variables": [
      {"code": "SOGN", "values": [str(sognKode)]}, \
      {"code": "ALDER", "values": ["1"]}, \
      {"code": "FKMED", "values":["*"]},\
      {"code": "Tid", "values": ["*"]}]}
kald2DK = {"table": "KM5", "format": "CSV",\
   "variables": [ \
      {"code": "ALDER", "values": ["1"]}, \
      {"code": "FKMED", "values":["*"]},\
      {"code": "Tid", "values": ["*"]}]}
r = requests.post(url_API, json=kald2)
print("******************")
print("Status code:", r.status_code)
print("******************")

txtData = StringIO(r.text)
df = pd.read_csv(txtData, sep=";")
sognDaab = df.iloc[0,0][9:]
dfx = df.pivot(index='TID', columns='FKMED', values='INDHOLD')
dfx['Daab'] = dfx.apply (lambda row: medlemsPct(row), axis=1)

r = requests.post(url_API, json=kald2DK)
print("******************")
print("Status code (DK):", r.status_code)
print("******************")

txtData = StringIO(r.text)
df = pd.read_csv(txtData, sep=";")
dfxDK = df.pivot(index='TID', columns='FKMED', values='INDHOLD')
dfxDK['DaabDK'] = dfxDK.apply (lambda row: medlemsPct(row), axis=1)

dfDaab = dfx.merge(pd.DataFrame(dfxDK['DaabDK']), left_index=True, right_index=True)
del dfx, dfxDK, kald2, kald2DK

fig, ax = plt.subplots()
ax.set_title('Dåbsprocent')
ax.set_ylabel('Pct.')
#ax.set_xlabel(None)
#ax.spines['right'].set_visible(False)
#ax.spines['top'].set_visible(False)
#ax.spines['left'].set_visible(False)
#ax.spines['bottom'].set_visible(False)
#ax.set_xticklabels( rotation=45, rotation_mode="anchor")
#ax.yaxis.set_ticks_position('left')
#ax.xaxis.set_ticks_position('bottom')
dfDaab['Daab'].plot(label=sognDaab)
dfDaab['DaabDK'].plot(label='Danmark')
ax.legend()
plt.show()