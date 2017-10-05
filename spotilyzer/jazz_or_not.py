import pdb
from sklearn.decomposition import PCA
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
	prediction = classifier.predict(song_df)[0]
	if prediction:
		print("This is Jazz")
	else:
		print("This is not Jazz")
	print("="*100)


def PCAOnDataFrame(df, training_set, features, components):
	pca = PCA(n_components=components, random_state=7)
	pca.fit(training_set[features])
	components_col = [x for x in range(0, components)]	
	training_set_pca = pca.fit_transform(training_set[features])
	sdf = pca.transform(df[features])
	sdf = pd.DataFrame(sdf, columns=components_col)
	return sdf 


categories = ['Jazz', 'Rock', 'Hip-Hop', 'Metal', 'Electronic/Dance', 'Pop']
allFeatures = ["popularity", "danceability", "energy", "loudness", "speechiness", "acousticness",
                 "instrumentalness", "liveness", "valence", "tempo"]

test_set = pd.read_csv('jazz_te.csv')
training_set = pd.read_csv('jazz_tr.csv')
training_group = training_set.groupby(['category'])
test_group = test_set.groupby(['category'])

tr_list = []
te_list = []

for genre in categories:
    tr_list.append(training_group.get_group(genre))
    te_list.append(test_group.get_group(genre))

training_set = pd.concat(tr_list)
test_set = pd.concat(te_list)
target = training_set['jazz']
test_target = test_set['jazz']


fileObject = open(sys.argv[2],'rb')  
classifier = pickle.load(fileObject)  


song_df = songDataFrame(SONGID)
song_df = PCAOnDataFrame(song_df, training_set, allFeatures, 3)

printResults(song_df, classifier)
