import pdb
from random import shuffle
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
	features = ["popularity", "danceability", "energy", "loudness", "speechiness", "acousticness",
							 "instrumentalness", "liveness", "valence", "tempo"]
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
	for k in list(range(0,len(classes))):
		count += 1
		if k < len(ordered_keys):
			print("Prediction " + str(count) + ":"  + connected[ordered_keys[k]] + " (" + str(ordered_keys[k]) + ")")
	print("="*100)

if __name__ == '__main__':
	fileObject = open(sys.argv[1],'rb')
	classifier = pickle.load(fileObject)

	#song ids from playlist
	sid = sys.argv[2]

	#song ids from test set
	test_set = pd.read_csv('song-data-te.csv')
	categories = ['Jazz', 'Hip-Hop', 'Metal', 'Electronic/Dance', 'Pop']

	test_group = test_set.groupby(['category'])

	te_list = []

	song_df = songDataFrame(sid)

	printResults(song_df, classifier)
