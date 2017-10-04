import getData as gd
import requests
import pandas as pd
from sklearn import preprocessing
import itertools
import numpy as np
from scipy.spatial.distance import pdist, squareform
import random

#Creates data frame where song features are stored
def createDataFrame(afpd, features):
	preFrameDict = {}
	for i in features:
		preFrameDict[i] = []
	preFrameDict["songid"] = []
	for i in sorted(afpd.keys()):
		for j in afpd[i]:
			preFrameDict["songid"].append(j["songid"])
			for q in features:
				preFrameDict[q].append(j[q])
	df = pd.DataFrame(preFrameDict)
	#normalize data
    #May have to be changed for future distance functions
	min_max_scaler = preprocessing.MinMaxScaler()
	for i in features:
		df[i] = pd.DataFrame(min_max_scaler.fit_transform(df[i]))
	return df.set_index("songid")

#Creates an n*n array that corresponds to weights on how close 2 songs are
#The ith row and jth column corresponds to relation from the ith song to the jth song
def createWeightArray(df):
    weightArray = np.zeros((df.shape[0],df.shape[0]))
    #Probabilistic weight for song i -> song j
    for i in range(df.shape[0]):
        for j in range(df.shape[0]):
            weightArray[i][j] = songWeight(df.ix[i],df.ix[j])
            if (i == j):
                weightArray[i][j] = 0

    return weightArray



#Gives a weight for song1 -> song2 based off of their distance. Song 1 and 2 are arrays of numbers.
#TODO add different weight functions
def songWeight(song1,song2):
    dist = pdist([song1,song2],'minkowski',1)[0] #Taxicab
    return max(1.5-dist,0)


#Gives a random walk over k steps. Will not repeat the last r responses.
#Array needs to be n*n and r<n.
def randomWalk(weightArray,startIndex=0,k=100,r=0):
    walkPath = np.zeros(k)
    walkPath[0] = startIndex
    for i  in range(1,k):
        walkWeights = weightArray[walkPath[i-1]]
        #Remove last r songs
        for j in range(max(i-r,0),i):
            walkWeights[walkPath[j]] = 0
        walkPath[i] = weightedChoice(walkWeights)
    return walkPath


def weightedChoice(weights):
    totalWeight = np.sum(weights)
    if totalWeight == 0:
        return random.randint(0,len(weights))
    #Subtract the weight from choice at each step and return the song it gets below 0 at
    choice = random.random() * totalWeight
    for i in range(len(weights)):
        choice -= weights[i]
        if choice <= 0:
            return i
    return len(weights) - 1


access_header = gd.getAccessHeader()

featuredPlaylists = requests.get("https://api.spotify.com/v1/browse/featured-playlists", headers=access_header).json()["playlists"]["items"]
allFeaturedPlaylistData = {}
for i in featuredPlaylists:
	tracks = requests.get(i["href"] + "/tracks", headers=access_header).json()["items"]
	tracksList = []
	for j in tracks:
		tracksList.append(j["track"]["id"])
	allFeaturedPlaylistData[i["id"]] = gd.getSongs(tracksList)

allFeatures = ["danceability", "energy", "key", "loudness", "speechiness", "acousticness",
				 "instrumentalness", "liveness", "valence", "tempo", "time_signature"]

playlists = sorted(list(allFeaturedPlaylistData.keys()))
df = createDataFrame(allFeaturedPlaylistData, allFeatures)
wa = createWeightArray(df.ix[:300])
rw = randomWalk(wa)
