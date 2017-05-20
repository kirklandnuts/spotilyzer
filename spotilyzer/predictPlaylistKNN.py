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
	preFrameDict = {}
	for i in features:
		preFrameDict[i] = []
	preFrameDict["songid"] = []
	preFrameDict["playlist"] = []
	for i in sorted(afpd.keys()):
		for j in afpd[i]:
			preFrameDict["playlist"].append(i) 
			preFrameDict["songid"].append(j["songid"]) 
			for q in features:
				preFrameDict[q].append(j[q])
	df = pd.DataFrame(preFrameDict)
	#normalize data
	min_max_scaler = preprocessing.MinMaxScaler()
	for i in features:
		df[i] = pd.DataFrame(min_max_scaler.fit_transform(df[i]))
	return df.set_index("songid")

def graph3DAllNodes(features):
	if len(features) == 3:
		df = createDataFrame(allFeaturedPlaylistData, features)
		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')
		
		xs = df[features[0]]
		ys = df[features[1]]
		zs = df[features[2]]
		ax.scatter(xs, ys, zs, c='g', marker='o')
		
		
		ax.set_xlabel(features[0])
		ax.set_ylabel(features[1])
		ax.set_zlabel(features[2])
		plt.show()
	else:
		print("need 3 features to do 3D graph")

graph3DAllNodes(["danceability", "instrumentalness", "speechiness"])
graph3DAllNodes(["popularity", "energy", "loudness"])
graph3DAllNodes(["acousticness", "liveness", "valence"])
	
import pdb
pdb.set_trace()
