import pdb
import requests
import sys
import pandas as pd
import pickle
import getData as gd
#USAGE: python Demo.py songid model
#input songid
#output genre 

ACCESS_HEADER = gd.getAccessHeader()

def songDataFrame(songid):
	features = ["popularity", "danceability", "energy", "key", "loudness", "speechiness", "acousticness",\
			"instrumentalness", "liveness", "valence", "tempo", "time_signature"]
	data = gd.getSongs([songid])[0]
	pre_frame_d = {}
	for f in features:
		pre_frame_d[f] = data[f]
	df = pd.DataFrame(index=[0], data=pre_frame_d)
	return df

def getPlaylistSongIDs(access_header):
	url = "https://api.spotify.com/v1/users/12139793063/playlists/21kX3cArKDRsEKpJOS7NBi/tracks"
	resp = requests.get(url, headers=access_header)
	songIDs = []
	if resp.status_code == 200:
		for i in resp.json()["items"]:
			songIDs.append(i["track"]["id"])
	return songIDs

def printResults(df, clf):
	classes = clf.classes_
	probs = classifier.predict_proba(song_df)[0]
	connected = {}
	for i in list(range(0,len(classes))):
		connected[probs[i]] = classes[i]
	ordered_keys = sorted(connected.keys(), reverse=True)
	count = 0
	for k in list(range(0,3)):
		count += 1
		print("Prediction " + str(count) + ":"  + connected[ordered_keys[k]])
	print("="*100)

fileObject = open(sys.argv[2],'rb')  
classifier = pickle.load(fileObject)  
song_ids = getPlaylistSongIDs(ACCESS_HEADER)
for sid in song_ids:
	if sid is not None:
		song_df = songDataFrame(sid)
		printResults(song_df, classifier)
