import requests
import pandas as pd
from sklearn import preprocessing
import itertools
import numpy as np
from scipy.spatial.distance import pdist, squareform
import random


#Normalize data frame where song features are stored
def normalizeDf(df):
	min_max_scaler = preprocessing.MinMaxScaler()
	for i in allFeatures: #Change for general df
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
    dist = pdist([song1,song2],'minkowski',1)[0] #taxicab
    return max(1.5-dist,0)


#Gives a random walk over k steps. Will not repeat the last r responses.
#Array needs to be n*n and r<n.
def randomWalk(weightArray,startIndex=0,k=100,r=0):
    walkPath = np.zeros((k,), dtype=np.int)
    walkPath[0] = startIndex
    for i  in range(1,k):
        walkWeights = weightArray[int(walkPath[i-1])]
        #Remove last r songs
        for j in range(max(i-r,0),i):
            walkWeights[walkPath[j]] = 0
        walkPath[i] = weightedChoice(walkWeights)
    return walkPath

#Defines a choce function given weights. TODO make more varied weight functions
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


#Creates a song list given a random walk on df
def toSongList(randomWalk, df):
	songList = []
	for i in range(len(randomWalk)):
		songList += [df.ix[int(randomWalk[i])].name]
	return songList

# featuredPlaylists = requests.get("https://api.spotify.com/v1/browse/featured-playlists", headers=access_header).json()["playlists"]["items"]
# allFeaturedPlaylistData = {}
# for i in featuredPlaylists:
# 	tracks = requests.get(i["href"] + "/tracks", headers=access_header).json()["items"]
# 	tracksList = []
# 	for j in tracks:
# 		tracksList.append(j["track"]["id"])
# 	allFeaturedPlaylistData[i["id"]] = gd.getSongs(tracksList)


#To pass in data, pass in a df with song ids and normalized data
allFeatures = ["danceability", "energy", "key", "loudness", "speechiness", "acousticness",
				 "instrumentalness", "liveness", "valence", "tempo", "time_signature"]

df = pd.read_csv('song-data-unique.csv')
del df['category']
del df['popularity']
ndf = normalizeDf(df)

#Getting some demo code to run
wa = createWeightArray(ndf.ix[:150])
rw = randomWalk(wa, r = 10)
sl = toSongList(rw,ndf)

print(sl)
print(rw)

print("mean: ", np.mean(wa))
print("variance: ", np.var(wa))
print("elements > 0: ", len(wa[wa > 0]))
