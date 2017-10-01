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
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve # ROC Curves
from sklearn.metrics import auc # Calculating AUC for ROC's!
import plotly.plotly as py
import plotly.graph_objs as go

style.use("ggplot")

#20 different colors for graphing
#COLORS = itertools.cycle(["#f4c242", "#61a323", "#161efc", "#cc37c7", 
#			"#ff0000", "#f6ff05", "#000000", "#706c6c",
#			"#7200ff", "#4d8e82", "#c1fff3", "#7a89e8",
#			"#82689b", "b", "g", "r", "c", "m", "y", "w",])
COLORS = itertools.cycle(["b", "g"])

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
		
		plt.xlabel(features[0])
		plt.ylabel(features[1])
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
		plt.xlabel(features[0])
		plt.ylabel(features[1])
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

def graph3DPlotlyCategoriesDifferentColors(df, features, categories):
	if len(features) == 3:
		traces = []
		for i in list(range(0,len(categories))):
			pdf = df[df["category"] == categories[i]]
			x = pdf[features[0]]
			y = pdf[features[1]]
			z = pdf[features[2]]
			traces.append(go.Scatter3d(
			    x=x,
			    y=y,
			    z=z,
				name=categories[i],
			    mode='markers',
			    marker=dict(
			        size=12,
			        line=dict(
			            color='rgba(217, 217, 217, 0.14)',
			            width=0.5
			        ),
			        opacity=0.8
			    )
			))
		data = traces
		layout = go.Layout(
		    margin=dict(
		        l=0,
		        r=0,
		        b=0,
		        t=0
		    )
		)
		fig = go.Figure(data=data, layout=layout)
	else:
		print("need 3 features to do 3D graph")

def graph2DPlotlyCategoriesDifferentColors(df, features, categories):
	if len(features) == 2:
		traces = []
		for i in list(range(0,len(categories))):
			pdf = df[df["category"] == categories[i]]
			x = pdf[features[0]]
			y = pdf[features[1]]
			traces.append(go.Scatter(
			    x=x,
			    y=y,
				name=categories[i],
			    mode='markers',
			    marker=dict(
			        size=12,
			        line=dict(
			            color='rgba(217, 217, 217, 0.14)',
			            width=0.5
			        ),
			        opacity=0.8
			    )
			))
		data = traces
		layout = go.Layout(
		    margin=dict(
		        l=0,
		        r=0,
		        b=0,
		        t=0
		    )
		)
		fig = go.Figure(data=data, layout=layout)
	else:
		print("need 2 features to do 2D graph")

def PCAOnDataFrame(training_set, test_set, features, components):
	pca = PCA(n_components=components, random_state=7)
	pca.fit(training_set[features])
	training_set_pca = pca.fit_transform(training_set[features])
	components_col = [x for x in range(0, components)]
	training_set = pd.DataFrame(training_set_pca, columns = components_col)

	test_set_pca = pca.transform(test_set[features])
	test_set = pd.DataFrame(test_set_pca, columns = components_col)
	return training_set, test_set, components_col

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
	train, test = train_test_split(df, test_size = 0.2, random_state=7)
	
	std_scale = preprocessing.MinMaxScaler().fit(train[features])
	train_trans = std_scale.fit_transform(train[features])
	training_set = pd.DataFrame(train_trans, columns = features)
	target = train['category']
	test_trans =  std_scale.transform(test[features])
	test_set = pd.DataFrame(test_trans, columns = features)
	test_targert = test['category']
	return df.set_index("songid"), training_set, test_set, target, test_targert

def predictCategoryKNN(training_set, test_set,  target, test_targert, componentsList, k):
	classifier = KNeighborsClassifier(n_neighbors=k, metric='minkowski')
	classifier.fit(training_set[componentsList], target)
	return test_set, classifier.predict(test_set[componentsList]), test_targert, classifier.score(test_set[componentsList], test_targert)

categories = ["Jazz", "Rock"] 
allFeatures = ["popularity", "danceability", "energy", "key", "loudness", "speechiness", "acousticness",
				 "instrumentalness", "liveness", "valence", "tempo", "time_signature"]

cdf, training_set_trans, test_set_trans, target, test_targert = createCategoriesDataFrame(categories, allFeatures)

training_set, test_set, components_col = PCAOnDataFrame(training_set_trans, test_set_trans, allFeatures, 2)

#graph2DPlotlyCategoriesDifferentColors(cdf, ['danceability','acousticness'], categories)
#graph3DPlotlyCategoriesDifferentColors(cdf, ['danceability','acousticness', 'valence'], categories)

#graph2DPlotlyCategoriesDifferentColors(training_set, ['1','2'], categories)
#pcadf, training_set, test_set = PCAOnDataFrame(training_set_trans, test_set_trans, allFeatures, 3)
#graph3DPlotlyCategoriesDifferentColors(pcadf, ['1','2', '3'], categories)

#save to csv
#pcadf.to_csv('demo.csv')
#
##using demo csv
#pcadf = pd.read_csv("demo.csv")
##Test different K values:
#scores = []
#for k in list(range(1,100)):
	#testdf, predictions, score = predictCategoryKNN(training_set, ['1', '2', '3'], k)
	#scores.append(score)
#bestK = scores.index(max(score)) 
#print(bestK)

#testing KNN on pcadf
testdf, predictions, correctValues, score = predictCategoryKNN(training_set, test_set, target, test_targert, components_col, 83)


#
#out_csv = pd.concat([cv_df, pd_df])
#
#import pdb
#pdb.set_trace()

#out_csv.to_csv('test.csv')

print(pd.crosstab(predictions, correctValues,
                  rownames=['Predicted Values'],
                  colnames=['Actual Values']))

print("Score: " + str(score))

cv_df = pd.DataFrame(correctValues)
#
pd_df = pd.DataFrame(predictions)

pred_bin = pd_df[0] .map({'Jazz':1, 'Rock':0})

corr_bin = cv_df['category'].map({'Jazz':1, 'Rock':0})


fpr3, tpr3, _ = roc_curve(pred_bin, corr_bin)
auc_knn = auc(fpr3, tpr3)

f, ax = plt.subplots(figsize=(11, 11))
	

plt.plot(fpr3, tpr3,label='KNN ROC Curve (area = {0: .3f})'\
    .format(auc_knn), 
         color = 'purple', 
         linestyle=':', 
         linewidth=3)

ax.set_facecolor('#fafafa')
plt.plot([0, 1], [0, 1], 'k--', lw=2)
plt.plot([0, 0], [1, 0], 'k--', lw=2, color = 'black')
plt.plot([1, 0], [1, 1], 'k--', lw=2, color = 'black')
plt.xlim([-0.01, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve Comparison For All Models')
plt.legend(loc="lower right")

plt.show()