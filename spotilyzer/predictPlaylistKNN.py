#!/usr/bin/env python3
######################

import getData as gd
import requests
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
from sklearn import preprocessing

#getSongs test
access_header = gd.getAccessHeader()

featuredPlaylists = requests.get("https://api.spotify.com/v1/browse/featured-playlists", headers=access_header).json()["playlists"]["items"]
allFeaturedPlaylistData = {}
for i in featuredPlaylists:
	tracks = requests.get(i["href"] + "/tracks", headers=access_header).json()["items"]
	tracksList = []
	for j in tracks:
		tracksList.append(j["track"]["id"])
	allFeaturedPlaylistData[i["id"]] = gd.getSongs(tracksList)

#The goal of this analysis is to predict which playlist a given song belongs to using KNN
#will use 3 features of the songs, randomly choosing danceability, instrumentalness, speechiness

def createDataFrame(afpd, features):
	preFrameDict = {"songid":[],
					"danceability":[],
					"instrumentalness":[],
					"speechiness":[],
					"playlist":[],}
	for i in sorted(afpd.keys()):
		for j in afpd[i]:
			preFrameDict["playlist"].append(i) 
			preFrameDict["songid"].append(j["songid"]) 
			for q in features:
				preFrameDict[q].append(j[q])
	df = pd.DataFrame(preFrameDict)
	#normalize data
	import pdb
	pdb.set_trace()
	min_max_scaler = preprocessing.MinMaxScaler()
	for i in features:
		df[i] = pd.DataFrame(min_max_scaler.fit_transform(df[i]))
	return df.set_index("songid")

df = createDataFrame(allFeaturedPlaylistData, ["danceability", "instrumentalness", "speechiness"])
# plot songs on a 3D graph with variables danceability, instrumentalness, speechiness
# looks like the 3 features are on the same scale 0-1
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

xs = df["danceability"]
ys = df["instrumentalness"]
zs = df["speechiness"]
ax.scatter(xs, ys, zs, c='r', marker='o')


ax.set_xlabel('danceability')
ax.set_ylabel('instrumentalness')
ax.set_zlabel('speechiness')
plt.show()

df = createDataFrame(allFeaturedPlaylistData, ["", "", ""])
# plot songs on a 3D graph with variables danceability, instrumentalness, speechiness
# looks like the 3 features are on the same scale 0-1
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

xs = df[""]
ys = df[""]
zs = df[""]
ax.scatter(xs, ys, zs, c='r', marker='o')


ax.set_xlabel('')
ax.set_ylabel('')
ax.set_zlabel('')
plt.show()

df = createDataFrame(allFeaturedPlaylistData, ["", "", ""])
# plot songs on a 3D graph with variables danceability, instrumentalness, speechiness
# looks like the 3 features are on the same scale 0-1
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

xs = df[""]
ys = df[""]
zs = df[""]
ax.scatter(xs, ys, zs, c='r', marker='o')


ax.set_xlabel('')
ax.set_ylabel('')
ax.set_zlabel('')
plt.show()

import pdb
pdb.set_trace()
