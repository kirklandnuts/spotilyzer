import pandas as pd
import getData as gd

ACCESS_HEADER = gd.getAccessHeader()
categories = list(gd.__getCategories(ACCESS_HEADER).keys())
features = ["popularity", "danceability", "energy", "key", "loudness", "speechiness", "acousticness",
				 "instrumentalness", "liveness", "valence", "tempo", "time_signature"]
cols = ["category", "songid", "popularity", "danceability", "energy", "key", "loudness", "speechiness", "acousticness",
				"instrumentalness", "liveness", "valence", "tempo", "time_signature"]
genres = ['Pop', 'Electronic/Dance', 'Hip-Hop', 'Rock', 'Indie', 'R&B', 'Metal', 'Soul', 'Romance', 'Jazz']


preFrameDict = {}
for i in features:
    preFrameDict[i] = []
preFrameDict["songid"] = []
preFrameDict["category"] = []
for i in categories:
    songs = gd.getSongsInCategory(i)
    for j in songs:
        preFrameDict["category"].append(i)
        preFrameDict["songid"].append(j["songid"])
        for q in features:
            preFrameDict[q].append(j[q])
df = pd.DataFrame(preFrameDict)
df = df[cols]
df = df[df.category.isin(genres)]
df.to_csv('./song-data.csv', index = False)
