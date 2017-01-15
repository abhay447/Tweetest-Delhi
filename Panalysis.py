import pandas as pd
import pickle
import matplotlib.pyplot as plt

with open('Result.txt', 'rb') as handle:
    myDict = pickle.load(handle)
handle.close()
df = pd.DataFrame(list(myDict.iteritems()),columns=['word','times'])
df.loc[df['word']=='#','times'] = 0
df = df.sort(['times'],ascending=[False])
df.reset_index(drop=True)
sdf = df[0:50]
ax = sdf.plot(kind='bar', title ="Topics", x='word', y='times')
ax.set_xlabel("Topic", fontsize=12)
ax.set_ylabel("Count", fontsize=12)
plt.tight_layout()
plt.show()