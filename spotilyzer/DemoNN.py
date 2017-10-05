#!/usr/bin/env python3
######################
#Kaizen Towfiq

import getData as gd
import pandas as pd
from sklearn import preprocessing
from sklearn.neural_network import MLPClassifier
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sknn.mlp import Classifier, Layer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split


def predictCategoryRF(training_set, test_set,  target, test_targert, componentsList, estimators):
	classifier = RandomForestClassifier(max_features=None, n_estimators=estimators)
	classifier.fit(training_set[componentsList], target)
	return test_set, classifier.predict(test_set[componentsList]), test_targert, classifier.score(test_set[componentsList], test_targert)

def predictCategoryKNN(training_set, test_set,  target, test_targert, componentsList, k):
	scaler = StandardScaler()
	scaler.fit(training_set[componentsList])
	training_set[componentsList] = scaler.transform(training_set[componentsList])
	test_set[componentsList] = scaler.transform(test_set[componentsList])
	classifier = KNeighborsClassifier(n_neighbors=k, metric='minkowski')
	classifier.fit(training_set[componentsList], target)
	return test_set, classifier.predict(test_set[componentsList]), test_targert, classifier.score(test_set[componentsList], test_targert)

def predictCategoryNN(training_set, test_set,  target, test_targert, componentsList):
	scaler = StandardScaler()
	scaler.fit(training_set[componentsList])
	training_set[componentsList] = scaler.transform(training_set[componentsList])
	test_set[componentsList] = scaler.transform(test_set[componentsList])
	nn = Classifier(
	layers=[
	Layer("Sigmoid", units=100),
	Layer("Softmax")],
	learning_rate=0.001,
	n_iter=25)
	nn.fit(training_set[componentsList].as_matrix(), target.as_matrix())
	return nn.predict(test_set[componentsList].as_matrix()), pd.DataFrame(test_targert), nn.score(test_set[componentsList].as_matrix(), test_targert.as_matrix())
	#mlp = MLPClassifier(hidden_layer_sizes=(13,13,13), max_iter=500)
	#mlp.fit(training_set[componentsList], target)
	#return test_set, mlp.predict(test_set[componentsList]), test_targert, mlp.score(test_set[componentsList], test_targert)

#def predictCategoryNN(training_set, test_set,  target, test_targert, componentsList):
#	scaler = StandardScaler()
#	scaler.fit(training_set[componentsList])
#	training_set[componentsList] = scaler.transform(training_set[componentsList])
#	test_set[componentsList] = scaler.transform(test_set[componentsList])
#	fc = skflow.infer_real_valued_columns_from_input(training_set[componentsList])
#	# Jazz = 1
#	# Rock = 2
#	training_set.category = training_set.category.replace('Jazz', 1)
#	training_set.category = training_set.category.replace('Rock', 2)
#	test_set.replace('Jazz', 1)
#	test_set.replace('Rock', 2)
#	target = training_set['category']
#	test_target = test_set['category']
#	mlp = skflow.DNNClassifier(hidden_units=[10, 20, 10], feature_columns=fc, n_classes=2)
#	mlp.fit(training_set[componentsList], target)
#	return test_set, mlp.predict(test_set[componentsList]), test_targert, mlp.score(test_set[componentsList], test_targert)

categories = ['Jazz', 'Rock']#, 'Hip-Hop', 'Metal', 'Electronic/Dance', 'Pop', 'Indie']
allFeatures = ["popularity", "danceability", "energy", "key", "loudness", "speechiness", "acousticness",
				 "instrumentalness", "liveness", "valence", "tempo", "time_signature"]

test_set = pd.read_csv('song-data-te.csv')
training_set = pd.read_csv('song-data-tr.csv')
training_group = training_set.groupby(['category'])
test_group = test_set.groupby(['category'])

tr_list = []
te_list = []

for genre in categories:
	tr_list.append(training_group.get_group(genre))
	te_list.append(test_group.get_group(genre))

training_set = pd.concat(tr_list)
test_set = pd.concat(te_list)
target = training_set['category']
test_target = test_set['category']

predictions, correctValues, score = predictCategoryNN(training_set, test_set, target, test_target, allFeatures)
#testdf, predictions, correctValues, score = predictCategoryKNN(training_set, test_set, target, test_target, allFeatures, 83)

print("Score: " + str(score))
