import pdb
import requests
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
	features = ["popularity", "danceability", "energy", "loudness", "speechiness", "acousticness",\
			"instrumentalness", "liveness", "valence", "tempo"]
	data = gd.getSongs([songid])[0]
	pre_frame_d = {}
	for f in features:
		pre_frame_d[f] = data[f]
	df = pd.DataFrame(index=[0], data=pre_frame_d)
	return df

def printResults(df, clf):
	classes = clf.classes_
	prediction = classifier.predict(song_df)
	if prediction == 'Jazz':
		print("This is Jazz")
	else:
		print("This is not Jazz")
	print("="*100)

fileObject = open(sys.argv[2],'rb')  
classifier = pickle.load(fileObject)  

song_df = songDataFrame(SONGID)
printResults(song_df, classifier)
