#!/usr/bin/env python3
######################

import requests
import os
import json

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np

from sklearn.neighbors import NearestNeighbors

import getData

style.use("ggplot")

accessToken = "BQDIvDu2Q4Pvea8pAvkzKiL1VdgiBRdrIvVuWcIqwrn97Lxb_zKF09JWDshpwrEqPDbbHwFDRNgwHWRB3ulxvZnXWgxx8xlF1qXoait-Z5rt5vTuue1RB42xX7iwxFl_RXGhNN4FC7BG6ae-_vuScosEdsC6LKBz6yUEaY8V0pDGmh_3Rw1K9Wxm_P1jxA"

userID = "kaizentowfiq"

def getData(userID, accessToken):
	savedTracks = []
	request = "https://api.spotify.com/v1/me/tracks?limit=50"
	s = requests.Session()
	s.headers.update({'Authorization':'Bearer ' + accessToken})
	resp = s.get(request)
	if resp.status_code == 200:
		messySavedTracks = resp.json()["items"]
		for i in messySavedTracks:
			savedTracks.append(str(i["track"]["id"]))
	
	# now we collect playlists and their ids
	request = "https://api.spotify.com/v1/users/" + userID + "/playlists"
	s = requests.Session()
	s.headers.update({'Authorization':'Bearer ' + accessToken})
	resp = s.get(request)
	if resp.status_code == 200:
		messyPlaylists = resp.json()["items"]
		playlistSongs = {}
		playlistID = {}
		for i in messyPlaylists:
			playlistSongs[str(i["name"])] = []
			playlistID[str(i["name"])] = str(i["id"])
		
		# now we collect the songs within each playlist
		for i in playlistID.keys():
			request = "https://api.spotify.com/v1/users/" + userID + "/playlists/" + playlistID[i] + "/tracks"
			s = requests.Session()
			s.headers.update({'Authorization':'Bearer ' + accessToken})
			resp = s.get(request)
			if resp.status_code == 200:
				messySongs = resp.json()["items"]
				for j in messySongs:
					playlistSongs[i].append(str(j["track"]["id"]))
		playlistSongs["savedTracks"] = savedTracks
		playlistID["savedTracks"] = "savedTracks"
	
	#remove empty playlists
	toRemove = []
	for i in playlistID.keys():
		if playlistSongs[i] == []:
			toRemove.append(i)
	
	for i in toRemove:
		playlistSongs.pop(i)
		playlistID.pop(i)
	
	#https://api.spotify.com/v1/audio-features?ids=id1,id2,id3...
	playlistSongFeatures = {}
	for i in playlistID.keys():
		queryString = ",".join(playlistSongs[i])
		request = "https://api.spotify.com/v1/audio-features?ids=" + queryString
		s = requests.Session()
		s.headers.update({'Authorization':'Bearer ' + accessToken})
		resp = s.get(request)
		messyPlaylistSongFeatures = resp.json()["audio_features"]
		playlistSongFeatures[i] = {}
		for song in messyPlaylistSongFeatures:
			playlistSongFeatures[i][song["id"]] = song
	return playlistID, playlistSongs, playlistSongFeatures

def playlistToDataFrame(playlistName, playlistSongList, playlistSongFeatures):
	songList = playlistSongList
	preDataFrameDict = {}
	preDataFrameDict = {"Song":[],
						"acousticness":[],
						"danceability":[],
						"energy":[],
						"instrumentalness":[],
						"liveness":[],
						"loudness":[],
						"speechiness":[],
						"tempo":[],
						"valence":[]}
	for i in songList:
		preDataFrameDict["Song"].append(songList.index(i))
		preDataFrameDict["acousticness"].append(playlistSongFeatures[i]["acousticness"])
		preDataFrameDict["danceability"].append(playlistSongFeatures[i]["danceability"])
		preDataFrameDict["energy"].append(playlistSongFeatures[i]["energy"])
		preDataFrameDict["instrumentalness"].append(playlistSongFeatures[i]["instrumentalness"])
		preDataFrameDict["liveness"].append(playlistSongFeatures[i]["liveness"])
		preDataFrameDict["loudness"].append(playlistSongFeatures[i]["loudness"])
		preDataFrameDict["speechiness"].append(playlistSongFeatures[i]["speechiness"])
		preDataFrameDict["tempo"].append(playlistSongFeatures[i]["tempo"])
		preDataFrameDict["valence"].append(playlistSongFeatures[i]["valence"])
	df = pd.DataFrame(preDataFrameDict)
	return df.set_index("Song")

