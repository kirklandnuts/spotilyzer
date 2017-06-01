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
	std_scale = preprocessing.StandardScaler().fit(df[features])
	df_std = std_scale.transform(df[features])
	import pdb
	pdb.set_trace()
	return df.set_index("songid")

categories = ["Jazz", "Rock", "Chill", "Pop", "Mood"] 
allFeatures = ["popularity", "danceability", "energy", "key", "loudness", "speechiness", "acousticness",
				 "instrumentalness", "liveness", "valence", "tempo", "time_signature"]

cdf = createCategoriesDataFrame(categories, allFeatures)
import pdb
pdb.set_trace()

pcadf = PCAOnDataFrame(cdf, allFeatures, 2)
graph2DCategoriesDifferentColors(pcadf, ['1','2'], categories)
pcadf = PCAOnDataFrame(cdf, allFeatures, 3)
graph3DCategoriesDifferentColors(pcadf, ['1','2', '3'], categories)
