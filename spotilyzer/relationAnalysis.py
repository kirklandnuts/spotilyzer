#!/usr/bin/env python3
######################
#Setup (Copy/pasted from Kaizen KNN code)

import getData as gd
import requests
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
from sklearn import preprocessing
from sklearn.decomposition import PCA
from matplotlib import style
import itertools
import numpy as np

style.use("ggplot")

#20 different colors for graphing
COLORS = itertools.cycle(["#f4c242", "#61a323", "#161efc", "#cc37c7",
			"#ff0000", "#f6ff05", "#000000", "#706c6c",
			"#7200ff", "#4d8e82", "#c1fff3", "#7a89e8",
			"#82689b", "b", "g", "r", "c", "m", "y", "w",])

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


def createDataFrame(afpd, features):
	preFrameDict = {}
	#Create dict of lists
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

allFeatures = ["popularity", "danceability", "energy", "key", "loudness", "speechiness", "acousticness",
				 "instrumentalness", "liveness", "valence", "tempo", "time_signature"]

playlists = sorted(list(allFeaturedPlaylistData.keys()))
df = createDataFrame(allFeaturedPlaylistData, allFeatures)

########## Alex data analysis

#df dataframe, categories a a list of lists of songs in each category
#components number of end components
#Do a weighted PCA with mean and variance of each feature in each category
#e.g. do PCA on categories rather than aggregate songs to get better results
def PCAOnCategories(df, features, categories, components):

    #Create new dict of values, corresponding to the mean of each category
    #Same thing as dataframe, but with averages of features in each category
    #instead of song data
    category_means = {}
    for feature in features:
        feature_averages = []
        for i in list(range(0,len(playlists))):
            #category a list of song ids of songs in category
            #Temporarily using playlists (Will change to looking up songid in category in the future)
            category_feature_data = df[df["playlist"] == playlists[i]][feature]
            feature_mean = np.mean(category_feature_data)
            feature_averages += [feature_mean]
        category_means[feature] = feature_averages
    cmdf = pd.DataFrame(category_means)
    #import pdb
    #pdb.set_trace()

	#Fit data
    pca = PCA(n_components=components)
    pca.fit(cmdf[features])
    newData = pca.transform(df[features])

    preFrameDict = {}
    preFrameDict["songid"] = []
    preFrameDict["playlist"] = []
    for i in list(range(1,components+1)):
    	preFrameDict[str(i)] = []
    for i in list(range(0, len(newData))):
        preFrameDict["songid"].append(df.index.tolist()[i])
        preFrameDict["playlist"].append(df["playlist"][i])
        for j in list(range(0,components)):
            preFrameDict[str(j+1)].append(newData[i][j])

    newDataFrame = pd.DataFrame(preFrameDict)
	#normalize data
    min_max_scaler = preprocessing.MinMaxScaler()
    for i in list(range(1,components+1)):
        newDataFrame[str(i)] = pd.DataFrame(min_max_scaler.fit_transform(newDataFrame[str(i)]))
    return newDataFrame.set_index("songid")

### Using Kaizen plotting methods
def graph2DPlaylistsDifferentColors(df, features, playlists):
	if len(features) == 2:
		for i in list(range(0,len(playlists))):
			pdf = df[df["playlist"] == playlists[i]]
			xs = pdf[features[0]]
			ys = pdf[features[1]]
			plt.scatter(xs, ys, color=next(COLORS), marker='o')
		plt.xlabel = features[0]
		plt.ylabel = features[1]
		plt.show()
	else:
		print("need 2 features to do 3D graph")

def graph3DPlaylistsDifferentColors(df, features, playlists):
	if len(features) == 3:
		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')
		for i in list(range(0,len(playlists))):
			pdf = df[df["playlist"] == playlists[i]]
			xs = pdf[features[0]]
			ys = pdf[features[1]]
			zs = pdf[features[2]]
			ax.scatter(xs, ys, zs, c=next(COLORS), marker='o')

		ax.set_xlabel(features[0])
		ax.set_ylabel(features[1])
		ax.set_zlabel(features[2])
		plt.show()
	else:
		print("need 3 features to do 3D graph")


#pcadf = PCAOnDataFrame(df, allFeatures, 2)
#graph2DPlaylistsDifferentColors(pcadf, ['1','2'], playlists)
#pcadf = PCAOnDataFrame(df, allFeatures, 3)
#graph3DPlaylistsDifferentColors(pcadf, ['1','2', '3'], playlists)
#graph3DPlaylistsDifferentColors(df, ['popularity','danceability', 'loudness'], playlists)
#graph3DPlaylistsDifferentColors(df, ['acousticness','instrumentalness', 'valence'], playlists)

pcadf = PCAOnCategories(df, allFeatures, playlists, 2)
graph2DPlaylistsDifferentColors(pcadf, ['1','2'], playlists[0:10])

pcadf = PCAOnCategories(df, allFeatures, playlists, 3)
graph3DPlaylistsDifferentColors(pcadf, ['1','2','3'], playlists[0:10])

#pcadf = PCAOnDataFrame(df, allFeatures, 3)
#graph3DPlaylistsDifferentColors(pcadf, ['1','2', '3'], playlists[0:5])
