import pdb
import sys
import pandas as pd
import pickle
import getData as gd
#USAGE: python Demo.py songid model
#input songid
#output genre 


SONGID = sys.argv[1]
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
    url = "GET https://api.spotify.com/v1/users/12139793063/playlists/21kX3cArKDRsEKpJOS7NBi/tracks"
    resp = requests.get(url, headers=access_header)
    songIDs = []
    if resp.status_code == 200:
        for i in resp.json()["tracks"]["items"]:
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
	for k in ordered_keys:
		count += 1
		print("Prediction " + str(count) + ":"  + connected[k])

fileObject = open(sys.argv[2],'rb')  
classifier = pickle.load(fileObject)  

song_df = songDataFrame(SONGID)

song_ids = getPlaylistSongIDs(ACCESS_HEADER)

import pdb
pdb.set_trace()
printResults(song_df, classifier)