#getting data to play with
playlistIDs, playlistSongs, playlistSongFeatures = getData(userID, accessToken)

#example of basic visual
#DeathflowFrame = playlistToDataFrame("Deathflow", playlistSongs["Deathflow"], playlistSongFeatures["Deathflow"])
#DeathflowFrame[["acousticness","danceability","energy"]].plot.area()
#plt.show()

SavedTracksFrame = playlistToDataFrame("savedTracks", playlistSongs["savedTracks"], playlistSongFeatures["savedTracks"])
SavedTracksFrame[["acousticness","danceability","energy"]].plot.area()
plt.show()

# using KNN to determine which playlist a song belongs in
# to do this i will average the song features of each playlist dataframe and construct
# a new dataframe where the index is the playlist and the features are the averaged features of the 
# songs in each playlist, then see what the nearest neighbors of a given song are in that dataframe
playlists = []
for i in sorted(playlistIDs.keys()):
	playlists.append(playlistToDataFrame(i, playlistSongs[i], playlistSongFeatures[i]))

def playlistDataFramesToAveragedDataFrame(playlists):
	preDataFrameDict = {"Playlist":[],
						"acousticness":[],
						"danceability":[],
						"energy":[],
						"instrumentalness":[],
						"liveness":[],
						"loudness":[],
						"speechiness":[],
						"tempo":[],
						"valence":[]}
	for i in range(0, len(playlists)):
		preDataFrameDict["Playlist"].append(i)
		preDataFrameDict["acousticness"].append(playlists[i]["acousticness"].mean())
		preDataFrameDict["danceability"].append(playlists[i]["danceability"].mean())
		preDataFrameDict["energy"].append(playlists[i]["energy"].mean())
		preDataFrameDict["instrumentalness"].append(playlists[i]["instrumentalness"].mean())
		preDataFrameDict["liveness"].append(playlists[i]["liveness"].mean())
		preDataFrameDict["loudness"].append(playlists[i]["loudness"].mean())
		preDataFrameDict["speechiness"].append(playlists[i]["speechiness"].mean())
		preDataFrameDict["tempo"].append(playlists[i]["tempo"].mean())
		preDataFrameDict["valence"].append(playlists[i]["valence"].mean())
	df = pd.DataFrame(preDataFrameDict)
	return df.set_index("Playlist")

averagedPlaylistsFrame = playlistDataFramesToAveragedDataFrame(playlists)
def nearestPlaylistForSong(song, averagedPlaylistsFrame, playlists):
	nn = NearestNeighbors(3)
	nn.fit(averagedPlaylistsFrame)
	indexList = nn.kneighbors(np.array(song).reshape(1,-1), 3)[1]
	top3PlaylistIDs = []
	for i in indexList[0]:
		top3PlaylistIDs.append(sorted(playlistIDs.keys())[i])
	return top3PlaylistIDs

features = ["acousticness","danceability","energy","instrumentalness","liveness","loudness","speechiness","tempo","valence"]
song = []
#for i in features:
#	song.append(playlistSongFeatures["Deathflow"]["3eqEq53sUsaukd560hw7Dh"][i])
for i in features:
	song.append(playlistSongFeatures["Trueflow"]["26pYZfK8RSln7Etk4OTFuR"][i])

nearestPlaylists = nearestPlaylistForSong(song, averagedPlaylistsFrame, playlistIDs)

for i in nearestPlaylists:
	print(i)
