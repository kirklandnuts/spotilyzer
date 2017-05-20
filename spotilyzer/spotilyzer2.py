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

import base64

import asyncio
import aiohttp

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
#playlistIDs, playlistSongs, playlistSongFeatures = getData(userID, accessToken)

#example of basic visual
#DeathflowFrame = playlistToDataFrame("Deathflow", playlistSongs["Deathflow"], playlistSongFeatures["Deathflow"])
#DeathflowFrame[["acousticness","danceability","energy"]].plot.area()
#plt.show()

#SavedTracksFrame = playlistToDataFrame("savedTracks", playlistSongs["savedTracks"], playlistSongFeatures["savedTracks"])
#SavedTracksFrame[["acousticness","danceability","energy"]].plot.area()
#plt.show()

# using KNN to determine which playlist a song belongs in
# to do this i will average the song features of each playlist dataframe and construct
# a new dataframe where the index is the playlist and the features are the averaged features of the 
# songs in each playlist, then see what the nearest neighbors of a given song are in that dataframe
#playlists = []
#for i in sorted(playlistIDs.keys()):
#	playlists.append(playlistToDataFrame(i, playlistSongs[i], playlistSongFeatures[i]))

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

#averagedPlaylistsFrame = playlistDataFramesToAveragedDataFrame(playlists)
def nearestPlaylistForSong(song, averagedPlaylistsFrame, playlists):
	nn = NearestNeighbors(3)
	nn.fit(averagedPlaylistsFrame)
	indexList = nn.kneighbors(np.array(song).reshape(1,-1), 3)[1]
	top3PlaylistIDs = []
	for i in indexList[0]:
		top3PlaylistIDs.append(sorted(playlistIDs.keys())[i])
	return top3PlaylistIDs

#features = ["acousticness","danceability","energy","instrumentalness","liveness","loudness","speechiness","tempo","valence"]
#song = []
#for i in features:
#	song.append(playlistSongFeatures["Deathflow"]["3eqEq53sUsaukd560hw7Dh"][i])
#for i in features:
#	song.append(playlistSongFeatures["Trueflow"]["26pYZfK8RSln7Etk4OTFuR"][i])

#nearestPlaylists = nearestPlaylistForSong(song, averagedPlaylistsFrame, playlistIDs)

#for i in nearestPlaylists:
#	print(i)

def getFeaturedPlaylists():
	# Get an access token
	TOKEN_URL = "https://accounts.spotify.com/api/token"
	CLIENT_ID = "fa7e7c8d114a487c81a31a32dd0c0ef5"
	CLIENT_SECRET = "7df74727c0a846b1ba7bf042f9421f6c"
	DATA = {"grant_type":"client_credentials"}
	temp1 = CLIENT_ID+":"+CLIENT_SECRET
	temp2 = temp1.encode('utf-8','strict')
	HEADER_64_STRING = base64.b64encode(temp2)
	HEADERS = {"Authorization":b"Basic "+HEADER_64_STRING}
	response = requests.post(TOKEN_URL, data=DATA, headers=HEADERS)
	response.content
	access_token = response.json()['access_token']
	access_headers = {"Authorization":"Bearer "+access_token}

	# Request featured playlists
	access_headers = {"Authorization":"Bearer "+access_token}
	featuredPlaylistsResponse = requests.get("https://api.spotify.com/v1/browse/featured-playlists", headers=access_headers)

	# Convert to dataframe
	df = pd.DataFrame(featuredPlaylistsResponse.json()["playlists"]["items"])

	# Get a list of tracks in each playlist, then add a list of their id's to a new column
	df['trackslist'] = ""
	df['trackslist'] = df['trackslist'].astype(object)
	for index, row in df.iterrows():
	    tracks = requests.get(row['href']+'/tracks', headers=access_headers)
	    throwaway = df.set_value(index, 'trackslist', [ item['track']['id'] for item in tracks.json()['items'] ] )
	df = df.drop('collaborative', 1)
	df = df.drop('external_urls', 1)
	df = df.drop('href', 1)
	df = df.drop('public', 1)
	df = df.drop('snapshot_id', 1)
	df = df.drop('type', 1)
	#for i in range(0,len(df["trackslist"])-1):
	for i in range(0,3):
		newTracksList = []
		for sid in df["trackslist"][i]:
			resp = requests.get("https://api.spotify.com/v1/audio-features/"+sid, headers=access_headers).json()
			newTracksList.append(resp)
		df["trackslist"][i] = newTracksList
	return df

masterFrame = getFeaturedPlaylists()
import pdb
pdb.set_trace()
