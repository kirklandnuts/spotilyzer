import requests
import json

accessToken = "BQA6UxOOy9OIY7QH8pa4nwaCpxtOGLzLiRZ23aXvTzxe8gkq2ZPvqLPjIHQG_yqrivJ8MT9UGkM7IAoofgX0FgW1Mdz1sk-Jh9caxGN9IwSi4qrvPM8tRz8Ra18bWsDRfX3aiVZODJ-31-R25_6q2LTx4tgbBVUYMAQ2xLRVRezMsmMMaTvnurXt9EzTcA"

userID = "kaizentowfiq"
#playlists = json.loads(os.system(request))
#request = "curl -X GET 'https://api.spotify.com/v1/me/tracks' -H 'Authorization: Bearer " + accessToken +  "' > newData"
#output playlist file that holds song ids
#request = "curl -X GET 'https://api.spotify.com/v1/users/" + userID + "/playlists' -H 'Authorization: Bearer " + accessToken + "'"

#https://api.spotify.com/v1/users/{user_id}/playlists/{playlist_id}/tracks

#First we collect saved song ids

savedTracks = []
request = "https://api.spotify.com/v1/me/tracks?limit=50"
s = requests.Session()
s.headers.update({'Authorization':'Bearer ' + accessToken})
resp = s.get(request)
messySavedTracks = resp.json()["items"]

for i in messySavedTracks:
	savedTracks.append(str(i["track"]["id"]))
#now we collect playlist song ids

request = "https://api.spotify.com/v1/users/" + userID + "/playlists"
s = requests.Session()
s.headers.update({'Authorization':'Bearer ' + accessToken})
resp = s.get(request)

messyPlaylists = resp.json()["items"]
playlists = {}
for i in messyPlaylists:
	playlists[str(i["name"])] = []



