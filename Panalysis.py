import pandas as pd
import pickle
import matplotlib.pyplot as plt
from pylab import *

with open('Result.txt', 'rb') as handle:
    myDict = pickle.load(handle)
handle.close()
df = pd.DataFrame(list(myDict.iteritems()),columns=['word','times'])
df.loc[df['word']=='#','times'] = 0
df = df.sort(['times'],ascending=[False])
df.reset_index(drop=True)
sdf = df[0:50]

#plot the bar chart for keywords
ax = sdf.plot(kind='bar', title ="Topics", x='word', y='times')
ax.set_xlabel("Topic", fontsize=12)
ax.set_ylabel("Count", fontsize=12)
plt.tight_layout()
plt.show()

#seperate category wise data
mediaTags = ['film','television','video','website','series','channel','network','band','comedy'
             ,'drama','cable','music','fiction']
politicalTags = ['city','republic','leader','country','campaigns','world','land','area',
                 'capital','district','states','territories','region']
millitaryTags = ['millitary','borders','fighter','aircraft','bomber']

mediaCount = sdf.loc[sdf.word.isin(mediaTags),'times'].sum()
politicalCount = sdf.loc[sdf.word.isin(politicalTags),'times'].sum()
millitaryCount = sdf.loc[sdf.word.isin(millitaryTags),'times'].sum()
untaggedCount = sdf.times.sum() - mediaCount - politicalCount - millitaryCount

#pie chart for category wise data
figure(1, figsize=(6,6))
ax = axes([0.1, 0.1, 0.8, 0.8])
labels = 'Media,Movies,Tv', 'Politics', 'Millitary', 'Untagged'
fracs = [mediaCount*100.0/sdf.times.sum(), politicalCount*100.0/sdf.times.sum(),
        millitaryCount*100.0/sdf.times.sum(), untaggedCount*100.0/sdf.times.sum()]
explode=(0, 0.05, 0, 0)
pie(fracs, explode=explode, labels=labels,autopct='%1.1f%%', shadow=True, startangle=90)
title('Keywords by categories', bbox={'facecolor':'0.8', 'pad':5})
show()