import requests
import os
import json

accessToken = "BQDpzz-Ai9UvNGRPfjG1vqUWhNx1zT1xq7iXCOxgxiTA49rIwDV6Ziw-DVR5LX8qJ8-4Oi90H2WwQ4wR4o435dWe_cAZJNNz-x2JQa15qfwv3SKIHatkv7ql82n2XR74RZ6Gz-CbezlgMxvjO65VkhF3B2qHYnEgnQnC-Ea6FzBOuXNXn94hO1iJfUT_MA"

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
