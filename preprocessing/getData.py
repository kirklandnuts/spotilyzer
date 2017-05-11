#!/usr/bin/env python3
######################

import requests
import os
import json

accessToken = "BQD6DROn3wWpLZky4CiMgsaLEcI0KMyrAxirfksb4Q6b8I2Ku0BXGCJ0xVZj4RsFtPvXG-1dkIN9w-Q4uffWOXXU2qV3YA9nHhFzi9s6m8Aikh8U9MTDeTQu-Wsixw9sR1Q8j090t85SixLc7KNu_DHRcBH9tlt6aXNIlKKKHlvm_nD0kVcHch5IgKAopA"

userID = "kaizentowfiq"

#First we collect saved song ids
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

# now we save our data to text files for further processing by the unauthorized requests
#dirName = userID + "Data"
#os.system("mkdir " + dirName)

# we will create the saved Tracks data file first
#f = open(dirName + "/" + "savedTracks", 'w')
#for id in savedTracks:
#	f.write(id + ", ")
#f.close()

#for i in playlistID.keys():
#	f = open(dirName + "/" + i, 'w')
#	for id in playlistSongs[i]:
#		f.write(id + ", ")
#	f.close

#https://api.spotify.com/v1/audio-features/{id}

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

import pdb
pdb.set_trace()
