import requests
import os
import json

accessToken = "BQA6UxOOy9OIY7QH8pa4nwaCpxtOGLzLiRZ23aXvTzxe8gkq2ZPvqLPjIHQG_yqrivJ8MT9UGkM7IAoofgX0FgW1Mdz1sk-Jh9caxGN9IwSi4qrvPM8tRz8Ra18bWsDRfX3aiVZODJ-31-R25_6q2LTx4tgbBVUYMAQ2xLRVRezMsmMMaTvnurXt9EzTcA"

userID = "kaizentowfiq"

#First we collect saved song ids
savedTracks = []
request = "https://api.spotify.com/v1/me/tracks?limit=50"
s = requests.Session()
s.headers.update({'Authorization':'Bearer ' + accessToken})
resp = s.get(request)
messySavedTracks = resp.json()["items"]

for i in messySavedTracks:
	savedTracks.append(str(i["track"]["id"]))

# now we collect playlists and their ids
request = "https://api.spotify.com/v1/users/" + userID + "/playlists"
s = requests.Session()
s.headers.update({'Authorization':'Bearer ' + accessToken})
resp = s.get(request)

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

# now we save our data to text files for further processing by the unauthorized requests
dirName = userID + "Data"
os.system("mkdir " + dirName)

# we will create the saved Tracks data file first
f = open(dirName + "/" + "savedTracks", 'w')
for id in savedTracks:
	f.write(id + ", ")
f.close()

for i in playlistID.keys():
	f = open(dirName + "/" + i, 'w')
	for id in playlistSongs[i]:
		f.write(id + ", ")
	f.close

