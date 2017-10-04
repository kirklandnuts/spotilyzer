import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv('song-data.csv')
df = df.drop_duplicates(df.columns.difference(['category']), keep = False)


genres = df.groupby(['category'])
genre_names = list(genres.groups.keys())

tr_list = []
te_list = []

for genre in genre_names:
    gdf = genres.get_group(genre)
    tr, te = train_test_split(gdf, train_size = 0.8)
    tr_list.append(tr)
    te_list.append(te)

tr = pd.concat(tr_list)
te = pd.concat(te_list)

df.to_csv('song-data-unique.csv', index = False)
tr.to_csv('song-data-tr.csv', index = False)
te.to_csv('song-data-te.csv', index = False)
