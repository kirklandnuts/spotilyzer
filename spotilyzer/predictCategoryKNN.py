#!/usr/bin/env python3
######################

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
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

style.use("ggplot")

#20 different colors for graphing
COLORS = itertools.cycle(["#f4c242", "#61a323", "#161efc", "#cc37c7", 
			"#ff0000", "#f6ff05", "#000000", "#706c6c",
			"#7200ff", "#4d8e82", "#c1fff3", "#7a89e8",
			"#82689b", "b", "g", "r", "c", "m", "y", "w",])

def graph3DAllNodes(df, features):
	if len(features) == 3:
		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')
		
		xs = df[features[0]]
		ys = df[features[1]]
		zs = df[features[2]]
		ax.scatter(xs, ys, zs, c='g', marker='o')
		
		
		ax.set_xlabel(features[0])
		ax.set_ylabel(features[1])
		ax.set_zlabel(features[2])
		plt.show()
	else:
		print("need 3 features to do 3D graph")

def graph2DAllNodes(df, features):
	if len(features) == 2:
		
		xs = df[features[0]]
		ys = df[features[1]]
		plt.scatter(xs, ys, c='g', marker='o')
		
		
		plt.xlabel = features[0]
		plt.ylabel = features[1]
		plt.show()
	else:
		print("need 2 features to do 3D graph")

def graph2DCategoriesDifferentColors(df, features, categories):
	if len(features) == 2:
		for i in list(range(0,len(categories))):
			pdf = df[df["category"] == categories[i]]
			xs = pdf[features[0]]
			ys = pdf[features[1]]
			plt.scatter(xs, ys, color=next(COLORS), marker='o')
		plt.xlabel = features[0]
		plt.ylabel = features[1]
		plt.show()
	else:
		print("need 2 features to do 3D graph")

def graph3DCategoriesDifferentColors(df, features, categories):
	if len(features) == 3:
		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')
		for i in list(range(0,len(categories))):
			pdf = df[df["category"] == categories[i]]
			xs = pdf[features[0]]
			ys = pdf[features[1]]
			zs = pdf[features[2]]
			ax.scatter(xs, ys, zs, c=next(COLORS), marker='o')
		
		ax.set_xlabel(features[0])
		ax.set_ylabel(features[1])
		ax.set_zlabel(features[2])
		plt.show()
	else:
		print("need 3 features to do 3D graph")

def PCAOnDataFrame(df, features, components):
	pca = PCA(n_components=components)
	pca.fit(df[features])
	newData = pca.transform(df[features])
	preFrameDict = {}
	preFrameDict["songid"] = []
	preFrameDict["category"] = []
	for i in list(range(1,components+1)):
		preFrameDict[str(i)] = []
	for i in list(range(0, len(newData))):
		preFrameDict["songid"].append(df.index.tolist()[i])
		preFrameDict["category"].append(df["category"][i])
		for j in list(range(0,components)):
			preFrameDict[str(j+1)].append(newData[i][j])
	newDataFrame = pd.DataFrame(preFrameDict)	
	return newDataFrame.set_index("songid")

def createCategoriesDataFrame(categories, features):
	preFrameDict = {}
	for i in features:
		preFrameDict[i] = []
	preFrameDict["songid"] = []
	preFrameDict["category"] = []
	for i in categories:
		songs = gd.getSongsInCategory(i)
		for j in songs:
			preFrameDict["category"].append(i)
			preFrameDict["songid"].append(j["songid"])
			for q in features:
				preFrameDict[q].append(j[q])
	df = pd.DataFrame(preFrameDict)
	#normalize data
	for feature in features:
		std_scale = preprocessing.StandardScaler().fit(df[feature])
		df[feature] = pd.DataFrame(std_scale.transform(df[feature]))
	return df.set_index("songid")

def predictCategoryKNN(sid, df, componentsList):
	classifier = KNeighborsClassifier(n_neighbors=500, metric='minkowski')
	train, test = train_test_split(df, test_size = 0.2)
	target = train['category']
	classifier.fit(train[componentsList], target)
	return test, classifier.predict(test[componentsList]), classifier.score(test[componentsList], test['category'])

categories = ["Jazz", "Rock", "Chill"] 
allFeatures = ["popularity", "danceability", "energy", "key", "loudness", "speechiness", "acousticness",
				 "instrumentalness", "liveness", "valence", "tempo", "time_signature"]

cdf = createCategoriesDataFrame(categories, allFeatures)
#pcadf = PCAOnDataFrame(cdf, allFeatures, 2)
#graph2DCategoriesDifferentColors(pcadf, ['1','2'], categories)
pcadf = PCAOnDataFrame(cdf, allFeatures, 3)
#graph3DCategoriesDifferentColors(pcadf, ['1','2', '3'], categories)
sid = pcadf.index.tolist()[7]
testdf, predictions, score = predictCategoryKNN(sid, pcadf, ['1', '2', '3'])
correct = 0
wrong = 0
for i in list(range(0, len(predictions))):
	if testdf['category'].tolist()[i] == predictions[i]:
		correct += 1
	else:
		wrong += 1
	#print(testdf['category'].tolist()[i] + "	" + predictions[i])
import pdb
pdb.set_trace()
