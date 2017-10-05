import pdb
import sys
import pandas as pd
import pickle
import getData as gd
#USAGE: python Demo.py songid model
#input songid
#output genre 


SONGID = sys.argv[1]

def songDataFrame(songid):
	features = ["popularity", "danceability", "energy", "key", "loudness", "speechiness", "acousticness",\
			"instrumentalness", "liveness", "valence", "tempo", "time_signature"]
	data = gd.getSongs([songid])[0]
	pre_frame_d = {}
	for f in features:
		pre_frame_d[f] = data[f]
	df = pd.DataFrame(index=[0], data=pre_frame_d)
	return df

song_df = songDataFrame(SONGID)
fileObject = open(sys.argv[2],'rb')  
classifier = pickle.load(fileObject)  

prediction = classifier.predict(song_df)

print("Prediction: " + prediction)

