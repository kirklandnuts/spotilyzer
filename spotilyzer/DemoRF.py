#!/usr/bin/env python3
######################
#Kaizen Towfiq

import getData as gd
import requests
import pickle
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
from sklearn import preprocessing
from sklearn.decomposition import PCA
from matplotlib import style
import itertools
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve # ROC Curves
from sklearn.metrics import auc # Calculating AUC for ROC's!
import plotly.plotly as py
import plotly.graph_objs as go


def PCAOnDataFrame(training_set, test_set, features, components):
    pca = PCA(n_components=components, random_state=7)
    pca.fit(training_set[features])
    training_set_pca = pca.fit_transform(training_set[features])
    components_col = [x for x in range(0, components)]
    training_set = pd.DataFrame(training_set_pca, columns = components_col)

    test_set_pca = pca.transform(test_set[features])
    test_set = pd.DataFrame(test_set_pca, columns = components_col)
    return training_set, test_set, components_col

def predictCategoryRF(training_set, test_set,  target, test_targert, componentsList, estimators):
	#scale
	scaler = StandardScaler()
	scaler.fit(training_set[componentsList])
	training_set[componentsList] = scaler.transform(training_set[componentsList])
	test_set[componentsList] = scaler.transform(test_set[componentsList])

	#PCA
	training_set, test_set, componentsList = PCAOnDataFrame(training_set, test_set, componentsList, 3)
	import pdb
	pdb.set_trace()

	classifier = RandomForestClassifier(max_features=None, n_estimators=estimators)
	classifier.fit(training_set[componentsList], target)
	file_Name = "jazz_or_not_RF.pickle"
	fileObject = open(file_Name,'wb')
	pickle.dump(classifier,fileObject)   
	fileObject.close()
	return classifier.predict(test_set[componentsList]), test_targert, classifier.score(test_set[componentsList], test_targert)

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

predictions, correctValues, score = predictCategoryRF(training_set, test_set, target, test_target, allFeatures, 5000)

print(pd.crosstab(predictions, correctValues,
                  rownames=['Predicted Values'],
                  colnames=['Actual Values']))

print("Score: " + str(score))
