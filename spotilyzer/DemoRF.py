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

allFeatures = ["popularity", "danceability", "energy", "key", "loudness", "speechiness", "acousticness",
				 "instrumentalness", "liveness", "valence", "tempo", "time_signature"]


test_set = pd.read_csv('song-data-te.csv')
training_set = pd.read_csv('song-data-tr.csv')
target = training_set['category']
test_target = test_set['category']

testdf, predictions, correctValues, score = predictCategoryRF(training_set, test_set, target, test_target, allFeatures, 1000)

print(pd.crosstab(predictions, correctValues,
                  rownames=['Predicted Values'],
                  colnames=['Actual Values']))

print("Score: " + str(score))
