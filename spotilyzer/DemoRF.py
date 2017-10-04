#!/usr/bin/env python3
######################
#Kaizen Towfiq

import getData as gd
import requests
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
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve # ROC Curves
from sklearn.metrics import auc # Calculating AUC for ROC's!
import plotly.plotly as py
import plotly.graph_objs as go


def predictCategoryRF(training_set, test_set,  target, test_targert, componentsList, estimators):
	classifier = RandomForestClassifier(max_features=None, n_estimators=estimators)
	classifier.fit(training_set[componentsList], target)
	return test_set, classifier.predict(test_set[componentsList]), test_targert, classifier.score(test_set[componentsList], test_targert)


categories = ['Jazz', 'Metal'] #'Hip-Hop', 'Metal', 'Electronic/Dance', 'Pop', 'Indie']
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

testdf, predictions, correctValues, score = predictCategoryRF(training_set, test_set, target, test_target, allFeatures, 9001)

print(pd.crosstab(predictions, correctValues,
                  rownames=['Predicted Values'],
                  colnames=['Actual Values']))

print("Score: " + str(score))
